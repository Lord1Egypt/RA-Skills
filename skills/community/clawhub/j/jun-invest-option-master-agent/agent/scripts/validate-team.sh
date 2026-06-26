#!/usr/bin/env bash
set -euo pipefail

# Gate A: validate the internal team structure is consistent and complete.
# This script is intended to run inside the runtime workspace (source of truth).

WORKSPACE_DIR="${1:-/Users/lijunsheng/.openclaw/workspace-jun-invest-option-master-agent}"
cd "${WORKSPACE_DIR}" || { echo "FAIL: workspace not found: ${WORKSPACE_DIR}" >&2; exit 1; }

CFG="config/agents.yaml"
[[ -f "$CFG" ]] || { echo "FAIL: missing $CFG" >&2; exit 1; }

# Expected internal roles (must exist in config and in invest_agent/prompts)
roles=(PM Data Regime EquityAlpha Options Portfolio Risk Execution Postmortem Growth)

missing=0

echo "Validate roles in $CFG ..."
for r in "${roles[@]}"; do
  if ! grep -Eq "^[[:space:]]+${r}:[[:space:]]*$" "$CFG"; then
    echo "FAIL: missing role in $CFG: $r" >&2
    missing=1
  fi
  if [[ ! -f "invest_agent/prompts/${r}.md" ]]; then
    echo "FAIL: missing prompt invest_agent/prompts/${r}.md" >&2
    missing=1
  fi
  # top-level prompts are optional for Growth, but required for core pipeline roles
  if [[ "$r" != "Growth" ]]; then
    if [[ ! -f "prompts/${r}.md" ]]; then
      echo "FAIL: missing prompt prompts/${r}.md" >&2
      missing=1
    fi
  fi

done

# Ensure PM prompt includes the no-roster-talk and CSP/CC-only constraints
PM_PROMPT="invest_agent/prompts/PM.md"
if ! grep -q "禁止.*roster" "$PM_PROMPT"; then
  echo "FAIL: PM prompt missing 'no roster talk' constraint" >&2
  missing=1
fi
if ! grep -Eq "只提供 CSP/CC|只给 CSP/CC" "$PM_PROMPT"; then
  echo "FAIL: PM prompt missing 'CSP/CC only' entry constraint" >&2
  missing=1
fi

# It's OK for PM prompt to *mention* disallowed strategies in a negative/forbidden context.
# We only enforce that PM prompt explicitly restricts user-facing entry options to CSP/CC above.

[[ $missing -eq 0 ]] || exit 1

echo "OK: team structure validated"
