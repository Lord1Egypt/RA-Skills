#!/usr/bin/env bash
set -euo pipefail

# Browser Use Skill — Installer
# Installs agent-browser (npm CLI) + browser-use (Python venv) + system deps

VENV_DIR="${BROWSER_USE_VENV:-/opt/browser-use}"
WRAPPER="/usr/local/bin/browser-use-agent"

echo "=== Browser Use Skill Installer ==="

# --- System dependencies ---
echo "[1/5] Installing system dependencies..."
if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3 python3-venv xvfb \
        libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
        libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
        libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
        libatspi2.0-0 2>/dev/null || true
elif command -v brew &>/dev/null; then
    echo "  macOS detected — Chromium ships with Playwright, skipping system deps"
else
    echo "  WARNING: Unknown package manager. Ensure python3, chromium deps are installed."
fi

# --- agent-browser (npm global CLI) ---
echo "[2/5] Installing agent-browser..."
if command -v agent-browser &>/dev/null; then
    echo "  agent-browser already installed: $(agent-browser --version 2>/dev/null || echo 'unknown')"
else
    npm install -g agent-browser
    echo "  Installed agent-browser"
fi

# Install Playwright + Chromium for agent-browser
echo "[3/5] Installing Playwright browsers..."
agent-browser install --with-deps 2>/dev/null || agent-browser install 2>/dev/null || {
    npx playwright install chromium 2>/dev/null || true
}

# --- browser-use (Python venv) ---
echo "[4/5] Setting up browser-use Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q browser-use langchain-anthropic langchain-openai

# Install Playwright in the venv too
"$VENV_DIR/bin/python3" -m playwright install chromium 2>/dev/null || true

# --- Wrapper script ---
echo "[5/5] Creating browser-use-agent wrapper..."
cat > "$WRAPPER" << 'WRAPPER_EOF'
#!/bin/bash
# browser-use-agent — Autonomous browser agent wrapper
# Usage: browser-use-agent "task description" [--model MODEL] [--max-steps N]
set -euo pipefail

VENV_DIR="${BROWSER_USE_VENV:-/opt/browser-use}"
TASK="${1:?Usage: browser-use-agent \"task description\" [--model MODEL] [--max-steps N]}"
shift

MODEL="gpt-4o-mini"
MAX_STEPS=12

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model) MODEL="$2"; shift 2 ;;
        --max-steps) MAX_STEPS="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Auto-detect API key from OpenClaw config if not set
if [ -z "${OPENAI_API_KEY:-}" ] && [ -f "/root/.openclaw/openclaw.json" ]; then
    export OPENAI_API_KEY=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['openai']['apiKey'])" 2>/dev/null || true)
fi
if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -f "/root/.openclaw/openclaw.json" ]; then
    export ANTHROPIC_API_KEY=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['anthropic']['apiKey'])" 2>/dev/null || true)
fi

# Determine LLM provider from model name
if [[ "$MODEL" == claude* ]] || [[ "$MODEL" == anthropic* ]]; then
    LLM_IMPORT="from langchain_anthropic import ChatAnthropic"
    LLM_INIT="ChatAnthropic(model='$MODEL', api_key=os.environ['ANTHROPIC_API_KEY'])"
else
    LLM_IMPORT="from langchain_openai import ChatOpenAI"
    LLM_INIT="ChatOpenAI(model='$MODEL', api_key=os.environ['OPENAI_API_KEY'])"
fi

SCRIPT=$(cat << PYEOF
import asyncio, os, sys
$LLM_IMPORT
from browser_use import Agent

async def run():
    llm = $LLM_INIT
    agent = Agent(task="""$TASK""", llm=llm)
    result = await agent.run(max_steps=$MAX_STEPS)
    final = result.final_result()
    if final:
        print(final.extracted_content if hasattr(final, 'extracted_content') else str(final))
    else:
        for r in result.all_results:
            if r.extracted_content:
                print(r.extracted_content)

asyncio.run(run())
PYEOF
)

echo "$SCRIPT" > /tmp/_bu_task.py
xvfb-run "$VENV_DIR/bin/python3" /tmp/_bu_task.py
WRAPPER_EOF

chmod +x "$WRAPPER"

echo ""
echo "=== Installation complete ==="
echo "  agent-browser: $(command -v agent-browser 2>/dev/null || echo 'not found')"
echo "  browser-use:   $VENV_DIR/bin/python3"
echo "  wrapper:       $WRAPPER"
echo ""
echo "Quick test:"
echo "  agent-browser open https://example.com && agent-browser snapshot -i && agent-browser close"
echo "  browser-use-agent \"Describe what you see on example.com\""
