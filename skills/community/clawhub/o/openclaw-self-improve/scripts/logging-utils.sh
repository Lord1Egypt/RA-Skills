#!/usr/bin/env bash
# Logging utility functions for OpenClaw Self-Improve.
# Source this file (do not run directly) to use the helpers.

# Initialize logging for a run. Prints the log file path on stdout.
init_logging() {
  local run_dir="$1"
  local log_file="$run_dir/run.log"

  cat > "$log_file" <<EOF
================================================================================
OpenClaw Self-Improve Run Log
Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
Run Directory: $run_dir
================================================================================

EOF

  echo "$log_file"
}

# Log a message with timestamp and level.
log_message() {
  local log_file="$1"
  local level="$2"
  shift 2
  local message="$*"
  local timestamp
  timestamp="$(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  printf '[%s] [%s] %s\n' "$timestamp" "$level" "$message" >> "$log_file"
}

log_info()  { local lf="$1"; shift; log_message "$lf" "INFO"  "$@"; }
log_warn()  { local lf="$1"; shift; log_message "$lf" "WARN"  "$@"; }
log_error() { local lf="$1"; shift; log_message "$lf" "ERROR" "$@"; }

# Run a command safely — no eval. Pass the command and its arguments as
# separate positional args. Captures stdout+stderr to the log file.
log_command() {
  local log_file="$1"
  shift
  if [[ $# -eq 0 ]]; then
    log_error "$log_file" "log_command called with no command"
    return 2
  fi

  log_info "$log_file" "Executing: $*"
  local exit_code=0
  if "$@" >> "$log_file" 2>&1; then
    log_info "$log_file" "Command succeeded (exit code: 0)"
  else
    exit_code=$?
    log_error "$log_file" "Command failed (exit code: $exit_code)"
  fi
  return $exit_code
}

# Log a section separator.
log_section() {
  local log_file="$1"
  local section_name="$2"
  {
    echo ""
    echo "================================================================================"
    echo "Section: $section_name"
    echo "================================================================================"
    echo ""
  } >> "$log_file"
}

# Append a file's content to the log under a labeled section.
log_file_content() {
  local log_file="$1"
  local file_to_log="$2"
  local label="${3:-File Content}"

  if [[ -f "$file_to_log" ]]; then
    log_section "$log_file" "$label"
    cat "$file_to_log" >> "$log_file"
  else
    log_warn "$log_file" "File not found for logging: $file_to_log"
  fi
}

# Append a closing summary block.
create_run_summary() {
  local run_dir="$1"
  local log_file="$run_dir/run.log"
  local end_time
  end_time="$(date -u '+%Y-%m-%d %H:%M:%S UTC')"

  cat >> "$log_file" <<EOF

================================================================================
Run Summary
Completed: $end_time
================================================================================

EOF
}

# Make functions available to subshells.
export -f init_logging log_message log_info log_warn log_error \
  log_command log_section log_file_content create_run_summary
