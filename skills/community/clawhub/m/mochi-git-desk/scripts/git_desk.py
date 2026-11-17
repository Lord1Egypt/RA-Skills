"""Selected Git project inventory, history and verified private work snapshots."""
import os,subprocess,uuid,zipfile
from core import *
def git(repo,*args,limit=10*1024*1024):
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}; env['GIT_TERMINAL_PROMPT']='0'; env['GIT_OPTIONAL_LOCKS']='0'
    p=subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-C',str(repo),*args],capture_output=True,timeout=45,env=env)
    if p.returncode: raise ValueError('Git operation failed: '+args[0])
    if len(p.stdout)>limit: raise ValueError('Git output exceeds limit')
    return p.stdout
def repo_for(st,r):
    repo=local(st.root,r['repository'])
    if not repo.is_dir(): raise ValueError('Repository directory missing')
    root=Path(git(repo,'rev-parse','--show-toplevel').decode().strip()).resolve()
    if root!=repo: raise ValueError('Choose repository root explicitly')
    return repo
def status(repo):
    raw=git(repo,'status','--porcelain=v1','-z','--untracked-files=all'); parts=raw.split(b'\0'); out=[]; i=0
    while i<len(parts):
        p=parts[i]; i+=1
        if not p: continue
        row={'status':p[:2].decode('ascii'),'path':os.fsdecode(p[3:])}
        if b'R' in p[:2] or b'C' in p[:2]:
            row['originalPath']=os.fsdecode(parts[i]); i+=1
        out.append(row)
    return out
def handle(st,r):
    repo=repo_for(st,r); action=r['action']
    if action=='status':
        branch=git(repo,'branch','--show-current').decode().strip(); return {'branch':branch,'changes':status(repo),'diffStat':git(repo,'diff','--no-ext-diff','--stat').decode('utf8','replace'),'stagedStat':git(repo,'diff','--cached','--no-ext-diff','--stat').decode('utf8','replace')}
    if action=='history':
        raw=git(repo,'log','-'+str(bounded(r.get('limit',30),1,200)),'--format=%H%x00%aI%x00%s%x00'); fields=raw.decode('utf8','replace').split('\0'); out=[]
        for i in range(0,len(fields)-2,3): out.append({'commit':fields[i].strip(),'date':fields[i+1],'subject':fields[i+2]})
        return out
    if action=='changes':
        path=r.get('path')
        if path: local(repo,path)
        args=['diff','--no-ext-diff','--no-textconv','--numstat']+(['--',path] if path else [])
        return {'working':git(repo,*args).decode('utf8','replace'),'staged':git(repo,'diff','--cached','--no-ext-diff','--no-textconv','--numstat',*(['--',path] if path else [])).decode('utf8','replace')}
    if action=='checkpoint':
        id=ident(r['id']); dest=local(st.root,r.get('output','exports/git/'+id+'.zip'))
        if dest.exists(): raise ValueError('Checkpoint already exists')
        if repo in dest.parents: raise ValueError('Place checkpoint outside repository')
        files={}; before=status(repo); head=git(repo,'rev-parse','HEAD').decode().strip()
        files['working.patch']=git(repo,'diff','--binary','--no-ext-diff','--no-textconv',limit=25*1024*1024)
        files['staged.patch']=git(repo,'diff','--cached','--binary','--no-ext-diff','--no-textconv',limit=25*1024*1024)
        # Include untracked files only when requested, excluding ignored files.
        if r.get('includeUntracked',False):
            for item in before:
                if item['status']!='??': continue
                p=local(repo,item['path'],True)
                if p.is_symlink() or p.stat().st_size>10*1024*1024: raise ValueError('Untracked link or file over 10 MiB')
                files['untracked/'+item['path'].replace('\\','/')]=p.read_bytes()
        if sum(len(b) for b in files.values())>50*1024*1024: raise ValueError('Checkpoint <=50 MiB')
        if status(repo)!=before or git(repo,'rev-parse','HEAD').decode().strip()!=head or git(repo,'diff','--binary','--no-ext-diff','--no-textconv',limit=25*1024*1024)!=files['working.patch'] or git(repo,'diff','--cached','--binary','--no-ext-diff','--no-textconv',limit=25*1024*1024)!=files['staged.patch']: raise ValueError('Repository changed during checkpoint; retry')
        for name,b in files.items():
            if name.startswith('untracked/') and local(repo,name[len('untracked/'):],True).read_bytes()!=b: raise ValueError('Untracked file changed during checkpoint')
        manifest={'baseCommit':head,'status':before,'files':{k:{'bytes':len(b),'sha256':digest(b)} for k,b in files.items()},'includesUntracked':bool(r.get('includeUntracked',False)),'createdAt':stamp()}; files['manifest.json']=json.dumps(manifest,ensure_ascii=False,indent=2).encode()
        import io
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for name,b in files.items(): z.writestr(name,b)
        raw=buf.getvalue(); atomic(dest,raw)
        with zipfile.ZipFile(dest) as z:
            if z.testzip(): raise ValueError('Checkpoint ZIP integrity failure')
            for k,b in files.items():
                if z.read(k)!=b: raise ValueError('Checkpoint verification failed')
        return {'file':str(dest),'sha256':digest(raw),'manifest':manifest}
    raise ValueError('Unknown Git action')
if __name__=='__main__': runmain(handle,'git-desk')
