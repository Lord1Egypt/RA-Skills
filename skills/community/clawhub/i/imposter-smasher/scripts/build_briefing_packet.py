#!/usr/bin/env python3
"""Build a concise meeting prep packet from event + research JSON inputs.

Usage:
  python scripts/build_briefing_packet.py \
    --event assets/example-event.json \
    --research assets/example-research.json \
    --outdir /tmp/imposter-smasher-output
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _format_summary(event: dict[str, Any], research: dict[str, Any]) -> str:
    title = event.get("title", "Unknown Event")
    start = event.get("start", "Unknown time")
    organizer = event.get("organizer", "Unknown organizer")
    attendees = event.get("attendees", [])

    top_points = research.get("top_points", [])[:3]
    risks = research.get("risks", [])[:3]
    questions = research.get("questions", [])[:8]
    sources = research.get("sources", [])

    lines = [
        "# Executive Summary",
        "",
        "## Meeting Snapshot",
        f"- Event: {title}",
        f"- Date/time: {start}",
        f"- Organizer: {organizer}",
        f"- Attendees: {', '.join(attendees) if attendees else 'Not provided'}",
        "",
        "## What Matters Most",
    ]

    if top_points:
        lines.extend([f"- {p}" for p in top_points])
    else:
        lines.append("- Research points pending.")

    lines.extend(["", "## Risks", *([f"- {r}" for r in risks] or ["- Risks not provided."])])
    lines.extend(["", "## Question Bank"])
    lines.extend([f"{i}. {q}" for i, q in enumerate(questions, start=1)] or ["1. What is the primary success criterion for this meeting?"])
    lines.extend(["", "## Sources"])

    if sources:
        for s in sources:
            name = s.get("name", "Unknown")
            date = s.get("date", "Unknown date")
            url = s.get("url", "")
            lines.append(f"- [{name}, {date}] {url}".strip())
    else:
        lines.append("- Sources pending.")

    return "\n".join(lines) + "\n"


def _format_audio_script(
    event: dict[str, Any], research: dict[str, Any], min_words: int
) -> str:
    title = event.get("title", "your upcoming meeting")
    objective = research.get("objective", "align on goals and next decisions")
    top_points = research.get("top_points", [])[:4]
    risks = research.get("risks", [])[:3]
    questions = research.get("questions", [])[:4]
    attendees = event.get("attendees", [])[:6]
    notes = event.get("notes", "")

    lines = [
        f"This is your briefing for {title}.",
        f"The objective is to {objective}.",
        "",
        "Key context:",
    ]

    if top_points:
        lines.extend([f"- {p}" for p in top_points])
    else:
        lines.append("- Context collection is still in progress.")

    lines.append("")
    lines.append("Watchouts:")
    lines.extend([f"- {r}" for r in risks] or ["- Confirm current constraints and decision timeline."])

    lines.append("")
    lines.append("Recommended questions:")
    lines.extend([f"- {q}" for q in questions] or ["- What outcome would make this meeting a clear success?"])

    lines.append("")
    lines.append("Execution plan before the meeting:")
    lines.append("- Open by aligning on objective, timeline, and ownership.")
    lines.append("- Validate decision process and hidden blockers early.")
    lines.append("- Confirm what decision can be made in this meeting versus follow-up.")
    lines.append("")
    lines.append("Confidence framing:")
    lines.append("- High confidence: role priorities, timeline constraints, and likely objections.")
    lines.append("- Medium confidence: budget sensitivity and legal review complexity.")
    lines.append("- Low confidence: new initiatives not yet publicly disclosed.")
    lines.append("")
    if attendees:
        lines.append("Participant focus reminders:")
        for name in attendees:
            lines.append(
                f"- For {name}, tie recommendations to measurable outcomes, risk controls, and execution speed."
            )
        lines.append("")
    if notes:
        lines.append("Meeting note context:")
        lines.append(f"- {notes}")
        lines.append("")
    lines.append("Close with a direct recap, one clear ask, and agreed next steps.")

    # Pad script if needed to satisfy the 3-5 minute narration target in sparse inputs.
    while len(" ".join(lines).split()) < min_words:
        lines.extend(
            [
                "",
                "Preparation drill-down:",
                "- Rehearse two concise value statements and one fallback position.",
                "- Prepare one proof point for impact, one for reliability, and one for speed to value.",
                "- If challenged on scope, redirect to phased milestones with clear acceptance criteria.",
            ]
        )

    return "\n".join(lines) + "\n"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build executive summary and audio script drafts")
    parser.add_argument("--event", type=Path, required=True, help="Path to event JSON")
    parser.add_argument("--research", type=Path, required=True, help="Path to research JSON")
    parser.add_argument("--outdir", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--narration-min-words",
        type=int,
        default=430,
        help="Minimum narration words to target 3-5 minute output",
    )
    args = parser.parse_args()

    event = _read_json(args.event)
    research = _read_json(args.research)

    summary = _format_summary(event, research)
    script = _format_audio_script(event, research, args.narration_min_words)

    _write(args.outdir / "executive_summary.md", summary)
    _write(args.outdir / "audio_script.txt", script)

    manifest = {
        "event_title": event.get("title"),
        "audio_engine": "set-at-runtime",
        "target_duration_seconds": [180, 300],
        "script_file": "audio_script.txt",
        "notes": "Render via ElevenLabs or Chatterbox integration.",
    }
    _write(args.outdir / "audio_manifest.json", json.dumps(manifest, indent=2) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
