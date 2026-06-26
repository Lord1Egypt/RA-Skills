#!/bin/bash
# Claude Code Orchestrator — One-time setup
# Run this after installing the skill to verify everything works.
#
# Usage: setup.sh [--check-only]
#
# What it does:
#   1. Verifies claude CLI is installed and authenticated
#   2. Verifies python3 is available
#   3. Creates required temp directories
#   4. Runs a smoke test (dispatches a tiny task, polls, verifies)
#   5. Reports status

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHECK_ONLY="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ERRORS=0

default_runner_user=""
if [ "$(id -u)" = "0" ] && id ccbot >/dev/null 2>&1 && [ -d /home/ccbot ]; then
  default_runner_user="ccbot"
fi

export CLAUDE_RUNNER_USER="${CLAUDE_RUNNER_USER:-$default_runner_user}"
if [ -n "$CLAUDE_RUNNER_USER" ]; then
  export CLAUDE_RUNNER_HOME="${CLAUDE_RUNNER_HOME:-/home/$CLAUDE_RUNNER_USER}"
  export CLAUDE_BIN="${CLAUDE_BIN:-$CLAUDE_RUNNER_HOME/.local/bin/claude}"
else
  export CLAUDE_RUNNER_HOME="${CLAUDE_RUNNER_HOME:-$HOME}"
  export CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude 2>/dev/null || true)}"
fi
export CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-bypassPermissions}"
export CLAUDE_BACKEND="${CLAUDE_BACKEND:-cli}"
export CLAUDE_DELEGATE_PROFILES="${CLAUDE_DELEGATE_PROFILES:-${SCRIPT_DIR%/scripts}/profiles.json}"
export CLAUDE_DELEGATE_BOOTSTRAP="${CLAUDE_DELEGATE_BOOTSTRAP:-1}"
export CLAUDE_DELEGATE_DOC_BASENAME="${CLAUDE_DELEGATE_DOC_BASENAME:-CLAUDE.delegate.md}"
default_oauth_env="$HOME/.claude/.oauth-token.env"
if [ "$(id -u)" = "0" ] && [ -f /root/.claude/.oauth-token.env ]; then
  default_oauth_env="/root/.claude/.oauth-token.env"
fi
export CLAUDE_OAUTH_ENV_FILE="${CLAUDE_OAUTH_ENV_FILE:-$default_oauth_env}"

if [ -f "$CLAUDE_OAUTH_ENV_FILE" ]; then
  # shellcheck disable=SC1090
  . "$CLAUDE_OAUTH_ENV_FILE"
fi

build_runner_cmd() {
  local -a cmd
  if [ -n "${CLAUDE_RUNNER_USER:-}" ]; then
    cmd=(sudo -u "$CLAUDE_RUNNER_USER" -H env HOME="$CLAUDE_RUNNER_HOME")
  else
    cmd=(env HOME="$CLAUDE_RUNNER_HOME")
  fi
  if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    cmd+=(CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN")
  fi
  cmd+=("${CLAUDE_BIN:-claude}")
  RUNNER_CMD=("${cmd[@]}")
}

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }

echo "Claude Code Orchestrator — Setup Check"
echo "========================================"
echo ""

# 1. Check claude CLI
echo "Dependencies:"
if [ -x "$CLAUDE_BIN" ] || command -v claude &>/dev/null; then
  VERSION=$({ "$CLAUDE_BIN" --version 2>/dev/null || claude --version 2>&1; } | head -1)
  ok "claude CLI found: $VERSION"
else
  fail "claude CLI not found. Install: npm install -g @anthropic-ai/claude-code"
fi

# 2. Check python3
if command -v python3 &>/dev/null; then
  PY_VERSION=$(python3 --version 2>&1)
  ok "python3 found: $PY_VERSION"
else
  fail "python3 not found. Install python3."
fi

# 3. Check scripts exist and are executable
echo ""
echo "Scripts:"
for script in run-task.sh cc-orchestrator.sh; do
  if [ -f "$SCRIPT_DIR/$script" ]; then
    if [ -x "$SCRIPT_DIR/$script" ]; then
      ok "$script — present and executable"
    else
      warn "$script — present but not executable, fixing..."
      chmod +x "$SCRIPT_DIR/$script"
      ok "$script — fixed"
    fi
  else
    fail "$script — missing!"
  fi
done

# 4. Create temp directories
echo ""
echo "Directories:"
for dir in /tmp/claude-subagent-results /tmp/claude-subagent-registry /tmp/claude-subagent-logs; do
  mkdir -p "$dir" 2>/dev/null
  ok "$dir"
done

# 5. Check claude auth (quick test)
echo ""
echo "Authentication:"
if [ -x "$CLAUDE_BIN" ] || command -v claude &>/dev/null; then
  build_runner_cmd
  AUTH_TEST=$(timeout 30 "${RUNNER_CMD[@]}" --print "respond with only the word 'authenticated'" 2>&1 || true)
  if echo "$AUTH_TEST" | grep -qi "authenticated"; then
    ok "Claude Code authenticated and responding via runner"
  elif echo "$AUTH_TEST" | grep -qi "error\|unauthorized\|login\|expired"; then
    fail "Claude Code auth issue. Run 'claude' interactively to re-authenticate."
  else
    warn "Could not confirm auth (response: ${AUTH_TEST:0:100})"
  fi
fi

# 6. Smoke test (skip if --check-only)
if [ "$CHECK_ONLY" != "--check-only" ] && [ $ERRORS -eq 0 ]; then
  echo ""
  echo "Smoke Test:"
  
  RESULT=$("$SCRIPT_DIR/run-task.sh" run /tmp 0.10 haiku "Respond with exactly: SMOKE_TEST_PASS" 2>&1)
  
  if echo "$RESULT" | grep -q "SMOKE_TEST_PASS"; then
    COST=$(echo "$RESULT" | python3 -c "import json,sys; print(f'\${json.load(sys.stdin).get(\"cost_usd\",0):.4f}')" 2>/dev/null || echo "unknown")
    SESSION=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id','')[:12])" 2>/dev/null || echo "unknown")
    ok "Smoke test passed (cost: $COST, session: $SESSION...)"
  else
    fail "Smoke test failed. Output: ${RESULT:0:200}"
  fi
elif [ "$CHECK_ONLY" = "--check-only" ]; then
  echo ""
  echo "(Smoke test skipped — --check-only mode)"
fi

# Summary
echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
  ok "Setup complete! All checks passed."
  echo ""
  echo "Quick start:"
  echo "  $SCRIPT_DIR/cc-orchestrator.sh dispatch /tmp 0.50 sonnet my-first-task \"List all files in the current directory\""
else
  fail "$ERRORS check(s) failed. Fix the issues above and re-run."
  exit 1
fi
