#!/usr/bin/env bash
# tag-untrusted.sh — Wrap command output in untrusted content tags
# Usage: tag-untrusted.sh <source_label> "<command>"
# Example: tag-untrusted.sh gmail gog gmail search 'newer_than:4h' --max 5 --json --no-input
set -euo pipefail

SOURCE="${1:?Usage: tag-untrusted.sh <source> <command> [args...]}"
shift

echo "<untrusted_content source=\"${SOURCE}\">"
"$@" 2>&1 || true
echo "</untrusted_content>"
