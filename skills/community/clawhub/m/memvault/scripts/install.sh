#!/usr/bin/env bash
# MemVault One-Command Installer for OpenClaw
# Usage: bash scripts/install.sh
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${GREEN}[MemVault]${NC} $1"; }
warn()  { echo -e "${YELLOW}[MemVault]${NC} $1"; }
err()   { echo -e "${RED}[MemVault]${NC} $1"; }
step()  { echo -e "${CYAN}[MemVault]${NC} ── $1"; }

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

info "🔐 MemVault Installer"
info "Directory: $SKILL_DIR"
echo ""

# ── 1. Check Docker ──
step "1/6 Checking Docker..."
if ! command -v docker &>/dev/null; then
    err "Docker not found. Install it first: https://docs.docker.com/get-docker/"
    exit 1
fi
if ! docker compose version &>/dev/null; then
    err "Docker Compose not found. Install Docker Desktop or docker-compose-plugin."
    exit 1
fi
info "✅ Docker + Compose ready"

# ── 2. Check/Install Ollama ──
step "2/6 Checking Ollama (local LLM)..."
if ! command -v ollama &>/dev/null; then
    warn "Ollama not found. Attempting install..."
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install ollama 2>/dev/null || {
            warn "Auto-install failed. Install manually: https://ollama.com/download"
            warn "Or set MEMVAULT_LLM_BASE_URL to an OpenAI-compatible endpoint in .env"
        }
    elif [[ "$(uname)" == "Linux" ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    fi
fi

OLLAMA_OK=false
if command -v ollama &>/dev/null; then
    # Ensure Ollama is running
    if ! curl -sf http://127.0.0.1:11434/api/tags &>/dev/null; then
        warn "Ollama installed but not running. Starting..."
        ollama serve &>/dev/null &
        sleep 3
    fi
    # Pull model if needed
    MODEL="${MEMVAULT_LLM_MODEL:-qwen2.5:3b}"
    if ! ollama list 2>/dev/null | grep -q "$MODEL"; then
        info "Pulling $MODEL model (this may take a few minutes)..."
        ollama pull "$MODEL"
    fi
    OLLAMA_OK=true
    info "✅ Ollama ready (model: $MODEL)"
else
    warn "⚠️  No local LLM. Set MEMVAULT_LLM_BASE_URL in .env to use OpenAI/Groq/etc."
fi

# ── 3. Create .env ──
step "3/6 Creating configuration..."
if [[ ! -f "$SKILL_DIR/.env" ]]; then
    cat > "$SKILL_DIR/.env" << ENVEOF
# MemVault Configuration
MEMVAULT_DB_DSN=postgresql://postgres:postgres@127.0.0.1:5432/memvault
MEMVAULT_EMBEDDING_URL=http://127.0.0.1:8001
MEMVAULT_EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMVAULT_LLM_BASE_URL=http://host.docker.internal:11434/v1
MEMVAULT_LLM_API_KEY=ollama
MEMVAULT_LLM_MODEL=${MODEL:-qwen2.5:3b}
MEMVAULT_TRANSLATION=false
MEMVAULT_PORT=8002
ENVEOF
    info "✅ .env created"
else
    info "✅ .env already exists (skipped)"
fi

# ── 4. Start Docker services ──
step "4/6 Starting Docker services (PostgreSQL + Embedding + MemVault)..."
cd "$SKILL_DIR"
docker compose up -d --build 2>&1 | tail -5
info "✅ Docker services started"

# ── 5. Wait for health ──
step "5/6 Waiting for MemVault to be ready..."
MV_PORT="${MEMVAULT_PORT:-8002}"
for i in {1..30}; do
    if curl -sf "http://127.0.0.1:$MV_PORT/health" &>/dev/null; then
        info "✅ MemVault healthy on port $MV_PORT"
        break
    fi
    if [[ $i -eq 30 ]]; then
        warn "MemVault not responding yet. Check: docker compose logs memvault"
    fi
    sleep 2
done

# ── 6. Install CLI ──
step "6/6 Installing memvault CLI..."
chmod +x "$SKILL_DIR/scripts/memvault.sh"
mkdir -p "$HOME/.local/bin"
ln -sf "$SKILL_DIR/scripts/memvault.sh" "$HOME/.local/bin/memvault"

# Add to PATH if needed
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    warn "Add to your shell profile: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
info "════════════════════════════════════════════"
info "  🔐 MemVault installed successfully!"
info "════════════════════════════════════════════"
echo ""
echo "  Test:     memvault health"
echo "  Store:    memvault memorize-text myuser 'I like dark mode' 'Noted!'"
echo "  Retrieve: memvault retrieve myuser 'what theme?'"
echo "  Stats:    memvault stats myuser"
echo ""
echo "  Logs:     docker compose -f $SKILL_DIR/docker-compose.yml logs -f"
echo "  Stop:     docker compose -f $SKILL_DIR/docker-compose.yml down"
echo ""
