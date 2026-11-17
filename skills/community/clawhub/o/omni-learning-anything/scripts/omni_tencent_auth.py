"""Official Tencent Docs public OAuth device client; secrets stay in OS keyring."""
import json,re,time
from urllib.parse import urlsplit,urlencode
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError
ORIGIN='https://docs.qq.com'
SERVICE='omni-learning-anything/tencent'

def official_url(url):
    u=urlsplit(url)
    if u.scheme!='https' or u.hostname!='docs.qq.com' or u.username or u.password or u.port not in (None,443):raise ValueError('Tencent OAuth requires an official docs.qq.com HTTPS URL.')
    return url

def name_ok(name):
    if not isinstance(name,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',name):raise ValueError('Use a lowercase authorization name, starting with a letter.')

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Unexpected OAuth redirect; no credential forwarded.')

def request(url,data=None):
    official_url(url)
    headers={'Accept':'application/json'}
    payload=None
    if data is not None:
        if url.endswith('/register'):payload=json.dumps(data).encode();headers['Content-Type']='application/json'
        else:payload=urlencode(data).encode();headers['Content-Type']='application/x-www-form-urlencoded'
    req=Request(url,data=payload,headers=headers)
    try:
        with build_opener(NoRedirect).open(req,timeout=30) as r:return json.load(r)
    except HTTPError as error:
        if error.code in (400,401):
            try:return json.load(error)
            except Exception:pass
        raise RuntimeError('Tencent OAuth HTTP request failed; check the official service and connectivity.') from None

class KeyringStore:
    def __init__(self):
        try:
            import keyring
            backend=keyring.get_keyring()
            module=type(backend).__module__
            if module not in ('keyring.backends.macOS','keyring.backends.Windows','keyring.backends.SecretService','keyring.backends.libsecret'):raise RuntimeError('Select an OS credential store; plaintext keyring backends are not supported.')
            self.keyring=keyring
        except ImportError:raise RuntimeError('Install requirements-tencent-mcp.txt in the selected Python environment for OS keyring authorization.') from None
    def get(self,name):
        name_ok(name);value=self.keyring.get_password(SERVICE,name)
        return json.loads(value) if value else None
    def put(self,name,value):
        name_ok(name);self.keyring.set_password(SERVICE,name,json.dumps(value))

class Auth:
    def __init__(self,store=None,transport=None,clock=None):self.store=store or KeyringStore();self.request=transport or request;self.clock=clock or time.time
    def start(self,name):
        name_ok(name)
        old=self.store.get(name)
        if old and old.get('access_token'):return self.status(name)
        if old and old.get('device_code') and old['expires_at']>self.clock():return self.summary(old)
        meta=self.request(ORIGIN+'/.well-known/oauth-authorization-server')
        if meta.get('issuer')!=ORIGIN:raise ValueError('Unexpected Tencent OAuth issuer.')
        for key in ('registration_endpoint','device_authorization_endpoint','token_endpoint'):official_url(meta[key])
        reg=self.request(meta['registration_endpoint'],{'client_name':'Omni Learning Anything','redirect_uris':['http://127.0.0.1:8765/callback'],'response_types':['code'],'grant_types':['urn:ietf:params:oauth:grant-type:device_code','refresh_token'],'token_endpoint_auth_method':'none'})
        if not isinstance(reg.get('client_id'),str) or not reg['client_id']:raise ValueError('Official OAuth registration did not return a public client ID.')
        value=self.request(meta['device_authorization_endpoint'],{'client_id':reg['client_id'],'scope':'docs:read docs:write'})
        uri=value.get('verification_uri_complete') or value.get('verification_uri');official_url(uri)
        if not value.get('device_code') or not value.get('user_code') or not isinstance(value.get('expires_in'),(int,float)):raise ValueError('Official device grant response is incomplete.')
        value.update(client_id=reg['client_id'],token_endpoint=meta['token_endpoint'],expires_at=self.clock()+value['expires_in'],next_poll=self.clock()+value.get('interval',5),interval=max(5,value.get('interval',5)),verification_uri_complete=uri)
        self.store.put(name,value);return self.summary(value)
    def summary(self,value):return {'ready':False,'stage':'authorization','verification_uri':value['verification_uri_complete'],'user_code':value['user_code'],'expires_in':max(0,int(value['expires_at']-self.clock())),'note':'Review the account and document permissions on the official Tencent page, then run auth poll. No tokens belong in chat.'}
    def poll(self,name):
        name_ok(name);v=self.store.get(name)
        if not v:return {'ready':False,'stage':'missing'}
        if v.get('access_token'):return self.status(name)
        if v['expires_at']<=self.clock():return {'ready':False,'stage':'expired'}
        if v.get('next_poll',0)>self.clock():return {'ready':False,'stage':'pending','retry_after':int(v['next_poll']-self.clock())+1}
        result=self.request(official_url(v['token_endpoint']),{'grant_type':'urn:ietf:params:oauth:grant-type:device_code','client_id':v['client_id'],'device_code':v['device_code']})
        error=result.get('error')
        if error in ('authorization_pending','slow_down'):
            if error=='slow_down':v['interval']+=5
            v['next_poll']=self.clock()+v['interval'];self.store.put(name,v);return {'ready':False,'stage':'pending','retry_after':v['interval']}
        if error:return {'ready':False,'stage':'expired' if error=='expired_token' else 'denied','note':'Official authorization did not complete. Review the account/permissions before requesting another code.'}
        self.accept(name,v,result);return self.status(name)
    def accept(self,name,old,result):
        if not isinstance(result.get('access_token'),str) or not result['access_token']:raise RuntimeError('Tencent OAuth returned no access token.')
        value={k:result[k] for k in ('access_token','refresh_token','scope','token_type') if k in result}
        value.update(client_id=old['client_id'],token_endpoint=old['token_endpoint'],expires_at=self.clock()+result.get('expires_in',3600));self.store.put(name,value)
    def status(self,name):
        name_ok(name);v=self.store.get(name)
        return {'ready':bool(v and v.get('access_token') and v['expires_at']>self.clock()),'stage':'authorized' if v and v.get('access_token') else 'missing','expires_in':max(0,int(v['expires_at']-self.clock())) if v else 0}
    def token(self,name):
        name_ok(name);v=self.store.get(name)
        if not v or not v.get('access_token'):raise RuntimeError('Complete official Tencent authorization first.')
        if v['expires_at']<=self.clock()+60:
            if not v.get('refresh_token'):raise RuntimeError('Tencent authorization expired; renew it on the official page.')
            result=self.request(official_url(v['token_endpoint']),{'grant_type':'refresh_token','client_id':v['client_id'],'refresh_token':v['refresh_token']})
            if 'refresh_token' not in result:result['refresh_token']=v['refresh_token']
            self.accept(name,v,result);v=self.store.get(name)
        return v['access_token']

    def start_code(self,name,port):
        import secrets,hashlib,base64
        name_ok(name)
        if type(port) is not int or not 1024<=port<=65535:raise ValueError('Use a local unprivileged callback port.')
        meta=self.request(ORIGIN+'/.well-known/oauth-authorization-server')
        if meta.get('issuer')!=ORIGIN:raise ValueError('Unexpected Tencent OAuth issuer.')
        for k in ('authorization_endpoint','registration_endpoint','token_endpoint'):official_url(meta[k])
        redirect='http://127.0.0.1:'+str(port)+'/callback'
        reg=self.request(meta['registration_endpoint'],{'client_name':'Omni Learning Anything','redirect_uris':[redirect],'response_types':['code'],'grant_types':['authorization_code','refresh_token'],'token_endpoint_auth_method':'none'})
        if not isinstance(reg.get('client_id'),str) or not reg['client_id']:raise RuntimeError('Official OAuth public registration failed.')
        verifier=secrets.token_urlsafe(48);state=secrets.token_urlsafe(32)
        challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
        value=dict(client_id=reg['client_id'],token_endpoint=meta['token_endpoint'],redirect_uri=redirect,code_verifier=verifier,state=state,expires_at=self.clock()+600)
        self.store.put(name,value)
        args={'client_id':reg['client_id'],'response_type':'code','redirect_uri':redirect,'scope':'docs:read docs:write','state':state,'code_challenge':challenge,'code_challenge_method':'S256'}
        return {'ready':False,'stage':'authorization','authorization_url':meta['authorization_endpoint']+('&' if '?' in meta['authorization_endpoint'] else '?')+urlencode(args),'expires_in':600}
    def finish_code(self,name,code,state):
        import secrets
        name_ok(name);v=self.store.get(name)
        if not v or not isinstance(state,str) or not secrets.compare_digest(state,v.get('state','')) or v['expires_at']<=self.clock():raise ValueError('OAuth callback state mismatched or expired; do not exchange this code.')
        if not isinstance(code,str) or not code:raise ValueError('OAuth callback contains no code.')
        result=self.request(official_url(v['token_endpoint']),{'grant_type':'authorization_code','client_id':v['client_id'],'redirect_uri':v['redirect_uri'],'code_verifier':v['code_verifier'],'code':code})
        self.accept(name,v,result);return self.status(name)

def login(name):
    """One foreground login, loopback-only callback; no browser cookies or hosted proxy."""
    from http.server import HTTPServer,BaseHTTPRequestHandler
    from urllib.parse import parse_qs
    auth=Auth();outcome={}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            u=urlsplit(self.path);query=parse_qs(u.query)
            if u.path!='/callback':self.send_error(404);return
            try:
                result=auth.finish_code(name,query.get('code',[''])[0],query.get('state',[''])[0]);outcome.update(result);text='Authorization complete. You can return to the agent.';status=200
            except Exception:outcome.update(ready=False,stage='failed');text='Authorization could not be confirmed. Return to the agent for diagnosis.';status=400
            self.send_response(status);self.send_header('Content-Type','text/plain; charset=utf-8');self.end_headers();self.wfile.write(text.encode())
    with HTTPServer(('127.0.0.1',0),Handler) as server:
        server.timeout=1
        summary=auth.start_code(name,server.server_port);print(json.dumps(summary,ensure_ascii=False),flush=True)
        deadline=time.monotonic()+600
        while not outcome and time.monotonic()<deadline:server.handle_request()
    return outcome or {'ready':False,'stage':'expired'}
