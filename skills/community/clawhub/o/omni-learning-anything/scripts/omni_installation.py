"""Complete bundle checks and managed ZIP replacement, never a cross-host installer."""
import ast
import hashlib
import io
import json
import os
import posixpath
import re
import shutil
import tempfile
import uuid
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, is_zipfile, BadZipFile

NAME='omni-learning-anything'
RECEIPT='.omni-install.json'
MAX_BYTES=25*1024*1024


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def allowed(name):
    parts=PurePosixPath(name).parts
    if not parts or any(x.startswith('.') or '.local.' in x for x in parts):return False
    return name in ('SKILL.md','LICENSE','agents/openai.yaml','references/course-catalog.json','references/textbook-index.json') or (parts[0]=='references' and name.endswith('.md')) or (len(parts)==2 and parts[0]=='scripts' and ((parts[1].startswith('omni_') and name.endswith('.py')) or (parts[1].startswith('requirements') and name.endswith('.txt'))))


def validate(files):
    issues=[]
    for name in ('SKILL.md','LICENSE','agents/openai.yaml','scripts/omni_learning.py','references/install.md','references/setup.md'):
        if name not in files:issues.append('Missing '+name)
    version=None
    if 'SKILL.md' in files:
        content=files['SKILL.md'].decode('utf-8');match=re.match(r'^---\n(.*?)\n---',content,re.S)
        if not match or not re.search(r'^name: '+NAME+r'\s*$',match[1],re.M):issues.append('Unexpected Skill identity/frontmatter')
        found=re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',content,re.M)
        if not found:issues.append('Missing version metadata')
        else:version=found[1]
    for name,raw in files.items():
        if name.endswith('.md'):
            for ref in re.findall(r'\]\(([^)]+)\)',raw.decode('utf-8')):
                ref=ref.split('#')[0]
                if ref.endswith('.md') and '://' not in ref:
                    linked=posixpath.normpath(str(PurePosixPath(name).parent/ref))
                    if linked not in files:issues.append('Missing linked reference '+linked)
        if name.startswith('scripts/') and name.endswith('.py'):
            try:tree=ast.parse(raw,filename=name)
            except (SyntaxError,ValueError):issues.append('Invalid Python: '+name);continue
            for node in ast.walk(tree):
                modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or ''] if isinstance(node,ast.ImportFrom) else []
                for module in modules:
                    if module.startswith('omni_') and 'scripts/'+module+'.py' not in files:issues.append('Missing local module '+module)
    if 'scripts/omni_courses.py' in files:
        name='references/course-catalog.json'
        if name not in files:issues.append('Missing '+name)
        else:
            try:
                from omni_courses import validate_course
                data=json.loads(files[name])
                require(data.get('schema')==1 and isinstance(data.get('courses'),list) and data['courses'],'Invalid course catalog.')
                for course in data['courses']:validate_course(course)
                ids=[course['id'] for course in data['courses']]
                require(len(ids)==len(set(ids)),'Duplicate course ID.')
            except (ValueError,TypeError,KeyError,AttributeError):issues.append('Invalid '+name)
    if 'scripts/omni_textbook_index.py' in files:
        name='references/textbook-index.json'
        if name not in files:issues.append('Missing '+name)
        else:
            try:
                index=json.loads(files[name])
                require(isinstance(index['books'],list) and index['books'],'Empty textbook index.')
            except (ValueError,TypeError,KeyError,AttributeError):issues.append('Invalid '+name)
    return version,sorted(set(issues))


def tree_files(root):
    files={};issues=[]
    for p in root.rglob('*'):
        if p.is_symlink():issues.append('Symlink: '+str(p.relative_to(root)));continue
        if not p.is_file():continue
        name=p.relative_to(root).as_posix()
        if name==RECEIPT or ('__pycache__' in p.parts and p.suffix=='.pyc'):continue
        if not allowed(name):issues.append('Unmanaged file: '+name)
        else:files[name]=p.read_bytes()
    return files,issues


def inspect(path):
    root=Path(path).absolute();require(root.is_dir(), 'Choose the installed Skill folder containing SKILL.md.')
    files,issues=tree_files(root);version,_=validate(files)
    receipt=root/RECEIPT;managed=receipt.is_file() and not receipt.is_symlink();verified=False
    normalized=[]
    # Recognition is for read-only completeness, never authenticity or adoption.
    meta=root/'_meta.json'
    if not managed and meta.is_file() and not meta.is_symlink() and meta.stat().st_size<=8192:
        try:
            value=json.loads(meta.read_text())
            recognized=isinstance(value,dict) and set(value)=={'ownerId','publishedAt','slug','version'} and value['slug']==NAME and value['version']==version and isinstance(value['ownerId'],str) and bool(value['ownerId']) and type(value['publishedAt']) is int and value['publishedAt']>0
        except (ValueError,UnicodeError):recognized=False
        if recognized:
            issues.remove('Unmanaged file: _meta.json');normalized.append('_meta.json: registry metadata, not integrity proof')
            alias=root/'LICENSE.txt'
            if 'LICENSE' not in files and alias.is_file() and not alias.is_symlink() and alias.stat().st_size<=65536:
                files['LICENSE']=alias.read_bytes();issues.remove('Unmanaged file: LICENSE.txt');normalized.append('LICENSE.txt: license filename alias')
    version,missing=validate(files);issues+=missing
    if managed:
        value=json.loads(receipt.read_text());verified=value.get('schema')==1 and value.get('version')==version and value.get('files')=={n:digest(raw) for n,raw in files.items()} and not issues
    return {'path':str(root),'version':version,'complete':not issues,'issues':issues,'managed_zip_install':managed,
            'integrity_verified':verified,'native_discovery':'unknown',
            'inspection_normalizations':normalized,
            'next_action':'Verify the selected host native inventory or actual skill invocation; file presence alone is not discovery.',
            'update_route':'managed_zip' if managed else 'original_native_manager'}


def no_symlinks(path):
    system_aliases={'/var':'/private/var','/tmp':'/private/tmp'}
    for p in [path,*path.parents]:
        if p.is_symlink() and system_aliases.get(str(p))!=str(p.resolve()):
            raise ValueError('Installation paths cannot use symlinks; use the original manager for linked installs.')


def archive_files(archive,sha256):
    require(isinstance(sha256,str) and re.fullmatch('[0-9a-f]{64}',sha256), 'Supply the verified release SHA256 from SHA256SUMS.')
    archive=Path(archive);require(archive.stat().st_size<=10*1024*1024, 'Skill ZIP exceeds the download limit.')
    raw=archive.read_bytes();require(digest(raw)==sha256, 'ZIP checksum mismatch; existing installation was not changed.')
    require(is_zipfile(io.BytesIO(raw)), 'Invalid Skill ZIP; download a verified release archive again.')
    files={}
    with ZipFile(io.BytesIO(raw)) as z:
        members=z.infolist();require(len(members)<=1000 and sum(m.file_size for m in members)<=MAX_BYTES,'ZIP exceeds the extraction budget.')
        for m in members:
            parts=PurePosixPath(m.filename).parts
            require(parts and parts[0]==NAME and '..' not in parts and '\\' not in m.filename and not m.filename.startswith('/'),'Unsafe ZIP path.')
            require((m.external_attr>>16)&0o170000!=0o120000,'ZIP symlinks are not supported.')
            if m.is_dir():continue
            name='/'.join(parts[1:]);require(allowed(name) and name not in files,'Unknown or duplicate ZIP entry: '+name)
            try:files[name]=z.read(m)
            except BadZipFile:raise ValueError('Corrupt Skill ZIP; download the release archive again.')
    version,issues=validate(files);require(not issues,'Incomplete bundle: '+', '.join(issues))
    return version,files


def install(archive,destination,sha256,*,update=False):
    version,files=archive_files(archive,sha256);target=Path(destination).absolute();no_symlinks(target);target=target.resolve()
    require(target.name==NAME,'Destination must be the exact omni-learning-anything Skill folder, outside course archives.')
    require(not any(all((parent/name).is_file() for name in ('config.json','plan.json','state.json')) for parent in target.parents), 'Install Skill files outside existing course archives.')
    target.parent.mkdir(parents=True,exist_ok=True)
    lock=target.parent/('.'+NAME+'.install-lock')
    try:lock.mkdir()
    except FileExistsError:raise RuntimeError('Skill install/update is already running; do not remove its lock while active.')
    backup=None
    try:
        if target.exists():
            require(update,'Destination already exists; use the original manager or an explicit managed update.')
            status=inspect(target);require(status['managed_zip_install'] and status['integrity_verified'],'Unmanaged/edited/incomplete installation; preserve it and use its original updater or a fresh destination.')
            receipt=json.loads((target/RECEIPT).read_text())
            if receipt['files']=={n:digest(raw) for n,raw in files.items()}:
                return {'action':'unchanged','path':str(target),'version':version,'backup':None}
        else:require(not update,'No managed installation exists to update; install into a fresh destination.')
        with tempfile.TemporaryDirectory(prefix='.omni-stage-',dir=target.parent) as temporary:
            staged=Path(temporary)/'bundle';staged.mkdir(mode=0o700)
            for name,raw in files.items():
                path=staged/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
            receipt={'schema':1,'version':version,'archive_sha256':sha256,'files':{n:digest(raw) for n,raw in files.items()}}
            (staged/RECEIPT).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(staged/RECEIPT).chmod(0o600)
            require(inspect(staged)['integrity_verified'],'Staged bundle validation failed.')
            if target.exists():
                backup=target.parent/('.'+NAME+'.backup-'+uuid.uuid4().hex);os.replace(target,backup)
            try:os.replace(staged,target)
            except BaseException:
                # Ctrl-C/SystemExit must not leave an absent active installation.
                # If the atomic swap already completed, keep that complete target.
                if backup and not target.exists():os.replace(backup,target)
                raise
        return {'action':'updated' if backup else 'installed','path':str(target),'version':version,'backup':str(backup) if backup else None}
    finally:lock.rmdir()


def adopt(archive,destination,sha256):
    """Enroll an exact historical ZIP copy; never guess ownership or accept local edits."""
    version,files=archive_files(archive,sha256);target=Path(destination).absolute();no_symlinks(target);target=target.resolve()
    require(target.name==NAME and target.is_dir(),'Choose the existing standalone Skill folder, not a manager cache.')
    lock=target.parent/('.'+NAME+'.install-lock')
    try:lock.mkdir()
    except FileExistsError:raise RuntimeError('Skill install/update is already running.')
    try:
        actual,issues=tree_files(target)
        require(not issues and actual==files,'Installed files differ from the verified old release; preserve local changes and use a fresh installation.')
        value={'schema':1,'version':version,'archive_sha256':sha256,'files':{n:digest(raw) for n,raw in files.items()}}
        receipt=target/RECEIPT
        if receipt.exists():require(inspect(target)['integrity_verified'],'Existing installation receipt is invalid.')
        else:
            fd=os.open(receipt,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'w',encoding='utf-8') as stream:json.dump(value,stream,indent=2);stream.write('\n')
        return {'action':'adopted','path':str(target),'version':version}
    finally:lock.rmdir()
