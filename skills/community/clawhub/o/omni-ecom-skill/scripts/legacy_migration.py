"""Copy legacy v1 handoff/action/report JSON into read-only v2 history objects.

Never edits originals, inherits approval, replays an action, or manufactures a
current Agent return. Restoration creates a NEW directory, never an overwrite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

from run_journal import check_payload,digest,encoded

ROOT=Path(__file__).resolve().parents[1]
SCHEMAS={'handoff':'handoff.schema.json','action':'action-record.schema.json','report':'report-package.schema.json',
         'claim':'claim-ledger.schema.json'}
MIGRATOR_VERSION='2.0.3-candidate.1'
MAX_FILE_BYTES=64*1024*1024
MAX_TOTAL_BYTES=256*1024*1024


def require(value,reason):
    if not value: raise ValueError(reason)


def sha_bytes(value): return hashlib.sha256(value).hexdigest()
def sha(path): return sha_bytes(Path(path).read_bytes())


def unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'migration_duplicate_json_key')
        result[key]=value
    return result


def decode(raw):
    def reject_constant(value): raise ValueError('migration_nonfinite_json')
    value=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=unique_object,parse_constant=reject_constant)
    require(isinstance(value,dict),'migration_json_root_invalid')
    return value


def read(path):
    path=Path(path)
    require(path.is_file() and path.stat().st_size<=MAX_FILE_BYTES,'migration_input_missing_or_too_large')
    raw=path.read_bytes()
    require(len(raw)<=MAX_FILE_BYTES,'migration_input_missing_or_too_large')
    return decode(raw)


def inside(root,relative):
    require(isinstance(relative,str) and relative and not Path(relative).is_absolute(),'migration_path_invalid')
    path=(root/relative).resolve()
    require(path.is_relative_to(root) and path!=root,'migration_path_outside')
    return path


def validate_legacy(kind,payload,client_scope,allowed_stores):
    require(kind in SCHEMAS,'migration_kind_unknown')
    require(payload.get('schema_version')=='1.0','migration_schema_version_unsupported')
    check_payload(payload)
    try:
        from jsonschema import Draft202012Validator,FormatChecker
    except ImportError as exc:
        raise ValueError('migration_validator_unavailable_install_jsonschema') from exc
    schema=read(ROOT/'schemas'/'legacy-v1'/SCHEMAS[kind])
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(payload))
    require(not errors,'migration_legacy_contract_invalid:'+kind)
    claimed=payload.get('client_scope')
    if kind in ('report','action','claim') or claimed is not None:
        require(claimed==client_scope,'migration_client_scope_mismatch')
    scope=payload.get('scope',{})
    store=scope.get('store') if isinstance(scope,dict) else None
    if store is not None:
        require(store in allowed_stores,'migration_store_not_allowed')
    if kind=='handoff' and claimed is None:
        require(store in allowed_stores,'migration_legacy_scope_unresolved')


def normalize(kind,payload,client_scope,source):
    legacy_id=payload.get('action_id') if kind=='action' else (
        payload['run_id']+':'+payload['agent_id'] if kind=='handoff' else payload['run_id'])
    identity=digest(dict(kind=kind,source_sha256=source['sha256'],legacy_id=legacy_id,client_scope=client_scope))
    result=dict(schema_version='2.0',entity_type='legacy_'+kind,record_id='legacy-'+identity,
        client_scope=client_scope,legacy_id=legacy_id,legacy_run_id=payload['run_id'],
        migration_status='historical_reference_only',migrator_version=MIGRATOR_VERSION,
        permissions=dict(current_agent_return=False,execution_allowed=False,approval_inherited=False),
        origin=dict(**source,source_schema_version='1.0',
                    source_team_version=payload.get('agent_version',payload.get('team_version'))))
    if kind=='action':
        result['proposal']={key:payload.get(key) for key in ('action','priority','owner','target','baseline','acceptance','stop_condition','source_ids')}
        result['historical_execution']={key:payload.get(key) for key in ('status','approval_required','approval_state','proposed_at',
                                    'approved_at','executed_at','verified_at','outcome','artifact_refs')}
        result['current_execution']=dict(status='not_authorized',approval_state='requires_new_authorization',replay_allowed=False)
    elif kind=='claim':
        result['historical_content']={key:payload.get(key) for key in
            ('period','additional_periods','scope','source_context_policy','claims')}
        result['current_validation']=dict(status='not_revalidated',claim_guard_receipt=None,
                                          source_context_verified=False)
        result['permissions']['current_numeric_evidence']=False
    else:
        names=('scope','gate_status','status','facts','judgments','hypotheses','actions','risks','missing_data','evidence_ledger') if kind=='handoff' else (
               'title','period','scope','gate_status','status','data_gate','metrics','facts','judgments','hypotheses','actions','missing_data','risks','sources','provenance')
        result['historical_content']={key:payload.get(key) for key in names}
        result['current_validation']=dict(status='not_revalidated',review_attestation=None,agent_task_id=None)
        if kind=='handoff':
            result['historical_agent']=dict(role=payload['agent_id'],task_id=payload.get('agent_task_id'))
    return result


def prepare(source_root,plan,client_scope,allowed_stores):
    root=Path(source_root).resolve()
    require(root.is_dir(),'migration_source_root_missing')
    require(isinstance(client_scope,str) and bool(client_scope.strip()),'migration_scope_required')
    require(isinstance(plan,dict),'migration_plan_invalid')
    require(plan.get('client_scope')==client_scope,'migration_plan_scope_mismatch')
    files=plan.get('files')
    require(isinstance(files,list) and 0<len(files)<=500,'migration_file_list_invalid')
    allowed_stores=set(allowed_stores or [client_scope])
    seen=set(); record_ids=set(); selected=[]; total=0
    for index,item in enumerate(files):
        require(isinstance(item,dict),'migration_file_entry_invalid')
        kind=item.get('kind'); path=inside(root,item.get('file'))
        require(path not in seen,'migration_duplicate_source'); seen.add(path)
        require(path.suffix.lower()=='.json' and path.is_file(),'migration_source_not_json')
        require(path.stat().st_size<=MAX_FILE_BYTES,'migration_input_missing_or_too_large')
        raw=path.read_bytes(); total+=len(raw)
        require(len(raw)<=MAX_FILE_BYTES,'migration_input_missing_or_too_large')
        require(total<=MAX_TOTAL_BYTES,'migration_total_size_exceeded')
        payload=decode(raw)
        validate_legacy(kind,payload,client_scope,allowed_stores)
        require(sha(path)==sha_bytes(raw),'migration_source_changed')
        source=dict(relative_path=str(path.relative_to(root)),sha256=sha_bytes(raw),bytes=len(raw),
                    backup_file=f'originals/{index:04d}-{kind}.json')
        converted=normalize(kind,payload,client_scope,source)
        require(converted['record_id'] not in record_ids,'migration_duplicate_record')
        record_ids.add(converted['record_id'])
        # Ensure any unexpected nonfinite value fails before creating a target.
        encoded(converted)
        selected.append(dict(kind=kind,path=path,raw=raw,source=source,record=converted,
                             record_file=f'records/{index:04d}-{kind}.json'))
    return root,selected


def write_bytes(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream: stream.write(raw)


def write_json(path,value): write_bytes(path,(encoded(value)+'\n').encode('utf-8'))


def migrate(source_root,plan,output,client_scope,allowed_stores=()):
    root,selected=prepare(source_root,plan,client_scope,allowed_stores)
    target=Path(output).resolve()
    require(not target.exists(),'migration_target_already_exists')
    require(not target.is_relative_to(root) and not root.is_relative_to(target),'migration_source_target_overlap')
    planned=dict(schema_version='2.0',client_scope=client_scope,migrator_version=MIGRATOR_VERSION,
                 state='migration_planned_not_complete',files=[dict(kind=i['kind'],source=i['source'],record_file=i['record_file']) for i in selected])
    target.mkdir(parents=True,exist_ok=False)
    write_json(target/'migration-plan.json',planned)
    results=[]
    for item in selected:
        require(sha(item['path'])==item['source']['sha256'],'migration_source_changed')
        backup=inside(target,item['source']['backup_file'])
        destination=inside(target,item['record_file'])
        write_bytes(backup,item['raw']); write_json(destination,item['record'])
        require(sha(backup)==item['source']['sha256'],'migration_backup_mismatch')
        results.append(dict(kind=item['kind'],record_file=item['record_file'],record_sha256=sha(destination),
                            source=item['source'],record_id=item['record']['record_id']))
    for item in selected:
        require(sha(item['path'])==item['source']['sha256'],'migration_source_changed')
    receipt=dict(schema_version='2.0',status='migration_copy_verified',client_scope=client_scope,
                 migrator_version=MIGRATOR_VERSION,created_at=datetime.now(timezone.utc).isoformat(),
                 plan_sha256=sha(target/'migration-plan.json'),records=results,
                 originals_modified=False,permissions_inherited=False,current_runtime_verified=False)
    write_json(target/'migration-receipt.json',receipt)
    verify(target,client_scope,sha(target/'migration-receipt.json'))
    return receipt,sha(target/'migration-receipt.json')


def verify(migration_dir,client_scope,expected_receipt_sha256):
    root=Path(migration_dir).resolve(); receipt_path=root/'migration-receipt.json'
    require(receipt_path.is_file() and sha(receipt_path)==expected_receipt_sha256,'migration_receipt_missing_or_changed')
    receipt=read(receipt_path)
    require(receipt.get('status')=='migration_copy_verified' and receipt.get('schema_version')=='2.0' and
            receipt.get('client_scope')==client_scope and receipt.get('permissions_inherited') is False and
            receipt.get('current_runtime_verified') is False,'migration_receipt_invalid')
    require(sha(root/'migration-plan.json')==receipt.get('plan_sha256'),'migration_plan_changed')
    plan=read(root/'migration-plan.json')
    require(plan.get('client_scope')==client_scope and len(plan.get('files',[]))==len(receipt.get('records',[]))>0,'migration_plan_mismatch')
    expected={root/'migration-plan.json',receipt_path}; ids=set()
    for item,planned in zip(receipt['records'],plan['files']):
        require(all(item.get(k)==planned.get(k) for k in ('kind','source','record_file')),'migration_plan_mismatch')
        source=item['source']; backup=inside(root,source['backup_file']); path=inside(root,item['record_file'])
        require(backup not in expected and path not in expected and path!=backup,'migration_duplicate_artifact')
        expected.update((backup,path))
        require(sha(backup)==source['sha256'] and backup.stat().st_size==source['bytes'],'migration_backup_changed')
        require(sha(path)==item['record_sha256'],'migration_record_changed')
        raw=read(backup); record=read(path)
        require(record==normalize(item['kind'],raw,client_scope,source),'migration_normalization_mismatch')
        require(record['record_id']==item['record_id'] and item['record_id'] not in ids,'migration_record_id_invalid')
        ids.add(item['record_id'])
    actual={p.resolve() for p in root.rglob('*') if p.is_file()}
    require(actual==expected,'migration_unexpected_or_missing_files')
    return receipt


def restore(migration_dir,output,client_scope,expected_receipt_sha256):
    root=Path(migration_dir).resolve()
    receipt=verify(root,client_scope,expected_receipt_sha256)
    target=Path(output).resolve()
    require(not target.exists(),'migration_restore_target_exists')
    require(not target.is_relative_to(root) and not root.is_relative_to(target),'migration_restore_overlap')
    # Validate all historical relative names before creating the new directory.
    paths=[inside(target,item['source']['relative_path']) for item in receipt['records']]
    require(len(paths)==len(set(paths)),'migration_restore_duplicate_path')
    target.mkdir(parents=True,exist_ok=False)
    restored=[]
    for item,path in zip(receipt['records'],paths):
        source=item['source']; backup=inside(root,source['backup_file'])
        raw=backup.read_bytes()
        require(sha_bytes(raw)==source['sha256'],'migration_backup_changed')
        write_bytes(path,raw)
        require(sha(path)==source['sha256'],'migration_restore_mismatch')
        restored.append(dict(file=source['relative_path'],sha256=source['sha256']))
    return dict(schema_version='2.0',status='legacy_copy_restored',client_scope=client_scope,files=restored,
                original_directory_overwritten=False,platform_actions_replayed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    move=sub.add_parser('migrate'); move.add_argument('--source-root',required=True); move.add_argument('--plan',required=True)
    move.add_argument('--output',required=True); move.add_argument('--allow-store',action='append',default=[])
    for command in ('verify','restore'):
        p=sub.add_parser(command); p.add_argument('--migration-dir',required=True); p.add_argument('--receipt-sha256',required=True)
        if command=='restore': p.add_argument('--output',required=True)
    for p in sub.choices.values(): p.add_argument('--client-scope',required=True)
    args=parser.parse_args()
    try:
        if args.command=='migrate':
            receipt,fingerprint=migrate(args.source_root,read(args.plan),args.output,args.client_scope,args.allow_store)
            result=dict(status=receipt['status'],files=len(receipt['records']),receipt_sha256=fingerprint)
        elif args.command=='verify':
            receipt=verify(args.migration_dir,args.client_scope,args.receipt_sha256)
            result=dict(status='migration_integrity_verified',files=len(receipt['records']))
        else:
            result=restore(args.migration_dir,args.output,args.client_scope,args.receipt_sha256)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (ValueError,OSError,KeyError,TypeError,RecursionError) as exc:
        print(json.dumps(dict(status='migration_blocked',reason=str(exc)),ensure_ascii=False)); return 2


if __name__=='__main__': raise SystemExit(main())
