#!/usr/bin/env python3
"""Best-effort installer queue for ClawHub skills.

Reads: memory/skill-install-queue.json
Attempts: `clawhub install <name>`
Writes back status.

Meant to be run by cron/heartbeat.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

WS = Path("/Users/aibaobao/.openclaw/workspace")
Q = WS / "memory" / "skill-install-queue.json"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def load() -> dict:
    if not Q.exists():
        return {"schemaVersion": 1, "updatedAt": now_iso(), "items": []}
    return json.loads(Q.read_text(encoding="utf-8"))


def save(j: dict) -> None:
    j["updatedAt"] = now_iso()
    Q.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def try_install(name: str) -> tuple[bool, str]:
    try:
        cp = subprocess.run(
            ["clawhub", "install", name],
            cwd=str(WS),
            text=True,
            capture_output=True,
            timeout=600,
        )
        out = (cp.stdout or "") + ("\n" + cp.stderr if cp.stderr else "")
        if cp.returncode == 0:
            return True, out.strip()
        return False, out.strip() or f"exit={cp.returncode}"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, repr(e)


def main() -> None:
    j = load()
    items = j.get("items") or []
    changed = False

    for it in items:
        if not isinstance(it, dict):
            continue
        if it.get("state") in ("installed", "skipped"):
            continue
        name = str(it.get("name") or "").strip()
        if not name:
            continue

        it["lastTriedAt"] = now_iso()
        ok, msg = try_install(name)
        changed = True
        if ok:
            it["state"] = "installed"
            it["lastError"] = ""
            it["note"] = (msg[:4000] if msg else "ok")
        else:
            it["state"] = "queued"
            it["lastError"] = (msg[:4000] if msg else "error")

    if changed:
        save(j)

    # Print a short summary for cron capture
    pending = [it for it in items if isinstance(it, dict) and it.get("state") != "installed"]
    print(f"queue_total={len(items)} pending={len(pending)}")
    for it in pending[:5]:
        print(f"- {it.get('name')}: {it.get('lastError','')[:120]}")


if __name__ == "__main__":
    main()
