#!/usr/bin/env sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
WORKSPACE_ROOT="$(CDPATH= cd -- "$ROOT/../.." && pwd)"
PACKAGE_JSON="$ROOT/package.json"
CHANGELOG_MD="$ROOT/CHANGELOG.md"
VALIDATOR="$WORKSPACE_ROOT/tmp/validate_clawhub_skill_dir.sh"
VERSION="$(node -e "process.stdout.write(require(process.argv[1]).version)" "$PACKAGE_JSON")"
CHANGELOG="$(node -e "const fs=require('fs'); const text=fs.readFileSync(process.argv[1], 'utf8'); const match=text.match(/Suggested one-line changelog:\\n- (.+)/); process.stdout.write(match ? match[1] : 'Launch PriceTide.');" "$CHANGELOG_MD")"
TAGS="latest,shopping,buy-timing,price-history,wait-or-buy,deal-timing,ecommerce,taobao,jd,pdd"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found in PATH" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required to read version and changelog metadata" >&2
  exit 1
fi

if [ -f "$VALIDATOR" ]; then
  bash "$VALIDATOR" "$ROOT"
fi

echo "Publishing PriceTide from: $ROOT"
echo "Version: $VERSION"
echo "Tags: $TAGS"

clawhub publish "$ROOT" \
  --slug pricetide \
  --name "PriceTide" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "$TAGS"
