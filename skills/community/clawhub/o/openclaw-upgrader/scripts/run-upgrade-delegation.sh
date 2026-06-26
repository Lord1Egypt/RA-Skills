#!/usr/bin/env bash
set -euo pipefail

# run-upgrade-delegation.sh — outer runner for the openclaw-upgrader skill.
#
# Responsibilities:
#   1. Call collect-upgrade-context.sh which claims the host-level active-run lock
#   2. Hold that lock for the ENTIRE upgrader lifecycle
#   3. Execute delegated upgrade via the selected agent
#   4. Release the lock ONLY when the run reaches a terminal state
#
# Terminal states: success, failed, already_latest, delegation_blocked, rejected_reentry
# The lock must NOT be released at any intermediate point.

TARGET_VERSION="${1:-latest}"
RESULT_JSON="${2:-$HOME/.openclaw/.upgrade-result.json}"
CONTEXT_JSON="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTOR="$SCRIPT_DIR/collect-upgrade-context.sh"
LOCK_DIR="${OPENCLAW_UPGRADER_LOCK_DIR:-$HOME/.openclaw/openclaw-upgrader.lock}"
LOCK_INFO_FILE="$LOCK_DIR/run.json"

mkdir -p "$(dirname "$RESULT_JSON")"

json_escape() {
  python3 - <<'PY' "$1"
import json,sys
print(json.dumps(sys.argv[1]))
PY
}

release_lock() {
  rm -f "$LOCK_INFO_FILE" >/dev/null 2>&1 || true
  rmdir "$LOCK_DIR" >/dev/null 2>&1 || true
}

write_terminal_result() {
  local status="$1"
  local extra="${2:-}"

  # Build a full result aligned with SKILL.md schema by pulling fields
  # from context JSON when available.
  python3 - <<PY "$status" "$CONTEXT_JSON" "$RESULT_JSON" "$TARGET_VERSION" "$LOCK_DIR" "$extra"
import json, sys, os, datetime

status = sys.argv[1]
ctx_path = sys.argv[2]
result_path = sys.argv[3]
target_version = sys.argv[4]
lock_dir = sys.argv[5]
extra_json_fragment = sys.argv[6]

ctx = {}
if ctx_path and os.path.isfile(ctx_path):
    try:
        ctx = json.load(open(ctx_path))
    except Exception:
        pass

result = {
    "status": status,
    "start_time": ctx.get("started_at", None),
    "end_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "previous_version": ctx.get("current_version", "unknown"),
    "new_version": None,
    "target_version": target_version,
    "selected_agent": ctx.get("selected_agent", "none"),
    "delegation_status": ctx.get("delegation_status", "unknown"),
    "delegation_block_reason": ctx.get("delegation_block_reason", None),
    "agent_checks": ctx.get("agent_checks", {
        "codex": {"installed": False, "authenticated": False, "preflight_ok": False},
        "claude_code": {"installed": False, "authenticated": False, "preflight_ok": False}
    }),
    "service_definition_status": "not_started",
    "service_status": "unknown",
    "endpoint_status": "unknown",
    "auth_probe_status": "unknown",
    "service_model": ctx.get("service_model", "unknown"),
    "instance_identity": {
        "config_path": ctx.get("config_path", "unknown"),
        "state_dir": ctx.get("state_dir", "unknown"),
        "profile": ctx.get("profile", "unknown"),
        "service_name": ctx.get("service_identity", "unknown"),
        "endpoint": ctx.get("known_endpoint", "unknown")
    },
    "repair_actions": [],
    "error": None,
    "log_file": None,
    "context_path": ctx_path,
    "run_lock_path": lock_dir
}

# Merge extra fields from the JSON fragment string
if extra_json_fragment:
    try:
        extra_obj = json.loads("{" + extra_json_fragment + "}")
        result.update(extra_obj)
    except Exception:
        pass

json.dump(result, open(result_path, "w"), indent=2)
PY
}

# Always release lock on exit. This is the safety net: no matter how the
# script terminates (success, error, signal), the lock is freed.
# Individual terminal paths also call release_lock explicitly for clarity,
# but this trap guarantees it even on unexpected exits.
trap release_lock EXIT

# --- Phase 1: Context collection (also claims the lock) ---

if [[ -z "$CONTEXT_JSON" ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  CONTEXT_JSON="$HOME/.openclaw/upgrade-context-$TS.json"
fi

"$COLLECTOR" "$TARGET_VERSION" "$CONTEXT_JSON" >/dev/null

if [[ ! -f "$CONTEXT_JSON" ]]; then
  write_terminal_result "failed" '"error": "Context collection did not produce a context file"'
  release_lock
  exit 1
fi

# --- Phase 2: Evaluate context ---

read_field() {
  python3 - <<PY "$CONTEXT_JSON" "$1"
import json,sys
obj=json.load(open(sys.argv[1]))
print(obj.get(sys.argv[2],'unknown'))
PY
}

DELEGATION_STATUS="$(read_field delegation_status)"
SELECTED_AGENT="$(read_field selected_agent)"
DELEGATION_BLOCK_REASON="$(read_field delegation_block_reason)"

# Rejected re-entry: the lock belongs to another run; we never held it,
# so we must NOT release it. Remove the EXIT trap.
if [[ "$DELEGATION_STATUS" == "rejected_reentry" ]]; then
  trap - EXIT
  write_terminal_result "rejected_reentry" \
    '"delegation_status": "rejected_reentry", "delegation_block_reason": "active_run_exists"'
  exit 0
fi

# Delegation blocked: we hold the lock but cannot proceed.
if [[ "$SELECTED_AGENT" == "none" ]]; then
  write_terminal_result "delegation_blocked" \
    "\"delegation_status\": \"blocked\", \"delegation_block_reason\": $(json_escape "$DELEGATION_BLOCK_REASON"), \"selected_agent\": \"none\""
  release_lock
  exit 0
fi

# --- Phase 3: Execute delegated upgrade ---
# The lock is held from here through the entire delegated run.
# Update lock info to reflect we are now in delegation phase.

cat > "$LOCK_INFO_FILE" <<JSON
{
  "run_id": $(json_escape "$(read_field run_id)"),
  "pid": $$,
  "started_at": $(json_escape "$(date -u +%Y-%m-%dT%H:%M:%SZ)"),
  "target_version": $(json_escape "$TARGET_VERSION"),
  "holder": "run-upgrade-delegation.sh",
  "phase": "delegating",
  "selected_agent": $(json_escape "$SELECTED_AGENT")
}
JSON

# Write in_progress so external observers can see delegation is active.
cat > "$RESULT_JSON" <<JSON
{
  "status": "in_progress",
  "target_version": $(json_escape "$TARGET_VERSION"),
  "delegation_status": "started",
  "selected_agent": $(json_escape "$SELECTED_AGENT"),
  "context_path": $(json_escape "$CONTEXT_JSON"),
  "run_lock_path": $(json_escape "$LOCK_DIR")
}
JSON

# ---- Delegation execution hook ----
# The caller (OpenClaw agent) is expected to:
#   1. Read $RESULT_JSON and $CONTEXT_JSON
#   2. Formulate the delegated-agent prompt per SKILL.md
#   3. Spawn the selected agent (codex / claude-code)
#   4. Wait for the delegated agent to finish
#   5. Write the final terminal result to $RESULT_JSON
#   6. Call: rmdir "$LOCK_DIR" (or let this script's EXIT trap handle it)
#
# For scripted / non-interactive delegation, insert the execution logic below.
# The lock remains held until this script exits (EXIT trap) or the caller
# explicitly releases it.
#
# Placeholder: if no delegation logic is wired in, we report failed so the
# lock is released and the caller knows delegation was not actually executed.

if [[ "${OPENCLAW_UPGRADER_DELEGATE_CMD:-}" != "" ]]; then
  # External delegation command provided — run it.
  # The command receives: TARGET_VERSION CONTEXT_JSON RESULT_JSON
  # It must write the final result to RESULT_JSON before returning.
  # Lock release happens via EXIT trap after it returns.
  if "$OPENCLAW_UPGRADER_DELEGATE_CMD" "$TARGET_VERSION" "$CONTEXT_JSON" "$RESULT_JSON"; then
    # Delegation command succeeded; trust it wrote the result.
    # Lock released by EXIT trap.
    exit 0
  else
    DELEGATE_EXIT=$?
    # Check if the delegate at least wrote a result.
    if [[ -f "$RESULT_JSON" ]]; then
      FINAL_STATUS="$(python3 -c "import json; print(json.load(open('$RESULT_JSON')).get('status','unknown'))")"
      if [[ "$FINAL_STATUS" == "success" || "$FINAL_STATUS" == "failed" || "$FINAL_STATUS" == "already_latest" ]]; then
        exit "$DELEGATE_EXIT"
      fi
    fi
    write_terminal_result "failed" \
      "\"error\": \"Delegation command exited with code $DELEGATE_EXIT\", \"selected_agent\": $(json_escape "$SELECTED_AGENT")"
    exit 1
  fi
fi

# No delegation command wired — report that delegation is ready but was not
# executed by this script. The caller (OpenClaw agent) should handle delegation
# itself after reading this result.
# Lock remains held. The caller MUST release it when done.
# We remove the EXIT trap so the lock survives this script's exit.
trap - EXIT

cat > "$RESULT_JSON" <<JSON
{
  "status": "in_progress",
  "target_version": $(json_escape "$TARGET_VERSION"),
  "delegation_status": "started",
  "selected_agent": $(json_escape "$SELECTED_AGENT"),
  "context_path": $(json_escape "$CONTEXT_JSON"),
  "run_lock_path": $(json_escape "$LOCK_DIR"),
  "note": "Lock held. Caller must execute delegation and release lock on terminal state."
}
JSON
