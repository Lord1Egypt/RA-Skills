#!/usr/bin/env bash
# Fetch a single OpenClaw doc page.
# Usage: fetch.sh <path>
# Accepts with/without leading slash. If no extension is given, .md is assumed.
# Recognized extensions are preserved (.md, .json, .txt, .yaml, .yml).
# Examples:
#   fetch.sh concepts/soul
#   fetch.sh concepts/soul.md
#   fetch.sh /channels/telegram.md
#   fetch.sh api-reference/openapi.json
set -eu
[ $# -lt 1 ] && { echo "usage: $0 <path>" >&2; exit 2; }
path="$1"
path="${path#/}"
case "$path" in
  *.md|*.json|*.txt|*.yaml|*.yml) ;;
  *) path="${path}.md" ;;
esac
curl -sfL "https://docs.openclaw.ai/${path}"
