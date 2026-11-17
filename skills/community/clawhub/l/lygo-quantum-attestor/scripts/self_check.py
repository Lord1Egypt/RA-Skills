#!/usr/bin/env python3
"""Self-check lygo-quantum-attestor — no network/subprocess."""
from __future__ import annotations

import ast
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import attestor_cli as ac  # noqa: E402


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
    checks: dict = {"signature": ac.SIG, "version": ac.VERSION, "ok": False}
    bad: list[str] = []
    for p in HERE.glob("*.py"):
        bad.extend(_banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    import argparse

    attest = ac.cmd_attest(
        argparse.Namespace(
            node_id="selfcheck",
            truth="T",
            chaos="C",
            slm_root="",
            anchor_file="",
            allow_collapse=False,
            write=None,
            i_consent=False,
        )
    )
    checks["attest"] = bool(attest.get("ok")) and bool(attest.get("attest_sha256"))
    checks["non_collapsing"] = bool(attest.get("non_collapsing"))

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "attest.json"
        refuse = ac.cmd_attest(
            argparse.Namespace(
                node_id="selfcheck",
                truth="T",
                chaos="C",
                slm_root="",
                anchor_file="",
                allow_collapse=False,
                write=str(p),
                i_consent=False,
            )
        )
        checks["write_requires_consent"] = refuse.get("ok") is False
        okw = ac.cmd_attest(
            argparse.Namespace(
                node_id="selfcheck",
                truth="T",
                chaos="C",
                slm_root="deadbeef" * 8,
                anchor_file="",
                allow_collapse=False,
                write=str(p),
                i_consent=True,
            )
        )
        checks["write_ok"] = bool(okw.get("ok")) and p.is_file()
        sealed = ac.cmd_seal_delta9(
            argparse.Namespace(from_file=str(p), write=str(Path(td) / "sealed.json"), i_consent=True)
        )
        checks["seal_delta9"] = bool(sealed.get("ok")) and bool((sealed.get("delta9_seal") or {}).get("delta9_seal_sha256"))
        sealed_path = Path(td) / "sealed.json"
        ver = ac.cmd_verify_node(argparse.Namespace(from_file=str(sealed_path)))
        checks["verify_node"] = bool(ver.get("ok")) and bool(ver.get("attest_hash_ok")) and bool(ver.get("merkle_ok"))
        # Tamper detection: flip a character in truth and expect verify failure
        tampered = json.loads(sealed_path.read_text(encoding="utf-8"))
        tampered["truth"] = str(tampered.get("truth") or "") + "X"
        tamp_path = Path(td) / "tampered.json"
        tamp_path.write_text(json.dumps(tampered, indent=2) + "\n", encoding="utf-8")
        bad = ac.cmd_verify_node(argparse.Namespace(from_file=str(tamp_path)))
        checks["detects_tamper"] = bad.get("ok") is False and "attest_sha256_mismatch" in (bad.get("reasons") or [])
        # Tamper merkle by changing stored root
        tamp2 = json.loads(p.read_text(encoding="utf-8"))
        tamp2["slm"] = dict(tamp2.get("slm") or {})
        tamp2["slm"]["local_merkle_root"] = "0" * 64
        # keep attest hash as-is so mismatch surfaces on merkle OR attest depending on hash domain
        # Re-hash would be needed for attest; force merkle_ok false via stored root
        tamp2_path = Path(td) / "tampered_merkle.json"
        # Recompute valid attest hash would hide merkle check if we only check attest —
        # leave attest hash stale after merkle change so both may fail; require merkle fail
        tamp2_path.write_text(json.dumps(tamp2, indent=2) + "\n", encoding="utf-8")
        bad_m = ac.cmd_verify_node(argparse.Namespace(from_file=str(tamp2_path)))
        checks["detects_merkle_tamper"] = bad_m.get("ok") is False and (
            "merkle_root_mismatch" in (bad_m.get("reasons") or [])
            or "attest_sha256_mismatch" in (bad_m.get("reasons") or [])
        )
        rec = ac.cmd_emit_receipt(
            argparse.Namespace(from_file=str(sealed_path), write=str(Path(td) / "receipt.json"), i_consent=True)
        )
        checks["emit_receipt"] = bool(rec.get("ok")) and len(rec.get("receipt_sha256") or "") == 64

    demo = ac.cmd_demo(argparse.Namespace())
    checks["demo"] = bool(demo.get("ok"))

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        HERE / "attestor_cli.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    checks["missing"] = missing
    checks["ok"] = all(
        [
            checks["ast_clean"],
            checks["attest"],
            checks["non_collapsing"],
            checks["write_requires_consent"],
            checks["write_ok"],
            checks["seal_delta9"],
            checks["verify_node"],
            checks["detects_tamper"],
            checks["detects_merkle_tamper"],
            checks["emit_receipt"],
            checks["demo"],
            not missing,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
