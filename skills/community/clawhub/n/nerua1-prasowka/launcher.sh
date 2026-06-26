#!/bin/bash
# Launcher dla prasowki - ustawia środowisko przed uruchomieniem

export HOME=/Users/nerucb1
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin
export USER=nerucb1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Prasówka launcher start" >> /Users/nerucb1/.openclaw/logs/prasowka.log

exec /bin/bash /Users/nerucb1/.openclaw/workspace/skills/prasowka/run.sh >> /Users/nerucb1/.openclaw/logs/prasowka.log 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Prasówka launcher end" >> /Users/nerucb1/.openclaw/logs/prasowka.log
