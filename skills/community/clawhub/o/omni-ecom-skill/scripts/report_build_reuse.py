"""Reuse unchanged draft builds; frozen artifacts are never overwritten."""
import hashlib
import json
from pathlib import Path

ARTIFACTS=('report.json','report.md','report.pdf','pdf-delivery.json','claim-receipt.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def signature(args,root):
    options=vars(args).copy()
    for key in ('format','output_dir'):options.pop(key,None)
    inputs={}
    for key in ('handoff','metrics','config','action_store','version_info','decision_pack','report_inventory','report_clusters',
                'chapter_plan','coverage_gate','claim_ledger','previous_action_review'):
        value=getattr(args,key,None)
        if value and Path(value).is_file():inputs[str(Path(value).resolve())]=sha(Path(value))
    for value in getattr(args,'member_handoff',[]) or []:
        path=Path(value).resolve(); inputs[str(path)]=sha(path)
    # Actual original sources referenced by claims are part of the cache key.
    ledger=Path(args.claim_ledger).resolve()
    for name in ('quality-inputs.json','run-scope.json','baseline-pack.json','conflict-verdict.json'):
        path=ledger.parent/name
        if path.is_file():inputs[str(path)]=sha(path)
    scope=ledger.parent/'run-scope.json'
    if scope.is_file():
        scope_body=json.loads(scope.read_text(encoding='utf-8-sig'))
        for row in scope_body.get('files',[]):
            path=(ledger.parent/row['file']).resolve()
            if not path.is_relative_to(ledger.parent):raise ValueError('report_reuse_scope_outside_run')
            inputs[str(path)]=sha(path)
    quality=ledger.parent/'quality-inputs.json'
    if quality.is_file():
        quality_body=json.loads(quality.read_text(encoding='utf-8-sig'))
        refs=[quality_body.get(k) for k in ('inventory','chapter_plan','baseline','adjudication','run_scope')]
        refs.extend(quality_body.get('handoffs',{}).values())
        for value in refs:
            if value:
                path=(ledger.parent/value).resolve()
                if not path.is_relative_to(ledger.parent):raise ValueError('report_reuse_quality_outside_run')
                inputs[str(path)]=sha(path)
    claims=json.loads(ledger.read_text(encoding='utf-8-sig'))
    for row in claims.get('claims',[]):
        value=row.get('source_ref',{}).get('source_file')
        if value:
            path=(ledger.parent/value).resolve()
            if not path.is_relative_to(ledger.parent):raise ValueError('report_reuse_source_outside_run')
            inputs[str(path)]=sha(path)
    code={p.relative_to(root).as_posix():sha(p) for folder in ('scripts','schemas','config')
          for p in (root/folder).rglob('*') if p.is_file() and p.suffix in ('.py','.json','.md')}
    code['version-info.json']=sha(root/'version-info.json')
    native_binding={}
    if (ledger.parent/'run-journal.sqlite').is_file():
        from host_runtime import Runtime
        runtime=Runtime(ledger.parent,claims['run_id'],claims['client_scope'],read_only=True)
        try:
            state=runtime.status()
            native_binding={k:v for k,v in state.get('selected_returns',{}).items() if k!='delivery-review'}
        finally:runtime.close()
    from client_registry import resolve_client_registry
    registry=resolve_client_registry(root)
    if registry.is_file():inputs[str(registry.resolve())]=sha(registry)
    body=json.dumps({'options':options,'inputs':inputs,'code':code,'native_binding':native_binding},ensure_ascii=False,sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()

def existing(args,root):
    directory=Path(args.output_dir).resolve()
    key=signature(args,root)
    receipt=directory/'report-build-receipt.json'
    if receipt.is_file():
        old=json.loads(receipt.read_text(encoding='utf-8-sig'))
        if old.get('input_sha256')==key:
            if all((directory/name).is_file() and sha(directory/name)==digest for name,digest in old.get('artifacts',{}).items()) and set(old.get('artifacts',{}))==set(ARTIFACTS):
                return key,old
    if any(directory.glob('review-manifest*.json')) or (directory/'completion-receipt.json').exists():
        raise ValueError('frozen_report_requires_new_revision_directory')
    return key,None

def record(directory,key):
    directory=Path(directory)
    receipt={'status':'report_build_complete_not_delivery','input_sha256':key,
             'artifacts':{name:sha(directory/name) for name in ARTIFACTS}}
    path=directory/'report-build-receipt.json'
    path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return receipt

