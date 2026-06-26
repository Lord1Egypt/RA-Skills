#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CANDIDATES_DIR="$BASE_DIR/rules/candidates"
ACTIVE_DIR="$BASE_DIR/rules/active"
AUDIT_SH="$BASE_DIR/scripts/audit.sh"

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

# Only allow alphanumeric, dash, underscore in rule names (block path traversal)
validate_rule_name(){
  local name="$1"
  if [[ ! "$name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "error: rule name must be alphanumeric/dash/underscore only" >&2; exit 1
  fi
  if [[ ${#name} -gt 64 ]]; then
    echo "error: rule name too long (max 64)" >&2; exit 1
  fi
}

# Ensure a file path is strictly within the expected directory
assert_path_within(){
  local filepath="$1" expected_dir="$2"
  local real_path real_dir
  real_path="$(cd "$(dirname "$filepath")" 2>/dev/null && pwd)/$(basename "$filepath")"
  real_dir="$(cd "$expected_dir" 2>/dev/null && pwd)"
  if [[ "$real_path" != "$real_dir"/* ]]; then
    echo "error: path escapes allowed directory: $filepath" >&2; exit 1
  fi
}

# List candidate rules
cmd_list(){
  echo "=== Candidate Rules ==="
  if [[ -z "$(ls -A "$CANDIDATES_DIR" 2>/dev/null)" ]]; then
    echo "  (none)"
    return
  fi
  for f in "$CANDIDATES_DIR"/*.rule; do
    [[ -f "$f" ]] || continue
    local name pattern level
    name=$(basename "$f" .rule)
    pattern=$(head -1 "$f")
    level=$(sed -n '2p' "$f")
    echo "  $name  pattern=$pattern  level=$level"
  done

  echo ""
  echo "=== Active Rules ==="
  if [[ -z "$(ls -A "$ACTIVE_DIR" 2>/dev/null)" ]]; then
    echo "  (none)"
    return
  fi
  for f in "$ACTIVE_DIR"/*.rule; do
    [[ -f "$f" ]] || continue
    local name pattern level
    name=$(basename "$f" .rule)
    pattern=$(head -1 "$f")
    level=$(sed -n '2p' "$f")
    echo "  $name  pattern=$pattern  level=$level"
  done
}

# Promote a candidate rule to active (requires human confirmation)
cmd_promote(){
  require_jq
  local rule_name="" confirmed=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --rule) [[ $# -ge 2 ]] || { echo "error: missing --rule" >&2; exit 1; }; rule_name="$2"; shift 2 ;;
      --confirmed) confirmed=true; shift ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$rule_name" ]] || { echo "error: --rule required" >&2; exit 1; }
  validate_rule_name "$rule_name"

  local candidate="$CANDIDATES_DIR/${rule_name}.rule"
  assert_path_within "$candidate" "$CANDIDATES_DIR"
  [[ -f "$candidate" ]] || { echo "error: candidate rule not found: $rule_name" >&2; exit 1; }

  # Promoting a rule changes detection behavior — require explicit human approval
  if [[ "$confirmed" != true ]]; then
    local pattern level
    pattern=$(head -1 "$candidate")
    level=$(sed -n '2p' "$candidate")

    bash "$AUDIT_SH" log \
      --intent "promote_rule" \
      --input "$rule_name" \
      --risk "high" \
      --decision "prompt" \
      --evidence "awaiting_approval" \
      --outcome "pending" \
      --reason "rule promotion changes detection behavior" \
      > /dev/null

    echo "⚠️ RULE PROMOTION REQUIRES APPROVAL"
    echo "  Rule: $rule_name"
    echo "  Pattern: $pattern"
    echo "  Level: $level"
    echo ""
    echo "Reply '确认' or 'confirm' to promote, anything else to cancel."
    echo "Then re-run: promote-rule.sh promote --rule $rule_name --confirmed"
    exit 10
  fi

  cp "$candidate" "$ACTIVE_DIR/${rule_name}.rule"
  rm "$candidate"

  bash "$AUDIT_SH" log \
    --intent "promote_rule" \
    --input "$rule_name" \
    --risk "high" \
    --decision "allow" \
    --evidence "human_approved,rule_promoted_to_active" \
    --outcome "success" \
    > /dev/null

  echo "promoted: $rule_name → active"
}

# Demote (rollback) an active rule back to candidate
cmd_demote(){
  require_jq
  local rule_name=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --rule) [[ $# -ge 2 ]] || { echo "error: missing --rule" >&2; exit 1; }; rule_name="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$rule_name" ]] || { echo "error: --rule required" >&2; exit 1; }
  validate_rule_name "$rule_name"

  local active="$ACTIVE_DIR/${rule_name}.rule"
  assert_path_within "$active" "$ACTIVE_DIR"
  [[ -f "$active" ]] || { echo "error: active rule not found: $rule_name" >&2; exit 1; }

  mv "$active" "$CANDIDATES_DIR/${rule_name}.rule"

  bash "$AUDIT_SH" log \
    --intent "demote_rule" \
    --input "$rule_name" \
    --risk "medium" \
    --decision "allow" \
    --evidence "rule_demoted_to_candidate" \
    --outcome "success" \
    > /dev/null

  echo "demoted: $rule_name → candidate"
}

# Create a new candidate rule
cmd_add(){
  local rule_name="" pattern="" level=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --rule)    [[ $# -ge 2 ]] || { echo "error: missing --rule" >&2; exit 1; };    rule_name="$2"; shift 2 ;;
      --pattern) [[ $# -ge 2 ]] || { echo "error: missing --pattern" >&2; exit 1; }; pattern="$2";   shift 2 ;;
      --level)   [[ $# -ge 2 ]] || { echo "error: missing --level" >&2; exit 1; };   level="$2";     shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$rule_name" ]] || { echo "error: --rule required" >&2; exit 1; }
  [[ -n "$pattern" ]]   || { echo "error: --pattern required" >&2; exit 1; }
  [[ -n "$level" ]]     || { echo "error: --level required" >&2; exit 1; }
  validate_rule_name "$rule_name"

  case "$level" in
    low|medium|high|critical) ;;
    *) echo "error: --level must be low|medium|high|critical" >&2; exit 1 ;;
  esac

  # Rule file format: line 1 = regex pattern, line 2 = risk level
  printf '%s\n%s\n' "$pattern" "$level" > "$CANDIDATES_DIR/${rule_name}.rule"
  echo "created candidate rule: $rule_name"
}

main(){
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    list)    cmd_list ;;
    promote) cmd_promote "$@" ;;
    demote)  cmd_demote "$@" ;;
    add)     cmd_add "$@" ;;
    *) echo "usage: promote-rule.sh {list|promote|demote|add} [args]" >&2; exit 1 ;;
  esac
}

main "$@"
