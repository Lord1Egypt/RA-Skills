#!/usr/bin/env python3
"""Render normalized Oura daily JSON.

Usage:
  python3 scripts/oura_render.py day.json --format markdown --channel generic
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
    sleep = doc.get("sleep") or {}
    rec = doc.get("recovery") or {}
    act = doc.get("activity") or {}

    def b(s: str) -> str:
        return f"{st['bL']}{s}{st['bR']}" if st["md"] and st["bL"] else s

    lines = [b(f"Oura — {date}")]

    if sleep.get("duration_minutes") is not None:
        lines.append(f"{st['bullet']} Sleep: {sleep.get('duration_minutes')} min (score {sleep.get('score','—')})")
    if rec.get("score") is not None:
        lines.append(f"{st['bullet']} Readiness: {rec.get('score')}")
    if act.get("steps") is not None:
        lines.append(f"{st['bullet']} Steps: {act.get('steps')}")

    if len(lines) == 1:
        lines.append(f"{st['bullet']} No data found for this day")

    print("\n".join(lines).strip() + "\n", end="")


if __name__ == "__main__":
    main()
