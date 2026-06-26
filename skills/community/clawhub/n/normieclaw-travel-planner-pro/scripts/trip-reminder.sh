#!/bin/bash
# ============================================================================
# trip-reminder.sh — Travel Planner Pro Pre-Trip Reminder Generator
# 
# Reads upcoming trip files and generates contextual reminders based on
# days-until-departure. Output is plain text suitable for agent consumption.
#
# Usage: ./trip-reminder.sh [trip-id]
#   If trip-id is provided, generates reminders for that specific trip.
#   If omitted, scans all trips for upcoming departures.
#
# Exit codes:
#   0 — Success (reminders generated or no upcoming trips)
#   1 — Error (workspace not found, invalid trip file, etc.)
# ============================================================================

set -euo pipefail

# --- Workspace Root Detection ---
    # Skill directory detection (stay within skill boundary)
# Works whether script runs from workspace/scripts/ or from the skill package.
resolve_workspace_root() {
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Walk up from script location looking for marker files
    while [ "$dir" != "/" ]; do
    # Skill directory detection (stay within skill boundary)
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    
    # Fallback: try current working directory
    # Skill directory detection (stay within skill boundary)
        pwd
        return 0
    fi
    
    # Skill directory detection (stay within skill boundary)
    return 1
}

SKILL_DIR="$(resolve_workspace_root)"
TRAVEL_DIR="$SKILL_DIR/travel"
TRIPS_DIR="$TRAVEL_DIR/trips"
CONFIG_FILE="$SKILL_DIR/config/travel-config.json"

is_safe_trip_id() {
    local trip_id="${1:-}"
    [[ "$trip_id" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]
}

# --- Validation ---
if [ ! -d "$TRAVEL_DIR" ]; then
    echo "ERROR: Travel directory not found at $TRAVEL_DIR. Run setup first." >&2
    exit 1
fi

if [ ! -d "$TRIPS_DIR" ]; then
    echo "No trips directory found. No upcoming trips to check."
    exit 0
fi

# --- Load Config (reminder schedule) ---
# Default reminder thresholds (days before departure)
REMIND_VISA=30
REMIND_INSURANCE=21
REMIND_PACKING=7
REMIND_BANK=7
REMIND_WEATHER=3
REMIND_OFFLINE_MAPS=3
REMIND_CHECKIN=1
REMIND_FINAL=1

if [ -f "$CONFIG_FILE" ]; then
    # Extract reminder schedule from config if available
    if command -v python3 &>/dev/null; then
        config_lines="$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null || true
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    s = cfg.get("reminder_schedule", {})
    print(f"REMIND_VISA={s.get('visa_and_docs', 30)}")
    print(f"REMIND_INSURANCE={s.get('travel_insurance', 21)}")
    print(f"REMIND_PACKING={s.get('packing_review', 7)}")
    print(f"REMIND_BANK={s.get('bank_notification', 7)}")
    print(f"REMIND_WEATHER={s.get('weather_recheck', 3)}")
    print(f"REMIND_OFFLINE_MAPS={s.get('offline_maps', 3)}")
    print(f"REMIND_CHECKIN={s.get('flights_checkin', 1)}")
    print(f"REMIND_FINAL={s.get('final_reminder', 1)}")
except Exception:
    pass
PY
)"
        while IFS='=' read -r key value; do
            case "$key" in
                REMIND_VISA|REMIND_INSURANCE|REMIND_PACKING|REMIND_BANK|REMIND_WEATHER|REMIND_OFFLINE_MAPS|REMIND_CHECKIN|REMIND_FINAL)
                    if [[ "$value" =~ ^[0-9]+$ ]]; then
                        printf -v "$key" '%s' "$value"
                    fi
                    ;;
            esac
        done <<< "${config_lines:-}"
    fi
fi

# --- Date Math ---
today_epoch() {
    if date --version &>/dev/null 2>&1; then
        # GNU date (Linux)
        date -d "today" +%s
    else
        # BSD date (macOS)
        date +%s
    fi
}

date_to_epoch() {
    local d="$1"
    if date --version &>/dev/null 2>&1; then
        date -d "$d" +%s 2>/dev/null || echo "0"
    else
        date -j -f "%Y-%m-%d" "$d" +%s 2>/dev/null || echo "0"
    fi
}

days_until() {
    local target_epoch="$1"
    local today="$(today_epoch)"
    local diff=$(( (target_epoch - today) / 86400 ))
    echo "$diff"
}

# --- Generate Reminders for a Single Trip ---
generate_reminders() {
    local trip_file="$1"
    
    if [ ! -f "$trip_file" ]; then
        echo "WARNING: Trip file not found: $trip_file" >&2
        return 0
    fi

    # Extract trip details using Python for reliable JSON parsing
    local trip_info
    trip_info="$(python3 - "$trip_file" <<'PY' 2>/dev/null || true
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as f:
        trip = json.load(f)
    print(trip.get("trip_id", "unknown"))
    print(trip.get("destination", "Unknown"))
    print(trip.get("start_date", ""))
    print(trip.get("status", "unknown"))
except Exception:
    pass
PY
)"
    [ -n "$trip_info" ] || return 0

    local trip_id dest start_date status
    trip_id="$(echo "$trip_info" | sed -n '1p')"
    dest="$(echo "$trip_info" | sed -n '2p')"
    start_date="$(echo "$trip_info" | sed -n '3p')"
    status="$(echo "$trip_info" | sed -n '4p')"

    # Skip completed or cancelled trips
    if [ "$status" = "completed" ] || [ "$status" = "cancelled" ]; then
        return 0
    fi

    # Skip if no start date
    if [ -z "$start_date" ]; then
        return 0
    fi

    local dep_epoch
    dep_epoch="$(date_to_epoch "$start_date")"
    if [ "$dep_epoch" = "0" ]; then
        echo "WARNING: Could not parse start_date '$start_date' for trip $trip_id" >&2
        return 0
    fi

    local days_left
    days_left="$(days_until "$dep_epoch")"

    # Skip past trips
    if [ "$days_left" -lt 0 ]; then
        return 0
    fi

    echo "========================================"
    echo "🧳 TRIP: $dest ($trip_id)"
    echo "📅 Departure: $start_date ($days_left days away)"
    echo "========================================"
    echo ""

    local has_reminders=false

    if [ "$days_left" -le "$REMIND_VISA" ] && [ "$days_left" -gt "$REMIND_INSURANCE" ]; then
        has_reminders=true
        echo "📋 DOCUMENTS & VISA ($REMIND_VISA-day reminder)"
        echo "  - Check passport validity (6+ months required for most countries)"
        echo "  - Research visa requirements for $dest"
        echo "  - Start visa application if needed (processing can take 2-4 weeks)"
        echo ""
    fi

    if [ "$days_left" -le "$REMIND_INSURANCE" ] && [ "$days_left" -gt "$REMIND_PACKING" ]; then
        has_reminders=true
        echo "🛡️ TRAVEL INSURANCE ($REMIND_INSURANCE-day reminder)"
        echo "  - Purchase travel insurance if not yet covered"
        echo "  - Check if credit card provides trip protection"
        echo "  - Verify coverage for planned activities"
        echo ""
    fi

    if [ "$days_left" -le "$REMIND_PACKING" ] && [ "$days_left" -gt "$REMIND_WEATHER" ]; then
        has_reminders=true
        echo "👕 PACKING REVIEW ($REMIND_PACKING-day reminder)"
        echo "  - Review your packing list"
        echo "  - Order any missing items (adapters, toiletries, etc.)"
        echo "  - Check luggage weight limits for your airline"
        echo ""
        echo "🏦 BANK NOTIFICATION ($REMIND_BANK-day reminder)"
        echo "  - Notify your bank/credit card about travel dates & destination"
        echo "  - Check foreign transaction fees"
        echo "  - Consider ordering local currency if needed"
        echo ""
    fi

    if [ "$days_left" -le "$REMIND_WEATHER" ] && [ "$days_left" -gt "$REMIND_FINAL" ]; then
        has_reminders=true
        echo "🌤️ WEATHER CHECK ($REMIND_WEATHER-day reminder)"
        echo "  - Check updated forecast for $dest"
        echo "  - Adjust packing list if weather changed"
        echo "  - Swap outdoor/indoor activities if needed"
        echo ""
        echo "📱 DIGITAL PREP ($REMIND_OFFLINE_MAPS-day reminder)"
        echo "  - Download offline maps for $dest"
        echo "  - Set up eSIM or pocket WiFi reservation"
        echo "  - Download translation app if needed"
        echo "  - Save important confirmations offline"
        echo ""
    fi

    if [ "$days_left" -le "$REMIND_FINAL" ]; then
        has_reminders=true
        echo "✈️ FINAL CHECK ($REMIND_FINAL-day reminder)"
        echo "  - Check in for your flight online"
        echo "  - Confirm hotel/accommodation reservation"
        echo "  - Passport, tickets, charger, adapter — in your bag?"
        echo "  - Set out-of-office if needed"
        echo "  - Have an amazing trip to $dest! 🎉"
        echo ""
    fi

    if [ "$has_reminders" = false ]; then
        echo "  ✅ No action needed yet. Next reminder at $REMIND_VISA days before departure."
        echo ""
    fi
}

# --- Main ---
SPECIFIC_TRIP="${1:-}"

if [ -n "$SPECIFIC_TRIP" ]; then
    if ! is_safe_trip_id "$SPECIFIC_TRIP"; then
        echo "ERROR: Invalid trip ID. Use only letters, numbers, dot, underscore, and dash." >&2
        exit 1
    fi

    # Check specific trip
    trip_file="$TRIPS_DIR/${SPECIFIC_TRIP}.json"
    if [ -L "$trip_file" ]; then
        echo "ERROR: Refusing to read symlinked trip file: $trip_file" >&2
        exit 1
    fi
    if [ ! -f "$trip_file" ]; then
        echo "ERROR: Trip file not found: $trip_file" >&2
        echo "Available trips:" >&2
        found_any=false
        for candidate in "$TRIPS_DIR"/*.json; do
            [ -f "$candidate" ] || continue
            [ -L "$candidate" ] && continue
            found_any=true
            basename "$candidate" .json >&2
        done
        [ "$found_any" = false ] && echo "  (none)" >&2
        exit 1
    fi
    generate_reminders "$trip_file"
else
    # Scan all trips
    found_trips=false
    for trip_file in "$TRIPS_DIR"/*.json; do
        [ -f "$trip_file" ] || continue
        [ -L "$trip_file" ] && continue
        # Skip budget and packing files
        case "$(basename "$trip_file")" in
            *-budget.json|*-packing.json) continue ;;
        esac
        found_trips=true
        generate_reminders "$trip_file"
    done

    if [ "$found_trips" = false ]; then
        echo "No upcoming trips found. Plan one with: 'Plan a trip to [destination]'"
    fi
fi
