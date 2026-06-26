#!/usr/bin/env bash
# install.sh — Idempotent install for pctx skill dependencies
# Run once on a new VM or after a full rollback to re-establish the pctx layer.
set -euo pipefail

PCTX_CONFIG="$HOME/.config/pctx/pctx.json"
PCTX_PLIST="$HOME/Library/LaunchAgents/ai.openclaw.pctx.plist"

ok()   { echo "✅ $*"; }
info() { echo "ℹ️  $*"; }
die()  { echo "❌ $*" >&2; exit 1; }

echo "🚀 pctx skill install — idempotent"
echo ""

# 1. pctx binary
if command -v pctx &>/dev/null; then
  ok "pctx already installed: $(pctx --version 2>/dev/null)"
else
  info "Installing pctx via brew..."
  brew install portofcontext/tap/pctx
  ok "pctx installed"
fi

# 2. Deno (Code Mode sandbox runtime)
if command -v deno &>/dev/null; then
  ok "deno already installed: $(deno --version 2>/dev/null | head -1)"
else
  info "Installing deno..."
  brew install deno
  ok "deno installed"
fi

# 3. github-mcp-server
if command -v github-mcp-server &>/dev/null; then
  ok "github-mcp-server already installed: $(github-mcp-server --version 2>&1 | head -1)"
else
  info "Installing github-mcp-server..."
  brew install github-mcp-server
  ok "github-mcp-server installed"
fi

# 4. @tacticlaunch/mcp-linear
if command -v mcp-linear &>/dev/null; then
  ok "mcp-linear already installed"
else
  info "Installing @tacticlaunch/mcp-linear..."
  npm install -g @tacticlaunch/mcp-linear
  ok "mcp-linear installed"
fi

# 5. pctx config
if [[ -f "$PCTX_CONFIG" ]]; then
  ok "pctx config exists: $PCTX_CONFIG"
else
  info "Initialising pctx config..."
  mkdir -p "$HOME/.config/pctx"
  pctx mcp init -y -c "$PCTX_CONFIG"
  chmod 600 "$PCTX_CONFIG"
  ok "pctx config created"
  echo ""
  echo "⚠️  MCP servers not configured. Add them manually:"
  echo "   pctx-skill mcp-add linear --command 'mcp-linear' --env 'LINEAR_API_TOKEN=your_key'"
  echo "   pctx-skill mcp-add github --command 'github-mcp-server' --arg 'stdio' --env 'GITHUB_PERSONAL_ACCESS_TOKEN=your_pat'"
fi

# 6. launchd daemon
if [[ -f "$PCTX_PLIST" ]]; then
  ok "launchd plist exists: $PCTX_PLIST"
else
  info "⚠️  launchd plist not found at $PCTX_PLIST"
  echo "   The plist was configured during MJM-210 setup."
  echo "   If you need to recreate it, see ROLLBACK-MCP-PCTX.md for the full plist content."
fi

# 7. Start daemon if not running
if launchctl list 2>/dev/null | grep -q "ai.openclaw.pctx"; then
  ok "pctx daemon already running"
else
  if [[ -f "$PCTX_PLIST" ]]; then
    info "Loading pctx daemon..."
    launchctl load "$PCTX_PLIST"
    sleep 2
    if curl -sf --max-time 3 http://127.0.0.1:8080/mcp -o /dev/null 2>/dev/null; then
      ok "pctx daemon started on http://127.0.0.1:8080/mcp"
    else
      echo "⚠️  Daemon loaded but /mcp not yet responding. Check /tmp/pctx.err"
    fi
  fi
fi

echo ""
ok "pctx skill install complete"
echo ""
echo "Quick test:"
echo "  bash $(dirname "$0")/pctx-skill.sh status"
echo "  bash $(dirname "$0")/pctx-skill.sh mcp-list"
