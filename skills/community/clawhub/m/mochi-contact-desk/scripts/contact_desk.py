"""Local contact import, exact-key duplicate review, merge and follow-ups."""
import csv, io, re, uuid
from core import *
def norm(c):
    c=dict(c); c['id']=ident(c.get('id',str(uuid.uuid4()))); c['name']=str(c.get('name','')).strip()
    if not c['name']: raise ValueError('Contact name required')
    for key in ('emails','phones','tags'):
        values=c.get(key,[])
        if isinstance(values,str): values=[x.strip() for x in values.split(';') if x.strip()]
        if not isinstance(values,list): raise ValueError('Contact fields must be lists')
        c[key]=sorted(set(str(x).strip() for x in values if str(x).strip()))
    c['emails']=sorted(set(x.casefold() for x in c['emails']))
    c['phoneKeys']=sorted(set(re.sub(r'[^0-9+]','',x) for x in c['phones']))
    return c
def duplicates(rows):
    pairs=[]
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            emails=set(a['emails'])&set(b['emails']); phones=set(a['phoneKeys'])&set(b['phoneKeys'])
            if emails or phones: pairs.append({'left':a['id'],'right':b['id'],'sharedEmails':sorted(emails),'sharedPhones':sorted(phones)})
    return pairs
def handle(st,r):
    action=r['action']
    if action=='put':
        c=norm(r['contact']); return st.put('contact',c['id'],c)
    if action=='search':
        q=r.get('query','').casefold(); return [c for c in st.all('contact') if q in json.dumps(c,ensure_ascii=False).casefold()]
    if action=='duplicates': return duplicates(st.all('contact'))
    if action=='import':
        p=local(st.root,r['file'],True)
        if p.stat().st_size>5*1024*1024: raise ValueError('Contacts import <=5 MiB')
        rows=[]
        if p.suffix.lower()=='.csv': rows=list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig'))))
        else:
            import vobject
            for v in vobject.readComponents(p.read_text(encoding='utf8')):
                rows.append({'name':str(v.fn.value) if hasattr(v,'fn') else '', 'emails':[str(x.value) for x in v.contents.get('email',[])],'phones':[str(x.value) for x in v.contents.get('tel',[])],'organization':str(v.org.value) if hasattr(v,'org') else ''})
        if len(rows)>2000: raise ValueError('Import <=2000 contacts')
        normalized=[norm({**c,'id':'import-'+digest(json.dumps(c,sort_keys=True,ensure_ascii=False).encode())[:24]}) for c in rows]
        if r.get('apply',False):
            for c in normalized: st.put('contact',c['id'],c)
        return {'applied':bool(r.get('apply',False)),'contacts':normalized,'duplicates':duplicates(st.all('contact')+normalized)[:500]}
    if action=='merge':
        target=ident(r['target']); ids=list(dict.fromkeys([target]+r['sources'])); contacts=[st.get('contact',id) for id in ids]
        if any(c is None for c in contacts): raise ValueError('Merge contact missing')
        merged=dict(contacts[0]); conflicts={}
        for key in ('name','organization','notes'):
            choices=sorted(set(str(c.get(key,'')) for c in contacts if c.get(key)))
            if len(choices)>1 and key not in r.get('choose',{}): conflicts[key]=choices
            elif choices: merged[key]=r.get('choose',{}).get(key,choices[0])
        if conflicts: return {'needsChoice':conflicts,'applied':False}
        for key in ('emails','phones','tags'): merged[key]=sorted(set(v for c in contacts for v in c.get(key,[])))
        merged=norm(merged)
        # One transaction preserves the contact history when merging.
        st.db.execute('BEGIN IMMEDIATE')
        try:
            for note in st.all('followup'):
                if note['contactId'] in ids:
                    note['contactId']=target; st.db.execute('UPDATE objects SET data=? WHERE kind=? AND id=?',(json.dumps(note),'followup',note['id']))
            st.db.execute('INSERT INTO objects VALUES(?,?,?) ON CONFLICT(kind,id) DO UPDATE SET data=excluded.data',('contact',target,json.dumps(merged)))
            for id in ids:
                if id!=target: st.db.execute('DELETE FROM objects WHERE kind=? AND id=?',('contact',id))
            st.db.commit()
        except Exception: st.db.rollback(); raise
        return {'merged':merged}
    if action=='followup':
        if not st.get('contact',r['contactId']): raise ValueError('Contact missing')
        note={'id':ident(r.get('id',str(uuid.uuid4()))),'contactId':r['contactId'],'note':r['note'],'date':str(iso_date(r['date'])),'nextDate':str(iso_date(r['nextDate'])) if r.get('nextDate') else None}; return st.put('followup',note['id'],note)
    if action=='due':
        today=iso_date(r['date']); notes=st.all('followup'); latest={}
        for n in sorted(notes,key=lambda n:(n['date'],n['id'])): latest[n['contactId']]=n
        return [{'contact':st.get('contact',id),'followup':n} for id,n in latest.items() if n.get('nextDate') and iso_date(n['nextDate'])<=today]
    if action=='export':
        fmt=r.get('format','csv'); rows=st.all('contact'); p=local(st.root,r.get('output','exports/contacts.'+('vcf' if fmt=='vcard' else 'csv')))
        if p.exists(): raise ValueError('Export output exists')
        if fmt=='vcard':
            import vobject
            result=''
            for c in rows:
                v=vobject.vCard(); v.add('fn').value=c['name']; v.add('uid').value=c['id']
                for e in c['emails']: v.add('email').value=e
                for phone in c['phones']: v.add('tel').value=phone
                result+=v.serialize()
        elif fmt=='csv':
            buf=io.StringIO(newline=''); w=csv.writer(buf); keys=['id','name','emails','phones','tags','organization']; w.writerow(keys)
            for c in rows:
                vals=[';'.join(c.get(k,[])) if isinstance(c.get(k),list) else str(c.get(k,'')) for k in keys]; w.writerow(["'"+v if v.startswith(('=','+','-','@','\t','\r')) else v for v in vals])
            result=buf.getvalue()
        else: raise ValueError('format csv or vcard')
        atomic(p,result.encode('utf-8-sig' if fmt=='csv' else 'utf8')); return {'file':str(p),'contacts':len(rows)}
    raise ValueError('Unknown contact action')
if __name__=='__main__': runmain(handle,'contact-desk')
