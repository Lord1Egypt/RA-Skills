from helpers import *
from urllib.parse import urlencode

def summarize(d):
 require(isinstance(d,dict) and isinstance(d.get('daily'),dict),'Invalid provider data');daily=d['daily'];names=['time','temperature_2m_max','temperature_2m_min','precipitation_probability_max','wind_speed_10m_max'];arrays=[daily.get(n) for n in names]
 require(all(isinstance(a,list) for a in arrays) and len({len(a) for a in arrays})==1 and 0<len(arrays[0])<=16,'Forecast arrays must align')
 rows=[]
 for vals in zip(*arrays):
  day,high,low,rain,wind=vals;dt.date.fromisoformat(day)
  require(all(x is None or isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in [high,low,rain,wind]),'Invalid weather value')
  require(rain is None or 0<=rain<=100,'Invalid rain probability')
  rows.append(dict(zip(names,vals)))
 return {'timezone':d.get('timezone'),'units':d.get('daily_units',{}),'forecast':rows,'provider':'Open-Meteo','attribution':'Weather data by Open-Meteo (https://open-meteo.com/)','warning':'Forecast, not an official severe-weather alert.'}

def handle(s,r):
 if r.get('action')=='import':d=readjson(local(s.root,r['file'],'file'));mode='imported-provider-response'
 elif r.get('action')=='fetch':
  require(r.get('network') is True,'Network request needs explicit network=true for the user-selected place')
  lat=r.get('latitude');lon=r.get('longitude');require(all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in [lat,lon]) and -90<=lat<=90 and -180<=lon<=180,'Invalid coordinates')
  q=urlencode({'latitude':lat,'longitude':lon,'daily':'temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max','timezone':'auto','forecast_days':limit(r.get('days',3),1,7)})
  response=safe_request('https://api.open-meteo.com/v1/forecast?'+q,max_bytes=1024*1024);require(response['status']==200,'Weather provider returned an error');d=json.loads(response['body']);mode='live-provider-response'
 else:raise ValueError('Actions: import, fetch')
 result=summarize(d);result.update(mode=mode,retrievedAt=now());return s.report(result)
