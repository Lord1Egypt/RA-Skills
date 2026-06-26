#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/data/release-security"
mkdir -p "$OUT"

if ! command -v cyclonedx-py >/dev/null 2>&1; then
  echo "cyclonedx-py not found, installing..."
  python3 -m pip install --user cyclonedx-bom >/dev/null
  export PATH="$HOME/.local/bin:$PATH"
fi

cyclonedx-py environment --output-format json --output-file "$OUT/sbom.cdx.json" >/dev/null
echo "sbom -> $OUT/sbom.cdx.json"
