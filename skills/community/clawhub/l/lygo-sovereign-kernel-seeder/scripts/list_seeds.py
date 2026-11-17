#!/usr/bin/env python3
"""List sovereign seeds in registry."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed_kernel import default_seed_root, load_registry  # type: ignore


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root) if args.root else default_seed_root()
    reg = load_registry(root / "registry.json")
    eggs = reg.get("eggs") or {}
    if args.json:
        print(json.dumps({"registry_merkle_root": reg.get("registry_merkle_root"), "eggs": eggs}, indent=2))
        return 0
    print(f"root={root}")
    print(f"registry_merkle_root={reg.get('registry_merkle_root')}")
    print(f"count={len(eggs)}")
    for eid, m in sorted(eggs.items()):
        print(f"  {eid}  v{m.get('version')}  {m.get('kind')}  {m.get('content_sha256', '')[:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
