#!/bin/bash
# Monitor prasówki - sprawdza czy dzisiejsza prasówka istnieje, jak nie to generuje

DATE=$(date +%Y%m%d)
FILE="$HOME/.openclaw/canvas/prasowka-$DATE.html"
LOG="$HOME/.openclaw/logs/prasowka-monitor.log"

if [ ! -f "$FILE" ]; then
    echo "$(date): Prasówka $DATE nie istnieje! Generuję..." >> "$LOG"
    cd "$HOME/.openclaw/workspace/skills/prasowka" && bash run.sh >> "$LOG" 2>&1
    echo "$(date): Wygenerowano" >> "$LOG"
else
    echo "$(date): Prasówka $DATE OK ($(du -h $FILE | cut -f1))" >> "$LOG"
fi
