#!/bin/bash
set -o pipefail
# downloader.sh
# Usage: downloader.sh <subfolder> <"url1 url2 ...">
# Downloads all URLs into /mnt/jellyfin_media/<subfolder> using yt-dlp.
# Writes structured progress snapshots to /tmp/media_sync_progress.log.

ROOT="/mnt/jellyfin_media"
SUBFOLDER="${1:-}"
LINKS_STR="${2:-}"
PROGRESS_LOG="/tmp/media_sync_progress.log"
SESSION_ID="$(date +%s)"

# ── Validate args ────────────────────────────────────────────────────────────
if [[ -z "$SUBFOLDER" ]]; then
  echo "ERROR: No subfolder specified."
  exit 1
fi

if [[ -z "$LINKS_STR" ]]; then
  echo "ERROR: No links provided."
  exit 1
fi

# ── Sanitize subfolder path ──────────────────────────────────────────────────
SAFE_SUB=$(echo "$SUBFOLDER" | sed 's|^\/*||; s|\/*$||; s|\.\.||g')
DEST="$ROOT/$SAFE_SUB"

# ── Ensure destination exists ────────────────────────────────────────────────
if ! mkdir -p "$DEST"; then
  echo "ERROR: Could not create directory '$DEST'. Check permissions."
  exit 1
fi

# ── Split links ──────────────────────────────────────────────────────────────
read -ra LINKS <<< "$LINKS_STR"
TOTAL=${#LINKS[@]}

# ── Initialize progress log ──────────────────────────────────────────────────
# Each session overwrites the log so status always reflects the current run.
cat > "$PROGRESS_LOG" <<EOF
SESSION_ID=$SESSION_ID
SESSION_START=$(date '+%Y-%m-%d %H:%M:%S')
DEST=$DEST
TOTAL=$TOTAL
COMPLETED=0
FAILED=0
STATUS=RUNNING
EOF

echo "INFO: Destination → $DEST"
echo "INFO: Total links  → $TOTAL"
echo "INFO: Progress log → $PROGRESS_LOG"
echo "────────────────────────────────────────"

# ── yt-dlp progress template ─────────────────────────────────────────────────
# Writes a snapshot file per-file during download, named by link index.
# Fields: filename, percent, speed, eta, total_bytes_estimate
PROGRESS_TMPL='%(progress.filename)s|%(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s|%(progress._total_bytes_estimate_str)s'

COMPLETED=0
FAILED=0

for i in "${!LINKS[@]}"; do
  URL="${LINKS[$i]}"
  IDX=$((i + 1))
  SNAP="/tmp/media_sync_snap_${SESSION_ID}_${IDX}.log"

  echo ""
  echo "[$IDX/$TOTAL] Starting: $URL"

  # Write initial per-file snapshot
  cat > "$SNAP" <<EOF
INDEX=$IDX
URL=$URL
FILE_STATUS=DOWNLOADING
PERCENT=0%
SPEED=N/A
ETA=N/A
SIZE=N/A
FILENAME=resolving...
EOF

  # Update main log to mark which file is active
  sed -i "s/^ACTIVE_FILE=.*//" "$PROGRESS_LOG" 2>/dev/null
  echo "ACTIVE_FILE=$IDX" >> "$PROGRESS_LOG"

  YTDLP_EXIT_FILE="/tmp/media_sync_exit_${SESSION_ID}_${IDX}"

  # Run yt-dlp with progress hooks writing to snap file
  ( yt-dlp \
    --output "$DEST/%(title)s.%(ext)s" \
    --no-playlist \
    --newline \
    --merge-output-format mkv \
    --progress-template "SNAP:$PROGRESS_TMPL" \
    --exec "echo DONE_FILE:%(filepath)q" \
    "$URL"; echo "$?" > "$YTDLP_EXIT_FILE" ) 2>&1 | \
  while IFS= read -r line; do
    echo "$line"  # pass through to stdout (captured by openclaw on finish)

    # Parse progress template lines
    if [[ "$line" == SNAP:* ]]; then
      DATA="${line#SNAP:}"
      IFS='|' read -r FNAME PCT SPEED ETA SIZE <<< "$DATA"
      cat > "$SNAP" <<EOF
INDEX=$IDX
URL=$URL
FILE_STATUS=DOWNLOADING
PERCENT=$PCT
SPEED=$SPEED
ETA=$ETA
SIZE=$SIZE
FILENAME=$(basename "$FNAME")
EOF
    fi

    # Parse completion line injected by --exec
    if [[ "$line" == DONE_FILE:* ]]; then
      FPATH="${line#DONE_FILE:}"
      FPATH="${FPATH//\'/}"  # strip quotes added by %q
      FSIZE=$(du -sh "$FPATH" 2>/dev/null | cut -f1)
      cat > "$SNAP" <<EOF
INDEX=$IDX
URL=$URL
FILE_STATUS=DONE
PERCENT=100%
SPEED=N/A
ETA=0s
SIZE=${FSIZE:-unknown}
FILENAME=$(basename "$FPATH")
EOF
    fi
  done

  # Read yt-dlp exit code written by subshell (survives the pipe)
  PIPE_EXIT=0
  if [[ -f "$YTDLP_EXIT_FILE" ]]; then
    PIPE_EXIT=$(cat "$YTDLP_EXIT_FILE")
    rm -f "$YTDLP_EXIT_FILE"
  fi

  if [[ $PIPE_EXIT -ne 0 ]]; then
    echo "WARN: yt-dlp exited with code $PIPE_EXIT for: $URL"
    FAILED=$((FAILED + 1))
    # Mark snap as failed
    sed -i 's/^FILE_STATUS=.*/FILE_STATUS=FAILED/' "$SNAP" 2>/dev/null
    echo "ERROR_CODE=$PIPE_EXIT" >> "$SNAP"
  else
    COMPLETED=$((COMPLETED + 1))
  fi

  # Update totals in main log
  sed -i "s/^COMPLETED=.*/COMPLETED=$COMPLETED/" "$PROGRESS_LOG"
  sed -i "s/^FAILED=.*/FAILED=$FAILED/" "$PROGRESS_LOG"
done

echo ""
echo "────────────────────────────────────────"

# ── Finalize main log ────────────────────────────────────────────────────────
sed -i "s/^STATUS=.*/STATUS=DONE/" "$PROGRESS_LOG"
sed -i "s/^ACTIVE_FILE=.*/ACTIVE_FILE=none/" "$PROGRESS_LOG"
echo "SESSION_END=$(date '+%Y-%m-%d %H:%M:%S')" >> "$PROGRESS_LOG"

if [[ $FAILED -eq 0 ]]; then
  echo "SUCCESS: All $TOTAL file(s) downloaded to $DEST"
  exit 0
else
  echo "PARTIAL: $COMPLETED/$TOTAL succeeded, $FAILED failed. Check warnings above."
  exit 1
fi