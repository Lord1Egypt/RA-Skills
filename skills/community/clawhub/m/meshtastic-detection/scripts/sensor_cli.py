#!/usr/bin/env python3
"""
Sensor CLI — Query tool for AI detection data stored by usb_receiver.py.

Commands:
    sensor_cli.py latest [--type TYPE] [--limit N]
    sensor_cli.py query  --type TYPE [--min-confidence F] [--since DURATION]
    sensor_cli.py stats  [--since DURATION]
    sensor_cli.py status

All output is JSON for easy parsing by AI agents.
"""

import json
import sys
import argparse
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

DEFAULT_DATA_DIR = os.environ.get(
    "MESH_DATA_DIR",
    str(Path(__file__).resolve().parent.parent / "data"),
)
PID_INDICATOR_FILE = "/tmp/meshtastic_receiver.pid"

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════


def parse_duration(duration_str: str) -> timedelta:
    """Parse a human-friendly duration string into a timedelta.

    Supports: 30s, 5m, 2h, 1d, 7d, 1h30m, etc.
    """
    if not duration_str:
        raise ValueError("Empty duration string")

    pattern = re.compile(r"(\d+)\s*([smhd])", re.IGNORECASE)
    matches = pattern.findall(duration_str)
    if not matches:
        raise ValueError(f"Invalid duration: {duration_str}")

    total = timedelta()
    for value, unit in matches:
        v = int(value)
        if unit == "s":
            total += timedelta(seconds=v)
        elif unit == "m":
            total += timedelta(minutes=v)
        elif unit == "h":
            total += timedelta(hours=v)
        elif unit == "d":
            total += timedelta(days=v)
    return total


def load_records(data_dir: str, max_lines: int = 10000) -> list[dict]:
    """Load records from JSONL files (current + archives). Returns newest last.

    Reads archives (.2, .1) first, then the current file, so result is
    chronologically ordered.
    """
    data_path = Path(data_dir)
    files_to_read = []

    for i in range(9, 0, -1):
        archive = data_path / f"sensor_data.jsonl.{i}"
        if archive.exists():
            files_to_read.append(archive)
    current = data_path / "sensor_data.jsonl"
    if current.exists():
        files_to_read.append(current)

    records = []
    for fpath in files_to_read:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                    if len(records) >= max_lines:
                        return records
        except Exception:
            continue
    return records


def load_latest(data_dir: str) -> dict:
    """Load the latest.json cache."""
    latest_path = Path(data_dir) / "latest.json"
    if not latest_path.exists():
        return {}
    try:
        return json.loads(latest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_timestamp(ts_str: str) -> datetime:
    """Parse an ISO timestamp, handling timezone-naive and timezone-aware strings."""
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def output_json(data) -> None:
    """Print JSON output and exit."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ═══════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════


def cmd_latest(args):
    """Show the latest N detection records, optionally filtered by type."""
    records = load_records(args.data_dir)

    if args.type:
        records = [
            r for r in records if r.get("data", {}).get("type") == args.type
        ]

    records = records[-args.limit :]

    output_json({
        "command": "latest",
        "count": len(records),
        "records": records,
    })


def cmd_query(args):
    """Query records with filters: type, min-confidence, since."""
    records = load_records(args.data_dir)
    now = datetime.now(timezone.utc)

    if args.since:
        try:
            delta = parse_duration(args.since)
            cutoff = now - delta
            records = [
                r
                for r in records
                if parse_timestamp(r.get("received_at", "")) >= cutoff
            ]
        except ValueError as e:
            output_json({"error": str(e)})
            sys.exit(1)

    if args.type:
        records = [
            r for r in records if r.get("data", {}).get("type") == args.type
        ]

    if args.min_confidence is not None:
        records = [
            r
            for r in records
            if r.get("data", {}).get("confidence", 0) >= args.min_confidence
        ]

    records = records[-args.limit :]

    output_json({
        "command": "query",
        "filters": {
            "type": args.type,
            "min_confidence": args.min_confidence,
            "since": args.since,
        },
        "count": len(records),
        "records": records,
    })


def cmd_stats(args):
    """Show detection statistics grouped by type."""
    records = load_records(args.data_dir)
    now = datetime.now(timezone.utc)

    if args.since:
        try:
            delta = parse_duration(args.since)
            cutoff = now - delta
            records = [
                r
                for r in records
                if parse_timestamp(r.get("received_at", "")) >= cutoff
            ]
        except ValueError as e:
            output_json({"error": str(e)})
            sys.exit(1)

    type_counts: dict[str, int] = {}
    type_avg_confidence: dict[str, list[float]] = {}
    senders: set[str] = set()

    for r in records:
        data = r.get("data", {})
        det_type = data.get("type", "unknown")
        confidence = data.get("confidence")
        sender = r.get("sender", "")

        type_counts[det_type] = type_counts.get(det_type, 0) + 1
        if confidence is not None:
            type_avg_confidence.setdefault(det_type, []).append(confidence)
        if sender:
            senders.add(sender)

    by_type = {}
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        entry = {"count": count}
        if t in type_avg_confidence and type_avg_confidence[t]:
            vals = type_avg_confidence[t]
            entry["avg_confidence"] = round(sum(vals) / len(vals), 3)
            entry["max_confidence"] = round(max(vals), 3)
        by_type[t] = entry

    first_ts = records[0].get("received_at", "") if records else None
    last_ts = records[-1].get("received_at", "") if records else None

    output_json({
        "command": "stats",
        "since": args.since,
        "total_records": len(records),
        "unique_senders": len(senders),
        "first_record": first_ts,
        "last_record": last_ts,
        "by_type": by_type,
    })


def cmd_status(args):
    """Check receiver daemon health and data summary."""
    data_dir = Path(args.data_dir)
    jsonl_path = data_dir / "sensor_data.jsonl"
    latest_path = data_dir / "latest.json"

    record_count = 0
    file_size_kb = 0
    last_record_time = None
    archive_count = 0

    if jsonl_path.exists():
        file_size_kb = round(jsonl_path.stat().st_size / 1024, 1)
        try:
            with open(jsonl_path, "r", encoding="utf-8") as f:
                last_line = ""
                for line in f:
                    if line.strip():
                        record_count += 1
                        last_line = line
                if last_line:
                    last_record = json.loads(last_line)
                    last_record_time = last_record.get("received_at")
        except Exception:
            pass

    for i in range(1, 10):
        archive = data_dir / f"sensor_data.jsonl.{i}"
        if archive.exists():
            archive_count += 1
            file_size_kb += round(archive.stat().st_size / 1024, 1)
        else:
            break

    latest = load_latest(args.data_dir)

    # Check if the receiver process is running (simple PID file check)
    receiver_running = False
    if os.path.exists(PID_INDICATOR_FILE):
        try:
            pid = int(Path(PID_INDICATOR_FILE).read_text().strip())
            os.kill(pid, 0)
            receiver_running = True
        except (ValueError, ProcessLookupError, PermissionError):
            pass

    output_json({
        "command": "status",
        "receiver_running": receiver_running,
        "data_dir": str(data_dir),
        "jsonl_file": str(jsonl_path),
        "record_count": record_count,
        "archive_files": archive_count,
        "total_size_kb": file_size_kb,
        "last_record_time": last_record_time,
        "detection_types_in_latest": list(latest.keys()),
    })


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="Query detection data from Meshtastic Detection Sensor"
    )
    parser.add_argument(
        "--data-dir",
        default=DEFAULT_DATA_DIR,
        help="Data storage directory",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # latest
    p_latest = subparsers.add_parser("latest", help="Latest N detection records")
    p_latest.add_argument("--type", "-t", help="Filter by detection type")
    p_latest.add_argument(
        "--limit", "-l", type=int, default=10, help="Max records (default 10)"
    )

    # query
    p_query = subparsers.add_parser("query", help="Query records with filters")
    p_query.add_argument("--type", "-t", help="Filter by detection type")
    p_query.add_argument(
        "--min-confidence", "-c", type=float, help="Minimum confidence (0.0-1.0)"
    )
    p_query.add_argument(
        "--since", "-s", help="Time window (e.g. 30m, 2h, 1d)"
    )
    p_query.add_argument(
        "--limit", "-l", type=int, default=50, help="Max records (default 50)"
    )

    # stats
    p_stats = subparsers.add_parser("stats", help="Detection statistics")
    p_stats.add_argument(
        "--since", "-s", help="Time window (e.g. 1h, 24h, 7d)"
    )

    # status
    subparsers.add_parser("status", help="Receiver daemon status")

    args = parser.parse_args()

    commands = {
        "latest": cmd_latest,
        "query": cmd_query,
        "stats": cmd_stats,
        "status": cmd_status,
    }

    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        output_json({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
