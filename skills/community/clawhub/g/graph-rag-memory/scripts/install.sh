#!/usr/bin/env bash
# install.sh — memory-upgrade full installation script
#
# Installs and configures the graph-rag memory system for OpenClaw.
# Safe to re-run — idempotent checks at each step.
#
# Usage:
#   bash install.sh [OPTIONS]
#
# Options:
#   --workspace DIR        Path to OpenClaw workspace (default: auto-detect)
#   --ollama-url URL       Ollama URL for embeddings (default: http://172.18.0.1:11436)
#   --llm-url URL          Ollama URL for LLM/entity extraction (default: http://172.18.0.1:11437)
#   --llm-model MODEL      LLM model name (default: gemma4:e4b)
#   --falkordb-host HOST   FalkorDB host (default: 172.18.0.1)
#   --falkordb-port PORT   FalkorDB port (default: 6379)
#   --ollama-container NAME  Docker container for model pulls (default: ollama-modern-gpu)
#   --skip-models          Skip Ollama model pulls
#   --skip-seed            Skip initial graph seeding
#   --dry-run              Show what would be done without doing it
#
# What this does:
#   1.  Checks prerequisites
#   2.  Installs Python dependencies
#   3.  Pulls required Ollama embedding models (bge-m3, snowflake-arctic-embed2,
#       nomic-embed-text, mxbai-embed-large)
#   4.  Configures endpoints in config.py
#   5.  Builds the C inotify daemon (memwatchd)
#   6.  Patches openclaw.json (skills.extraDirs + memorySearch.extraPaths)
#   7.  Seeds the graph from workspace memory files
#   8.  Creates FalkorDB vector index
#   9.  Recalibrates domain routing centroids
#   10. Starts memwatchd daemon
#   11. Generates initial GRAPH_MEMORY_BRIEF.md
#   12. Creates 5-minute OpenClaw cron job (via API)
#   13. Validates the installation

set -euo pipefail

# ─── Defaults ────────────────────────────────────────────────────────────────
WORKSPACE="${WORKSPACE:-}"
OLLAMA_URL="${OLLAMA_URL:-http://172.18.0.1:11436}"
LLM_URL="${LLM_URL:-http://172.18.0.1:11437}"
LLM_MODEL="${LLM_MODEL:-gemma4:e4b}"
FALKORDB_HOST="${FALKORDB_HOST:-172.18.0.1}"
FALKORDB_PORT="${FALKORDB_PORT:-6379}"
OLLAMA_CONTAINER="${OLLAMA_CONTAINER:-ollama-modern-gpu}"
SKIP_MODELS=0
SKIP_SEED=0
DRY_RUN=0
OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# ─── Parse args ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --workspace)        WORKSPACE="$2"; shift 2 ;;
    --ollama-url)       OLLAMA_URL="$2"; shift 2 ;;
    --llm-url)          LLM_URL="$2"; shift 2 ;;
    --llm-model)        LLM_MODEL="$2"; shift 2 ;;
    --falkordb-host)    FALKORDB_HOST="$2"; shift 2 ;;
    --falkordb-port)    FALKORDB_PORT="$2"; shift 2 ;;
    --ollama-container) OLLAMA_CONTAINER="$2"; shift 2 ;;
    --skip-models)      SKIP_MODELS=1; shift ;;
    --skip-seed)        SKIP_SEED=1; shift ;;
    --dry-run)          DRY_RUN=1; shift ;;
    -h|--help) grep "^#" "$0" | head -40 | sed 's/^# \?//'; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ─── Auto-detect workspace ───────────────────────────────────────────────────
if [[ -z "$WORKSPACE" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  WORKSPACE="$(dirname "$SCRIPT_DIR")"
  # Verify it looks like an OpenClaw workspace
  if [[ ! -f "$WORKSPACE/MEMORY.md" && ! -f "$WORKSPACE/AGENTS.md" ]]; then
    # Try standard location
    WORKSPACE="${HOME}/.openclaw/workspace"
  fi
fi
MEM_DIR="$WORKSPACE/memory-upgrade"

# ─── Helpers ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${GREEN}[install]${NC} $*"; }
warn() { echo -e "${YELLOW}[install]${NC} ⚠️  $*"; }
err()  { echo -e "${RED}[install]${NC} ❌ $*"; }
run()  { [[ $DRY_RUN -eq 1 ]] && echo "  [dry-run] $*" || "$@"; }
check_service() {
    python3 -c "
import socket, sys
s = socket.socket()
s.settimeout(2)
try:
    s.connect(('$1', $2))
    print('ok')
except:
    print('fail')
finally:
    s.close()
" 2>/dev/null
}

# ─── Header ──────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     memory-upgrade — Graph-RAG Memory Installer          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
log "Workspace:    $WORKSPACE"
log "Ollama emb:   $OLLAMA_URL"
log "Ollama LLM:   $LLM_URL ($LLM_MODEL)"
log "FalkorDB:     $FALKORDB_HOST:$FALKORDB_PORT"
[[ $DRY_RUN -eq 1 ]] && warn "DRY RUN — no changes will be made"
echo ""

# ─── Step 1: Prerequisites ───────────────────────────────────────────────────
log "Step 1/13: Checking prerequisites..."

[[ ! -d "$MEM_DIR" ]] && { err "memory-upgrade directory not found at $MEM_DIR"; exit 1; }
log "  ✅ memory-upgrade directory found"

python3 --version &>/dev/null || { err "python3 not found"; exit 1; }
log "  ✅ python3 $(python3 --version 2>&1 | cut -d' ' -f2)"

HAS_GCC=0
if command -v gcc &>/dev/null; then
    HAS_GCC=1; log "  ✅ gcc available"
else
    warn "gcc not found — C daemon will not be built (cron fallback only)"
fi

[[ "$(check_service $FALKORDB_HOST $FALKORDB_PORT)" == "ok" ]] && \
    log "  ✅ FalkorDB reachable at $FALKORDB_HOST:$FALKORDB_PORT" || \
    warn "FalkorDB not reachable — start with: docker run -d -p 6379:6379 falkordb/falkordb"

OLLAMA_HOST=$(echo $OLLAMA_URL | sed 's|http://||' | cut -d: -f1)
OLLAMA_PORT=$(echo $OLLAMA_URL | sed 's|http://||' | cut -d: -f2)
[[ "$(check_service $OLLAMA_HOST $OLLAMA_PORT)" == "ok" ]] && \
    log "  ✅ Ollama reachable at $OLLAMA_URL" || \
    warn "Ollama not reachable at $OLLAMA_URL"

# ─── Step 2: Python packages ─────────────────────────────────────────────────
log "Step 2/13: Installing Python packages..."
export PATH=$PATH:/home/node/.local/bin

if ! python3 -c "import graphiti_core" &>/dev/null; then
    if ! command -v pip3 &>/dev/null; then
        run curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        run python3 /tmp/get-pip.py --user --break-system-packages --quiet
    fi
    run pip3 install --user --break-system-packages --quiet \
        graphiti-core falkordb sentence-transformers httpx
    log "  ✅ Packages installed"
else
    log "  ✅ Packages already present"
fi

# ─── Step 3: Ollama models ───────────────────────────────────────────────────
if [[ $SKIP_MODELS -eq 0 ]]; then
    log "Step 3/13: Pulling Ollama embedding models..."
    REQUIRED_MODELS=("nomic-embed-text" "bge-m3" "snowflake-arctic-embed2" "mxbai-embed-large")
    LLM_REQUIRED_MODELS=("$LLM_MODEL")

    pull_model() {
        local MODEL=$1 CONTAINER=$2 URL=$3
        # Check if already loaded
        if curl -sf "$URL/api/tags" 2>/dev/null | grep -q "\"$MODEL\""; then
            log "  ✅ $MODEL already loaded"
            return 0
        fi
        log "  Pulling $MODEL onto $CONTAINER..."
        if command -v docker &>/dev/null; then
            run docker exec "$CONTAINER" ollama pull "$MODEL" 2>&1 | tail -1
        else
            warn "  docker not available — pull $MODEL manually: ollama pull $MODEL"
        fi
    }

    for MODEL in "${REQUIRED_MODELS[@]}"; do
        pull_model "$MODEL" "$OLLAMA_CONTAINER" "$OLLAMA_URL"
    done
    for MODEL in "${LLM_REQUIRED_MODELS[@]}"; do
        LLM_CONTAINER="${LLM_CONTAINER:-$OLLAMA_CONTAINER}"
        pull_model "$MODEL" "$LLM_CONTAINER" "$LLM_URL"
    done
else
    log "Step 3/13: Skipping model pulls (--skip-models)"
fi

# ─── Step 4: Configure endpoints ─────────────────────────────────────────────
log "Step 4/13: Configuring endpoints..."
CONFIG="$MEM_DIR/config.py"
if [[ -f "$CONFIG" ]]; then
    run sed -i \
        -e "s|OLLAMA_URL.*=.*os.environ.*|OLLAMA_URL = os.environ.get(\"OLLAMA_URL\", \"$OLLAMA_URL\")|" \
        -e "s|AMD_OLLAMA_URL.*=.*os.environ.*|AMD_OLLAMA_URL = os.environ.get(\"AMD_OLLAMA_URL\", \"$LLM_URL\")|" \
        -e "s|LLM_MODEL.*=.*os.environ.*|LLM_MODEL = os.environ.get(\"LLM_MODEL\", \"$LLM_MODEL\")|" \
        -e "s|FALKORDB_HOST.*=.*os.environ.*|FALKORDB_HOST = os.environ.get(\"FALKORDB_HOST\", \"$FALKORDB_HOST\")|" \
        -e "s|FALKORDB_PORT.*=.*os.environ.*|FALKORDB_PORT = int(os.environ.get(\"FALKORDB_PORT\", \"$FALKORDB_PORT\"))|" \
        "$CONFIG"
    log "  ✅ config.py updated"
fi

# ─── Step 5: Build C daemon ──────────────────────────────────────────────────
log "Step 5/13: Building memwatchd daemon..."
if [[ $HAS_GCC -eq 1 && -f "$MEM_DIR/memwatchd.c" ]]; then
    run gcc -O2 -Wall -o "$MEM_DIR/memwatchd" "$MEM_DIR/memwatchd.c" 2>&1
    log "  ✅ memwatchd built ($(du -h "$MEM_DIR/memwatchd" 2>/dev/null | cut -f1))"
else
    warn "Skipping daemon build — using cron fallback"
fi

# ─── Step 6: Patch OpenClaw config ───────────────────────────────────────────
log "Step 6/13: Patching OpenClaw config..."
BRIEF_PATH="$WORKSPACE/GRAPH_MEMORY_BRIEF.md"
SKILLS_PUBLIC="$WORKSPACE/skills/public"

if [[ $DRY_RUN -eq 0 && -f "$OPENCLAW_CONFIG" ]]; then
    python3 - << PYEOF
import json, sys
path = "$OPENCLAW_CONFIG"
try:
    with open(path) as f:
        cfg = json.load(f)
except:
    print("  Could not read openclaw.json")
    sys.exit(0)

changed = False

# skills.load.extraDirs
skills = cfg.setdefault("skills", {})
load = skills.setdefault("load", {})
dirs = load.setdefault("extraDirs", [])
if "$SKILLS_PUBLIC" not in dirs:
    dirs.append("$SKILLS_PUBLIC")
    changed = True

# agents.defaults.memorySearch.extraPaths
agents = cfg.setdefault("agents", {})
defs = agents.setdefault("defaults", {})
mem = defs.setdefault("memorySearch", {})
paths = mem.setdefault("extraPaths", [])
if "$BRIEF_PATH" not in paths:
    paths.append("$BRIEF_PATH")
    changed = True

if changed:
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print("  ✅ openclaw.json patched (skills.extraDirs + memorySearch.extraPaths)")
else:
    print("  ✅ openclaw.json already configured")
PYEOF
else
    [[ $DRY_RUN -eq 1 ]] && echo "  [dry-run] Would patch openclaw.json"
    [[ ! -f "$OPENCLAW_CONFIG" ]] && warn "openclaw.json not found at $OPENCLAW_CONFIG — patch manually"
fi

# ─── Step 7: Seed graph ──────────────────────────────────────────────────────
if [[ $SKIP_SEED -eq 0 ]]; then
    log "Step 7/13: Seeding graph from workspace memory files..."
    if [[ $DRY_RUN -eq 0 ]]; then
        cd "$MEM_DIR"
        export PATH=$PATH:/home/node/.local/bin
        python3 phase3_ingest.py && log "  ✅ Core memories seeded" || warn "Seeding failed — run manually: python3 $MEM_DIR/phase3_ingest.py"
        python3 phase6_full_ingest.py && log "  ✅ Full workspace ingested" || warn "Full ingest failed"
    else
        echo "  [dry-run] Would run phase3_ingest.py + phase6_full_ingest.py"
    fi
else
    log "Step 7/13: Skipping seed (--skip-seed)"
fi

# ─── Step 8: Vector index ────────────────────────────────────────────────────
log "Step 8/13: Creating FalkorDB vector index..."
if [[ $DRY_RUN -eq 0 ]]; then
    export PATH=$PATH:/home/node/.local/bin
    python3 "$MEM_DIR/phase5_vector_index.py" && log "  ✅ Vector index ready" || warn "Vector index failed — run manually"
else
    echo "  [dry-run] Would run phase5_vector_index.py"
fi

# ─── Step 9: Calibrate centroids ─────────────────────────────────────────────
log "Step 9/13: Calibrating domain routing centroids..."
if [[ $DRY_RUN -eq 0 ]]; then
    export PATH=$PATH:/home/node/.local/bin
    python3 - << 'PYEOF'
import asyncio, sys
sys.path.insert(0, '/home/node/.openclaw/workspace/memory-upgrade' if True else '')
import os; sys.path.insert(0, os.path.join(os.environ.get('MEM_DIR', '.'), ''))
from router import DomainRouter
from config import OLLAMA_URL

SEED = {
    "personal":  ["Jebadiah prefers Telegram for milestone updates", "user contact preferences timezone"],
    "project":   ["Phase complete FalkorDB Ollama environment setup", "milestone spec progress checkpoint"],
    "technical": ["docker exec ollama pull ROCm AMD container", "gcc inotify daemon build compile"],
    "research":  ["RouterRetriever centroid routing AAAI 2025 MoE", "embedding model benchmark evaluation"],
    "episodic":  ["black apples test message session memory", "what happened today conversation recall"],
    "meta":      ["SOUL.md HEARTBEAT.md agent identity persona", "graph_refresh memwatchd brief generation"],
}

async def main():
    r = DomainRouter(ollama_base_url=OLLAMA_URL)
    await r.bootstrap_centroids(SEED)
    print("  ✅ Centroids calibrated")

asyncio.run(main())
PYEOF
else
    echo "  [dry-run] Would calibrate routing centroids"
fi

# ─── Step 10: Start daemon ───────────────────────────────────────────────────
log "Step 10/13: Starting memwatchd daemon..."
run bash "$MEM_DIR/start_memwatchd.sh" "$WORKSPACE"

# ─── Step 11: Initial brief ──────────────────────────────────────────────────
log "Step 11/13: Generating initial GRAPH_MEMORY_BRIEF.md..."
if [[ $DRY_RUN -eq 0 ]]; then
    export PATH=$PATH:/home/node/.local/bin
    python3 "$MEM_DIR/graph_refresh.py" --brief-only --quiet && \
        log "  ✅ Brief generated: $BRIEF_PATH" || \
        warn "Brief generation failed — will retry at next cron tick"
else
    echo "  [dry-run] Would run graph_refresh.py --brief-only"
fi

# ─── Step 12: Cron job ───────────────────────────────────────────────────────
log "Step 12/13: Cron job setup..."
echo "  ℹ️  Create the 5-minute refresh cron via OpenClaw API or web UI:"
echo "     Schedule: */5 * * * * UTC"
echo "     Task:     agentTurn — starts daemon + runs graph_refresh.py --quiet"
echo "     Delivery: none (silent background)"
echo "     See memory-upgrade/OPENCLAW_INTEGRATION.md for exact API call"

# ─── Step 13: Validate ───────────────────────────────────────────────────────
log "Step 13/13: Validating installation..."
if [[ $DRY_RUN -eq 0 ]]; then
    export PATH=$PATH:/home/node/.local/bin
    echo ""
    python3 "$WORKSPACE/skills/public/graph-rag-memory/scripts/status.py" 2>/dev/null || \
        python3 - << 'PYEOF'
import sys; sys.path.insert(0, '/home/node/.openclaw/workspace/memory-upgrade')
import falkordb, httpx
from config import FALKORDB_HOST, FALKORDB_PORT, OLLAMA_URL

try:
    r = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    graphs = r.list_graphs()
    g = r.select_graph('workspace')
    n = g.query("MATCH (n) RETURN count(n)").result_set[0][0]
    e = g.query("MATCH ()-[r:RELATES_TO]->() RETURN count(r)").result_set[0][0]
    print(f"  ✅ FalkorDB: workspace graph ({n} nodes, {e} edges)")
except Exception as ex:
    print(f"  ❌ FalkorDB: {ex}")

try:
    resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    models = [m['name'] for m in resp.json().get('models', [])]
    required = ['nomic-embed-text', 'bge-m3', 'snowflake-arctic-embed2']
    for m in required:
        hit = any(m in loaded for loaded in models)
        print(f"  {'✅' if hit else '❌'} Ollama: {m}")
except Exception as ex:
    print(f"  ❌ Ollama: {ex}")
PYEOF
fi

# ─── Done ────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Installation complete!                               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Quick test:"
echo "    python3 $MEM_DIR/phase4_query_test.py"
echo ""
echo "  Query memory:"
echo "    python3 $WORKSPACE/skills/public/graph-rag-memory/scripts/query_memory.py 'your question'"
echo ""
echo "  System status:"
echo "    python3 $WORKSPACE/skills/public/graph-rag-memory/scripts/status.py"
echo ""
echo "  Restart OpenClaw to pick up config changes:"
echo "    openclaw gateway restart"
echo ""
