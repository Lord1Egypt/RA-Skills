"""Private immutable material versions, exact learning scopes and bounded evidence."""
import hashlib,json,os,re,tempfile
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit
import omni_core as c


def require(ok,message):
    if not ok:raise ValueError(message)


def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def path(root,*parts):
    root=Path(root).resolve();base=root/'materials';target=base.joinpath(*parts)
    require(target.resolve().is_relative_to(base.resolve()) and base.resolve().is_relative_to(root),'Material path escapes archive.')
    for p in [base,target,*target.parents]:
        if p==root:break
        require(not p.is_symlink(),'Material storage cannot use symlinks.')
    return target


def save(root,parts,value):
    target=path(root,*parts);parent=Path(root).resolve()/'materials';parent.mkdir(mode=0o700,exist_ok=True)
    for part in target.relative_to(parent).parts[:-1]:parent=parent/part;parent.mkdir(mode=0o700,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=target.parent,delete=False) as f:
            temporary=Path(f.name);json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
        os.replace(temporary,target)
    finally:
        if temporary and temporary.exists():temporary.unlink()


def identity(material_id,version):
    require(isinstance(material_id,str) and bool(re.fullmatch(r'm_[0-9a-f]{16}',material_id)),'Invalid material ID.')
    require(isinstance(version,str) and bool(re.fullmatch(r'[0-9a-f]{64}',version)),'Invalid material version.')


def public_url(value):
    u=urlsplit(value)
    require(u.scheme in ('http','https') and u.hostname and not u.username and not u.password and not any(x in u.query.lower() for x in ('token','secret','key=','auth=')),'Use a public canonical URL without credentials or token query data.')
    return value


def import_file(root,file,*,material_id=None,url=None,retry=False,max_file=None,pdf_ocr=None,title=None,publisher=None):
    from omni_material_readers import read,ReaderError
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True);file=Path(file)
    require(file.is_file(),'Material file is unavailable; ask for a readable local copy.')
    from omni_material_readers import MAX_FILE
    limit=MAX_FILE if max_file is None else max_file
    require(file.stat().st_size<=limit,f'File exceeds {limit//(1024*1024)} MiB; split it before importing.')
    # Parse exactly the private bytes used to compute this version, never reread a changing original.
    with tempfile.TemporaryDirectory(prefix='omni-material-') as temporary:
        captured=Path(temporary)/('source'+file.suffix)
        digest=hashlib.sha256();size=0
        with file.open('rb') as src,captured.open('wb') as dst:
            for part in iter(lambda:src.read(1024*1024),b''):
                size+=len(part);require(size<=limit,'Input grew beyond the import budget; retry a stable smaller file.')
                digest.update(part);dst.write(part)
        version=digest.hexdigest();material_id=material_id or 'm_'+hashlib.sha256(file.name.casefold().encode()).hexdigest()[:16]
        identity(material_id,version)
        if url:public_url(url)
        with c.lock(root):
            target=path(root,'items',material_id,version+'.json')
            if target.exists():
                old=load(root,material_id,version)
                require(old.get('url')==url,'Same file version has different origin metadata; use an explicit different material identity.')
                if not retry or old['status'] in ('ready','partial'):return brief(old)
                save(root,('failed_attempts',material_id,version+'-'+str(datetime.now(timezone.utc).timestamp())+'.json'),old)
            options = {}
            if max_file is not None: options['max_file'] = max_file
            if pdf_ocr is not None: options['pdf_ocr'] = pdf_ocr
            try:parsed=read(captured, **options)
            except ReaderError as error:parsed={'kind':file.suffix.lstrip('.'),'status':'failed','units':[],'warnings':[str(error)],'missing_pages':[],'total_pages':None}
            except ModuleNotFoundError:parsed={'kind':file.suffix.lstrip('.'),'status':'needs_dependency','units':[],'warnings':['Install selected PDF reader requirements, or provide TXT/DOCX.'],'missing_pages':[],'total_pages':None}
            except Exception:parsed={'kind':file.suffix.lstrip('.'),'status':'failed','units':[],'warnings':['Extraction failed or input is unsafe/unreadable; provide a simpler authorized text copy.'],'missing_pages':[],'total_pages':None}
            value=dict(parsed,id=material_id,version=version,title=title or file.name,imported_at=datetime.now(timezone.utc).isoformat())
            if url:value['url']=url
            if publisher:value['publisher']=publisher
            value['integrity']=fingerprint(value);save(root,('items',material_id,version+'.json'),value)
            return brief(value)


def load(root,material_id,version):
    identity(material_id,version);value=c.read(path(root,'items',material_id,version+'.json'))
    require(value.get('id')==material_id and value.get('version')==version,'Material identity mismatch.')
    require(value.get('integrity')==fingerprint({k:v for k,v in value.items() if k!='integrity'}),'Material snapshot changed; preserve history and import a new version.')
    return value


def brief(value):return {k:value[k] for k in ('id','version','title','kind','status','warnings')} | {'unit_count':len(value['units'])}


def inspect(root,material_id,version):
    value=load(root,material_id,version)
    return dict(brief(value),units=[{k:u[k] for k in ('id','locator','heading','page')} for u in value['units']],missing_pages=value['missing_pages'])


def listing(root):
    return [brief(load(root,p.parent.name,p.stem)) for p in path(root,'items').glob('m_*/*.json')]


def select(root,material_id,version,*,pages=None,heading=None,units=None,exclude=None):
    value=load(root,material_id,version);require(value['status'] in ('ready','partial') and bool(value['units']),'Material has no accepted text; resolve its exact import status first.')
    chosen=list(value['units'])
    if pages:
        require(value['kind']=='pdf','Page ranges refer only to original PDF pages; use headings/unit IDs for converted documents.')
        requested=set()
        for part in pages.split(','):
            match=re.fullmatch(r'(\d+)(?:-(\d+))?',part.strip());require(bool(match),'Use page ranges such as 2-4,7.')
            lo=int(match[1]);hi=int(match[2] or lo)
            require(1<=lo<=hi<=value['total_pages'],'Page range is outside this PDF.')
            requested.update(range(lo,hi+1))
        require(not requested.intersection(value['missing_pages']),'Requested range includes unreadable/empty pages; provide OCR/text or explicitly select readable pages.')
        chosen=[u for u in chosen if u['page'] in requested]
    if heading:
        nodes={(sid,title) for u in chosen for sid,title in zip(u['section_path'],u['heading_path']) if heading.casefold() in title.casefold()}
        exact={node for node in nodes if node[1].casefold()==heading.casefold()}
        if exact:nodes=exact
        require(len(nodes)==1,'Heading is absent or ambiguous; inspect occurrences and select explicit unit IDs.')
        section_id=next(iter(nodes))[0]
        chosen=[u for u in chosen if section_id in u['section_path']]
    if units:
        require(isinstance(units,list) and set(units)<=set(u['id'] for u in chosen),'Selected units are outside the requested range.')
        chosen=[u for u in chosen if u['id'] in units]
    if exclude:
        require(set(exclude)<=set(u['id'] for u in chosen),'Excluded units must be inside the current range.')
        chosen=[u for u in chosen if u['id'] not in exclude]
    require(bool(chosen),'No readable content remains selected.')
    selection={'id':material_id,'version':version,'snapshot_hash':value['integrity'],'units':[u['id'] for u in chosen]}
    selection['hash']=fingerprint(selection);return selection


def verify_selection(root,selection):
    require(isinstance(selection,dict) and set(selection)=={'id','version','snapshot_hash','units','hash'},'Selections must be immutable id/version/units/hash objects.')
    value=load(root,selection['id'],selection['version']);units=selection['units']
    require(selection['snapshot_hash']==value['integrity'],'Selected material snapshot changed; use a new reviewed selection.')
    require(isinstance(units,list) and bool(units) and all(isinstance(x,str) for x in units) and len(units)==len(set(units)),'Selection needs unique unit IDs.')
    require(value['status'] in ('ready','partial') and set(units)<=set(u['id'] for u in value['units']),'Selection includes unavailable material units.')
    require(selection['hash']==fingerprint({k:v for k,v in selection.items() if k!='hash'}),'Selection hash changed; preserve approved scope.')
    return value


def validate_config(value):
    require(isinstance(value,dict) and set(value)=={'policy','selections'} and value['policy'] in ('strict','supplemented','open'),'materials needs strict/supplemented/open policy and selections.')
    require(isinstance(value['selections'],list) and bool(value['selections']),'Choose at least one material range.')
    for s in value['selections']:
        require(isinstance(s,dict) and set(s)=={'id','version','snapshot_hash','units','hash'},'Invalid material selection.')
        identity(s['id'],s['version']);require(isinstance(s['units'],list) and bool(s['units']),'Select readable units.')
        require(s['hash']==fingerprint({k:v for k,v in s.items() if k!='hash'}),'Selection hash is invalid.')


def scoped(root,selection=None):
    root=Path(root).resolve();config_path=root/'config.json';configured=None
    if config_path.exists():configured=c.read(config_path).get('materials');require(configured is not None,'This course has no approved material scope; propose a new course/version instead of retargeting it.')
    selections=[selection] if selection else (configured or {}).get('selections',[])
    require(bool(selections),'Select a material range before retrieval.')
    if configured:
        validate_config(configured)
        require(all(s in configured['selections'] for s in selections),'Retrieval is outside this course material scope.')
    return selections


def search(root,query,*,selection=None,limit=5):
    require(isinstance(query,str) and bool(query.strip()) and type(limit) is int and 1<=limit<=10,'Provide a query and limit from 1 to 10.')
    terms=set(re.findall(r'[a-z0-9_]+|[\u4e00-\u9fff]',query.casefold()));hits=[]
    for s in scoped(root,selection):
        value=verify_selection(root,s)
        for u in value['units']:
            if u['id'] not in s['units']:continue
            score=sum(u['text'].casefold().count(t) for t in terms)
            if score:hits.append({'id':s['id'],'version':s['version'],'selection_hash':s['hash'],'unit':u['id'],'locator':u['locator'],'text':u['text'],'score':score})
    return sorted(hits,key=lambda x:-x['score'])[:limit]


def citation(root,selection,unit,quote,source_id,*,checked_at=None):
    require(isinstance(source_id,str) and bool(re.fullmatch('S[0-9]+',source_id)),'Use an S-number source ID.')
    scoped(root,selection);value=verify_selection(root,selection)
    found=next((u for u in value['units'] if u['id']==unit and unit in selection['units']),None)
    require(found and isinstance(quote,str) and bool(quote.strip()) and quote in found['text'],'Evidence quote must occur in a selected material unit.')
    ref={'id':selection['id'],'version':selection['version'],'selection_hash':selection['hash'],'unit':unit,'quote':quote}
    result={'id':source_id,'title':value['title'],'publisher':value.get('publisher','User-provided material'),'published_at':'未标注','checked_at':checked_at or (c.today(Path(root)) if (Path(root)/'config.json').exists() else datetime.now(timezone.utc).date().isoformat()),'note':found['locator']+' — '+quote,'material_ref':ref}
    if value.get('url'):result['url']=value['url']
    return result


def validate_source(root,source,config):
    ref=source.get('material_ref');require(isinstance(ref,dict) and set(ref)=={'id','version','selection_hash','unit','quote'},'Material citation needs an exact evidence reference.')
    settings=config.get('materials');require(settings is not None,'Material citations need explicit course material settings.')
    validate_config(settings)
    selected=next((s for s in settings['selections'] if s['id']==ref['id'] and s['version']==ref['version'] and s['hash']==ref['selection_hash']),None)
    require(selected is not None,'Citation references an unselected material/version.')
    value=verify_selection(root,selected);unit=next((u for u in value['units'] if u['id']==ref['unit'] and u['id'] in selected['units']),None)
    require(unit and isinstance(ref['quote'],str) and bool(ref['quote'].strip()) and ref['quote'] in unit['text'],'Citation quote is not supported by the selected original unit.')
    require(unit['locator'] in source.get('note',''),'Delivered source notes must include the actual original locator.')
    require(source.get('url')==value.get('url'),'Material source URL must match the captured public origin (or be absent).')
