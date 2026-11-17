"""ICS recurrence expansion, conflict reports and conditional CalDAV resource edits."""
import datetime as dt, uuid
from core import *
from dav import DAV,xml
def parse(b):
    from icalendar import Calendar
    if len(b)>5*1024*1024: raise ValueError('Calendar exceeds 5 MiB')
    return Calendar.from_ical(b)
def store_calendar(st,b,source):
    cal=parse(b); entries=[]
    for e in cal.walk('VEVENT'):
        uid=str(e.get('UID',''))
        if not uid: raise ValueError('Calendar event lacks UID')
        if not e.get('DTSTART'): raise ValueError('Calendar event lacks DTSTART')
        start=e.decoded('DTSTART'); end=e.decoded('DTEND',None)
        if end is not None:
            try:
                if end<start: raise ValueError('Calendar end precedes start')
            except TypeError: raise ValueError('Calendar start/end date types differ')
        # Store the whole resource, including recurrence overrides and VTIMEZONE.
        entries.append(uid)
    id=digest(source.encode()); atomic(st.home/(id+'.ics'),b); st.put('calendar',id,{'id':id,'source':source,'uids':entries}); return {'events':len(entries),'source':source}
def range_events(st,r):
    import recurring_ical_events
    start=zoned(r['from']); end=zoned(r['to'])
    if not 0<(end-start).total_seconds()<=366*86400: raise ValueError('Calendar range <=366 days')
    out=[]
    for c in st.all('calendar'):
        for e in recurring_ical_events.of(parse((st.home/(c['id']+'.ics')).read_bytes())).between(start,end):
            a=e.decoded('DTSTART'); b=e.decoded('DTEND',None)
            if isinstance(a,dt.date) and not isinstance(a,dt.datetime):
                a=dt.datetime.combine(a,dt.time(),tzinfo=start.tzinfo); b=dt.datetime.combine(b or (a.date()+dt.timedelta(days=1)),dt.time(),tzinfo=start.tzinfo)
            elif a.tzinfo is None: raise ValueError('Floating calendar time: import an explicit timezone first')
            if b is None: b=a+e.decoded('DURATION',dt.timedelta(0))
            if b.tzinfo is None: raise ValueError('Floating calendar end time')
            out.append({'uid':str(e['UID']),'summary':str(e.get('SUMMARY','')),'start':a.isoformat(),'end':b.isoformat(),'source':c['source'],'busy':str(e.get('TRANSP','OPAQUE')).upper()!='TRANSPARENT' and str(e.get('STATUS','')).upper()!='CANCELLED'})
            if len(out)>10000: raise ValueError('Too many recurrence instances; narrow date range')
    return sorted(out,key=lambda e:zoned(e['start']))
def handle(st,r):
    action=r['action']
    if action=='import': return store_calendar(st,local(st.root,r['file'],True).read_bytes(),r['file'])
    if action in ('agenda','conflicts'):
        items=range_events(st,r)
        if action=='agenda': return items
        out=[]
        for i,a in enumerate(items):
            if not a['busy']: continue
            for b in items[i+1:]:
                if zoned(b['start'])>=zoned(a['end']): break
                if b['busy'] and zoned(b['end'])>zoned(a['start']): out.append({'left':a,'right':b})
        return out
    if action=='create':
        from icalendar import Calendar,Event
        a=zoned(r['start']); b=zoned(r['end'])
        if b<=a: raise ValueError('End must follow start')
        cal=Calendar(); cal.add('version','2.0'); cal.add('prodid','-//MochiLab//Calendar Desk//EN'); e=Event(); e.add('uid',r.get('uid',str(uuid.uuid4())+'@mochilab.local')); e.add('dtstamp',dt.datetime.now(UTC)); e.add('dtstart',a); e.add('dtend',b); e.add('summary',r['title'])
        if r.get('description'): e.add('description',r['description'])
        if r.get('location'): e.add('location',r['location'])
        cal.add_component(e); p=local(st.root,r.get('output','exports/event.ics'))
        if p.exists(): raise ValueError('Calendar output already exists')
        atomic(p,cal.to_ical()); return {'file':str(p),'uid':str(e['UID'])}
    d=DAV(r['profile'])
    if action=='remote-list': return d.listing()
    if action=='pull':
        _,h,b=d.request('GET',r['remote']); etag=next((v for k,v in h.items() if k.lower()=='etag'),None)
        return {**store_calendar(st,b,d.base+r['remote']),'etag':etag}
    if action=='push':
        b=local(st.root,r['file'],True).read_bytes(); parse(b)
        headers={'Content-Type':'text/calendar; charset=utf-8',**({'If-Match':r['etag']} if r.get('etag') else {'If-None-Match':'*'})}; status,h,_=d.request('PUT',r['remote'],b,headers)
        return {'status':status,'etag':next((v for k,v in h.items() if k.lower()=='etag'),None)}
    if action=='remote-delete':
        if not r.get('etag'): raise ValueError('Deletion needs current ETag')
        status,_,_=d.request('DELETE',r['remote'],headers={'If-Match':r['etag']}); return {'status':status}
    raise ValueError('Unknown calendar action')
if __name__=='__main__': runmain(handle,'calendar-desk')
