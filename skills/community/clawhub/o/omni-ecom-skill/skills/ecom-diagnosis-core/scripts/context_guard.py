#!/usr/bin/env python3
"""Create a source-bound 2.0 read-scope receipt for one authoritative run."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PACKAGE_ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(PACKAGE_ROOT/'scripts'))

from artifact_contract import native_run_scope_identity,validate_run_scope_identity
from host_runtime import Runtime

TEXT_SUFFIXES={'.csv','.json','.md','.txt','.yaml','.yml','.py','.ps1'}


def inside(root:Path,candidate:Path)->bool:
    try: candidate.resolve().relative_to(root.resolve()); return True
    except ValueError: return False


def files_under(path:Path)->list[Path]:
    if path.is_file(): return [path]
    if path.is_dir(): return [item for item in path.rglob('*') if item.is_file()]
    return []


def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main()->int:
    parser=argparse.ArgumentParser(description='生成并校验本次任务允许读取的 2.0 范围凭证')
    parser.add_argument('--run-dir',required=True)
    parser.add_argument('--client-scope',required=True)
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--team-version',required=True)
    parser.add_argument('--allowed-root',action='append',required=True)
    parser.add_argument('--path',action='append',required=True)
    parser.add_argument('--forbid-term',action='append',default=[])
    parser.add_argument('--output',required=True)
    args=parser.parse_args()

    run_dir=Path(args.run_dir).resolve(); output=Path(args.output).resolve()
    errors=[]; allowed=[Path(value).resolve() for value in args.allowed_root]
    inputs=[Path(value).resolve() for value in args.path]
    try:
        if not run_dir.is_dir(): raise ValueError('run_scope_run_directory_missing')
        if not inside(run_dir,output): raise ValueError('run_scope_output_outside_run')
        runtime=Runtime(run_dir,args.run_id,args.client_scope,read_only=True)
        try:
            identity=runtime.identity()
            if identity['team_version']!=args.team_version: raise ValueError('run_scope_version_mismatch')
        finally: runtime.close()
    except (OSError,ValueError) as exc:
        errors.append(str(exc))
    for root in allowed:
        if not root.exists(): errors.append('allowed_root_missing')
        elif not inside(run_dir,root): errors.append('allowed_root_outside_run')
    for path in inputs:
        if not any(inside(root,path) for root in allowed): errors.append('input_path_outside_allowed_root')
        elif not path.exists(): errors.append('input_path_missing')
        elif path.is_dir() and inside(path,output): errors.append('scope_output_inside_input_path')
        elif path==output: errors.append('scope_output_overwrites_input')

    files=[]; seen=set()
    for path in inputs:
        if not path.exists() or not inside(run_dir,path) or not any(inside(root,path) for root in allowed): continue
        for file_path in files_under(path):
            relative=file_path.relative_to(run_dir).as_posix()
            if relative in seen: continue
            seen.add(relative)
            original=sha(file_path)
            if file_path.suffix.casefold() in TEXT_SUFFIXES:
                try: text=file_path.read_text(encoding='utf-8-sig')
                except (OSError,UnicodeDecodeError): text=''
                for term in args.forbid_term:
                    if term and term.casefold() in text.casefold(): errors.append('forbidden_cross_scope_term:'+relative)
            if sha(file_path)!=original: errors.append('scope_input_changed_during_scan:'+relative)
            files.append({'file':relative,'sha256':original,'size_bytes':file_path.stat().st_size})
    if not files: errors.append('run_scope_no_files')
    payload=dict(**native_run_scope_identity(args.team_version),run_id=args.run_id,
                 client_scope=args.client_scope,team_version=args.team_version,
                 status='scope_verified' if not errors else 'scope_blocked',
                 allowed_roots=[path.relative_to(run_dir).as_posix() if inside(run_dir,path) else str(path) for path in allowed],
                 input_paths=[path.relative_to(run_dir).as_posix() if inside(run_dir,path) else str(path) for path in inputs],
                 files=files,scanned_files=len(files),errors=sorted(set(errors)))
    validate_run_scope_identity(payload,args.team_version,args.run_id,args.client_scope)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':payload['status'],'output':output.name,'scanned_files':len(files),'errors':payload['errors']},ensure_ascii=False))
    return 0 if not errors else 1


if __name__=='__main__': raise SystemExit(main())
