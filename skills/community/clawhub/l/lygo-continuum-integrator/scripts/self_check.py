#!/usr/bin/env python3
"""Skill self-check — pure local, no network."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import integrator_cli as ic  # noqa: E402

BANNED_IMPORTS = {"subprocess"}


def _ast_banned(path: Path) -> list[str]:
    hits: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in BANNED_IMPORTS:
                    hits.append(f"import:{a.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = (node.module or "").split(".")[0]
            if mod in BANNED_IMPORTS:
                hits.append(f"from:{mod}")
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id == "os" and f.attr in {"system", "popen"}:
                    hits.append(f"call:os.{f.attr}")
    return hits


def main() -> int:
    checks: dict = {
        "signature": ic.SIG,
        "version": ic.VERSION,
        "ast_clean": True,
        "integrate": False,
        "phase_lock": False,
        "emit_receipt": False,
        "verify_lock": False,
        "collapse_refused": False,
        "ok": False,
    }

    bad: list[str] = []
    for p in sorted(HERE.glob("*.py")):
        bad.extend(f"{p.name}:{h}" for h in _ast_banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    integ = ic.integrate("Eternal Truth", "Creative Chaos", node_id="self-check")
    checks["integrate"] = bool(integ.get("ok")) and float((integ.get("integral") or {}).get("value") or -1) >= 0

    # force collapse probe
    collapsed = ic.build_psi("x", "y")
    # manually break
    bad_psi = {
        "ok": True,
        "psi": {
            "prob_truth": 0.0,
            "prob_chaos": 1.0,
            "collapse": True,
            "interference": "constructive",
            "phase_truth": 0.0,
        },
        "receipt_sha256": "00",
        "integral": {"value": 0},
    }
    refused = ic.phase_lock(bad_psi, ["n1"])
    checks["collapse_refused"] = refused.get("ok") is False

    lock = ic.phase_lock(integ, ["a", "b", "c"])
    checks["phase_lock"] = bool(lock.get("ok")) and bool(lock.get("merkle_root"))

    receipt = ic.emit_receipt(lock, integ)
    checks["emit_receipt"] = bool(receipt.get("ok")) and bool(receipt.get("non_collapsing"))

    checks["verify_lock"] = all(
        [
            ic.verify_lock(integ).get("ok"),
            ic.verify_lock(lock).get("ok"),
            ic.verify_lock(receipt).get("ok"),
        ]
    )

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        ROOT / "references" / "SKILLSPECTOR_AUDIT.md",
        HERE / "integrator_cli.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    checks["files_missing"] = missing

    checks["ok"] = all(
        [
            checks["ast_clean"],
            checks["integrate"],
            checks["phase_lock"],
            checks["emit_receipt"],
            checks["verify_lock"],
            checks["collapse_refused"],
            not missing,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
