#!/usr/bin/env python3
"""Self-check Emotional RAM — no network/subprocess; encode/index/recall/swarm."""
from __future__ import annotations

import ast
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import emotional_ram as er  # noqa: E402


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
            if "subprocess" in names or "socket" in names or "requests" in names:
                hits.append(f"{path.name}:{names}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if node.func.attr in {"system", "popen"}:
                    hits.append(f"{path.name}:os.{node.func.attr}")
    return hits


def main() -> int:
    checks: dict = {"signature": er.SIG, "version": er.VERSION, "ok": False}
    bad: list[str] = []
    for p in HERE.glob("*.py"):
        bad.extend(_banned(p))
    checks["ast_clean"] = not bad
    checks["ast_hits"] = bad

    st = er.emotion_ram_encode(
        "grief and loss call for compassion and forgiveness with grace",
        shared_context=0.8,
        conflict=0.3,
    )
    checks["encode"] = st.primary_principle in er.UMP_BASIS and len(st.digest) == 64
    checks["grace_damped"] = 0.05 <= st.grace <= 1.0
    g_hi = er.grace_function(0.9, 0.1)
    g_lo = er.grace_function(0.2, 0.9)
    checks["grace_ordering"] = g_hi > g_lo

    with tempfile.TemporaryDirectory() as td:
        idx = Path(td) / "emotional_ram_index.json"
        refuse = er.index_memory("x", idx, i_consent=False)
        checks["index_requires_consent"] = refuse.get("ok") is False
        ok = er.index_memory(
            "A human feels fear then finds courage and trust",
            idx,
            i_consent=True,
            label="demo",
            tags=["human"],
        )
        checks["index"] = bool(ok.get("ok"))
        rec = er.recall(idx, principle="courage", top_k=1)
        checks["recall"] = bool(rec.get("returned"))

    swarm = er.swarm_aggregate(
        [
            "animal fear then calm safety",
            "swarm curiosity integrity resolve",
            "cyborg consent agency sovereignty",
        ]
    )
    checks["swarm"] = bool(swarm.get("ok")) and swarm.get("nodes") == 3

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        HERE / "emotional_ram.py",
        HERE / "emotional_ram_cli.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    checks["missing"] = missing
    checks["ok"] = all(
        [
            checks["ast_clean"],
            checks["encode"],
            checks["grace_damped"],
            checks["grace_ordering"],
            checks["index_requires_consent"],
            checks["index"],
            checks["recall"],
            checks["swarm"],
            not missing,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
