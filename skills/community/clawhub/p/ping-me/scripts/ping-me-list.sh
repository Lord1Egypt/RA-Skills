#!/bin/bash
# List active ping-me reminders with formatted output.
# All data parsing uses stdin — no inline string embedding.
set -euo pipefail

OPENCLAW=$(which openclaw 2>/dev/null || echo "openclaw")

# Try JSON output first, fall back to plain text
OUTPUT=$("$OPENCLAW" cron list --json 2>&1) || OUTPUT=""

if [ -z "$OUTPUT" ] || echo "$OUTPUT" | grep -q "No cron jobs"; then
  echo "📋 No active reminders."
  exit 0
fi

# Parse JSON safely via stdin
echo "$OUTPUT" | python3 -c '
import json, sys

try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    print("📋 Could not parse cron output.")
    sys.exit(0)

jobs_list = data.get("jobs", data) if isinstance(data, dict) else data
if not isinstance(jobs_list, list):
    print("📋 No active reminders.")
    sys.exit(0)

jobs = [j for j in jobs_list if isinstance(j, dict) and j.get("name", "") in ("ping-me", "reminder")]

if not jobs:
    print("📋 No active reminders.")
    sys.exit(0)

print(f"📋 Active reminders ({len(jobs)}):")
print()
for j in jobs:
    jid = j.get("id", "?")[:8]
    desc = j.get("description", "")
    if not desc:
        payload = j.get("payload", {})
        desc = payload.get("message", "?") if isinstance(payload, dict) else "?"
    sched = j.get("schedule", {})
    at = sched.get("at", sched.get("cron", "?")) if isinstance(sched, dict) else "?"
    enabled = "✅" if j.get("enabled", True) else "❌"
    delivery = j.get("delivery", {})
    channel = delivery.get("channel", "?") if isinstance(delivery, dict) else "?"
    print(f"  {enabled} [{jid}] {at}")
    print(f"     {desc}")
    print(f"     Channel: {channel}")
    print()
' 2>/dev/null || {
  # Fallback if python parsing fails entirely
  echo "📋 Active reminders:"
  echo "$OUTPUT" | grep -A1 "ping-me\|reminder" || echo "(none found)"
}
