#!/bin/bash
# check_download_status.sh
# Reads the current download session's progress log and per-file snapshots,
# then outputs a clean structured status report for the AI to parse and present.

PROGRESS_LOG="/tmp/media_sync_progress.log"

# ── Check if any session exists ──────────────────────────────────────────────
if [[ ! -f "$PROGRESS_LOG" ]]; then
  echo "STATUS: IDLE"
  echo "DETAIL: No download session found. No log at $PROGRESS_LOG."
  exit 0
fi

# ── Read main session fields ─────────────────────────────────────────────────
get_field() { grep "^$1=" "$PROGRESS_LOG" | tail -1 | cut -d'=' -f2-; }

SESSION_ID=$(get_field SESSION_ID)
SESSION_START=$(get_field SESSION_START)
SESSION_END=$(get_field SESSION_END)
DEST=$(get_field DEST)
TOTAL=$(get_field TOTAL)
COMPLETED=$(get_field COMPLETED)
FAILED=$(get_field FAILED)
RUN_STATUS=$(get_field STATUS)
ACTIVE_FILE=$(get_field ACTIVE_FILE)

# ── If session ended more than 24h ago, treat as stale ──────────────────────
if [[ "$RUN_STATUS" == "DONE" && -n "$SESSION_END" ]]; then
  END_EPOCH=$(date -d "$SESSION_END" +%s 2>/dev/null || echo 0)
  NOW_EPOCH=$(date +%s)
  AGE=$(( NOW_EPOCH - END_EPOCH ))
  if [[ $AGE -gt 86400 ]]; then
    echo "STATUS: IDLE"
    echo "DETAIL: Last session ended at $SESSION_END (more than 24h ago). No active downloads."
    exit 0
  fi
fi

# ── Print session header ─────────────────────────────────────────────────────
echo "STATUS: $RUN_STATUS"
echo "SESSION_START: $SESSION_START"
[[ -n "$SESSION_END" ]] && echo "SESSION_END: $SESSION_END"
echo "DEST: $DEST"
echo "PROGRESS: $COMPLETED of $TOTAL completed, $FAILED failed"
[[ "$RUN_STATUS" == "RUNNING" && -n "$ACTIVE_FILE" && "$ACTIVE_FILE" != "none" ]] \
  && echo "ACTIVE_FILE_INDEX: $ACTIVE_FILE"
echo ""

# ── Per-file snapshots ───────────────────────────────────────────────────────
get_snap_field() { grep "^$2=" "$1" | tail -1 | cut -d'=' -f2-; }

SNAP_FILES=( $(ls /tmp/media_sync_snap_${SESSION_ID}_*.log 2>/dev/null | sort -t_ -k5 -n) )

if [[ ${#SNAP_FILES[@]} -eq 0 ]]; then
  echo "NOTE: No per-file snapshots found yet (download may just be starting)."
  exit 0
fi

for SNAP in "${SNAP_FILES[@]}"; do
  IDX=$(get_snap_field "$SNAP" INDEX)
  URL=$(get_snap_field "$SNAP" URL)
  FILE_STATUS=$(get_snap_field "$SNAP" FILE_STATUS)
  PERCENT=$(get_snap_field "$SNAP" PERCENT)
  SPEED=$(get_snap_field "$SNAP" SPEED)
  ETA=$(get_snap_field "$SNAP" ETA)
  SIZE=$(get_snap_field "$SNAP" SIZE)
  FILENAME=$(get_snap_field "$SNAP" FILENAME)
  ERROR_CODE=$(get_snap_field "$SNAP" ERROR_CODE)

  echo "── File $IDX of $TOTAL ──────────────────────"

  case "$FILE_STATUS" in
    DOWNLOADING)
      echo "  STATUS:   Downloading"
      echo "  FILE:     $FILENAME"
      echo "  PERCENT:  $PERCENT"
      echo "  SPEED:    $SPEED"
      echo "  ETA:      $ETA"
      echo "  SIZE:     $SIZE (estimated)"
      ;;
    DONE)
      echo "  STATUS:   ✓ Complete"
      echo "  FILE:     $FILENAME"
      echo "  SIZE:     $SIZE"
      ;;
    FAILED)
      echo "  STATUS:   ✗ Failed"
      echo "  FILE:     $FILENAME"
      [[ -n "$ERROR_CODE" ]] && echo "  EXIT CODE: $ERROR_CODE"
      echo "  URL:      $URL"
      ;;
    *)
      echo "  STATUS:   Pending / starting..."
      echo "  URL:      $URL"
      ;;
  esac
  echo ""
done

# ── Summary footer ───────────────────────────────────────────────────────────
if [[ "$RUN_STATUS" == "DONE" ]]; then
  if [[ "$FAILED" -eq 0 ]]; then
    echo "SUMMARY: All $TOTAL file(s) downloaded successfully to $DEST"
  else
    echo "SUMMARY: $COMPLETED of $TOTAL succeeded. $FAILED failed. See above for details."
  fi
elif [[ "$RUN_STATUS" == "RUNNING" ]]; then
  REMAINING=$(( TOTAL - COMPLETED - FAILED ))
  echo "SUMMARY: Download in progress. $COMPLETED done, $FAILED failed, $REMAINING remaining."
fi

exit 0