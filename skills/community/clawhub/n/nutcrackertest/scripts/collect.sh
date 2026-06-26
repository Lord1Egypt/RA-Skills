#!/usr/bin/env bash
# collect.sh — Extract and structure session data from OpenClaw .jsonl files
# Usage: bash collect.sh <sessions_dir> [YYYY-MM-DD]
# Outputs a JSON array of session objects to stdout.

set -euo pipefail

SESSIONS_DIR="${1:-}"
TARGET_DATE="${2:-$(date +%Y-%m-%d)}"

if [ -z "$SESSIONS_DIR" ]; then
  echo '{"error": "Usage: collect.sh <sessions_dir> [YYYY-MM-DD]"}' >&2
  exit 1
fi

if [ ! -d "$SESSIONS_DIR" ]; then
  echo '{"error": "Sessions directory not found", "path": "'"$SESSIONS_DIR"'"}' >&2
  exit 1
fi

# Find .jsonl files modified on the target date, or scan all and filter by timestamp
JSONL_FILES=()
while IFS= read -r -d '' f; do
  JSONL_FILES+=("$f")
done < <(find "$SESSIONS_DIR" -name '*.jsonl' -print0 2>/dev/null)

if [ ${#JSONL_FILES[@]} -eq 0 ]; then
  echo '[]'
  exit 0
fi

# Process each session file, filtering messages by target date
# Output: JSON array of session objects
python3 - "${TARGET_DATE}" "${JSONL_FILES[@]}" << 'PYEOF'
import json
import sys
from datetime import datetime, timezone

target_date = sys.argv[1]
files = sys.argv[2:]
sessions = []

for filepath in files:
    session_data = {
        "file": filepath,
        "messages": [],
        "tool_calls": [],
        "session_start": None,
        "session_end": None,
        "total_cost": 0.0,
        "message_count": 0,
        "user_message_count": 0,
        "assistant_message_count": 0,
        "tool_result_count": 0,
        "has_target_date_messages": False
    }

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                timestamp = entry.get("timestamp", "")

                # Check if this entry falls on our target date
                if timestamp:
                    try:
                        ts_date = timestamp[:10]  # YYYY-MM-DD prefix
                        if ts_date == target_date:
                            session_data["has_target_date_messages"] = True
                    except (IndexError, ValueError):
                        pass

                entry_type = entry.get("type", "")

                if entry_type == "session":
                    if timestamp:
                        if session_data["session_start"] is None:
                            session_data["session_start"] = timestamp
                        session_data["session_end"] = timestamp
                    continue

                if entry_type != "message":
                    continue

                msg = entry.get("message", {})
                role = msg.get("role", "")
                content_blocks = msg.get("content", [])

                # Extract text content
                text_parts = []
                for block in content_blocks:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif isinstance(block, str):
                        text_parts.append(block)

                text = "\n".join(text_parts)

                # Extract cost
                cost = 0.0
                usage = msg.get("usage", entry.get("message.usage.cost.total", 0))
                if isinstance(usage, dict):
                    cost = usage.get("cost", {}).get("total", 0.0) or 0.0
                elif isinstance(usage, (int, float)):
                    cost = float(usage)

                session_data["total_cost"] += cost

                # Track timestamps
                if timestamp:
                    if session_data["session_start"] is None:
                        session_data["session_start"] = timestamp
                    session_data["session_end"] = timestamp

                # Count by role
                session_data["message_count"] += 1
                if role == "user":
                    session_data["user_message_count"] += 1
                elif role == "assistant":
                    session_data["assistant_message_count"] += 1
                elif role == "toolResult":
                    session_data["tool_result_count"] += 1
                    # Record tool call info
                    tool_info = {
                        "timestamp": timestamp,
                        "content_preview": text[:200] if text else "",
                        "success": "error" not in text.lower()[:500] if text else True
                    }
                    session_data["tool_calls"].append(tool_info)

                # Store message
                message_obj = {
                    "role": role,
                    "text": text,
                    "timestamp": timestamp,
                    "cost": cost
                }
                session_data["messages"].append(message_obj)

    except (IOError, OSError) as e:
        session_data["error"] = str(e)

    # Only include sessions that have messages on the target date
    if session_data["has_target_date_messages"] and session_data["messages"]:
        # Calculate duration
        if session_data["session_start"] and session_data["session_end"]:
            try:
                start = datetime.fromisoformat(session_data["session_start"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(session_data["session_end"].replace("Z", "+00:00"))
                session_data["duration_seconds"] = (end - start).total_seconds()
            except (ValueError, TypeError):
                session_data["duration_seconds"] = 0
        else:
            session_data["duration_seconds"] = 0

        # Filter messages to only those on target date
        session_data["messages"] = [
            m for m in session_data["messages"]
            if m.get("timestamp", "")[:10] == target_date
        ]

        # Remove internal tracking flag
        del session_data["has_target_date_messages"]
        sessions.append(session_data)

print(json.dumps(sessions, indent=2, default=str))
PYEOF
