#!/usr/bin/env python3
"""Self-check lygo-sanctuary-guardian — no network/subprocess."""
from __future__ import annotations

import ast
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import guardian_cli as gc  # noqa: E402


def _banned(path: Path) -> list[str]:
    hits: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [a.name.split(".")[0] for a in node.names]
                if isinstance(node, ast.Import)
                else [(node.module or "").split(".")[0]]
            )
            for bad in ("subprocess", "socket", "requests", "urllib"):
                if bad in names:
                    hits.append(f"{path.name}:{bad}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if node.func.attr in {"system", "popen"}:
                    hits.append(f"{path.name}:os.{node.func.attr}")
    return hits


def main() -> int:
    checks: dict = {"signature": gc.SIG, "version": gc.VERSION, "ok": False}
    bad: list[str] = []
    for p in HERE.glob("*.py"):
        bad.extend(_banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    import argparse

    nurture = gc.cmd_nurture_vector(
        argparse.Namespace(
            truth="T",
            light="L",
            compassion="C",
            grace="G",
            write=None,
            i_consent=False,
        )
    )
    checks["nurture_vector"] = bool(nurture.get("ok")) and len(nurture.get("vector_sha256") or "") == 64
    checks["non_collapsing"] = bool(nurture.get("non_collapsing"))

    shield = gc.cmd_shield_mandala(
        argparse.Namespace(
            nodes="a,b",
            seed="SELFCHECK",
            truth="T",
            light="L",
            allow_collapse=False,
            write=None,
            i_consent=False,
        )
    )
    checks["shield_mandala"] = bool(shield.get("ok")) and len(shield.get("shield_sha256") or "") == 64

    lock = gc.cmd_lock_truth(
        argparse.Namespace(
            nodes="a,b",
            truth="T",
            light="L",
            write=None,
            i_consent=False,
        )
    )
    checks["lock_truth"] = bool(lock.get("ok")) and len(lock.get("lock_sha256") or "") == 64

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        shield_path = td_path / "shield.json"
        lock_path = td_path / "lock.json"
        nurture_path = td_path / "nurture.json"
        barrier_path = td_path / "barrier.json"

        refuse = gc.cmd_shield_mandala(
            argparse.Namespace(
                nodes="a",
                seed="X",
                truth="T",
                light="L",
                allow_collapse=False,
                write=str(shield_path),
                i_consent=False,
            )
        )
        checks["write_requires_consent"] = refuse.get("ok") is False

        ok_shield = gc.cmd_shield_mandala(
            argparse.Namespace(
                nodes="a,b",
                seed="SELFCHECK",
                truth="T",
                light="L",
                allow_collapse=False,
                write=str(shield_path),
                i_consent=True,
            )
        )
        checks["write_ok"] = bool(ok_shield.get("ok")) and shield_path.is_file()

        ok_lock = gc.cmd_lock_truth(
            argparse.Namespace(
                nodes="a,b",
                truth="T",
                light="L",
                write=str(lock_path),
                i_consent=True,
            )
        )
        ok_nurture = gc.cmd_nurture_vector(
            argparse.Namespace(
                truth="T",
                light="L",
                compassion="C",
                grace="G",
                write=str(nurture_path),
                i_consent=True,
            )
        )
        checks["lock_write"] = bool(ok_lock.get("ok")) and lock_path.is_file()
        checks["nurture_write"] = bool(ok_nurture.get("ok")) and nurture_path.is_file()

        ver_s = gc.cmd_verify_barrier(argparse.Namespace(from_file=str(shield_path)))
        ver_l = gc.cmd_verify_barrier(argparse.Namespace(from_file=str(lock_path)))
        checks["verify_shield"] = bool(ver_s.get("ok"))
        checks["verify_lock"] = bool(ver_l.get("ok"))

        barrier = gc.cmd_emit_barrier(
            argparse.Namespace(
                shield_file=str(shield_path),
                lock_file=str(lock_path),
                nurture_file=str(nurture_path),
                write=str(barrier_path),
                i_consent=True,
            )
        )
        checks["emit_barrier"] = bool(barrier.get("ok")) and len(barrier.get("barrier_sha256") or "") == 64
        ver_b = gc.cmd_verify_barrier(argparse.Namespace(from_file=str(barrier_path)))
        checks["verify_barrier"] = bool(ver_b.get("ok"))

        # Tamper should fail verify
        tampered = json.loads(shield_path.read_text(encoding="utf-8"))
        tampered["truth"] = "TAMPERED"
        tamper_path = td_path / "tampered.json"
        tamper_path.write_text(json.dumps(tampered, indent=2), encoding="utf-8")
        ver_bad = gc.cmd_verify_barrier(argparse.Namespace(from_file=str(tamper_path)))
        checks["tamper_detected"] = ver_bad.get("ok") is False

    demo = gc.cmd_demo(argparse.Namespace())
    checks["demo"] = bool(demo.get("ok"))

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        HERE / "guardian_cli.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    checks["missing"] = missing
    checks["ok"] = all(
        [
            checks["ast_clean"],
            checks["nurture_vector"],
            checks["non_collapsing"],
            checks["shield_mandala"],
            checks["lock_truth"],
            checks["write_requires_consent"],
            checks["write_ok"],
            checks["lock_write"],
            checks["nurture_write"],
            checks["verify_shield"],
            checks["verify_lock"],
            checks["emit_barrier"],
            checks["verify_barrier"],
            checks["tamper_detected"],
            checks["demo"],
            not missing,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
