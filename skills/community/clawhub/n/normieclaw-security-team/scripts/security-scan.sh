#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Security Team — Security Council Scanner
# Scans for hardcoded secrets, npm vulnerabilities, and file permission issues.
# Output: JSON to stdout
# ============================================================================

# --- Workspace Root Detection ---
    # Skill directory detection (stay within skill boundary)
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}")" && pwd)"
  echo "$(dirname "$(dirname "$script_dir")")"
}

SKILL_DIR="$(cd "$(find_skill_root)" && pwd -P)"
CONFIG_FILE="$SKILL_DIR/config/security-config.json"

# --- OS Detection ---
OS="$(uname -s)"

# --- Dependency Detection ---
HAS_RG=false
HAS_NPM=false
HAS_JQ=false

command -v rg >/dev/null 2>&1 && HAS_RG=true
command -v npm >/dev/null 2>&1 && HAS_NPM=true
command -v jq >/dev/null 2>&1 && HAS_JQ=true

# --- Config Loading ---
SCAN_DIRS=()
SECRET_PATTERNS=()
FALSE_POSITIVE_PATTERNS=()
SCAN_EXCLUDES=()

resolve_scan_dir() {
  local rel_dir="$1"
  [ -n "$rel_dir" ] || return 1
  case "$rel_dir" in
    /*) return 1 ;;
  esac

  local candidate="$SKILL_DIR/$rel_dir"
  [ -d "$candidate" ] || return 1

  local resolved
  resolved="$(cd "$candidate" 2>/dev/null && pwd -P)" || return 1
  case "$resolved" in
    "$SKILL_DIR"|"$SKILL_DIR"/*) echo "$resolved" ;;
    *) return 1 ;;
  esac
}

if [ -f "$CONFIG_FILE" ]; then
  if $HAS_JQ; then
    # Load scan directories (filter out _comment entries)
    while IFS= read -r dir; do
      [ -n "$dir" ] && [[ "$dir" != _comment* ]] || continue
      local_safe_dir="$(resolve_scan_dir "$dir" || true)"
      [ -n "$local_safe_dir" ] && SCAN_DIRS+=("$local_safe_dir")
    done < <(jq -r '.scan_directories[]? // empty' "$CONFIG_FILE" 2>/dev/null)

    # Load secret patterns
    while IFS= read -r pat; do
      [ -n "$pat" ] && SECRET_PATTERNS+=("$pat")
    done < <(jq -r '.secret_patterns[]? // empty' "$CONFIG_FILE" 2>/dev/null)

    # Load false positive patterns
    while IFS= read -r pat; do
      [ -n "$pat" ] && FALSE_POSITIVE_PATTERNS+=("$pat")
    done < <(jq -r '.false_positive_patterns[]? // empty' "$CONFIG_FILE" 2>/dev/null)

    # Load scan excludes
    while IFS= read -r exc; do
      [ -n "$exc" ] && SCAN_EXCLUDES+=("$exc")
    done < <(jq -r '.scan_excludes[]? // empty' "$CONFIG_FILE" 2>/dev/null)
  fi
fi

# Defaults if config didn't load
if [ ${#SECRET_PATTERNS[@]} -eq 0 ]; then
  SECRET_PATTERNS=(
    'sk-[a-zA-Z0-9]{20,}'
    'AKIA[A-Z0-9]{16}'
    'eyJ[a-zA-Z0-9_-]{30,}\.[a-zA-Z0-9_-]+'
    'ghp_[a-zA-Z0-9]{36}'
    'gho_[a-zA-Z0-9]{36}'
    'xoxb-[a-zA-Z0-9-]+'
    'xoxp-[a-zA-Z0-9-]+'
  )
fi

if [ ${#SCAN_DIRS[@]} -eq 0 ]; then
  SCAN_DIRS=("$SKILL_DIR")
fi

if [ ${#SCAN_EXCLUDES[@]} -eq 0 ]; then
  SCAN_EXCLUDES=("node_modules" ".git" "vendor" "dist" "build" "__pycache__")
fi

# --- Output Collection ---
FINDINGS="[]"

add_finding() {
  local severity="$1"
  local description="$2"
  local location="$3"
  local remediation="$4"
  # Generate a simple hash from severity + description + location
  local hash
  hash="$(echo -n "${severity}-${description}-${location}" | shasum -a 256 | cut -c1-16)"

  if $HAS_JQ; then
    FINDINGS=$(echo "$FINDINGS" | jq \
      --arg sev "$severity" \
      --arg desc "$description" \
      --arg loc "$location" \
      --arg rem "$remediation" \
      --arg hash "$hash" \
      '. + [{"hash": $hash, "council": "security", "severity": $sev, "description": $desc, "location": $loc, "remediation": $rem}]')
  else
    # Fallback: append raw JSON (less robust but functional)
    local entry="{\"hash\":\"$hash\",\"council\":\"security\",\"severity\":\"$severity\",\"description\":\"$description\",\"location\":\"$location\",\"remediation\":\"$remediation\"}"
    if [ "$FINDINGS" = "[]" ]; then
      FINDINGS="[$entry]"
    else
      FINDINGS="${FINDINGS%]}, $entry]"
    fi
  fi
}

# --- Check 1: Hardcoded Secrets ---
check_secrets() {
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir" ] || continue

    for pattern in "${SECRET_PATTERNS[@]}"; do
      local results=""

      # Build exclude args
      if $HAS_RG; then
        local rg_excludes=()
        for exc in "${SCAN_EXCLUDES[@]}"; do
          rg_excludes+=("--glob" "!$exc")
        done
        results=$(rg -n --no-heading "${rg_excludes[@]}" -- "$pattern" "$dir" 2>/dev/null || true)
      else
        local grep_excludes=()
        for exc in "${SCAN_EXCLUDES[@]}"; do
          grep_excludes+=("--exclude-dir=$exc")
        done
        results=$(grep -rn "${grep_excludes[@]}" -E -- "$pattern" "$dir" 2>/dev/null || true)
      fi

      # Filter false positives
      if [ -n "$results" ]; then
        while IFS= read -r line; do
          [ -z "$line" ] && continue
          local is_fp=false
          for fp in "${FALSE_POSITIVE_PATTERNS[@]}"; do
            if echo "$line" | grep -qE -- "$fp" 2>/dev/null; then
              is_fp=true
              break
            fi
          done
          # Skip .env.example, test fixtures, comments
          if echo "$line" | grep -qiE '\.env\.example|\.env\.sample|test_fixture|mock|placeholder|CHANGEME|YOUR_.*_HERE' 2>/dev/null; then
            is_fp=true
          fi

          if ! $is_fp; then
            local file_loc
            file_loc=$(echo "$line" | cut -d: -f1-2)
            # Make path relative to workspace
            file_loc="${file_loc#"$SKILL_DIR/"}"
            local redacted
            redacted=$(echo "$line" | grep -oE "$pattern" 2>/dev/null | head -1 | cut -c1-6)
            add_finding "CRITICAL" "Possible hardcoded secret (${redacted}***) matching pattern $pattern" "$file_loc" "Move to environment variable. If committed to git, rotate the secret immediately."
          fi
        done <<< "$results"
      fi
    done
  done
}

# --- Check 2: npm Audit ---
check_npm_audit() {
  $HAS_NPM || return 0

  for dir in "${SCAN_DIRS[@]}"; do
    [ -f "$dir/package.json" ] || continue
    [ -d "$dir/node_modules" ] || continue

    local audit_output
    audit_output=$(cd "$dir" && npm audit --json 2>/dev/null || true)

    if [ -n "$audit_output" ] && $HAS_JQ; then
      local critical high moderate
      critical=$(echo "$audit_output" | jq '.metadata.vulnerabilities.critical // 0' 2>/dev/null || echo 0)
      high=$(echo "$audit_output" | jq '.metadata.vulnerabilities.high // 0' 2>/dev/null || echo 0)
      moderate=$(echo "$audit_output" | jq '.metadata.vulnerabilities.moderate // 0' 2>/dev/null || echo 0)
      local rel_dir="${dir#"$SKILL_DIR/"}"

      if [ "$critical" -gt 0 ] 2>/dev/null; then
        add_finding "CRITICAL" "npm audit: $critical critical vulnerabilities" "$rel_dir" "Run 'npm audit fix' or update affected packages."
      fi
      if [ "$high" -gt 0 ] 2>/dev/null; then
        add_finding "MEDIUM" "npm audit: $high high-severity vulnerabilities" "$rel_dir" "Run 'npm audit fix' or review with 'npm audit'."
      fi
      if [ "$moderate" -gt 0 ] 2>/dev/null; then
        add_finding "MEDIUM" "npm audit: $moderate moderate vulnerabilities" "$rel_dir" "Review with 'npm audit' and update as needed."
      fi
    fi
  done
}

# --- Check 3: File Permissions ---
check_permissions() {
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir" ] || continue

    # Find .env files with overly permissive permissions
    while IFS= read -r envfile; do
      [ -z "$envfile" ] && continue
      local perms
      if [ "$OS" = "Darwin" ]; then
        perms=$(stat -f '%Lp' "$envfile" 2>/dev/null || echo "000")
      else
        perms=$(stat -c '%a' "$envfile" 2>/dev/null || echo "000")
      fi

      # Flag if group or world readable (perms like 644, 755, 777, etc.)
      local group_other="${perms:1}"
      if [ -n "$group_other" ] && [ "$group_other" != "00" ]; then
        local rel_path="${envfile#"$SKILL_DIR/"}"
        add_finding "CRITICAL" ".env file has permissive permissions (chmod $perms)" "$rel_path" "Run: chmod 600 $rel_path"
      fi
    done < <(find "$dir" \( -name '.env' -o -name '.env.local' -o -name '.env.production' \) 2>/dev/null | head -50)

    # Check for world-writable directories
    while IFS= read -r wdir; do
      [ -z "$wdir" ] && continue
      local rel_path="${wdir#"$SKILL_DIR/"}"
      add_finding "MEDIUM" "World-writable directory detected" "$rel_path" "Run: chmod 755 $rel_path (or more restrictive)"
    done < <(find "$dir" -maxdepth 3 -type d -perm -o+w 2>/dev/null | grep -v node_modules | grep -v .git | head -20)
  done
}

# --- Check 4: .gitignore Verification ---
check_gitignore() {
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir/.git" ] || continue

    local gitignore="$dir/.gitignore"
    if [ -f "$gitignore" ]; then
      if ! grep -q '\.env' "$gitignore" 2>/dev/null; then
        local rel_path="${dir#"$SKILL_DIR/"}"
        add_finding "MEDIUM" ".gitignore does not include .env pattern" "$rel_path/.gitignore" "Add '.env*' to your .gitignore file."
      fi
    else
      if [ -f "$dir/.env" ]; then
        local rel_path="${dir#"$SKILL_DIR/"}"
        add_finding "MEDIUM" "No .gitignore found but .env file exists" "$rel_path" "Create a .gitignore and add '.env*' to it."
      fi
    fi
  done
}

# --- Check 5: Git History Secrets (lightweight) ---
check_git_history() {
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir/.git" ] || continue

    # Only check for the most dangerous patterns in recent history
    for pattern in 'sk-' 'AKIA'; do
      local count
      count=$(cd "$dir" && git log --all -p -n 100 -S "$pattern" --diff-filter=D -- '*.js' '*.ts' '*.py' '*.json' '*.yml' '*.yaml' 2>/dev/null | grep -c "^-.*$pattern" || echo 0)
      if [ "$count" -gt 0 ] 2>/dev/null && [ "$count" -ne 0 ]; then
        local rel_path="${dir#"$SKILL_DIR/"}"
        add_finding "MEDIUM" "Possible secret ($pattern...) found in deleted git history ($count occurrences)" "$rel_path" "Consider using BFG Repo-Cleaner or git filter-branch to purge history. Rotate the secret."
      fi
    done
  done
}

# --- Run All Checks ---
check_secrets
check_npm_audit
check_permissions
check_gitignore
check_git_history

# --- Calculate Score ---
SCORE=10
CRITICAL_COUNT=0
MEDIUM_COUNT=0

if $HAS_JQ; then
  CRITICAL_COUNT=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "CRITICAL")] | length')
  MEDIUM_COUNT=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "MEDIUM")] | length')
else
  CRITICAL_COUNT=$(echo "$FINDINGS" | grep -o '"CRITICAL"' | wc -l | tr -d ' ')
  MEDIUM_COUNT=$(echo "$FINDINGS" | grep -o '"MEDIUM"' | wc -l | tr -d ' ')
fi

# Scoring: -3 per critical, -1 per medium, floor at 0
SCORE=$(( SCORE - (CRITICAL_COUNT * 3) - MEDIUM_COUNT ))
[ "$SCORE" -lt 0 ] && SCORE=0

# --- Output JSON ---
if $HAS_JQ; then
  jq -n \
    --argjson score "$SCORE" \
    --argjson findings "$FINDINGS" \
    --argjson critical "$CRITICAL_COUNT" \
    --argjson medium "$MEDIUM_COUNT" \
    '{
      "council": "security",
      "score": $score,
      "findings": $findings,
      "summary": {
        "critical": $critical,
        "medium": $medium,
        "total": ($critical + $medium)
      }
    }'
else
  echo "{\"council\":\"security\",\"score\":$SCORE,\"findings\":$FINDINGS,\"summary\":{\"critical\":$CRITICAL_COUNT,\"medium\":$MEDIUM_COUNT,\"total\":$(( CRITICAL_COUNT + MEDIUM_COUNT ))}}"
fi
