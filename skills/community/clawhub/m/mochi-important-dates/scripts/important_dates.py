"""Private anniversaries, lunar birthdays and source-labelled holiday calendars."""
import calendar, csv, datetime as dt, io, uuid
from zoneinfo import ZoneInfo
from core import *

def wall(day,time,zone):
    naive=dt.datetime.combine(day,dt.time.fromisoformat(time)); z=ZoneInfo(zone)
    # First occurrence for an ambiguous wall time; advance through a DST gap.
    for offset in range(181):
        n=naive+dt.timedelta(minutes=offset); v=n.replace(tzinfo=z,fold=0)
        if v.astimezone(UTC).astimezone(z).replace(tzinfo=None)==n: return v
    raise ValueError('Unable to resolve reminder local time')
def occurrence(e,year):
    if e.get('calendar','gregorian')=='lunar':
        from lunar_python import Lunar
        month=int(e['month']); leap=e.get('leapMonth',False)
        if leap:
            from lunar_python import LunarYear
            has=LunarYear.fromYear(year).getLeapMonth()==month
            if not has and e.get('leapPolicy','skip')=='skip': return None
            month=-month if has else month
        from lunar_python import LunarMonth
        day=int(e['day']); last=LunarMonth.fromYm(year,month).getDayCount()
        if day>last:
            if e.get('lunarShortMonth','lastday')=='skip': return None
            day=last
        solar=Lunar.fromYmd(year,month,day).getSolar()
        return dt.date(solar.getYear(),solar.getMonth(),solar.getDay())
    month=int(e['month']); day=int(e['day'])
    if month==2 and day==29 and not calendar.isleap(year):
        policy=e.get('feb29','feb28')
        if policy=='skip': return None
        return dt.date(year,3,1) if policy=='mar1' else dt.date(year,2,28)
    return dt.date(year,month,day)
def validate(e):
    ident(e['id']); e=dict(e); e['title']=str(e['title']).strip()
    if not e['title'] or len(e['title'])>300: raise ValueError('Event title required, <=300 characters')
    ZoneInfo(e.get('timezone','Asia/Shanghai')); dt.time.fromisoformat(e.get('time','09:00'))
    if e.get('calendar','gregorian') not in ('gregorian','lunar'): raise ValueError('Unknown calendar')
    bounded(e['month'],1,12); bounded(e['day'],1,31)
    if e.get('calendar')=='lunar' and int(e['day'])>30: raise ValueError('Lunar day <=30')
    if e.get('feb29','feb28') not in ('feb28','mar1','skip'): raise ValueError('Invalid Feb 29 policy')
    if e.get('leapPolicy','skip') not in ('skip','regular'): raise ValueError('Invalid leap-month policy')
    if e.get('lunarShortMonth','lastday') not in ('lastday','skip'): raise ValueError('Invalid lunar short-month policy')
    offsets=e.get('advanceDays',[7,1,0])
    if not isinstance(offsets,list) or not offsets or len(offsets)>20: raise ValueError('Use 1..20 advance offsets')
    e['advanceDays']=sorted(set(bounded(x,0,365) for x in offsets),reverse=True)
    if e.get('year'): bounded(e['year'],1900,2200)
    if e.get('onDate'): dt.date.fromisoformat(e['onDate'])
    if e.get('calendar')!='lunar': occurrence(e,2000)
    return e
def occurrences(e,start,end):
    if e.get('onDate'):
        d=dt.date.fromisoformat(e['onDate']); return [d] if start<=d<=end else []
    result=[]
    for year in range(start.year-1,end.year+2):
        if e.get('year') and year<int(e['year']): continue
        d=occurrence(e,year)
        if d and start<=d<=end: result.append(d)
    return sorted(set(result))
def handle(st,r):
    action=r['action']
    if action=='put':
        e=validate(r['event']); old=st.get('event',e['id']); e['revision']=old.get('revision',1) if old else 1
        if old:
            before={k:v for k,v in old.items() if k!='revision'}
            if before!={k:v for k,v in e.items() if k!='revision'}: e['revision']+=1
        if old and e['revision']!=old.get('revision',1):
            for n in st.pending():
                if n.get('eventId')==e['id']: st.ack([n['noticeId']])
        return st.put('event',e['id'],e)
    if action=='list': return st.all('event')
    if action=='remove':
        st.delete('event',r['id'])
        for n in st.pending():
            if n.get('eventId')==r['id']: st.ack([n['noticeId']])
        return {'removed':r['id']}
    if action=='ack': return st.ack(r['noticeIds'])
    if action=='notifications': return st.pending()
    if action=='import-holidays':
        data=readjson(local(st.root,r['file'],True)); source=data['source']; country=data['country']; year=bounded(data['year'],1900,2200)
        if not source.startswith('https://') or not country: raise ValueError('Holiday import needs HTTPS source and country/region')
        events=[]
        for h in data['days']:
            d=dt.date.fromisoformat(h['date'])
            if d.year!=year: raise ValueError('Holiday date/year mismatch')
            if h.get('type','holiday') not in ('holiday','workday','observance'): raise ValueError('Invalid holiday day type')
            id='holiday-'+digest((country+'|'+str(d)+'|'+h.get('type','holiday')).encode())[:24]
            e=validate({'id':id,'title':h['name'],'kind':h.get('type','holiday'),'month':d.month,'day':d.day,'onDate':str(d),'country':country,'source':source,'timezone':data.get('timezone','Asia/Shanghai'),'advanceDays':r.get('advanceDays',[1,0]),'time':r.get('time','09:00')}); events.append(e)
        for e in events: handle(st,{'action':'put','event':e})
        return {'imported':len(events),'country':country,'year':year,'source':source}
    if action=='upcoming':
        start=dt.date.fromisoformat(r['from']); end=start+dt.timedelta(days=bounded(r.get('days',90),1,730)); out=[]
        for e in st.all('event'):
            for d in occurrences(e,start,end):
                item={'date':str(d),'daysAway':(d-start).days,'event':e}
                if e.get('year') and e.get('calendar')!='lunar': item['years']=d.year-int(e['year'])
                out.append(item)
        return sorted(out,key=lambda x:(x['date'],x['event']['id']))
    if action=='poll':
        now=zoned(r['now']) if r.get('now') else dt.datetime.now(UTC); window=bounded(r.get('catchupHours',48),1,168); since=now-dt.timedelta(hours=window)
        for e in st.all('event'):
            if e.get('enabled',True) is False: continue
            z=e.get('timezone','Asia/Shanghai'); today=now.astimezone(ZoneInfo(z)).date()
            for d in occurrences(e,today-dt.timedelta(days=8),today+dt.timedelta(days=366)):
                for lead in e['advanceDays']:
                    due=wall(d-dt.timedelta(days=lead),e.get('time','09:00'),z)
                    if since<due<=now:
                        id='date:'+e['id']+':'+str(e.get('revision',1))+':'+str(d)+':'+str(lead)
                        st.notice(id,{'eventId':e['id'],'title':e['title'],'date':str(d),'advanceDays':lead,'dueAt':due.isoformat(),'timezone':z,'kind':e.get('kind','anniversary'),'source':e.get('source')})
        return {'notifications':st.pending(),'checkedAt':now.isoformat(),'catchupHours':window}
    if action=='export-ics':
        from icalendar import Calendar,Event
        cal=Calendar(); cal.add('prodid','-//MochiLab//Important Dates//EN'); cal.add('version','2.0'); start=iso_date(r['from']); end=iso_date(r['to'])
        if not 0<=(end-start).days<=730: raise ValueError('Export range <=730 days')
        for e in st.all('event'):
            for d in occurrences(e,start,end):
                v=Event(); v.add('uid',e['id']+'-'+str(d)+'@mochilab.local'); v.add('dtstamp',dt.datetime.now(UTC)); v.add('summary',e['title']); v.add('dtstart',d); v.add('dtend',d+dt.timedelta(days=1)); cal.add_component(v)
        p=local(st.root,r.get('output','exports/important-dates.ics')); atomic(p,cal.to_ical()); return {'file':str(p)}
    raise ValueError('Unknown important-date action')
if __name__=='__main__': runmain(handle,'important-dates')
