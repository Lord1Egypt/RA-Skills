"""Semantic v2-lite pipeline: runs candidate_extract → semantic_consolidate → snapshot_render."""

from __future__ import annotations

import subprocess
from typing import Any, Dict

from .config import (
    WORKSPACE,
    SNAPSHOT_PATH,
    SNAPSHOT_RULE_PATH,
    SNAPSHOT_SEMANTIC_PATH,
    CANDIDATE_LATEST_PATH,
    SEMANTIC_LATEST_PATH,
    SEMANTIC_PIPELINE_STATUS_PATH,
    SEMANTIC_DIR,
)
from .core import save_json


def run_semantic_v2_lite_pipeline(now_iso: str) -> Dict[str, Any]:
    steps = [
        ("candidate_extract", WORKSPACE / "scripts" / "memory_candidate_extract.py"),
        ("semantic_consolidate", WORKSPACE / "scripts" / "memory_semantic_consolidate.py"),
        ("snapshot_render", WORKSPACE / "scripts" / "memory_snapshot_render.py"),
    ]
    status: Dict[str, Any] = {
        "generated_at": now_iso,
        "mode": "v2-lite",
        "status": "ok",
        "default_snapshot": str(SNAPSHOT_PATH),
        "rule_snapshot": str(SNAPSHOT_RULE_PATH),
        "semantic_snapshot": str(SNAPSHOT_SEMANTIC_PATH),
        "candidates": str(CANDIDATE_LATEST_PATH),
        "semantic": str(SEMANTIC_LATEST_PATH),
        "default_source": "pending",
        "steps": [],
    }

    SEMANTIC_DIR.mkdir(parents=True, exist_ok=True)

    for name, script_path in steps:
        step: Dict[str, Any] = {"name": name, "script": str(script_path)}

        if not script_path.exists():
            step["status"] = "missing"
            status["status"] = "degraded"
            status["steps"].append(step)
            break
        try:
            completed = subprocess.run(
                ["python3", str(script_path)],
                cwd=str(WORKSPACE),
                check=True,
                capture_output=True,
                text=True,
                timeout=90,
            )
            step["status"] = "ok"
            stdout = (completed.stdout or "").strip()
            stderr = (completed.stderr or "").strip()
            if stdout:
                step["stdout_tail"] = stdout[-500:]
            if stderr:
                step["stderr_tail"] = stderr[-500:]
        except Exception as exc:
            step["status"] = "error"
            step["error"] = str(exc)
            status["status"] = "degraded"
            status["steps"].append(step)
            break
        status["steps"].append(step)

    save_json(SEMANTIC_PIPELINE_STATUS_PATH, status)
    return status
