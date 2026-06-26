#!/usr/bin/env python3
"""PondDepth companion metrics generator.

This is packaged with the ponddepth-levels skill so other users get the
same XP/level calculation.

Outputs:
- companion-metrics.json into OpenClaw Control UI assets dir

Env overrides:
- OPENCLAW_UI_ASSETS_DIR: override target assets directory
- PONDDEPTH_TZ: timezone (default: Asia/Shanghai)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import subprocess
from pathlib import Path


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def detect_assets_dir() -> Path:
    env = os.environ.get("OPENCLAW_UI_ASSETS_DIR")
    if env:
        return Path(env).expanduser()

    # Default Homebrew global install path (macOS arm64). Users can override via env.
    return Path("/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets")


def read_json(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tz", default=os.environ.get("PONDDEPTH_TZ") or "Asia/Shanghai")
    args = ap.parse_args()

    assets_dir = detect_assets_dir()
    out_path = assets_dir / "companion-metrics.json"

    # We derive activity from the local workspace memory index if present.
    # On most OpenClaw setups, workspace is at ~/.openclaw/workspace
    ws = Path(os.environ.get("OPENCLAW_WORKSPACE") or (Path.home() / ".openclaw" / "workspace"))

    # Try to use the semantic index inputs if available; fallback to counting memory files.
    # For now: count distinct YYYY-MM-DD.md files with non-empty content as "active days".
    mem_dir = ws / "memory"
    days = []
    if mem_dir.exists():
        for p in sorted(mem_dir.glob("20??-??-??.md")):
            try:
                if p.stat().st_size > 50:
                    days.append(p.stem)
            except Exception:
                pass

    # Tokens/messages: best-effort from gateway logs via `openclaw status` is not exposed here.
    # We keep it simple: read previous metrics and only update what we can deterministically.
    prev = read_json(out_path) or {}

    T = float(prev.get("totalTokens") or 0)
    M = int(prev.get("messagesTotal") or 0)
    S = int(prev.get("extraSkillsReady") or prev.get("extraSkillsTotal") or 0)
    D = len(days)

    # Component scores
    xp_token = 220.0 * math.log10(1.0 + (T / 50_000.0 if T > 0 else 0.0))
    xp_skills = 25.0 * math.sqrt(max(S, 0))
    xp_msgs = 30.0 * math.log10(1.0 + (M / 200.0 if M > 0 else 0.0))
    xp_days = 20.0 * math.sqrt(max(D, 0))

    # New weights (no scaling; level may shift when weights change)
    XP = 0.40 * xp_token + 0.30 * xp_skills + 0.15 * xp_msgs + 0.15 * xp_days

    # Level thresholds (same as UI): B1 0-80, B2 80-160, B3 160-260, B4 260-360, B5 360-520
    def level_for_xp(x: float) -> str:
        if x < 80:
            return "B1"
        if x < 160:
            return "B2"
        if x < 260:
            return "B3"
        if x < 360:
            return "B4"
        if x < 520:
            return "B5"
        # beyond: keep B5 for now
        return "B5"

    level = level_for_xp(XP)

    j = {
        "schemaVersion": 1,
        "updatedAt": now_iso(),
        "timeZone": args.tz,
        "totalTokens": int(T),
        "messagesTotal": int(M),
        "messagesUser": int(prev.get("messagesUser") or 0),
        "messagesAssistant": int(prev.get("messagesAssistant") or 0),
        "companionDays": D,
        "activeDays": D,
        "days": days,
        "extraSkillsReady": int(S),
        "extraSkillsTotal": int(prev.get("extraSkillsTotal") or S),
        "xp": round(XP, 2),
        "xpBreakdown": {
            "token": round(xp_token, 2),
            "skills": round(xp_skills, 2),
            "msgs": round(xp_msgs, 2),
            "days": round(xp_days, 2),
        },
        "level": level,
        "levelProgressPct": int(prev.get("levelProgressPct") or 0),
    }

    assets_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {out_path}")


if __name__ == "__main__":
    main()
