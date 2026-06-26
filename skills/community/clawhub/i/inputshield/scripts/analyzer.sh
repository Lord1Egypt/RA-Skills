#!/usr/bin/env bash
# InputShield -- Core Analysis Engine
# Provides: file discovery, pattern scanning, score calculation, grades,
#           report generation, category breakdown, tier-based access control,
#           JSON/HTML output, and hook integration.
#
# This file is sourced by dispatcher.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors (safe to re-declare; sourcing scripts may set these)
# ---------------------------------------------------------------------------

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
SKILL_DIR="${SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
INPUTSHIELD_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array -- each entry:
#   FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
declare -a FINDINGS=()

# Per-file tracking
declare -A FILE_FINDINGS_COUNT=()

# Per-category tracking
declare -A CATEGORY_COUNTS=()

# ============================================================================
# File Discovery
# ============================================================================

# Check if a file should be skipped (binary, generated, vendor, etc.)
should_skip_file() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
  local ext="${basename_lower##*.}"

  # Skip binary/image/compiled file extensions
  case "$ext" in
    png|jpg|jpeg|gif|bmp|ico|svg|webp|mp3|mp4|avi|mov|mkv|wav|flac|ogg) return 0 ;;
    zip|tar|gz|bz2|xz|7z|rar|tgz|zst) return 0 ;;
    exe|dll|so|dylib|o|a|class|pyc|pyo|wasm|deb|rpm) return 0 ;;
    woff|woff2|ttf|eot|otf) return 0 ;;
    pdf|doc|docx|xls|xlsx|ppt|pptx) return 0 ;;
    lock) return 0 ;;
    map) return 0 ;;
    sqlite|db|mdb) return 0 ;;
  esac

  # Skip minified files
  case "$basename_lower" in
    *.min.js|*.min.css|*.min.mjs) return 0 ;;
    *.bundle.js|*.chunk.js) return 0 ;;
  esac

  # Skip known non-source files
  case "$basename_lower" in
    package-lock.json|yarn.lock|pnpm-lock.yaml|composer.lock) return 0 ;;
    gemfile.lock|cargo.lock|poetry.lock|go.sum) return 0 ;;
    .ds_store|thumbs.db|desktop.ini) return 0 ;;
  esac

  return 1
}

# Check if a path is in a directory that should be skipped
is_excluded_dir() {
  local filepath="$1"

  case "$filepath" in
    */.git/*|*/.git) return 0 ;;
    */node_modules/*|*/node_modules) return 0 ;;
    */vendor/*|*/vendor) return 0 ;;
    */.next/*|*/.next) return 0 ;;
    */dist/*|*/dist) return 0 ;;
    */build/*|*/build) return 0 ;;
    */coverage/*|*/coverage) return 0 ;;
    */__pycache__/*|*/__pycache__) return 0 ;;
    */.venv/*|*/.venv) return 0 ;;
    */venv/*|*/venv) return 0 ;;
    */.tox/*|*/.tox) return 0 ;;
    */.eggs/*|*/.eggs) return 0 ;;
    */.terraform/*|*/.terraform) return 0 ;;
    */.cache/*|*/.cache) return 0 ;;
    */.gradle/*|*/.gradle) return 0 ;;
    */target/*|*/target) return 0 ;;
    */.mvn/*|*/.mvn) return 0 ;;
  esac

  return 1
}

# Check if a file is ignored by .gitignore
is_gitignored() {
  local filepath="$1"

  if command -v git &>/dev/null; then
    if git rev-parse --git-dir &>/dev/null 2>&1; then
      if git check-ignore -q "$filepath" 2>/dev/null; then
        return 0
      fi
    fi
  fi

  return 1
}

# Find all scannable files in a directory tree
find_scannable_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  # Single file
  if [[ -f "$search_dir" ]]; then
    if ! should_skip_file "$search_dir"; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  # Directory scan
  while IFS= read -r -d '' file; do
    is_excluded_dir "$file" && continue
    should_skip_file "$file" && continue
    is_gitignored "$file" && continue
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 10 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" \
       -o -name "dist" -o -name "build" -o -name "coverage" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name ".tox" -o -name ".terraform" \
       -o -name ".cache" -o -name ".gradle" -o -name "target" \) -prune -o \
    -type f -print0 2>/dev/null)
}

# ============================================================================
# Pattern Scanning
# ============================================================================

# scan_file <filepath> <per_category_limit> [category_filter]
#
# Scans a single file against all (or filtered) InputShield pattern categories.
# Appends findings to global FINDINGS array.
# Respects tier-based pattern limits via per_category_limit.
scan_file() {
  local filepath="$1"
  local per_category_limit="${2:-5}"
  local category_filter="${3:-}"

  local categories_to_scan="$INPUTSHIELD_CATEGORIES"
  if [[ -n "$category_filter" ]]; then
    categories_to_scan="$category_filter"
  fi

  local file_count=0

  for category in $categories_to_scan; do
    local arr_name
    arr_name=$(get_inputshield_patterns_for_category "$category")

    if [[ -z "$arr_name" ]]; then
      continue
    fi

    local -n _patterns_ref="$arr_name"
    local idx=0

    for entry in "${_patterns_ref[@]}"; do
      # Enforce tier-based limit per category
      if [[ $idx -ge $per_category_limit ]]; then
        break
      fi

      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Run grep -nE to find matches with line numbers
      local matches
      matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"

          # Trim whitespace
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

          # Truncate long matches
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi

          local finding="${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}"
          FINDINGS+=("$finding")
          file_count=$((file_count + 1))

          # Track per-category counts
          CATEGORY_COUNTS["$category"]=$(( ${CATEGORY_COUNTS["$category"]:-0} + 1 ))
        done <<< "$matches"
      fi

      idx=$((idx + 1))
    done
  done

  # Track per-file counts
  FILE_FINDINGS_COUNT["$filepath"]=$file_count
}

# ============================================================================
# Score Calculation & Grading
# ============================================================================

# Calculate input safety score based on findings.
# Score starts at 100 (clean) and decreases with each finding.
# Weights: critical=25, high=15, medium=8, low=3
calculate_score() {
  local score=100

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _file _line severity _check_id _desc _rec _text <<< "$finding"
    local points
    points=$(severity_to_points "$severity")
    score=$((score - points))
  done

  # Floor at 0
  if [[ $score -lt 0 ]]; then
    score=0
  fi

  echo "$score"
}

# Convert score to letter grade
# A(90-100), B(80-89), C(70-79), D(60-69), F(<60)
score_to_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

# Grade color for terminal output
grade_color() {
  local grade="$1"
  case "$grade" in
    A) echo "$GREEN" ;;
    B) echo "$GREEN" ;;
    C) echo "$YELLOW" ;;
    D) echo "$YELLOW" ;;
    F) echo "$RED" ;;
    *) echo "$NC" ;;
  esac
}

# Severity color for terminal output
severity_color() {
  local severity="$1"
  case "$severity" in
    critical) echo "$RED" ;;
    high)     echo "$MAGENTA" ;;
    medium)   echo "$YELLOW" ;;
    low)      echo "$CYAN" ;;
    *)        echo "$NC" ;;
  esac
}

# ============================================================================
# Output Formatting -- Text (Terminal)
# ============================================================================

# Print findings to stdout in colorized text format
print_findings_text() {
  local count=0
  local crit_count=0
  local high_count=0
  local med_count=0
  local low_count=0

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    count=$((count + 1))

    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac

    local sev_col
    sev_col=$(severity_color "$severity")

    echo -e "  ${sev_col}${severity^^}${NC} ${DIM}${check_id}${NC} ${file}:${line}"
    echo -e "    ${description}"
    echo -e "    ${DIM}Matched: ${matched_text}${NC}"
    echo -e "    ${DIM}Fix: ${recommendation}${NC}"
    echo ""
  done

  echo -e "${BOLD}--- Summary ---${NC}"
  echo -e "  Total findings: ${BOLD}$count${NC}"
  if [[ $crit_count -gt 0 ]]; then
    echo -e "  ${RED}Critical: $crit_count${NC}"
  fi
  if [[ $high_count -gt 0 ]]; then
    echo -e "  ${MAGENTA}High: $high_count${NC}"
  fi
  if [[ $med_count -gt 0 ]]; then
    echo -e "  ${YELLOW}Medium: $med_count${NC}"
  fi
  if [[ $low_count -gt 0 ]]; then
    echo -e "  ${CYAN}Low: $low_count${NC}"
  fi
}

# Print category breakdown
print_category_breakdown() {
  echo ""
  echo -e "${BOLD}--- Category Breakdown ---${NC}"
  for cat in $INPUTSHIELD_CATEGORIES; do
    local cat_count="${CATEGORY_COUNTS[$cat]:-0}"
    local cat_label
    cat_label=$(get_category_label "$cat")
    if [[ $cat_count -gt 0 ]]; then
      echo -e "  ${BOLD}$cat${NC} ($cat_label): ${BOLD}$cat_count${NC} findings"
    fi
  done
}

# Print score and grade
print_score() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local gc
  gc=$(grade_color "$grade")

  echo ""
  echo -e "${BOLD}Input Safety Score: ${gc}${score}/100${NC} (Grade: ${gc}${BOLD}${grade}${NC})"

  if [[ $score -ge 70 ]]; then
    echo -e "${GREEN}PASS${NC} -- Score is at or above threshold (70)"
  else
    echo -e "${RED}FAIL${NC} -- Score is below threshold (70)"
  fi
}

# ============================================================================
# Output Formatting -- JSON
# ============================================================================

# Output findings in JSON format
print_findings_json() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local total_files="$2"
  local tier="$3"

  # Count severities
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac
  done

  # Build JSON
  local json="{"
  json="${json}\"tool\":\"inputshield\","
  json="${json}\"version\":\"${INPUTSHIELD_VERSION}\","
  json="${json}\"tier\":\"${tier}\","
  json="${json}\"score\":${score},"
  json="${json}\"grade\":\"${grade}\","
  json="${json}\"pass\":$([ "$score" -ge 70 ] && echo "true" || echo "false"),"
  json="${json}\"threshold\":70,"
  json="${json}\"filesScanned\":${total_files},"
  json="${json}\"totalFindings\":${#FINDINGS[@]},"
  json="${json}\"severity\":{\"critical\":${crit_count},\"high\":${high_count},\"medium\":${med_count},\"low\":${low_count}},"

  # Category breakdown
  json="${json}\"categories\":{"
  local first_cat=true
  for cat in $INPUTSHIELD_CATEGORIES; do
    local cat_count="${CATEGORY_COUNTS[$cat]:-0}"
    if [[ "$first_cat" == true ]]; then
      first_cat=false
    else
      json="${json},"
    fi
    json="${json}\"${cat}\":${cat_count}"
  done
  json="${json}},"

  # Findings array
  json="${json}\"findings\":["
  local first_finding=true
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"

    # Escape special JSON characters in matched_text
    local escaped_text
    escaped_text=$(echo "$matched_text" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\r//g')

    local escaped_desc
    escaped_desc=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g')

    local escaped_rec
    escaped_rec=$(echo "$recommendation" | sed 's/\\/\\\\/g; s/"/\\"/g')

    if [[ "$first_finding" == true ]]; then
      first_finding=false
    else
      json="${json},"
    fi

    json="${json}{"
    json="${json}\"file\":\"${file}\","
    json="${json}\"line\":${line},"
    json="${json}\"severity\":\"${severity}\","
    json="${json}\"checkId\":\"${check_id}\","
    json="${json}\"description\":\"${escaped_desc}\","
    json="${json}\"recommendation\":\"${escaped_rec}\","
    json="${json}\"matchedText\":\"${escaped_text}\""
    json="${json}}"
  done
  json="${json}]"

  json="${json}}"

  echo "$json"
}

# ============================================================================
# Output Formatting -- HTML
# ============================================================================

# Output findings as an HTML report
print_findings_html() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local total_files="$2"
  local tier="$3"
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Count severities
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac
  done

  # Determine grade color
  local grade_css
  case "$grade" in
    A|B) grade_css="color:#22c55e" ;;
    C)   grade_css="color:#eab308" ;;
    D)   grade_css="color:#f97316" ;;
    F)   grade_css="color:#ef4444" ;;
  esac

  cat <<HTML_EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>InputShield Report -- ${date_str}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
           background: #0f172a; color: #e2e8f0; padding: 2rem; line-height: 1.6; }
    .container { max-width: 960px; margin: 0 auto; }
    h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.3rem; margin: 1.5rem 0 0.75rem; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; }
    .meta { color: #94a3b8; font-size: 0.875rem; margin-bottom: 1.5rem; }
    .score-box { background: #1e293b; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                 display: flex; align-items: center; gap: 1.5rem; }
    .grade { font-size: 3rem; font-weight: 800; ${grade_css}; }
    .score-details span { display: block; }
    .score-num { font-size: 1.5rem; font-weight: 600; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;
             font-weight: 600; text-transform: uppercase; }
    .badge-critical { background: #7f1d1d; color: #fca5a5; }
    .badge-high { background: #581c87; color: #d8b4fe; }
    .badge-medium { background: #713f12; color: #fde68a; }
    .badge-low { background: #164e63; color: #67e8f9; }
    table { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.875rem; }
    th { background: #1e293b; text-align: left; padding: 8px 12px; font-weight: 600; }
    td { padding: 8px 12px; border-bottom: 1px solid #1e293b; }
    tr:hover td { background: #1e293b; }
    .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0; }
    .summary-card { background: #1e293b; border-radius: 8px; padding: 1rem; text-align: center; }
    .summary-card .num { font-size: 1.5rem; font-weight: 700; }
    .pass { color: #22c55e; } .fail { color: #ef4444; }
    footer { margin-top: 2rem; text-align: center; color: #64748b; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>InputShield Report</h1>
    <div class="meta">Generated on ${date_str} | v${INPUTSHIELD_VERSION} | Tier: ${tier} | Files scanned: ${total_files}</div>

    <div class="score-box">
      <div class="grade">${grade}</div>
      <div class="score-details">
        <span class="score-num">${score}/100</span>
        <span class="$([ "$score" -ge 70 ] && echo 'pass' || echo 'fail')">$([ "$score" -ge 70 ] && echo 'PASS' || echo 'FAIL')</span>
      </div>
    </div>

    <div class="summary-grid">
      <div class="summary-card"><div class="num" style="color:#ef4444">${crit_count}</div><div>Critical</div></div>
      <div class="summary-card"><div class="num" style="color:#a855f7">${high_count}</div><div>High</div></div>
      <div class="summary-card"><div class="num" style="color:#eab308">${med_count}</div><div>Medium</div></div>
      <div class="summary-card"><div class="num" style="color:#06b6d4">${low_count}</div><div>Low</div></div>
    </div>

    <h2>Category Breakdown</h2>
    <table>
      <tr><th>Category</th><th>Findings</th></tr>
HTML_EOF

  for cat in $INPUTSHIELD_CATEGORIES; do
    local cat_count="${CATEGORY_COUNTS[$cat]:-0}"
    local cat_label
    cat_label=$(get_category_label "$cat")
    echo "      <tr><td>${cat} -- ${cat_label}</td><td>${cat_count}</td></tr>"
  done

  cat <<HTML_EOF2
    </table>

    <h2>Findings</h2>
    <table>
      <tr><th>#</th><th>File</th><th>Line</th><th>Severity</th><th>Check</th><th>Description</th></tr>
HTML_EOF2

  local idx=0
  for finding in "${FINDINGS[@]}"; do
    idx=$((idx + 1))
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"

    local badge_class="badge-${severity}"
    # Escape HTML entities
    local esc_desc
    esc_desc=$(echo "$description" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    local esc_file
    esc_file=$(echo "$file" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

    echo "      <tr><td>${idx}</td><td>${esc_file}</td><td>${line}</td><td><span class=\"badge ${badge_class}\">${severity}</span></td><td>${check_id}</td><td>${esc_desc}</td></tr>"
  done

  cat <<HTML_EOF3
    </table>

    <footer>
      <p>InputShield v${INPUTSHIELD_VERSION} -- <a href="https://inputshield.pages.dev" style="color:#64748b">inputshield.pages.dev</a></p>
    </footer>
  </div>
</body>
</html>
HTML_EOF3
}

# ============================================================================
# Report Generation (Pro+)
# ============================================================================

generate_inputshield_report() {
  local target="${1:-.}"
  local per_category_limit="${2:-10}"
  local category_filter="${3:-}"
  FINDINGS=()
  CATEGORY_COUNTS=()
  FILE_FINDINGS_COUNT=()

  # Discover files
  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[InputShield]${NC} No scannable files found."
    return 0
  fi

  echo -e "${BLUE}[InputShield]${NC} Scanning ${BOLD}$total_files${NC} files for report..." >&2

  for filepath in "${files[@]}"; do
    scan_file "$filepath" "$per_category_limit" "$category_filter"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Count severities
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac
  done

  local total_issues=${#FINDINGS[@]}

  # Build category breakdown for template
  local cat_breakdown=""
  for cat in $INPUTSHIELD_CATEGORIES; do
    local cat_count="${CATEGORY_COUNTS[$cat]:-0}"
    local cat_label
    cat_label=$(get_category_label "$cat")
    cat_breakdown="${cat_breakdown}| ${cat} -- ${cat_label} | ${cat_count} |"$'\n'
  done

  # Build findings table for template
  local findings_table=""
  local idx=0
  for finding in "${FINDINGS[@]}"; do
    idx=$((idx + 1))
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    findings_table="${findings_table}| ${idx} | ${file} | ${line} | ${severity} | ${check_id} | ${description} |"$'\n'
  done

  # Build recommendations
  local recommendations=""
  if [[ $crit_count -gt 0 ]]; then
    recommendations="${recommendations}1. **CRITICAL:** ${crit_count} critical vulnerabilities -- fix immediately to prevent exploitation"$'\n'
  fi
  if [[ $high_count -gt 0 ]]; then
    recommendations="${recommendations}2. **HIGH:** ${high_count} high-severity findings -- remediate in current sprint"$'\n'
  fi
  if [[ $med_count -gt 0 ]]; then
    recommendations="${recommendations}3. **MEDIUM:** ${med_count} medium findings -- review and address in upcoming work"$'\n'
  fi
  if [[ $low_count -gt 0 ]]; then
    recommendations="${recommendations}4. **LOW:** ${low_count} low findings -- review for false positives and handle as needed"$'\n'
  fi

  # Get project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")

  # Read template and substitute
  local template_file="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_file" ]]; then
    echo -e "${RED}[InputShield]${NC} Report template not found: $template_file" >&2
    return 1
  fi

  local report
  report=$(cat "$template_file")
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{VERSION\}\}/$INPUTSHIELD_VERSION}"
  report="${report//\{\{DATE\}\}/$date_str}"
  report="${report//\{\{INPUTSHIELD_SCORE\}\}/$score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$total_files}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total_issues}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$crit_count}"
  report="${report//\{\{HIGH_COUNT\}\}/$high_count}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$med_count}"
  report="${report//\{\{LOW_COUNT\}\}/$low_count}"
  report="${report//\{\{CATEGORY_BREAKDOWN\}\}/$cat_breakdown}"
  report="${report//\{\{FINDINGS_TABLE\}\}/$findings_table}"
  report="${report//\{\{RECOMMENDATIONS\}\}/$recommendations}"

  echo "$report"

  echo "" >&2
  echo -e "${GREEN}[InputShield]${NC} Report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Main Scan Function
# ============================================================================

# do_inputshield_scan <target> <per_category_limit> <format> <category_filter> <tier> <verbose>
do_inputshield_scan() {
  local target="${1:-.}"
  local per_category_limit="${2:-5}"
  local format="${3:-text}"
  local category_filter="${4:-}"
  local tier="${5:-free}"
  local verbose="${6:-false}"

  FINDINGS=()
  CATEGORY_COUNTS=()
  FILE_FINDINGS_COUNT=()

  # Discover files
  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    if [[ "$format" == "json" ]]; then
      echo '{"tool":"inputshield","score":100,"grade":"A","pass":true,"totalFindings":0,"findings":[]}'
    else
      echo -e "${GREEN}[InputShield]${NC} No scannable files found in ${BOLD}$target${NC}"
      echo -e "  Clean scan -- no files to check."
    fi
    return 0
  fi

  local total_patterns
  total_patterns=$(get_total_patterns "$tier" 2>/dev/null || echo "30")

  if [[ "$format" == "text" ]]; then
    echo -e "${BLUE}[InputShield]${NC} Scanning ${BOLD}$total_files${NC} files (${BOLD}$total_patterns${NC} patterns, tier: ${BOLD}$tier${NC})..."
    if [[ -n "$category_filter" ]]; then
      local cat_label
      cat_label=$(get_category_label "$category_filter")
      echo -e "  Category filter: ${BOLD}${category_filter}${NC} ($cat_label)"
    fi
    echo ""
  fi

  # Scan all files
  for filepath in "${files[@]}"; do
    scan_file "$filepath" "$per_category_limit" "$category_filter"

    # Verbose mode: show per-file progress
    if [[ "$verbose" == "true" && "$format" == "text" ]]; then
      local fc="${FILE_FINDINGS_COUNT[$filepath]:-0}"
      if [[ $fc -gt 0 ]]; then
        echo -e "  ${YELLOW}$fc${NC} findings in ${DIM}$filepath${NC}"
      fi
    fi
  done

  # Calculate score
  local score
  score=$(calculate_score)

  # Output in requested format
  case "$format" in
    json)
      print_findings_json "$score" "$total_files" "$tier"
      ;;
    html)
      print_findings_html "$score" "$total_files" "$tier"
      ;;
    text|*)
      if [[ ${#FINDINGS[@]} -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}No input validation issues detected!${NC}"
        echo ""
        echo -e "Input Safety Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
        echo -e "${GREEN}PASS${NC}"
        return 0
      fi

      print_findings_text
      print_category_breakdown
      print_score "$score"

      if [[ "$tier" == "free" ]]; then
        echo ""
        local unlocked=$((per_category_limit * 6))
        echo -e "${YELLOW}Note:${NC} Free tier scanned with $unlocked of 90 patterns ($per_category_limit per category)."
        echo -e "  Upgrade to Pro for 60 patterns: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
      fi
      ;;
  esac

  # Return exit code based on score
  if [[ $score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ============================================================================
# Deep Audit (Team+)
# ============================================================================

do_inputshield_audit() {
  local target="${1:-.}"
  local format="${2:-text}"
  local category_filter="${3:-}"
  local verbose="${4:-true}"

  # Audit uses all 90 patterns (team+ tier = 15 per category)
  do_inputshield_scan "$target" 15 "$format" "$category_filter" "team" "$verbose"
}

# ============================================================================
# Hook Integration
# ============================================================================

# Called by lefthook pre-commit hook
hook_inputshield_check() {
  # Get list of staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  FINDINGS=()
  CATEGORY_COUNTS=()
  FILE_FINDINGS_COUNT=()

  # Determine tier for pattern limit
  local tier
  tier=$(get_inputshield_tier 2>/dev/null || echo "free")
  local per_category_limit
  per_category_limit=$(get_patterns_per_category "$tier" 2>/dev/null || echo 5)

  local file_count=0
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    [[ ! -f "$filepath" ]] && continue

    # Skip excluded dirs and binary files
    is_excluded_dir "$filepath" && continue
    should_skip_file "$filepath" && continue

    scan_file "$filepath" "$per_category_limit" ""
    file_count=$((file_count + 1))
  done <<< "$staged_files"

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[InputShield]${NC} No input validation issues in $file_count staged files."
    return 0
  fi

  # Check if any critical or high findings exist
  local has_blocking=false
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_blocking=true
      break
    fi
  done

  echo -e "${RED}${BOLD}[InputShield] Input validation issues detected in staged files!${NC}"
  echo ""
  print_findings_text
  print_category_breakdown

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ "$has_blocking" == true ]]; then
    echo ""
    echo -e "${RED}Commit blocked.${NC} Fix input validation issues before committing."
    echo -e "  Run: ${CYAN}inputshield scan${NC} for details"
    echo -e "  Skip: ${DIM}git commit --no-verify${NC} (not recommended)"
    return 1
  fi

  return 0
}

# ============================================================================
# Pattern Listing
# ============================================================================

do_list_patterns() {
  local per_category_limit="${1:-0}"  # 0 = all

  echo -e "${BOLD}--- InputShield Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(inputshield_pattern_count) patterns across 6 categories${NC}"
  echo ""

  for cat in $INPUTSHIELD_CATEGORIES; do
    local cat_label
    cat_label=$(get_category_label "$cat")
    local cat_count
    cat_count=$(inputshield_category_count "$cat")

    echo -e "${CYAN}${BOLD}${cat} -- ${cat_label} (${cat_count} patterns):${NC}"

    if [[ $per_category_limit -gt 0 ]]; then
      inputshield_list_patterns "$cat" "$per_category_limit" | while IFS= read -r line; do
        echo "  $line"
      done
      local remaining=$((cat_count - per_category_limit))
      if [[ $remaining -gt 0 ]]; then
        echo -e "  ${DIM}... and $remaining more (upgrade for access)${NC}"
      fi
    else
      inputshield_list_patterns "$cat" 0 | while IFS= read -r line; do
        echo "  $line"
      done
    fi
    echo ""
  done
}
