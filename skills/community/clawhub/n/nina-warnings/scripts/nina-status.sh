#!/bin/bash
# Fetch current NINA warnings for an ARS code, location, or source feed.
# Usage: nina-status.sh <ARS-code-or-location> [options]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_BASE="https://warnung.bund.de/api31"
EVENT_CODES_URL="$API_BASE/appdata/gsb/eventCodes/eventCodes.json"
LOOKUP_SCRIPT="$SCRIPT_DIR/nina-lookup-ars.sh"

INPUT=""
JSON_OUTPUT=false
DETAILS=false
GEOJSON=false
SOURCE=""
ARS=""
REGION_LABEL=""
NORMALIZED_ARS=""

usage() {
    echo "Usage: $0 <ARS-code-or-location> [options]" >&2
    echo "Usage: $0 --source <mowas|dwd|katwarn|biwapp|lhp|police> [options]" >&2
    echo "" >&2
    echo "  ARS-code: Amtlicher Regionalschluessel (z.B. 110000000000 fuer Berlin)" >&2
    echo "  location: city or district name from the local cache (z.B. Berlin)" >&2
    echo "  --json: Output raw JSON for the selected feed or enriched warnings" >&2
    echo "  --details: Fetch full warning details via /warnings/{identifier}.json" >&2
    echo "  --geojson: Fetch /warnings/{identifier}.geojson for each warning" >&2
    echo "  --source: Use a nationwide source feed instead of the regional dashboard" >&2
    exit 1
}

for bin in curl jq; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "Error: required command not found: $bin" >&2
        exit 1
    fi
done

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --details)
            DETAILS=true
            shift
            ;;
        --geojson)
            GEOJSON=true
            shift
            ;;
        --source)
            if [[ $# -lt 2 ]]; then
                echo "Error: --source requires a value" >&2
                usage
            fi
            SOURCE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            else
                echo "Error: unexpected extra argument: $1" >&2
                usage
            fi
            shift
            ;;
    esac
done

normalize_ars() {
    local raw="$1"
    if [[ ! "$raw" =~ ^[0-9]{12}$ ]]; then
        echo "$raw"
        return
    fi
    echo "${raw:0:5}0000000"
}

fetch_json() {
    local url="$1"
    curl --fail --silent --show-error --location --max-time 20 "$url"
}

event_label() {
    local code="$1"
    if [[ -z "$code" ]]; then
        echo "Unbekannter Typ"
        return
    fi
    echo "$EVENT_CODES_JSON" | jq -r --arg code "$code" '
        [
            (.[]? | objects | select(.value == $code) | .label.de),
            (.eventCodes[]? | objects | select(.eventCode == $code) | .eventCode)
        ]
        | map(select(. != null and . != ""))
        | .[0] // empty
    ' 2>/dev/null
}

warning_identifier() {
    jq -r '.id // .identifier // .payload.id // empty'
}

warning_headline() {
    jq -r '.payload.data.headline // .headline // .info[0].headline // .payload.data.i18nTitle.de // .i18nTitle.de // "Keine Überschrift"'
}

warning_provider() {
    jq -r '
        .payload.data.provider
        // .provider
        // .sender
        // first(.info[0].parameter[]? | select(.valueName == "sender_langname") | .value)
        // "Unknown"
    ' 2>/dev/null
}

warning_severity() {
    jq -r '.payload.data.severity // .severity // .info[0].severity // "Unknown"'
}

warning_urgency() {
    jq -r '.payload.data.urgency // .urgency // .info[0].urgency // "Unknown"'
}

warning_effective() {
    jq -r '.sent // .payload.data.sent // .effective // .startDate // "Unknown"'
}

warning_expires() {
    jq -r '.payload.data.expires // .expires // empty'
}

warning_event_code() {
    jq -r '.payload.data.transKeys.event // .transKeys.event // .info[0].eventCode[0].value // empty'
}

warning_description() {
    jq -r '.info[0].description // .description // empty'
}

warning_instruction() {
    jq -r '.info[0].instruction // .instruction // empty'
}

warning_area_desc() {
    jq -r '.info[0].area[0].areaDesc // .payload.data.area.data // empty'
}

warning_msg_type() {
    jq -r '.payload.data.msgType // .msgType // empty'
}

format_multiline_text() {
    sed 's/<br\/>/\
/g; s/<br>/\
/g; s/<[^>]*>//g' | awk '{print "   " $0}'
}

detail_link_for_warning() {
    local warning_json="$1"
    local warning_id headline_slug headline
    warning_id=$(echo "$warning_json" | warning_identifier)
    headline=$(echo "$warning_json" | warning_headline)
    if [[ -z "$warning_id" ]]; then
        echo ""
        return
    fi
    headline_slug=$(echo "$headline" | sed 's/  */_/g' | sed 's/[^a-zA-Z0-9_-]//g')
    echo "https://warnung.bund.de/meldungen/${warning_id}/${headline_slug}"
}

validate_source() {
    case "$1" in
        mowas|dwd|katwarn|biwapp|lhp|police)
            return 0
            ;;
        *)
            echo "Error: unsupported source '$1'" >&2
            echo "Supported values: mowas, dwd, katwarn, biwapp, lhp, police" >&2
            exit 1
            ;;
    esac
}

resolve_input() {
    if [[ -n "$SOURCE" ]]; then
        validate_source "$SOURCE"
        REGION_LABEL="Quelle $SOURCE (bundesweit)"
        return
    fi

    if [[ -z "$INPUT" ]]; then
        usage
    fi

    if [[ "$INPUT" =~ ^[0-9]{12}$ ]]; then
        ARS="$INPUT"
        REGION_LABEL="ARS $ARS"
    else
        lookup_line=$("$LOOKUP_SCRIPT" "$INPUT" --plain --first | head -1 || true)
        if [[ -z "$lookup_line" ]]; then
            echo "Error: could not resolve location to ARS: $INPUT" >&2
            exit 1
        fi
        REGION_LABEL=$(echo "$lookup_line" | cut -d'|' -f1 | xargs)
        ARS=$(echo "$lookup_line" | cut -d'|' -f2 | xargs)
    fi

    NORMALIZED_ARS=$(normalize_ars "$ARS")
}

fetch_feed() {
    if [[ -n "$SOURCE" ]]; then
        fetch_json "$API_BASE/$SOURCE/mapData.json"
    else
        fetch_json "$API_BASE/dashboard/$NORMALIZED_ARS.json"
    fi
}

enrich_warning_json() {
    local warning_json="$1"
    local warning_id detail_json geojson_json

    warning_id=$(echo "$warning_json" | warning_identifier)
    detail_json='null'
    geojson_json='null'

    if [[ "$DETAILS" == "true" && -n "$warning_id" ]]; then
        detail_json=$(fetch_json "$API_BASE/warnings/$warning_id.json" 2>/dev/null || echo 'null')
    fi

    if [[ "$GEOJSON" == "true" && -n "$warning_id" ]]; then
        geojson_json=$(fetch_json "$API_BASE/warnings/$warning_id.geojson" 2>/dev/null || echo 'null')
    fi

    jq -cn \
        --argjson summary "$warning_json" \
        --argjson detail "$detail_json" \
        --argjson geojson "$geojson_json" \
        '{summary: $summary, detail: $detail, geojson: $geojson}'
}

render_warning_text() {
    local warning_json="$1"
    local display_json detail_json
    local warning_id headline severity urgency effective expires provider event_code event_desc detail_link description instruction area_desc msg_type

    display_json="$warning_json"
    detail_json=$(echo "$warning_json" | jq -c '.detail // null')
    if [[ "$detail_json" != "null" ]]; then
        display_json="$detail_json"
    else
        display_json=$(echo "$warning_json" | jq -c '.summary // .')
    fi

    warning_id=$(echo "$display_json" | warning_identifier)
    headline=$(echo "$display_json" | warning_headline)
    severity=$(echo "$display_json" | warning_severity)
    urgency=$(echo "$display_json" | warning_urgency)
    effective=$(echo "$display_json" | warning_effective)
    expires=$(echo "$display_json" | warning_expires)
    provider=$(echo "$display_json" | warning_provider)
    event_code=$(echo "$display_json" | warning_event_code)
    event_desc=$(event_label "$event_code")
    if [[ -z "$event_desc" ]]; then
        event_desc="${event_code:-Unbekannter Typ}"
    fi
    detail_link=$(detail_link_for_warning "$display_json")
    description=$(echo "$display_json" | warning_description)
    instruction=$(echo "$display_json" | warning_instruction)
    area_desc=$(echo "$display_json" | warning_area_desc)
    msg_type=$(echo "$display_json" | warning_msg_type)

    echo "────────────────────────────────────────"
    echo "📋 $headline"
    echo "   Typ: $event_desc"
    if [[ -n "$event_code" && "$event_desc" != "$event_code" ]]; then
        echo "   Code: $event_code"
    fi
    echo "   Schwere: $severity | Dringlichkeit: $urgency"
    echo "   Anbieter: $provider"
    if [[ -n "$msg_type" ]]; then
        echo "   Meldungsart: $msg_type"
    fi
    echo "   Gesendet: $effective"
    if [[ -n "$expires" && "$expires" != "null" && "$expires" != "Unknown" ]]; then
        echo "   Gueltig bis: $expires"
    fi
    if [[ -n "$area_desc" ]]; then
        echo "   Gebiet: $area_desc"
    fi
    if [[ -n "$warning_id" ]]; then
        echo "   ID: $warning_id"
    fi
    if [[ -n "$detail_link" ]]; then
        echo "   🔗 Details: $detail_link"
    fi
    if [[ "$DETAILS" == "true" && -n "$description" ]]; then
        echo ""
        echo "   Beschreibung:"
        echo "$description" | format_multiline_text
    fi
    if [[ "$DETAILS" == "true" && -n "$instruction" ]]; then
        echo ""
        echo "   Handlungshinweise:"
        echo "$instruction" | format_multiline_text
    fi
    if [[ "$GEOJSON" == "true" ]]; then
        local feature_count
        feature_count=$(echo "$warning_json" | jq -r '
            if .geojson == null then 0
            elif .geojson.type == "FeatureCollection" then (.geojson.features | length)
            else 1
            end
        ')
        echo ""
        echo "   GeoJSON: $feature_count Feature(s) geladen"
    fi
    echo ""
}

resolve_input
EVENT_CODES_JSON=$(fetch_json "$EVENT_CODES_URL" 2>/dev/null || echo '[]')
warnings=$(fetch_feed)
count=$(echo "$warnings" | jq 'length')

if [[ "$JSON_OUTPUT" == "true" ]]; then
    if [[ "$DETAILS" == "true" || "$GEOJSON" == "true" ]]; then
        echo "$warnings" | jq -c '.[]' | while IFS= read -r warning_line; do
            enrich_warning_json "$warning_line"
        done | jq -s \
            --arg label "$REGION_LABEL" \
            --arg ars "$ARS" \
            --arg normalized_ars "$NORMALIZED_ARS" \
            --arg source "$SOURCE" \
            '{
                region: $label,
                ars: (if $ars == "" then null else $ars end),
                normalized_ars: (if $normalized_ars == "" then null else $normalized_ars end),
                source: (if $source == "" then null else $source end),
                count: length,
                warnings: .
            }'
    else
        echo "$warnings"
    fi
    exit 0
fi

if [[ "$count" -eq 0 ]]; then
    echo "✅ Keine aktuellen Warnungen fuer $REGION_LABEL"
    if [[ -n "$NORMALIZED_ARS" && "$ARS" != "$NORMALIZED_ARS" ]]; then
        echo "   Hinweis: NINA-Dashboard auf Kreisebene verwendet ARS $NORMALIZED_ARS"
    fi
    exit 0
fi

echo "⚠️  $count Warnung(en) fuer $REGION_LABEL:"
if [[ -n "$NORMALIZED_ARS" && "$ARS" != "$NORMALIZED_ARS" ]]; then
    echo "   Hinweis: Kreisebenen-ARS fuer Dashboard: $NORMALIZED_ARS"
fi
echo ""

while IFS= read -r warning_line; do
    if [[ "$DETAILS" == "true" || "$GEOJSON" == "true" ]]; then
        render_warning_text "$(enrich_warning_json "$warning_line")"
    else
        render_warning_text "$warning_line"
    fi
done < <(echo "$warnings" | jq -c '.[]')
