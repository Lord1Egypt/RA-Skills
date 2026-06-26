#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "[1/3] Running unit tests..."
npm test

echo "[2/3] Running text brief smoke test..."
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format text >/tmp/mindkeeper-smoke.txt
grep -q "What mattered" /tmp/mindkeeper-smoke.txt
grep -q "Recommendations" /tmp/mindkeeper-smoke.txt

echo "[3/4] Running html export smoke test..."
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format html --out ./tmp/mindkeeper-preview.html >/tmp/mindkeeper-html-smoke.txt
grep -q "Wrote output to" /tmp/mindkeeper-html-smoke.txt
grep -q "Firma de AI" ./tmp/mindkeeper-preview.html

echo "[4/4] Running email file smoke test..."
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --prompt "Focus on lossless-claw and openclaw-mindkeeper naming" --email-to alex@example.com --email-from mindkeeper@example.com --email-out ./tmp/mindkeeper.eml >/tmp/mindkeeper-email-smoke.txt
grep -q "Email delivery" /tmp/mindkeeper-email-smoke.txt
grep -q "Subject: Mindkeeper Daily Brief" ./tmp/mindkeeper.eml

echo "✅ Mindkeeper validation passed"
