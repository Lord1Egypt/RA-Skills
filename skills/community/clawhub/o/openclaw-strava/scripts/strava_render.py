#!/usr/bin/env python3
"""Render normalized Strava daily JSON.

Usage:
  python3 scripts/strava_render.py day.json --format markdown --channel generic
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict


def style(channel: str, markdown: bool) -> Dict[str, Any]:
    c = (channel or "generic").lower()
    if not markdown or c == "telegram":
        return {"md": False, "bL": "", "bR": "", "bullet": "-"}
    if c in ("slack", "whatsapp"):
        return {"md": True, "bL": "*", "bR": "*", "bullet": "-"}
    return {"md": True, "bL": "**", "bR": "**", "bullet": "-"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--format", choices=["text", "markdown"], default="markdown")
    ap.add_argument("--channel", default="generic")
    args = ap.parse_args()

    doc = json.load(open(args.input, "r", encoding="utf-8"))
    st = style(args.channel, args.format == "markdown")

    date = doc.get("date") or "(unknown date)"
    workouts = (((doc.get("training") or {}).get("workouts")) or [])

    def b(s: str) -> str:
        return f"{st['bL']}{s}{st['bR']}" if st["md"] and st["bL"] else s

    lines = [b(f"Strava — {date}")]

    if not workouts:
        lines.append(f"{st['bullet']} No activities found")
    else:
        lines.append(f"{st['bullet']} Activities: {len(workouts)}")
        for w in workouts[:10]:
            t = w.get("type") or "workout"
            dur = w.get("duration_minutes")
            dist = w.get("distance_km")
            bits = [t]
            if dur is not None:
                bits.append(f"{dur} min")
            if dist is not None:
                bits.append(f"{dist:.2f} km")
            lines.append(f"  {st['bullet']} " + " · ".join(bits))
        if len(workouts) > 10:
            lines.append(f"{st['bullet']} (+{len(workouts)-10} more)")

    print("\n".join(lines).strip() + "\n", end="")


if __name__ == "__main__":
    main()
