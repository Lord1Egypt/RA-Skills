from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


SECTION_HEADER = "## Timeline"
DEFAULT_DAILY_DIR = Path(r"C:\Users\frezn\iCloudDrive\iCloud~md~obsidian\superyas\01 Daily")
DEFAULT_TEMPLATE = Path(r"C:\Users\frezn\iCloudDrive\iCloud~md~obsidian\superyas\Templates\Daily Note.md")


@dataclass
class Entry:
    time: str
    text: str
    location: Optional[str] = None
    tags: Optional[str] = None

    def to_bullet(self) -> str:
        meta = []
        if self.location:
            meta.append(f"📍 {self.location.strip()}")
        if self.tags:
            meta.append(self.tags.strip())
        suffix = f" — {' | '.join(meta)}" if meta else ""
        return f"- {self.time} — {self.text.strip()}{suffix}"

    def to_table_row(self) -> str:
        location = (self.location or "").strip().replace("|", "\\|")
        tags = (self.tags or "").strip().replace("|", "\\|")
        text = self.text.strip().replace("|", "\\|")
        return f"| {self.time} | {text} | {location} | {tags} |"


TIME_RE = re.compile(r"^(?P<hour>\d{1,2})(?::(?P<minute>\d{2}))?\s*(?P<ampm>[ap]m)?$", re.IGNORECASE)


def normalize_time(raw: str) -> str:
    value = raw.strip().lower().replace('.', '')
    match = TIME_RE.match(value)
    if not match:
        raise ValueError(f"Unsupported time format: {raw}")

    hour = int(match.group("hour"))
    minute = int(match.group("minute") or 0)
    ampm = match.group("ampm")

    if ampm:
        if hour < 1 or hour > 12:
            raise ValueError(f"Invalid 12-hour time: {raw}")
        if ampm == "pm" and hour != 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
    elif hour > 23 or minute > 59:
        raise ValueError(f"Invalid 24-hour time: {raw}")

    return f"{hour:02d}:{minute:02d}"


def load_template(date_str: str, template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    replacements = {
        "{{date:YYYY-MM-DD}}": dt.strftime("%Y-%m-%d"),
        "{{date:dddd, MMMM D, YYYY}}": dt.strftime("%A, %B ") + str(dt.day) + dt.strftime(", %Y"),
    }
    for old, new in replacements.items():
        template = template.replace(old, new)
    return template.rstrip() + "\n"


def ensure_note(note_path: Path, date_str: str, template_path: Path) -> None:
    if note_path.exists():
        return
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(load_template(date_str, template_path), encoding="utf-8")


def ensure_timeline_section(content: str, mode: str) -> str:
    if SECTION_HEADER in content:
        return content

    insertion = f"\n{SECTION_HEADER}\n\n"
    if mode == "table":
        insertion += "| Time | Activity | Location | Tags |\n|---|---|---|---|\n"

    notes_header = "\n## Notes"
    if notes_header in content:
        return content.replace(notes_header, insertion + notes_header, 1)
    return content.rstrip() + insertion


def parse_existing_entries(section_body: str) -> List[str]:
    lines = []
    for line in section_body.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    return lines


def sort_key_from_line(line: str) -> tuple:
    if line.startswith("|"):
        parts = [p.strip() for p in line.strip("|").split("|")]
        time_part = parts[0] if parts else "99:99"
    else:
        match = re.match(r"^-\s+(\d{2}:\d{2})\b", line)
        time_part = match.group(1) if match else "99:99"
    return (time_part, line.lower())


def render_entries(existing_lines: List[str], new_entries: List[Entry], mode: str) -> List[str]:
    combined = set(existing_lines)
    for entry in new_entries:
        combined.add(entry.to_table_row() if mode == "table" else entry.to_bullet())
    rendered = sorted(combined, key=sort_key_from_line)
    if mode == "table":
        header = ["| Time | Activity | Location | Tags |", "|---|---|---|---|"]
        data = [line for line in rendered if not line.startswith("| Time |") and not line.startswith("|---|")]
        return header + data
    return rendered


def update_timeline(content: str, new_entries: List[Entry], mode: str) -> str:
    content = ensure_timeline_section(content, mode)
    pattern = re.compile(rf"(^## Timeline\s*$)(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(content)
    if not match:
        raise RuntimeError("Timeline section not found after insertion")

    body = match.group(2).strip("\n")
    existing_lines = parse_existing_entries(body)
    merged_lines = render_entries(existing_lines, new_entries, mode)
    replacement = f"## Timeline\n\n" + "\n".join(merged_lines) + "\n\n"
    start, end = match.span()
    return content[:start] + replacement + content[end:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append timestamped entries to an Obsidian daily note.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD")
    parser.add_argument("--time", action="append", required=True, help="Time for one entry (repeat for multiple entries)")
    parser.add_argument("--text", action="append", required=True, help="Activity text for one entry (repeat in same order as --time)")
    parser.add_argument("--location", action="append", help="Optional location for one entry (repeat in same order)")
    parser.add_argument("--tags", action="append", help="Optional tags for one entry (repeat in same order)")
    parser.add_argument("--mode", choices=["bullets", "table"], default="bullets")
    parser.add_argument("--daily-dir", default=str(DEFAULT_DAILY_DIR))
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    return parser.parse_args()


def build_entries(args: argparse.Namespace) -> List[Entry]:
    times = args.time or []
    texts = args.text or []
    if len(times) != len(texts):
        raise ValueError("--time and --text counts must match")

    locations = args.location or []
    tags = args.tags or []
    entries: List[Entry] = []
    for i, (time_value, text_value) in enumerate(zip(times, texts)):
        location = locations[i] if i < len(locations) else None
        tag_value = tags[i] if i < len(tags) else None
        entries.append(Entry(time=normalize_time(time_value), text=text_value, location=location, tags=tag_value))
    return entries


def main() -> int:
    args = parse_args()
    entries = build_entries(args)
    note_path = Path(args.daily_dir) / f"{args.date}.md"
    template_path = Path(args.template)

    ensure_note(note_path, args.date, template_path)
    content = note_path.read_text(encoding="utf-8")
    updated = update_timeline(content, entries, args.mode)
    note_path.write_text(updated, encoding="utf-8")

    print(str(note_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
