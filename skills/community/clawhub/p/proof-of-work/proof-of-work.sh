#!/bin/bash

################################################################################
# Proof of Work — Task Completion Verification for AI Agents
# A lightweight bash script for validating agent task outputs
################################################################################

set -o pipefail

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME:=$(cd ~ && pwd)}"
POW_DIR="${POW_DIR:-$HOME_DIR/.proof-of-work}"
CONFIG_FILE="${CONFIG_FILE:-$POW_DIR/config.json}"
LOG_FILE=""
VERBOSE=0
AI_CHECK=0
REPORT_FORMAT="text"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Utility Functions
################################################################################

log() {
    echo -e "$1"
}

verbose() {
    if [ "$VERBOSE" -eq 1 ]; then
        echo -e "${BLUE}[DEBUG]${NC} $1" >&2
    fi
}

error() {
    echo -e "${RED}Error:${NC} $1" >&2
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

fail() {
    echo -e "${RED}✗${NC} $1"
}

write_log() {
    if [ -n "$LOG_FILE" ] && [ -w "$(dirname "$LOG_FILE")" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    fi
}

expand_path() {
    local path="$1"
    # Expand ~ to home directory
    path="${path/#\~/$HOME_DIR}"
    # Expand ~ when followed by /
    path="${path/#\~\//$HOME_DIR/}"
    echo "$path"
}

################################################################################
# Configuration Management
################################################################################

load_config() {
    local config_file="$1"

    if [ ! -f "$config_file" ]; then
        error "Config file not found: $config_file"
        return 1
    fi

    verbose "Loading config from: $config_file"

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        error "jq is required but not installed. Install with: apt-get install jq (Linux) or brew install jq (macOS)"
        return 1
    fi

    # Validate JSON
    if ! jq empty "$config_file" 2>/dev/null; then
        error "Invalid JSON in config file: $config_file"
        return 1
    fi

    return 0
}

get_config_value() {
    local config_file="$1"
    local key="$2"
    local default="$3"

    if [ ! -f "$config_file" ]; then
        echo "$default"
        return 0
    fi

    local value
    value=$(jq -r ".$key // empty" "$config_file" 2>/dev/null)

    if [ -z "$value" ]; then
        echo "$default"
    else
        echo "$value"
    fi
}

get_config_array() {
    local config_file="$1"
    local key="$2"

    if [ ! -f "$config_file" ]; then
        return 0
    fi

    jq -r ".${key}[]? // empty" "$config_file" 2>/dev/null
}

################################################################################
# File Checking Logic
################################################################################

check_file_exists() {
    local file="$1"
    if [ ! -f "$file" ]; then
        fail "File does not exist: $file"
        return 1
    fi
    success "File exists"
    return 0
}

check_file_not_empty() {
    local file="$1"
    local size
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || wc -c < "$file")

    if [ "$size" -eq 0 ]; then
        fail "File is empty"
        return 1
    fi
    success "File is non-empty ($size bytes)"
    return 0
}

check_file_age() {
    local file="$1"
    local max_age_hours="$2"

    if [ "$max_age_hours" -eq 0 ]; then
        success "Age check skipped (max_age_hours = 0)"
        return 0
    fi

    local file_time
    local current_time
    local file_age_hours

    # Get file modification time (works on both macOS and Linux)
    file_time=$(stat -f%m "$file" 2>/dev/null || stat -c%Y "$file" 2>/dev/null)
    current_time=$(date +%s)

    file_age_hours=$(( (current_time - file_time) / 3600 ))

    if [ "$file_age_hours" -gt "$max_age_hours" ]; then
        fail "File is too old: ${file_age_hours}h (max: ${max_age_hours}h)"
        return 1
    fi

    success "File age is acceptable: ${file_age_hours}h ago (max: ${max_age_hours}h)"
    return 0
}

check_required_sections() {
    local file="$1"
    shift
    local sections=("$@")
    local all_present=0

    if [ ${#sections[@]} -eq 0 ]; then
        success "Required sections check skipped (none configured)"
        return 0
    fi

    for section in "${sections[@]}"; do
        if grep -q "$(escape_regex "$section")" "$file" 2>/dev/null; then
            success "Contains required section: $section"
        else
            fail "Missing required section: $section"
            all_present=1
        fi
    done

    return $all_present
}

check_content_length() {
    local file="$1"
    local min_length="$2"

    if [ "$min_length" -eq 0 ]; then
        success "Content length check skipped (min_length = 0)"
        return 0
    fi

    local actual_length
    actual_length=$(wc -c < "$file")

    if [ "$actual_length" -lt "$min_length" ]; then
        fail "Content too short: $actual_length bytes (minimum: $min_length)"
        return 1
    fi

    success "Content length acceptable: $actual_length bytes (minimum: $min_length)"
    return 0
}

check_placeholder_patterns() {
    local file="$1"
    shift
    local patterns=("$@")
    local found_any=0

    if [ ${#patterns[@]} -eq 0 ]; then
        success "Placeholder check skipped (none configured)"
        return 0
    fi

    for pattern in "${patterns[@]}"; do
        # Case-insensitive search for placeholder patterns
        if grep -iq "$(escape_regex "$pattern")" "$file" 2>/dev/null; then
            warning "File contains placeholder text: $pattern"
            found_any=1
        fi
    done

    if [ "$found_any" -eq 0 ]; then
        success "No placeholder text found"
        return 0
    fi

    return 0
}

check_json_validity() {
    local file="$1"

    # Only check .json files
    if [[ ! "$file" =~ \.json$ ]]; then
        verbose "Skipping JSON validation (not a .json file)"
        return 0
    fi

    if command -v jq &> /dev/null; then
        if jq empty "$file" 2>/dev/null; then
            success "JSON is valid"
            return 0
        else
            fail "JSON is invalid"
            return 1
        fi
    else
        verbose "Skipping JSON validation (jq not available)"
        return 0
    fi
}

check_markdown_validity() {
    local file="$1"

    # Only check .md files
    if [[ ! "$file" =~ \.md$ ]]; then
        verbose "Skipping Markdown validation (not a .md file)"
        return 0
    fi

    # Basic markdown checks: look for common issues
    local issues=0

    # Check for unmatched brackets/parentheses (basic check)
    local open_brackets
    local close_brackets
    open_brackets=$(grep -o '\[' "$file" | wc -l)
    close_brackets=$(grep -o '\]' "$file" | wc -l)

    if [ "$open_brackets" -ne "$close_brackets" ]; then
        warning "Markdown may have unmatched brackets"
        issues=$((issues + 1))
    fi

    if [ "$issues" -eq 0 ]; then
        success "Markdown structure looks valid"
        return 0
    fi

    return 0
}

escape_regex() {
    local string="$1"
    echo "$string" | sed 's/[[\.*^$/]/\\&/g'
}

################################################################################
# AI-Powered Checks (Optional Ollama Integration)
################################################################################

check_ollama_available() {
    if ! command -v ollama &> /dev/null; then
        verbose "Ollama not available"
        return 1
    fi

    if ! ollama list &> /dev/null 2>&1; then
        verbose "Ollama is not running"
        return 1
    fi

    return 0
}

ai_quality_check() {
    local file="$1"
    local task_description="${2:-}"

    if [ ! check_ollama_available ]; then
        warning "AI check skipped (Ollama not available)"
        return 0
    fi

    verbose "Running AI quality check via Ollama"

    local content
    content=$(head -c 2000 "$file")

    local prompt="Analyze this task output for completeness and quality. Is it substantive work or placeholder/incomplete content?

Content to analyze:
---
$content
---

Provide a single-word assessment: COMPLETE, PARTIAL, or INCOMPLETE"

    local response
    response=$(echo "$prompt" | ollama run llama2 2>/dev/null | tr '[:upper:]' '[:lower:]')

    case "$response" in
        *complete*)
            success "AI quality check: Content appears complete and substantive"
            return 0
            ;;
        *partial*)
            warning "AI quality check: Content appears partially complete"
            return 0
            ;;
        *incomplete*)
            fail "AI quality check: Content appears incomplete or placeholder"
            return 1
            ;;
        *)
            verbose "AI quality check inconclusive"
            return 0
            ;;
    esac
}

################################################################################
# Main Check Command
################################################################################

cmd_check() {
    local file_path="$1"
    file_path=$(expand_path "$file_path")

    if [ -z "$file_path" ]; then
        error "No file specified"
        return 2
    fi

    verbose "Checking file: $file_path"
    write_log "Checking file: $file_path"

    if ! load_config "$CONFIG_FILE"; then
        return 2
    fi

    echo ""
    log "=== Proof of Work Check ==="
    log "File: $file_path"
    echo ""

    # Get configuration values
    local required_sections
    local min_length
    local max_age
    local placeholders
    local enable_json
    local enable_markdown

    required_sections=$(get_config_array "$CONFIG_FILE" "required_sections")
    min_length=$(get_config_value "$CONFIG_FILE" "min_content_length" "100")
    max_age=$(get_config_value "$CONFIG_FILE" "max_age_hours" "48")
    enable_json=$(get_config_value "$CONFIG_FILE" "enable_json_validation" "false")
    enable_markdown=$(get_config_value "$CONFIG_FILE" "enable_markdown_validation" "true")

    local results=()
    local failed=0

    # Run checks
    check_file_exists "$file_path" || failed=1
    [ $failed -eq 0 ] && check_file_not_empty "$file_path" || failed=1
    [ $failed -eq 0 ] && check_file_age "$file_path" "$max_age" || failed=1

    if [ $failed -eq 0 ]; then
        if [ -n "$required_sections" ]; then
            check_required_sections "$file_path" $required_sections || failed=1
        fi

        check_content_length "$file_path" "$min_length" || failed=1

        # Get placeholder patterns
        local patterns
        patterns=$(get_config_array "$CONFIG_FILE" "placeholder_patterns")
        if [ -n "$patterns" ]; then
            check_placeholder_patterns "$file_path" $patterns
        fi

        if [ "$enable_json" = "true" ] || [ "$enable_json" = "True" ]; then
            check_json_validity "$file_path"
        fi

        if [ "$enable_markdown" = "true" ] || [ "$enable_markdown" = "True" ]; then
            check_markdown_validity "$file_path"
        fi

        if [ "$AI_CHECK" -eq 1 ]; then
            ai_quality_check "$file_path"
        fi
    fi

    echo ""
    if [ $failed -eq 0 ]; then
        log "${GREEN}Status: PASS${NC}"
        write_log "File: $file_path - PASS"
        return 0
    else
        log "${RED}Status: FAIL${NC}"
        write_log "File: $file_path - FAIL"
        return 1
    fi
}

################################################################################
# Check Directory Command
################################################################################

cmd_check_dir() {
    local dir_path="$1"
    dir_path=$(expand_path "$dir_path")

    if [ -z "$dir_path" ]; then
        error "No directory specified"
        return 2
    fi

    if [ ! -d "$dir_path" ]; then
        error "Directory not found: $dir_path"
        return 3
    fi

    verbose "Checking directory: $dir_path"
    write_log "Checking directory: $dir_path"

    echo ""
    log "=== Checking Directory ==="
    log "Path: $dir_path"
    echo ""

    local passed=0
    local failed=0
    local warnings=0
    local file_count=0

    # Find all files in directory
    while IFS= read -r -d '' file; do
        file_count=$((file_count + 1))
        verbose "Processing file: $file"

        # Run check silently and capture result
        if cmd_check "$file" > /dev/null 2>&1; then
            success "$(basename "$file")"
            passed=$((passed + 1))
        else
            fail "$(basename "$file")"
            failed=$((failed + 1))
        fi
    done < <(find "$dir_path" -type f -print0)

    # Summary
    echo ""
    log "=== Summary ==="
    log "Total files: $file_count"
    success "Passed: $passed"
    if [ $failed -gt 0 ]; then
        fail "Failed: $failed"
    fi
    log "Details logged to: $LOG_FILE"
    echo ""

    if [ $failed -gt 0 ]; then
        return 1
    fi
    return 0
}

################################################################################
# Report Command
################################################################################

cmd_report() {
    verbose "Generating report"
    write_log "Report generation started"

    if ! load_config "$CONFIG_FILE"; then
        return 2
    fi

    echo ""
    log "=== Proof of Work Report ==="
    log "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # Get check paths from config
    local check_paths
    check_paths=$(get_config_array "$CONFIG_FILE" "check_paths")

    if [ -z "$check_paths" ]; then
        error "No check_paths configured"
        return 2
    fi

    local total_passed=0
    local total_failed=0
    local total_checked=0

    for path in $check_paths; do
        path=$(expand_path "$path")
        if [ ! -d "$path" ]; then
            warning "Path does not exist: $path"
            continue
        fi

        log ""
        log "Checking: $path"
        log "---"

        local passed=0
        local failed=0

        while IFS= read -r -d '' file; do
            total_checked=$((total_checked + 1))

            if cmd_check "$file" > /dev/null 2>&1; then
                passed=$((passed + 1))
                total_passed=$((total_passed + 1))
            else
                failed=$((failed + 1))
                total_failed=$((total_failed + 1))
                fail "$(basename "$file")"
            fi
        done < <(find "$path" -type f -print0)

        log "Result: $passed passed, $failed failed"
    done

    echo ""
    log "=== Overall Summary ==="
    log "Total files checked: $total_checked"
    success "Passed: $total_passed"
    if [ $total_failed -gt 0 ]; then
        fail "Failed: $total_failed"
    fi
    echo ""

    write_log "Report generation completed: $total_passed passed, $total_failed failed"

    if [ $total_failed -gt 0 ]; then
        return 1
    fi
    return 0
}

################################################################################
# Watch Command (Continuous Monitoring)
################################################################################

cmd_watch() {
    verbose "Starting watch mode"
    write_log "Watch mode started"

    if ! load_config "$CONFIG_FILE"; then
        return 2
    fi

    local check_paths
    check_paths=$(get_config_array "$CONFIG_FILE" "check_paths")

    if [ -z "$check_paths" ]; then
        error "No check_paths configured"
        return 2
    fi

    log "Watching for changes..."
    log "Check paths: $(echo "$check_paths" | tr '\n' ', ')"
    log ""

    # Continuous monitoring loop
    while true; do
        for path in $check_paths; do
            path=$(expand_path "$path")
            if [ ! -d "$path" ]; then
                continue
            fi

            while IFS= read -r -d '' file; do
                if cmd_check "$file" > /dev/null 2>&1; then
                    log "[$(date '+%Y-%m-%d %H:%M:%S')] $(basename "$file"): PASS"
                else
                    log "[$(date '+%Y-%m-%d %H:%M:%S')] $(basename "$file"): FAIL"
                fi
            done < <(find "$path" -type f -newer "$POW_DIR/.watch_marker" -print0 2>/dev/null)
        done

        touch "$POW_DIR/.watch_marker"
        sleep 60
    done
}

################################################################################
# Init Command
################################################################################

cmd_init() {
    verbose "Initializing Proof of Work"

    log ""
    log "=== Initializing Proof of Work ==="
    log ""

    # Create directories
    mkdir -p "$POW_DIR"
    mkdir -p "$POW_DIR/reports"
    success "Created directory: $POW_DIR"

    # Copy sample config if it doesn't exist
    if [ ! -f "$POW_DIR/config.json" ]; then
        if [ -f "$SCRIPT_DIR/sample-config.json" ]; then
            cp "$SCRIPT_DIR/sample-config.json" "$POW_DIR/config.json"
            success "Created config: $POW_DIR/config.json"
        else
            # Create a basic config
            cat > "$POW_DIR/config.json" << 'EOF'
{
  "check_paths": [
    "~/agent-workspace/outputs/"
  ],
  "required_sections": [
    "## Summary",
    "## Result"
  ],
  "min_content_length": 100,
  "max_age_hours": 48,
  "placeholder_patterns": [
    "TODO",
    "TBD",
    "PLACEHOLDER",
    "FIXME"
  ],
  "output_format": "text",
  "log_file": "~/.proof-of-work/checks.log",
  "enable_json_validation": false,
  "enable_markdown_validation": true
}
EOF
            success "Created basic config: $POW_DIR/config.json"
        fi
    else
        warning "Config already exists: $POW_DIR/config.json"
    fi

    # Create log file
    touch "$POW_DIR/checks.log"
    success "Created log file: $POW_DIR/checks.log"

    echo ""
    log "Next steps:"
    log "1. Edit your config: $POW_DIR/config.json"
    log "2. Run a check: proof-of-work check ~/your-file.md"
    log "3. Set up cron: Add to crontab with 'crontab -e'"
    echo ""
}

################################################################################
# Help Command
################################################################################

show_help() {
    cat << 'EOF'
Proof of Work — Task Completion Verification for AI Agents

USAGE:
  proof-of-work [OPTIONS] <command> [arguments]

COMMANDS:
  check <file>              Check a single file against rules
  check-dir <directory>     Check all files in a directory
  report                    Generate summary report of all checks
  watch                     Run continuous monitoring (for cron)
  init                      Initialize config and directory structure
  help                      Show this message

OPTIONS:
  -c, --config FILE         Use alternate config file
  -v, --verbose             Enable debug output
  --ai-check                Enable AI-powered quality checks (requires Ollama)

EXAMPLES:
  # Check a single file
  proof-of-work check ~/outputs/task-001.md

  # Check all files in a directory
  proof-of-work check-dir ~/agent-workspace/outputs/

  # Generate a report
  proof-of-work report

  # Continuous monitoring
  proof-of-work watch

  # Initialize with custom config
  proof-of-work -c /etc/pow/custom-config.json check ~/file.md

  # Enable AI quality checks
  proof-of-work --ai-check check ~/file.md

CONFIGURATION:
  Default config location: ~/.proof-of-work/config.json
  See README.md for detailed configuration options

EXIT CODES:
  0 - All checks passed
  1 - One or more checks failed
  2 - Configuration or argument error
  3 - File or directory not found

EOF
}

################################################################################
# Main Entry Point
################################################################################

main() {
    # Parse global options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=1
                shift
                ;;
            --ai-check)
                AI_CHECK=1
                shift
                ;;
            help|-h|--help)
                show_help
                return 0
                ;;
            check|check-dir|report|watch|init)
                break
                ;;
            *)
                error "Unknown option: $1"
                show_help
                return 2
                ;;
        esac
    done

    # Expand config file path
    CONFIG_FILE=$(expand_path "$CONFIG_FILE")

    # Load log file location from config
    if [ -f "$CONFIG_FILE" ]; then
        LOG_FILE=$(get_config_value "$CONFIG_FILE" "log_file" "$POW_DIR/checks.log")
        LOG_FILE=$(expand_path "$LOG_FILE")
        REPORT_FORMAT=$(get_config_value "$CONFIG_FILE" "output_format" "text")
    fi

    # Ensure log directory exists
    if [ -n "$LOG_FILE" ]; then
        mkdir -p "$(dirname "$LOG_FILE")"
    fi

    # Parse command
    local command="$1"
    shift

    case "$command" in
        check)
            cmd_check "$@"
            ;;
        check-dir)
            cmd_check_dir "$@"
            ;;
        report)
            cmd_report "$@"
            ;;
        watch)
            cmd_watch "$@"
            ;;
        init)
            cmd_init "$@"
            ;;
        help|-h|--help)
            show_help
            return 0
            ;;
        "")
            error "No command specified"
            show_help
            return 2
            ;;
        *)
            error "Unknown command: $command"
            show_help
            return 2
            ;;
    esac
}

# Run main function
main "$@"
exit $?
