#!/usr/bin/env bash
# Verify inference-optimizer installation, wiring, and audit coverage.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_MAIN="${WORKSPACE_MAIN:-$HOME/clawd}"
WORKSPACE_WHATSAPP="${WORKSPACE_WHATSAPP:-$HOME/.openclaw/workspace-whatsapp}"
APPROVALS_FILE="${APPROVALS_FILE:-$HOME/.openclaw/exec-approvals.json}"

PASS=0
FAIL=0

check() {
  if eval "$1"; then
    echo "[OK] $2"
    ((PASS++)) || true
    return 0
  else
    echo "[FAIL] $2"
    ((FAIL++)) || true
    return 1
  fi
}

check_workspace_file() {
  local file="$1"
  local label="$2"
  local legacy=false
  local current=false

  if [[ ! -f "$file" ]]; then
    echo "[SKIP] $label missing"
    return 0
  fi

  grep -Fq "/clawd/skills/public/inference-optimizer" "$file" && legacy=true
  grep -Fq "~/clawdbot/code/scripts/openclaw-audit.sh" "$file" && legacy=true
  grep -Fq "~/clawdbot/code/scripts/purge-stale-sessions.sh" "$file" && legacy=true

  if grep -Fq "$SKILL_DIR/scripts/openclaw-audit.sh" "$file" || grep -Fq "$SKILL_DIR/scripts/preflight.sh" "$file"; then
    current=true
  fi

  if [[ "$legacy" = true ]]; then
    echo "[FAIL] $label has legacy inference-optimizer paths"
    ((FAIL++)) || true
  elif [[ "$current" = true ]]; then
    echo "[OK] $label references current skill path"
    ((PASS++)) || true
  else
    echo "[WARN] $label has no current managed skill wiring"
  fi
}

check_approval_patterns() {
  local agent="$1"
  shift

  if [[ ! -f "$APPROVALS_FILE" ]]; then
    echo "[FAIL] approvals file missing: $APPROVALS_FILE"
    ((FAIL++)) || true
    return 1
  fi

  local missing=0
  for pattern in "$@"; do
    if python3 - "$APPROVALS_FILE" "$agent" "$pattern" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
agent = sys.argv[2]
pattern = sys.argv[3]
data = json.loads(path.read_text())
allowlist = data.get("agents", {}).get(agent, {}).get("allowlist", [])
found = any(entry.get("pattern") == pattern for entry in allowlist)
raise SystemExit(0 if found else 1)
PY
    then
      echo "[OK] $agent allowlist covers $pattern"
      ((PASS++)) || true
    else
      echo "[FAIL] $agent allowlist missing $pattern"
      ((FAIL++)) || true
      missing=1
    fi
  done

  return "$missing"
}

echo "=== inference-optimizer verify ==="
echo ""

check "[[ -f $SKILL_DIR/optimization-agent.md ]]" "optimization-agent.md exists"
check "[[ -f $SKILL_DIR/scripts/openclaw-audit.sh ]]" "openclaw-audit.sh exists"
check "[[ -x $SKILL_DIR/scripts/openclaw-audit.sh ]]" "openclaw-audit.sh executable"
check "[[ -f $SKILL_DIR/scripts/purge-stale-sessions.sh ]]" "purge-stale-sessions.sh exists"
check "[[ -x $SKILL_DIR/scripts/purge-stale-sessions.sh ]]" "purge-stale-sessions.sh executable"
check "[[ -f $SKILL_DIR/scripts/preflight.sh ]]" "preflight.sh exists"
check "[[ -x $SKILL_DIR/scripts/preflight.sh ]]" "preflight.sh executable"
check "[[ -f $SKILL_DIR/SKILL.md ]]" "SKILL.md exists"

SETUP_PREVIEW="$(bash "$SKILL_DIR/scripts/setup.sh" 2>/dev/null || true)"
if grep -Fq "$SKILL_DIR/scripts/preflight.sh" <<<"$SETUP_PREVIEW" && grep -Fq "$SKILL_DIR/scripts/openclaw-audit.sh" <<<"$SETUP_PREVIEW"; then
  echo "[OK] setup preview uses current skill path"
  ((PASS++)) || true
else
  echo "[FAIL] setup preview does not use current skill path"
  ((FAIL++)) || true
fi

AUDIT_OUTPUT="$("$SKILL_DIR/scripts/openclaw-audit.sh" 2>/dev/null || true)"
if grep -Fq "=== Runtime health ===" <<<"$AUDIT_OUTPUT"; then
  echo "[OK] audit reports runtime health"
  ((PASS++)) || true
else
  echo "[FAIL] audit missing runtime health section"
  ((FAIL++)) || true
fi

if grep -Fq "=== Workspace command wiring ===" <<<"$AUDIT_OUTPUT"; then
  echo "[OK] audit checks workspace command wiring"
  ((PASS++)) || true
else
  echo "[FAIL] audit missing workspace command wiring section"
  ((FAIL++)) || true
fi

if grep -Fq "=== Recommended next steps ===" <<<"$AUDIT_OUTPUT"; then
  echo "[OK] audit emits recommended next steps"
  ((PASS++)) || true
else
  echo "[FAIL] audit missing recommended next steps"
  ((FAIL++)) || true
fi

check_workspace_file "$WORKSPACE_MAIN/AGENTS.md" "main AGENTS.md"
check_workspace_file "$WORKSPACE_MAIN/TOOLS.md" "main TOOLS.md"
check_workspace_file "$WORKSPACE_WHATSAPP/AGENTS.md" "whatsapp AGENTS.md"
check_workspace_file "$WORKSPACE_WHATSAPP/TOOLS.md" "whatsapp TOOLS.md"

APPROVAL_PATTERNS=(
  "$SKILL_DIR/scripts/openclaw-audit.sh"
  "$SKILL_DIR/scripts/preflight.sh"
  "$SKILL_DIR/scripts/purge-stale-sessions.sh"
  "$SKILL_DIR/scripts/setup.sh"
  "$SKILL_DIR/scripts/verify.sh"
)

for agent in main whatsapp; do
  check_approval_patterns "$agent" "${APPROVAL_PATTERNS[@]}"
done

echo ""
echo "---"
echo "Pass: $PASS  Fail: $FAIL"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
