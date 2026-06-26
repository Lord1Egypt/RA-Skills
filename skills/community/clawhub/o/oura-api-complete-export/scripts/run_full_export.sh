#!/usr/bin/env bash
set -euo pipefail

START="${1:-2020-01-01}"
END="${2:-$(date +%F)}"
OUT="${3:-./oura_export}"

python3 "$(dirname "$0")/export_oura_data.py" --start "$START" --end "$END" --out "$OUT"
