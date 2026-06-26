#!/bin/bash
set -euo pipefail

# Get current pollen data for a Swiss monitoring station
# Usage: pollen.sh <station_abbr>
# Requires: curl, iconv, awk
# Example: pollen.sh ZUE

STATION="${1:-}"

if [[ -z "$STATION" || "$1" == "--help" || "$1" == "-h" ]]; then
  echo "Usage: $(basename "$0") <station_abbr>"
  echo ""
  echo "Get latest pollen concentration data for a Swiss monitoring station."
  echo "Data source: MeteoSwiss Open Data (ogd-pollen collection)"
  echo ""
  echo "Stations: BAS BER BUC DAV GEN LAU LOG LUG LUZ MUN NEU VIS ZUE"
  echo ""
  echo "Output: pollen_type=concentration (particles/m³)"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") ZUE    # Zurich"
  echo "  $(basename "$0") BER    # Bern"
  echo "  $(basename "$0") GEN    # Geneva"
  exit "${STATION:+1}"
fi

ABBR=$(echo "$STATION" | tr '[:upper:]' '[:lower:]')
URL="https://data.geo.admin.ch/ch.meteoschweiz.ogd-pollen/${ABBR}/ogd-pollen_${ABBR}_d_now.csv"

DATA=$(curl -sf "$URL" | iconv -f latin1 -t utf-8) || {
  echo "Error: failed to fetch pollen data for '$STATION'" >&2
  echo "Hint: valid stations are BAS BER BUC DAV GEN LAU LOG LUG LUZ MUN NEU VIS ZUE" >&2
  exit 1
}

# Output header fields paired with latest row values
HEADER=$(echo "$DATA" | head -1)
LAST_ROW=$(echo "$DATA" | tail -1)

echo "$HEADER" | awk -F';' -v row="$LAST_ROW" '
BEGIN { split(row, vals, ";") }
{
  for (i = 1; i <= NF; i++) {
    gsub(/^[ \t]+|[ \t]+$/, "", $i)
    gsub(/^[ \t]+|[ \t]+$/, "", vals[i])
    if ($i == "station_abbr" || $i == "reference_timestamp" || $i == "Date") {
      print $i "=" vals[i]
    } else if (vals[i] != "" && vals[i] != "-") {
      print $i "=" vals[i]
    }
  }
}'
