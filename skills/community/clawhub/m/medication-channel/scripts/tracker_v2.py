#!/usr/bin/env python3
"""
Deterministic medication event tracker.

Environment variables:
  MEDICATION_TIMEZONE — IANA timezone string (required, e.g. America/Los_Angeles)
  WORKSPACE           — root workspace directory (optional, default: ~/.openclaw/workspace)

Medication configuration:
  Edit MORNING_MEDS, EVENING_MEDS, KNOWN_MEDS, and the aliases dict in
  canonical_medication() to match your regimen.
"""

import csv
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TZ_STR = os.environ.get("MEDICATION_TIMEZONE", "UTC")
TIMEZONE = ZoneInfo(TZ_STR)
WORKSPACE = os.environ.get("WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
DATA_DIR = os.path.join(WORKSPACE, "data")
STRUCTURED_LOG_FILE = os.path.join(DATA_DIR, "medication_log_v2.csv")
CSV_FIELDS = [
    "entry_id",
    "timestamp_utc",
    "date_local",
    "time_local",
    "timezone",
    "window",
    "event_type",
    "medication",
    "notes",
    "source_channel_id",
    "source_message_id",
    "source_author_id",
]

# ---------------------------------------------------------------------------
# Medication configuration — edit these lists to match your regimen
# ---------------------------------------------------------------------------
MORNING_MEDS: list[str] = []  # e.g. ["MedA", "MedB"]
EVENING_MEDS: list[str] = []  # e.g. ["MedC"]
KNOWN_MEDS: list[str] = []    # e.g. ["MedA", "MedB", "MedC"]

TAKEN_WORDS = {"taken", "take", "took", "done", "complete", "completed"}
MISSED_WORDS = {"missed", "skip", "skipped", "skipping"}


@dataclass
class ParsedMedicationEvent:
    event_type: str
    medication: str
    window: str
    notes: str


def ensure_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def initialize_logs() -> None:
    ensure_dirs()
    if not os.path.exists(STRUCTURED_LOG_FILE):
        with open(STRUCTURED_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def read_rows() -> list[dict]:
    initialize_logs()
    with open(STRUCTURED_LOG_FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_structured_row(row: dict) -> None:
    initialize_logs()
    with open(STRUCTURED_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(row)


def next_entry_id(rows: list[dict]) -> str:
    max_num = 0
    for row in rows:
        m = re.match(r"med-(\d+)", row.get("entry_id", ""))
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"med-{max_num + 1:06d}"


def format_time_local(dt_local: datetime) -> str:
    try:
        return dt_local.strftime("%-I:%M%p").lower()
    except ValueError:
        return dt_local.strftime("%I:%M%p").lstrip("0").lower()


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def canonical_medication(raw: str) -> str:
    """Normalize a medication name. Add your aliases here."""
    lowered = raw.strip().lower()
    # Example aliases — extend for your medications:
    # aliases = {
    #     "meda": "MedA",
    #     "med-a": "MedA",
    # }
    # return aliases.get(lowered, raw.strip())
    return raw.strip()


def detect_medications(lowered: str) -> list[str]:
    found = []
    for med in KNOWN_MEDS:
        if med.lower() in lowered:
            found.append(med)
    return found


def infer_window(text: str, dt_local: datetime | None = None) -> str:
    lowered = text.lower()
    if "morning" in lowered:
        return "morning"
    if "evening" in lowered or "night" in lowered:
        return "evening"
    if dt_local:
        return "morning" if dt_local.hour < 15 else "evening"
    return "unknown"


def parse_event(text: str, timestamp_utc: str | None = None) -> ParsedMedicationEvent:
    raw = normalize_ws(text)
    lowered = raw.lower()
    dt_local = None
    if timestamp_utc:
        dt_utc = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
        dt_local = dt_utc.astimezone(TIMEZONE)

    window = infer_window(raw, dt_local)
    found_meds = detect_medications(lowered)

    if lowered == "done" or lowered.endswith(" meds taken") or lowered.endswith(" medications taken"):
        return ParsedMedicationEvent("taken", "ALL", window, raw)

    if any(word in lowered for word in MISSED_WORDS):
        medication = found_meds[0] if found_meds else "UNSPECIFIED"
        return ParsedMedicationEvent("missed", medication, window, raw)

    if lowered.startswith("extra "):
        return ParsedMedicationEvent("extra", canonical_medication(raw[6:]), window, raw)

    if any(word in lowered.split() for word in TAKEN_WORDS) or "took my" in lowered:
        medication = found_meds[0] if found_meds else ("ALL" if "morning" in lowered or "evening" in lowered else "UNSPECIFIED")
        return ParsedMedicationEvent("taken", medication, window, raw)

    return ParsedMedicationEvent("unknown", "", window, raw)


def build_row(
    rows: list[dict],
    parsed: ParsedMedicationEvent,
    channel_id: str = "",
    message_id: str = "",
    author_id: str = "",
    timestamp_utc: str | None = None,
) -> dict:
    if not timestamp_utc:
        raise ValueError("timestamp_utc is required — source Discord message timestamp must be provided")
    dt_utc = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
    dt_local = dt_utc.astimezone(TIMEZONE)
    return {
        "entry_id": next_entry_id(rows),
        "timestamp_utc": dt_utc.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "date_local": dt_local.strftime("%Y-%m-%d"),
        "time_local": format_time_local(dt_local),
        "timezone": TZ_STR,
        "window": parsed.window,
        "event_type": parsed.event_type,
        "medication": parsed.medication,
        "notes": parsed.notes,
        "source_channel_id": channel_id,
        "source_message_id": message_id,
        "source_author_id": author_id,
    }


def dedupe_exists(rows: list[dict], source_message_id: str) -> dict | None:
    if not source_message_id:
        return None
    for row in rows:
        if row.get("source_message_id") == source_message_id:
            return row
    return None


def log_from_message(
    text: str,
    channel_id: str = "",
    message_id: str = "",
    author_id: str = "",
    timestamp_utc: str | None = None,
) -> dict:
    rows = read_rows()
    existing = dedupe_exists(rows, message_id)
    if existing:
        return existing
    parsed = parse_event(text, timestamp_utc)
    row = build_row(rows, parsed, channel_id, message_id, author_id, timestamp_utc)
    append_structured_row(row)
    return row


def format_confirmation(row: dict) -> str:
    med = row["medication"]
    if med == "ALL":
        med_text = f"{row['window'].title()} meds"
    elif med == "UNSPECIFIED" or not med:
        med_text = f"{row['window'].title()} medication event"
    else:
        med_text = med

    verb_map = {
        "taken": "taken",
        "missed": "skipped",
        "extra": "logged as extra dose",
        "unknown": "recorded",
    }
    verb = verb_map.get(row["event_type"], "recorded")
    return f"Logged: **{med_text} {verb}** ({row['date_local']} {row['time_local'].upper()} {row['timezone']})."


def print_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def usage() -> int:
    print("Usage: tracker_v2.py log-from-message|format-confirmation|parse ...", file=sys.stderr)
    return 1


def main() -> int:
    initialize_logs()
    if len(sys.argv) < 2:
        return usage()

    cmd = sys.argv[1]
    if cmd == "log-from-message":
        if len(sys.argv) < 3:
            return usage()
        text = sys.argv[2]
        channel_id = sys.argv[3] if len(sys.argv) > 3 else ""
        message_id = sys.argv[4] if len(sys.argv) > 4 else ""
        author_id = sys.argv[5] if len(sys.argv) > 5 else ""
        timestamp_utc = sys.argv[6] if len(sys.argv) > 6 else None
        row = log_from_message(text, channel_id, message_id, author_id, timestamp_utc)
        print_json(row)
        return 0

    if cmd == "format-confirmation":
        if len(sys.argv) < 3:
            return usage()
        row = json.loads(sys.argv[2])
        print(format_confirmation(row))
        return 0

    if cmd == "parse":
        if len(sys.argv) < 3:
            return usage()
        text = sys.argv[2]
        timestamp_utc = sys.argv[3] if len(sys.argv) > 3 else None
        parsed = parse_event(text, timestamp_utc)
        print_json(parsed.__dict__)
        return 0

    return usage()


if __name__ == "__main__":
    raise SystemExit(main())
