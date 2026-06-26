#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

rm -rf memory
mkdir -p memory

./scripts/gm-hook-event post_tool "tool completed" --owner test-owner --session s-123 >/tmp/gm-hook-event.out

grep -q '"ok": true' /tmp/gm-hook-event.out

grep -q '"event": "post_tool"' memory/graymatter-fallback.json
grep -q '"session": "s-123"' memory/graymatter-fallback.json

echo "gm_hook_event_test: ok"
