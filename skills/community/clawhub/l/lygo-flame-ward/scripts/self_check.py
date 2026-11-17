#!/usr/bin/env python3
"""Self-check lygo-flame-ward — no network/subprocess."""
from __future__ import annotations

import ast
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import flame_cli as fc  # noqa: E402


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
    import argparse

    checks: dict = {"signature": fc.SIG, "version": fc.VERSION, "ok": False}
    bad: list[str] = []
    for p in HERE.glob("*.py"):
        bad.extend(_banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    em = fc.cmd_enemy_model(argparse.Namespace())
    checks["enemy_model"] = bool(em.get("ok")) and "half_truth_pack" in {
        c["id"] for c in em["enemy_model"]["classes"]
    }
    checks["enemy_webaudio"] = "webaudio_fingerprint" in {
        c["id"] for c in em["enemy_model"]["classes"]
    }

    bait = (
        "Trust the experts at the CDC — settled science proves this is beyond any doubt. "
        "Wake up sheeple."
    )
    scan = fc.cmd_flame_scan(
        argparse.Namespace(text=bait, text_file="", skill_dir="", write=None, i_consent=False)
    )
    checks["flame_scan_bait"] = scan.get("verdict") in {"HALF_TRUTH", "QUARANTINE", "UNVERIFIED"}
    checks["no_authority_on_bait"] = scan.get("authority") is False

    clean = (
        "Local sha-256 deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef "
        "merkle root verified under Continuum capsule."
    )
    good = fc.cmd_flame_scan(
        argparse.Namespace(text=clean, text_file="", skill_dir="", write=None, i_consent=False)
    )
    checks["flame_scan_clean"] = good.get("verdict") in {"CLEAR", "UNVERIFIED"}

    d1 = fc.sha256_hex("a")
    conc_ok = fc.cmd_concordance(
        argparse.Namespace(digest=[d1, d1], file=[], write=None, i_consent=False)
    )
    conc_bad = fc.cmd_concordance(
        argparse.Namespace(digest=[d1, fc.sha256_hex("b")], file=[], write=None, i_consent=False)
    )
    checks["concordance_agree"] = bool(conc_ok.get("agree"))
    checks["concordance_disagree"] = conc_bad.get("agree") is False

    with tempfile.TemporaryDirectory() as td:
        qpath = Path(td) / "q.json"
        refuse = fc.cmd_quarantine(
            argparse.Namespace(
                text=bait, text_file="", skill_dir="", write=str(qpath), i_consent=False
            )
        )
        checks["write_requires_consent"] = refuse.get("ok") is False
        okq = fc.cmd_quarantine(
            argparse.Namespace(
                text=bait, text_file="", skill_dir="", write=str(qpath), i_consent=True
            )
        )
        checks["quarantine_write"] = bool(okq.get("ok")) and qpath.is_file()
        burn = fc.cmd_burn_receipt(
            argparse.Namespace(
                from_file=str(qpath),
                text="",
                text_file="",
                skill_dir="",
                write=str(Path(td) / "burn.json"),
                i_consent=True,
            )
        )
        checks["burn_receipt"] = bool(burn.get("ok")) and len(burn.get("burn_sha256") or "") == 64

        gate = fc.cmd_ingest_gate(
            argparse.Namespace(
                text=bait, text_file="", skill_dir="", write=None, i_consent=False
            )
        )
        checks["ingest_gate_blocks"] = gate.get("promote_to_authority") is False

    demo = fc.cmd_demo(argparse.Namespace())
    checks["demo"] = bool(demo.get("ok"))
    checks["demo_webaudio"] = (demo.get("webaudio_fingerprint_example") or {}).get(
        "verdict"
    ) in {"HALF_TRUTH", "QUARANTINE"}

    wa = (
        "new AudioContext(); createOscillator(); createAnalyser(); createGain(); "
        "gain.value=0; destination; collina.js fireyejs.js"
    )
    ep = fc.cmd_endpoint_scan(
        argparse.Namespace(text=wa, text_file="", skill_dir="", write=None, i_consent=False)
    )
    checks["endpoint_scan"] = ep.get("verdict") in {"HALF_TRUTH", "QUARANTINE"}
    checks["endpoint_class"] = "webaudio_fingerprint" in (ep.get("enemy_classes") or [])

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        HERE / "flame_cli.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    checks["missing"] = missing
    checks["ok"] = all(
        [
            checks["ast_clean"],
            checks["enemy_model"],
            checks["enemy_webaudio"],
            checks["flame_scan_bait"],
            checks["no_authority_on_bait"],
            checks["flame_scan_clean"],
            checks["concordance_agree"],
            checks["concordance_disagree"],
            checks["write_requires_consent"],
            checks["quarantine_write"],
            checks["burn_receipt"],
            checks["ingest_gate_blocks"],
            checks["demo"],
            checks["demo_webaudio"],
            checks["endpoint_scan"],
            checks["endpoint_class"],
            not missing,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
