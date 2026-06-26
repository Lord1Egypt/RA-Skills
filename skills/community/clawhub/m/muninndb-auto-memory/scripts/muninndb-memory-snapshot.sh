#!/bin/bash
# ==========================================
# MuninnDB Memory Snapshot
# ==========================================
# Cron-Skript: speichert periodisch einen Kontext-Snapshot in MuninnDB
# Vault: hermes
# Silent bei Erfolg, Error-Output bei Fehlschlag
# ==========================================
# Installiert via: cronjob action=create \
#   name="MuninnDB Memory Snapshot" \
#   schedule="every 30m" \
#   script=muninndb-memory-snapshot.sh \
#   no_agent=true \
#   workdir="/Users/bits"
# ==========================================

MUNINN_URL="http://127.0.0.1:8475"
MUNINN_TOKEN=$(cat ~/.muninn/openclaw.key 2>/dev/null || echo "")
VAULT="hermes"
HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Pruefe ob MuninnDB laeuft
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$MUNINN_URL/api/health" 2>/dev/null)
if [ "$HEALTH" != "200" ]; then
    exit 0  # silent fail
fi

# Aktuelles Verzeichnis + letzte Session-Info
CWD=$(pwd)
RECENT_SESSIONS=$(hermes sessions list --limit 3 2>/dev/null || echo "n/a")

SUMMARY="Cron-Snapshot von $HOSTNAME um $TIMESTAMP
Working Directory: $CWD
Letzte Sessions: $RECENT_SESSIONS"

# In MuninnDB speichern
RESULT=$(curl -s -X POST "$MUNINN_URL/api/engrams" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MUNINN_TOKEN" \
  -d "$(jq -n --arg c "cron-snapshot-$HOSTNAME" --arg x "$SUMMARY" \
    '{concept: $c, content: $x, vault: "hermes", tags: ["cron","snapshot","'$HOSTNAME'"], type: "event"}')" 2>/dev/null)

# Pruefe Ergebnis
ID=$(echo "$RESULT" | jq -r '.id // "FAIL"' 2>/dev/null)
if [ "$ID" = "FAIL" ] || [ -z "$ID" ]; then
    echo "ERR: Speichern fehlgeschlagen: $RESULT"
    exit 1
fi
exit 0  # silent success
