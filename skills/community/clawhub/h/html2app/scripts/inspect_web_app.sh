#!/usr/bin/env bash
set -euo pipefail

project_dir="${1:-.}"
cd "$project_dir"

echo "Project: $(pwd)"
echo "Likely HTML entry points:"
find . \( -path './node_modules' -o -path './release' -o -path './dist' -o -path './build' \) -prune -o -type f \( -name 'index.html' -o -name '*.html' \) -print | sed -n '1,30p'

if [[ -f package.json ]]; then
  echo
  echo "package.json scripts:"
  node -e 'const p=require("./package.json"); console.log(JSON.stringify(p.scripts || {}, null, 2))'
fi

echo
echo "Potential online dependencies:"
rg -n --glob '!node_modules/**' --glob '!release/**' --glob '!dist/**' --glob '!build/**' --glob '!package-lock.json' 'https?://|wss?://' . || true
