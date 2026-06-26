#!/bin/bash
set -euo pipefail

# Get weather forecast for a Swiss location by point_id
# Usage: forecast.sh <point_id> [point_type_id]
# Requires: curl, jq, awk
# Example: forecast.sh 48 1

POINT_ID="${1:-}"
POINT_TYPE="${2:-1}"

if [[ -z "$POINT_ID" || "$1" == "--help" || "$1" == "-h" ]]; then
  echo "Usage: $(basename "$0") <point_id> [point_type_id]"
  echo ""
  echo "Get weather forecast for a Swiss location."
  echo "Data source: MeteoSwiss Open Data (STAC local-forecasting collection)"
  echo ""
  echo "Arguments:"
  echo "  point_id       Forecast point ID (use search-forecast-points.sh to find)"
  echo "  point_type_id  1=station (default), 2=postal_code, 3=mountain"
  echo ""
  echo "Common point_ids (stations): Zurich=48, Bern=29, Geneva=53"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") 48       # Zurich station"
  echo "  $(basename "$0") 48 1     # explicit station type"
  exit "${POINT_ID:+1}"
fi

STAC_BASE="https://data.geo.admin.ch/api/stac/v1"
COLLECTION="ch.meteoschweiz.ogd-local-forecasting"

# Step 1: Get latest forecast item
ITEM=$(curl -sf "$STAC_BASE/collections/$COLLECTION/items?limit=10" \
  | jq -r '[.features[].id] | sort | reverse | .[0]') || { echo "Error: failed to fetch STAC items" >&2; exit 1; }

ITEM_URL="$STAC_BASE/collections/$COLLECTION/items/$ITEM"
ITEM_JSON=$(curl -sf "$ITEM_URL") || { echo "Error: failed to fetch item $ITEM" >&2; exit 1; }

# Step 2: Choose parameters based on point type
if [[ "$POINT_TYPE" == "1" ]]; then
  PARAMS="tre200dx tre200dn rka150d0 jp2000d0"
else
  PARAMS="tre200h0 rre150h0 jww003i0"
fi

echo "forecast_item=$ITEM"
echo "point_id=$POINT_ID"
echo "point_type_id=$POINT_TYPE"
echo "---"

# Step 3: Download each parameter CSV and extract values
for PARAM in $PARAMS; do
  ASSET_URL=$(echo "$ITEM_JSON" \
    | jq -r "[.assets | to_entries[] | select(.key | contains(\"$PARAM\"))] | sort_by(.key) | last | .value.href // empty")

  if [[ -z "$ASSET_URL" ]]; then
    echo "$PARAM=no_data"
    continue
  fi

  curl -sf "$ASSET_URL" \
    | awk -F';' -v pid="$POINT_ID" -v ptid="$POINT_TYPE" -v param="$PARAM" '
      NR == 1 { next }
      $1 == pid && $2 == ptid {
        printf "%s %s=%s\n", param, $3, $4
      }'
done
