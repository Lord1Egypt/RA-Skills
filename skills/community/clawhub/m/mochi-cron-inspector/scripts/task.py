import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 from zoneinfo import ZoneInfo
 fields=r['expression'].split();need(len(fields)==5,'Use a five-field cron expression')
 def parse(s,lo,hi):
  values=set()
  for term in s.split(','):
   pieces=term.split('/');need(len(pieces)<=2,'Invalid cron step');step=int(pieces[1]) if len(pieces)==2 else 1;need(step>0,'Cron step must be positive');span=pieces[0]
   need(len(pieces)==1 or span=='*' or '-' in span,'Steps require a wildcard or range');a,b=(lo,hi) if span=='*' else tuple(map(int,span.split('-'))) if '-' in span else (int(span),int(span));need(lo<=a<=b<=hi,'Cron value out of range');values.update(range(a,b+1,step))
  return values
 mins,hours,days,months,weekdays=[parse(s,*bounds) for s,bounds in zip(fields,[(0,59),(0,23),(1,31),(1,12),(0,7)])];weekdays={d%7 for d in weekdays};zone=ZoneInfo(r['timezone']);start=instant(r['after']).astimezone(dt.timezone.utc).replace(second=0,microsecond=0)+dt.timedelta(minutes=1);count=int(r.get('count',3));need(1<=count<=20,'count must be1..20');found=[]
 for i in range(366*24*60):
  v=(start+dt.timedelta(minutes=i)).astimezone(zone);dom=v.day in days;dow=(v.weekday()+1)%7 in weekdays
  day=(dom and dow) if fields[2].startswith('*') or fields[4].startswith('*') else (dom or dow)
  if v.minute in mins and v.hour in hours and v.month in months and day:found.append(v.isoformat())
  if len(found)==count:break
 return {'nextRuns':found,'timezone':r['timezone'],'systemCronModified':False,'searchHorizonDays':366}
