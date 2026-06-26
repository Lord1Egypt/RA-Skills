#!/usr/bin/env bash
# PerfGuard -- Core Performance Analysis Engine
# Provides: stack detection, source file discovery, anti-pattern scanning,
#           score calculation, report generation, hotspot identification,
#           budget enforcement, trend tracking, and pre-commit hook support.
#
# Sourced by perfguard.sh. Requires patterns.sh to be loaded first.

set -euo pipefail

# ─── Colors (safe to re-declare) ──────────────────────────────────────────────

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

PERFGUARD_VERSION="${VERSION:-1.0.0}"

# ─── Globals / Accumulators ──────────────────────────────────────────────────

TOTAL_FILES_SCANNED=0
TOTAL_ISSUES=0
CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0
ALL_FINDINGS=""
DETECTED_STACK="unknown"

# ─── Exclude directories ─────────────────────────────────────────────────────

EXCLUDE_DIRS=(".git" "node_modules" "dist" "build" "vendor" "__pycache__" ".next" ".nuxt" "coverage" ".venv" "venv" "env" ".tox" "target" ".gradle" ".mvn" ".idea" ".mypy_cache" ".pytest_cache" "migrations")

should_exclude() {
  local filepath="$1"
  local d
  for d in "${EXCLUDE_DIRS[@]}"; do
    if [[ "$filepath" == *"/$d/"* || "$filepath" == *"\\$d\\"* || "$filepath" == "$d/"* ]]; then
      return 0
    fi
  done
  return 1
}

# ─── Project Stack Detection ─────────────────────────────────────────────────
# Detect which languages and frameworks are present in the project.
# Returns a space-separated list of detected stacks.

detect_project_stack() {
  local target="$1"
  local stacks=""

  if [[ -f "$target" ]]; then
    # Single file detection
    local ext="${target##*.}"
    case "$ext" in
      py)   stacks="python" ;;
      js|ts|jsx|tsx|mjs|cjs) stacks="javascript" ;;
      rb)   stacks="ruby" ;;
      java) stacks="java" ;;
      *)    stacks="unknown" ;;
    esac
    echo "$stacks"
    return
  fi

  # Directory-level detection

  # Python
  if [[ -f "$target/requirements.txt" || -f "$target/pyproject.toml" || -f "$target/setup.py" || -f "$target/Pipfile" ]]; then
    stacks+="python "
  elif compgen -G "$target/*.py" &>/dev/null || compgen -G "$target/**/*.py" &>/dev/null; then
    stacks+="python "
  fi

  # JavaScript/TypeScript
  if [[ -f "$target/package.json" || -f "$target/tsconfig.json" ]]; then
    stacks+="javascript "
  elif compgen -G "$target/*.js" &>/dev/null || compgen -G "$target/*.ts" &>/dev/null; then
    stacks+="javascript "
  fi

  # Ruby
  if [[ -f "$target/Gemfile" || -f "$target/Rakefile" ]]; then
    stacks+="ruby "
  fi

  # Java
  if [[ -f "$target/pom.xml" || -f "$target/build.gradle" || -f "$target/build.gradle.kts" ]]; then
    stacks+="java "
  fi

  if [[ -z "$stacks" ]]; then
    stacks="unknown"
  fi

  echo "$stacks"
}

# Detect specific framework for a single file based on content
detect_file_stack() {
  local filepath="$1"
  local ext="${filepath##*.}"

  case "$ext" in
    py)       echo "python" ;;
    js|ts|jsx|tsx|mjs|cjs) echo "javascript" ;;
    rb)       echo "ruby" ;;
    java)     echo "java" ;;
    *)        echo "unknown" ;;
  esac
}

# ─── Source File Discovery ────────────────────────────────────────────────────
# Find relevant source files for performance scanning.

find_source_files() {
  local target="$1"
  local max_files="${2:-0}"  # 0 = unlimited
  local count=0

  if [[ -f "$target" ]]; then
    echo "$target"
    return
  fi

  local extensions=("py" "js" "ts" "jsx" "tsx" "rb" "java" "mjs" "cjs")

  local found_files=()
  local ext f
  for ext in "${extensions[@]}"; do
    while IFS= read -r f; do
      [[ -z "$f" ]] && continue
      should_exclude "$f" && continue
      found_files+=("$f")
    done < <(find "$target" -name "*.$ext" -type f 2>/dev/null)
  done

  # Score each file: prioritize files likely to have perf issues
  local scored_files=()
  local perf_keywords=("model" "models" "query" "queries" "service" "services" "handler" "handlers" "controller" "controllers" "api" "views" "view" "repository" "repo" "dao" "db" "database" "worker" "task" "tasks" "job" "jobs" "serializer" "serializers")

  for f in "${found_files[@]}"; do
    local base_lower
    base_lower=$(basename "$f" | tr '[:upper:]' '[:lower:]')
    local score=1  # All files get at least 1 (we scan everything)

    # Filename scoring
    local p
    for p in "${perf_keywords[@]}"; do
      if [[ "$base_lower" == *"$p"* ]]; then
        score=$((score + 10))
        break
      fi
    done

    # Directory scoring
    local dir_lower
    dir_lower=$(dirname "$f" | tr '[:upper:]' '[:lower:]')
    for p in "${perf_keywords[@]}"; do
      if [[ "$dir_lower" == *"$p"* ]]; then
        score=$((score + 5))
        break
      fi
    done

    # File size scoring: larger files are more likely to have issues
    local file_size
    file_size=$(wc -c < "$f" 2>/dev/null || echo 0)
    if [[ $file_size -gt 5000 ]]; then
      score=$((score + 3))
    fi

    scored_files+=("$score|$f")
  done

  # Sort by score descending and output
  local entry
  for entry in $(printf '%s\n' "${scored_files[@]}" | sort -t'|' -k1 -rn); do
    local file_path="${entry#*|}"
    echo "$file_path"
    count=$((count + 1))
    if [[ $max_files -gt 0 && $count -ge $max_files ]]; then
      return
    fi
  done
}

# ─── Pattern Scanning ─────────────────────────────────────────────────────────
# Run pattern arrays against a file and collect findings.

scan_file_with_patterns() {
  local filepath="$1"
  shift
  local pattern_arrays=("$@")
  local findings=""

  local arr_name
  for arr_name in "${pattern_arrays[@]}"; do
    # Get the array by reference
    local -n patterns_ref="$arr_name" 2>/dev/null || continue

    local entry
    for entry in "${patterns_ref[@]}"; do
      # Entry format: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
      local regex severity check_id description recommendation

      regex=$(echo "$entry" | cut -d'|' -f1)
      severity=$(echo "$entry" | cut -d'|' -f2)
      check_id=$(echo "$entry" | cut -d'|' -f3)
      description=$(echo "$entry" | cut -d'|' -f4)
      recommendation=$(echo "$entry" | cut -d'|' -f5)

      # Skip empty patterns
      [[ -z "$regex" ]] && continue

      # Search for the pattern
      local line_matches
      line_matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$line_matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local line_content="${match_line#*:}"
          # Trim long lines
          if [[ ${#line_content} -gt 120 ]]; then
            line_content="${line_content:0:120}..."
          fi

          findings+="$filepath|$line_num|$check_id|$severity|$description|$recommendation|$line_content"$'\n'

          # Increment counters
          TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
          case "$severity" in
            critical) CRITICAL_COUNT=$((CRITICAL_COUNT + 1)) ;;
            high)     HIGH_COUNT=$((HIGH_COUNT + 1)) ;;
            medium)   MEDIUM_COUNT=$((MEDIUM_COUNT + 1)) ;;
            low)      LOW_COUNT=$((LOW_COUNT + 1)) ;;
          esac
        done <<< "$line_matches"
      fi
    done
  done

  echo -n "$findings"
}

# ─── Scan a Single File ──────────────────────────────────────────────────────

scan_single_file() {
  local filepath="$1"
  local stack="${2:-}"

  if [[ -z "$stack" ]]; then
    stack=$(detect_file_stack "$filepath")
  fi

  # Determine which pattern arrays to scan with based on language
  local pattern_arrays=()

  case "$stack" in
    python)
      pattern_arrays+=("DB_NPLUS1_PATTERNS" "DB_SELECT_STAR_PATTERNS" "DB_EAGER_LOADING_PATTERNS")
      pattern_arrays+=("DB_UNBOUNDED_PATTERNS" "DB_SQL_CONCAT_PATTERNS" "DB_SEQUENTIAL_PATTERNS")
      pattern_arrays+=("PY_IMPORT_PATTERNS" "PY_STRING_PATTERNS" "PY_GENERATOR_PATTERNS")
      pattern_arrays+=("PY_ASYNC_PATTERNS" "PY_CONNECTION_PATTERNS" "PY_REGEX_PATTERNS")
      ;;
    javascript)
      pattern_arrays+=("DB_NPLUS1_PATTERNS" "DB_SELECT_STAR_PATTERNS" "DB_EAGER_LOADING_PATTERNS")
      pattern_arrays+=("DB_UNBOUNDED_PATTERNS" "DB_SQL_CONCAT_PATTERNS")
      pattern_arrays+=("JS_ASYNC_PATTERNS" "JS_PROMISE_PATTERNS" "JS_SYNC_IO_PATTERNS")
      pattern_arrays+=("JS_SERIALIZATION_PATTERNS" "JS_ARRAY_PATTERNS" "JS_MEMORY_PATTERNS")
      pattern_arrays+=("JS_REACT_PATTERNS" "JS_PAGINATION_PATTERNS" "JS_CONSOLE_PATTERNS")
      ;;
    ruby)
      pattern_arrays+=("DB_NPLUS1_PATTERNS" "DB_SELECT_STAR_PATTERNS" "DB_EAGER_LOADING_PATTERNS")
      pattern_arrays+=("DB_UNBOUNDED_PATTERNS" "DB_SQL_CONCAT_PATTERNS")
      ;;
    java)
      pattern_arrays+=("DB_NPLUS1_PATTERNS" "DB_SELECT_STAR_PATTERNS" "DB_EAGER_LOADING_PATTERNS")
      pattern_arrays+=("DB_UNBOUNDED_PATTERNS" "DB_SQL_CONCAT_PATTERNS")
      ;;
  esac

  # General patterns (always check)
  pattern_arrays+=("GEN_RETRY_PATTERNS" "GEN_TIMEOUT_PATTERNS" "GEN_POLLING_PATTERNS" "GEN_DELAY_PATTERNS" "GEN_CACHE_PATTERNS" "GEN_PAYLOAD_PATTERNS")

  # Load patterns if not already loaded
  if [[ -z "${DB_NPLUS1_PATTERNS+x}" ]]; then
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    source "$script_dir/patterns.sh"
  fi

  # Run scan
  local file_findings
  file_findings=$(scan_file_with_patterns "$filepath" "${pattern_arrays[@]}")

  TOTAL_FILES_SCANNED=$((TOTAL_FILES_SCANNED + 1))
  ALL_FINDINGS+="$file_findings"

  echo -n "$file_findings"
}

# ─── Performance Score Calculation ────────────────────────────────────────────
# Score 0-100 based on severity-weighted findings and file count

calculate_perf_score() {
  local total_files="${1:-$TOTAL_FILES_SCANNED}"
  local critical="${2:-$CRITICAL_COUNT}"
  local high="${3:-$HIGH_COUNT}"
  local medium="${4:-$MEDIUM_COUNT}"
  local low="${5:-$LOW_COUNT}"

  # Base score
  local score=100

  # Deductions (weighted)
  local penalty=0
  penalty=$((critical * 25 + high * 10 + medium * 4 + low * 1))

  # Scale penalty relative to number of files scanned (more files = smaller per-issue impact)
  if [[ $total_files -gt 0 ]]; then
    local adjusted_penalty=$(( (penalty * 10) / (total_files + 5) ))
    score=$((100 - adjusted_penalty))
  else
    score=$((100 - penalty))
  fi

  # Clamp to 0-100
  [[ $score -lt 0 ]] && score=0
  [[ $score -gt 100 ]] && score=100

  echo "$score"
}

get_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

get_score_color() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "$GREEN"
  elif [[ $score -ge 70 ]]; then echo "$YELLOW"
  else echo "$RED"
  fi
}

# ─── Output Formatting ───────────────────────────────────────────────────────

severity_color() {
  case "$1" in
    critical) echo "$RED" ;;
    high)     echo "$YELLOW" ;;
    medium)   echo "$BLUE" ;;
    low)      echo "$DIM" ;;
    *)        echo "$NC" ;;
  esac
}

severity_icon() {
  case "$1" in
    critical) echo "!!" ;;
    high)     echo "! " ;;
    medium)   echo "* " ;;
    low)      echo "- " ;;
    *)        echo "  " ;;
  esac
}

print_finding() {
  local filepath="$1" line_num="$2" check_id="$3" severity="$4" description="$5" recommendation="$6" line_content="$7"
  local color
  color=$(severity_color "$severity")
  local icon
  icon=$(severity_icon "$severity")

  echo -e "  ${icon} ${color}${BOLD}[${severity^^}]${NC} ${check_id}"
  echo -e "    ${DIM}${filepath}:${line_num}${NC}"
  echo -e "    ${description}"
  if [[ -n "$line_content" ]]; then
    echo -e "    ${DIM}> ${line_content}${NC}"
  fi
  echo -e "    ${CYAN}Fix: ${recommendation}${NC}"
  echo ""
}

print_findings_summary() {
  local findings="$1"
  [[ -z "$findings" ]] && return

  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local filepath line_num check_id severity description recommendation line_content
    IFS='|' read -r filepath line_num check_id severity description recommendation line_content <<< "$line"
    print_finding "$filepath" "$line_num" "$check_id" "$severity" "$description" "$recommendation" "$line_content"
  done <<< "$findings"
}

# ─── Main Scan Command ───────────────────────────────────────────────────────

do_perf_scan() {
  local target="$1"
  local max_files="${2:-0}"

  # Reset accumulators
  TOTAL_FILES_SCANNED=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Detect project stack
  DETECTED_STACK=$(detect_project_stack "$target")
  if [[ "$DETECTED_STACK" != "unknown" ]]; then
    echo -e "  Stack: ${BOLD}${DETECTED_STACK}${NC}"
  else
    echo -e "  Stack: ${DIM}auto-detect (all patterns)${NC}"
  fi

  # Find source files
  local source_files
  source_files=$(find_source_files "$target" "$max_files")

  if [[ -z "$source_files" ]]; then
    echo ""
    echo -e "  ${GREEN}+${NC} No source files found -- clean scan."
    echo -e "  ${DIM}Tip: run from your project root, or specify a source directory.${NC}"
    return 0
  fi

  local file_count=0
  local truncated=false
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    file_count=$((file_count + 1))
  done <<< "$source_files"

  if [[ $max_files -gt 0 && $file_count -ge $max_files ]]; then
    truncated=true
  fi

  echo -e "  Files: ${BOLD}${file_count}${NC} source file(s)"
  echo ""

  # Scan each file
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    local rel_path="${sf#$target/}"
    [[ "$rel_path" == "$sf" ]] && rel_path="$sf"

    echo -e "  ${DIM}Scanning: ${rel_path}${NC}"
    local file_stack
    file_stack=$(detect_file_stack "$sf")
    scan_single_file "$sf" "$file_stack"
  done <<< "$source_files"

  # Calculate score
  local score
  score=$(calculate_perf_score)
  local grade
  grade=$(get_grade "$score")
  local score_color
  score_color=$(get_score_color "$score")

  # Output summary
  echo ""
  echo -e "  ================================================================"
  echo -e "  ${BOLD}PerfGuard Performance Scan Results${NC}"
  echo -e "  ================================================================"
  echo ""
  echo -e "  Performance Score: ${score_color}${BOLD}${score}/100 (${grade})${NC}"
  echo ""
  echo -e "  ${DIM}Files scanned:${NC}  ${TOTAL_FILES_SCANNED}"
  echo -e "  ${DIM}Total issues:${NC}   ${TOTAL_ISSUES}"

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo ""
    [[ $CRITICAL_COUNT -gt 0 ]] && echo -e "  ${RED}!! Critical:${NC}  ${CRITICAL_COUNT}"
    [[ $HIGH_COUNT -gt 0 ]]     && echo -e "  ${YELLOW}!  High:${NC}      ${HIGH_COUNT}"
    [[ $MEDIUM_COUNT -gt 0 ]]   && echo -e "  ${BLUE}*  Medium:${NC}    ${MEDIUM_COUNT}"
    [[ $LOW_COUNT -gt 0 ]]      && echo -e "  ${DIM}-  Low:${NC}       ${LOW_COUNT}"
  fi

  echo ""

  # Print detailed findings
  if [[ -n "$ALL_FINDINGS" ]]; then
    echo -e "  ${BOLD}Findings:${NC}"
    echo ""
    print_findings_summary "$ALL_FINDINGS"
  else
    echo -e "  ${GREEN}+ No performance anti-patterns found.${NC}"
  fi

  # Free tier warning
  if [[ "$truncated" == true ]]; then
    echo -e "  ${YELLOW}-----------------------------------------------------------${NC}"
    echo -e "  ${YELLOW}!${NC}  Free tier: scanned ${max_files} of ${file_count}+ source files."
    echo -e "  ${YELLOW}!${NC}  Upgrade to Pro for unlimited scanning: ${CYAN}https://perfguard.pages.dev/pricing${NC}"
    echo -e "  ${YELLOW}-----------------------------------------------------------${NC}"
    echo ""
  fi

  # Exit code: 0 if score >= 70 and no critical issues, 1 otherwise
  if [[ $score -lt 70 || $CRITICAL_COUNT -gt 0 ]]; then
    return 1
  fi
  return 0
}

# ─── Hook Scan (for lefthook pre-commit) ─────────────────────────────────────

hook_perf_scan() {
  echo -e "${BLUE}[PerfGuard]${NC} Scanning staged files for performance anti-patterns..."

  # Get staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    echo -e "${GREEN}[PerfGuard]${NC} No staged files to scan."
    return 0
  fi

  # Filter to relevant extensions
  local source_files=""
  local ext
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    ext="${sf##*.}"
    case "$ext" in
      js|ts|jsx|tsx|py|rb|java|mjs|cjs) source_files+="$sf"$'\n' ;;
    esac
  done <<< "$staged_files"

  if [[ -z "$source_files" ]]; then
    echo -e "${GREEN}[PerfGuard]${NC} No relevant source files in staged changes."
    return 0
  fi

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Reset counters
  TOTAL_FILES_SCANNED=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  # Scan each staged file
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    [[ ! -f "$sf" ]] && continue

    local stack
    stack=$(detect_file_stack "$sf")
    scan_single_file "$sf" "$stack"
  done <<< "$source_files"

  # Summary
  if [[ $CRITICAL_COUNT -gt 0 ]]; then
    echo -e "${RED}[PerfGuard]${NC} ${BOLD}${CRITICAL_COUNT} critical performance issue(s)${NC} found in staged files!"
    if [[ -n "$ALL_FINDINGS" ]]; then
      print_findings_summary "$ALL_FINDINGS"
    fi
    return 1
  fi

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo -e "${YELLOW}[PerfGuard]${NC} ${TOTAL_ISSUES} issue(s) found (${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
    return 0  # Non-critical issues don't block commit
  fi

  echo -e "${GREEN}[PerfGuard]${NC} + Staged files look clean. No performance anti-patterns detected."
  return 0
}

# ─── Generate Report (Pro+) ──────────────────────────────────────────────────

generate_report() {
  local target="$1"

  # Run full scan first
  echo -e "${BLUE}[PerfGuard]${NC} Running full performance scan..."
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Reset counters
  TOTAL_FILES_SCANNED=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  DETECTED_STACK=$(detect_project_stack "$target")

  local source_files
  source_files=$(find_source_files "$target" 0)

  if [[ -z "$source_files" ]]; then
    echo -e "${YELLOW}[PerfGuard]${NC} No source files found -- nothing to report."
    return 0
  fi

  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    local stack
    stack=$(detect_file_stack "$sf")
    scan_single_file "$sf" "$stack" >/dev/null
  done <<< "$source_files"

  local score
  score=$(calculate_perf_score)
  local grade
  grade=$(get_grade "$score")

  # Format findings for markdown
  local md_findings=""
  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local fp ln cid sev desc rec lc
      IFS='|' read -r fp ln cid sev desc rec lc <<< "$line"
      md_findings+="### ${sev^^}: ${cid}"$'\n'
      md_findings+="- **File:** \`${fp}:${ln}\`"$'\n'
      md_findings+="- **Severity:** ${sev}"$'\n'
      md_findings+="- **Description:** ${desc}"$'\n'
      md_findings+="- **Fix:** ${rec}"$'\n'
      [[ -n "$lc" ]] && md_findings+="- **Code:** \`${lc}\`"$'\n'
      md_findings+=""$'\n'
    done <<< "$ALL_FINDINGS"
  else
    md_findings="No performance anti-patterns found."$'\n'
  fi

  # Build recommendations
  local recommendations=""
  [[ $CRITICAL_COUNT -gt 0 ]] && recommendations+="- **URGENT:** Fix ${CRITICAL_COUNT} critical issue(s) immediately -- these cause measurable latency"$'\n'
  [[ $HIGH_COUNT -gt 0 ]] && recommendations+="- Fix ${HIGH_COUNT} high-severity issue(s) before next deployment"$'\n'
  [[ $MEDIUM_COUNT -gt 0 ]] && recommendations+="- Address ${MEDIUM_COUNT} medium-severity issue(s) in upcoming sprint"$'\n'
  [[ $LOW_COUNT -gt 0 ]] && recommendations+="- Review ${LOW_COUNT} low-severity finding(s) for best practices"$'\n'
  [[ -z "$recommendations" ]] && recommendations="No recommendations -- your code looks performant!"$'\n'

  # Load template and substitute
  local template_path="$script_dir/../templates/report.md.tmpl"
  local report_content
  if [[ -f "$template_path" ]]; then
    report_content=$(< "$template_path")
  else
    # Inline fallback
    report_content="# PerfGuard Performance Audit Report\n\n**Score:** {{PERF_SCORE}}/100 ({{GRADE}})\n\n## Findings\n\n{{FINDINGS}}\n\n## Recommendations\n\n{{RECOMMENDATIONS}}"
  fi

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd || echo "$target")")
  local today
  today=$(date +%Y-%m-%d)

  report_content="${report_content//\{\{DATE\}\}/$today}"
  report_content="${report_content//\{\{PROJECT\}\}/$project_name}"
  report_content="${report_content//\{\{PERF_SCORE\}\}/$score}"
  report_content="${report_content//\{\{GRADE\}\}/$grade}"
  report_content="${report_content//\{\{FILES_SCANNED\}\}/$TOTAL_FILES_SCANNED}"
  report_content="${report_content//\{\{TOTAL_ISSUES\}\}/$TOTAL_ISSUES}"
  report_content="${report_content//\{\{CRITICAL_COUNT\}\}/$CRITICAL_COUNT}"
  report_content="${report_content//\{\{HIGH_COUNT\}\}/$HIGH_COUNT}"
  report_content="${report_content//\{\{MEDIUM_COUNT\}\}/$MEDIUM_COUNT}"
  report_content="${report_content//\{\{LOW_COUNT\}\}/$LOW_COUNT}"
  report_content="${report_content//\{\{STACK\}\}/$DETECTED_STACK}"
  report_content="${report_content//\{\{FINDINGS\}\}/$md_findings}"
  report_content="${report_content//\{\{RECOMMENDATIONS\}\}/$recommendations}"
  report_content="${report_content//\{\{VERSION\}\}/$PERFGUARD_VERSION}"

  local report_file="PERFGUARD-REPORT.md"
  echo -e "$report_content" > "$report_file"

  echo -e "${GREEN}[PerfGuard]${NC} Report generated: ${BOLD}${report_file}${NC}"
  echo -e "  Score: ${score}/100 (${grade})"
  echo -e "  Issues: ${TOTAL_ISSUES} (${CRITICAL_COUNT} critical, ${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
}

# ─── Find Hotspots (Pro+) ────────────────────────────────────────────────────
# Identify files with the most performance anti-patterns.

find_hotspots() {
  local target="$1"

  echo -e "${BLUE}[PerfGuard]${NC} Analyzing performance hotspots..."

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  local source_files
  source_files=$(find_source_files "$target" 0)

  if [[ -z "$source_files" ]]; then
    echo -e "${YELLOW}[PerfGuard]${NC} No source files found."
    return 0
  fi

  # Track per-file issue counts
  declare -A file_issues
  declare -A file_critical
  declare -A file_high
  declare -A file_score

  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue

    # Reset per-file counters
    TOTAL_FILES_SCANNED=0
    TOTAL_ISSUES=0
    CRITICAL_COUNT=0
    HIGH_COUNT=0
    MEDIUM_COUNT=0
    LOW_COUNT=0
    ALL_FINDINGS=""

    local stack
    stack=$(detect_file_stack "$sf")
    scan_single_file "$sf" "$stack" >/dev/null

    if [[ $TOTAL_ISSUES -gt 0 ]]; then
      local rel="${sf#$target/}"
      [[ "$rel" == "$sf" ]] && rel="$sf"
      local weight=$((CRITICAL_COUNT * 25 + HIGH_COUNT * 10 + MEDIUM_COUNT * 4 + LOW_COUNT * 1))
      file_issues["$rel"]="$TOTAL_ISSUES"
      file_critical["$rel"]="$CRITICAL_COUNT"
      file_high["$rel"]="$HIGH_COUNT"
      file_score["$rel"]="$weight"
    fi
  done <<< "$source_files"

  if [[ ${#file_issues[@]} -eq 0 ]]; then
    echo ""
    echo -e "  ${GREEN}+ No performance hotspots found. Your code looks clean!${NC}"
    return 0
  fi

  # Sort by weighted score and show top 10
  echo ""
  echo -e "  ${BOLD}Performance Hotspots (ranked by severity-weighted issue count)${NC}"
  echo -e "  ================================================================"
  echo ""
  echo -e "  ${BOLD}Rank  Score  Crit  High  Total  File${NC}"
  echo -e "  ----  -----  ----  ----  -----  ----"

  local rank=0
  local sorted_files
  sorted_files=$(for f in "${!file_score[@]}"; do echo "${file_score[$f]}|$f"; done | sort -t'|' -k1 -rn)

  while IFS= read -r entry; do
    [[ -z "$entry" ]] && continue
    rank=$((rank + 1))
    [[ $rank -gt 10 ]] && break

    local weight="${entry%%|*}"
    local filepath="${entry#*|}"
    local total="${file_issues[$filepath]:-0}"
    local crit="${file_critical[$filepath]:-0}"
    local high="${file_high[$filepath]:-0}"

    local color="$NC"
    [[ $crit -gt 0 ]] && color="$RED"
    [[ $crit -eq 0 && $high -gt 0 ]] && color="$YELLOW"

    printf "  ${color}%-4s  %-5s  %-4s  %-4s  %-5s  %s${NC}\n" \
      "#$rank" "$weight" "$crit" "$high" "$total" "$filepath"
  done <<< "$sorted_files"

  echo ""
  echo -e "  ${DIM}Score = (critical x 25) + (high x 10) + (medium x 4) + (low x 1)${NC}"
  echo ""
  echo -e "${GREEN}[PerfGuard]${NC} Hotspot analysis complete. Focus on the top-ranked files first."
}

# ─── Check Budget (Team+) ────────────────────────────────────────────────────
# Performance budget enforcement for CI/CD gates.

check_budget() {
  local target="$1"

  echo -e "${BLUE}[PerfGuard]${NC} Checking performance budgets..."

  # Default budgets (can be overridden via config)
  local budget_max_critical=0
  local budget_max_total=20
  local budget_min_score=70

  # Try to read budget config from openclaw.json
  local config_file="${HOME}/.openclaw/openclaw.json"
  if [[ -f "$config_file" ]]; then
    local cfg_max_critical cfg_max_total cfg_min_score
    if command -v python3 &>/dev/null; then
      cfg_max_critical=$(python3 -c "
import json
try:
    with open('$config_file') as f:
        cfg = json.load(f)
    print(cfg.get('skills',{}).get('entries',{}).get('perfguard',{}).get('config',{}).get('budgets',{}).get('maxCritical',''))
except: pass
" 2>/dev/null)
      cfg_max_total=$(python3 -c "
import json
try:
    with open('$config_file') as f:
        cfg = json.load(f)
    print(cfg.get('skills',{}).get('entries',{}).get('perfguard',{}).get('config',{}).get('budgets',{}).get('maxTotal',''))
except: pass
" 2>/dev/null)
      cfg_min_score=$(python3 -c "
import json
try:
    with open('$config_file') as f:
        cfg = json.load(f)
    print(cfg.get('skills',{}).get('entries',{}).get('perfguard',{}).get('config',{}).get('budgets',{}).get('minScore',''))
except: pass
" 2>/dev/null)
    fi
    [[ -n "${cfg_max_critical:-}" ]] && budget_max_critical="$cfg_max_critical"
    [[ -n "${cfg_max_total:-}" ]] && budget_max_total="$cfg_max_total"
    [[ -n "${cfg_min_score:-}" ]] && budget_min_score="$cfg_min_score"
  fi

  # Run full scan
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  TOTAL_FILES_SCANNED=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  DETECTED_STACK=$(detect_project_stack "$target")
  local source_files
  source_files=$(find_source_files "$target" 0)

  if [[ -n "$source_files" ]]; then
    while IFS= read -r sf; do
      [[ -z "$sf" ]] && continue
      local stack
      stack=$(detect_file_stack "$sf")
      scan_single_file "$sf" "$stack" >/dev/null
    done <<< "$source_files"
  fi

  local score
  score=$(calculate_perf_score)

  # Check budgets
  local budget_passed=true

  echo ""
  echo -e "  ${BOLD}Performance Budget Report${NC}"
  echo -e "  ================================================================"
  echo ""

  # Check critical count
  if [[ $CRITICAL_COUNT -gt $budget_max_critical ]]; then
    echo -e "  ${RED}FAIL${NC}  Critical issues: ${CRITICAL_COUNT} (max: ${budget_max_critical})"
    budget_passed=false
  else
    echo -e "  ${GREEN}PASS${NC}  Critical issues: ${CRITICAL_COUNT} (max: ${budget_max_critical})"
  fi

  # Check total issues
  if [[ $TOTAL_ISSUES -gt $budget_max_total ]]; then
    echo -e "  ${RED}FAIL${NC}  Total issues: ${TOTAL_ISSUES} (max: ${budget_max_total})"
    budget_passed=false
  else
    echo -e "  ${GREEN}PASS${NC}  Total issues: ${TOTAL_ISSUES} (max: ${budget_max_total})"
  fi

  # Check score
  if [[ $score -lt $budget_min_score ]]; then
    echo -e "  ${RED}FAIL${NC}  Performance score: ${score} (min: ${budget_min_score})"
    budget_passed=false
  else
    echo -e "  ${GREEN}PASS${NC}  Performance score: ${score} (min: ${budget_min_score})"
  fi

  echo ""

  if [[ "$budget_passed" == true ]]; then
    echo -e "  ${GREEN}${BOLD}All performance budgets passed.${NC}"
    return 0
  else
    echo -e "  ${RED}${BOLD}Performance budget exceeded.${NC}"
    echo -e "  ${DIM}Fix the issues above or adjust budgets in ~/.openclaw/openclaw.json${NC}"
    return 1
  fi
}

# ─── Show Trend (Team+) ──────────────────────────────────────────────────────
# Performance trend over recent git history.

show_trend() {
  local target="$1"

  if ! git rev-parse --git-dir &>/dev/null 2>&1; then
    echo -e "${RED}[PerfGuard]${NC} Not inside a git repository. Trend requires git history."
    return 1
  fi

  echo -e "${BLUE}[PerfGuard]${NC} Analyzing performance trend over recent commits..."

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  # Get last 10 commits
  local commits
  commits=$(git log --oneline -10 --format="%H %s" 2>/dev/null)

  if [[ -z "$commits" ]]; then
    echo -e "${YELLOW}[PerfGuard]${NC} No git history found."
    return 0
  fi

  local current_branch
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD")
  local current_commit
  current_commit=$(git rev-parse HEAD 2>/dev/null || echo "")

  echo ""
  echo -e "  ${BOLD}Performance Trend (last 10 commits)${NC}"
  echo -e "  ================================================================"
  echo ""
  echo -e "  ${BOLD}Commit    Score  Grade  Issues  Message${NC}"
  echo -e "  ------    -----  -----  ------  -------"

  local prev_score=""

  while IFS= read -r commit_line; do
    [[ -z "$commit_line" ]] && continue
    local commit_hash="${commit_line%% *}"
    local commit_msg="${commit_line#* }"
    local short_hash="${commit_hash:0:7}"

    # Truncate message
    if [[ ${#commit_msg} -gt 40 ]]; then
      commit_msg="${commit_msg:0:40}..."
    fi

    # Checkout commit silently
    git checkout "$commit_hash" --quiet 2>/dev/null || continue

    # Reset and scan
    TOTAL_FILES_SCANNED=0
    TOTAL_ISSUES=0
    CRITICAL_COUNT=0
    HIGH_COUNT=0
    MEDIUM_COUNT=0
    LOW_COUNT=0
    ALL_FINDINGS=""

    source "$script_dir/patterns.sh"

    local source_files
    source_files=$(find_source_files "$target" 0 2>/dev/null)

    if [[ -n "$source_files" ]]; then
      while IFS= read -r sf; do
        [[ -z "$sf" ]] && continue
        [[ ! -f "$sf" ]] && continue
        local stack
        stack=$(detect_file_stack "$sf")
        scan_single_file "$sf" "$stack" >/dev/null 2>/dev/null
      done <<< "$source_files"
    fi

    local score
    score=$(calculate_perf_score)
    local grade
    grade=$(get_grade "$score")
    local score_color
    score_color=$(get_score_color "$score")

    # Trend indicator
    local trend=""
    if [[ -n "$prev_score" ]]; then
      if [[ $score -gt $prev_score ]]; then
        trend="${GREEN}^${NC}"
      elif [[ $score -lt $prev_score ]]; then
        trend="${RED}v${NC}"
      else
        trend="${DIM}=${NC}"
      fi
    fi

    printf "  %-9s ${score_color}%-5s${NC}  %-5s  %-6s  %s %b\n" \
      "$short_hash" "$score" "$grade" "$TOTAL_ISSUES" "$commit_msg" "$trend"

    prev_score=$score
  done <<< "$commits"

  # Return to original branch
  if [[ -n "$current_commit" ]]; then
    git checkout "$current_branch" --quiet 2>/dev/null || \
    git checkout "$current_commit" --quiet 2>/dev/null || true
  fi

  echo ""
  echo -e "  ${DIM}^ = improved, v = degraded, = = unchanged${NC}"
  echo ""
  echo -e "${GREEN}[PerfGuard]${NC} Trend analysis complete."
}
