#!/usr/bin/env python3
"""Preflight before plant/retrieve — stack tools, no secret paths in egg catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _stack_paths import resolve_stack_root

FORBIDDEN_FRAGMENTS = ("API_KEY", "APIKEY", "token_backup", "NzI1MD", "xai-", "nvapi-")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-root", default=None)
    args = ap.parse_args()
    stack = resolve_stack_root(args.stack_root)
    ok = True
    print("Δ9Φ963 Egg Planter preflight")
    print(f"  stack: {stack}")

    reg = stack / "data" / "kernel_eggs" / "registry.json"
    if reg.is_file():
        reg_data = json.loads(reg.read_text(encoding="utf-8"))
        root = reg_data.get("registry_merkle_root", "")[:24]
        print(f"  registry: present merkle={root}…")
        for e in reg_data.get("eggs", []):
            for art in []:  # decoded at verify time
                pass
    else:
        print("  registry: (none yet — first plant will create)")

    for rel in (
        "tools/build_kernel_eggs.py",
        "tools/verify_kernel_eggs.py",
        "tools/retrieve_kernel_egg.py",
        "protocol0_byte_entropy_filter/fixtures/p0_canonical.sha256",
    ):
        if not (stack / rel).is_file():
            print(f"  [FAIL] missing {rel}")
            ok = False
        else:
            print(f"  ok: {rel}")

    catalog = stack / "tools" / "kernel_egg_catalog.py"
    if catalog.is_file():
        text = catalog.read_text(encoding="utf-8", errors="replace")
        for bad in FORBIDDEN_FRAGMENTS:
            if bad.lower() in text.lower():
                print(f"  [WARN] catalog mentions forbidden fragment pattern (review): {bad}")
    print("preflight: PASS" if ok else "preflight: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())