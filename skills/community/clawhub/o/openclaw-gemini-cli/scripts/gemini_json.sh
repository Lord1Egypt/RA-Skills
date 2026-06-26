#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 '<instruction asking for strict JSON>'" >&2
  exit 1
fi

prompt="$1"
exec gemini -p "Return only valid JSON. No markdown fences. ${prompt}"
