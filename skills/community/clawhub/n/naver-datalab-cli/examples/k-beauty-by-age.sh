#!/usr/bin/env bash
# k-beauty-by-age.sh — 화장품/미용 (50000002) by age cohort, monthly H1 2024.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$here/../scripts/shop-age.sh" \
  --start 2024-01-01 --end 2024-06-30 --time-unit month \
  --category 50000002
