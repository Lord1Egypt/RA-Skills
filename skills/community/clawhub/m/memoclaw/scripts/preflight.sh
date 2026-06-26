#!/usr/bin/env bash
# MemoClaw preflight check — verify prerequisites before a session.
# Usage: bash scripts/preflight.sh
# Exit 0 = ready, exit 1 = something needs fixing.
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'
ERRORS=0

ok()   { echo -e "  ${GREEN}✔${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
fail() { echo -e "  ${RED}✘${NC} $1"; ERRORS=$((ERRORS + 1)); }

echo "MemoClaw preflight check"
echo "========================"
echo

# 1. CLI installed?
if command -v memoclaw &>/dev/null; then
  VER=$(memoclaw --version 2>/dev/null || echo "unknown")
  ok "CLI installed (${VER})"
else
  fail "memoclaw CLI not found — run: npm install -g memoclaw"
fi

# 2. Config present?
if [ -f "$HOME/.memoclaw/config.json" ]; then
  ok "Config file exists (~/.memoclaw/config.json)"
else
  if [ -n "${MEMOCLAW_PRIVATE_KEY:-}" ]; then
    ok "Wallet configured via MEMOCLAW_PRIVATE_KEY env var"
  else
    fail "No config and no MEMOCLAW_PRIVATE_KEY — run: memoclaw init"
  fi
fi

# 3. Config valid?
if command -v memoclaw &>/dev/null; then
  if memoclaw config check &>/dev/null 2>&1; then
    ok "Config is valid"
  else
    fail "Config check failed — run: memoclaw config check"
  fi
fi

# 4. API reachable?
if command -v memoclaw &>/dev/null; then
  if memoclaw count &>/dev/null 2>&1; then
    ok "API is reachable"
  else
    warn "API unreachable — check network or https://api.memoclaw.com"
  fi
fi

# 5. Free tier status
if command -v memoclaw &>/dev/null; then
  STATUS_OUT=$(memoclaw status --json 2>/dev/null || echo "")
  if [ -n "$STATUS_OUT" ]; then
    FREE_LEFT=$(echo "$STATUS_OUT" | grep -oP '"free_calls_remaining"\s*:\s*\K[0-9]+' 2>/dev/null || echo "")
    if [ -n "$FREE_LEFT" ]; then
      if [ "$FREE_LEFT" -gt 0 ]; then
        ok "Free tier: ${FREE_LEFT} calls remaining"
      else
        warn "Free tier exhausted — USDC on Base required for paid commands"
      fi
    else
      ok "Status check ran (could not parse free calls)"
    fi
  fi
fi

# 6. Memory count
if command -v memoclaw &>/dev/null; then
  COUNT=$(memoclaw count 2>/dev/null | grep -oP '[0-9]+' | head -1 || echo "")
  if [ -n "$COUNT" ]; then
    ok "Memory store: ${COUNT} memories"
  fi
fi

echo
if [ "$ERRORS" -gt 0 ]; then
  echo -e "${RED}${ERRORS} issue(s) found. Fix them before using MemoClaw.${NC}"
  exit 1
else
  echo -e "${GREEN}All checks passed — ready to go!${NC}"
  exit 0
fi
