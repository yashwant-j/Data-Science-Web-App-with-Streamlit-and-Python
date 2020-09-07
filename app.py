import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

DATA_URL = (
"/home/rhyme/Desktop/Project/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collision in New York City")
st.markdown("This application is a streamlit dashboard that can use"
"to analyze motor vehicle collision in NYC")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates =[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset = ['LATITUDE', 'LONGITUDE'], inplace = True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis ='columns',inplace =True)
    data.rename(columns = {'crash_date_crash_time':'date/time'}, inplace= True)
    return data

data = load_data(100000)

st.header("Where are the most people injured in NYC ?")
injured_people = st.slider("Number of persons injured in vehicle collision",0, 19)
st.map(data.query("injured_persons >= @injured_people")[['latitude','longitude']].dropna(how = "any"))


st.header("How many collisions occur during time of day")
hour=st.sidebar.slider("Hour to liik at", 0,23)
data = data[data['date/time'].dt.hour ==hour]


st.header("Vehicle collisions between %i:00 and %i:00" % (hour, (hour +1) % 24))

midpoint = (np.average(data['latitude'], np.average(data['longitude'])))
st.write(pdk.Deck(
    map_style = 'mapbox://styles/mapbox/light-v9',
    intial_view_state = {
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layer =[
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/time','latitude','longitude']],
        get_position = ['latitude','longitude'],
        radius = 100,
        extruded = True,
        pickable =True,
        elelvation_scale = 4,
        elevation_range = [0,1000],        )
    ]
))




if st.checkbox("Show raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
