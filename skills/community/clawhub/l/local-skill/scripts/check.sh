#!/usr/bin/env bash
set -euo pipefail

echo "Running repository checks..."

test -f package.json
test -f README.md
test -f src/index.js
test -f scripts/publish.sh
test -f docs/release.md

node -e "const pkg=require('./package.json'); if(!pkg.name || !pkg.version){process.exit(1)}"
node -e "const skill=require('./src'); if(typeof skill.inspectSkill !== 'function'){process.exit(1)}"

echo "All checks passed."
