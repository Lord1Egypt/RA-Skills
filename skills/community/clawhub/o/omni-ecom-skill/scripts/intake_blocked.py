#!/usr/bin/env python3
"""Close a zero-input run without creating a report or claiming formal delivery."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

from artifact_contract import (native_receipt_identity,validate_receipt_identity,
                               validate_run_scope_identity,validate_stage_identity)
from host_runtime import Runtime


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value,dict): raise ValueError('intake_json_invalid')
    return value


def require(value,reason):
    if not value: raise ValueError(reason)


def main():
    parser=argparse.ArgumentParser(description='无可用文件时安全结束接收阶段，不生成报告')
    parser.add_argument('--run-dir',required=True); parser.add_argument('--run-id',required=True)
    parser.add_argument('--client-scope',required=True); parser.add_argument('--team-version',required=True)
    parser.add_argument('--inventory',default='report-inventory.json')
    parser.add_argument('--run-scope',default='run-scope.json')
    parser.add_argument('--output',default='intake-blocked.json')
    args=parser.parse_args()
    runtime=None
    try:
        root=Path(args.run_dir).resolve(); runtime=Runtime(root,args.run_id,args.client_scope)
        identity=runtime.identity(); require(identity['team_version']==args.team_version,'intake_version_mismatch')
        inventory_path=runtime.path(args.inventory); scope_path=runtime.path(args.run_scope); output=runtime.path(args.output)
        require(inventory_path.is_file() and scope_path.is_file(),'intake_evidence_missing')
        require(output not in (inventory_path,scope_path),'intake_output_overlaps_input')
        inventory=read(inventory_path); scope=read(scope_path)
        validate_stage_identity(inventory,'report_inventory',args.team_version,args.run_id,args.client_scope)
        validate_run_scope_identity(scope,args.team_version,args.run_id,args.client_scope)
        require(inventory.get('report_count')==0 and inventory.get('reports')==[],'intake_inventory_not_empty')
        require(scope.get('status')=='scope_blocked' and scope.get('errors')==['run_scope_no_files'] and
                scope.get('files')==[] and scope.get('scanned_files')==0,'intake_scope_not_zero_input')
        artifacts=[{'file':args.inventory,'sha256':sha(inventory_path),'bytes':inventory_path.stat().st_size},
                   {'file':args.run_scope,'sha256':sha(scope_path),'bytes':scope_path.stat().st_size}]
        if output.exists():
            receipt=read(output); validate_receipt_identity(receipt,'intake_blocked',args.team_version)
            require(receipt.get('run_id')==args.run_id and receipt.get('client_scope')==args.client_scope and
                    receipt.get('artifacts')==artifacts,'intake_existing_receipt_stale')
        else:
            receipt=dict(**native_receipt_identity('intake_blocked',args.team_version),run_id=args.run_id,
                client_scope=args.client_scope,team_version=args.team_version,status='closed_without_report_data_required',
                reason_code='no_supported_files',report_generated=False,formal_delivery_completed=False,
                artifacts=artifacts,next_action='请上传本次客户范围内的原始报表后创建新运行',
                checked_at=datetime.now(timezone.utc).isoformat())
            with output.open('x',encoding='utf-8') as handle:
                handle.write(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        receipt_hash=sha(output)
        event=dict(**native_receipt_identity('intake_blocked_event',args.team_version),
                   receipt_file=args.output,receipt_sha256=receipt_hash,reason_code='no_supported_files',
                   report_generated=False)
        runtime.journal.append(args.run_id,args.client_scope,'intake-blocked','intake_blocked',event)
        print(json.dumps({'status':receipt['status'],'receipt':args.output,'receipt_sha256':receipt_hash,
                          'formal_delivery_completed':False},ensure_ascii=False))
        return 0
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'intake_blocked_failed','reason':str(exc)},ensure_ascii=False))
        return 1
    finally:
        if runtime is not None: runtime.close()


if __name__=='__main__': raise SystemExit(main())
