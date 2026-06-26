#!/bin/bash
set -euo pipefail

# Search forecast locations by postal code, name, or abbreviation
# Usage: search-forecast-points.sh <query>
# Requires: curl, jq, iconv, awk
# Example: search-forecast-points.sh 8001

QUERY="${1:-}"

if [[ -z "$QUERY" || "$1" == "--help" || "$1" == "-h" ]]; then
  echo "Usage: $(basename "$0") <query>"
  echo ""
  echo "Search ~6000 Swiss forecast locations (stations, postal codes, mountains)."
  echo "Data source: MeteoSwiss Open Data (forecast point metadata)"
  echo ""
  echo "Arguments:"
  echo "  query  Postal code, place name, or station abbreviation"
  echo ""
  echo "Output: point_id | type | postal_code | abbr | name | elevation"
  echo "  type: 1=station, 2=postal_code, 3=mountain"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") 8001       # Zurich postal code"
  echo "  $(basename "$0") Bern       # place name"
  echo "  $(basename "$0") SMA        # station abbreviation"
  exit "${QUERY:+1}"
fi

QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')
STAC_URL="https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-local-forecasting"

# Get metadata CSV URL from STAC (handles the known "forcasting" typo)
META_URL=$(curl -sf "$STAC_URL" \
  | jq -r '[.assets | to_entries[] | select(.key | contains("meta_point")) | .value.href] | first') \
  || { echo "Error: failed to fetch STAC collection" >&2; exit 1; }

curl -sf "$META_URL" \
  | iconv -f latin1 -t utf-8 \
  | awk -F';' -v q="$QUERY_LOWER" '
    NR == 1 { next }
    {
      line = tolower($0)
      if (line ~ q) {
        printf "%s | type=%s | zip=%s | abbr=%s | %s | %sm\n", $1, $2, $4, $3, $5, $10
      }
    }' || { echo "Error: failed to fetch forecast point metadata" >&2; exit 1; }
