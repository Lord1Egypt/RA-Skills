#!/usr/bin/env python3
"""Render a markdown report from an hh.ru submission bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_absolute_or_private(path_text: str) -> bool:
    return path_text.startswith("/") or path_text.startswith("~") or ":\\" in path_text or path_text.startswith("file://")


def safe_display_path(path_text: str) -> str:
    value = path_text.strip()
    if not value:
        return "n/a"
    if is_absolute_or_private(value):
        return "[redacted-private-path]"
    return value


def redact_url(url: str, include_sensitive: bool) -> str:
    value = url.strip()
    if not value:
        return "n/a"
    if include_sensitive:
        return value
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[redacted-private-url]"
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        return "[redacted-private-url]"
    if host == "hh.ru" or host.endswith(".hh.ru"):
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return "[redacted-private-url]"


def render_cover_letter(body: str, include_sensitive: bool) -> str:
    if not body:
        return "_No cover letter recorded._"
    if include_sensitive:
        return body
    return "_Redacted by default. Re-run with `--include-sensitive` for a full export._"


def format_artifacts(artifacts: dict[str, str]) -> list[str]:
    labels = {
        "screenshot": "screenshot",
        "snapshot_json": "snapshot",
        "console_log": "console",
    }
    out: list[str] = []
    for key, label in labels.items():
        value = artifacts.get(key, "").strip()
        if value:
            out.append(f"{label}: `{safe_display_path(value)}`")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Packet JSON.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    parser.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include the full cover letter body and unredacted apply/outcome URLs.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    packet = payload.get("packet", {})
    content = payload.get("content", {})
    review = payload.get("review", {})
    summary = payload.get("summary", {})
    steps = payload.get("steps", [])

    lines = [
        "# HH Submission Report",
        "",
        f"- Packet: `{packet.get('packet_id', '')}`",
        f"- Vacancy ID: {packet.get('vacancy_id', '')}",
        f"- Vacancy title: {packet.get('vacancy_title', '')}",
        f"- Company: {packet.get('company_name', '')}",
        f"- Resume title: {packet.get('resume_title', '')}",
        f"- Vacancy URL: {redact_url(packet.get('vacancy_url', ''), args.include_sensitive)}",
        f"- Apply URL: {redact_url(packet.get('apply_url', ''), args.include_sensitive)}",
        f"- Browser profile: {packet.get('browser_profile', '') or 'n/a'}",
        f"- Review status: **{review.get('status', 'unknown')}**",
        f"- Reviewer: {review.get('reviewer', '') or 'n/a'}",
        f"- Summary status: **{summary.get('status', 'unknown')}**",
        f"- Submitted: {summary.get('submitted', False)}",
        "",
        "## Cover Letter",
        "",
        render_cover_letter(content.get("cover_letter", ""), args.include_sensitive),
        "",
        "## Steps",
        "",
    ]

    for index, step in enumerate(steps, start=1):
        lines.append(f"### {index}. {step.get('step_id', f'step-{index}')}")
        lines.append(f"- Status: **{step.get('status', 'unknown')}**")
        lines.append(f"- Effect: {step.get('effect', '') or 'n/a'}")
        lines.append(f"- Action: {step.get('action', '')}")
        lines.append(f"- Expected: {step.get('expected', '')}")
        lines.append(f"- Actual: {step.get('actual', '')}")
        if step.get("note"):
            lines.append(f"- Note: {step['note']}")
        if step.get("issue_keys"):
            lines.append(f"- Issue keys: {', '.join(step['issue_keys'])}")
        if step.get("outcome_url"):
            lines.append(f"- Outcome URL: {redact_url(step['outcome_url'], args.include_sensitive)}")
        artifact_parts = format_artifacts(step.get("artifacts", {}))
        if artifact_parts:
            lines.append(f"- Artifacts: {'; '.join(artifact_parts)}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
