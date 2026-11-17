#!/usr/bin/env python3
"""Self-check lygo-immutable-anchor — no network / subprocess."""
from __future__ import annotations

import argparse
import ast
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import anchor_cli as ac  # noqa: E402

BANNED = ("subprocess", "socket", "requests", "urllib", "http.client")


def banned(path: Path) -> list[str]:
    hits: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in BANNED:
                    hits.append(f"{path.name}:{a.name}")
        if isinstance(node, ast.ImportFrom):
            mod = (node.module or "").split(".")[0]
            if mod in BANNED:
                hits.append(f"{path.name}:{mod}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if node.func.attr in {"system", "popen"}:
                    hits.append(f"{path.name}:os.{node.func.attr}")
    return hits


def main() -> int:
    checks: dict = {"signature": ac.SIG, "version": ac.VERSION, "ok": False}
    bad: list[str] = []
    for p in HERE.glob("*.py"):
        bad.extend(banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    demo = ac.cmd_demo(argparse.Namespace())
    checks["demo"] = bool(demo.get("ok"))
    checks["non_collapsing"] = bool(demo.get("seal", {}).get("non_collapsing"))
    checks["worker_does_not_execute"] = demo.get("plan", {}).get("executes") is False

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "seal.json"
        refuse = ac.cmd_seal(
            argparse.Namespace(
                node_id="sc",
                truth="T",
                light="L",
                chaos="C",
                write=str(p),
                i_consent=False,
            )
        )
        checks["write_requires_consent"] = refuse.get("ok") is False and not p.exists()
        okw = ac.cmd_seal(
            argparse.Namespace(
                node_id="sc",
                truth="T",
                light="L",
                chaos="C",
                write=str(p),
                i_consent=True,
            )
        )
        checks["write_with_consent"] = bool(okw.get("ok")) and p.is_file()
        v = ac.cmd_verify(argparse.Namespace(from_file=str(p)))
        checks["verify"] = bool(v.get("ok"))
        tampered = json.loads(p.read_text(encoding="utf-8"))
        tampered["merkle_root"] = "0" * 64
        tp = Path(td) / "bad.json"
        tp.write_text(json.dumps(tampered), encoding="utf-8")
        vt = ac.cmd_verify(argparse.Namespace(from_file=str(tp)))
        checks["detects_tamper"] = vt.get("ok") is False

    checks["ok"] = all(
        checks[k]
        for k in (
            "ast_clean",
            "demo",
            "non_collapsing",
            "worker_does_not_execute",
            "write_requires_consent",
            "write_with_consent",
            "verify",
            "detects_tamper",
        )
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
