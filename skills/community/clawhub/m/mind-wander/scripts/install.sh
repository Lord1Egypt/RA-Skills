#!/usr/bin/env bash
# install.sh — mind-wander skill installer
#
# Usage:
#   bash install.sh [OPTIONS]
#
# Options:
#   --workspace DIR       OpenClaw workspace path (default: auto-detect)
#   --ollama-url URL      Ollama endpoint (default: http://172.18.0.1:11436)
#   --model-variant q4|q8 Quantization (default: q8)
#   --falkordb-host HOST  FalkorDB host (default: 172.18.0.1)
#   --perplexity-key KEY  Perplexity API key for web search
#   --skip-download       Skip GGUF download (model already in Ollama)
#   --dry-run             Show what would be done without doing it

set -euo pipefail

WORKSPACE="${WORKSPACE:-}"
OLLAMA_URL="${OLLAMA_URL:-http://172.18.0.1:11436}"
MODEL_VARIANT="${MODEL_VARIANT:-q8}"
FALKORDB_HOST="${FALKORDB_HOST:-172.18.0.1}"
FALKORDB_PORT="${FALKORDB_PORT:-6379}"
PERPLEXITY_KEY="${PERPLEXITY_KEY:-}"
SKIP_DOWNLOAD=0
DRY_RUN=0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
  case $1 in
    --workspace)      WORKSPACE="$2"; shift 2 ;;
    --ollama-url)     OLLAMA_URL="$2"; shift 2 ;;
    --model-variant)  MODEL_VARIANT="$2"; shift 2 ;;
    --falkordb-host)  FALKORDB_HOST="$2"; shift 2 ;;
    --perplexity-key) PERPLEXITY_KEY="$2"; shift 2 ;;
    --skip-download)  SKIP_DOWNLOAD=1; shift ;;
    --dry-run)        DRY_RUN=1; shift ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

# Auto-detect workspace
if [[ -z "$WORKSPACE" ]]; then
  PARENT="$(dirname "$SCRIPT_DIR")"
  if [[ -f "$PARENT/../AGENTS.md" ]]; then
    WORKSPACE="$(realpath "$PARENT/..")"
  elif [[ -f "${HOME}/.openclaw/workspace/AGENTS.md" ]]; then
    WORKSPACE="${HOME}/.openclaw/workspace"
  else
    echo "ERROR: Cannot auto-detect workspace. Use --workspace DIR"
    exit 1
  fi
fi

MW_DIR="$WORKSPACE/mind-wander"
log() { echo "[install] $*"; }
run() { [[ $DRY_RUN -eq 1 ]] && echo "[dry-run] $*" || "$@"; }

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         mind-wander skill installer                  ║"
echo "╚══════════════════════════════════════════════════════╝"
log "Workspace:  $WORKSPACE"
log "Ollama:     $OLLAMA_URL"
log "Model:      qwen3.5-wander-$MODEL_VARIANT"
log "FalkorDB:   $FALKORDB_HOST:$FALKORDB_PORT"
[[ $DRY_RUN -eq 1 ]] && log "DRY RUN"
echo ""

# Step 1: Python packages
log "Installing Python packages..."
export PATH=$PATH:/home/node/.local/bin
if ! python3 -c "import huggingface_hub" &>/dev/null; then
  if ! command -v pip3 &>/dev/null; then
    run curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
    run python3 /tmp/get-pip.py --user --break-system-packages --quiet
  fi
  run pip3 install --user --break-system-packages --quiet huggingface_hub httpx falkordb numpy
  log "  ✅ Packages installed"
else
  log "  ✅ Already present"
fi

# Step 2: Copy scripts to workspace
log "Installing scripts to $MW_DIR..."
run mkdir -p "$MW_DIR"
for f in "$SCRIPT_DIR"/*.py "$SCRIPT_DIR"/*.sh; do
  [[ -f "$f" ]] && run cp "$f" "$MW_DIR/"
done
run chmod +x "$MW_DIR/install.sh" 2>/dev/null || true
log "  ✅ Scripts installed"

# Step 3: Download and register model
if [[ $SKIP_DOWNLOAD -eq 0 ]]; then
  GGUF_FILE="Qwen3.5-9B.Q${MODEL_VARIANT^^:0:1}_${MODEL_VARIANT^^:1}.gguf"
  log "Downloading $GGUF_FILE (~$([ "$MODEL_VARIANT" = "q8" ] && echo "9.5" || echo "5.6")GB)..."
  if [[ $DRY_RUN -eq 0 ]]; then
    python3 - << PYEOF
from huggingface_hub import hf_hub_download
import os
fname = "Qwen3.5-9B.Q${MODEL_VARIANT^^:0:1}_${MODEL_VARIANT^^:1:}.gguf"
# Normalize to actual filename format
if "$MODEL_VARIANT" == "q4":
    fname = "Qwen3.5-9B.Q4_K_M.gguf"
else:
    fname = "Qwen3.5-9B.Q8_0.gguf"
path = hf_hub_download(
    repo_id="Jackrong/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled-v2-GGUF",
    filename=fname,
    local_dir="/tmp/qwen35_wander"
)
print(f"Downloaded: {path} ({os.path.getsize(path)/1e9:.1f}GB)")
PYEOF
    log "  ✅ Downloaded"
    log "Registering with Ollama..."
    python3 "$MW_DIR/scripts/register_model.py" \
      --gguf "/tmp/qwen35_wander/$([ "$MODEL_VARIANT" = "q4" ] && echo "Qwen3.5-9B.Q4_K_M.gguf" || echo "Qwen3.5-9B.Q8_0.gguf")" \
      --variant "$MODEL_VARIANT" \
      --ollama "$OLLAMA_URL" 2>&1 || log "  ⚠️  Register failed — see references/setup.md for manual steps"
  else
    echo "  [dry-run] Would download and register model"
  fi
else
  log "Skipping model download (--skip-download)"
fi

# Step 4: Init wander graph
log "Initialising wander graph..."
if [[ $DRY_RUN -eq 0 ]]; then
  python3 - << PYEOF
import sys; sys.path.insert(0, "$MW_DIR")
from wander_graph import init_wander_graph
init_wander_graph()
print("  Wander graph ready")
PYEOF
  log "  ✅ Wander graph initialised"
fi

# Step 5: Create ON_YOUR_MIND.md template
ON_YOUR_MIND="$WORKSPACE/ON_YOUR_MIND.md"
if [[ ! -f "$ON_YOUR_MIND" ]]; then
  log "Creating ON_YOUR_MIND.md template..."
  if [[ $DRY_RUN -eq 0 ]]; then
    cat > "$ON_YOUR_MIND" << 'TEMPLATE'
# On My Mind

*Questions and tangents for the mind-wander agent to explore.*
*The agent picks ONE per session. Mark done items with ## ✅ COMPLETED.*

---

## Open Questions

- Write your first open question here

## Interesting Tangents

- A connection worth exploring

---
*The agent will explore these during background sessions and write novel findings
to MENTAL_EXPLORATION.md. Check there periodically for discoveries.*
TEMPLATE
    log "  ✅ Created ON_YOUR_MIND.md"
  fi
fi

# Step 6: Register cron job
log "Registering 30-minute cron job..."
if [[ $DRY_RUN -eq 0 ]]; then
  python3 - << PYEOF
import httpx, json, os
try:
    cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    token = cfg.get("gateway", {}).get("auth", {}).get("token", "")
    port  = cfg.get("gateway", {}).get("port", 18789)
    if not token:
        print("  ⚠️  No gateway token found — create cron manually (see references/setup.md)")
    else:
        job = {
            "name": "mind-wander Q8 (30min)",
            "schedule": {"kind": "cron", "expr": "*/30 * * * *", "tz": "UTC"},
            "payload": {
                "kind": "agentTurn",
                "message": f"Run mind-wander. Write /tmp/mw.py: import subprocess,sys\\nr=subprocess.run([sys.executable,'$MW_DIR/run.py','--model','$MODEL_VARIANT'],capture_output=True,text=True,timeout=600,cwd='$WORKSPACE')\\nprint(r.stdout[-800:])\\nif r.returncode!=0: print('ERR:',r.stderr[-200:])\\nThen run it. Reply with last few lines.",
                "timeoutSeconds": 660
            },
            "delivery": {"mode": "none"},
            "sessionTarget": "isolated"
        }
        resp = httpx.post(f"http://localhost:{port}/api/cron/jobs",
            headers={"Authorization": f"Bearer {token}"}, json=job)
        if resp.status_code in (200, 201):
            print(f"  ✅ Cron registered (id: {resp.json().get('id','')})")
        else:
            print(f"  ⚠️  Cron registration failed ({resp.status_code}) — see references/setup.md")
except Exception as e:
    print(f"  ⚠️  Cron registration skipped: {e}")
PYEOF
fi

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     Installation complete!                           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Test: python3 $MW_DIR/run.py --status"
echo "  Run:  python3 $MW_DIR/run.py --verbose"
echo "  Edit: $WORKSPACE/ON_YOUR_MIND.md"
echo ""
