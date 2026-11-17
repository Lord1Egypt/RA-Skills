#!/usr/bin/env python3
"""Install the version/hash-pinned webchat-only Active Memory compatibility guard."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from core.safe_fs import atomic_write_bytes, lexical_path, read_bytes
from scripts.configure_native_memory import protected_backup, GUARD_MARKER, SCOPE_MARKER, verify_runtime_guard

VERSION="2026.9.5"
ORIGINAL_SHA256="b709fab02c05e8d90846a96e9fc58b86ac14055af8b5e2402dcbad1c83645eae"
PATCHED_SHA256="a56adeaaae73a2805235c1578a3fcb8d8c56291014d1ca5aab84b05bdde7a766"

def digest(data): return hashlib.sha256(data).hexdigest()

def patched_bytes(raw: bytes) -> bytes:
    if digest(raw)==PATCHED_SHA256: return raw
    if digest(raw)!=ORIGINAL_SHA256:
        raise ValueError("runtime file changed; refuse an unreviewed patch")
    text=raw.decode("utf-8")
    start='\t\tapi.on("before_prompt_build", async (event, ctx) => {\n'
    gate='\t\t\t\t\tif (activeMemoryConfigured && effectiveAgentId && deterministicRecallToolName'
    if text.count(start)!=1 or text.count(gate)!=1:
        raise ValueError("unexpected runtime patch anchors")
    text=text.replace(start,start+'\t\t\t'+SCOPE_MARKER+'\n\t\t\tif ((ctx.messageProvider ?? "").trim().toLowerCase() !== "webchat") return;\n',1)
    text=text.replace(gate,'\t\t\t\t\t'+GUARD_MARKER+'\n\t\t\t\t\tif (activeMemoryConfigured && isAllowedChatType(invocationConfig, destinationContext) && effectiveAgentId && deterministicRecallToolName',1)
    updated=text.encode("utf-8")
    if digest(updated)!=PATCHED_SHA256:
        raise ValueError("patched runtime hash mismatch")
    return updated

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-entry",required=True)
    parser.add_argument("--backup-dir",required=True)
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args(argv)
    entry=lexical_path(args.runtime_entry)
    if json.loads(read_bytes(entry.parents[3]/"package.json")).get("version")!=VERSION:
        raise ValueError("runtime version changed; re-audit before patching")
    raw=read_bytes(entry); updated=patched_bytes(raw)
    report={"mode":"apply" if args.apply else "preview","version":VERSION,
            "changed":raw!=updated,"original_sha256":digest(raw),"patched_sha256":digest(updated),
            "scope":"webchat only; host entry retains authentication responsibility"}
    if args.apply and raw!=updated:
        backup=lexical_path(args.backup_dir)/("active-memory-before-hui-yi-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".js")
        protected_backup(entry,backup,raw)
        if read_bytes(entry)!=raw: raise ValueError("runtime changed during preparation")
        atomic_write_bytes(entry,updated)
        verify_runtime_guard(entry)
        if digest(read_bytes(entry))!=PATCHED_SHA256: raise ValueError("installed runtime verification failed")
        report["backup_path"]=str(backup)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except (OSError,ValueError) as exc:
        print(json.dumps({"ok":False,"error_type":type(exc).__name__}),file=sys.stderr)
        raise SystemExit(1)
