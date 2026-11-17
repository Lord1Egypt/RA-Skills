#!/usr/bin/env python3
"""Verify sovereign seed registry + eggs. Exit 0 ALIGNED, 3 QUARANTINE."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# import helpers from seed_kernel
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed_kernel import (  # type: ignore
    default_seed_root,
    load_registry,
    recompute_root,
    verify_egg_object,
    SIG,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--egg", default="", help="Verify single egg_id")
    args = ap.parse_args()
    root = Path(args.root) if args.root else default_seed_root()
    reg_path = root / "registry.json"
    eggs_dir = root / "eggs"

    report = {
        "seeder": SIG,
        "root": str(root),
        "verdict": "ALIGNED",
        "errors": [],
        "eggs_checked": 0,
        "registry_merkle_root": None,
        "computed_merkle_root": None,
    }

    if not reg_path.is_file():
        report["verdict"] = "EMPTY"
        report["errors"].append("no registry.json")
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print("EMPTY — no registry")
        return 0

    registry = load_registry(reg_path)
    report["registry_merkle_root"] = registry.get("registry_merkle_root")
    computed = recompute_root(registry)
    report["computed_merkle_root"] = computed
    if computed != registry.get("registry_merkle_root"):
        report["verdict"] = "QUARANTINE"
        report["errors"].append("registry_merkle_root mismatch")

    eggs = registry.get("eggs") or {}
    if args.egg:
        eggs = {args.egg: eggs[args.egg]} if args.egg in eggs else {}
        if not eggs:
            report["verdict"] = "QUARANTINE"
            report["errors"].append(f"egg not in registry: {args.egg}")

    for eid, meta in eggs.items():
        report["eggs_checked"] += 1
        path = eggs_dir / (meta.get("path") or f"{eid}.egg.json")
        if not path.is_file():
            report["verdict"] = "QUARANTINE"
            report["errors"].append(f"missing egg file {path.name}")
            continue
        try:
            egg = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            report["verdict"] = "QUARANTINE"
            report["errors"].append(f"{eid}: parse error {e}")
            continue
        errs = verify_egg_object(egg)
        if errs:
            report["verdict"] = "QUARANTINE"
            report["errors"].extend([f"{eid}: {e}" for e in errs])
        if meta.get("content_sha256") != egg.get("content_sha256"):
            report["verdict"] = "QUARANTINE"
            report["errors"].append(f"{eid}: registry content_sha256 drift")
        if meta.get("leaf_hash") != egg.get("seal", {}).get("leaf_hash"):
            report["verdict"] = "QUARANTINE"
            report["errors"].append(f"{eid}: registry leaf_hash drift")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"verdict={report['verdict']} eggs={report['eggs_checked']} root={report['computed_merkle_root']}")
        for e in report["errors"]:
            print(f"  ERROR: {e}")

    return 0 if report["verdict"] in ("ALIGNED", "EMPTY") else 3


if __name__ == "__main__":
    sys.exit(main())
