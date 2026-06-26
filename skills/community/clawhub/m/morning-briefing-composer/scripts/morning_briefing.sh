#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_PATH="${HOME}/.openclaw/config/morning-briefing.json"
OUTPUT_PATH="${SKILL_DIR}/data/briefing.md"

if [[ ! -f "$CONFIG_PATH" ]]; then
    echo "Config not found at $CONFIG_PATH" >&2
    echo "Run init_config.sh first." >&2
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"

config=$(cat "$CONFIG_PATH")
tz=$(echo "$config" | jq -r '.timezone // "UTC"')
today=$(TZ="$tz" date +%Y-%m-%d)

# --- Build briefing into output file ---
{

# --- Header ---
echo "# Morning Briefing"
echo "$(TZ="$tz" date '+%A, %B %d, %Y')"
echo ""

# --- Weather ---
weather_enabled=$(echo "$config" | jq -r '.weather.enabled // false')
if [[ "$weather_enabled" == "true" ]]; then
    location=$(echo "$config" | jq -r '.weather.location // "Valencia"')
    echo "## Weather"
    echo ""
    weather_data=$(curl -s --max-time 10 "wttr.in/${location}?format=%l:+%c+%t+(feels+like+%f),+%w+wind,+%h+humidity" 2>/dev/null) || weather_data="Weather unavailable"
    echo "$weather_data"
    echo ""
fi

# --- Sources ---
echo "$config" | jq -r '.sources | keys[]' | while read -r source_id; do
    enabled=$(echo "$config" | jq -r ".sources[\"$source_id\"].enabled // true")
    [[ "$enabled" == "false" ]] && continue

    data_path=$(echo "$config" | jq -r ".sources[\"$source_id\"].data_path")
    data_path="${data_path/#\~/$HOME}"
    # Resolve relative paths from skill directory
    [[ "$data_path" != /* ]] && data_path="${SKILL_DIR}/${data_path}"

    [[ ! -f "$data_path" ]] && continue

    template="${SKILL_DIR}/assets/templates/${source_id}.jq"
    [[ ! -f "$template" ]] && continue

    preferences=$(echo "$config" | jq -c ".sources[\"$source_id\"].preferences // {}")

    # Compute cutoff date if days_ahead is set in preferences
    days_ahead=$(echo "$preferences" | jq -r '.days_ahead // 0')
    cutoff=""
    if [[ "$days_ahead" -gt 0 ]] 2>/dev/null; then
        if date -d "1 day" +%Y-%m-%d &>/dev/null; then
            cutoff=$(TZ="$tz" date -d "+${days_ahead} days" +%Y-%m-%d)
        else
            cutoff=$(TZ="$tz" date -v "+${days_ahead}d" +%Y-%m-%d)
        fi
    fi

    section=$(jq -r \
        --argjson preferences "$preferences" \
        --arg today "$today" \
        --arg cutoff "$cutoff" \
        -f "$template" "$data_path" 2>/dev/null) || continue

    if [[ -n "$section" && "$section" != "null" ]]; then
        echo "$section"
        echo ""
    fi
done

# --- Footer ---
echo "---"
echo "*Generated at $(TZ="$tz" date '+%H:%M %Z')*"

} > "$OUTPUT_PATH"

echo "IMPORTANT: Read $OUTPUT_PATH and present its contents to the user EXACTLY as written. Do not summarize, reformat, paraphrase, or editorialize. Output the markdown verbatim."
