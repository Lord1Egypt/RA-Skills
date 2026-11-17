#!/usr/bin/env bash
# Companion-Starter fuer macOS und Linux.
# Gleiche Logik wie start.ps1: Laufzeit suchen, nicht doppelt starten,
# auf den Port warten, beim Scheitern das Protokoll zeigen.
set -uo pipefail

APP_NAME="Companion"
SCRIPT="server.py"
PORT="${PORT:-8765}"
INTERVAL="${INTERVAL:-120}"
HEALTH="/api/status"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="$ROOT/data"; PIDF="$DATA/companion.pid"; LOG="$DATA/companion.log"
URL="http://127.0.0.1:$PORT"

alive() { curl -sf -o /dev/null --max-time 2 "$URL$HEALTH"; }

case "${1:-}" in
  stop)
    [ -f "$PIDF" ] && kill "$(cat "$PIDF")" 2>/dev/null && echo "  $APP_NAME beendet."
    rm -f "$PIDF"; exit 0 ;;
  status)
    alive && echo "  Laeuft auf $URL" || echo "  Auf $URL antwortet nichts."; exit 0 ;;
esac

PY=""
for c in python3 python; do command -v "$c" >/dev/null 2>&1 && { PY="$c"; break; }; done
if [ -z "$PY" ]; then
  echo "  Python wurde nicht gefunden."
  echo "  macOS:  brew install python3"
  echo "  Debian: sudo apt install python3"
  exit 1
fi
echo "  Python: $PY"

if alive; then
  echo "  Laeuft bereits auf $URL — wird nicht erneut gestartet."
else
  mkdir -p "$DATA"
  ( cd "$ROOT" && nohup "$PY" "$SCRIPT" --port "$PORT" \
      --poll-interval "$INTERVAL" --no-browser > "$LOG" 2>&1 & echo $! > "$PIDF" )
  echo "  Gestartet (PID $(cat "$PIDF")), warte auf Antwort ..."
  ok=0
  for _ in $(seq 40); do sleep 0.5; alive && { ok=1; break; }; done
  if [ "$ok" -eq 0 ]; then
    echo "  Keine Antwort. Letzte Zeilen des Protokolls:"
    tail -n 15 "$LOG" 2>/dev/null | sed 's/^/    /'
    exit 1
  fi
  echo "  Antwortet."
fi

if command -v open >/dev/null 2>&1;      then open "$URL"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1
fi
echo "  Laeuft im Hintergrund auf $URL"
echo "  Beenden:  ./start.sh stop"
