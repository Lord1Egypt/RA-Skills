#!/usr/bin/env bash
# ============================================================================
# install.sh — OpenClaw Local Compaction Proxy Installer
# 安装引导 / Installation Guide
#
# Usage:
#   Interactive (recommended):  bash install.sh
#   Non-interactive:            bash install.sh --port 19000 \
#                                 --provider "myprovider|https://api.example.com|sk-mykey" \
#                                 --ollama-model qwen2.5:7b
#
# The installer will:
#   1. Check / guide ollama installation
#   2. Pull the summarisation model
#   3. Collect your LLM provider API key(s)
#   4. Deploy the proxy and register it as a macOS background service
#   5. Show you exactly what to add to ~/.openclaw/openclaw.json
# ============================================================================
set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${BLUE}[info]${RESET}  $*"; }
success() { echo -e "${GREEN}[ok]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
error()   { echo -e "${RED}[error]${RESET} $*" >&2; }
header()  { echo -e "\n${BOLD}$*${RESET}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Defaults ─────────────────────────────────────────────────────────────────
PROXY_DIR="${HOME}/.openclaw/compaction-proxy"
PLIST_PATH="${HOME}/Library/LaunchAgents/ai.openclaw.compaction-proxy.plist"
LOG_DIR="${HOME}/.openclaw/logs"
PORT=19000
OLLAMA_MODEL="qwen3.5:9b-q4_K_M"
OLLAMA_URL="http://127.0.0.1:11434"
PROVIDERS=()          # filled interactively or via --provider flags

# ── Arg parsing ──────────────────────────────────────────────────────────────
NON_INTERACTIVE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)          PORT="$2";         shift 2 ;;
    --ollama-model)  OLLAMA_MODEL="$2"; shift 2 ;;
    --ollama-url)    OLLAMA_URL="$2";   shift 2 ;;
    --provider)      PROVIDERS+=("$2"); shift 2 ;;   # format: "prefix|baseUrl|apiKey"
    --non-interactive) NON_INTERACTIVE=true; shift ;;
    -h|--help)
      echo "Usage: bash install.sh [options]"
      echo "  --port <n>                      Proxy listen port (default: 19000)"
      echo "  --ollama-model <model>          Ollama summarisation model (default: qwen3.5:9b-q4_K_M)"
      echo "  --ollama-url <url>              Ollama base URL (default: http://127.0.0.1:11434)"
      echo "  --provider 'prefix|url|apikey' Add an upstream provider (repeatable)"
      echo "  --non-interactive              Skip interactive prompts"
      exit 0 ;;
    *) error "Unknown argument: $1"; exit 1 ;;
  esac
done

# ═════════════════════════════════════════════════════════════════════════════
# STEP 1: Welcome
# ═════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║   OpenClaw Local Compaction Proxy — Installer v1.1.0    ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════╝${RESET}"
echo ""
echo "This proxy sits between OpenClaw and your LLM providers."
echo "It uses a local ollama model to summarise long conversations"
echo "before they reach the context-window limit, saving API tokens."
echo ""

# ═════════════════════════════════════════════════════════════════════════════
# STEP 2: System checks
# ═════════════════════════════════════════════════════════════════════════════
header "Step 1 / 5 — System checks"

# macOS only
if [[ "$(uname)" != "Darwin" ]]; then
  error "This installer currently supports macOS only."
  error "For Linux, adapt the launchd plist section to use systemd."
  exit 1
fi
success "macOS detected"

# Node.js
NODE_BIN=""
for candidate in \
    "$(which node 2>/dev/null)" \
    "${HOME}/.local/share/fnm/node-versions/v22.22.1/installation/bin/node" \
    /opt/homebrew/bin/node /usr/local/bin/node; do
  if [[ -x "${candidate}" ]]; then
    NODE_BIN="${candidate}"; break
  fi
done
if [[ -z "${NODE_BIN}" ]]; then
  error "Node.js not found. Install it first:"
  echo "  brew install node   # or: https://nodejs.org"
  exit 1
fi
NODE_VER=$("${NODE_BIN}" --version)
success "Node.js ${NODE_VER} at ${NODE_BIN}"

# ═════════════════════════════════════════════════════════════════════════════
# STEP 3: ollama
# ═════════════════════════════════════════════════════════════════════════════
header "Step 2 / 5 — ollama (local summarisation engine)"

OLLAMA_BIN="$(which ollama 2>/dev/null || echo '')"

if [[ -z "${OLLAMA_BIN}" ]]; then
  warn "ollama is not installed."
  echo ""
  echo "ollama runs AI models locally on your Mac — no cloud, no cost."
  echo "The compaction proxy uses it to summarise long conversations,"
  echo "so your paid API quota is consumed much more slowly."
  echo ""
  echo "Install options:"
  echo "  A) Auto-install via Homebrew:  brew install ollama"
  echo "  B) Download the macOS app:     https://ollama.com/download"
  echo "  C) Skip for now (proxy will still work but won't compact contexts)"
  echo ""

  if [[ "${NON_INTERACTIVE}" == "true" ]]; then
    OLLAMA_CHOICE="C"
  else
    read -rp "Choice [A/B/C]: " OLLAMA_CHOICE
  fi

  case "${OLLAMA_CHOICE^^}" in
    A)
      if ! command -v brew &>/dev/null; then
        error "Homebrew not found. Install from https://brew.sh first, then re-run."
        exit 1
      fi
      info "Installing ollama via Homebrew…"
      brew install ollama
      brew services start ollama
      sleep 3
      OLLAMA_BIN="$(which ollama)"
      success "ollama installed" ;;
    B)
      echo ""
      echo "Please download and install ollama from https://ollama.com/download"
      echo "then run this installer again."
      exit 0 ;;
    C)
      warn "Skipping ollama. Proxy will forward requests without compaction."
      OLLAMA_BIN="" ;;
  esac
fi

if [[ -n "${OLLAMA_BIN}" ]]; then
  success "ollama found at ${OLLAMA_BIN}"

  # Check ollama is running
  if ! curl -sf "${OLLAMA_URL}/api/tags" >/dev/null 2>&1; then
    warn "ollama does not appear to be running at ${OLLAMA_URL}"
    echo "Starting ollama service…"
    ollama serve &>/dev/null &
    sleep 3
    if ! curl -sf "${OLLAMA_URL}/api/tags" >/dev/null 2>&1; then
      warn "Could not start ollama automatically."
      echo "Please start it manually: ollama serve"
      echo "Then re-run this installer, or proceed (compaction will be unavailable)."
    fi
  fi

  # Pull summarisation model
  AVAILABLE_MODELS=$(curl -sf "${OLLAMA_URL}/api/tags" 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join(m['name'] for m in d.get('models',[])))" 2>/dev/null || echo "")

  if echo "${AVAILABLE_MODELS}" | grep -q "^${OLLAMA_MODEL}"; then
    success "Summarisation model '${OLLAMA_MODEL}' already available"
  else
    info "Pulling summarisation model '${OLLAMA_MODEL}' (this may take a few minutes)…"
    echo "  Size: ~5.2 GB for qwen3.5:9b-q4_K_M | ~1.9 GB for qwen2.5:3b"
    echo ""
    if [[ "${NON_INTERACTIVE}" == "false" ]]; then
      read -rp "Use '${OLLAMA_MODEL}'? Press Enter to confirm, or type another model name: " ALT_MODEL
      [[ -n "${ALT_MODEL}" ]] && OLLAMA_MODEL="${ALT_MODEL}"
    fi
    ollama pull "${OLLAMA_MODEL}"
    success "Model '${OLLAMA_MODEL}' ready"
  fi
fi

# ═════════════════════════════════════════════════════════════════════════════
# STEP 4: Provider configuration
# ═════════════════════════════════════════════════════════════════════════════
header "Step 3 / 5 — LLM provider API key(s)"

echo "The proxy needs to know which LLM providers to forward requests to,"
echo "along with your API key for each provider."
echo ""
echo "The 'provider prefix' must match the part BEFORE the first '/' in"
echo "the model ID you configure in OpenClaw."
echo ""
echo "Examples:"
echo "  model ID 'kimi-coding/k2p5'            → prefix 'kimi-coding'"
echo "  model ID 'anthropic/claude-sonnet-4.6' → prefix 'anthropic'"
echo "  model ID 'openai/gpt-4o'               → prefix 'openai'"
echo ""

if [[ ${#PROVIDERS[@]} -eq 0 && "${NON_INTERACTIVE}" == "false" ]]; then
  while true; do
    read -rp "Provider prefix (e.g. 'anthropic'): " P_PREFIX
    [[ -z "${P_PREFIX}" ]] && break
    read -rp "Base URL for '${P_PREFIX}': " P_URL
    read -rsp "API key for '${P_PREFIX}': " P_KEY; echo ""
    PROVIDERS+=("${P_PREFIX}|${P_URL}|${P_KEY}")
    read -rp "Add another provider? [y/N]: " MORE
    [[ "${MORE,,}" != "y" ]] && break
  done
fi

if [[ ${#PROVIDERS[@]} -eq 0 ]]; then
  warn "No providers configured. You can edit routes.json later:"
  warn "  ${PROXY_DIR}/routes.json"
fi

# Build routes.json content
ROUTES_JSON="{"
FIRST=true
for PROVIDER in "${PROVIDERS[@]}"; do
  IFS='|' read -r P_PREFIX P_URL P_KEY <<< "${PROVIDER}"
  [[ "${FIRST}" == "false" ]] && ROUTES_JSON+=","
  ROUTES_JSON+="
  \"${P_PREFIX}\": {
    \"baseUrl\": \"${P_URL}\",
    \"apiKey\": \"${P_KEY}\"
  }"
  FIRST=false
done
ROUTES_JSON+="
}"

# ═════════════════════════════════════════════════════════════════════════════
# STEP 5: Deploy
# ═════════════════════════════════════════════════════════════════════════════
header "Step 4 / 5 — Deploying proxy"

mkdir -p "${PROXY_DIR}" "${LOG_DIR}"

# Copy proxy source
cp "${SCRIPT_DIR}/src/index.js" "${PROXY_DIR}/index.js"
success "Deployed proxy source → ${PROXY_DIR}/index.js"

# Write routes.json (skip if exists and no providers supplied)
ROUTES_FILE="${PROXY_DIR}/routes.json"
if [[ -f "${ROUTES_FILE}" && ${#PROVIDERS[@]} -eq 0 ]]; then
  warn "routes.json already exists — keeping existing file"
else
  echo "${ROUTES_JSON}" > "${ROUTES_FILE}"
  chmod 600 "${ROUTES_FILE}"   # API keys — restrict permissions
  success "Created routes.json (permissions: 600)"
fi

# Write launchd plist
cat > "${PLIST_PATH}" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.compaction-proxy</string>

  <key>ProgramArguments</key>
  <array>
    <string>${NODE_BIN}</string>
    <string>${PROXY_DIR}/index.js</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key>
    <string>${HOME}</string>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>COMPACTION_PROXY_PORT</key>
    <string>${PORT}</string>
    <key>OLLAMA_BASE_URL</key>
    <string>${OLLAMA_URL}</string>
    <key>COMPACTION_OLLAMA_MODEL</key>
    <string>${OLLAMA_MODEL}</string>
    <key>COMPACTION_THRESHOLD</key>
    <string>0.85</string>
    <key>RECOMPACT_THRESHOLD</key>
    <string>0.92</string>
    <key>CIRCUIT_BREAKER_TTL_MS</key>
    <string>300000</string>
    <key>MIN_SUMMARY_LENGTH</key>
    <string>100</string>
    <key>COMPACTION_RECENT_TURNS</key>
    <string>10</string>
    <key>COMPACTION_OLLAMA_TIMEOUT_MS</key>
    <string>120000</string>
    <key>COMPACTION_TRANSCRIPT_MAX_CHARS</key>
    <string>80000</string>
    <key>COMPACTION_LOG_FILE</key>
    <string>${LOG_DIR}/compaction-proxy.log</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>Crashed</key>  <true/>
    <key>SuccessfulExit</key> <false/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>StandardOutPath</key>
  <string>${LOG_DIR}/compaction-proxy.out.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/compaction-proxy.err.log</string>
  <key>ProcessType</key>
  <string>Background</string>
</dict>
</plist>
PLIST
success "Created launchd plist → ${PLIST_PATH}"

# Start
launchctl unload "${PLIST_PATH}" 2>/dev/null || true
launchctl load "${PLIST_PATH}"
sleep 2

PID=$(launchctl list ai.openclaw.compaction-proxy 2>/dev/null | grep '"PID"' | grep -oE '[0-9]+' | head -1 || echo "")
if [[ -n "${PID}" ]]; then
  success "Proxy started (PID ${PID}) on port ${PORT}"
else
  warn "Proxy loaded but PID not visible yet — check: ${LOG_DIR}/compaction-proxy.log"
fi

# ═════════════════════════════════════════════════════════════════════════════
# STEP 6: OpenClaw config guide
# ═════════════════════════════════════════════════════════════════════════════
header "Step 5 / 5 — OpenClaw configuration"

echo ""
echo "Add the following to your ~/.openclaw/openclaw.json"
echo "(inside the models.providers object):"
echo ""

# Build model list from providers
MODEL_LIST=""
for PROVIDER in "${PROVIDERS[@]}"; do
  IFS='|' read -r P_PREFIX P_URL P_KEY <<< "${PROVIDER}"
  echo "  For provider '${P_PREFIX}', add one entry per model you use, e.g.:"
  echo ""
  echo "    {"
  echo "      \"id\": \"${P_PREFIX}/your-model-id\","
  echo "      \"name\": \"Your Model via Proxy\","
  echo "      \"contextWindow\": 200000,"
  echo "      \"maxTokens\": 16000,"
  echo "      \"input\": [\"text\", \"image\"],"
  echo "      \"cost\": {\"input\": 0, \"output\": 0, \"cacheRead\": 0, \"cacheWrite\": 0}"
  echo "    }"
  echo ""
done

cat <<JSON
"local-compaction-proxy": {
  "baseUrl": "http://127.0.0.1:${PORT}",
  "apiKey": "proxy-passthrough",
  "api": "anthropic-messages",
  "models": [
    // ... one entry per model (see above)
  ]
}
JSON

echo ""
echo "Then set your primary model (example):"
echo ""
cat <<JSON
"agents": {
  "defaults": {
    "model": {
      "primary": "local-compaction-proxy/YOUR-PREFIX/YOUR-MODEL-ID",
      "fallbacks": [
        "YOUR-PREFIX/YOUR-MODEL-ID",   // direct (no proxy) as fallback
        "ollama/qwen2.5:7b"            // local fallback when APIs are exhausted
      ]
    },
    "compaction": {
      "mode": "default"    // do NOT use "safeguard" — it calls the primary model
    }
  }
}
JSON

echo ""
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "Test the proxy is working:"
echo ""
FIRST_PREFIX=""
FIRST_MODEL_EXAMPLE="your-prefix/your-model-id"
if [[ ${#PROVIDERS[@]} -gt 0 ]]; then
  IFS='|' read -r FIRST_PREFIX _ _ <<< "${PROVIDERS[0]}"
  FIRST_MODEL_EXAMPLE="${FIRST_PREFIX}/your-model-id"
fi
cat <<CMD
  curl -s -X POST http://127.0.0.1:${PORT}/v1/messages \\
    -H "Content-Type: application/json" \\
    -H "x-api-key: proxy-passthrough" \\
    -d '{"model":"${FIRST_MODEL_EXAMPLE}","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
CMD

echo ""
echo "View logs:"
echo "  tail -f ${LOG_DIR}/compaction-proxy.log"
echo ""
success "Installation complete!"
