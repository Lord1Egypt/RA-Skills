#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$ROOT}"
HITS=0

echo "[scan] target=$TARGET"

if command -v yara >/dev/null 2>&1; then
  echo "[scan] yara available (run your org rules here)"
else
  echo "[scan] yara not installed (skip)"
fi

if command -v clamscan >/dev/null 2>&1; then
  clamscan -r "$TARGET" || HITS=$((HITS+1))
else
  echo "[scan] clamscan not installed (skip)"
fi

# lightweight suspicious string scan (local heuristic)
if grep -RInE --exclude='pre_release_scan.sh' "(powershell\s+-enc|frombase64string\(|Invoke-Expression|curl\s+.*\|\s*sh|wget\s+.*\|\s*sh)" "$TARGET" >/tmp/pengbo-scan-suspicious.txt 2>/dev/null; then
  echo "[scan] suspicious patterns found:"
  cat /tmp/pengbo-scan-suspicious.txt
  HITS=$((HITS+1))
else
  echo "[scan] no suspicious shell-loader patterns"
fi

THRESHOLD="${SCAN_FAIL_THRESHOLD:-1}"
echo "[scan] hits=$HITS threshold=$THRESHOLD"
if [ "$HITS" -ge "$THRESHOLD" ]; then
  echo "[scan] FAIL"
  exit 2
fi

echo "[scan] PASS"
