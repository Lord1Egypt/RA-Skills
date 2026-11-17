#!/usr/bin/env python3
"""Safely extract a validated LaTeX project ZIP."""
import argparse, json, shutil, zipfile
from pathlib import Path, PurePosixPath
from check_supported_input import inspect_latex_zip, safe_member

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("zip",type=Path); parser.add_argument("output_dir",type=Path); parser.add_argument("--main"); args=parser.parse_args()
    payload,code=inspect_latex_zip(args.zip)
    if code not in {0,4}: print(json.dumps(payload,ensure_ascii=False,indent=2)); return code
    candidates=payload.get("candidates") or [payload.get("main_tex")]; main_tex=args.main or payload.get("main_tex")
    if not main_tex or main_tex not in candidates: print(json.dumps({"status":"needs_main_selection","candidates":candidates},ensure_ascii=False,indent=2)); return 4
    destination=args.output_dir.resolve(); destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.zip) as package:
        for info in package.infolist():
            if not safe_member(info.filename): raise RuntimeError("unsafe ZIP member")
            target=(destination/PurePosixPath(info.filename)).resolve()
            if destination!=target and destination not in target.parents: raise RuntimeError("ZIP member escapes output directory")
            if info.is_dir(): target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                with package.open(info) as source,target.open("wb") as output: shutil.copyfileobj(source,output)
    print(json.dumps({"status":"extracted","output_dir":str(destination),"main_tex":str(destination/PurePosixPath(main_tex))},ensure_ascii=False,indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
