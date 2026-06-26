#!/usr/bin/env bash
set -euo pipefail

# recover_tier2_delivery.sh — Poll pending Tier 2 artifacts, download completed ones,
# and update delivery-status.json.
#
# Usage:
#   recover_tier2_delivery.sh [output_dir]
#
# Scans output/<slug>/delivery-status.json for pending artifacts, polls their
# status, downloads completed ones, and updates the status file.
# Designed to run as a cron job every 5 minutes.
#
# Telegram delivery is agent-only (requires OpenClaw message tool).
# This script handles download + status tracking so files are ready
# when the user checks, or for a subsequent agent run to deliver.
#
# Environment:
#   RECOVERY_TTL_HOURS  — skip status files older than this (default: 24)
#
# Exit codes:
#   0  — all done or nothing to do
#   1  — auth failure (needs notebooklm login)
#   2  — partial failure (some artifacts failed)

# --- Concurrent-run guard ---
exec 200>/tmp/recover_tier2_delivery.lock
flock -n 200 || { echo "Already running"; exit 0; }

OUTPUT_DIR="${1:-./output}"
TTL_HOURS="${RECOVERY_TTL_HOURS:-24}"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Output directory not found: $OUTPUT_DIR" >&2
  exit 0
fi

# Pre-flight: auth check
AUTH_STATUS=$(notebooklm auth check --test --json 2>/dev/null || echo '{"status":"error"}')
if echo "$AUTH_STATUS" | grep -q '"status": *"error"'; then
  echo "Auth check failed — run 'notebooklm login' first" >&2
  exit 1
fi

HAS_FAILURE=0
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for STATUS_FILE in "$OUTPUT_DIR"/*/delivery-status.json; do
  [ -f "$STATUS_FILE" ] || continue

  SLUG_DIR="$(dirname "$STATUS_FILE")"

  # Read pending artifacts + notebook_id, skip stale files
  READ_OUTPUT=$(python3 - "$STATUS_FILE" "$TTL_HOURS" <<'PYEOF'
import json, sys
from datetime import datetime, timedelta, timezone

status_file = sys.argv[1]
ttl_hours = int(sys.argv[2])

with open(status_file) as f:
    data = json.load(f)

# TTL check — skip if older than threshold
created_at = data.get("created_at", "")
if created_at:
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - created > timedelta(hours=ttl_hours):
            sys.exit(0)  # stale, skip silently
    except ValueError:
        pass  # can't parse date, process anyway

notebook_id = data.get("notebook_id", "")
print(f"NOTEBOOK_ID={notebook_id}")

for a in data.get("artifacts", []):
    if a.get("status") == "pending":
        print(f"PENDING={a['type']}|{a['task_id']}|{a.get('output_path', '')}")
PYEOF
  ) || continue

  # Parse notebook_id
  NOTEBOOK_ID=$(echo "$READ_OUTPUT" | grep '^NOTEBOOK_ID=' | cut -d= -f2-)
  # Parse pending list
  PENDING_LINES=$(echo "$READ_OUTPUT" | grep '^PENDING=' | cut -d= -f2- || true)

  [ -z "$PENDING_LINES" ] && continue

  echo "Processing: $SLUG_DIR ($NOTEBOOK_ID)"

  while IFS='|' read -r TYPE TASK_ID OUTPUT_PATH; do
    [ -z "$TASK_ID" ] && continue

    echo "  Checking $TYPE (task: ${TASK_ID:0:12}...)"

    # Poll artifact status
    POLL_RESULT=$(notebooklm artifact poll "$TASK_ID" --json 2>/dev/null || echo '{"status":"unknown"}')
    STATUS=$(echo "$POLL_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "unknown")

    case "$STATUS" in
      completed)
        echo "  ✓ $TYPE completed — downloading"

        # Download
        notebooklm download "$TYPE" "$OUTPUT_PATH" -n "$NOTEBOOK_ID" 2>/dev/null && {
          # Post-process audio
          if [ "$TYPE" = "audio" ] && command -v ffmpeg >/dev/null 2>&1; then
            COMPRESSED="${OUTPUT_PATH%.mp3}_compressed.mp3"
            bash "$SCRIPT_DIR/compress_audio.sh" "$OUTPUT_PATH" "$COMPRESSED" 2>/dev/null && {
              echo "  ✓ Audio compressed: $COMPRESSED"
            } || true
          fi

          # Update status to completed (lookup by task_id, not index)
          python3 - "$STATUS_FILE" "$TASK_ID" "completed" <<'PYEOF'
import json, sys
status_file, task_id, new_status = sys.argv[1], sys.argv[2], sys.argv[3]
with open(status_file) as f:
    data = json.load(f)
for a in data["artifacts"]:
    if a.get("task_id") == task_id:
        a["status"] = new_status
        break
with open(status_file, "w") as f:
    json.dump(data, f, indent=2)
PYEOF
          echo "  ✓ $TYPE delivered"
        } || {
          echo "  ✗ $TYPE download failed" >&2
          HAS_FAILURE=1
        }
        ;;

      failed)
        echo "  ✗ $TYPE generation failed"
        python3 - "$STATUS_FILE" "$TASK_ID" "failed" "generation failed on server" <<'PYEOF'
import json, sys
status_file, task_id, new_status, error = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
with open(status_file) as f:
    data = json.load(f)
for a in data["artifacts"]:
    if a.get("task_id") == task_id:
        a["status"] = new_status
        a["error"] = error
        break
with open(status_file, "w") as f:
    json.dump(data, f, indent=2)
PYEOF
        HAS_FAILURE=1
        ;;

      processing|pending)
        echo "  … $TYPE still generating"
        ;;

      *)
        echo "  ? $TYPE unknown status: $STATUS"
        ;;
    esac

  done <<< "$PENDING_LINES"
done

if [ "$HAS_FAILURE" -eq 1 ]; then
  exit 2
fi

echo "Recovery check complete."
