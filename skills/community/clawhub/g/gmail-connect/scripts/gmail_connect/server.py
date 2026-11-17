import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import threading
import urllib.parse
import webbrowser
from .core import Problem
from . import service

ASSETS=Path(__file__).resolve().parents[2]/'assets/ui'

class Wizard(ThreadingHTTPServer):
    daemon_threads=True
    allow_reuse_address=False
    def __init__(self, gmail, port):
        super().__init__(('127.0.0.1',port), Handler)
        self.gmail=gmail
        self.key=secrets.token_urlsafe(32)
        self.pending=None
        self.pending_lock=threading.Lock()
        self.origin='http://127.0.0.1:'+str(self.server_address[1])

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass # callback URLs contain authorization codes
    def headers_ok(self):
        return self.headers.get('Host')==urllib.parse.urlparse(self.server.origin).netloc
    def reply(self,code,body,ctype='application/json'):
        if ctype=='application/json':body=json.dumps(body).encode()
        elif isinstance(body,str):body=body.encode()
        self.send_response(code)
        self.send_header('Content-Type',ctype)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.end_headers();self.wfile.write(body)
    def authorized(self):
        return secrets.compare_digest(self.headers.get('Authorization',''),'Bearer '+self.server.key)
    def do_GET(self):
        if not self.headers_ok():return self.reply(403,{'error':'Invalid host'})
        p=urllib.parse.urlparse(self.path)
        if p.path=='/oauth/callback':
            args=urllib.parse.parse_qs(p.query)
            state=args.get('state',[''])[0]
            try:
                with self.server.pending_lock:
                    pending=self.server.pending
                    if not pending or not secrets.compare_digest(state,pending['state']):
                        raise Problem('Authorization state mismatch. Return to setup and try again.')
                    self.server.pending=None # consume only matching state, once
                if 'error' in args:raise Problem('Google authorization was cancelled or denied. Return to setup to retry.')
                self.server.gmail.finish(pending,args.get('code',[''])[0],state)
                return self.reply(200,'<!doctype html><title>Gmail connected</title><h1>Gmail connected</h1><p>Close this tab and return to the setup wizard. Click Refresh status.</p>','text/html; charset=utf-8')
            except Problem as e:return self.reply(400,'Authorization failed. Return to the setup wizard and reconnect. Check the Desktop client, consent, test user and requested permissions.','text/plain')
        routes={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/guide.css':'guide.css'}
        if p.path in routes:
            filename=routes[p.path]
            return self.reply(200,(ASSETS/filename).read_bytes(),{'index.html':'text/html; charset=utf-8','app.js':'text/javascript','style.css':'text/css','guide.css':'text/css'}[filename])
        if p.path=='/api/status':
            if not self.authorized():return self.reply(401,{'error':'Open the private setup link printed by the launcher.'})
            return self.reply(200,dict(self.server.gmail.status(),service=service.status()))
        return self.reply(404,{'error':'Not found'})
    def do_POST(self):
        if not self.headers_ok() or not self.authorized() or self.headers.get('Origin') != self.server.origin:
            return self.reply(403,{'error':'Unauthorized local request'})
        if self.headers.get('Content-Type')!='application/json':return self.reply(415,{'error':'JSON required'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<2 or size>200000:raise Problem('Request exceeds size limit.')
            data=json.loads(self.rfile.read(size))
            if not isinstance(data,dict):raise Problem('JSON object required.')
            g=self.server.gmail
            action=self.path
            if action=='/api/client':result=g.import_client(data)
            elif action=='/api/connect':
                url,pending=g.begin(self.server.origin+'/oauth/callback',data.get('sending') is True)
                with self.server.pending_lock:self.server.pending=pending
                result={'url':url}
            elif action=='/api/check':result={'profile':g.api('profile'),'sync':g.sync()}
            elif action=='/api/search':result=g.search(data.get('query','in:inbox'),20,data.get('page'))
            elif action=='/api/read':result=g.message(data.get('id'),True)
            elif action=='/api/drafts':result=g.drafts()
            elif action=='/api/send':result=g.send_approved(data.get('id'))
            elif action=='/api/monitor/start':
                if not g.status()['connected']:raise Problem('Connect Gmail first.')
                result=service.install(g.s)
            elif action=='/api/monitor/stop':result=service.stop()
            elif action=='/api/disconnect':
                service.stop()
                with self.server.pending_lock:self.server.pending=None
                result=g.disconnect()
            else:return self.reply(404,{'error':'Not found'})
            return self.reply(200,result)
        except Problem as e:return self.reply(e.status if 400<=e.status<=599 else 400,{'error':str(e)})
        except (ValueError,TypeError,KeyError):return self.reply(400,{'error':'Invalid request. Check the supplied fields.'})
        except Exception:return self.reply(500,{'error':'Local operation failed. Check private state permissions and available disk space.'})

def serve(gmail,port=8766,open_browser=True):
    try:server=Wizard(gmail,port)
    except OSError:raise Problem('Setup port is already in use. Reopen the running wizard or use --port 8767.') from None
    url=server.origin+'/#'+server.key
    print('Private setup link (do not share): '+url,flush=True)
    print('Keep this process running during setup. Ctrl+C closes the wizard; an installed monitor keeps running.',flush=True)
    if open_browser:webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
