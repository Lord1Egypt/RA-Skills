"""IMAP/POP3 mail reader, SMTP outbox and durable notifications."""
import base64, datetime as dt, email, email.policy, email.utils, imaplib, json, mimetypes, os, poplib, re, smtplib, ssl, urllib.parse, urllib.request, uuid
from email.message import EmailMessage
from html.parser import HTMLParser
from pathlib import Path
from core import *

MAX_MESSAGE=8*1024*1024
class TextHTML(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style'): self.skip+=1
        if t in ('br','p','div','li'): self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip: self.parts.append(s)
def parsed(raw):
    if len(raw)>MAX_MESSAGE: raise ValueError('Message exceeds 8 MiB')
    m=email.message_from_bytes(raw,policy=email.policy.default); text=[]; html=[]; attachments=[]
    for i,p in enumerate(m.walk()):
        if p.is_multipart(): continue
        b=p.get_payload(decode=True) or b''; fn=p.get_filename()
        if fn or p.get_content_disposition()=='attachment':
            attachments.append({'part':i,'name':str(fn or 'attachment.bin'),'bytes':len(b),'sha256':digest(b)}); continue
        if p.get_content_type() in ('text/plain','text/html'):
            try: t=b.decode(p.get_content_charset() or 'utf-8',errors='replace')
            except LookupError: t=b.decode('utf-8',errors='replace')
            (text if p.get_content_type()=='text/plain' else html).append(t)
    if not text:
        h=TextHTML(); h.feed('\n'.join(html)); text=[''.join(h.parts)]
    return {'subject':str(m.get('Subject','')),'from':str(m.get('From','')),'to':str(m.get('To','')),'date':str(m.get('Date','')),'messageId':str(m.get('Message-ID','')),'inReplyTo':str(m.get('In-Reply-To','')),'text':'\n'.join(text)[:200000],'attachments':attachments}
def addresses(values):
    if not isinstance(values,list): raise ValueError('Recipients must be a list of email addresses')
    out=[]
    for v in values:
        if '\r' in v or '\n' in v: raise ValueError('Header newline rejected')
        _,a=email.utils.parseaddr(v)
        if a!=v or not re.fullmatch(r'[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+',a) or not a.isascii(): raise ValueError('Use plain ASCII mailbox addresses')
        out.append(a)
    if len(out)>100: raise ValueError('Maximum 100 recipients')
    return out
def profile(r):
    c=privateconfig(r['profile']); ident(c['account']); addresses([c['username']])
    for protocol in ('incoming','smtp'):
        if protocol not in c: continue
        p=c[protocol]
        if p.get('security') not in ('ssl','starttls'): raise ValueError('Use SSL or STARTTLS')
        if not isinstance(p['host'],str) or any(x in p['host'] for x in '/@\r\n'): raise ValueError('Invalid mail server')
        bounded(p['port'],1,65535)
    return c
def token(c):
    auth=c.get('auth','password')
    if auth=='password': return secret(c)
    if auth!='oauth2': raise ValueError('auth must be password or oauth2')
    if c.get('accessTokenEnv') and os.environ.get(c['accessTokenEnv']): return secret(c,'accessTokenEnv')
    o=c['oauth']; provider=o['provider']
    if provider=='google': endpoint='https://oauth2.googleapis.com/token'
    elif provider=='microsoft':
        tenant=o.get('tenant','common')
        if not re.fullmatch(r'[A-Za-z0-9-]+',tenant): raise ValueError('Invalid OAuth tenant')
        endpoint='https://login.microsoftonline.com/'+tenant+'/oauth2/v2.0/token'
    else: raise ValueError('OAuth refresh provider must be google or microsoft')
    rotating=Path(o['rotatedTokenFile']).expanduser() if o.get('rotatedTokenFile') else None
    refresh=rotating.read_text(encoding='utf8').strip() if rotating and rotating.exists() else secret(o,'refreshTokenEnv')
    fields={'grant_type':'refresh_token','client_id':o['clientId'],'refresh_token':refresh}
    if o.get('clientSecretEnv'): fields['client_secret']=secret(o,'clientSecretEnv')
    if o.get('scope'): fields['scope']=o['scope']
    req=urllib.request.Request(endpoint,urllib.parse.urlencode(fields).encode())
    with urllib.request.urlopen(req,timeout=25) as res: data=json.loads(res.read(1024*1024))
    # Rotating refresh tokens must be retained outside the Skill package.
    if data.get('refresh_token') and data['refresh_token']!=fields['refresh_token']:
        target=o.get('rotatedTokenFile')
        if not target: raise ValueError('OAuth requires rotatedTokenFile for refresh token rotation')
        atomic(Path(target).expanduser(),data['refresh_token'].encode())
    return data['access_token']
def xoauth(c,t): return ('user='+c['username']+'\x01auth=Bearer '+t+'\x01\x01').encode()
def connect(c,which):
    p=c[which]; ctx=ssl.create_default_context(); t=token(c)
    if which=='smtp':
        s=(smtplib.SMTP_SSL(p['host'],p['port'],timeout=25,context=ctx) if p['security']=='ssl' else smtplib.SMTP(p['host'],p['port'],timeout=25))
        s.ehlo()
        if p['security']=='starttls': s.starttls(context=ctx); s.ehlo()
        if c.get('auth')=='oauth2':
            code,_=s.docmd('AUTH','XOAUTH2 '+base64.b64encode(xoauth(c,t)).decode())
            if code!=235: s.close(); raise ValueError('SMTP OAuth authentication failed')
        else: s.login(c['username'],t)
    elif p.get('protocol','imap')=='imap':
        s=(imaplib.IMAP4_SSL(p['host'],p['port'],ssl_context=ctx,timeout=25) if p['security']=='ssl' else imaplib.IMAP4(p['host'],p['port'],timeout=25))
        if p['security']=='starttls': s.starttls(ssl_context=ctx)
        if c.get('auth')=='oauth2': s.authenticate('XOAUTH2',lambda _:xoauth(c,t))
        else: s.login(c['username'],t)
        if 'ID' in s.capabilities or b'ID' in s.capabilities:
            # NetEase may require an RFC 2971 client ID. No credentials in ID.
            imaplib.Commands.setdefault('ID',('AUTH','SELECTED')); s._simple_command('ID','("name" "MochiLab Email Desk" "version" "1.0.0")')
    else:
        s=(poplib.POP3_SSL(p['host'],p['port'],timeout=25,context=ctx) if p['security']=='ssl' else poplib.POP3(p['host'],p['port'],timeout=25))
        if p['security']=='starttls': s.stls(context=ctx)
        if c.get('auth')=='oauth2':
            s._shortcmd('AUTH XOAUTH2 '+base64.b64encode(xoauth(c,t)).decode())
        else: s.user(c['username']); s.pass_(t)
    return s
def close(s,protocol):
    try: s.logout() if protocol=='imap' else s.quit()
    except Exception:
        try: s.close()
        except Exception: pass
def mailbox(v):
    if not isinstance(v,str) or not v or len(v)>300 or any(ord(x)<32 for x in v): raise ValueError('Invalid mailbox')
    try: v.encode('ascii')
    except UnicodeEncodeError: raise ValueError('Use server IMAP modified-UTF7 mailbox name from folders')
    return '"'+v.replace('\\','\\\\').replace('"','\\"')+'"'
def ingest(st,c,folder,valid,uid,raw,notify):
    id=digest((c['account']+'\0'+folder+'\0'+valid+'\0'+uid).encode())
    file=st.home/'messages'/(id+'.eml'); atomic(file,raw)
    data={'id':id,'account':c['account'],'folder':folder,'uid':uid,'uidValidity':valid,**parsed(raw)}
    st.put('message',id,data)
    if notify: st.notice('mail:'+id,{'type':'new-mail','account':c['account'],'messageId':id,'from':data['from'],'subject':data['subject']})
    return data
def sync(st,r,c):
    limit=bounded(r.get('limit',50),1,200); folder=r.get('folder','INBOX'); proto=c['incoming'].get('protocol','imap'); s=connect(c,'incoming'); fetched=[]
    key=c['account']+'|'+folder+'|'+proto
    cursor=st.get('cursor',key); initialize=cursor is None
    try:
        if proto=='imap':
            code,_=s.select(mailbox(folder),readonly=True)
            if code!='OK': raise ValueError('Cannot select mailbox')
            response=s.response('UIDVALIDITY')[1]; valid=(response[0] or b'0').decode()
            if valid=='0': raise ValueError('Server did not supply UIDVALIDITY')
            code,data=s.uid('search',None,'ALL')
            if code!='OK': raise ValueError('IMAP UID search failed')
            ids=[x.decode() for x in data[0].split()]
            reset=cursor is not None and cursor.get('valid')!=valid; initialize=initialize or reset
            seen=set(cursor['seen']) if cursor and not reset else set()
            targets=ids[-limit:] if initialize else [u for u in ids if u not in seen][:limit]
            if initialize:
                cursor={'valid':valid,'seen':ids}; st.put('cursor',key,cursor)
            for uid in targets:
                code,size=s.uid('fetch',uid,'(RFC822.SIZE)')
                match=re.search(rb'RFC822.SIZE (\d+)',b' '.join(x for x in size if isinstance(x,bytes)))
                if code!='OK' or not match or int(match[1])>MAX_MESSAGE: raise ValueError('Message size unknown or above 8 MiB; narrow mailbox')
                code,data=s.uid('fetch',uid,'(BODY.PEEK[])')
                raw=next((x[1] for x in data if isinstance(x,tuple)),None)
                if code!='OK' or raw is None: raise ValueError('IMAP fetch failed')
                fetched.append(ingest(st,c,folder,valid,uid,raw,not initialize)); seen.add(uid)
                st.put('cursor',key,{'valid':valid,'seen':sorted(set(ids)&(set(cursor['seen']) if initialize else seen))})
        else:
            listing=s.uidl()[1]; pairs=[x.decode().split(None,1) for x in listing]; ids=[x[1] for x in pairs]; valid='pop3'
            seen=set(cursor['seen']) if cursor else set(); targets=pairs[-limit:] if initialize else [x for x in pairs if x[1] not in seen][:limit]
            if initialize: cursor={'valid':valid,'seen':ids}; st.put('cursor',key,cursor)
            for num,uid in targets:
                if int(s.list(int(num)).decode().split()[-1])>MAX_MESSAGE: raise ValueError('POP message exceeds 8 MiB')
                raw=b'\r\n'.join(s.retr(int(num))[1])+b'\r\n'; fetched.append(ingest(st,c,folder,valid,uid,raw,not initialize)); seen.add(uid)
                st.put('cursor',key,{'valid':valid,'seen':ids if initialize else sorted(set(ids)&seen)})
        remain=0 if initialize else len([u for u in ids if u not in seen])
        return {'baselineCreated':initialize,'fetched':len(fetched),'remaining':remain,'messages':fetched,'notifications':st.pending()}
    finally: close(s,proto)
def draft(st,r,c):
    id=ident(r['draftId']); to=addresses(r.get('to',[])); cc=addresses(r.get('cc',[])); bcc=addresses(r.get('bcc',[])); recipients=list(dict.fromkeys(to+cc+bcc))
    if not recipients: raise ValueError('Supply recipients')
    m=EmailMessage(); m['From']=c['username']; m['To']=', '.join(to)
    if cc: m['Cc']=', '.join(cc)
    m['Subject']=r.get('subject',''); m['Message-ID']=email.utils.make_msgid(); m['Date']=email.utils.formatdate(localtime=False)
    if r.get('replyToMessage'):
        original=st.get('message',r['replyToMessage'])
        if not original or original['account']!=c['account']: raise ValueError('Reply source missing or wrong account')
        if original['messageId']: m['In-Reply-To']=original['messageId']; m['References']=original['messageId']
    m.set_content(r.get('body',''))
    total=0
    for rel in r.get('attachments',[]):
        p=local(st.root,rel,True); total+=p.stat().st_size
        if total>6*1024*1024: raise ValueError('Attachments exceed 6 MiB total')
        typ=(mimetypes.guess_type(p.name)[0] or 'application/octet-stream').split('/')
        m.add_attachment(p.read_bytes(),maintype=typ[0],subtype=typ[1],filename=p.name)
    raw=m.as_bytes(policy=email.policy.SMTP)
    if len(raw)>MAX_MESSAGE: raise ValueError('Encoded draft exceeds 8 MiB')
    if st.get('draft',id): raise ValueError('Draft ID exists; use a new ID for a revision')
    atomic(st.home/'drafts'/(id+'.eml'),raw)
    return st.put('draft',id,{'id':id,'account':c['account'],'from':c['username'],'to':to,'cc':cc,'bcc':bcc,'recipients':recipients,'subject':str(m['Subject']),'messageId':str(m['Message-ID']),'sha256':digest(raw),'state':'prepared','preview':parsed(raw)})
def send(st,r,c):
    id=ident(r['draftId']); d=st.get('draft',id)
    if not d or d['account']!=c['account'] or d['from']!=c['username']: raise ValueError('Draft/account mismatch')
    if d['state']=='sent': return d
    if d['state']!='prepared': raise ValueError('Delivery outcome uncertain; inspect Sent mailbox before preparing a new draft')
    if r.get('sha256')!=d['sha256']: raise ValueError('Send requires the reviewed draft hash')
    raw=(st.home/'drafts'/(id+'.eml')).read_bytes()
    if digest(raw)!=d['sha256']: raise ValueError('Draft bytes changed')
    # Atomic claim: concurrent workers cannot both send the same draft.
    st.db.execute('BEGIN IMMEDIATE')
    current=json.loads(st.db.execute('SELECT data FROM objects WHERE kind=? AND id=?',('draft',id)).fetchone()[0])
    if current['state']!='prepared': st.db.rollback(); raise ValueError('Draft already claimed')
    current['state']='sending'; st.db.execute('UPDATE objects SET data=? WHERE kind=? AND id=?',(json.dumps(current),'draft',id)); st.db.commit()
    s=None
    try:
        s=connect(c,'smtp'); refused=s.sendmail(d['from'],d['recipients'],raw)
        d.update(state='sent',sentAt=stamp(),refusedRecipients=list(refused)); st.put('draft',id,d); return d
    except Exception:
        d['state']='uncertain'; st.put('draft',id,d); raise
    finally:
        if s: close(s,'smtp')
def handle(st,r):
    action=r['action']
    if action=='notifications': return st.pending()
    if action=='ack': return st.ack(r['noticeIds'])
    if action=='search':
        q=r.get('query','').casefold(); rows=st.all('message')
        return {'scope':'locally synced messages','messages':[m for m in rows if (not r.get('account') or m['account']==r['account']) and q in '\n'.join(str(m.get(k,'')) for k in ('subject','from','to','text')).casefold()][:bounded(r.get('limit',50),1,500)]}
    if action in ('read','attachments'):
        id=r['messageId']; m=st.get('message',id)
        if not m: raise ValueError('Message missing; sync first')
        if action=='read': return m
        raw=(st.home/'messages'/(ident(id)+'.eml')).read_bytes(); msg=email.message_from_bytes(raw,policy=email.policy.default); out=[]
        for a in m['attachments']:
            name=a['name']
            if any(x in name for x in '/\\:<>"|?*') or name.endswith(('.',' ')) or name in ('.','..') or name.split('.')[0].upper() in ('CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]) or any(ord(x)<32 for x in name): raise ValueError('Unsafe attachment filename')
            dest=local(st.root,r.get('output','exports/mail')+'/'+id+'/'+str(a['part'])+'-'+name)
            b=list(msg.walk())[a['part']].get_payload(decode=True) or b''
            if dest.exists() and digest(dest.read_bytes())!=digest(b): raise ValueError('Attachment output conflict')
            atomic(dest,b); out.append(str(dest))
        return {'files':out}
    c=profile(r)
    if action=='sync': return sync(st,r,c)
    if action=='prepare': return draft(st,r,c)
    if action=='send': return send(st,r,c)
    if action in ('folders','flag','remote-search','fetch'):
        if c['incoming'].get('protocol','imap')!='imap': raise ValueError('Folders and flags require IMAP')
        s=connect(c,'incoming')
        try:
            if action=='folders':
                code,data=s.list(); return {'status':code,'folders':[x.decode('ascii','replace') for x in data if x]}
            if action in ('remote-search','fetch'):
                folder=r.get('folder','INBOX'); code,_=s.select(mailbox(folder),readonly=True)
                if code!='OK': raise ValueError('Mailbox select failed')
                valid=(s.response('UIDVALIDITY')[1][0] or b'').decode()
                if not valid: raise ValueError('Missing UIDVALIDITY')
                if action=='remote-search':
                    field=r.get('field','TEXT').upper()
                    if field not in ('TEXT','SUBJECT','FROM','TO','BODY'): raise ValueError('Search field TEXT, SUBJECT, FROM, TO or BODY')
                    query=r['query']
                    if not isinstance(query,str) or not 1<=len(query)<=1000: raise ValueError('Search query 1..1000 characters')
                    s.literal=query.encode('utf8'); code,data=s.uid('SEARCH','CHARSET','UTF-8',field)
                    if code!='OK': raise ValueError('Server UTF-8 search failed; use local cache search or provider web search')
                    ids=[x.decode() for x in data[0].split()]; limit=bounded(r.get('limit',50),1,500)
                    return {'folder':folder,'uidValidity':valid,'total':len(ids),'uids':ids[-limit:],'limited':len(ids)>limit,'scope':'server mailbox'}
                uid=str(r['uid'])
                if not uid.isdigit() or valid!=str(r['uidValidity']): raise ValueError('UID or UIDVALIDITY mismatch')
                code,size=s.uid('fetch',uid,'(RFC822.SIZE)'); match=re.search(rb'RFC822.SIZE (\d+)',b' '.join(x for x in size if isinstance(x,bytes)))
                if code!='OK' or not match or int(match[1])>MAX_MESSAGE: raise ValueError('Message size unknown or above 8 MiB')
                code,data=s.uid('fetch',uid,'(BODY.PEEK[])'); raw=next((x[1] for x in data if isinstance(x,tuple)),None)
                if code!='OK' or raw is None: raise ValueError('IMAP fetch failed')
                return ingest(st,c,folder,valid,uid,raw,False)
            uid=str(r['uid'])
            if not uid.isdigit(): raise ValueError('UID must be numeric')
            flag=r.get('flag','seen')
            flags={'seen':'\\Seen','unseen':'\\Seen','starred':'\\Flagged','unstarred':'\\Flagged'}
            if flag not in flags: raise ValueError('Unsupported flag')
            code,_=s.select(mailbox(r.get('folder','INBOX')))
            if code!='OK': raise ValueError('Mailbox select failed')
            valid=(s.response('UIDVALIDITY')[1][0] or b'').decode()
            if valid!=str(r['uidValidity']): raise ValueError('UIDVALIDITY changed; sync again')
            code,_=s.uid('store',uid,'-FLAGS.SILENT' if flag in ('unseen','unstarred') else '+FLAGS.SILENT','('+flags[flag]+')'); return {'status':code}
        finally: close(s,'imap')
    raise ValueError('Unknown email action')

if __name__=='__main__': runmain(handle,'email-desk')
