#!/usr/bin/env bash
set -euo pipefail

required=(
  "SKILL.md"
  "docs/review-checklist.md"
  "docs/assessment-notes.md"
  "examples/sample-skill.md"
  "templates/publish-request.md"
  "assets/package-manifest.json"
)

for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing required file: $file" >&2
    exit 1
  fi
done

grep -q "^name:" SKILL.md
grep -q "^version:" SKILL.md
grep -q '"version": "0.2.0"' assets/package-manifest.json

echo "validation passed"
