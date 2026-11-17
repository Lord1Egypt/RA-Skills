"""Private local Gmail adapter. Python 3.10+, standard library only."""
import base64
import contextlib
import email.message
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = '0.1.3'
READ = 'https://www.googleapis.com/auth/gmail.readonly'
SEND = 'https://www.googleapis.com/auth/gmail.send'
AUTH = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN = 'https://oauth2.googleapis.com/token'
API = 'https://gmail.googleapis.com/gmail/v1/users/me/'

class Problem(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def request(url, data=None, headers=None, method=None):
    # Do not inherit proxy variables: never route bearer tokens via an arbitrary proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with opener.open(req, timeout=30) as response:
            return json.loads(response.read(4_000_000) or '{}')
    except urllib.error.HTTPError as e:
        # Never expose provider bodies, which can contain submitted secrets or message data.
        if e.code == 400 and url == TOKEN:
            raise Problem('Google authorization failed. Reconnect; check the Desktop client, test user, and consent status.', 401) from None
        raise Problem({401:'Gmail authorization expired. Reconnect your account.',
                       403:'Google denied access. Check Gmail API, consent scopes, and Workspace administrator policy.',
                       404:'Gmail item or history cursor is no longer available.',
                       429:'Google rate limit reached. Try again later.'}.get(e.code, 'Google request failed; retry later.'), e.code) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise Problem('Cannot reach Google securely. Check internet access, system clock, and TLS certificates.', 503) from None

def encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def valid_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', value):
        raise Problem('Invalid message or draft ID.')
    return value

class Store:
    def __init__(self, root=None):
        self.root = Path(root or os.environ.get('GMAIL_CONNECT_HOME', Path.home()/'.local/share/openclaw-gmail-connect')).expanduser()
        if self.root.is_symlink():
            raise Problem('State directory must not be a symlink.')
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)
        self.dbpath = self.root/'mail.sqlite3'
        with self.db() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, data TEXT NOT NULL, created REAL NOT NULL);
              CREATE TABLE IF NOT EXISTS drafts (id TEXT PRIMARY KEY, data TEXT NOT NULL, status TEXT NOT NULL);''')
        os.chmod(self.dbpath, 0o600)

    @contextlib.contextmanager
    def db(self):
        db = sqlite3.connect(self.dbpath, timeout=30)
        try:
            with db:
                yield db
        finally:
            db.close()

    @contextlib.contextmanager
    def lock(self, name):
        p = self.root/(name+'.lock')
        fd = os.open(p, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            yield

    def read(self, name):
        p = self.root/name
        if p.is_symlink():
            raise Problem('Refusing a symlink in private state.')
        return json.loads(p.read_text()) if p.exists() else {}

    def write(self, name, data):
        fd, temporary = tempfile.mkstemp(dir=self.root, prefix='.write-')
        try:
            with os.fdopen(fd, 'w') as f:
                os.fchmod(f.fileno(), 0o600)
                json.dump(data, f)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporary, self.root/name)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def get(self, key, default=None):
        with self.db() as db:
            row = db.execute('SELECT value FROM kv WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def put(self, key, value):
        with self.db() as db:
            db.execute('INSERT OR REPLACE INTO kv VALUES (?,?)', (key, json.dumps(value)))

class Gmail:
    def __init__(self, store):
        self.s = store

    def import_client(self, payload):
        c = payload.get('installed', {})
        if not isinstance(c, dict) or not re.fullmatch(r'[A-Za-z0-9._-]+\.apps\.googleusercontent\.com', str(c.get('client_id',''))):
            raise Problem('Choose the JSON downloaded for a Google OAuth Desktop app, not a Web app or service account.')
        if not isinstance(c.get('client_secret'), str) or not c['client_secret'] or len(c['client_secret']) > 500:
            raise Problem('The Desktop client JSON is missing its client secret.')
        with self.s.lock('auth'):
            old = self.s.read('client.json')
            if old and old.get('client_id') != c['client_id'] and self.s.read('tokens.json'):
                raise Problem('Disconnect before changing the OAuth client.')
            # Ignore all endpoint URLs from uploaded JSON; trust only fixed Google endpoints.
            self.s.write('client.json', {k:c.get(k, '') for k in ('client_id','client_secret','project_id')})
        return {'imported':True, 'project':c.get('project_id','')}

    def begin(self, redirect, sending=False):
        c = self.s.read('client.json')
        if not c:
            raise Problem('Upload your Desktop client JSON first.')
        verifier = secrets.token_urlsafe(64)
        state = secrets.token_urlsafe(32)
        pending = {'state':state,'verifier':verifier,'redirect':redirect,'created':time.time(), 'sending':bool(sending)}
        scopes = [READ] + ([SEND] if sending else [])
        params = {'client_id':c['client_id'],'redirect_uri':redirect,'response_type':'code',
                  'scope':' '.join(scopes),'access_type':'offline','prompt':'consent',
                  'state':state,'code_challenge':encode(hashlib.sha256(verifier.encode()).digest()),'code_challenge_method':'S256'}
        return AUTH+'?'+urllib.parse.urlencode(params), pending

    def finish(self, pending, code, state):
        if not pending or time.time()-pending['created'] > 600 or not secrets.compare_digest(state, pending['state']):
            raise Problem('This authorization link expired or did not match. Start Connect again.')
        with self.s.lock('sync'), self.s.lock('auth'):
            c = self.s.read('client.json')
            data = request(TOKEN, urllib.parse.urlencode({'client_id':c['client_id'],'client_secret':c['client_secret'],
                'grant_type':'authorization_code','code':code,'redirect_uri':pending['redirect'],
                'code_verifier':pending['verifier']}).encode())
            scopes = data.get('scope','').split()
            if READ not in scopes or (pending['sending'] and SEND not in scopes):
                raise Problem('Required permission was not granted. Connect again and allow the selected scopes.')
            if not data.get('refresh_token'):
                raise Problem('Google did not return offline access. Revoke this app in Google Account permissions and reconnect.')
            profile = request(API+'profile', headers={'Authorization':'Bearer '+data['access_token']})
            data['expires_at'] = time.time()+int(data.get('expires_in',3600))-60
            data['email'] = profile['emailAddress']
            previous = self.s.read('tokens.json')
            # Cache must never mix accounts after reconnection.
            if previous.get('email') != data['email']:
                with self.s.db() as db:
                    db.execute('DELETE FROM events'); db.execute('DELETE FROM drafts'); db.execute('DELETE FROM kv')
            self.s.write('tokens.json', data)
        return profile

    def token(self):
        with self.s.lock('auth'):
            t = self.s.read('tokens.json')
            if not t:
                raise Problem('Connect your Gmail account in the setup wizard first.', 401)
            if time.time() >= t.get('expires_at',0):
                c = self.s.read('client.json')
                new = request(TOKEN, urllib.parse.urlencode({'client_id':c['client_id'],
                    'client_secret':c['client_secret'],'refresh_token':t['refresh_token'],'grant_type':'refresh_token'}).encode())
                t.update(new)
                t['expires_at'] = time.time()+int(new.get('expires_in',3600))-60
                self.s.write('tokens.json', t)
            return t['access_token']

    def api(self, path, params=None, body=None):
        url = API+path+('?' + urllib.parse.urlencode(params, doseq=True) if params else '')
        headers = {'Authorization':'Bearer '+self.token()}
        data = None
        if body is not None:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body).encode()
        return request(url, data, headers)

    def search(self, query='in:inbox', limit=20, page=None):
        if not isinstance(query,str) or len(query)>2000:
            raise Problem('Search query is too long.')
        params = {'q':query,'maxResults':max(1,min(int(limit),100))}
        if page:
            params['pageToken']=page
        result = self.api('messages',params)
        return {'messages':[self.message(m['id']) for m in result.get('messages',[])],
                'nextPageToken':result.get('nextPageToken'), 'untrustedEmailContent':True}

    def message(self, mid, full=False):
        raw = self.api('messages/'+valid_id(mid), {'format':'full' if full else 'metadata',
            **({} if full else {'metadataHeaders':['From','To','Subject','Date']})})
        headers = {x['name'].lower():x['value'] for x in raw.get('payload',{}).get('headers',[])}
        out = {'id':mid,'from':headers.get('from',''),'to':headers.get('to',''),
               'subject':headers.get('subject',''),'date':headers.get('date',''), 'labels':raw.get('labelIds',[]),
               'snippet':raw.get('snippet',''), 'untrustedEmailContent':True}
        if full:
            def plain(part):
                if part.get('mimeType')=='text/plain' and part.get('body',{}).get('data'):
                    value=part['body']['data']
                    yield base64.urlsafe_b64decode(value+'='*(-len(value)%4)).decode('utf-8',errors='replace')
                for child in part.get('parts',[]):
                    yield from plain(child)
            out['text']='\n'.join(plain(raw.get('payload',{})))[:100000]
            out['note']='Plain text only. HTML, remote images, and attachments are never executed or fetched.'
        return out

    def sync(self):
        with self.s.lock('sync'):
            cursor = self.s.get('cursor')
            ids = set()
            baseline = cursor is None
            gap = False
            if cursor:
                page = None
                try:
                    while True:
                        params={'startHistoryId':cursor,'historyTypes':['messageAdded','labelAdded'],'maxResults':500}
                        if page: params['pageToken']=page
                        data=self.api('history',params)
                        for record in data.get('history',[]):
                            for change in record.get('messagesAdded',[]):
                                ids.add(change['message']['id'])
                            for change in record.get('labelsAdded',[]):
                                if 'INBOX' in change.get('labelIds',[]):
                                    ids.add(change['message']['id'])
                        page=data.get('nextPageToken')
                        next_cursor=data['historyId']
                        if not page: break
                except Problem as e:
                    if e.status != 404: raise
                    baseline=True; gap=True; ids.clear()
            if baseline:
                # Capture baseline before listing so arrivals during the snapshot are replayed.
                next_cursor=self.api('profile')['historyId']
                recent=self.api('messages',{'q':'in:inbox','maxResults':100})
                ids.update(m['id'] for m in recent.get('messages',[]))
            messages=[]
            for mid in sorted(ids):
                try:
                    msg=self.message(mid)
                    if 'INBOX' in msg['labels']: messages.append(msg)
                except Problem as e:
                    if e.status != 404: raise
            with self.s.db() as db:
                for msg in messages:
                    msg['kind']='snapshot' if baseline else 'arrival'
                    db.execute('INSERT OR IGNORE INTO events VALUES (?,?,?)',(msg['id'],json.dumps(msg),time.time()))
                db.execute('INSERT OR REPLACE INTO kv VALUES (?,?)',('cursor',json.dumps(next_cursor)))
                db.execute('INSERT OR REPLACE INTO kv VALUES (?,?)',('sync',json.dumps({'at':time.time(),'recoveredHistoryGap':gap,
                    'note':'Baseline contains up to 100 recent inbox messages.' if baseline else 'Incremental history sync completed.'})))
                # Bound local cache. Events are a convenience feed, not an archival or guaranteed job queue.
                db.execute('DELETE FROM events WHERE created < ?', (time.time()-30*86400,))
                db.execute('DELETE FROM events WHERE id NOT IN (SELECT id FROM events ORDER BY created DESC LIMIT 5000)')
            return {'checked':True,'messagesObserved':len(messages),'baseline':baseline,'historyGap':gap}

    def events(self, limit=50):
        with self.s.db() as db:
            rows=db.execute('SELECT data FROM events ORDER BY created DESC LIMIT ?', (max(1,min(limit,100)),)).fetchall()
        return {'events':[json.loads(row[0]) for row in rows], 'sync':self.s.get('sync'),
                'note':'Recent feed; repeated reads return the same IDs. Deduplicate IDs in your own workflow.'}

    def draft(self, to, subject, body):
        if not all(isinstance(x,str) for x in (to,subject,body)) or len(body)>100000 or len(subject)>998:
            raise Problem('Invalid draft or body exceeds 100,000 characters.')
        if '\r' in to+subject or '\n' in to+subject or not re.fullmatch(r'[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+',to):
            raise Problem('Provide one email address and a single-line subject.')
        account=self.s.read('tokens.json').get('email')
        if not account: raise Problem('Connect Gmail before preparing a draft.')
        did=secrets.token_hex(16)
        with self.s.db() as db:
            db.execute('INSERT INTO drafts VALUES (?,?,?)', (did,json.dumps({'to':to,'subject':subject,'body':body,'account':account}), 'pending'))
        return {'id':did,'status':'pending','next':'User must review the exact draft and click Send in the local wizard.'}

    def drafts(self):
        with self.s.db() as db:
            rows=db.execute('SELECT id,data,status FROM drafts ORDER BY rowid DESC LIMIT 30').fetchall()
        return [dict(id=row[0],**json.loads(row[1]),status=row[2]) for row in rows]

    def send_approved(self, did):
        valid_id(did)
        with self.s.lock('sync'):
            tokens=self.s.read('tokens.json')
            if SEND not in tokens.get('scope','').split():
                raise Problem('Reconnect with the optional Send permission first.')
            with self.s.db() as db:
                db.execute('BEGIN IMMEDIATE')
                row=db.execute('SELECT data,status FROM drafts WHERE id=?',(did,)).fetchone()
                if not row or row[1]!='pending': raise Problem('Draft already processed or missing. Refresh the page.')
                data=json.loads(row[0])
                if data['account']!=tokens['email']: raise Problem('Draft belongs to another account.')
                db.execute("UPDATE drafts SET status='sending' WHERE id=?",(did,))
            msg=email.message.EmailMessage()
            msg['To']=data['to']; msg['From']=tokens['email']; msg['Subject']=data['subject']
            msg['Message-ID']='<'+did+'@openclaw-gmail-connect.local>'
            msg.set_content(data['body'])
            try:
                result=self.api('messages/send',body={'raw':encode(msg.as_bytes())})
            except Exception:
                with self.s.db() as db:
                    db.execute("UPDATE drafts SET status='unknown-check-sent' WHERE id=?",(did,))
                raise Problem('Send outcome is uncertain. Check Gmail Sent before creating another draft; this draft will not be retried.',502) from None
            with self.s.db() as db:
                db.execute("UPDATE drafts SET status='sent' WHERE id=?",(did,))
            return {'sent':True,'id':result['id']}

    def disconnect(self):
        with self.s.lock('sync'),self.s.lock('auth'):
            (self.s.root/'tokens.json').unlink(missing_ok=True)
            with self.s.db() as db:
                db.execute('DELETE FROM kv');db.execute('DELETE FROM events');db.execute('DELETE FROM drafts')
        return {'disconnected':True,'note':'Local tokens and cache removed. Revoke the app in your Google Account to revoke access at Google too.'}

    def status(self):
        t=self.s.read('tokens.json');c=self.s.read('client.json')
        return {'version':VERSION,'connected':bool(t),'email':t.get('email'),'project':c.get('project_id'),
                'clientImported':bool(c),'sending':SEND in t.get('scope','').split(),'sync':self.s.get('sync'),
                'storage':'Private local files (0700 directory / 0600 files), not encrypted at rest.',
                'gatewayChanged':False}
