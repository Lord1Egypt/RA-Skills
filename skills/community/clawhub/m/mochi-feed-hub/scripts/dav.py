"""Authenticated HTTPS DAV client: fixed origin, no redirects, conditional writes."""
import base64, ssl, urllib.error, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from core import *
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
def xml(b):
    if b'<!DOCTYPE' in b.upper() or b'<!ENTITY' in b.upper(): raise ValueError('XML entities rejected')
    return ET.fromstring(b)
class DAV:
    def __init__(self,config):
        c=privateconfig(config); self.base=c['url'].rstrip('/')+'/'
        p=urllib.parse.urlsplit(self.base)
        if p.scheme!='https' or not p.hostname or p.username or p.password or p.query or p.fragment: raise ValueError('DAV profile needs plain HTTPS collection URL')
        self.auth='Basic '+base64.b64encode((c['username']+':'+secret(c)).encode()).decode()
        self.opener=urllib.request.build_opener(NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    def url(self,path):
        if path=='': return self.base
        if not isinstance(path,str) or path.startswith('/') or any(x in path for x in ('\\','?','#',':')) or any(ord(x)<32 for x in path): raise ValueError('Use collection-relative DAV paths')
        parts=path.split('/')
        if any(p in ('.','..') or '%' in p for p in parts): raise ValueError('DAV traversal/encoded path rejected')
        return self.base+'/'.join(urllib.parse.quote(p,safe='') for p in parts)
    def request(self,method,path='',body=None,headers=None,limit=50*1024*1024):
        h={'Authorization':self.auth,**(headers or {})}; req=urllib.request.Request(self.url(path),body,h,method=method)
        with self.opener.open(req,timeout=30) as res:
            b=res.read(limit+1)
            if len(b)>limit: raise ValueError('DAV response exceeds size limit')
            return res.status,dict(res.headers),b
    def path_from_href(self,href):
        absolute=urllib.parse.urljoin(self.base,href); p=urllib.parse.urlsplit(absolute); root=urllib.parse.urlsplit(self.base)
        if (p.scheme,p.netloc)!=(root.scheme,root.netloc) or not p.path.startswith(root.path): raise ValueError('DAV response points outside collection')
        return urllib.parse.unquote(p.path[len(root.path):])
    def listing(self):
        body=b'<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop><d:getetag/><d:getcontentlength/><d:getlastmodified/><d:resourcetype/></d:prop></d:propfind>'
        _,_,b=self.request('PROPFIND',body=body,headers={'Depth':'1','Content-Type':'application/xml'},limit=4*1024*1024); out=[]
        for r in xml(b).findall('{DAV:}response'):
            href=r.findtext('{DAV:}href')
            for ps in r.findall('{DAV:}propstat'):
                if ' 200 ' not in ps.findtext('{DAV:}status',''): continue
                p=ps.find('{DAV:}prop'); path=self.path_from_href(href)
                if not path: continue
                out.append({'path':path,'etag':p.findtext('{DAV:}getetag'),'size':p.findtext('{DAV:}getcontentlength'),'collection':p.find('{DAV:}resourcetype/{DAV:}collection') is not None})
                if len(out)>10000: raise ValueError('Collection exceeds 10000 entries')
        return out
