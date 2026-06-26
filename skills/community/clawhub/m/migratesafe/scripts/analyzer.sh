#!/usr/bin/env bash
# MigrateSafe -- Core Analysis Engine
# Provides: framework detection, file scanning, risk scoring, rollback checking,
#           diff analysis, history scanning, and report generation.
#
# This file is sourced by migratesafe.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# ─── Colors (safe to re-declare; sourcing scripts may set these) ─────────────

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

# ─── Constants ───────────────────────────────────────────────────────────────

MIGRATESAFE_VERSION="${VERSION:-1.0.0}"

# Known migration directories (relative patterns)
declare -a MIGRATION_DIR_PATTERNS=(
  "db/migrate"
  "migrations"
  "prisma/migrations"
  "sql"
  "database/migrations"
  "src/migrations"
  "src/database/migrations"
  "alembic/versions"
  "flyway/sql"
  "liquibase"
  "changesets"
)

# Known migration file extensions
declare -a MIGRATION_FILE_EXTENSIONS=(
  "sql" "rb" "py" "js" "ts" "xml"
)

# ─── Framework Detection ─────────────────────────────────────────────────────

# Detect the migration framework for a given file based on its path and extension.
# Outputs one of: sql, rails, django, knex, prisma, flyway, liquibase, unknown
detect_framework() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local dirpath
  dirpath=$(dirname "$filepath")
  local ext="${basename_f##*.}"

  # By extension first
  case "$ext" in
    rb)
      # Rails migrations live in db/migrate/
      echo "rails"
      return 0
      ;;
    py)
      # Django migrations
      echo "django"
      return 0
      ;;
    xml)
      # Liquibase changesets
      echo "liquibase"
      return 0
      ;;
    js|ts)
      # Knex.js migrations
      echo "knex"
      return 0
      ;;
    sql)
      # Could be Prisma, Flyway, or raw SQL -- check path
      if echo "$dirpath" | grep -qi "prisma/migrations"; then
        echo "prisma"
        return 0
      fi
      if echo "$basename_f" | grep -qE "^[VUR][0-9]"; then
        echo "flyway"
        return 0
      fi
      if echo "$dirpath" | grep -qi "flyway"; then
        echo "flyway"
        return 0
      fi
      echo "sql"
      return 0
      ;;
  esac

  # Fallback: check directory name for clues
  if echo "$dirpath" | grep -qi "db/migrate"; then
    echo "rails"
  elif echo "$dirpath" | grep -qi "prisma/migrations"; then
    echo "prisma"
  elif echo "$dirpath" | grep -qi "alembic"; then
    echo "django"
  elif echo "$dirpath" | grep -qi "flyway\|/sql/V"; then
    echo "flyway"
  elif echo "$dirpath" | grep -qi "liquibase\|changeset"; then
    echo "liquibase"
  else
    echo "sql"
  fi
}

# ─── Find Migration Files ───────────────────────────────────────────────────

# Find all migration files in a directory tree.
# Usage: find_migration_files <directory> <array_name>
find_migration_files() {
  local search_dir="$1"
  local -n _result_arr="$2"
  _result_arr=()

  # If target is a single file, just add it
  if [[ -f "$search_dir" ]]; then
    local ext="${search_dir##*.}"
    for valid_ext in "${MIGRATION_FILE_EXTENSIONS[@]}"; do
      if [[ "$ext" == "$valid_ext" ]]; then
        _result_arr+=("$search_dir")
        return 0
      fi
    done
    return 0
  fi

  # Search known migration directories first
  local found_known_dir=false
  for pattern in "${MIGRATION_DIR_PATTERNS[@]}"; do
    local candidate="$search_dir/$pattern"
    if [[ -d "$candidate" ]]; then
      found_known_dir=true
      while IFS= read -r -d '' file; do
        # Skip binary files
        if file "$file" 2>/dev/null | grep -q "text"; then
          _result_arr+=("$file")
        fi
      done < <(find "$candidate" -type f \( -name "*.sql" -o -name "*.rb" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.xml" \) -print0 2>/dev/null | sort -z)
    fi
  done

  # If no known dirs found, search entire tree for migration-like files
  if [[ "$found_known_dir" == false ]]; then
    while IFS= read -r -d '' file; do
      local dir_of_file
      dir_of_file=$(dirname "$file")
      local base_of_file
      base_of_file=$(basename "$file")
      # Heuristic: file is in a directory named *migrat* or *changeset* or file starts with a timestamp/version
      if echo "$dir_of_file" | grep -qiE "migrat|changeset|alembic|flyway|schema|db/"; then
        if file "$file" 2>/dev/null | grep -q "text"; then
          _result_arr+=("$file")
        fi
      elif echo "$base_of_file" | grep -qE "^[0-9]{8,14}|^V[0-9]+|^[0-9]+_"; then
        if file "$file" 2>/dev/null | grep -q "text"; then
          _result_arr+=("$file")
        fi
      fi
    done < <(find "$search_dir" -type f \( -name "*.sql" -o -name "*.rb" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.xml" \) -print0 2>/dev/null | sort -z)
  fi
}

# ─── Scan File With Patterns ─────────────────────────────────────────────────

# Scan a single file against a pattern array. Collects findings.
# Each finding is appended to the global FINDINGS array as:
#   FILE|LINE|SEVERITY|CATEGORY|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
#
# Usage: scan_file_with_patterns <filepath> <patterns_array_name>
scan_file_with_patterns() {
  local filepath="$1"
  local patterns_array_name="$2"
  local -n _patterns_ref="$patterns_array_name"

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity category description recommendation <<< "$entry"

    # Use grep -nE to find matches with line numbers
    # grep may return non-zero if no match, so use || true
    local matches
    matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

    if [[ -n "$matches" ]]; then
      while IFS= read -r match_line; do
        local line_num="${match_line%%:*}"
        local matched_text="${match_line#*:}"
        # Trim whitespace from matched text
        matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        # Truncate long lines
        if [[ ${#matched_text} -gt 120 ]]; then
          matched_text="${matched_text:0:117}..."
        fi
        FINDINGS+=("${filepath}|${line_num}|${severity}|${category}|${description}|${recommendation}|${matched_text}")
      done <<< "$matches"
    fi
  done
}

# ─── Analyze Single Migration File ──────────────────────────────────────────

# Analyze a single migration file. Detects framework, selects patterns, scans.
# Appends results to global FINDINGS array.
# Returns 0 always; check FINDINGS for results.
analyze_migration_file() {
  local filepath="$1"
  local framework

  framework=$(detect_framework "$filepath")

  # Get the appropriate patterns array name
  local patterns_name
  patterns_name=$(get_patterns_for_framework "$framework")

  # Scan with framework-specific patterns
  scan_file_with_patterns "$filepath" "$patterns_name"

  # For SQL-based frameworks, also check for missing transactions and lock hazards
  case "$framework" in
    sql|prisma|flyway)
      detect_missing_transactions "$filepath"
      detect_lock_hazards "$filepath"
      ;;
    rails)
      # Rails has its own transaction handling, but check for raw SQL
      ;;
    django)
      # Django wraps migrations in transactions by default
      ;;
    knex)
      # Knex has transaction support via knex.transaction
      ;;
    liquibase)
      # Liquibase has its own transaction management
      ;;
  esac
}

# ─── Calculate Risk Score ────────────────────────────────────────────────────

# Calculate a risk score from an array of findings.
# Usage: calculate_risk_score -> prints score (0-100)
calculate_risk_score() {
  local score=0

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _file _line severity _category _desc _rec _text <<< "$finding"
    local points
    points=$(severity_to_risk "$severity")
    score=$((score + points))
  done

  # Cap at 100
  if [[ $score -gt 100 ]]; then
    score=100
  fi

  echo "$score"
}

# Convert risk score to letter grade
risk_grade() {
  local score="$1"
  if [[ $score -le 10 ]]; then
    echo "A"
  elif [[ $score -le 25 ]]; then
    echo "B"
  elif [[ $score -le 50 ]]; then
    echo "C"
  elif [[ $score -le 75 ]]; then
    echo "D"
  else
    echo "F"
  fi
}

# Color for a given grade
grade_color() {
  local grade="$1"
  case "$grade" in
    A) echo "$GREEN" ;;
    B) echo "$GREEN" ;;
    C) echo "$YELLOW" ;;
    D) echo "$RED" ;;
    F) echo "$RED" ;;
    *) echo "$NC" ;;
  esac
}

# Color for a given severity
severity_color() {
  local sev="$1"
  case "$sev" in
    critical) echo "$RED" ;;
    high)     echo "$MAGENTA" ;;
    medium)   echo "$YELLOW" ;;
    low)      echo "$CYAN" ;;
    *)        echo "$NC" ;;
  esac
}

# Severity label padded
severity_label() {
  local sev="$1"
  case "$sev" in
    critical) echo "CRITICAL" ;;
    high)     echo "HIGH    " ;;
    medium)   echo "MEDIUM  " ;;
    low)      echo "LOW     " ;;
    *)        echo "UNKNOWN " ;;
  esac
}

# ─── Check Rollback Exists ──────────────────────────────────────────────────

# For a given migration file, check if a corresponding rollback/down migration exists.
# Outputs "found" or "missing".
check_rollback_exists() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local dirpath
  dirpath=$(dirname "$filepath")
  local ext="${basename_f##*.}"
  local framework
  framework=$(detect_framework "$filepath")

  case "$framework" in
    rails)
      # Rails uses reversible blocks or separate down methods inside the same file
      if grep -qE "def[[:space:]]+down|reversible[[:space:]]+do|change[[:space:]]+do" "$filepath" 2>/dev/null; then
        echo "found"
        return 0
      fi
      echo "missing"
      return 0
      ;;

    django)
      # Django auto-generates reverse operations; check for RunSQL with reverse_sql or RunPython with reverse_code
      # If the file has only auto-reversible operations, it is OK
      if grep -q "RunSQL" "$filepath" 2>/dev/null; then
        if grep -q "reverse_sql" "$filepath" 2>/dev/null; then
          echo "found"
        else
          echo "missing"
        fi
        return 0
      fi
      if grep -q "RunPython" "$filepath" 2>/dev/null; then
        if grep -q "reverse_code" "$filepath" 2>/dev/null; then
          echo "found"
        else
          echo "missing"
        fi
        return 0
      fi
      # Auto-reversible operations are fine
      echo "found"
      return 0
      ;;

    knex)
      # Knex: check for exports.down or down function
      if grep -qE "exports\.down|\.down[[:space:]]*=|async[[:space:]]+function[[:space:]]+down" "$filepath" 2>/dev/null; then
        echo "found"
        return 0
      fi
      echo "missing"
      return 0
      ;;

    sql|prisma|flyway)
      # SQL: look for a corresponding DOWN file
      # Flyway: V001__name.sql -> U001__name.sql (undo)
      # General: look for *down*.sql, *rollback*.sql, *revert*.sql
      local name_no_ext="${basename_f%.*}"

      # Flyway undo convention: V -> U
      if [[ "$basename_f" =~ ^V ]]; then
        local undo_file="${basename_f/V/U}"
        if [[ -f "$dirpath/$undo_file" ]]; then
          echo "found"
          return 0
        fi
      fi

      # General: look for companion down/rollback/revert file
      local search_name
      # Strip common prefixes like timestamp
      search_name=$(echo "$name_no_ext" | sed -E 's/^[0-9]+_?//')

      if ls "$dirpath"/*down*"$search_name"* 2>/dev/null | head -1 | grep -q . 2>/dev/null; then
        echo "found"
        return 0
      fi
      if ls "$dirpath"/*rollback*"$search_name"* 2>/dev/null | head -1 | grep -q . 2>/dev/null; then
        echo "found"
        return 0
      fi
      if ls "$dirpath"/*revert*"$search_name"* 2>/dev/null | head -1 | grep -q . 2>/dev/null; then
        echo "found"
        return 0
      fi

      # Check if the file itself contains both UP and DOWN sections
      if grep -qiE "^--[[:space:]]*down|^--[[:space:]]*rollback|^--[[:space:]]*revert" "$filepath" 2>/dev/null; then
        echo "found"
        return 0
      fi

      echo "missing"
      return 0
      ;;

    liquibase)
      # Liquibase: rollback tags inside changeset
      if grep -qE "<rollback" "$filepath" 2>/dev/null; then
        echo "found"
        return 0
      fi
      echo "missing"
      return 0
      ;;

    *)
      echo "missing"
      return 0
      ;;
  esac
}

# ─── Detect Missing Transactions ────────────────────────────────────────────

# Check if a SQL migration file is wrapped in BEGIN/COMMIT.
# Appends a finding to FINDINGS if not.
detect_missing_transactions() {
  local filepath="$1"

  # Skip non-SQL files
  local ext="${filepath##*.}"
  if [[ "$ext" != "sql" ]]; then
    return 0
  fi

  # Check for BEGIN/START TRANSACTION
  local has_begin=false
  if grep -qiE "^[[:space:]]*(BEGIN|START[[:space:]]+TRANSACTION)" "$filepath" 2>/dev/null; then
    has_begin=true
  fi

  # Check for COMMIT
  local has_commit=false
  if grep -qiE "^[[:space:]]*COMMIT" "$filepath" 2>/dev/null; then
    has_commit=true
  fi

  if [[ "$has_begin" == false || "$has_commit" == false ]]; then
    # Only flag if the file has actual DDL statements
    if grep -qiE "(CREATE|ALTER|DROP|TRUNCATE|INSERT|UPDATE|DELETE)" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|missing_transaction|Migration not wrapped in BEGIN/COMMIT — Partial failures leave database in inconsistent state|Wrap all migration statements in BEGIN; ... COMMIT; to ensure atomicity. PostgreSQL DDL is transactional; MySQL InnoDB DDL is not.|Missing BEGIN/COMMIT block")
    fi
  fi
}

# ─── Detect Lock Hazards ────────────────────────────────────────────────────

# Check for CREATE INDEX without CONCURRENTLY in SQL files.
detect_lock_hazards() {
  local filepath="$1"
  local ext="${filepath##*.}"

  if [[ "$ext" != "sql" ]]; then
    return 0
  fi

  # CREATE INDEX without CONCURRENTLY
  local matches
  matches=$(grep -nE "CREATE[[:space:]]+INDEX[[:space:]]+(IF[[:space:]]+NOT[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_]" "$filepath" 2>/dev/null || true)

  if [[ -n "$matches" ]]; then
    while IFS= read -r match_line; do
      local line_num="${match_line%%:*}"
      local matched_text="${match_line#*:}"

      # Check if this line already has CONCURRENTLY
      if ! echo "$matched_text" | grep -qi "CONCURRENTLY"; then
        # Only flag if not already caught by pattern matching
        local already_found=false
        for existing in "${FINDINGS[@]:-}"; do
          if [[ "$existing" == *"${filepath}|${line_num}|"*"index_no_concurrent"* ]]; then
            already_found=true
            break
          fi
        done
        if [[ "$already_found" == false ]]; then
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi
          FINDINGS+=("${filepath}|${line_num}|medium|lock_hazard|CREATE INDEX without CONCURRENTLY — Acquires exclusive lock, blocks writes during index build|Use CREATE INDEX CONCURRENTLY to avoid blocking. Note: CONCURRENTLY cannot run inside a transaction block.|${matched_text}")
        fi
      fi
    done <<< "$matches"
  fi

  # ALTER TABLE on tables - potential lock on large tables
  local alter_matches
  alter_matches=$(grep -ncE "^[[:space:]]*ALTER[[:space:]]+TABLE" "$filepath" 2>/dev/null || echo "0")

  if [[ "$alter_matches" -gt 3 ]]; then
    FINDINGS+=("${filepath}|1|medium|multiple_alters|$alter_matches ALTER TABLE statements in single migration — Each ALTER acquires a lock; batching can cause extended lock time|Split ALTER TABLE statements into separate migrations to minimize lock duration. Consider using pg_repack or pt-online-schema-change for large tables.|Multiple ALTER TABLE statements detected")
  fi
}

# ─── Estimate Table References ───────────────────────────────────────────────

# Count how many distinct tables are referenced in a migration file.
estimate_table_references() {
  local filepath="$1"
  local framework
  framework=$(detect_framework "$filepath")

  local tables=0
  case "$framework" in
    sql|prisma|flyway)
      # Count unique table names after CREATE TABLE, ALTER TABLE, DROP TABLE, etc.
      tables=$(grep -oiE "(CREATE|ALTER|DROP|TRUNCATE|INSERT[[:space:]]+INTO|UPDATE|DELETE[[:space:]]+FROM)[[:space:]]+(TABLE[[:space:]]+)?(IF[[:space:]]+(NOT[[:space:]]+)?EXISTS[[:space:]]+)?[A-Za-z_\"\`\[]+" "$filepath" 2>/dev/null \
        | sed -E 's/.*(TABLE[[:space:]]+)?(IF[[:space:]]+(NOT[[:space:]]+)?EXISTS[[:space:]]+)?//' \
        | tr -d '"`[' \
        | sort -u \
        | wc -l)
      ;;
    rails)
      tables=$(grep -oE "(create_table|drop_table|add_column|remove_column|change_column|rename_column|add_index|remove_index|add_reference|remove_reference|rename_table)[[:space:]]*[:(][[:space:]]*:?[A-Za-z_]+" "$filepath" 2>/dev/null \
        | sed -E 's/.*[:(][[:space:]]*:?//' \
        | sort -u \
        | wc -l)
      ;;
    django)
      tables=$(grep -oE "(model_name|name)[[:space:]]*=[[:space:]]*['\"][A-Za-z_]+" "$filepath" 2>/dev/null \
        | sed -E "s/.*=[[:space:]]*['\"]?//" \
        | sort -u \
        | wc -l)
      ;;
    knex)
      tables=$(grep -oE "\.(createTable|dropTable|table|alterTable|renameTable)[[:space:]]*\([[:space:]]*['\"][A-Za-z_]+" "$filepath" 2>/dev/null \
        | sed -E "s/.*\([[:space:]]*['\"]?//" \
        | sort -u \
        | wc -l)
      ;;
    liquibase)
      tables=$(grep -oE "tableName=\"[A-Za-z_]+" "$filepath" 2>/dev/null \
        | sed 's/tableName="//' \
        | sort -u \
        | wc -l)
      ;;
  esac

  echo "${tables:-0}"
}

# ─── Format Finding ─────────────────────────────────────────────────────────

# Pretty-print a single finding with color, file, line, severity, description.
format_finding() {
  local finding="$1"
  IFS='|' read -r f_file f_line f_severity f_category f_desc f_rec f_text <<< "$finding"

  local color
  color=$(severity_color "$f_severity")
  local label
  label=$(severity_label "$f_severity")

  local relative_file
  relative_file=$(basename "$f_file")

  echo -e "  ${color}${BOLD}${label}${NC}  ${relative_file}:${f_line}"
  echo -e "           ${f_desc}"
  if [[ -n "${f_text:-}" ]]; then
    echo -e "           ${DIM}> ${f_text}${NC}"
  fi
  echo -e "           ${DIM}Recommendation: ${f_rec}${NC}"
  echo ""
}

# ─── Print Summary ───────────────────────────────────────────────────────────

# Print scan summary: total issues by severity, risk score, grade.
print_summary() {
  local files_scanned="$1"
  local risk_score="$2"

  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done

  local total=$((critical + high + medium + low))
  local grade
  grade=$(risk_grade "$risk_score")
  local gcolor
  gcolor=$(grade_color "$grade")

  echo -e "${BOLD}━━━ Scan Summary ━━━${NC}"
  echo ""
  echo -e "  Files scanned:  ${BOLD}$files_scanned${NC}"
  echo -e "  Total issues:   ${BOLD}$total${NC}"
  if [[ $critical -gt 0 ]]; then
    echo -e "    Critical:     ${RED}${BOLD}$critical${NC}"
  else
    echo -e "    Critical:     ${DIM}$critical${NC}"
  fi
  if [[ $high -gt 0 ]]; then
    echo -e "    High:         ${MAGENTA}${BOLD}$high${NC}"
  else
    echo -e "    High:         ${DIM}$high${NC}"
  fi
  if [[ $medium -gt 0 ]]; then
    echo -e "    Medium:       ${YELLOW}$medium${NC}"
  else
    echo -e "    Medium:       ${DIM}$medium${NC}"
  fi
  if [[ $low -gt 0 ]]; then
    echo -e "    Low:          ${CYAN}$low${NC}"
  else
    echo -e "    Low:          ${DIM}$low${NC}"
  fi
  echo ""
  echo -e "  Risk Score:     ${gcolor}${BOLD}$risk_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $critical -gt 0 || $high -gt 0 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} — Destructive operations detected. Review findings above."
  elif [[ $medium -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} — Potential issues found. Review recommended."
  elif [[ $total -eq 0 ]]; then
    echo -e "  ${GREEN}${BOLD}PASS${NC} — No destructive operations detected."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} — Low severity items only. Likely safe to proceed."
  fi
}

# ─── Hook Entry Point ───────────────────────────────────────────────────────

# Pre-commit hook entry point. Scans staged migration files via git diff.
# Returns exit code 1 if critical or high severity findings.
hook_migration_scan() {
  # Get staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  # Filter for migration files only
  local -a migration_staged=()
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue

    local ext="${file##*.}"
    local is_migration=false

    # Check extension
    for valid_ext in "${MIGRATION_FILE_EXTENSIONS[@]}"; do
      if [[ "$ext" == "$valid_ext" ]]; then
        is_migration=true
        break
      fi
    done

    if [[ "$is_migration" == false ]]; then
      continue
    fi

    # Check if file is in a migration directory or has migration-like name
    local dir_of_file
    dir_of_file=$(dirname "$file")
    if echo "$dir_of_file" | grep -qiE "migrat|changeset|alembic|flyway|schema|db/migrate|prisma"; then
      migration_staged+=("$file")
    elif echo "$file" | grep -qE "^[0-9]{8,14}|V[0-9]+|[0-9]+_"; then
      migration_staged+=("$file")
    fi
  done <<< "$staged_files"

  if [[ ${#migration_staged[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[MigrateSafe]${NC} Scanning ${#migration_staged[@]} staged migration file(s)..."

  declare -a FINDINGS=()
  local has_critical_or_high=false

  for file in "${migration_staged[@]}"; do
    if [[ -f "$file" ]]; then
      analyze_migration_file "$file"
    fi
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[MigrateSafe]${NC} All staged migrations look safe."
    return 0
  fi

  echo ""
  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
    fi
  done

  local risk_score
  risk_score=$(calculate_risk_score)

  print_summary "${#migration_staged[@]}" "$risk_score"

  if [[ "$has_critical_or_high" == true ]]; then
    return 1
  fi

  return 0
}

# ─── Main Scan Orchestrator ─────────────────────────────────────────────────

# Main scan entry point. Finds migration files, analyzes each, aggregates results.
# Usage: do_migration_scan <target> <max_files>
# max_files=0 means unlimited
do_migration_scan() {
  local target="$1"
  local max_files="${2:-0}"

  # Find migration files
  local -a migration_files=()
  find_migration_files "$target" migration_files

  if [[ ${#migration_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[MigrateSafe]${NC} No migration files found in ${BOLD}$target${NC}"
    echo -e "${DIM}  Searched for: *.sql, *.rb, *.py, *.js, *.ts, *.xml${NC}"
    echo -e "${DIM}  In directories: db/migrate, migrations, prisma/migrations, sql, etc.${NC}"
    return 0
  fi

  # Apply file limit
  local files_to_scan=("${migration_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#migration_files[@]} -gt $max_files ]]; then
    files_to_scan=("${migration_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "Found ${BOLD}${#migration_files[@]}${NC} migration file(s)"
  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#migration_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://migratesafe.pages.dev${NC}"
  fi
  echo ""

  # Analyze each file
  declare -a FINDINGS=()
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local framework
    framework=$(detect_framework "$file")
    local tables
    tables=$(estimate_table_references "$file")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($framework, $tables table(s))${NC}"

    analyze_migration_file "$file"
  done

  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No destructive operations detected.${NC}"
    echo ""
    print_summary "$files_scanned" 0
    return 0
  fi

  echo -e "${BOLD}━━━ Findings ━━━${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
  done

  local risk_score
  risk_score=$(calculate_risk_score)

  print_summary "$files_scanned" "$risk_score"

  # Set exit code based on severity
  local has_critical_or_high=false
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
      break
    fi
  done

  if [[ "$has_critical_or_high" == true ]]; then
    return 1
  fi

  return 0
}

# ─── Schema Diff ─────────────────────────────────────────────────────────────

# Compare two SQL schema files and highlight dangerous changes.
# Usage: do_schema_diff <file1> <file2>
do_schema_diff() {
  local file1="$1"
  local file2="$2"

  # Extract tables from each file
  local -a tables_old=()
  local -a tables_new=()

  while IFS= read -r tbl; do
    [[ -n "$tbl" ]] && tables_old+=("$tbl")
  done < <(grep -oiE "CREATE[[:space:]]+TABLE[[:space:]]+(IF[[:space:]]+NOT[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_\"\`\[]+" "$file1" 2>/dev/null \
    | sed -E 's/CREATE[[:space:]]+TABLE[[:space:]]+(IF[[:space:]]+NOT[[:space:]]+EXISTS[[:space:]]+)?//' \
    | tr -d '"`[' \
    | sort -u)

  while IFS= read -r tbl; do
    [[ -n "$tbl" ]] && tables_new+=("$tbl")
  done < <(grep -oiE "CREATE[[:space:]]+TABLE[[:space:]]+(IF[[:space:]]+NOT[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_\"\`\[]+" "$file2" 2>/dev/null \
    | sed -E 's/CREATE[[:space:]]+TABLE[[:space:]]+(IF[[:space:]]+NOT[[:space:]]+EXISTS[[:space:]]+)?//' \
    | tr -d '"`[' \
    | sort -u)

  local exit_code=0

  echo -e "${BOLD}━━━ Schema Comparison ━━━${NC}"
  echo ""

  # Find dropped tables (in old, not in new)
  local dropped_count=0
  for old_tbl in "${tables_old[@]:-}"; do
    [[ -z "$old_tbl" ]] && continue
    local found=false
    for new_tbl in "${tables_new[@]:-}"; do
      if [[ "$old_tbl" == "$new_tbl" ]]; then
        found=true
        break
      fi
    done
    if [[ "$found" == false ]]; then
      echo -e "  ${RED}${BOLD}DROPPED${NC}  Table ${BOLD}$old_tbl${NC} exists in old schema but not in new"
      dropped_count=$((dropped_count + 1))
      exit_code=1
    fi
  done

  # Find new tables (in new, not in old)
  local added_count=0
  for new_tbl in "${tables_new[@]:-}"; do
    [[ -z "$new_tbl" ]] && continue
    local found=false
    for old_tbl in "${tables_old[@]:-}"; do
      if [[ "$old_tbl" == "$new_tbl" ]]; then
        found=true
        break
      fi
    done
    if [[ "$found" == false ]]; then
      echo -e "  ${GREEN}${BOLD}ADDED${NC}    Table ${BOLD}$new_tbl${NC}"
      added_count=$((added_count + 1))
    fi
  done

  # For tables that exist in both, compare column definitions
  local modified_count=0
  for old_tbl in "${tables_old[@]:-}"; do
    [[ -z "$old_tbl" ]] && continue
    local exists_in_new=false
    for new_tbl in "${tables_new[@]:-}"; do
      if [[ "$old_tbl" == "$new_tbl" ]]; then
        exists_in_new=true
        break
      fi
    done

    if [[ "$exists_in_new" == true ]]; then
      # Extract column lines for this table from both files
      # This is a simplified comparison — extract block between CREATE TABLE name and next );
      local old_cols new_cols
      old_cols=$(sed -n "/CREATE[[:space:]]*TABLE[[:space:]]*[^;]*${old_tbl}/I,/);/p" "$file1" 2>/dev/null | grep -vE "CREATE|^\)" | sed 's/^[[:space:]]*//' | sort)
      new_cols=$(sed -n "/CREATE[[:space:]]*TABLE[[:space:]]*[^;]*${old_tbl}/I,/);/p" "$file2" 2>/dev/null | grep -vE "CREATE|^\)" | sed 's/^[[:space:]]*//' | sort)

      if [[ "$old_cols" != "$new_cols" ]]; then
        echo -e "  ${YELLOW}${BOLD}MODIFIED${NC} Table ${BOLD}$old_tbl${NC} — column definitions changed"

        # Find removed columns
        local old_col_names new_col_names
        old_col_names=$(echo "$old_cols" | grep -oE "^[A-Za-z_]+" | sort -u)
        new_col_names=$(echo "$new_cols" | grep -oE "^[A-Za-z_]+" | sort -u)

        while IFS= read -r col; do
          [[ -z "$col" ]] && continue
          if ! echo "$new_col_names" | grep -qw "$col"; then
            echo -e "           ${RED}- Column ${BOLD}$col${NC}${RED} removed${NC}"
            exit_code=1
          fi
        done <<< "$old_col_names"

        # Find added columns
        while IFS= read -r col; do
          [[ -z "$col" ]] && continue
          if ! echo "$old_col_names" | grep -qw "$col"; then
            echo -e "           ${GREEN}+ Column ${BOLD}$col${NC}${GREEN} added${NC}"
          fi
        done <<< "$new_col_names"

        # Find type changes
        while IFS= read -r col; do
          [[ -z "$col" ]] && continue
          if echo "$new_col_names" | grep -qw "$col"; then
            local old_def new_def
            old_def=$(echo "$old_cols" | grep -E "^${col}[[:space:]]" | head -1)
            new_def=$(echo "$new_cols" | grep -E "^${col}[[:space:]]" | head -1)
            if [[ "$old_def" != "$new_def" && -n "$old_def" && -n "$new_def" ]]; then
              echo -e "           ${YELLOW}~ Column ${BOLD}$col${NC}${YELLOW} changed${NC}"
              echo -e "             ${DIM}old: $old_def${NC}"
              echo -e "             ${DIM}new: $new_def${NC}"
              exit_code=1
            fi
          fi
        done <<< "$old_col_names"

        modified_count=$((modified_count + 1))
      fi
    fi
  done

  echo ""
  echo -e "${BOLD}━━━ Diff Summary ━━━${NC}"
  echo ""
  echo -e "  Tables in old schema: ${BOLD}${#tables_old[@]}${NC}"
  echo -e "  Tables in new schema: ${BOLD}${#tables_new[@]}${NC}"
  echo -e "  Dropped:  ${RED}$dropped_count${NC}"
  echo -e "  Added:    ${GREEN}$added_count${NC}"
  echo -e "  Modified: ${YELLOW}$modified_count${NC}"

  if [[ $dropped_count -gt 0 ]]; then
    echo ""
    echo -e "  ${RED}${BOLD}WARNING:${NC} $dropped_count table(s) will be permanently dropped."
    echo -e "  ${DIM}Ensure data has been backed up or migrated before applying.${NC}"
  fi

  return $exit_code
}

# ─── History Scan ────────────────────────────────────────────────────────────

# Scan all migrations chronologically, build risk timeline.
# Usage: do_history_scan <target>
do_history_scan() {
  local target="$1"

  local -a migration_files=()
  find_migration_files "$target" migration_files

  if [[ ${#migration_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[MigrateSafe]${NC} No migration files found."
    return 0
  fi

  echo -e "${BOLD}━━━ Migration Risk Timeline ━━━${NC}"
  echo ""
  printf "  ${BOLD}%-40s %-12s %-8s %-8s${NC}\n" "Migration" "Framework" "Risk" "Grade"
  echo -e "  ${DIM}$(printf '%.0s─' {1..72})${NC}"

  local cumulative_score=0
  local total_findings_count=0
  local highest_risk=0

  for file in "${migration_files[@]}"; do
    declare -a FINDINGS=()

    local framework
    framework=$(detect_framework "$file")
    analyze_migration_file "$file"

    local file_score=0
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
      local points
      points=$(severity_to_risk "$severity")
      file_score=$((file_score + points))
      total_findings_count=$((total_findings_count + 1))
    done

    if [[ $file_score -gt 100 ]]; then
      file_score=100
    fi

    cumulative_score=$((cumulative_score + file_score))
    if [[ $file_score -gt $highest_risk ]]; then
      highest_risk=$file_score
    fi

    local grade
    grade=$(risk_grade "$file_score")
    local gcolor
    gcolor=$(grade_color "$grade")

    local display_name
    display_name=$(basename "$file")
    if [[ ${#display_name} -gt 38 ]]; then
      display_name="${display_name:0:35}..."
    fi

    local issue_count=${#FINDINGS[@]}

    printf "  %-40s %-12s ${gcolor}%-8s${NC} ${gcolor}%-8s${NC}\n" "$display_name" "$framework" "$file_score/100" "$grade"

    unset FINDINGS
  done

  echo ""
  echo -e "${BOLD}━━━ Timeline Summary ━━━${NC}"
  echo ""

  local avg_score=0
  if [[ ${#migration_files[@]} -gt 0 ]]; then
    avg_score=$((cumulative_score / ${#migration_files[@]}))
  fi

  local overall_grade
  overall_grade=$(risk_grade "$avg_score")
  local overall_color
  overall_color=$(grade_color "$overall_grade")

  echo -e "  Total migrations:   ${BOLD}${#migration_files[@]}${NC}"
  echo -e "  Total findings:     ${BOLD}$total_findings_count${NC}"
  echo -e "  Average risk:       ${overall_color}${BOLD}$avg_score/100${NC} (Grade: ${overall_color}${BOLD}$overall_grade${NC})"
  echo -e "  Highest single:     ${BOLD}$highest_risk/100${NC}"
  echo -e "  Cumulative score:   ${BOLD}$cumulative_score${NC}"
  echo ""

  if [[ $avg_score -gt 50 ]]; then
    echo -e "  ${RED}${BOLD}HIGH RISK${NC} — This project has a pattern of risky migrations."
    echo -e "  ${DIM}Consider adding pre-commit hooks: migratesafe hooks install${NC}"
  elif [[ $avg_score -gt 25 ]]; then
    echo -e "  ${YELLOW}${BOLD}MODERATE RISK${NC} — Some migrations need attention."
  else
    echo -e "  ${GREEN}${BOLD}LOW RISK${NC} — Migration history looks healthy."
  fi
}

# ─── Generate Report ─────────────────────────────────────────────────────────

# Generate a full markdown compliance report from the template.
# Usage: generate_report <target>
generate_report() {
  local target="$1"

  # Find and analyze all migration files
  local -a migration_files=()
  find_migration_files "$target" migration_files

  if [[ ${#migration_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[MigrateSafe]${NC} No migration files found. Nothing to report."
    return 0
  fi

  declare -a FINDINGS=()
  local files_scanned=0

  for file in "${migration_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    analyze_migration_file "$file"
  done

  local risk_score
  risk_score=$(calculate_risk_score)
  local grade
  grade=$(risk_grade "$risk_score")

  # Count by severity
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done
  local total=$((critical + high + medium + low))

  # Rollback coverage
  local total_rb=0
  local has_rb=0
  for file in "${migration_files[@]}"; do
    total_rb=$((total_rb + 1))
    local rb_result
    rb_result=$(check_rollback_exists "$file")
    if [[ "$rb_result" == "found" ]]; then
      has_rb=$((has_rb + 1))
    fi
  done
  local rollback_pct=0
  if [[ $total_rb -gt 0 ]]; then
    rollback_pct=$(( (has_rb * 100) / total_rb ))
  fi

  # Build findings section
  local findings_md=""
  if [[ $total -eq 0 ]]; then
    findings_md="No destructive operations detected. All migrations look safe."
  else
    for finding in "${FINDINGS[@]}"; do
      IFS='|' read -r f_file f_line f_severity f_category f_desc f_rec f_text <<< "$finding"
      local sev_upper
      sev_upper=$(echo "$f_severity" | tr '[:lower:]' '[:upper:]')
      findings_md+="### ${sev_upper}: ${f_category}"$'\n'
      findings_md+="- **File:** $(basename "$f_file"):${f_line}"$'\n'
      findings_md+="- **Issue:** ${f_desc}"$'\n'
      if [[ -n "${f_text:-}" ]]; then
        findings_md+="- **Code:** \`${f_text}\`"$'\n'
      fi
      findings_md+="- **Recommendation:** ${f_rec}"$'\n'
      findings_md+=""$'\n'
    done
  fi

  # Build rollback status section
  local rollback_md=""
  for file in "${migration_files[@]}"; do
    local rb_result
    rb_result=$(check_rollback_exists "$file")
    local rb_icon="[x]"
    if [[ "$rb_result" == "missing" ]]; then
      rb_icon="[ ]"
    fi
    rollback_md+="- ${rb_icon} $(basename "$file")"$'\n'
  done

  # Build recommendations section
  local recommendations_md=""
  if [[ $critical -gt 0 ]]; then
    recommendations_md+="- **URGENT:** $critical critical issue(s) found. These involve irreversible data destruction. Review and remediate before deploying."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). These may cause significant data or schema loss."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). These may cause operational problems."$'\n'
  fi
  if [[ $rollback_pct -lt 100 ]]; then
    recommendations_md+="- **ROLLBACK:** Only ${rollback_pct}% rollback coverage. Add rollback migrations for uncovered files."$'\n'
  fi
  if [[ $total -eq 0 && $rollback_pct -eq 100 ]]; then
    recommendations_md="No action items. All migrations are safe and have rollback coverage."
  fi
  if [[ -z "$recommendations_md" ]]; then
    recommendations_md="Review low severity items at your discretion. No blocking issues found."
  fi

  # Get project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || pwd)")

  # Read template and substitute
  local template_path="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_path" ]]; then
    echo -e "${RED}[MigrateSafe]${NC} Report template not found at $template_path"
    return 1
  fi

  local report
  report=$(cat "$template_path")

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{RISK_SCORE\}\}/$risk_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{ROLLBACK_PCT\}\}/$rollback_pct}"
  report="${report//\{\{VERSION\}\}/$MIGRATESAFE_VERSION}"

  # Multi-line substitutions need special handling
  report=$(echo "$report" | awk -v findings="$findings_md" '{gsub(/\{\{FINDINGS\}\}/, findings); print}')
  report=$(echo "$report" | awk -v rbstatus="$rollback_md" '{gsub(/\{\{ROLLBACK_STATUS\}\}/, rbstatus); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  # Output report
  local output_file="migratesafe-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[MigrateSafe]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:    $files_scanned"
  echo -e "  Total issues:     $total"
  echo -e "  Risk score:       $risk_score/100 (Grade: $grade)"
  echo -e "  Rollback coverage: ${rollback_pct}%"
}
