#!/usr/bin/env python3
"""Self-check — no network/subprocess."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import workflow_planner as wp  # noqa: E402


def banned(path: Path) -> list[str]:
    hits = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] == "subprocess":
                    hits.append("subprocess")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == "subprocess":
                hits.append("subprocess")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if node.func.attr in {"system", "popen"}:
                    hits.append(f"os.{node.func.attr}")
    return hits


def main() -> int:
    bad = []
    for p in HERE.glob("*.py"):
        bad.extend(f"{p.name}:{h}" for h in banned(p))
    scored = wp.score_task(
        minutes=15,
        frequency_per_month=20,
        repetitive=True,
        judgment_required=False,
        touches_pii=False,
        external_vendors=1,
    )
    plan = wp.plan_workflow(
        name="demo",
        trigger="manual",
        conditions=[],
        actions=["a"],
        data_fields=["email"],
        tools=["lygo-sandcastle"],
        error_notify="alert",
    )
    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "skill-card.md",
        ROOT / "references" / "SECURITY.md",
        ROOT / "references" / "SKILLSPECTOR_AUDIT.md",
        HERE / "workflow_planner.py",
    ]
    missing = [str(r.relative_to(ROOT)) for r in req if not r.is_file()]
    out = {
        "ok": not bad and scored["recommend_automate"] and plan.get("ok") and not missing,
        "signature": wp.SIG,
        "version": wp.VERSION,
        "ast_hits": bad,
        "missing": missing,
        "score_demo": scored["priority_score"],
    }
    print(json.dumps(out, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
