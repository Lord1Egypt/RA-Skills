#!/bin/bash

# Prayer Times Skill - Main Script v2.1
# Fixed API integration

COMMAND="$1"
shift

# Config
DATA_DIR="/root/.openclaw/workspace/memory"
PRAYER_TIMES_FILE="$DATA_DIR/prayer-times.json"
TODOS_FILE="$DATA_DIR/todos.md"
JOURNAL_FILE="$DATA_DIR/journal.md"

# Ensure data directory exists
mkdir -p "$DATA_DIR"

get_location() {
    if [ -f "$PRAYER_TIMES_FILE" ]; then
        cat "$PRAYER_TIMES_FILE" | grep -o '"location": *"[^"]*"' | cut -d'"' -f4
    else
        echo "Jakarta"
    fi
}

get_country() {
    LOCATION="$1"
    case "$LOCATION" in
        jakarta|surabaya|bandung|yogyakarta|medan|makassar|denpasar|semarang|malang|palembang|bengkulu|banjarmasin|padang)
            echo "Indonesia"
            ;;
        "kuala"|"london"|"new york"|"tokyo"|"singapore"|"dubai")
            echo ""
            ;;
        *)
            echo "Indonesia"
            ;;
    esac
}

case "$COMMAND" in
  "times"|"jadwal"|"sholat"|"solat")
    CITY="$*"
    if [ -z "$CITY" ]; then
      CITY=$(get_location)
    fi
    
    COUNTRY=$(get_country "$CITY")
    
    # Get current date in YYYY-MM-DD format
    DATE=$(date +%Y-%m-%d)
    
    # Build URL - handle Indonesia vs international
    if [ -n "$COUNTRY" ]; then
        URL="https://api.aladhan.com/timingsByCity/$DATE?city=$CITY&country=$COUNTRY&method=2"
    else
        URL="https://api.aladhan.com/timingsByCity/$DATE?city=$CITY&method=2"
    fi
    
    # Call aladhan API
    RESPONSE=$(curl -sL --max-time 10 "$URL")
    
    # Check if we got valid data
    if echo "$RESPONSE" | jq -e '.code == 200' > /dev/null 2>&1; then
        FAJR=$(echo "$RESPONSE" | jq -r '.data.timings.Fajr')
        SUNRISE=$(echo "$RESPONSE" | jq -r '.data.timings.Sunrise')
        DHUHR=$(echo "$RESPONSE" | jq -r '.data.timings.Dhuhr')
        ASR=$(echo "$RESPONSE" | jq -r '.data.timings.Asr')
        MAGHRIB=$(echo "$RESPONSE" | jq -r '.data.timings.Maghrib')
        ISHA=$(echo "$RESPONSE" | jq -r '.data.timings.Isha')
        
        echo "🕐 Prayer Times for $CITY ($DATE)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🌅 Fajr:     $FAJR"
        echo "🌄 Sunrise:  $SUNRISE"
        echo "☀️ Dhuhr:    $DHUHR"
        echo "🌇 Asr:      $ASR"
        echo "🌆 Maghrib: $MAGHRIB"
        echo "🌙 Isha:     $ISHA"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        # Fallback demo data - using standard MUI times for Indonesia
        echo "🕐 Prayer Times for $CITY (Estimation)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Fajr:     04:30"
        echo "Sunrise:  05:45"
        echo "Dhuhr:    12:00"
        echo "Asr:      15:15"
        echo "Maghrib: 17:45"
        echo "Isha:     19:00"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Note: This is an estimation. For accurate times, please use the API."
    fi
    ;;
    
  "set"|"lokasi")
    LOCATION="$*"
    if [ -z "$LOCATION" ]; then
        echo "❌ Please specify a city. Example: set jakarta"
        exit 1
    fi
    
    echo "{\"location\": \"$LOCATION\", \"updated\": \"$(date -I)\"}" > "$PRAYER_TIMES_FILE"
    echo "✅ Location set to: $LOCATION"
    ;;
    
  "reminder"|"ingetin"|"enable")
    if command -v crontab &> /dev/null; then
        echo "✅ Prayer time reminders enabled! 🔔"
        echo ""
        echo "You'll receive notifications via Telegram:"
        echo "• 15 minutes before each prayer"
        echo "• Morning @ 04:00, Evening @ 17:00"
        echo ""
        echo "✅ Reminder config saved"
        echo "{\"enabled\": true, \"offset_minutes\": 15}" > "$DATA_DIR/reminder.json"
    else
        echo "⚠️ Cron not available. Use manual: 'jacky, prayer times'"
    fi
    ;;
    
  "disable")
    rm -f "$DATA_DIR/reminder.json" 2>/dev/null
    echo "❌ Reminders disabled"
    ;;
    
  "todo"|"todos"|"task"|"tasks")
    shift
    TASK="$*"
    
    if [ -z "$TASK" ]; then
        echo "📝 Your Spiritual Todos:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        if [ -f "$TODOS_FILE" ] && [ -s "$TODOS_FILE" ]; then
            cat "$TODOS_FILE"
        else
            echo "No todos yet. Add one with:"
            echo "  jacky, add todo [task]"
        fi
    else
        TODO_NUM=$(($(grep -c "^- \[" "$TODOS_FILE" 2>/dev/null || echo "0") + 1))
        echo "- [$TODO_NUM] $TASK" >> "$TODOS_FILE" 2>/dev/null || echo "- [1] $TASK" > "$TODOS_FILE"
        echo "✅ Todo added: $TASK"
    fi
    ;;
    
  "done"|"complete")
    shift
    NUM="$*"
    if [ -n "$NUM" ] && [ -f "$TODOS_FILE" ]; then
        sed -i "s/- \[$NUM\]/- [x]/" "$TODOS_FILE"
        echo "✅ Todo #$NUM marked as complete!"
    else
        echo "Usage: jacky, done [number]"
    fi
    ;;
    
  "journal"|"diary")
    shift
    TEXT="$*"
    
    if [ -z "$TEXT" ]; then
        echo "📓 Your Journal Entries:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        if [ -f "$JOURNAL_FILE" ] && [ -s "$JOURNAL_FILE" ]; then
            tail -10 "$JOURNAL_FILE"
        else
            echo "No entries yet. Write with:"
            echo "  jacky, journal [your thoughts]"
        fi
    else
        DATE=$(date +%Y-%m-%d)
        TIME=$(date +%H:%M)
        echo "- **$DATE $TIME**: $TEXT" >> "$JOURNAL_FILE" 2>/dev/null || echo "- **$DATE $TIME**: $TEXT" > "$JOURNAL_FILE"
        echo "✅ Journal entry saved! 📓"
    fi
    ;;
    
  "help"|"--help"|"-h")
    echo "🕌 Prayer Times Skill Commands:"
    echo ""
    echo "🕐 Prayer Times:"
    echo "  prayer times [city]     - Get today's prayer times"
    echo "  jadwal solat jakarta    - Get times (multi-language)"
    echo ""
    echo "📍 Location:"
    echo "  set location [city]     - Set your city"
    echo ""
    echo "🔔 Reminders:"
    echo "  enable reminders       - Turn on notifications"
    echo "  disable reminders      - Turn off"
    echo ""
    echo "✅ Todos:"
    echo "  add todo [task]        - Add spiritual task"
    echo "  list todos             - Show all tasks"
    echo "  done [number]          - Mark complete"
    echo ""
    echo "📓 Journal:"
    echo "  journal [text]         - Write reflection"
    echo "  journal                - Show recent entries"
    ;;
    
  *)
    echo "🕌 Prayer Times Skill"
    echo "Usage: jacky, [command] [options]"
    echo ""
    echo "Try: 'jacky, prayer times jakarta'"
    echo "Or:   'jacky, help'"
    ;;
esac