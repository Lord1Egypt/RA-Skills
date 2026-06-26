#!/usr/bin/env bash
# HTTPLint -- Core Analysis Engine
# Provides: file discovery, pattern scanning, score calculation, grades,
#           category breakdown, file-by-file results, tier-based filtering,
#           report generation, and multi-format output (text, json, html).
#
# This file is sourced by dispatcher.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# --- Colors (safe to re-declare; sourcing scripts may set these) --------------

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
HTTPLINT_VERSION="${VERSION:-1.0.0}"

# Global findings array
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
declare -a FINDINGS=()

# Global file tracking
declare -A FILE_FINDING_COUNTS=()

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
    zip|tar|gz|bz2|xz|7z|rar|tgz) return 0 ;;
    exe|dll|so|dylib|o|a|class|pyc|pyo|wasm) return 0 ;;
    woff|woff2|ttf|eot|otf) return 0 ;;
    pdf|doc|docx|xls|xlsx|ppt|pptx) return 0 ;;
    lock) return 0 ;;  # package-lock.json, yarn.lock, etc.
    map) return 0 ;;   # source maps
  esac

  # Skip minified files
  case "$basename_lower" in
    *.min.js|*.min.css|*.min.mjs) return 0 ;;
    *.bundle.js|*.chunk.js) return 0 ;;
  esac

  # Skip known non-source files
  case "$basename_lower" in
    package-lock.json|yarn.lock|pnpm-lock.yaml|composer.lock|gemfile.lock|cargo.lock|poetry.lock) return 0 ;;
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
    */target/*|*/target) return 0 ;;
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

  if [[ -f "$search_dir" ]]; then
    if ! should_skip_file "$search_dir"; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  while IFS= read -r -d '' file; do
    # Skip excluded directories
    is_excluded_dir "$file" && continue

    # Skip binary/generated files
    should_skip_file "$file" && continue

    # Skip gitignored files
    is_gitignored "$file" && continue

    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 10 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" \
       -o -name "dist" -o -name "build" -o -name "coverage" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name ".tox" -o -name ".terraform" \
       -o -name ".cache" -o -name "target" \) -prune -o \
    -type f -print0 2>/dev/null)
}

# ============================================================================
# Pattern Scanning
# ============================================================================

# Scan a single file against patterns for given categories.
# Appends findings to global FINDINGS array.
# Tracks per-file finding counts in FILE_FINDING_COUNTS.
#
# Arguments:
#   $1 -- filepath to scan
#   $2 -- space-separated list of category codes (e.g., "HC HS CK CH")
#   $3 -- optional: specific category filter (only scan this category)
scan_file() {
  local filepath="$1"
  local categories="$2"
  local category_filter="${3:-}"

  local file_count_before=${#FINDINGS[@]}

  for category in $categories; do
    # If a specific category filter is set, skip non-matching categories
    if [[ -n "$category_filter" ]]; then
      local filter_upper
      filter_upper=$(echo "$category_filter" | tr '[:lower:]' '[:upper:]')
      if [[ "$category" != "$filter_upper" ]]; then
        continue
      fi
    fi

    local patterns_name
    patterns_name=$(get_httplint_patterns_for_category "$category")

    if [[ -z "$patterns_name" ]]; then
      continue
    fi

    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Use grep -nE to find matches with line numbers
      local matches
      matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"

          # Trim whitespace
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

          # Truncate long lines
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi

          local finding="${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}"
          FINDINGS+=("$finding")

        done <<< "$matches"
      fi
    done
  done

  # Track per-file counts
  local file_count_after=${#FINDINGS[@]}
  local file_new_findings=$((file_count_after - file_count_before))
  if [[ $file_new_findings -gt 0 ]]; then
    FILE_FINDING_COUNTS["$filepath"]=$file_new_findings
  fi
}

# ============================================================================
# Score Calculation & Grading
# ============================================================================

# Calculate an HTTP configuration quality score based on findings.
# Score starts at 100 (clean) and decreases with each finding.
# Severity weights: critical=25, high=15, medium=8, low=3
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
# A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: <60
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
# Severity Counting
# ============================================================================

# Count findings by severity level
count_by_severity() {
  local target_severity="$1"
  local count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    if [[ "$severity" == "$target_severity" ]]; then
      count=$((count + 1))
    fi
  done
  echo "$count"
}

# Count findings by category prefix
count_by_category() {
  local target_prefix="$1"
  local count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    if [[ "$prefix" == "$target_prefix" ]]; then
      count=$((count + 1))
    fi
  done
  echo "$count"
}

# ============================================================================
# Text Output
# ============================================================================

# Print findings to stdout in text format
print_findings_text() {
  local verbose="${1:-false}"

  local count=0
  local crit_count high_count med_count low_count
  crit_count=$(count_by_severity "critical")
  high_count=$(count_by_severity "high")
  med_count=$(count_by_severity "medium")
  low_count=$(count_by_severity "low")

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    count=$((count + 1))

    local sev_col
    sev_col=$(severity_color "$severity")

    echo -e "  ${sev_col}${severity^^}${NC} ${DIM}${check_id}${NC} ${file}:${line}"
    echo -e "    ${description}"
    if [[ "$verbose" == "true" ]]; then
      echo -e "    ${DIM}Matched: ${matched_text}${NC}"
    fi
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

# Print category breakdown in text format
print_category_breakdown_text() {
  echo ""
  echo -e "${BOLD}--- Category Breakdown ---${NC}"

  for cat in HC HS CK CH RH ER; do
    local cat_count
    cat_count=$(count_by_category "$cat")
    if [[ $cat_count -gt 0 ]]; then
      local label
      label=$(get_httplint_category_label "$cat")
      echo -e "  ${BOLD}$cat${NC} ($label): $cat_count findings"
    fi
  done
}

# Print file-by-file results
print_file_results_text() {
  if [[ ${#FILE_FINDING_COUNTS[@]} -eq 0 ]]; then
    return
  fi

  echo ""
  echo -e "${BOLD}--- Files with Findings ---${NC}"

  for file in "${!FILE_FINDING_COUNTS[@]}"; do
    echo -e "  ${FILE_FINDING_COUNTS[$file]} findings in ${DIM}$file${NC}"
  done
}

# Print score and grade in text format
print_score_text() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local gc
  gc=$(grade_color "$grade")

  echo ""
  echo -e "${BOLD}HTTP Configuration Quality Score: ${gc}${score}/100${NC} (Grade: ${gc}${BOLD}${grade}${NC})"

  if [[ $score -ge 70 ]]; then
    echo -e "${GREEN}PASS${NC} -- Score is above threshold (70)"
  else
    echo -e "${RED}FAIL${NC} -- Score is below threshold (70)"
  fi
}

# ============================================================================
# JSON Output
# ============================================================================

# Generate JSON output for all findings
generate_json_output() {
  local target="$1"
  local files_scanned="$2"
  local score="$3"
  local grade="$4"
  local pass_status="$5"

  local crit_count high_count med_count low_count
  crit_count=$(count_by_severity "critical")
  high_count=$(count_by_severity "high")
  med_count=$(count_by_severity "medium")
  low_count=$(count_by_severity "low")

  local date_str
  date_str=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Build findings JSON array
  local findings_json=""
  local idx=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"

    # Escape special characters for JSON
    local esc_desc esc_rec esc_match esc_file
    esc_file=$(echo "$file" | sed 's/\\/\\\\/g; s/"/\\"/g')
    esc_desc=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g')
    esc_rec=$(echo "$recommendation" | sed 's/\\/\\\\/g; s/"/\\"/g')
    esc_match=$(echo "$matched_text" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')

    [[ $idx -gt 0 ]] && findings_json="${findings_json},"
    findings_json="${findings_json}
    {
      \"file\": \"${esc_file}\",
      \"line\": ${line},
      \"severity\": \"${severity}\",
      \"check_id\": \"${check_id}\",
      \"category\": \"${check_id%%-*}\",
      \"description\": \"${esc_desc}\",
      \"recommendation\": \"${esc_rec}\",
      \"matched_text\": \"${esc_match}\"
    }"
    idx=$((idx + 1))
  done

  # Build category breakdown
  local categories_json=""
  local cat_idx=0
  for cat in HC HS CK CH RH ER; do
    local cat_count
    cat_count=$(count_by_category "$cat")
    local label
    label=$(get_httplint_category_label "$cat")

    [[ $cat_idx -gt 0 ]] && categories_json="${categories_json},"
    categories_json="${categories_json}
    {
      \"code\": \"${cat}\",
      \"name\": \"${label}\",
      \"count\": ${cat_count}
    }"
    cat_idx=$((cat_idx + 1))
  done

  cat <<JSON_EOF
{
  "tool": "HTTPLint",
  "version": "${HTTPLINT_VERSION}",
  "timestamp": "${date_str}",
  "target": "${target}",
  "score": ${score},
  "grade": "${grade}",
  "pass": ${pass_status},
  "summary": {
    "files_scanned": ${files_scanned},
    "total_findings": ${#FINDINGS[@]},
    "critical": ${crit_count},
    "high": ${high_count},
    "medium": ${med_count},
    "low": ${low_count}
  },
  "categories": [${categories_json}
  ],
  "findings": [${findings_json}
  ]
}
JSON_EOF
}

# ============================================================================
# HTML Output
# ============================================================================

# Generate HTML report output
generate_html_output() {
  local target="$1"
  local files_scanned="$2"
  local score="$3"
  local grade="$4"

  local crit_count high_count med_count low_count
  crit_count=$(count_by_severity "critical")
  high_count=$(count_by_severity "high")
  med_count=$(count_by_severity "medium")
  low_count=$(count_by_severity "low")

  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Determine grade color
  local grade_css_color
  case "$grade" in
    A|B) grade_css_color="#22c55e" ;;
    C)   grade_css_color="#eab308" ;;
    D)   grade_css_color="#f97316" ;;
    F)   grade_css_color="#ef4444" ;;
    *)   grade_css_color="#6b7280" ;;
  esac

  # Build findings table rows
  local findings_rows=""
  local idx=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    idx=$((idx + 1))

    local sev_color
    case "$severity" in
      critical) sev_color="#ef4444" ;;
      high)     sev_color="#a855f7" ;;
      medium)   sev_color="#eab308" ;;
      low)      sev_color="#06b6d4" ;;
      *)        sev_color="#6b7280" ;;
    esac

    # HTML-escape text
    local esc_file esc_desc esc_rec
    esc_file=$(echo "$file" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    esc_desc=$(echo "$description" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    esc_rec=$(echo "$recommendation" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

    findings_rows="${findings_rows}
      <tr>
        <td>${idx}</td>
        <td><code>${esc_file}:${line}</code></td>
        <td><span style=\"color:${sev_color};font-weight:bold\">${severity^^}</span></td>
        <td><code>${check_id}</code></td>
        <td>${esc_desc}</td>
        <td><em>${esc_rec}</em></td>
      </tr>"
  done

  cat <<HTML_EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTTPLint Report -- ${target}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1100px; margin: 0 auto; padding: 2rem; background: #f8fafc; color: #1e293b; }
    h1 { color: #0f172a; border-bottom: 3px solid #3b82f6; padding-bottom: 0.5rem; }
    h2 { color: #334155; margin-top: 2rem; }
    .score-badge { display: inline-block; padding: 0.5rem 1.5rem; border-radius: 0.5rem; color: white; font-size: 1.5rem; font-weight: bold; background: ${grade_css_color}; }
    .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
    .summary-card { background: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
    .summary-card .number { font-size: 2rem; font-weight: bold; }
    .summary-card .label { color: #64748b; font-size: 0.875rem; }
    table { width: 100%; border-collapse: collapse; margin: 1rem 0; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 0.5rem; overflow: hidden; }
    th { background: #1e293b; color: white; padding: 0.75rem; text-align: left; font-size: 0.875rem; }
    td { padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-size: 0.875rem; }
    tr:hover { background: #f1f5f9; }
    code { background: #e2e8f0; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.8rem; }
    .footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.75rem; }
  </style>
</head>
<body>
  <h1>HTTPLint Report</h1>
  <p>Target: <code>${target}</code> | Date: ${date_str} | Version: ${HTTPLINT_VERSION}</p>

  <div class="score-badge">${score}/100 (${grade})</div>

  <h2>Summary</h2>
  <div class="summary-grid">
    <div class="summary-card"><div class="number">${files_scanned}</div><div class="label">Files Scanned</div></div>
    <div class="summary-card"><div class="number">${#FINDINGS[@]}</div><div class="label">Total Findings</div></div>
    <div class="summary-card"><div class="number" style="color:#ef4444">${crit_count}</div><div class="label">Critical</div></div>
    <div class="summary-card"><div class="number" style="color:#a855f7">${high_count}</div><div class="label">High</div></div>
    <div class="summary-card"><div class="number" style="color:#eab308">${med_count}</div><div class="label">Medium</div></div>
    <div class="summary-card"><div class="number" style="color:#06b6d4">${low_count}</div><div class="label">Low</div></div>
  </div>

  <h2>Category Breakdown</h2>
  <table>
    <tr><th>Category</th><th>Code</th><th>Findings</th></tr>
    <tr><td>HTTP Client</td><td>HC</td><td>$(count_by_category "HC")</td></tr>
    <tr><td>HTTP Server</td><td>HS</td><td>$(count_by_category "HS")</td></tr>
    <tr><td>Cookie & Session</td><td>CK</td><td>$(count_by_category "CK")</td></tr>
    <tr><td>Caching & Headers</td><td>CH</td><td>$(count_by_category "CH")</td></tr>
    <tr><td>Request Handling</td><td>RH</td><td>$(count_by_category "RH")</td></tr>
    <tr><td>Error & Response</td><td>ER</td><td>$(count_by_category "ER")</td></tr>
  </table>

  <h2>Findings</h2>
  <table>
    <tr><th>#</th><th>Location</th><th>Severity</th><th>Check</th><th>Description</th><th>Recommendation</th></tr>
    ${findings_rows}
  </table>

  <div class="footer">
    Generated by <a href="https://httplint.pages.dev">HTTPLint</a> v${HTTPLINT_VERSION} on ${date_str}.
  </div>
</body>
</html>
HTML_EOF
}

# ============================================================================
# Markdown Report Generation
# ============================================================================

# Generate a markdown report using the template file
generate_markdown_report() {
  local target="$1"
  local files_scanned="$2"

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Count severities
  local crit_count high_count med_count low_count
  crit_count=$(count_by_severity "critical")
  high_count=$(count_by_severity "high")
  med_count=$(count_by_severity "medium")
  low_count=$(count_by_severity "low")

  local total_issues=${#FINDINGS[@]}

  # Build category breakdown
  local cat_breakdown=""
  for cat in HC HS CK CH RH ER; do
    local cat_count
    cat_count=$(count_by_category "$cat")
    local label
    label=$(get_httplint_category_label "$cat")
    cat_breakdown="${cat_breakdown}| ${label} (${cat}) | ${cat_count} |"$'\n'
  done

  # Build findings table
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
    recommendations="${recommendations}1. **CRITICAL:** ${crit_count} critical findings -- address immediately (plaintext HTTP, disabled cookie security, stack trace exposure)${NEWLINE:-$'\n'}"
  fi
  if [[ $high_count -gt 0 ]]; then
    recommendations="${recommendations}2. **HIGH:** ${high_count} high-severity findings -- fix wildcard CORS, URL injection risks, and error information leakage"$'\n'
  fi
  if [[ $med_count -gt 0 ]]; then
    recommendations="${recommendations}3. **MEDIUM:** ${med_count} medium findings -- add missing timeouts, body size limits, and cache headers"$'\n'
  fi
  if [[ $low_count -gt 0 ]]; then
    recommendations="${recommendations}4. **LOW:** ${low_count} low findings -- review for best practices and false positives"$'\n'
  fi

  # Get project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")

  # Read template and substitute
  local template_file="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_file" ]]; then
    echo -e "${RED}[HTTPLint]${NC} Report template not found: $template_file" >&2
    return 1
  fi

  local report
  report=$(cat "$template_file")
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{VERSION\}\}/$HTTPLINT_VERSION}"
  report="${report//\{\{DATE\}\}/$date_str}"
  report="${report//\{\{SCORE\}\}/$score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total_issues}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$crit_count}"
  report="${report//\{\{HIGH_COUNT\}\}/$high_count}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$med_count}"
  report="${report//\{\{LOW_COUNT\}\}/$low_count}"
  report="${report//\{\{CATEGORY_BREAKDOWN\}\}/$cat_breakdown}"
  report="${report//\{\{FINDINGS_TABLE\}\}/$findings_table}"
  report="${report//\{\{RECOMMENDATIONS\}\}/$recommendations}"

  echo "$report"
}

# ============================================================================
# Main Scan Function
# ============================================================================

# do_httplint_scan <target> <tier_level> <format> <verbose> <category_filter>
#
# Arguments:
#   target          -- file or directory to scan
#   tier_level      -- numeric tier (0=free, 1=pro, 2=team, 3=enterprise)
#   format          -- output format: text, json, html
#   verbose         -- "true" or "false"
#   category_filter -- optional category code to filter (e.g., "CK")
do_httplint_scan() {
  local target="${1:-.}"
  local tier_level="${2:-0}"
  local format="${3:-text}"
  local verbose="${4:-false}"
  local category_filter="${5:-}"

  FINDINGS=()
  FILE_FINDING_COUNTS=()

  # Determine which categories are available for this tier
  local categories
  categories=$(get_httplint_categories_for_tier "$tier_level")

  # Validate category filter if provided
  if [[ -n "$category_filter" ]]; then
    local filter_upper
    filter_upper=$(echo "$category_filter" | tr '[:lower:]' '[:upper:]')
    if ! is_valid_httplint_category "$filter_upper"; then
      echo -e "${RED}[HTTPLint]${NC} Invalid category: ${BOLD}$category_filter${NC}" >&2
      echo -e "  Valid categories: HC, HS, CK, CH, RH, ER" >&2
      return 1
    fi

    # Check if the filtered category is available for this tier
    local cat_available=false
    for available_cat in $categories; do
      if [[ "$available_cat" == "$filter_upper" ]]; then
        cat_available=true
        break
      fi
    done

    if [[ "$cat_available" == false ]]; then
      echo -e "${RED}[HTTPLint]${NC} Category ${BOLD}$filter_upper${NC} is not available on your current tier." >&2
      echo -e "  Available categories for your tier: ${BOLD}$categories${NC}" >&2
      echo -e "  Upgrade at: ${CYAN}https://httplint.pages.dev/pricing${NC}" >&2
      return 1
    fi
  fi

  # Discover files
  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    if [[ "$format" == "json" ]]; then
      generate_json_output "$target" 0 100 "A" "true"
    elif [[ "$format" == "html" ]]; then
      generate_html_output "$target" 0 100 "A"
    else
      echo -e "${GREEN}[HTTPLint]${NC} No scannable files found in ${BOLD}$target${NC}"
      echo -e "  Clean scan -- no files to check."
    fi
    return 0
  fi

  # Only print progress info for text format
  if [[ "$format" == "text" ]]; then
    local pattern_count=0
    for cat in $categories; do
      local cnt
      cnt=$(httplint_category_count "$cat")
      pattern_count=$((pattern_count + cnt))
    done

    echo -e "${BLUE}[HTTPLint]${NC} Scanning ${BOLD}$total_files${NC} files with ${BOLD}$pattern_count${NC} patterns..."
    if [[ -n "$category_filter" ]]; then
      echo -e "  ${DIM}Category filter: ${category_filter^^}${NC}"
    fi
    echo ""
  fi

  # Scan each file
  for filepath in "${files[@]}"; do
    scan_file "$filepath" "$categories" "$category_filter"
  done

  # Calculate results
  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local pass_status
  if [[ $score -ge 70 ]]; then
    pass_status="true"
  else
    pass_status="false"
  fi

  # Output results in requested format
  case "$format" in
    json)
      generate_json_output "$target" "$total_files" "$score" "$grade" "$pass_status"
      ;;
    html)
      generate_html_output "$target" "$total_files" "$score" "$grade"
      ;;
    text|*)
      if [[ ${#FINDINGS[@]} -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}No HTTP configuration issues detected!${NC}"
        echo ""
        echo -e "HTTP Configuration Quality Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
        echo -e "${GREEN}PASS${NC}"
        return 0
      fi

      print_findings_text "$verbose"
      print_category_breakdown_text
      print_file_results_text
      print_score_text "$score"
      ;;
  esac

  # Return exit code based on score
  if [[ $score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ============================================================================
# Hook Integration
# ============================================================================

# Called by lefthook pre-commit hook
hook_httplint_check() {
  local tier_level="${1:-0}"

  # Get list of staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  FINDINGS=()
  FILE_FINDING_COUNTS=()

  # Determine categories for tier
  local categories
  categories=$(get_httplint_categories_for_tier "$tier_level")

  local file_count=0
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    [[ ! -f "$filepath" ]] && continue

    # Skip excluded dirs and binary files
    is_excluded_dir "$filepath" && continue
    should_skip_file "$filepath" && continue

    scan_file "$filepath" "$categories" ""
    file_count=$((file_count + 1))
  done <<< "$staged_files"

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[HTTPLint]${NC} No HTTP configuration issues in $file_count staged files."
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

  echo -e "${RED}${BOLD}[HTTPLint] HTTP configuration issues detected in staged files!${NC}"
  echo ""
  print_findings_text "false"

  local score
  score=$(calculate_score)
  print_score_text "$score"

  if [[ "$has_blocking" == true ]]; then
    echo ""
    echo -e "${RED}Commit blocked.${NC} Fix HTTP configuration issues before committing."
    echo -e "  Run: ${CYAN}httplint scan${NC} for details"
    echo -e "  Skip: ${DIM}git commit --no-verify${NC} (not recommended)"
    return 1
  fi

  return 0
}
