#!/usr/bin/env python3
"""Write book-brain reference stubs for planted eggs (user-owned files)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def require_consent(flag: bool) -> None:
    if flag or os.environ.get("LYGO_EGG_PLANT_CONSENT", "").lower() in ("yes", "1", "true"):
        return
    raise SystemExit(2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-consent", action="store_true")
    ap.add_argument("--stack-root", required=True)
    ap.add_argument("--out", default="reference/LYGO_KERNEL_EGGS.ref.txt")
    args = ap.parse_args()
    require_consent(args.i_consent)

    stack = Path(args.stack_root)
    reg_path = stack / "data" / "kernel_eggs" / "registry.json"
    if not reg_path.is_file():
        raise SystemExit("No registry — plant eggs first")

    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    verify_path = stack / "tests" / "kernel_eggs_last_run.json"
    verdict = "unknown"
    if verify_path.is_file():
        verdict = json.loads(verify_path.read_text(encoding="utf-8")).get("verdict", "unknown")
    lines = [
        "# LYGO Kernel Eggs — book-brain reference stub",
        f"# generated {datetime.now(timezone.utc).isoformat()}",
        f"tamper_verdict: {verdict}",
        f"registry_merkle_root: {reg.get('registry_merkle_root')}",
        f"git_head: {reg.get('git_head')}",
        "retrieval: https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html",
        "cli: python tools/retrieve_kernel_egg.py --list",
        "",
    ]
    for a in reg.get("anchored", []):
        lines.append(f"egg:{a.get('egg_id')} sha256:{(a.get('content_sha256') or '')[:16]}… url:{a.get('url', '')}")
    out = Path(args.out)
    if not out.is_absolute():
        out = SKILL_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[stubs] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())