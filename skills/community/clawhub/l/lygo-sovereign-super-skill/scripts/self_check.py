#!/usr/bin/env python3
"""Self-check sovereign super skill (optional stack)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _stack_paths import resolve_stack_root  # noqa: E402

SKILL = HERE.parent
CATALOG = SKILL / "references" / "EGG_CATALOG.md"


def main() -> int:
    if not (SKILL / "SKILL.md").is_file():
        print("FAIL missing SKILL.md")
        return 1
    if not CATALOG.is_file():
        print("FAIL missing EGG_CATALOG.md")
        return 1
    try:
        root = resolve_stack_root()
    except SystemExit:
        print("OK lygo-sovereign-super-skill self_check (skill-only; set LYGO_STACK_ROOT for stack checks)")
        return 0
    sys.path.insert(0, str(root / "tools"))
    from kernel_egg_catalog import EGG_SPECS  # noqa: E402

    reg_path = root / "data" / "kernel_eggs" / "registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    ids = {e["egg_id"] for e in reg.get("eggs", [])}
    spec_ids = set(EGG_SPECS.keys())
    if ids != spec_ids:
        print(f"FAIL registry mismatch catalog={len(spec_ids)} registry={len(ids)}")
        return 1
    print(f"OK lygo-sovereign-super-skill self_check eggs={len(ids)} stack={root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())