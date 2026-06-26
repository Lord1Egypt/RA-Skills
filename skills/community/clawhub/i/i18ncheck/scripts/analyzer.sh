#!/usr/bin/env bash
# I18nCheck -- Core Analysis Engine
# Provides: file discovery, pattern scanning, .gitignore-aware scanning,
#           allowlist support, score calculation, grades, report generation,
#           baseline management, hook integration, watch mode, CI mode,
#           and team report generation.
#
# This file is sourced by i18ncheck.sh and by the lefthook pre-commit hook.
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
I18NCHECK_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

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

# Check if file is a scannable source file for i18n checks
is_scannable_for_i18n() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local ext="${basename_f##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  case "$ext" in
    # JavaScript / TypeScript
    js|jsx|ts|tsx|mjs|cjs) return 0 ;;
    # Python
    py) return 0 ;;
    # Java / Kotlin
    java|kt|kts) return 0 ;;
    # Go
    go) return 0 ;;
    # Ruby
    rb|erb) return 0 ;;
    # PHP
    php|phtml|blade.php) return 0 ;;
    # HTML / Templates
    html|htm|hbs|mustache|ejs|pug|jade|njk|twig|jinja|jinja2) return 0 ;;
    # CSS / Styling
    css|scss|sass|less|styl) return 0 ;;
    # Vue / Svelte / Angular
    vue|svelte) return 0 ;;
    # Config / Data (for translation files)
    json|yaml|yml) return 0 ;;
    # Swift / ObjC
    swift|m|mm) return 0 ;;
    # C# / .NET
    cs|cshtml|razor) return 0 ;;
    # Rust
    rs) return 0 ;;
    # Everything else: skip
    *) return 1 ;;
  esac
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
    */.idea/*|*/.idea) return 0 ;;
    */.vscode/*|*/.vscode) return 0 ;;
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
discover_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    if ! should_skip_file "$search_dir" && is_scannable_for_i18n "$search_dir"; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  while IFS= read -r -d '' file; do
    # Skip excluded directories
    is_excluded_dir "$file" && continue

    # Skip binary/generated files
    should_skip_file "$file" && continue

    # Only include i18n-scannable file types
    is_scannable_for_i18n "$file" || continue

    # Skip gitignored files
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
# Allowlist Support
# ============================================================================

declare -a ALLOWLIST_PATTERNS=()

load_allowlist() {
  local search_dir="${1:-.}"
  ALLOWLIST_PATTERNS=()

  local allowlist_file=""

  # Check for allowlist in the scan directory
  if [[ -f "$search_dir/.i18ncheck-allowlist" ]]; then
    allowlist_file="$search_dir/.i18ncheck-allowlist"
  fi

  # Check git repo root
  if [[ -z "$allowlist_file" ]] && command -v git &>/dev/null; then
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [[ -n "$repo_root" && -f "$repo_root/.i18ncheck-allowlist" ]]; then
      allowlist_file="$repo_root/.i18ncheck-allowlist"
    fi
  fi

  # Read from openclaw.json config
  local config_allowlist=""
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      config_allowlist=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    af = cfg.get('skills', {}).get('entries', {}).get('i18ncheck', {}).get('config', {}).get('allowlistFile', '')
    print(af)
except: pass
" 2>/dev/null)
    fi

    if [[ -n "$config_allowlist" && -f "$search_dir/$config_allowlist" ]]; then
      allowlist_file="$search_dir/$config_allowlist"
    fi
  fi

  if [[ -n "$allowlist_file" && -f "$allowlist_file" ]]; then
    while IFS= read -r line; do
      # Skip empty lines and comments
      [[ -z "$line" || "$line" == \#* ]] && continue
      ALLOWLIST_PATTERNS+=("$line")
    done < "$allowlist_file"
  fi
}

# Check if a finding is allowlisted
is_allowlisted() {
  local finding="$1"

  for pattern in "${ALLOWLIST_PATTERNS[@]}"; do
    if echo "$finding" | grep -qF "$pattern" 2>/dev/null; then
      return 0
    fi
  done

  return 1
}

# ============================================================================
# Baseline Support
# ============================================================================

declare -a BASELINE_HASHES=()

load_baseline() {
  local search_dir="${1:-.}"
  BASELINE_HASHES=()

  local baseline_file=""

  if [[ -f "$search_dir/.i18ncheck-baseline.json" ]]; then
    baseline_file="$search_dir/.i18ncheck-baseline.json"
  fi

  if [[ -z "$baseline_file" ]] && command -v git &>/dev/null; then
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [[ -n "$repo_root" && -f "$repo_root/.i18ncheck-baseline.json" ]]; then
      baseline_file="$repo_root/.i18ncheck-baseline.json"
    fi
  fi

  if [[ -n "$baseline_file" && -f "$baseline_file" ]]; then
    if command -v python3 &>/dev/null; then
      while IFS= read -r hash; do
        [[ -n "$hash" ]] && BASELINE_HASHES+=("$hash")
      done < <(python3 -c "
import json
try:
    with open('$baseline_file') as f:
        data = json.load(f)
    for h in data.get('hashes', []):
        print(h)
except: pass
" 2>/dev/null)
    fi
  fi
}

# Compute a simple hash for a finding (file + line + check_id)
finding_hash() {
  local finding="$1"
  local file line severity check_id
  IFS='|' read -r file line severity check_id _ _ _ <<< "$finding"
  echo "${file}:${line}:${check_id}" | md5sum 2>/dev/null | cut -d' ' -f1 || \
  echo "${file}:${line}:${check_id}" | openssl md5 2>/dev/null | awk '{print $NF}' || \
  echo "${file}:${line}:${check_id}"
}

is_baselined() {
  local finding="$1"
  local hash
  hash=$(finding_hash "$finding")

  for baseline_hash in "${BASELINE_HASHES[@]}"; do
    if [[ "$hash" == "$baseline_hash" ]]; then
      return 0
    fi
  done

  return 1
}

# ============================================================================
# Pattern Scanning
# ============================================================================

# run_pattern_scan -- Scan a single file against all i18n pattern categories.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
run_pattern_scan() {
  local filepath="$1"

  local categories
  categories=$(get_all_i18ncheck_categories)

  for category in $categories; do
    local patterns_name
    patterns_name=$(get_i18ncheck_patterns_for_category "$category")

    if [[ -z "$patterns_name" ]]; then
      continue
    fi

    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Skip placeholder patterns (handled by file-level checks)
      [[ "$regex" == PLACEHOLDER_* ]] && continue

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

          # Check allowlist
          if is_allowlisted "$finding"; then
            continue
          fi

          # Check baseline
          if [[ ${#BASELINE_HASHES[@]} -gt 0 ]] && is_baselined "$finding"; then
            continue
          fi

          FINDINGS+=("$finding")
        done <<< "$matches"
      fi
    done
  done
}

# ============================================================================
# File-Level Checks (not pattern-based)
# ============================================================================

# Check if a file with UI strings is missing i18n imports
check_missing_i18n_import() {
  local filepath="$1"
  local ext="${filepath##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  # Only check JS/TS files
  case "$ext" in
    js|jsx|ts|tsx|mjs) ;;
    *) return ;;
  esac

  # Check if file has UI-like strings (JSX elements or alert/confirm)
  local has_ui_strings=false
  if grep -qE '<(h[1-6]|p|span|div|button|label)>[[:space:]]*[A-Z]' "$filepath" 2>/dev/null; then
    has_ui_strings=true
  fi
  if grep -qE '(alert|confirm|prompt)[[:space:]]*\(' "$filepath" 2>/dev/null; then
    has_ui_strings=true
  fi

  if [[ "$has_ui_strings" == true ]]; then
    # Check for i18n imports
    local has_i18n_import=false
    if grep -qE '(import.*i18n|import.*useTranslation|import.*Trans|import.*t[[:space:]]*from|import.*intl|require.*i18n|from.*react-intl|from.*i18next|from.*vue-i18n)' "$filepath" 2>/dev/null; then
      has_i18n_import=true
    fi

    if [[ "$has_i18n_import" == false ]]; then
      FINDINGS+=("${filepath}|1|medium|TK-009|File contains UI strings but has no i18n/translation import|Add translation import: import { useTranslation } from 'react-i18next'|No i18n import found")
    fi
  fi
}

# Run all file-level checks for a file
run_file_level_checks() {
  local filepath="$1"
  check_missing_i18n_import "$filepath"
}

# ============================================================================
# Analyze single file / directory
# ============================================================================

analyze_file() {
  local filepath="$1"
  run_pattern_scan "$filepath"
  run_file_level_checks "$filepath"
}

analyze_directory() {
  local target="$1"
  local file_limit="${2:-0}"

  local -a files=()
  discover_files "$target" files

  local total_files=${#files[@]}
  local scan_count=$total_files

  if [[ $file_limit -gt 0 && $total_files -gt $file_limit ]]; then
    scan_count=$file_limit
  fi

  local i=0
  for filepath in "${files[@]}"; do
    if [[ $file_limit -gt 0 && $i -ge $file_limit ]]; then
      break
    fi
    analyze_file "$filepath"
    i=$((i + 1))
  done

  echo "$total_files"
}

# ============================================================================
# Score Calculation & Grading
# ============================================================================

# calculate_score -- Score starts at 100 (clean) and decreases with each finding.
# Scoring: critical=25pts, high=15pts, medium=8pts, low=3pts
# Pass threshold: 70
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
score_to_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

# Grade color
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

# Severity color
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
# Output Formatting
# ============================================================================

# Print findings to stdout
print_findings() {
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

# Print score and grade
print_score() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local gc
  gc=$(grade_color "$grade")

  echo ""
  echo -e "${BOLD}I18n Readiness Score: ${gc}${score}/100${NC} (Grade: ${gc}${BOLD}${grade}${NC})"

  if [[ $score -ge 70 ]]; then
    echo -e "${GREEN}PASS${NC} -- Score is above threshold (70)"
  else
    echo -e "${RED}FAIL${NC} -- Score is below threshold (70)"
  fi
}

# ============================================================================
# Main Scan Function (FREE)
# ============================================================================

# do_i18ncheck_scan <target> <file_limit>
# file_limit: max files for free tier (0 = unlimited)
do_i18ncheck_scan() {
  local target="${1:-.}"
  local file_limit="${2:-0}"
  FINDINGS=()

  # Load allowlist
  load_allowlist "$target"

  # Load baseline if exists
  load_baseline "$target"

  # Discover files
  local -a files=()
  discover_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[I18nCheck]${NC} No scannable files found in ${BOLD}$target${NC}"
    echo -e "  Clean scan -- no files to check."
    return 0
  fi

  # Apply file limit for free tier
  local scan_count=$total_files
  local limited=false
  if [[ $file_limit -gt 0 && $total_files -gt $file_limit ]]; then
    scan_count=$file_limit
    limited=true
    echo -e "${YELLOW}[I18nCheck]${NC} Free tier: scanning $file_limit of $total_files files"
    echo -e "  ${DIM}Upgrade to Pro for unlimited scans: https://i18ncheck.pages.dev/pricing${NC}"
    echo ""
  fi

  echo -e "${BLUE}[I18nCheck]${NC} Scanning ${BOLD}$scan_count${NC} files for i18n issues..."
  echo ""

  local i=0
  for filepath in "${files[@]}"; do
    if [[ $file_limit -gt 0 && $i -ge $file_limit ]]; then
      break
    fi

    # Pattern scan
    run_pattern_scan "$filepath"

    # File-level checks
    run_file_level_checks "$filepath"

    i=$((i + 1))
  done

  # Print results
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No i18n issues detected!${NC}"
    echo ""
    echo -e "I18n Readiness Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
    echo -e "${GREEN}PASS${NC}"
    return 0
  fi

  print_findings

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ $limited == true ]]; then
    echo ""
    echo -e "${YELLOW}Note:${NC} Only $file_limit of $total_files files were scanned (free tier limit)."
    echo -e "  Upgrade to Pro for a complete scan: ${CYAN}https://i18ncheck.pages.dev/pricing${NC}"
  fi

  # Exit code
  if [[ $score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ============================================================================
# Report Generation (FREE)
# ============================================================================

generate_report() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  discover_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[I18nCheck]${NC} No scannable files found."
    return 0
  fi

  echo -e "${BLUE}[I18nCheck]${NC} Scanning ${BOLD}$total_files${NC} files for report..." >&2

  for filepath in "${files[@]}"; do
    run_pattern_scan "$filepath"
    run_file_level_checks "$filepath"
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

  # Build category breakdown
  local cat_breakdown=""
  local -A cat_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    cat_counts["$prefix"]=$(( ${cat_counts["$prefix"]:-0} + 1 ))
  done

  for cat in "${!cat_counts[@]}"; do
    local cat_label
    case "$cat" in
      HS) cat_label="Hardcoded Strings" ;;
      TK) cat_label="Translation Keys" ;;
      DF) cat_label="Date & Number Formatting" ;;
      RL) cat_label="RTL & Layout" ;;
      SC) cat_label="String Concatenation" ;;
      EN) cat_label="Encoding & Locale" ;;
      *)  cat_label="$cat" ;;
    esac
    cat_breakdown="${cat_breakdown}| ${cat_label} | ${cat_counts[$cat]} |"$'\n'
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
    recommendations="${recommendations}1. **CRITICAL:** ${crit_count} critical i18n issues -- fix string concatenation in translations and hardcoded UI text immediately"$'\n'
  fi
  if [[ $high_count -gt 0 ]]; then
    recommendations="${recommendations}2. **HIGH:** ${high_count} high-severity findings -- wrap hardcoded strings with translation functions, fix date/number formatting"$'\n'
  fi
  if [[ $med_count -gt 0 ]]; then
    recommendations="${recommendations}3. **MEDIUM:** ${med_count} medium findings -- improve RTL layout support, add missing translation keys"$'\n'
  fi
  if [[ $low_count -gt 0 ]]; then
    recommendations="${recommendations}4. **LOW:** ${low_count} low findings -- address encoding and minor locale issues"$'\n'
  fi

  # Get project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")

  # Read template and substitute
  local template_file="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_file" ]]; then
    echo -e "${RED}[I18nCheck]${NC} Report template not found: $template_file" >&2
    return 1
  fi

  local report
  report=$(cat "$template_file")
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{VERSION\}\}/$I18NCHECK_VERSION}"
  report="${report//\{\{DATE\}\}/$date_str}"
  report="${report//\{\{I18N_SCORE\}\}/$score}"
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
  echo -e "${GREEN}[I18nCheck]${NC} Report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Hook Integration (FREE)
# ============================================================================

# hook_i18n_scan -- Called by lefthook pre-commit hook
hook_i18n_scan() {
  # Get list of staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  FINDINGS=()
  load_allowlist "."
  load_baseline "."

  local file_count=0
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    [[ ! -f "$filepath" ]] && continue

    # Skip excluded dirs and binary files
    is_excluded_dir "$filepath" && continue
    should_skip_file "$filepath" && continue
    is_scannable_for_i18n "$filepath" || continue

    run_pattern_scan "$filepath"
    run_file_level_checks "$filepath"

    file_count=$((file_count + 1))
  done <<< "$staged_files"

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[I18nCheck]${NC} No i18n issues detected in $file_count staged files."
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

  echo -e "${RED}${BOLD}[I18nCheck] Internationalization issues detected in staged files!${NC}"
  echo ""
  print_findings

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ "$has_blocking" == true ]]; then
    echo ""
    echo -e "${RED}Commit blocked.${NC} Fix i18n issues before committing."
    echo -e "  Run: ${CYAN}i18ncheck scan${NC} for details"
    echo -e "  Skip: ${DIM}git commit --no-verify${NC} (not recommended)"
    return 1
  fi

  return 0
}

# ============================================================================
# Watch Mode (PRO+)
# ============================================================================

watch_mode() {
  local target="${1:-.}"

  echo -e "${BLUE}[I18nCheck]${NC} Watch mode started for ${BOLD}$target${NC}"
  echo -e "  ${DIM}Monitoring for file changes... Press Ctrl+C to stop.${NC}"
  echo ""

  load_allowlist "$target"
  load_baseline "$target"

  # Track file modification times
  declare -A file_mtimes=()

  # Initial scan
  local -a files=()
  discover_files "$target" files

  for filepath in "${files[@]}"; do
    local mtime
    mtime=$(stat -c %Y "$filepath" 2>/dev/null || stat -f %m "$filepath" 2>/dev/null || echo "0")
    file_mtimes["$filepath"]="$mtime"
  done

  echo -e "${GREEN}[I18nCheck]${NC} Watching ${#files[@]} files. Initial scan complete."
  echo ""

  # Poll for changes
  while true; do
    sleep 2

    local -a current_files=()
    discover_files "$target" current_files

    for filepath in "${current_files[@]}"; do
      local mtime
      mtime=$(stat -c %Y "$filepath" 2>/dev/null || stat -f %m "$filepath" 2>/dev/null || echo "0")
      local prev_mtime="${file_mtimes[$filepath]:-0}"

      if [[ "$mtime" != "$prev_mtime" ]]; then
        file_mtimes["$filepath"]="$mtime"

        # Scan changed file
        local prev_count=${#FINDINGS[@]}
        run_pattern_scan "$filepath"
        run_file_level_checks "$filepath"
        local new_count=${#FINDINGS[@]}

        if [[ $new_count -gt $prev_count ]]; then
          local new_findings=$((new_count - prev_count))
          echo -e "${YELLOW}[I18nCheck]${NC} ${BOLD}$filepath${NC} changed -- $new_findings new issue(s)"

          # Print only new findings
          local idx=$prev_count
          while [[ $idx -lt $new_count ]]; do
            local finding="${FINDINGS[$idx]}"
            IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
            local sev_col
            sev_col=$(severity_color "$severity")
            echo -e "  ${sev_col}${severity^^}${NC} ${DIM}${check_id}${NC} ${file}:${line}"
            echo -e "    ${description}"
            echo -e "    ${DIM}Fix: ${recommendation}${NC}"
            echo ""
            idx=$((idx + 1))
          done
        else
          echo -e "${GREEN}[I18nCheck]${NC} ${DIM}$filepath${NC} changed -- no new issues"
        fi
      fi
    done
  done
}

# ============================================================================
# CI Mode (PRO+)
# ============================================================================

ci_mode() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  discover_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo "I18NCHECK_RESULT=PASS"
    echo "I18NCHECK_SCORE=100"
    echo "I18NCHECK_GRADE=A"
    echo "I18NCHECK_ISSUES=0"
    return 0
  fi

  echo -e "${BLUE}[I18nCheck]${NC} CI mode: scanning ${BOLD}$total_files${NC} files..." >&2

  for filepath in "${files[@]}"; do
    run_pattern_scan "$filepath"
    run_file_level_checks "$filepath"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local total_issues=${#FINDINGS[@]}

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

  # Machine-parseable output
  local result="PASS"
  if [[ $score -lt 70 ]]; then
    result="FAIL"
  fi

  echo "I18NCHECK_RESULT=$result"
  echo "I18NCHECK_SCORE=$score"
  echo "I18NCHECK_GRADE=$grade"
  echo "I18NCHECK_ISSUES=$total_issues"
  echo "I18NCHECK_CRITICAL=$crit_count"
  echo "I18NCHECK_HIGH=$high_count"
  echo "I18NCHECK_MEDIUM=$med_count"
  echo "I18NCHECK_LOW=$low_count"
  echo "I18NCHECK_FILES=$total_files"

  # Also print human-readable summary to stderr
  echo "" >&2
  if [[ $total_issues -gt 0 ]]; then
    print_findings >&2
  fi
  print_score "$score" >&2

  if [[ $score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ============================================================================
# Team Report (TEAM+)
# ============================================================================

team_report() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  discover_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[I18nCheck]${NC} No scannable files found."
    return 0
  fi

  echo -e "${BLUE}[I18nCheck]${NC} Scanning ${BOLD}$total_files${NC} files for team report..." >&2

  for filepath in "${files[@]}"; do
    run_pattern_scan "$filepath"
    run_file_level_checks "$filepath"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")
  local total_issues=${#FINDINGS[@]}

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

  # Build per-category breakdown
  local -A cat_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    cat_counts["$prefix"]=$(( ${cat_counts["$prefix"]:-0} + 1 ))
  done

  # Build top-offending files
  local -A file_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file _ _ _ _ _ _ <<< "$finding"
    file_counts["$file"]=$(( ${file_counts["$file"]:-0} + 1 ))
  done

  # Build top issues by check ID
  local -A check_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    check_counts["$check_id"]=$(( ${check_counts["$check_id"]:-0} + 1 ))
  done

  # Output team report
  echo "# I18nCheck Team Report: $(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")"
  echo ""
  echo "> Generated by [I18nCheck](https://i18ncheck.pages.dev) v${I18NCHECK_VERSION} on ${date_str}"
  echo ""
  echo "## Executive Summary"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| I18n Readiness Score | **${score}/100** (Grade: **${grade}**) |"
  echo "| Files scanned | ${total_files} |"
  echo "| Total issues | ${total_issues} |"
  echo "| Critical | ${crit_count} |"
  echo "| High | ${high_count} |"
  echo "| Medium | ${med_count} |"
  echo "| Low | ${low_count} |"
  echo ""
  echo "## Issues by Category"
  echo ""
  echo "| Category | Count |"
  echo "|----------|-------|"
  for cat in "${!cat_counts[@]}"; do
    local cat_label
    case "$cat" in
      HS) cat_label="Hardcoded Strings" ;;
      TK) cat_label="Translation Keys" ;;
      DF) cat_label="Date & Number Formatting" ;;
      RL) cat_label="RTL & Layout" ;;
      SC) cat_label="String Concatenation" ;;
      EN) cat_label="Encoding & Locale" ;;
      *)  cat_label="$cat" ;;
    esac
    echo "| ${cat_label} | ${cat_counts[$cat]} |"
  done
  echo ""
  echo "## Top Offending Files"
  echo ""
  echo "| File | Issues |"
  echo "|------|--------|"
  for file in "${!file_counts[@]}"; do
    echo "| ${file} | ${file_counts[$file]} |"
  done | sort -t'|' -k3 -rn | head -10
  echo ""
  echo "## Top Issues by Rule"
  echo ""
  echo "| Check ID | Count |"
  echo "|----------|-------|"
  for check in "${!check_counts[@]}"; do
    echo "| ${check} | ${check_counts[$check]} |"
  done | sort -t'|' -k3 -rn | head -10
  echo ""
  echo "## Remediation Priority"
  echo ""
  if [[ $crit_count -gt 0 ]]; then
    echo "1. **IMMEDIATE:** Fix ${crit_count} critical issues (string concatenation in translations, hardcoded UI text)"
  fi
  if [[ $high_count -gt 0 ]]; then
    echo "2. **THIS SPRINT:** Address ${high_count} high-severity issues (missing translations, date formatting, RTL layout)"
  fi
  if [[ $med_count -gt 0 ]]; then
    echo "3. **NEXT SPRINT:** Improve ${med_count} medium issues (encoding, locale handling)"
  fi
  if [[ $low_count -gt 0 ]]; then
    echo "4. **BACKLOG:** Review ${low_count} low-priority items"
  fi
  echo ""
  echo "---"
  echo ""
  echo "*Report generated by [I18nCheck](https://i18ncheck.pages.dev). Run \`i18ncheck scan\` for interactive results.*"

  echo "" >&2
  echo -e "${GREEN}[I18nCheck]${NC} Team report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Baseline Management (TEAM+)
# ============================================================================

baseline_mode() {
  local target="${1:-.}"
  FINDINGS=()

  # Scan without loading existing baseline
  BASELINE_HASHES=()
  load_allowlist "$target"

  local -a files=()
  discover_files "$target" files

  for filepath in "${files[@]}"; do
    run_pattern_scan "$filepath"
    run_file_level_checks "$filepath"
  done

  # Compute hashes for all findings
  local hashes_json="["
  local first=true
  for finding in "${FINDINGS[@]}"; do
    local hash
    hash=$(finding_hash "$finding")
    if [[ "$first" == true ]]; then
      first=false
    else
      hashes_json="${hashes_json},"
    fi
    hashes_json="${hashes_json}\"${hash}\""
  done
  hashes_json="${hashes_json}]"

  local date_str
  date_str=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%d 2>/dev/null || echo "unknown")

  local baseline_file="$target/.i18ncheck-baseline.json"

  if command -v python3 &>/dev/null; then
    python3 -c "
import json
data = {
    'version': '1.0.0',
    'created': '$date_str',
    'tool': 'i18ncheck',
    'total_findings': ${#FINDINGS[@]},
    'hashes': json.loads('$hashes_json')
}
with open('$baseline_file', 'w') as f:
    json.dump(data, f, indent=2)
print('OK')
" 2>/dev/null
  else
    # Fallback: write JSON manually
    cat > "$baseline_file" <<BASELINE_EOF
{
  "version": "1.0.0",
  "created": "${date_str}",
  "tool": "i18ncheck",
  "total_findings": ${#FINDINGS[@]},
  "hashes": ${hashes_json}
}
BASELINE_EOF
  fi

  echo -e "${GREEN}[I18nCheck]${NC} Baseline created: ${BOLD}$baseline_file${NC}"
  echo -e "  ${#FINDINGS[@]} findings baselined."
  echo -e "  Future scans will only report NEW i18n issues not in this baseline."
}
