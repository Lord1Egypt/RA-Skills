"""Bounded ZIP/TAR inventory, extraction into new directories and verified ZIP creation."""
import io,os,stat,tarfile,zipfile
from pathlib import PurePosixPath
from core import *
MAX=100*1024*1024; COUNT=5000
def safe(name):
    name=name.replace('\\','/'); p=PurePosixPath(name)
    if not name or p.is_absolute() or any(x in ('..','.') for x in name.rstrip('/').split('/')): raise ValueError('Unsafe archive path')
    if any(':' in x or x.endswith(('.',' ')) or x.split('.')[0].upper() in ('CON','PRN','AUX','NUL','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3','LPT4','LPT5','LPT6','LPT7','LPT8','LPT9') or any(ord(c)<32 for c in x) for x in p.parts): raise ValueError('Unsafe portable archive filename')
    return p.as_posix()
def members(p):
    out=[]; total=0; seen=set()
    if zipfile.is_zipfile(p):
        container=zipfile.ZipFile(p)
        for e in container.infolist():
            name=safe(e.filename); mode=(e.external_attr>>16)&0xFFFF
            if stat.S_ISLNK(mode) or e.flag_bits&1: container.close(); raise ValueError('Links/encrypted ZIP entries unsupported')
            out.append((name,e.file_size,e.is_dir(),e)); total+=e.file_size
            if total>MAX or len(out)>COUNT: container.close(); raise ValueError('Expanded archive >100 MiB or 5000 entries')
            if name.casefold() in seen: container.close(); raise ValueError('Duplicate/case-colliding archive paths')
            seen.add(name.casefold())
    else:
        container=tarfile.open(p,mode='r:*')
        for e in container:
            name=safe(e.name)
            if not e.isfile() and not e.isdir(): container.close(); raise ValueError('Only ordinary files/directories allowed in TAR')
            out.append((name,e.size,e.isdir(),e)); total+=e.size
            if total>MAX or len(out)>COUNT: container.close(); raise ValueError('Expanded archive >100 MiB or 5000 entries')
            if name.casefold() in seen: container.close(); raise ValueError('Duplicate/case-colliding archive paths')
            seen.add(name.casefold())
    files={name.casefold() for name,size,isdir,e in out if not isdir}
    for name,size,isdir,e in out:
        if any(str(parent).casefold() in files for parent in PurePosixPath(name).parents if str(parent)!='.'):
            container.close(); raise ValueError('Archive file/directory conflict')
    return container,out
def handle(st,r):
    action=r['action']
    if action in ('inspect','extract'):
        p=local(st.root,r['file'],True)
        if p.stat().st_size>MAX: raise ValueError('Input archive <=100 MiB')
        c,entries=members(p)
        try:
            inventory=[{'path':n,'bytes':s,'directory':d} for n,s,d,e in entries]
            if action=='inspect': return {'entries':inventory,'expandedBytes':sum(x['bytes'] for x in inventory),'archiveSha256':digest(p.read_bytes())}
            dest=local(st.root,r['directory'])
            if dest.exists(): raise ValueError('Extract into a new directory')
            # Fully validate/decompress before creating output, so corrupt data never
            # leaves an apparently successful partial extraction.
            data=[]
            for name,size,isdir,e in entries:
                if isdir: continue
                if isinstance(c,zipfile.ZipFile): b=c.read(e)
                else:
                    with c.extractfile(e) as f: b=f.read(MAX+1)
                if len(b)!=size: raise ValueError('Archive entry size mismatch')
                data.append((name,b))
            dest.mkdir(parents=True)
            for name,size,isdir,e in entries:
                if isdir: local(dest,name).mkdir(parents=True,exist_ok=True)
            receipt=[]
            for name,b in data:
                target=local(dest,name); atomic(target,b); receipt.append({'path':name,'sha256':digest(b),'bytes':len(b)})
            return {'directory':str(dest),'files':receipt}
        finally: c.close()
    if action=='create':
        dest=local(st.root,r['output'])
        if dest.exists(): raise ValueError('Archive output exists')
        paths=r['files']
        if not isinstance(paths,list) or not 1<=len(paths)<=COUNT: raise ValueError('Provide 1..5000 files explicitly')
        data=[]; seen=set(); total=0
        for rel in paths:
            name=safe(rel); p=local(st.root,rel,True)
            if p==dest or p.is_symlink(): raise ValueError('Archive cannot contain output or links')
            if name.casefold() in seen: raise ValueError('Duplicate archive input')
            seen.add(name.casefold()); total+=p.stat().st_size
            if total>MAX: raise ValueError('Archive inputs >100 MiB')
            data.append((name,p.read_bytes()))
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for name,b in data: z.writestr(name,b)
        raw=buf.getvalue()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            if z.testzip(): raise ValueError('Archive verification failed')
        atomic(dest,raw); return {'file':str(dest),'sha256':digest(raw),'files':[{'path':n,'bytes':len(b),'sha256':digest(b)} for n,b in data]}
    raise ValueError('Unknown archive action')
if __name__=='__main__': runmain(handle,'archive-desk')
