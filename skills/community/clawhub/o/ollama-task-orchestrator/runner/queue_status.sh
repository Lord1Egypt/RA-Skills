#!/bin/bash
# queue_status.sh — Check and optionally clean the Ollama task queue on worker Mac
# Usage:
#   ./queue_status.sh                        # check status
#   ./queue_status.sh clean                  # clean stale locks (asks confirmation if Ollama busy)
#   ./queue_status.sh clean --force          # clean without prompting (safe for SSH/scripts)
#   ./queue_status.sh clean --kill-ollama    # stop Ollama server entirely (cancels active generation)

WORKER_ROOT="$HOME/worker"
QUEUE_DIR="$WORKER_ROOT/queue"
LOCK_DIR="$QUEUE_DIR/ollama.lock.d"
OLLAMA_API="http://localhost:11434"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=== Ollama Queue Status ==="
echo ""

# ── 1. Ollama server ──────────────────────────────────────────────────────────
echo -n "Ollama server:     "
if curl -s --max-time 3 "$OLLAMA_API/api/tags" > /dev/null 2>&1; then
  echo -e "${GREEN}running${NC}"
else
  echo -e "${RED}NOT RESPONDING${NC}"
  echo ""
  echo "Ollama is not running. Start it with: ollama serve"
  exit 1
fi

# ── 2. Active model ───────────────────────────────────────────────────────────
echo -n "Active model:      "
ACTIVE=$(curl -s --max-time 3 "$OLLAMA_API/api/ps" | \
  python3 -c "import sys,json; m=json.load(sys.stdin).get('models',[]); print(m[0]['name'] if m else '')" 2>/dev/null)
if [ -n "$ACTIVE" ]; then
  echo -e "${YELLOW}BUSY — $ACTIVE is generating${NC}"
  OLLAMA_BUSY=true
else
  echo -e "${GREEN}idle${NC}"
  OLLAMA_BUSY=false
fi

# ── 3. Lock directory ─────────────────────────────────────────────────────────
echo -n "Lock dir:          "
if [ -d "$LOCK_DIR" ]; then
  if [ -f "$LOCK_DIR/pid" ]; then
    LOCK_PID=$(cat "$LOCK_DIR/pid" 2>/dev/null)
    if kill -0 "$LOCK_PID" 2>/dev/null; then
      echo -e "${YELLOW}held by PID $LOCK_PID (alive)${NC}"
      LOCK_STATE="alive"
    else
      echo -e "${RED}STALE — PID $LOCK_PID is dead${NC}"
      LOCK_STATE="stale"
    fi
  else
    echo -e "${RED}STALE — no PID file (process killed before write)${NC}"
    LOCK_STATE="stale_nopid"
  fi
else
  echo -e "${GREEN}clear${NC}"
  LOCK_STATE="clear"
fi

# ── 4. Runner processes ───────────────────────────────────────────────────────
echo -n "Runner processes:  "
RUNNERS=$(pgrep -f "run_task.sh" 2>/dev/null | tr '\n' ' ')
CURLS=$(pgrep -f "curl.*11434" 2>/dev/null | tr '\n' ' ')
if [ -n "$RUNNERS" ] || [ -n "$CURLS" ]; then
  echo -e "${YELLOW}running${NC}"
  [ -n "$RUNNERS" ] && echo "  run_task.sh PIDs: $RUNNERS"
  [ -n "$CURLS"   ] && echo "  curl PIDs:        $CURLS"
else
  echo -e "${GREEN}none${NC}"
fi

# ── 5. Queue files ────────────────────────────────────────────────────────────
echo -n "Queue files:       "
PENDING=$(ls "$QUEUE_DIR/pending/" 2>/dev/null | wc -l | tr -d ' ')
DONE=$(ls "$QUEUE_DIR/done/" 2>/dev/null | wc -l | tr -d ' ')
FAILED=$(ls "$QUEUE_DIR/failed/" 2>/dev/null | wc -l | tr -d ' ')
echo "pending=$PENDING  done=$DONE  failed=$FAILED"

# ── 6. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=== Summary ==="

if [ "$OLLAMA_BUSY" = true ] && [ "$LOCK_STATE" = "alive" ]; then
  echo -e "${YELLOW}✓ Normal: Ollama is running a job with a valid lock${NC}"
  echo "  Wait for it to finish, or run with 'clean' to force-reset."

elif [ "$OLLAMA_BUSY" = true ] && [ "$LOCK_STATE" = "clear" ]; then
  echo -e "${RED}⚠ Orphan: Ollama is busy but no lock dir exists${NC}"
  echo "  A runner process started Ollama but was killed before acquiring/releasing lock."
  echo "  Ollama will finish its current job. Lock is clear so next job can start."

elif [ "$OLLAMA_BUSY" = false ] && [ "$LOCK_STATE" != "clear" ]; then
  echo -e "${RED}⚠ Stale lock: Ollama is idle but lock dir exists${NC}"
  echo "  Run with 'clean' to clear it."

elif [ "$OLLAMA_BUSY" = false ] && [ "$LOCK_STATE" = "clear" ]; then
  echo -e "${GREEN}✓ All clear: Ollama idle, no lock, ready for next job${NC}"
fi

echo ""

# ── 7. Clean (optional) ───────────────────────────────────────────────────────
if [ "${1:-}" = "clean" ]; then
  FORCE="${2:-}"
  echo "=== Cleaning ==="

  if [ "$OLLAMA_BUSY" = true ] && [ "$FORCE" = "--kill-ollama" ]; then
    echo -e "${RED}--kill-ollama: stopping Ollama server to cancel active generation...${NC}"
    pkill -9 -f "ollama" 2>/dev/null
    sleep 3
    echo "Restarting Ollama server..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
    echo -e "${GREEN}Ollama restarted.${NC}"

  elif [ "$OLLAMA_BUSY" = true ]; then
    echo -e "${YELLOW}Warning: Ollama is actively generating internally.${NC}"
    echo "  Killing curl/runners will NOT stop it — Ollama processes requests internally."
    echo "  To fully stop: use 'clean --kill-ollama' to restart Ollama server."
    echo "  Or wait for it to finish naturally."
    if [ "$FORCE" != "--force" ]; then
      echo -n "  Still clean locks/runners? (y/N): "
      read -r confirm
      if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Aborted."
        exit 0
      fi
    else
      echo "  --force: cleaning locks and runners only (Ollama will keep generating)."
    fi
  fi

  # Kill stuck runner bash processes (force kill)
  if [ -n "$RUNNERS" ]; then
    echo "Killing run_task.sh processes: $RUNNERS"
    kill -9 $RUNNERS 2>/dev/null
  fi

  # Kill curl processes
  if [ -n "$CURLS" ]; then
    echo "Killing curl processes: $CURLS"
    kill -9 $CURLS 2>/dev/null
  fi

  sleep 2

  # Remove stale lock
  if [ -d "$LOCK_DIR" ]; then
    echo "Removing lock dir: $LOCK_DIR"
    rm -rf "$LOCK_DIR"
  fi

  echo -e "${GREEN}Done. Processes killed.${NC}"
  echo ""

  # Wait for Ollama to settle after curl disconnect
  echo -n "Waiting for Ollama to settle..."
  for i in 1 2 3 4 5; do
    sleep 2
    ACTIVE2=$(curl -s --max-time 3 "$OLLAMA_API/api/ps" | \
      python3 -c "import sys,json; m=json.load(sys.stdin).get('models',[]); print(m[0]['name'] if m else '')" 2>/dev/null)
    if [ -z "$ACTIVE2" ]; then
      echo " idle"
      break
    fi
    echo -n "."
  done

  echo ""
  echo "=== Final Status ==="
  ACTIVE2=$(curl -s --max-time 3 "$OLLAMA_API/api/ps" | \
    python3 -c "import sys,json; m=json.load(sys.stdin).get('models',[]); print(m[0]['name'] if m else 'idle')" 2>/dev/null)
  RUNNERS2=$(pgrep -f "run_task.sh" 2>/dev/null | tr '\n' ' ')
  CURLS2=$(pgrep -f "curl.*11434" 2>/dev/null | tr '\n' ' ')
  echo "Ollama:  ${ACTIVE2:-idle}"
  echo "Lock:    $([ -d "$LOCK_DIR" ] && echo 'exists' || echo 'clear')"
  echo "Runners: ${RUNNERS2:-none}"
  echo "Curls:   ${CURLS2:-none}"
  echo ""
fi
