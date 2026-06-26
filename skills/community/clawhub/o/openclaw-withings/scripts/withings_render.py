#!/usr/bin/env python3
"""Render normalized Withings daily JSON.

Usage:
  python3 scripts/withings_render.py day.json --format markdown --channel generic
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
    body = doc.get("body") or {}
    vit = doc.get("vitals") or {}

    def b(s: str) -> str:
        return f"{st['bL']}{s}{st['bR']}" if st["md"] and st["bL"] else s

    lines = [b(f"Withings — {date}")]

    dur = sleep.get("duration_minutes")
    if dur is not None:
        lines.append(f"{st['bullet']} Sleep: {dur} min")

    w = body.get("weight_kg")
    if w is not None:
        lines.append(f"{st['bullet']} Weight: {w:.2f} kg")

    bf = body.get("body_fat_percent")
    if bf is not None:
        lines.append(f"{st['bullet']} Body fat: {bf:.1f}%")

    sys = vit.get("bp_systolic")
    dia = vit.get("bp_diastolic")
    if sys is not None or dia is not None:
        lines.append(f"{st['bullet']} BP: {sys if sys is not None else '—'}/{dia if dia is not None else '—'}")

    hr = vit.get("resting_hr_bpm")
    if hr is not None:
        lines.append(f"{st['bullet']} HR: {hr} bpm")

    if len(lines) == 1:
        lines.append(f"{st['bullet']} No measurements found for this day")

    print("\n".join(lines).strip() + "\n", end="")


if __name__ == "__main__":
    main()
