#!/bin/bash
# meeting-context.sh — Quick meeting context for OpenClaw agents
# Usage: ./meeting-context.sh [search|recent|today|speakers|actions|sync|status] [args...]

set -euo pipefail

PERCEPT_CMD="${PERCEPT_CMD:-percept}"

case "${1:-status}" in
  search)
    shift
    $PERCEPT_CMD search "$@"
    ;;
  recent)
    $PERCEPT_CMD transcripts --limit "${2:-5}"
    ;;
  today)
    $PERCEPT_CMD transcripts --today
    ;;
  speakers)
    $PERCEPT_CMD speakers
    ;;
  actions)
    $PERCEPT_CMD actions --limit "${2:-10}"
    ;;
  sync)
    # Sync all sources
    echo "=== Granola ===" 
    $PERCEPT_CMD granola-sync 2>/dev/null || echo "Granola: not available"
    echo "=== Zoom ==="
    $PERCEPT_CMD zoom-sync --days "${2:-7}" 2>/dev/null || echo "Zoom: not configured"
    ;;
  status)
    $PERCEPT_CMD status
    ;;
  *)
    echo "Usage: meeting-context.sh [search|recent|today|speakers|actions|sync|status] [args...]"
    exit 1
    ;;
esac
