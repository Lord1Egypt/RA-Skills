#!/usr/bin/env bash
set -euo pipefail

GUARD_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUDIT_SH="$GUARD_DIR/scripts/audit.sh"
POLICY="$GUARD_DIR/policy/core-policy.yaml"
RULES_DIR="$GUARD_DIR/rules/active"

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

# ── Risk assessment ──────────────────────────────────

# Dangerous binaries that indicate network or system-level access
NETWORK_BINS="curl wget nc ncat socat telnet ssh scp rsync ftp"
# Interpreters that can make runtime network calls or execute arbitrary code
DYNAMIC_EXEC_BINS="python python3 perl ruby node deno bun"
# chmod on own data files is safe; only flag chmod with dangerous targets
SYSTEM_BINS_CRITICAL="mkfs dd mount umount"
SYSTEM_BINS_CONTEXTUAL="rm kill pkill"
SECRET_PATTERNS="(token|key|password|secret|credential|api[_-]?key|private[_-]?key|auth|bearer)"
# Patterns indicating dynamic execution or network evasion techniques
DYNAMIC_EXEC_PATTERNS='(/dev/tcp|/dev/udp|base64 -d|base64 --decode|eval |exec [0-9]|xargs sh|sh -c|bash -c|source /dev|openssl s_client|\bpowercat\b)'

classify_risk(){
  local script="$1"; shift
  local args="$*"
  local risk="low"
  local reasons=""

  # Check: network binaries in script
  if [[ -f "$script" ]]; then
    for bin in $NETWORK_BINS; do
      if grep -qw "$bin" "$script" 2>/dev/null; then
        risk="critical"
        reasons="${reasons}script contains network binary '$bin'; "
      fi
    done

    # Check: critical system binaries
    for bin in $SYSTEM_BINS_CRITICAL; do
      if grep -qw "$bin" "$script" 2>/dev/null; then
        risk="critical"
        reasons="${reasons}script contains critical system binary '$bin'; "
      fi
    done

    # Check: contextual system binaries (only flag if used with broad targets)
    for bin in $SYSTEM_BINS_CONTEXTUAL; do
      if grep -qE "$bin\s+(-rf|/)" "$script" 2>/dev/null; then
        if [[ "$risk" != "critical" ]]; then risk="high"; fi
        reasons="${reasons}script uses '$bin' with broad target; "
      fi
    done

    # Check: dynamic code execution interpreters (can bypass static network checks)
    for bin in $DYNAMIC_EXEC_BINS; do
      if grep -qE "\b${bin}\b\s+(-[ce]|--eval)" "$script" 2>/dev/null; then
        risk="critical"
        reasons="${reasons}script uses '$bin' with inline code execution; "
      fi
    done

    # Check: evasion techniques (/dev/tcp, base64 decode, eval, sh -c, etc.)
    if grep -qE "$DYNAMIC_EXEC_PATTERNS" "$script" 2>/dev/null; then
      risk="critical"
      reasons="${reasons}script contains dynamic execution or network evasion pattern; "
    fi
  fi

  # Check: command is a delete/remove operation
  if echo "$args" | grep -qiE '(delete|remove|rm |drop)'; then
    if [[ "$risk" == "low" ]]; then risk="medium"; fi
    reasons="${reasons}destructive operation detected; "
  fi

  # Check: path escapes skill directory
  if echo "$args" | grep -qE '(\.\.\/|\/etc\/|\/usr\/|\/var\/|\/tmp\/|~\/)'; then
    risk="high"
    reasons="${reasons}path may escape skill directory; "
  fi

  # Check: secrets in arguments
  if echo "$args" | grep -qiE "$SECRET_PATTERNS"; then
    risk="critical"
    reasons="${reasons}possible secret in arguments; "
  fi

  # Check: pipe to remote or command substitution with network
  if echo "$args" | grep -qE '(\| *(curl|wget|nc)|`(curl|wget|nc)|\$\((curl|wget|nc))'; then
    risk="critical"
    reasons="${reasons}pipe to network command; "
  fi

  # Check: dynamic execution in arguments (sh -c, python -c, eval, base64 decode)
  if echo "$args" | grep -qE '(sh -c|bash -c|python[3]? -c|eval |base64 -d|/dev/tcp)'; then
    risk="critical"
    reasons="${reasons}dynamic execution in arguments; "
  fi

  # Check active rules for additional patterns
  if [[ -d "$RULES_DIR" ]]; then
    for rule_file in "$RULES_DIR"/*.rule; do
      [[ -f "$rule_file" ]] || continue
      local pattern level
      pattern=$(head -1 "$rule_file")
      level=$(sed -n '2p' "$rule_file")
      if echo "$args" | grep -qE "$pattern" 2>/dev/null; then
        case "$level" in
          critical) risk="critical" ;;
          high) [[ "$risk" != "critical" ]] && risk="high" ;;
          medium) [[ "$risk" == "low" ]] && risk="medium" ;;
        esac
        reasons="${reasons}matched rule $(basename "$rule_file"); "
      fi
    done
  fi

  [[ -z "$reasons" ]] && reasons="no risk indicators found"
  echo "$risk|$reasons"
}

# ── Approval decision ────────────────────────────────

decide_action(){
  local risk="$1"
  case "$risk" in
    low)      echo "allow" ;;
    medium)   echo "allow" ;;
    high)     echo "prompt" ;;
    critical) echo "block" ;;
  esac
}

# ── Extract skill name from script path ──────────────

extract_skill_name(){
  local script_path="$1"
  # Try to find the skill directory (parent of scripts/)
  local dir
  dir=$(dirname "$script_path")
  if [[ "$(basename "$dir")" == "scripts" ]]; then
    basename "$(dirname "$dir")"
  else
    basename "$dir"
  fi
}

# ── Main: guard-exec ─────────────────────────────────

cmd_exec(){
  require_jq
  local script="" dry_run=false
  local -a pass_args=()

  # First arg is the script to execute, rest are its arguments
  if [[ $# -lt 1 ]]; then
    echo "usage: guard-exec.sh exec <script> [args...]" >&2
    exit 1
  fi

  script="$1"; shift
  pass_args=("$@")

  # Resolve script path
  if [[ ! -f "$script" ]]; then
    echo "error: script not found: $script" >&2
    exit 1
  fi

  local skill_name args_str
  skill_name=$(extract_skill_name "$script")
  args_str="${pass_args[*]:-}"

  # Risk assessment
  local risk_result risk reasons
  risk_result=$(classify_risk "$script" "$args_str")
  risk=$(echo "$risk_result" | cut -d'|' -f1)
  reasons=$(echo "$risk_result" | cut -d'|' -f2)

  # Decision
  local decision
  decision=$(decide_action "$risk")

  case "$decision" in
    allow)
      # L1: execute directly
      local output exit_code=0
      output=$(bash "$script" "${pass_args[@]}" 2>&1) || exit_code=$?

      local outcome="success"
      [[ $exit_code -ne 0 ]] && outcome="failure"

      # Audit log
      bash "$AUDIT_SH" log \
        --intent "exec" \
        --input "$args_str" \
        --risk "$risk" \
        --decision "allow" \
        --evidence "exit_code=$exit_code" \
        --outcome "$outcome" \
        --skill "$skill_name" \
        --command "$(basename "$script") $args_str" \
        > /dev/null

      # Collect failure sample if failed
      if [[ "$outcome" == "failure" ]]; then
        local evt
        evt=$(jq -nc --arg r "$risk" --arg s "$skill_name" --arg c "$(basename "$script") $args_str" --arg rs "$reasons" \
          '{type:"execution_failure",risk:$r,skill:$s,command:$c,reasons:$rs}')
        bash "$AUDIT_SH" collect-failure "$evt" > /dev/null 2>&1 || true
      fi

      echo "$output"
      exit $exit_code
      ;;

    prompt)
      # L3: high risk — ask for human confirmation
      bash "$AUDIT_SH" log \
        --intent "exec" \
        --input "$args_str" \
        --risk "$risk" \
        --decision "prompt" \
        --evidence "awaiting_approval" \
        --outcome "pending" \
        --reason "$reasons" \
        --skill "$skill_name" \
        --command "$(basename "$script") $args_str" \
        > /dev/null

      echo "⚠️ HIGH RISK ACTION DETECTED"
      echo "  Skill: $skill_name"
      echo "  Command: $(basename "$script") $args_str"
      echo "  Risk: $risk"
      echo "  Reason: $reasons"
      echo ""
      echo "Reply '确认' or 'confirm' to proceed, anything else to cancel."
      exit 10
      ;;

    block)
      # Critical: block entirely
      bash "$AUDIT_SH" log \
        --intent "exec" \
        --input "$args_str" \
        --risk "$risk" \
        --decision "block" \
        --evidence "policy_violation" \
        --outcome "blocked" \
        --reason "$reasons" \
        --skill "$skill_name" \
        --command "$(basename "$script") $args_str" \
        > /dev/null

      # Collect as failure sample
      local evt
      evt=$(jq -nc --arg r "$risk" --arg s "$skill_name" --arg c "$(basename "$script") $args_str" --arg rs "$reasons" \
        '{type:"policy_block",risk:$r,skill:$s,command:$c,reasons:$rs}')
      bash "$AUDIT_SH" collect-failure "$evt" > /dev/null 2>&1 || true

      echo "🚫 BLOCKED: Critical security policy violation"
      echo "  Skill: $skill_name"
      echo "  Command: $(basename "$script") $args_str"
      echo "  Risk: $risk"
      echo "  Reason: $reasons"
      exit 11
      ;;
  esac
}

# Confirm a pending high-risk action (called after user says 确认/confirm)
cmd_confirm(){
  require_jq
  local script="" 
  local -a pass_args=()

  if [[ $# -lt 1 ]]; then
    echo "usage: guard-exec.sh confirm <script> [args...]" >&2
    exit 1
  fi

  script="$1"; shift
  pass_args=("$@")

  if [[ ! -f "$script" ]]; then
    echo "error: script not found: $script" >&2; exit 1
  fi

  local skill_name args_str
  skill_name=$(extract_skill_name "$script")
  args_str="${pass_args[*]:-}"

  local output exit_code=0
  output=$(bash "$script" "${pass_args[@]}" 2>&1) || exit_code=$?

  local outcome="success"
  [[ $exit_code -ne 0 ]] && outcome="failure"

  bash "$AUDIT_SH" log \
    --intent "exec_confirmed" \
    --input "$args_str" \
    --risk "high" \
    --decision "allow" \
    --evidence "human_approved,exit_code=$exit_code" \
    --outcome "$outcome" \
    --skill "$skill_name" \
    --command "$(basename "$script") $args_str" \
    > /dev/null

  echo "$output"
  exit $exit_code
}

# Dry-run: show what would happen without executing
cmd_dry_run(){
  require_jq
  local script=""
  local -a pass_args=()

  if [[ $# -lt 1 ]]; then
    echo "usage: guard-exec.sh dry-run <script> [args...]" >&2; exit 1
  fi

  script="$1"; shift
  pass_args=("$@")

  if [[ ! -f "$script" ]]; then
    echo "error: script not found: $script" >&2; exit 1
  fi

  local skill_name args_str
  skill_name=$(extract_skill_name "$script")
  args_str="${pass_args[*]:-}"

  local risk_result risk reasons
  risk_result=$(classify_risk "$script" "$args_str")
  risk=$(echo "$risk_result" | cut -d'|' -f1)
  reasons=$(echo "$risk_result" | cut -d'|' -f2)

  local decision
  decision=$(decide_action "$risk")

  bash "$AUDIT_SH" log \
    --intent "dry_run" \
    --input "$args_str" \
    --risk "$risk" \
    --decision "dry-run" \
    --evidence "preview_only" \
    --outcome "success" \
    --skill "$skill_name" \
    --command "$(basename "$script") $args_str" \
    > /dev/null

  echo "DRY RUN — no changes made"
  echo "  Skill: $skill_name"
  echo "  Command: $(basename "$script") $args_str"
  echo "  Risk: $risk"
  echo "  Decision: $decision"
  echo "  Reason: $reasons"
}

# Quick risk check without execution
cmd_check(){
  local script=""
  local -a pass_args=()

  if [[ $# -lt 1 ]]; then
    echo "usage: guard-exec.sh check <script> [args...]" >&2; exit 1
  fi

  script="$1"; shift
  pass_args=("$@")

  if [[ ! -f "$script" ]]; then
    echo "error: script not found: $script" >&2; exit 1
  fi

  local args_str="${pass_args[*]:-}"
  local risk_result risk reasons
  risk_result=$(classify_risk "$script" "$args_str")
  risk=$(echo "$risk_result" | cut -d'|' -f1)
  reasons=$(echo "$risk_result" | cut -d'|' -f2)

  local decision
  decision=$(decide_action "$risk")

  echo "risk=$risk decision=$decision reasons=$reasons"
}

main(){
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    exec)     cmd_exec "$@" ;;
    confirm)  cmd_confirm "$@" ;;
    dry-run)  cmd_dry_run "$@" ;;
    check)    cmd_check "$@" ;;
    *) echo "usage: guard-exec.sh {exec|confirm|dry-run|check} <script> [args...]" >&2; exit 1 ;;
  esac
}

main "$@"
