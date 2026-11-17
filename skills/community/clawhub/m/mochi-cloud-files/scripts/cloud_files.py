"""WebDAV cloud file inventory, conflict-aware transfer and comparison."""
from core import *
from dav import DAV
def handle(st,r):
    d=DAV(r['profile']); action=r['action']
    if action=='list': return d.listing()
    if action=='mkdir':
        status,_,_=d.request('MKCOL',r['remote']); return {'status':status}
    if action=='plan':
        base=local(st.root,r['directory']); remote={v['path']:v for v in d.listing() if not v['collection']}; out=[]
        if not base.is_dir(): raise ValueError('Local directory missing')
        for p in sorted(base.iterdir()):
            if p.is_symlink(): raise ValueError('Symbolic links rejected')
            if not p.is_file(): continue
            previous=st.get('transfer',d.base+p.name); current=remote.pop(p.name,None); sha=digest(p.read_bytes())
            unchanged=previous and previous.get('localSha256')==sha and current and previous.get('etag')==current['etag']
            out.append({'path':p.name,'action':'unchanged' if unchanged else 'review' if current else 'upload-new','localSha256':sha,'remote':current})
        out.extend({'path':k,'action':'remote-only','remote':v} for k,v in remote.items()); return {'scope':'one directory, no deletion','plan':out}
    if action=='download':
        p=local(st.root,r['file']); expected=r.get('localSha256')
        if p.exists() and (not expected or digest(p.read_bytes())!=expected): raise ValueError('Local output exists or changed; provide its current hash')
        h={'If-Match':r['etag']} if r.get('etag') else {}; status,headers,b=d.request('GET',r['remote'],headers=h)
        if p.exists() and (not expected or digest(p.read_bytes())!=expected): raise ValueError('Local output changed during download')
        atomic(p,b); etag=next((v for k,v in headers.items() if k.lower()=='etag'),None); sha=digest(b)
        st.put('transfer',d.base+r['remote'],{'localSha256':sha,'etag':etag}); return {'file':str(p),'sha256':sha,'etag':etag}
    if action=='upload':
        p=local(st.root,r['file'],True)
        if p.stat().st_size>50*1024*1024: raise ValueError('Single transfer <=50 MiB')
        b=p.read_bytes(); h={'Content-Type':'application/octet-stream',**({'If-Match':r['etag']} if r.get('etag') else {'If-None-Match':'*'})}
        status,headers,_=d.request('PUT',r['remote'],b,h); etag=next((v for k,v in headers.items() if k.lower()=='etag'),None)
        st.put('transfer',d.base+r['remote'],{'localSha256':digest(b),'etag':etag}); return {'status':status,'sha256':digest(b),'etag':etag}
    if action=='delete':
        if not r.get('etag'): raise ValueError('Deletion needs current remote ETag')
        status,_,_=d.request('DELETE',r['remote'],headers={'If-Match':r['etag']}); return {'status':status}
    raise ValueError('Unknown cloud-file action')
if __name__=='__main__': runmain(handle,'cloud-files')
