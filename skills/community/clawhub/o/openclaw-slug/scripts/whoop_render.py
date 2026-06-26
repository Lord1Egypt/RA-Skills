#!/usr/bin/env python3
"""Render normalized WHOOP JSON into human-friendly text/markdown.

Usage:
  python3 scripts/whoop_render.py whoop.json --format markdown --channel generic

Channel affects formatting only (no hardcoded sending).
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict


def fmt_line(key: str, val: Any) -> str:
    return f"{key}: {val}" if val is not None else f"{key}: —"


def style_for_channel(channel: str) -> Dict[str, str]:
    c = (channel or "generic").lower()
    # Keep it simple and robust across clients.
    # - discord: **bold**
    # - slack: *bold*
    # - whatsapp: *bold* (avoid headings/tables)
    # - telegram: prefer plain text (MarkdownV2 escaping is annoying)
    if c in ("slack", "whatsapp"):
        return {"bold_l": "*", "bold_r": "*", "bullet": "-", "use_markdown": "1"}
    if c in ("discord",):
        return {"bold_l": "**", "bold_r": "**", "bullet": "-", "use_markdown": "1"}
    if c in ("telegram",):
        return {"bold_l": "", "bold_r": "", "bullet": "-", "use_markdown": "0"}
    return {"bold_l": "**", "bold_r": "**", "bullet": "-", "use_markdown": "1"}


def render_generic(doc: Dict[str, Any], markdown: bool, channel: str) -> str:
    date = doc.get("date") or "(unknown date)"

    r = doc.get("recovery", {})
    s = doc.get("sleep", {})
    c = doc.get("cycle", {})
    w = doc.get("workout", {})

    st = style_for_channel(channel)
    use_md = markdown and st.get("use_markdown") == "1"
    bl, br = st.get("bold_l", ""), st.get("bold_r", "")
    bullet = st.get("bullet", "-")

    title = f"WHOOP summary — {date}"

    def b(x: str) -> str:
        return f"{bl}{x}{br}" if use_md and bl and br else x

    if use_md:
        out = [b(title), ""]
        out.append(f"{bullet} Recovery: {b(str(r.get('score'))) if r.get('score') is not None else '—'}")
        out.append(f"{bullet} HRV (ms): {r.get('hrv_ms') if r.get('hrv_ms') is not None else '—'}")
        out.append(f"{bullet} RHR (bpm): {r.get('rhr_bpm') if r.get('rhr_bpm') is not None else '—'}")
        out.append(f"{bullet} Sleep duration (min): {s.get('duration_minutes') if s.get('duration_minutes') is not None else '—'}")
        out.append(f"{bullet} Sleep performance (%): {s.get('performance_percent') if s.get('performance_percent') is not None else '—'}")
        out.append(f"{bullet} Day strain: {b(str(c.get('strain'))) if c.get('strain') is not None else '—'}")
        out.append(
            f"{bullet} Workouts: {w.get('count') if w.get('count') is not None else '—'} "
            f"(top strain: {w.get('top_strain') if w.get('top_strain') is not None else '—'})"
        )
        return "\n".join(out).strip() + "\n"

    # Plain text fallback
    out = [title]
    out.append(fmt_line("Recovery", r.get("score")))
    out.append(fmt_line("HRV (ms)", r.get("hrv_ms")))
    out.append(fmt_line("RHR (bpm)", r.get("rhr_bpm")))
    out.append(fmt_line("Sleep duration (min)", s.get("duration_minutes")))
    out.append(fmt_line("Sleep performance (%)", s.get("performance_percent")))
    out.append(fmt_line("Day strain", c.get("strain")))
    out.append(f"Workouts: {w.get('count','—')} (top strain: {w.get('top_strain','—')})")
    return "\n".join(out).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="normalized whoop.json")
    ap.add_argument("--format", choices=["text", "markdown"], default="markdown")
    ap.add_argument("--channel", default="generic", help="generic|whatsapp|telegram|slack|discord (formatting only)")
    args = ap.parse_args()

    doc = json.load(open(args.input, "r", encoding="utf-8"))
    markdown = args.format == "markdown"

    # For now, keep channel differences minimal; avoid tables and fancy markup.
    # WhatsApp can be markdown-ish but safest is simple bullets.
    msg = render_generic(doc, markdown=markdown, channel=args.channel)
    print(msg, end="")


if __name__ == "__main__":
    main()
