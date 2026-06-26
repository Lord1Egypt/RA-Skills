#!/usr/bin/env bash
# Purge stale OpenClaw sessions (>24h) and stub memory files (<200 chars).
# Default: move to timestamped archive. Use --delete for immediate deletion (no archive).
# Part of inference-optimizer skill. Run on VPS.

set -euo pipefail

SESSIONS="${OPENCLAW_SESSIONS:-$HOME/.openclaw/agents/main/sessions}"
[[ -d "$SESSIONS" ]] || SESSIONS="$HOME/.clawdbot/agents.main/sessions"
MEMORY_DIR="$HOME/.openclaw/workspace-whatsapp/memory"
[[ -d "$MEMORY_DIR" ]] || MEMORY_DIR="$HOME/clawd/memory"
ARCHIVE_BASE="${OPENCLAW_ARCHIVE:-$HOME/openclaw-purge-archive}"

DO_DELETE=false
[[ "${1:-}" = "--delete" ]] && DO_DELETE=true
SESSION_ACTION_COUNT=0
MEMORY_ACTION_COUNT=0
SESSION_ACTION_LABEL="archived"
MEMORY_ACTION_LABEL="archived"

if [[ ! -d "$SESSIONS" ]]; then
  echo "Sessions dir not found (run on VPS): $SESSIONS"
  exit 0
fi

if [[ "$DO_DELETE" = true ]]; then
  SESSION_ACTION_LABEL="deleted"
  MEMORY_ACTION_LABEL="deleted"
  echo "=== Delete stale sessions (>24h) [no archive] ==="
  BEFORE=$(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)
  find "$SESSIONS" -type f -name "*.jsonl" -mtime +1 -delete 2>/dev/null || true
  AFTER=$(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)
  SESSION_ACTION_COUNT=$((BEFORE - AFTER))
  echo "  Sessions: $BEFORE -> $AFTER (${SESSION_ACTION_LABEL} $SESSION_ACTION_COUNT)"
else
  ARCHIVE_DIR="$ARCHIVE_BASE/$(date +%Y-%m-%d-%H%M%S)"
  mkdir -p "$ARCHIVE_DIR/sessions" "$ARCHIVE_DIR/memory"
  echo "=== Archive stale sessions (>24h) ==="
  BEFORE=$(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)
  MOVED=0
  while IFS= read -r -d '' f; do
    mv "$f" "$ARCHIVE_DIR/sessions/" 2>/dev/null && ((MOVED++)) || true
  done < <(find "$SESSIONS" -type f -name "*.jsonl" -mtime +1 -print0 2>/dev/null)
  AFTER=$(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)
  SESSION_ACTION_COUNT=$MOVED
  echo "  Sessions: $BEFORE -> $AFTER (${SESSION_ACTION_LABEL} $SESSION_ACTION_COUNT to $ARCHIVE_DIR/sessions/)"
fi

echo ""
echo "=== Stub memory files (<200 chars) ==="
PURGED=0
if [[ -d "$MEMORY_DIR" ]]; then
  shopt -s nullglob 2>/dev/null || true
  for f in "$MEMORY_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    if [[ $(wc -c < "$f") -lt 200 ]]; then
      if [[ "$DO_DELETE" = true ]]; then
        rm -f "$f" && ((PURGED++)) || true
        echo "  deleted $(basename "$f")"
      else
        mkdir -p "$ARCHIVE_DIR/memory"
        mv "$f" "$ARCHIVE_DIR/memory/" 2>/dev/null && ((PURGED++)) || true
        echo "  archived $(basename "$f")"
      fi
    fi
  done
  [[ $PURGED -eq 0 ]] && echo "  none found" || true
else
  echo "  memory dir not found: $MEMORY_DIR"
fi
MEMORY_ACTION_COUNT=$PURGED

if [[ "$DO_DELETE" != true ]]; then
  echo ""
  echo "  Archive: ${ARCHIVE_DIR:-$ARCHIVE_BASE/...} (verify contents, then rm -rf to free disk)"
fi

echo ""
echo "=== Verify ==="
echo "  Sessions: $(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)"
echo "  Memory files: $(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)"
echo ""
echo "=== Summary ==="
if [[ "$DO_DELETE" = true ]]; then
  echo "  Mode: delete (no archive)"
else
  echo "  Mode: archive-first"
  echo "  Archive directory: ${ARCHIVE_DIR:-$ARCHIVE_BASE/...}"
fi
echo "  Sessions stale $SESSION_ACTION_LABEL: $SESSION_ACTION_COUNT"
echo "  Memory stub files $MEMORY_ACTION_LABEL: $MEMORY_ACTION_COUNT"
