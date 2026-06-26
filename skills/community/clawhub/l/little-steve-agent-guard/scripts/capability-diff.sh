#!/usr/bin/env bash
set -euo pipefail

# Capability Diff: compare SKILL.md declared commands vs script actual commands
# Detects mismatches that indicate inconsistent behavior.

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

cmd_check(){
  local skill_dir=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --skill-dir) [[ $# -ge 2 ]] || { echo "error: missing --skill-dir" >&2; exit 1; }; skill_dir="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$skill_dir" ]] || { echo "error: --skill-dir required" >&2; exit 1; }
  [[ -d "$skill_dir" ]] || { echo "error: directory not found: $skill_dir" >&2; exit 1; }

  local skill_md="$skill_dir/SKILL.md"
  [[ -f "$skill_md" ]] || { echo "error: SKILL.md not found in $skill_dir" >&2; exit 1; }

  local skill_name
  skill_name=$(basename "$skill_dir")
  local issues=0
  local warnings=""

  echo "=== Capability Diff: $skill_name ==="
  echo ""

  # 1. Extract declared script references from SKILL.md
  local declared_scripts
  declared_scripts=$(grep -oE 'scripts/[a-zA-Z0-9_-]+\.sh' "$skill_md" | sort -u)

  # 2. Find actual scripts in skill directory
  local actual_scripts
  actual_scripts=$(find "$skill_dir/scripts" -name "*.sh" -type f 2>/dev/null | sed "s|$skill_dir/||" | sort -u)

  # 3. Check: scripts referenced in SKILL.md but not present
  echo "--- Declared scripts (SKILL.md) ---"
  if [[ -z "$declared_scripts" ]]; then
    echo "  (none found)"
    warnings="${warnings}WARN: No script references found in SKILL.md\n"
    ((issues++))
  else
    for s in $declared_scripts; do
      if [[ -f "$skill_dir/$s" ]]; then
        echo "  ✓ $s"
      else
        echo "  ✗ $s (MISSING)"
        warnings="${warnings}ERROR: SKILL.md references $s but file not found\n"
        ((issues++))
      fi
    done
  fi
  echo ""

  # 4. Check: scripts present but not referenced in SKILL.md
  echo "--- Actual scripts (filesystem) ---"
  if [[ -z "$actual_scripts" ]]; then
    echo "  (none found)"
  else
    for s in $actual_scripts; do
      if echo "$declared_scripts" | grep -qF "$s"; then
        echo "  ✓ $s (declared)"
      else
        echo "  ⚠ $s (UNDECLARED)"
        warnings="${warnings}WARN: $s exists but is not referenced in SKILL.md\n"
        ((issues++))
      fi
    done
  fi
  echo ""

  # 5. Check: declared commands vs actual script subcommands
  # Extract commands from SKILL.md code blocks (e.g., "inbox.sh add", "inbox.sh list")
  for script_ref in $declared_scripts; do
    local script_file="$skill_dir/$script_ref"
    [[ -f "$script_file" ]] || continue

    local script_base
    script_base=$(basename "$script_ref")

    echo "--- Command check: $script_base ---"

    # Extract declared subcommands from SKILL.md
    local declared_cmds
    declared_cmds=$(grep -oE "${script_base} [a-z_-]+" "$skill_md" | awk '{print $2}' | sort -u)

    # Extract actual subcommands from script's main case dispatch
    # Match lines like: add) cmd_add ;; — only top-level commands, not --option flags
    local actual_cmds
    actual_cmds=$(grep -oE '^\s*[a-z][a-z_-]*\)' "$script_file" 2>/dev/null | \
      sed -E 's/[[:space:]]*//g; s/\)//' | \
      grep -vE '^(esac|case|in|do|done|then|else|fi|end)$' | \
      sort -u)

    if [[ -n "$declared_cmds" ]]; then
      for cmd in $declared_cmds; do
        if echo "$actual_cmds" | grep -qxF "$cmd"; then
          echo "  ✓ $cmd"
        else
          echo "  ✗ $cmd (declared but NOT in script)"
          warnings="${warnings}ERROR: $script_base declares command '$cmd' but script does not implement it\n"
          ((issues++))
        fi
      done
    fi

    # Check for undeclared commands in script
    if [[ -n "$actual_cmds" ]]; then
      for cmd in $actual_cmds; do
        if [[ -n "$declared_cmds" ]] && ! echo "$declared_cmds" | grep -qxF "$cmd"; then
          echo "  ⚠ $cmd (in script but UNDECLARED)"
          warnings="${warnings}WARN: $script_base implements '$cmd' but not declared in SKILL.md\n"
          ((issues++))
        fi
      done
    fi
    echo ""
  done

  # 6. Check: jq dependency declared if used
  if find "$skill_dir/scripts" -name "*.sh" -exec grep -l '\bjq\b' {} + >/dev/null 2>&1; then
    if grep -qi 'requires' "$skill_md" && grep -qi 'jq' "$skill_md"; then
      echo "✓ jq dependency declared"
    else
      echo "⚠ Scripts use jq but SKILL.md does not declare it as required"
      warnings="${warnings}WARN: jq used in scripts but not declared in SKILL.md requires\n"
      ((issues++))
    fi
  fi

  # 7. Check: network binaries in scripts
  local net_bins="curl wget nc ncat socat telnet ssh scp rsync ftp"
  for script_file in "$skill_dir"/scripts/*.sh; do
    [[ -f "$script_file" ]] || continue
    for bin in $net_bins; do
      if grep -qw "$bin" "$script_file" 2>/dev/null; then
        echo "⚠ $(basename "$script_file") contains network binary: $bin"
        warnings="${warnings}WARN: $(basename "$script_file") contains network binary '$bin'\n"
        ((issues++))
      fi
    done
  done

  echo ""
  echo "=== Result ==="
  if [[ $issues -eq 0 ]]; then
    echo "PASS: No mismatches found"
  else
    echo "FAIL: $issues issue(s) found"
    echo ""
    echo "--- Issues ---"
    echo -e "$warnings"
  fi

  return $issues
}

main(){
  require_jq
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    check) cmd_check "$@" ;;
    *) echo "usage: capability-diff.sh check --skill-dir <path>" >&2; exit 1 ;;
  esac
}

main "$@"
