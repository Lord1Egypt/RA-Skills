#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Install Playwright locally (kept inside this skill folder)
if [[ ! -f package.json ]]; then
  cat > package.json <<'JSON'
{
  "name": "neomano-web-snapshot",
  "private": true,
  "type": "module",
  "dependencies": {
    "playwright": "^1.54.0"
  }
}
JSON
fi

bun install

# Install Chromium for Playwright (headless)
bunx playwright install chromium

echo "✓ Playwright ready"