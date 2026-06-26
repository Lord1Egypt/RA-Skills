"""Read/write helpers for openclaw's cron registry (~/.openclaw/cron/jobs.json).

openclaw's cron model: each job sends a `systemEvent` text payload to a specific
agent+session at the scheduled time. The agent interprets the text as a prompt.
This module knows how to add/update/remove jobs by name without touching others.

User config (agent_id, session_key, session_target) lives in
~/.glancely/openclaw.toml — written by install.sh after asking the user.
"""

from __future__ import annotations

import json
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))
JOBS_PATH = OPENCLAW_HOME / "cron" / "jobs.json"

PR_HOME = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely"))
PR_OPENCLAW_CONFIG = PR_HOME / "openclaw.toml"

JOB_NAME_TAG = "[glancely]"


class CronConfigMissing(RuntimeError):
    pass


def load_user_config() -> dict[str, str]:
    if not PR_OPENCLAW_CONFIG.is_file():
        raise CronConfigMissing(
            f"Missing {PR_OPENCLAW_CONFIG}. Run install.sh to configure your "
            f"openclaw agent_id / session_target / session_key, or set them by hand:\n"
            f'  agent_id       = "your_agent_id"\n'
            f'  session_target = "main"\n'
            f'  session_key    = "agent:your_agent_id:telegram:direct:<your-id>"'
        )
    with PR_OPENCLAW_CONFIG.open("rb") as fh:
        cfg = tomllib.load(fh)
    required = ("agent_id", "session_target", "session_key")
    missing = [k for k in required if not cfg.get(k)]
    if missing:
        raise CronConfigMissing(f"{PR_OPENCLAW_CONFIG} is missing keys: {missing}")
    return cfg


def _read_jobs() -> dict[str, Any]:
    if not JOBS_PATH.is_file():
        return {"version": 1, "jobs": []}
    with JOBS_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_jobs(data: dict[str, Any]) -> None:
    JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    backup = JOBS_PATH.with_suffix(f".json.bak.glancely.{int(time.time())}")
    if JOBS_PATH.is_file():
        shutil.copy2(JOBS_PATH, backup)
    tmp = JOBS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(JOBS_PATH)


def _job_name(component: str, label: str) -> str:
    return f"{label} {JOB_NAME_TAG} ({component})"


def upsert_component_cron(
    *,
    component: str,
    label: str,
    cron_expr: str,
    tz: str,
    notification_text: str,
    enabled: bool = True,
) -> dict[str, Any]:
    """Create or replace the cron job for one component. Idempotent by job name."""
    cfg = load_user_config()
    data = _read_jobs()
    jobs = data.setdefault("jobs", [])

    name = _job_name(component, label)
    now_ms = int(time.time() * 1000)
    new_job = {
        "id": str(uuid.uuid4()),
        "agentId": cfg["agent_id"],
        "sessionKey": cfg["session_key"],
        "name": name,
        "enabled": enabled,
        "createdAtMs": now_ms,
        "schedule": {"kind": "cron", "expr": cron_expr, "tz": tz},
        "sessionTarget": cfg["session_target"],
        "wakeMode": "now",
        "payload": {"kind": "systemEvent", "text": notification_text},
        "state": {},
    }

    replaced = False
    for i, existing in enumerate(jobs):
        if existing.get("name") == name:
            new_job["id"] = existing.get("id", new_job["id"])
            new_job["createdAtMs"] = existing.get("createdAtMs", new_job["createdAtMs"])
            new_job["state"] = existing.get("state", {})
            jobs[i] = new_job
            replaced = True
            break
    if not replaced:
        jobs.append(new_job)

    _write_jobs(data)
    return {"action": "updated" if replaced else "created", "job": new_job}


def remove_component_cron(component: str, label: str | None = None) -> int:
    """Remove all jobs for a component. Returns count removed."""
    if not JOBS_PATH.is_file():
        return 0
    data = _read_jobs()
    jobs = data.get("jobs", [])
    needle_tag = f"{JOB_NAME_TAG} ({component})"
    if label:
        needle_label = f"{label} {needle_tag}"
        keep = [j for j in jobs if j.get("name") != needle_label]
    else:
        keep = [j for j in jobs if needle_tag not in (j.get("name") or "")]
    removed = len(jobs) - len(keep)
    if removed:
        data["jobs"] = keep
        _write_jobs(data)
    return removed


def list_component_crons() -> list[dict[str, Any]]:
    if not JOBS_PATH.is_file():
        return []
    return [
        j for j in _read_jobs().get("jobs", [])
        if JOB_NAME_TAG in (j.get("name") or "")
    ]
