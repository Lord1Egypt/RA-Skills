#!/usr/bin/env sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
VERSION="$(node -e "process.stdout.write(require(process.argv[1]).version)" "$ROOT/package.json")"
CHANGELOG="$(node -e "const fs=require('fs'); const text=fs.readFileSync(process.argv[1], 'utf8'); const match=text.match(/Suggested one-line changelog:\\n- (.+)/); process.stdout.write(match ? match[1] : 'Initial release of NextFromKnowledge.');" "$ROOT/CHANGELOG.md")"

clawhub publish "$ROOT" \
  --slug next-from-knowledge \
  --name "NextFromKnowledge" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "knowledge,action,planning,decision,experiment,productivity"
