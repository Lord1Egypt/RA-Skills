#!/usr/bin/env bash
# memory-oracle: install.sh
# Bootstrap installer — initializes DB, imports existing memory, sets up cron.
#
# Usage:
#   bash install.sh                    # Interactive install
#   bash install.sh --no-cron          # Skip cron setup
#   bash install.sh --workspace /path  # Custom workspace

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[memory-oracle]${NC} $*"; }
warn()  { echo -e "${YELLOW}[memory-oracle]${NC} $*"; }
error() { echo -e "${RED}[memory-oracle]${NC} $*"; }

# Parse args
NO_CRON=false
WORKSPACE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-cron)   NO_CRON=true; shift ;;
        --workspace) WORKSPACE="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: bash install.sh [--no-cron] [--workspace /path]"
            exit 0 ;;
        *) shift ;;
    esac
done

# Check Python
if ! command -v "$PYTHON" &>/dev/null; then
    error "Python 3 not found. Install it first."
    exit 1
fi

PY_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
info "Python: $PYTHON ($PY_VERSION)"

# Check sqlite3 FTS5 support
FTS5_OK=$("$PYTHON" -c "
import sqlite3, tempfile, os
db = os.path.join(tempfile.gettempdir(), 'fts5test.db')
try:
    c = sqlite3.connect(db)
    c.execute('CREATE VIRTUAL TABLE IF NOT EXISTS t USING fts5(x)')
    c.close()
    os.unlink(db)
    print('ok')
except Exception as e:
    print(f'fail: {e}')
" 2>&1)

if [[ "$FTS5_OK" != "ok" ]]; then
    error "SQLite FTS5 not available: $FTS5_OK"
    error "FTS5 is required for full-text search."
    error ""
    error "How to fix:"
    error "  Ubuntu/Debian: sudo apt install libsqlite3-dev && rebuild Python"
    error "  Alpine:        apk add sqlite-dev"
    error "  macOS:         brew install sqlite3 (FTS5 included by default)"
    error "  Or use pyenv:  PYTHON_CONFIGURE_OPTS='--enable-loadable-sqlite-extensions' pyenv install 3.12"
    exit 1
fi
info "SQLite FTS5: available"

# Update workspace in settings if custom
if [[ -n "$WORKSPACE" ]]; then
    info "Custom workspace: $WORKSPACE"
    "$PYTHON" -c "
import json
with open('$SCRIPT_DIR/config/settings.json', 'r') as f:
    s = json.load(f)
s['paths']['workspace'] = '$WORKSPACE'
s['paths']['db'] = '$WORKSPACE/memory-oracle.db'
s['paths']['memory_md'] = '$WORKSPACE/MEMORY.md'
s['paths']['daily_logs'] = '$WORKSPACE/memory'
s['paths']['reflections'] = '$WORKSPACE/memory/reflections'
s['paths']['failed_reflections'] = '$WORKSPACE/memory/failed_reflections'
s['paths']['pending_queue'] = '$WORKSPACE/memory-oracle-pending.json'
with open('$SCRIPT_DIR/config/settings.json', 'w') as f:
    json.dump(s, f, indent=2)
"
fi

# Backup existing MEMORY.md before any modifications
MEMORY_PATH=$("$PYTHON" -c "
import json, os
with open('$SCRIPT_DIR/config/settings.json') as f:
    s = json.load(f)
print(os.path.expanduser(s['paths']['memory_md']))
" 2>/dev/null || echo "$HOME/.openclaw/workspace/MEMORY.md")

if [[ -f "$MEMORY_PATH" ]]; then
    BACKUP_PATH="${MEMORY_PATH}.pre-oracle-backup"
    if [[ ! -f "$BACKUP_PATH" ]]; then
        cp "$MEMORY_PATH" "$BACKUP_PATH"
        info "Backed up MEMORY.md → $(basename "$BACKUP_PATH")"
        info "  (uninstall.sh can restore this)"
    else
        info "MEMORY.md backup already exists, skipping."
    fi
fi

# Initialize database
info "Initializing database..."
"$PYTHON" "$SCRIPT_DIR/scripts/init_db.py"

# Check for ANTHROPIC_API_KEY
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    warn "ANTHROPIC_API_KEY not set."
    warn "HEAVY process (consolidate, reflect) requires this."
    warn "LIGHT process (capture, recall) works without it."
    warn ""
    warn "Set it in your shell profile:"
    warn "  export ANTHROPIC_API_KEY='sk-ant-...'"
fi

# Setup cron
if [[ "$NO_CRON" == "false" ]]; then
    info ""
    info "The HEAVY process (consolidate + reflect + maintenance) runs via cron."
    info "This will add a nightly cron job at 03:00 to your user crontab."
    info ""
    read -r -p "Install cron job? [y/N] " CRON_CONFIRM
    if [[ "$CRON_CONFIRM" =~ ^[Yy]$ ]]; then
        CRON_CMD_NIGHTLY="0 3 * * * cd $SCRIPT_DIR && ANTHROPIC_API_KEY=\${ANTHROPIC_API_KEY} $PYTHON scripts/consolidate.py && $PYTHON scripts/reflect.py --auto && $PYTHON scripts/maintenance.py >> /tmp/memory-oracle-cron.log 2>&1"

        # Check if already installed
        EXISTING=$(crontab -l 2>/dev/null | grep -c "memory-oracle" || true)
        if [[ "$EXISTING" -gt 0 ]]; then
            warn "Cron jobs already exist. Skipping. To reinstall, remove them first:"
            warn "  crontab -e  # then remove memory-oracle lines"
        else
            (crontab -l 2>/dev/null || true; echo "# memory-oracle nightly pipeline"; echo "$CRON_CMD_NIGHTLY") | crontab -
            info "Cron installed: nightly at 03:00"
        fi
    else
        info "Skipping cron setup. You can run the HEAVY pipeline manually:"
        info "  $PYTHON scripts/consolidate.py && $PYTHON scripts/reflect.py --auto && $PYTHON scripts/maintenance.py"
    fi
else
    info "Skipping cron setup (--no-cron)"
fi

# Print AGENTS.md snippet
info ""
info "=============================="
info " Installation complete!"
info "=============================="
info ""
info "MANUAL STEP 1: Add this to your AGENTS.md (or equivalent):"
info ""
cat << 'AGENTS_SNIPPET'
## Memory Oracle Protocol

BEFORE responding to the user:
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/recall.py --query "<user message>"
  Inject the output into your context as relevant background.

AFTER responding to the user:
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --turn "<full turn text>"

When the user says "remember this" or "this is critical":
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --turn "<text>" --guardrail

Every 10 turns (heartbeat):
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --flush
AGENTS_SNIPPET

info ""
info "MANUAL STEP 2: For pre-compaction hook, add to your OpenClaw config"
info "  (e.g. settings.json or settings.toml — depends on your setup):"
info ""
info '  compaction.memoryFlush.prompt: "Run: python3 ~/.openclaw/skills/memory-oracle/scripts/checkpoint.py"'
info ""
info "NOTE: This installer does NOT auto-edit AGENTS.md or OpenClaw config."
info "      Review and paste the snippets above yourself."
info ""
info "Check memory stats anytime:"
info "  $PYTHON $SCRIPT_DIR/scripts/maintenance.py --stats"
