import json
import os
import sys
from pathlib import Path


def read_payload(path=None):
    if path:
        raw = Path(path).read_bytes()
        if not raw.strip():
            return default_payload()
        payload = json.loads(raw.decode("utf-8-sig", errors="replace"))
    else:
        payload = default_payload()
    merge_env_defaults(payload)
    return payload


def default_payload():
    return {
        "protocolVersion": "2.0",
        "skill": "kb_maintenance",
        "trigger": "openclaw_cron",
        "team": {
            "kbRepo": os.getenv("TEAM_KB_REPO") or "",
            "name": os.getenv("TEAM_NAME") or "",
            "researchDirection": os.getenv("TEAM_RESEARCH_DIRECTION") or "",
        },
        "platform": {
            "giteaUrl": os.getenv("GITEA_URL") or "",
            "giteaOwner": os.getenv("GITEA_ORG") or os.getenv("GITEA_BOT_USERNAME") or "",
            "sharedDir": os.getenv("OPENCLAW_SHARED_DIR") or "",
        },
        "maintenance": {},
    }


def merge_env_defaults(payload):
    payload.setdefault("protocolVersion", "2.0")
    payload.setdefault("skill", "kb_maintenance")
    team = payload.setdefault("team", {})
    platform = payload.setdefault("platform", {})
    maintenance = payload.setdefault("maintenance", {})
    if not team.get("kbRepo"):
        team["kbRepo"] = os.getenv("TEAM_KB_REPO") or ""
    if not team.get("name"):
        team["name"] = os.getenv("TEAM_NAME") or ""
    if not team.get("researchDirection"):
        team["researchDirection"] = os.getenv("TEAM_RESEARCH_DIRECTION") or ""
    if not platform.get("giteaUrl"):
        platform["giteaUrl"] = os.getenv("GITEA_URL") or ""
    if not platform.get("giteaOwner"):
        platform["giteaOwner"] = os.getenv("GITEA_ORG") or os.getenv("GITEA_BOT_USERNAME") or ""
    if not platform.get("sharedDir"):
        platform["sharedDir"] = os.getenv("OPENCLAW_SHARED_DIR") or ""
    if "mode" not in maintenance:
        maintenance["mode"] = "scheduled_overview_refresh"
    return payload


def envelope(result=None):
    base = {
        "success": True,
        "processedSources": [],
        "createdPages": [],
        "updatedPages": [],
        "archivedFiles": [],
        "skippedSources": [],
        "errors": [],
        "commitId": "",
    }
    base.update(result or {})
    return base


def write_result(path, result):
    data = envelope(result)
    if path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def print_json(data):
    text = json.dumps(data or {}, ensure_ascii=False, indent=2) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))
