#!/usr/bin/env python3
"""Compute companion metrics from local session JSONL logs + skills list.

Outputs a JSON file for Control UI badge hover.

Metrics:
- companionDays: distinct local days with any meaningful user/assistant message
- messagesTotal: count of meaningful user+assistant messages
- messagesUser / messagesAssistant
- extraSkillsReady: count of ready skills excluding openclaw-bundled
- timeZone: IANA tz used for day bucketing

Notes:
- We intentionally ignore assistant tool-call-only messages and NO_REPLY.
- This is best-effort and assumes this agent primarily chats with one human.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

WORKSPACE = Path("/Users/aibaobao/.openclaw/workspace")
SESS_DIR = Path("/Users/aibaobao/.openclaw/agents/main/sessions")
SESS_INDEX = SESS_DIR / "sessions.json"
CONTROL_ASSETS_DIR = Path("/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets")

NO_REPLY_RE = re.compile(r"^\s*NO_REPLY\s*$")


def run_json(cmd: list[str]) -> Any:
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def is_meaningful_message(msg: dict) -> bool:
    """Return True if this is a user/assistant conversational message worth counting."""
    role = msg.get("role")
    if role == "user":
        return True
    if role != "assistant":
        return False

    content = msg.get("content")
    # Some message formats use a simple text field
    if isinstance(msg.get("text"), str) and msg.get("text").strip():
        return not NO_REPLY_RE.match(msg.get("text"))

    if isinstance(content, str):
        return bool(content.strip()) and not NO_REPLY_RE.match(content)
    if not isinstance(content, list):
        return False

    # Count assistant message if it contains any text (non NO_REPLY)
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text":
            text = part.get("text")
            if isinstance(text, str) and text.strip() and not NO_REPLY_RE.match(text):
                return True
    return False


def date_key(ts_ms: int, tz: dt.tzinfo) -> str:
    return dt.datetime.fromtimestamp(ts_ms / 1000, tz=dt.timezone.utc).astimezone(tz).date().isoformat()


def load_tz(tz_name: str) -> dt.tzinfo:
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(tz_name)
    except Exception:
        # fallback to UTC
        return dt.timezone.utc


def compute_sessions_metrics(tz: dt.tzinfo) -> dict[str, Any]:
    if not SESS_INDEX.exists():
        return {
            "messagesTotal": 0,
            "messagesUser": 0,
            "messagesAssistant": 0,
            "companionDays": 0,
            "days": [],
        }

    index = json.loads(SESS_INDEX.read_text(encoding="utf-8"))
    # index is a map: sessionKey -> {sessionId, ...}
    keys = list(index.keys())

    days = set()
    user_ct = 0
    asst_ct = 0

    for sk in keys:
        meta = index.get(sk) or {}
        sid = meta.get("sessionId")
        if not isinstance(sid, str) or not sid:
            continue
        p = SESS_DIR / f"{sid}.jsonl"
        if not p.exists():
            continue
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except Exception:
                    continue
                if not isinstance(msg, dict):
                    continue

                # Session logs are event envelopes; conversational payload is under `message`.
                payload = msg.get("message") if isinstance(msg.get("message"), dict) else None
                if not payload:
                    continue

                ts_raw = msg.get("timestamp")
                if not isinstance(ts_raw, str) or not ts_raw:
                    continue
                try:
                    # ISO like 2026-03-03T12:06:50.287Z
                    ts_dt = dt.datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                    ts_ms = int(ts_dt.timestamp() * 1000)
                except Exception:
                    continue

                if not is_meaningful_message(payload):
                    continue

                role = payload.get("role")
                if role == "user":
                    user_ct += 1
                elif role == "assistant":
                    asst_ct += 1

                days.add(date_key(ts_ms, tz))
        except Exception:
            continue

    days_list = sorted(days)

    # Companion days: distinct active days, but always include "today" (in the chosen tz)
    try:
        today = dt.datetime.now(dt.timezone.utc).astimezone(tz).date().isoformat()
    except Exception:
        today = None
    days_set = set(days_list)
    if today:
        days_set.add(today)

    return {
        "messagesTotal": user_ct + asst_ct,
        "messagesUser": user_ct,
        "messagesAssistant": asst_ct,
        "companionDays": max(1, len(days_set)),
        "activeDays": len(days_list),
        "days": days_list,
    }


def compute_extra_skills_ready() -> dict[str, Any]:
    try:
        j = run_json(["openclaw", "skills", "list", "--json"])
    except Exception:
        return {"extraSkillsReady": 0, "extraSkillsTotal": 0}

    skills = j.get("skills") or []
    extra = []
    extra_ready = []
    for s in skills:
        if not isinstance(s, dict):
            continue
        src = (s.get("source") or "").strip()
        # If source is missing, treat as bundled to avoid overcount.
        if not src or src == "openclaw-bundled":
            continue
        extra.append(s)
        eligible = bool(s.get("eligible"))
        disabled = bool(s.get("disabled"))
        blocked = bool(s.get("blockedByAllowlist"))
        if eligible and (not disabled) and (not blocked):
            extra_ready.append(s)

    return {
        "extraSkillsReady": len(extra_ready),
        "extraSkillsTotal": len(extra),
    }


def compute_total_tokens() -> int:
    try:
        j = run_json(["openclaw", "sessions", "--all-agents", "--json"])
    except Exception:
        return 0
    rows = j.get("sessions") or []
    total = 0
    for r in rows:
        tt = r.get("totalTokens")
        if isinstance(tt, (int, float)):
            total += int(tt)
    return total


def compute_level(payload: dict[str, Any]) -> dict[str, Any]:
    """Compute B1-B5 level + progress from metrics.

    Token is the highest weight, with diminishing returns.
    """
    T = int(payload.get("totalTokens") or 0)
    D = int(payload.get("companionDays") or 0)
    S = int(payload.get("extraSkillsReady") or 0)
    M = int(payload.get("messagesTotal") or 0)

    import math

    # XP components
    xp_token = 220.0 * math.log10(1.0 + (T / 50_000.0 if T > 0 else 0.0))
    xp_skills = 25.0 * math.sqrt(max(S, 0))
    xp_msgs = 30.0 * math.log10(1.0 + (M / 200.0 if M > 0 else 0.0))
    xp_days = 20.0 * math.sqrt(max(D, 0))

    # Weights tuned: reduce token dominance; reward skills/messages/days more.
    # Note: no global scaling; level may shift when weights change (acceptable).
    XP = 0.40 * xp_token + 0.30 * xp_skills + 0.15 * xp_msgs + 0.15 * xp_days

    # Thresholds (B1-B5)
    levels = [
        ("B1", 0.0, 80.0),
        ("B2", 80.0, 160.0),
        ("B3", 160.0, 260.0),
        ("B4", 260.0, 380.0),
        ("B5", 380.0, 999999.0),
    ]

    lvl = "B1"
    lo, hi = 0.0, 80.0
    for name, a, b in levels:
        if XP >= a and XP < b:
            lvl = name
            lo, hi = a, b
            break
        if XP >= b:
            lvl = name
            lo, hi = a, b

    pct = 100.0 if hi <= lo else max(0.0, min(100.0, (XP - lo) / (hi - lo) * 100.0))

    return {
        "xp": round(XP, 2),
        "xpBreakdown": {
            "token": round(xp_token, 2),
            "skills": round(xp_skills, 2),
            "msgs": round(xp_msgs, 2),
            "days": round(xp_days, 2),
        },
        "level": lvl,
        "levelProgressPct": int(round(pct)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tz", default=os.environ.get("COMPANION_TZ", "Asia/Shanghai"))
    ap.add_argument("--out", default=str(CONTROL_ASSETS_DIR / "companion-metrics.json"))
    args = ap.parse_args()

    tz = load_tz(args.tz)
    sess = compute_sessions_metrics(tz)
    skills = compute_extra_skills_ready()
    total_tokens = compute_total_tokens()

    payload = {
        "schemaVersion": 1,
        "updatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "timeZone": args.tz,
        "totalTokens": total_tokens,
        **sess,
        **skills,
    }

    payload.update(compute_level(payload))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {out_path}")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
