#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <file> '<review instruction>'" >&2
  exit 1
fi

file="$1"
instruction="$2"

if [ ! -f "$file" ]; then
  echo "File not found: $file" >&2
  exit 1
fi

content=$(cat "$file")
exec gemini -p "You are reviewing a local file. ${instruction}

Return concise output.

FILE: ${file}

CONTENT:
${content}"
