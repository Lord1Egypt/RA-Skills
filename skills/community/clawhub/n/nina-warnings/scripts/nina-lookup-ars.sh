#!/bin/bash
# Lookup ARS code candidates for a place or district name.
# Usage: nina-lookup-ars.sh <city-or-district-name> [--ars-only] [--first]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARS_CACHE="$SCRIPT_DIR/../references/ars-codes.json"

QUERY=""
ARS_ONLY=false
FIRST_ONLY=false
PLAIN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ars-only)
            ARS_ONLY=true
            shift
            ;;
        --first)
            FIRST_ONLY=true
            shift
            ;;
        --plain)
            PLAIN=true
            shift
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            if [[ -z "$QUERY" ]]; then
                QUERY="$1"
            else
                QUERY="$QUERY $1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$QUERY" ]]; then
    echo "Usage: $0 <city-or-district-name> [--ars-only] [--first] [--plain]" >&2
    echo "  Example: $0 Berlin" >&2
    echo "  Example: $0 Hamburg" >&2
    echo "  --ars-only: Print only matching ARS code(s)" >&2
    echo "  --first: Return only the first match" >&2
    echo "  --plain: Print raw 'name|ars|state' rows for scripting" >&2
    exit 1
fi

# Query local ARS cache (flat array format)
QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')

result=$(jq -r --arg q "$QUERY_LOWER" '
    .[] | 
    select((.name | ascii_downcase) | contains($q)) |
    "\(.name) | \(.ars) | \(.state // .bundesland // "")"
' "$ARS_CACHE" 2>/dev/null)

if [[ -z "$result" ]]; then
    echo "❌ Kein ARS-Code gefunden für: $QUERY"
    echo ""
    echo "Tipp: Nutze den ARS-Code direkt (z.B. 110000000000 fuer Berlin)"
    echo ""
    echo "Häufige ARS-Codes:"
    jq -r '.[] | "  \(.name): \(.ars)"' "$ARS_CACHE" | head -10
    exit 1
fi

if [[ "$FIRST_ONLY" == "true" ]]; then
    result=$(echo "$result" | head -1)
else
    result=$(echo "$result" | head -5)
fi

if [[ "$ARS_ONLY" == "true" ]]; then
    echo "$result" | while IFS='|' read -r _ ars _; do
        echo "$ars" | xargs
    done
    exit 0
fi

if [[ "$PLAIN" == "true" ]]; then
    echo "$result" | sed 's/ | /|/g'
    exit 0
fi

echo "📍 ARS-Codes für '$QUERY':"
echo ""
echo "$result" | while IFS='|' read -r name ars bundesland; do
    name=$(echo "$name" | xargs)
    ars=$(echo "$ars" | xargs)
    bundesland=$(echo "$bundesland" | xargs)
    echo "  $name"
    echo "    ARS: $ars"
    echo "    Bundesland: $bundesland"
    echo ""
done
