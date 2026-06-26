#!/usr/bin/env bash
# openclaw-audit.sh — runtime-first audit before optimization.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/clawd}"
[[ -d "$WORKSPACE" ]] || WORKSPACE="$HOME/.openclaw/workspace-whatsapp"

SESSIONS="${OPENCLAW_SESSIONS:-$HOME/.openclaw/agents/main/sessions}"
[[ -d "$SESSIONS" ]] || SESSIONS="$HOME/.clawdbot/agents.main/sessions"

CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
APPROVALS="${OPENCLAW_APPROVALS:-$HOME/.openclaw/exec-approvals.json}"
EXTENSIONS_DIR="${OPENCLAW_EXTENSIONS:-$HOME/.openclaw/extensions}"

WORKSPACE_MAIN="${WORKSPACE_MAIN:-$HOME/clawd}"
WORKSPACE_WHATSAPP="${WORKSPACE_WHATSAPP:-$HOME/.openclaw/workspace-whatsapp}"

NEXT_STEP=1
DUPLICATE_GATEWAY=0
RESTART_RISK=0
WIRING_ISSUE=0
ALLOWLIST_ISSUE=0
PLUGIN_ISSUE=0
STALE_SESSION_RISK=0

section() {
  echo "=== $1 ==="
}

add_step() {
  echo "$NEXT_STEP) $1"
  NEXT_STEP=$((NEXT_STEP + 1))
}

prop() {
  local blob="$1"
  local key="$2"
  awk -F= -v key="$key" '$1 == key { print $2 }' <<<"$blob" | tail -n1
}

chars_or_zero() {
  local file="$1"
  if [[ -f "$file" ]]; then
    wc -c < "$file"
  else
    echo 0
  fi
}

print_workspace_file() {
  local file="$1"
  local path="$WORKSPACE/$file"
  if [[ -f "$path" ]]; then
    local chars
    chars=$(wc -c < "$path")
    local tokens=$((chars / 4))
    echo "  $file: ${chars} chars ≈ ${tokens} tokens"
  else
    echo "  $file: NOT FOUND"
  fi
}

resolve_openclaw_bin() {
  local candidate

  candidate="$(command -v openclaw 2>/dev/null || true)"
  if [[ -n "$candidate" ]]; then
    echo "$candidate"
    return
  fi

  for candidate in \
    "$HOME/.nvm/current/bin/openclaw" \
    "$HOME/.local/bin/openclaw" \
    "/usr/local/bin/openclaw" \
    "/usr/bin/openclaw"
  do
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return
    fi
  done

  for candidate in "$HOME"/.nvm/versions/node/*/bin/openclaw; do
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return
    fi
  done

  find "$HOME/.nvm/versions/node" -path '*/bin/openclaw' \( -type f -o -type l \) 2>/dev/null | sort | tail -n1
}

section "Runtime health"

USER_GATEWAY_SHOW="$(systemctl --user show openclaw-gateway.service -p LoadState -p ActiveState -p SubState 2>/dev/null || true)"
SYSTEM_GATEWAY_SHOW="$(systemctl show clawdbot.service -p LoadState -p ActiveState -p SubState -p NRestarts 2>/dev/null || true)"

UG_LOAD="$(prop "$USER_GATEWAY_SHOW" LoadState)"
UG_ACTIVE="$(prop "$USER_GATEWAY_SHOW" ActiveState)"
UG_SUB="$(prop "$USER_GATEWAY_SHOW" SubState)"

SG_LOAD="$(prop "$SYSTEM_GATEWAY_SHOW" LoadState)"
SG_ACTIVE="$(prop "$SYSTEM_GATEWAY_SHOW" ActiveState)"
SG_SUB="$(prop "$SYSTEM_GATEWAY_SHOW" SubState)"
SG_RESTARTS="$(prop "$SYSTEM_GATEWAY_SHOW" NRestarts)"
[[ -n "$SG_RESTARTS" ]] || SG_RESTARTS=0

PORT_18789="$(ss -ltn 2>/dev/null | awk '$4 ~ /:18789$/ { print $4 }' | head -n1 || true)"

echo "  user gateway: ${UG_LOAD:-unknown}/${UG_ACTIVE:-unknown}/${UG_SUB:-unknown}"
echo "  clawdbot.service: ${SG_LOAD:-unknown}/${SG_ACTIVE:-unknown}/${SG_SUB:-unknown} restarts=${SG_RESTARTS}"
echo "  listener 18789: ${PORT_18789:-not-listening}"

if [[ "$UG_ACTIVE" = "active" && "$SG_ACTIVE" = "active" ]]; then
  DUPLICATE_GATEWAY=1
  echo "  duplicate supervisor risk: YES"
else
  echo "  duplicate supervisor risk: no"
fi

if [[ "$SG_ACTIVE" = "failed" || "$SG_SUB" = "auto-restart" || "$SG_RESTARTS" -gt 0 ]]; then
  RESTART_RISK=1
  echo "  restart-loop risk: YES"
else
  echo "  restart-loop risk: no"
fi

echo ""
section "OpenClaw binary and update status"

OPENCLAW_BIN="$(resolve_openclaw_bin)"
if [[ -n "$OPENCLAW_BIN" ]]; then
  OPENCLAW_BIN_REAL="$(readlink -f "$OPENCLAW_BIN" 2>/dev/null || echo "$OPENCLAW_BIN")"
else
  OPENCLAW_BIN_REAL=""
fi
OPENCLAW_APPROVAL_TARGET="${OPENCLAW_BIN:-}"

if [[ -n "$OPENCLAW_BIN_REAL" ]]; then
  UPDATE_STATUS="$("$OPENCLAW_BIN_REAL" update status 2>/dev/null || true)"
else
  UPDATE_STATUS=""
fi
INSTALL_TYPE="$(grep -i '^Install:' <<<"$UPDATE_STATUS" | sed 's/^[^:]*:[[:space:]]*//' || true)"
CHANNEL="$(grep -i '^Channel:' <<<"$UPDATE_STATUS" | sed 's/^[^:]*:[[:space:]]*//' || true)"
UPDATE_AVAILABLE="$(grep -i '^Update available:' <<<"$UPDATE_STATUS" | sed 's/^[^:]*:[[:space:]]*//' || true)"

echo "  openclaw in PATH: ${OPENCLAW_BIN:-not-found}"
echo "  resolved binary: ${OPENCLAW_BIN_REAL:-not-found}"
echo "  install type: ${INSTALL_TYPE:-unknown}"
echo "  channel: ${CHANNEL:-unknown}"
echo "  update available: ${UPDATE_AVAILABLE:-unknown}"

echo ""
section "Workspace command wiring"

CURRENT_AUDIT_PATH="$SKILL_DIR/scripts/openclaw-audit.sh"
CURRENT_PREFLIGHT_PATH="$SKILL_DIR/scripts/preflight.sh"
CURRENT_PURGE_PATH="$SKILL_DIR/scripts/purge-stale-sessions.sh"

check_workspace_file() {
  local file="$1"
  local legacy=0
  local current=0

  if [[ ! -f "$file" ]]; then
    echo "  $(basename "$file"): missing"
    return
  fi

  if grep -Fq "/clawd/skills/public/inference-optimizer" "$file" || \
     grep -Fq "~/clawdbot/code/scripts/openclaw-audit.sh" "$file" || \
     grep -Fq "~/clawdbot/code/scripts/purge-stale-sessions.sh" "$file"; then
    legacy=1
  fi

  if grep -Fq "$CURRENT_AUDIT_PATH" "$file" || grep -Fq "$CURRENT_PREFLIGHT_PATH" "$file"; then
    current=1
  fi

  if [[ $legacy -eq 1 ]]; then
    WIRING_ISSUE=1
    echo "  $(basename "$file"): legacy path wiring detected"
  elif [[ $current -eq 1 ]]; then
    echo "  $(basename "$file"): current skill wiring detected"
  else
    echo "  $(basename "$file"): no managed skill wiring detected"
  fi
}

check_workspace_file "$WORKSPACE_MAIN/AGENTS.md"
check_workspace_file "$WORKSPACE_MAIN/TOOLS.md"
check_workspace_file "$WORKSPACE_WHATSAPP/AGENTS.md"
check_workspace_file "$WORKSPACE_WHATSAPP/TOOLS.md"

echo ""
section "Allowlist coverage"

if [[ -f "$APPROVALS" && -n "$OPENCLAW_APPROVAL_TARGET" ]]; then
  NVM_WILDCARD_PATH="$(sed -E 's#/versions/node/[^/]+/#/versions/node/*/#' <<<"$OPENCLAW_APPROVAL_TARGET")"
  EXACT_ALLOWLIST=0
  WILDCARD_ALLOWLIST=0
  BASENAME_ONLY=0

  grep -Fq "$OPENCLAW_APPROVAL_TARGET" "$APPROVALS" && EXACT_ALLOWLIST=1
  grep -Fq "$NVM_WILDCARD_PATH" "$APPROVALS" && WILDCARD_ALLOWLIST=1
  grep -Fq '"openclaw"' "$APPROVALS" && BASENAME_ONLY=1

  echo "  approvals file: $APPROVALS"
  echo "  approval target path: $OPENCLAW_APPROVAL_TARGET"
  echo "  exact path covered: $([[ $EXACT_ALLOWLIST -eq 1 ]] && echo yes || echo no)"
  echo "  bounded NVM wildcard covered: $([[ $WILDCARD_ALLOWLIST -eq 1 ]] && echo yes || echo no)"
  echo "  basename-only entry present: $([[ $BASENAME_ONLY -eq 1 ]] && echo yes || echo no)"

  if [[ $EXACT_ALLOWLIST -eq 0 && $WILDCARD_ALLOWLIST -eq 0 ]]; then
    ALLOWLIST_ISSUE=1
    echo "  allowlist coverage for resolved binary: MISSING"
  else
    echo "  allowlist coverage for resolved binary: OK"
  fi
else
  echo "  approvals file or openclaw executable path not available"
fi

echo ""
section "Plugins and local extensions"

PROVENANCE_WARNINGS="$(journalctl --user -u openclaw-gateway.service -n 200 --no-pager 2>/dev/null | grep -F 'loaded without install/load-path provenance' || true)"
if [[ -d "$EXTENSIONS_DIR" ]]; then
  while IFS= read -r ext; do
    [[ -n "$ext" ]] || continue
    if grep -Fq "$ext" "$CONFIG" 2>/dev/null; then
      echo "  $ext: local extension present and referenced in config"
    else
      echo "  $ext: local extension present but not referenced in config"
      PLUGIN_ISSUE=1
    fi
  done < <(find "$EXTENSIONS_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort)
else
  echo "  local extensions: none"
fi

if [[ -n "$PROVENANCE_WARNINGS" ]]; then
  PLUGIN_ISSUE=1
  echo "  provenance warnings in recent gateway logs: YES"
else
  echo "  provenance warnings in recent gateway logs: no"
fi

echo ""
section "Workspace file sizes (chars -> ~tokens)"
for f in SOUL.md AGENTS.md TOOLS.md MEMORY.md USER.md HEARTBEAT.md; do
  print_workspace_file "$f"
done

echo ""
section "Daily memory files"
while read -r f; do
  [[ -n "$f" ]] || continue
  chars=$(wc -c < "$f")
  tokens=$((chars / 4))
  echo "  $(basename "$f"): ${chars} chars ≈ ${tokens} tokens"
done < <(find "$WORKSPACE/memory" -name "*.md" 2>/dev/null | sort)

echo ""
section "Session files (stale overhead)"
SESSION_COUNT=$(find "$SESSIONS" -name "*.jsonl" 2>/dev/null | wc -l)
SESSION_SIZE=$(du -sh "$SESSIONS" 2>/dev/null | cut -f1)
OLD_COUNT=$(find "$SESSIONS" -name "*.jsonl" -mtime +1 2>/dev/null | wc -l)
[[ -n "$SESSION_SIZE" ]] || SESSION_SIZE="0"
echo "  total sessions: $SESSION_COUNT ($SESSION_SIZE)"
echo "  sessions > 24h old: $OLD_COUNT"
if [[ "$OLD_COUNT" -gt 0 ]]; then
  STALE_SESSION_RISK=1
fi

echo ""
section "Config file"
CONFIG_CHARS=$(chars_or_zero "$CONFIG")
echo "  openclaw.json: ${CONFIG_CHARS} chars"

echo ""
section "Estimated total system prompt tokens per request"
TOTAL_TOKENS=0
for f in SOUL.md AGENTS.md TOOLS.md MEMORY.md USER.md HEARTBEAT.md; do
  fp="$WORKSPACE/$f"
  [[ -f "$fp" ]] && TOTAL_TOKENS=$((TOTAL_TOKENS + $(wc -c < "$fp") / 4))
done
echo "  workspace files: ~${TOTAL_TOKENS} tokens"
echo "  OpenClaw base system prompt: ~8000-15000 tokens (fixed overhead)"
echo "  tools/skills schema: ~500-2000 tokens (varies by enabled skills)"
echo "  -------"
echo "  estimated cold request total: ~$((TOTAL_TOKENS + 10000)) tokens"

echo ""
section "Recommended next steps"

if [[ $DUPLICATE_GATEWAY -eq 1 ]]; then
  add_step "Keep a single gateway supervisor. On this VPS, keep openclaw-gateway.service active, keep clawdbot.service disabled, and preserve secret injection in the user service."
fi

if [[ $RESTART_RISK -eq 1 ]]; then
  add_step "Inspect service logs before tuning models: journalctl or systemctl show indicates restart-loop risk."
fi

if [[ $WIRING_ISSUE -eq 1 ]]; then
  add_step "Repair workspace command wiring with: bash $SKILL_DIR/scripts/setup.sh --apply"
fi

if [[ $ALLOWLIST_ISSUE -eq 1 ]]; then
  add_step "Add the resolved openclaw binary path or a bounded NVM wildcard to exec approvals instead of relying on basename-only allowlist entries."
fi

if [[ -n "$UPDATE_AVAILABLE" && "$UPDATE_AVAILABLE" != "unknown" && "$UPDATE_AVAILABLE" != "none" && "$UPDATE_AVAILABLE" != "false" ]]; then
  add_step "A newer OpenClaw build is available. Run openclaw update only after command wiring and allowlist coverage are correct."
fi

if [[ $PLUGIN_ISSUE -eq 1 ]]; then
  add_step "Review local extensions and provenance warnings. Remove unused extensions or pin trust for the ones that are intentional."
fi

if [[ $STALE_SESSION_RISK -eq 1 ]]; then
  add_step "Archive stale sessions with bash $SKILL_DIR/scripts/purge-stale-sessions.sh before changing pruning or concurrency settings."
fi

if [[ $NEXT_STEP -eq 1 ]]; then
  add_step "No blocking runtime issue detected. The next highest-value action is token and session cleanup, then inference tuning."
fi
