#!/usr/bin/env bash
#
# job-tracker - CRUD CLI for Job Applications Tracker Google Sheet
# Provides a safe abstraction layer over gog sheets for job hunting agents
#
# Usage:
#   job-tracker add --company "Morgan Stanley" --role "AI Architect" --source LinkedIn
#   job-tracker log JOB002 --event interview --details "3rd round scheduled"
#   job-tracker update JOB002 --status interviewing --salary "$200k"
#   job-tracker show JOB002
#   job-tracker list [--status discovered] [--limit 10]
#   job-tracker search "morgan" [--columns company,role] [--regex] [--fuzzy]
#   job-tracker next-id
#   job-tracker schema

set -euo pipefail

# === Configuration ===
# Spreadsheet ID from environment variable (required)
# Set via: export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"
# Or configure in OpenClaw: openclaw config set skills.entries.jobs-hunter-claw.spreadsheetId "your-id"
SPREADSHEET_ID="${JOB_TRACKER_SPREADSHEET_ID:-}"

if [[ -z "$SPREADSHEET_ID" ]]; then
  echo "ERROR: JOB_TRACKER_SPREADSHEET_ID environment variable is required." >&2
  echo "Set it with: export JOB_TRACKER_SPREADSHEET_ID=\"your-google-sheet-id\"" >&2
  echo "Or configure in OpenClaw config." >&2
  exit 1
fi

JOBS_TAB="Jobs"
LOGS_TAB="Activity Log"

# Column mapping (1-indexed for awk, letter for gog)
declare -A COL_INDEX=(
  [our_job_id]=1      [employer_job_id]=2   [company]=3         [role]=4
  [location]=5        [salary]=6            [source]=7          [url]=8
  [status]=9          [applied_date]=10     [contacts]=11       [next_action]=12
  [next_date]=13      [resume]=14           [cover_letter]=15   [log]=16
)

declare -A COL_LETTER=(
  [our_job_id]=A      [employer_job_id]=B   [company]=C         [role]=D
  [location]=E        [salary]=F            [source]=G          [url]=H
  [status]=I          [applied_date]=J      [contacts]=K        [next_action]=L
  [next_date]=M       [resume]=N            [cover_letter]=O    [log]=P
)

# Valid status values (Title Case as displayed in form dropdown)
# Canonical list from Apps Script CONFIG.VALID_STATUSES
VALID_STATUSES_DISPLAY=("Discovered" "Applied" "Screening" "Interview" "Karat Test Scheduled" "Offer" "Rejected" "Withdrawn" "Accepted" "Closed")
VALID_STATUSES_PATTERN="discovered|applied|screening|interview|karat test scheduled|offer|rejected|withdrawn|accepted|closed"

# Valid event types for logs (lowercase as per form dropdown)
# Canonical list from Apps Script CONFIG.VALID_EVENTS
VALID_EVENTS_DISPLAY=("discovered" "applied" "recruiter_contact" "user_reply" "interview_scheduled" "interview_completed" "test_scheduled" "test_completed" "offer_received" "rejection" "follow_up" "status_change" "note")
VALID_EVENTS_PATTERN="discovered|applied|recruiter_contact|user_reply|interview_scheduled|interview_completed|test_scheduled|test_completed|offer_received|rejection|follow_up|status_change|note|historical_note"

# Google Contacts link pattern for validation
CONTACTS_PATTERN='^https://contacts\.google\.com/person/c[a-zA-Z0-9]+$'

# === Utility Functions ===

err() {
  echo "ERROR: $*" >&2
  exit 1
}

warn() {
  echo "WARNING: $*" >&2
}

info() {
  echo "$*"
}

now_ts() {
  date -u +"%Y-%m-%d %H:%M"
}

today() {
  date -u +"%Y-%m-%d"
}

json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip()))"
}

# Get all jobs data as TSV (filters out empty rows)
get_all_jobs() {
  gog sheets get "$SPREADSHEET_ID" "${JOBS_TAB}!A2:O1000" --plain 2>/dev/null | awk -F'\t' '$1 != "" || $3 != ""' || echo ""
}

# Get all logs as TSV (filters out empty rows)
get_all_logs() {
  gog sheets get "$SPREADSHEET_ID" "'${LOGS_TAB}'!A2:D10000" --plain 2>/dev/null | awk -F'\t' '$1 != "" || $2 != ""' || echo ""
}

# Find row number for a job ID (returns 0 if not found)
find_job_row() {
  local job_id="$1"
  local row=2
  while IFS=$'\t' read -r id rest; do
    if [[ "$id" == "$job_id" ]]; then
      echo "$row"
      return 0
    fi
    ((row++))
  done < <(get_all_jobs)
  echo "0"
}

# Get next job ID
get_next_id() {
  local max_num=0
  while IFS=$'\t' read -r id rest; do
    if [[ "$id" =~ ^JOB([0-9]+)$ ]]; then
      local num="${BASH_REMATCH[1]#0}"  # Remove leading zeros
      num=$((10#$num))  # Force base 10
      if (( num > max_num )); then
        max_num=$num
      fi
    fi
  done < <(get_all_jobs)
  printf "JOB%03d" $((max_num + 1))
}

# Validate status (case-insensitive, normalizes to Title Case)
validate_status() {
  local status_lower="${1,,}"  # lowercase input
  
  # Check against pattern
  if [[ ! "$status_lower" =~ ^($VALID_STATUSES_PATTERN)$ ]]; then
    err "Invalid status '$1'. Valid: ${VALID_STATUSES_DISPLAY[*]}"
  fi
  
  # Return normalized Title Case version
  for s in "${VALID_STATUSES_DISPLAY[@]}"; do
    if [[ "${s,,}" == "$status_lower" ]]; then
      echo "$s"
      return 0
    fi
  done
  echo "$1"  # fallback
}

# Validate event type
validate_event() {
  local event="$1"
  if [[ ! "$event" =~ ^($VALID_EVENTS_PATTERN)$ ]]; then
    err "Invalid event '$event'. Valid: ${VALID_EVENTS_DISPLAY[*]}"
  fi
}

# Validate Google Contacts links
# Returns 0 if valid, 1 if invalid (prints invalid links to stderr)
validate_contacts() {
  local contacts="$1"
  [[ -z "$contacts" ]] && return 0
  
  local invalid=()
  local IFS=', ;'
  read -ra links <<< "$contacts"
  
  for link in "${links[@]}"; do
    link=$(echo "$link" | xargs)  # trim whitespace
    [[ -z "$link" ]] && continue
    
    if [[ ! "$link" =~ $CONTACTS_PATTERN ]]; then
      invalid+=("$link")
    fi
  done
  
  if [[ ${#invalid[@]} -gt 0 ]]; then
    warn "Invalid Google Contacts links (expected format: https://contacts.google.com/person/c...):"
    for inv in "${invalid[@]}"; do
      echo "  - $inv" >&2
    done
    return 1
  fi
  return 0
}

# === Commands ===

cmd_schema() {
  cat << 'EOF'
Job Tracker Schema
==================

Jobs Tab Columns:
  A: our_job_id      - Internal tracking ID (JOB001, JOB002, ...)
  B: employer_job_id - Employer's job ID/requisition number
  C: company         - Company name
  D: role            - Job title/role
  E: location        - Location (city, remote, hybrid)
  F: salary          - Salary range or compensation
  G: source          - How discovered (LinkedIn, Recruiter Email, etc.)
  H: url             - Job posting URL
  I: status          - Current status (see below)
  J: applied_date    - Date applied (YYYY-MM-DD)
  K: contacts        - Google Contacts links (https://contacts.google.com/person/c...)
  L: next_action     - Next step to take
  M: next_date       - Date for next action
  N: resume          - Resume version used
  O: cover_letter    - Cover letter used (Y/N or filename)
  P: log             - [FORMULA - DO NOT EDIT] Latest 3 log entries

Valid Statuses (Title Case):
  Discovered, Applied, Screening, Interview, Karat Test Scheduled,
  Offer, Rejected, Withdrawn, Accepted, Closed

Logs Tab Columns:
  A: timestamp       - When event occurred (YYYY-MM-DD HH:MM)
  B: our_job_id      - Links to Jobs tab
  C: event_type      - Type of event (see below)
  D: details         - Event description

Valid Event Types (lowercase):
  discovered, applied, recruiter_contact, user_reply, 
  interview_scheduled, interview_completed, test_scheduled, 
  test_completed, offer_received, rejection, follow_up, 
  status_change, note, historical_note
EOF
}

cmd_next_id() {
  get_next_id
}

cmd_add() {
  local company="" role="" location="" salary="" source="" url=""
  local employer_id="" status="Discovered" contacts="" next_action=""
  local resume="" cover_letter="" strict_contacts=true
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --company)      company="$2"; shift 2 ;;
      --role)         role="$2"; shift 2 ;;
      --location)     location="$2"; shift 2 ;;
      --salary)       salary="$2"; shift 2 ;;
      --source)       source="$2"; shift 2 ;;
      --url)          url="$2"; shift 2 ;;
      --employer-id)  employer_id="$2"; shift 2 ;;
      --status)       status="$2"; shift 2 ;;
      --contacts)     contacts="$2"; shift 2 ;;
      --next-action)  next_action="$2"; shift 2 ;;
      --resume)       resume="$2"; shift 2 ;;
      --cover-letter) cover_letter="$2"; shift 2 ;;
      --no-strict-contacts) strict_contacts=false; shift ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  [[ -z "$company" ]] && err "Required: --company"
  [[ -z "$role" ]] && err "Required: --role"
  
  # Validate and normalize status to Title Case
  status=$(validate_status "$status")
  
  # Validate contacts (Google Contacts links only)
  if [[ -n "$contacts" ]] && $strict_contacts; then
    if ! validate_contacts "$contacts"; then
      err "Invalid contacts. Use --no-strict-contacts to allow non-Google Contacts links."
    fi
  fi
  
  local job_id
  job_id=$(get_next_id)
  local applied_date=""
  [[ "$status" != "Discovered" ]] && applied_date=$(today)
  
  # Build JSON row (columns A-O, skip P which is formula)
  local row_json
  row_json=$(python3 << EOF
import json
row = [
    "$job_id",
    "$employer_id",
    "$company",
    "$role",
    "$location",
    "$salary",
    "$source",
    "$url",
    "$status",
    "$applied_date",
    "$contacts",
    "$next_action",
    "",
    "$resume",
    "$cover_letter"
]
print(json.dumps([row]))
EOF
)
  
  # Find the next empty row (starting from row 2 to skip header)
  # We need to find the actual next row, not rely on append's detection
  local next_row
  next_row=$(gog sheets get "$SPREADSHEET_ID" "${JOBS_TAB}!A:A" --plain 2>/dev/null | wc -l)
  next_row=$((next_row + 1))
  # But we need to find first truly empty row - scan from a reasonable start
  # For safety, start from 2 and find first row where column A is empty
  local scan_row=2
  while true; do
    local cell_value
    cell_value=$(gog sheets get "$SPREADSHEET_ID" "${JOBS_TAB}!A${scan_row}" --plain 2>/dev/null | tr -d '[:space:]')
    if [[ -z "$cell_value" ]]; then
      next_row=$scan_row
      break
    fi
    ((scan_row++))
    # Safety limit
    if [[ $scan_row -gt 5000 ]]; then
      err "Could not find empty row within first 5000 rows"
    fi
  done
  
  # Use update instead of append to insert at specific row
  gog sheets update "$SPREADSHEET_ID" "${JOBS_TAB}!A${next_row}:O${next_row}" --values-json "$row_json" > /dev/null
  
  # Add initial log entry
  local log_json
  log_json=$(python3 << EOF
import json
print(json.dumps([["$(now_ts)", "$job_id", "discovered", "Job added: $role at $company"]]))
EOF
)
  gog sheets append "$SPREADSHEET_ID" "'${LOGS_TAB}'!A:D" --values-json "$log_json" > /dev/null
  
  # Add formula for log column
  local row_num
  row_num=$(find_job_row "$job_id")
  if [[ "$row_num" != "0" ]]; then
    local formula="=IFERROR(TEXTJOIN(CHAR(10),TRUE,QUERY(Logs!A:D,\"SELECT A,C,D WHERE B='\"&A${row_num}&\"' ORDER BY A DESC LIMIT 3\")),\"\")"
    local formula_json
    formula_json=$(python3 -c "import json; print(json.dumps([['$formula']]))")
    gog sheets update "$SPREADSHEET_ID" "${JOBS_TAB}!P${row_num}" --input=USER_ENTERED --values-json "$formula_json" > /dev/null
  fi
  
  info "Created $job_id: $role at $company"
}

cmd_log() {
  local job_id="" event="" details=""
  
  # First positional arg is job_id
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    job_id="$1"
    shift
  fi
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --event)   event="$2"; shift 2 ;;
      --details) details="$2"; shift 2 ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  [[ -z "$job_id" ]] && err "Required: job_id (positional)"
  [[ -z "$event" ]] && err "Required: --event"
  [[ -z "$details" ]] && err "Required: --details"
  
  validate_event "$event"
  
  # Verify job exists
  local row
  row=$(find_job_row "$job_id")
  [[ "$row" == "0" ]] && err "Job not found: $job_id"
  
  # Add log entry
  local log_json
  log_json=$(python3 << EOF
import json
print(json.dumps([["$(now_ts)", "$job_id", "$event", """$details"""]]))
EOF
)
  gog sheets append "$SPREADSHEET_ID" "'${LOGS_TAB}'!A:D" --values-json "$log_json" > /dev/null
  
  info "Logged '$event' for $job_id"
}

cmd_update() {
  local job_id="" strict_contacts=true
  declare -A updates
  
  # First positional arg is job_id
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    job_id="$1"
    shift
  fi
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --employer-id)  updates[employer_job_id]="$2"; shift 2 ;;
      --company)      updates[company]="$2"; shift 2 ;;
      --role)         updates[role]="$2"; shift 2 ;;
      --location)     updates[location]="$2"; shift 2 ;;
      --salary)       updates[salary]="$2"; shift 2 ;;
      --source)       updates[source]="$2"; shift 2 ;;
      --url)          updates[url]="$2"; shift 2 ;;
      --status)       updates[status]="$2"; shift 2 ;;
      --applied-date) updates[applied_date]="$2"; shift 2 ;;
      --contacts)     updates[contacts]="$2"; shift 2 ;;
      --next-action)  updates[next_action]="$2"; shift 2 ;;
      --next-date)    updates[next_date]="$2"; shift 2 ;;
      --resume)       updates[resume]="$2"; shift 2 ;;
      --cover-letter) updates[cover_letter]="$2"; shift 2 ;;
      --no-strict-contacts) strict_contacts=false; shift ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  [[ -z "$job_id" ]] && err "Required: job_id (positional)"
  [[ ${#updates[@]} -eq 0 ]] && err "No fields to update"
  
  # Validate and normalize status if provided
  if [[ -v updates[status] ]]; then
    updates[status]=$(validate_status "${updates[status]}")
  fi
  
  # Validate contacts if provided
  if [[ -v updates[contacts] ]] && $strict_contacts; then
    if ! validate_contacts "${updates[contacts]}"; then
      err "Invalid contacts. Use --no-strict-contacts to allow non-Google Contacts links."
    fi
  fi
  
  # Find job row
  local row
  row=$(find_job_row "$job_id")
  [[ "$row" == "0" ]] && err "Job not found: $job_id"
  
  # Update each field
  local updated_fields=()
  for field in "${!updates[@]}"; do
    local col="${COL_LETTER[$field]}"
    local val="${updates[$field]}"
    local val_json
    val_json=$(python3 -c "import json; print(json.dumps([['$val']]))")
    gog sheets update "$SPREADSHEET_ID" "${JOBS_TAB}!${col}${row}" --values-json "$val_json" > /dev/null
    updated_fields+=("$field")
  done
  
  # Log status change if status was updated
  if [[ -v updates[status] ]]; then
    local log_json
    log_json=$(python3 << EOF
import json
print(json.dumps([["$(now_ts)", "$job_id", "status_change", "Status changed to: ${updates[status]}"]]))
EOF
)
    gog sheets append "$SPREADSHEET_ID" "'${LOGS_TAB}'!A:D" --values-json "$log_json" > /dev/null
  fi
  
  info "Updated $job_id: ${updated_fields[*]}"
}

cmd_show() {
  local job_id="$1"
  [[ -z "$job_id" ]] && err "Required: job_id"
  
  local row
  row=$(find_job_row "$job_id")
  [[ "$row" == "0" ]] && err "Job not found: $job_id"
  
  # Get job data using awk for proper TSV parsing
  local data
  data=$(gog sheets get "$SPREADSHEET_ID" "${JOBS_TAB}!A${row}:O${row}" --plain)
  
  # Parse with awk to handle tabs properly
  local our_id emp_id company role location salary source url status applied contacts next_action next_date resume cover
  
  our_id=$(echo "$data" | awk -F'\t' '{print $1}')
  emp_id=$(echo "$data" | awk -F'\t' '{print $2}')
  company=$(echo "$data" | awk -F'\t' '{print $3}')
  role=$(echo "$data" | awk -F'\t' '{print $4}')
  location=$(echo "$data" | awk -F'\t' '{print $5}')
  salary=$(echo "$data" | awk -F'\t' '{print $6}')
  source=$(echo "$data" | awk -F'\t' '{print $7}')
  url=$(echo "$data" | awk -F'\t' '{print $8}')
  status=$(echo "$data" | awk -F'\t' '{print $9}')
  applied=$(echo "$data" | awk -F'\t' '{print $10}')
  contacts=$(echo "$data" | awk -F'\t' '{print $11}')
  next_action=$(echo "$data" | awk -F'\t' '{print $12}')
  next_date=$(echo "$data" | awk -F'\t' '{print $13}')
  resume=$(echo "$data" | awk -F'\t' '{print $14}')
  cover=$(echo "$data" | awk -F'\t' '{print $15}')
  
  cat << EOF
═══════════════════════════════════════════════════════════
$our_id: $role
═══════════════════════════════════════════════════════════
Company:        $company
Employer ID:    ${emp_id:--}
Location:       ${location:--}
Salary:         ${salary:--}
Source:         ${source:--}
URL:            ${url:--}
Status:         $status
Applied:        ${applied:--}
Contacts:       ${contacts:--}
Next Action:    ${next_action:--}
Next Date:      ${next_date:--}
Resume:         ${resume:--}
Cover Letter:   ${cover:--}
───────────────────────────────────────────────────────────
Recent Activity:
EOF
  
  # Get logs for this job
  while IFS=$'\t' read -r ts jid event details; do
    [[ "$jid" == "$job_id" ]] && echo "  [$ts] $event: $details"
  done < <(get_all_logs | tac | head -10)
}

cmd_list() {
  local status="" limit=50 format="table"
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --status) status="$2"; shift 2 ;;
      --limit)  limit="$2"; shift 2 ;;
      --json)   format="json"; shift ;;
      --tsv)    format="tsv"; shift ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  local data
  data=$(get_all_jobs)
  
  # Filter by status if specified (normalize to Title Case for comparison)
  if [[ -n "$status" ]]; then
    local normalized_status
    normalized_status=$(validate_status "$status") || exit 1
    # Case-insensitive match since sheet may have variations
    data=$(echo "$data" | awk -F'\t' -v s="$normalized_status" 'tolower($9) == tolower(s)')
  fi
  
  # Limit results
  data=$(echo "$data" | head -n "$limit")
  
  case "$format" in
    json)
      echo "$data" | python3 << 'EOF'
import sys, json
rows = []
for line in sys.stdin:
    if line.strip():
        parts = line.strip().split('\t')
        # Pad to 15 columns
        while len(parts) < 15:
            parts.append('')
        rows.append({
            'our_job_id': parts[0],
            'employer_job_id': parts[1],
            'company': parts[2],
            'role': parts[3],
            'location': parts[4],
            'salary': parts[5],
            'source': parts[6],
            'url': parts[7],
            'status': parts[8],
            'applied_date': parts[9],
            'contacts': parts[10],
            'next_action': parts[11],
            'next_date': parts[12],
            'resume': parts[13],
            'cover_letter': parts[14]
        })
print(json.dumps(rows, indent=2))
EOF
      ;;
    tsv)
      echo -e "our_job_id\tcompany\trole\tstatus\tnext_action"
      echo "$data" | awk -F'\t' '{printf "%s\t%s\t%s\t%s\t%s\n", $1, $3, $4, $9, $12}'
      ;;
    table)
      printf "%-8s %-25s %-35s %-15s\n" "ID" "COMPANY" "ROLE" "STATUS"
      printf "%-8s %-25s %-35s %-15s\n" "--------" "-------------------------" "-----------------------------------" "---------------"
      echo "$data" | awk -F'\t' '{printf "%-8s %-25.25s %-35.35s %-15s\n", $1, $3, $4, $9}'
      ;;
  esac
}

cmd_search() {
  local query="" columns="" use_regex=false use_fuzzy=false case_insensitive=true
  
  # First positional arg is query
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    query="$1"
    shift
  fi
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --columns|-c) columns="$2"; shift 2 ;;
      --regex|-r)   use_regex=true; shift ;;
      --fuzzy|-f)   use_fuzzy=true; shift ;;
      --case|-C)    case_insensitive=false; shift ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  [[ -z "$query" ]] && err "Required: search query"
  
  # Parse columns to search (default: all searchable)
  local col_indices=()
  if [[ -n "$columns" ]]; then
    IFS=',' read -ra cols <<< "$columns"
    for col in "${cols[@]}"; do
      col=$(echo "$col" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr '-' '_')
      if [[ -v COL_INDEX[$col] ]]; then
        col_indices+=("${COL_INDEX[$col]}")
      else
        err "Unknown column: $col. Valid: ${!COL_INDEX[*]}"
      fi
    done
  else
    # Default: search company, role, contacts, source
    col_indices=(3 4 11 7)
  fi
  
  local data
  data=$(get_all_jobs)
  
  # Build awk search command
  local awk_conditions=()
  for idx in "${col_indices[@]}"; do
    if $use_regex; then
      if $case_insensitive; then
        awk_conditions+=("tolower(\$$idx) ~ tolower(\"$query\")")
      else
        awk_conditions+=("\$$idx ~ \"$query\"")
      fi
    else
      if $case_insensitive; then
        awk_conditions+=("index(tolower(\$$idx), tolower(\"$query\")) > 0")
      else
        awk_conditions+=("index(\$$idx, \"$query\") > 0")
      fi
    fi
  done
  
  local condition
  condition=$(IFS='||'; echo "${awk_conditions[*]}")
  
  local results
  if $use_fuzzy && command -v fzf &> /dev/null; then
    # Fuzzy search with fzf
    results=$(echo "$data" | fzf --filter="$query" 2>/dev/null || true)
  else
    results=$(echo "$data" | awk -F'\t' "$condition")
  fi
  
  if [[ -z "$results" ]]; then
    info "No matches found for '$query'"
    return 0
  fi
  
  # Display results
  printf "%-8s %-25s %-35s %-15s\n" "ID" "COMPANY" "ROLE" "STATUS"
  printf "%-8s %-25s %-35s %-15s\n" "--------" "-------------------------" "-----------------------------------" "---------------"
  echo "$results" | awk -F'\t' '{printf "%-8s %-25.25s %-35.35s %-15s\n", $1, $3, $4, $9}'
}

cmd_logs() {
  local job_id="" limit=20
  
  # First positional arg is job_id (optional)
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    job_id="$1"
    shift
  fi
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --limit|-n) limit="$2"; shift 2 ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  local data
  data=$(get_all_logs)
  
  if [[ -n "$job_id" ]]; then
    data=$(echo "$data" | awk -F'\t' -v id="$job_id" '$2 == id')
  fi
  
  # Show most recent first
  data=$(echo "$data" | tac | head -n "$limit")
  
  printf "%-16s %-8s %-20s %s\n" "TIMESTAMP" "JOB" "EVENT" "DETAILS"
  printf "%-16s %-8s %-20s %s\n" "----------------" "--------" "--------------------" "----------------------------------------"
  echo "$data" | while IFS=$'\t' read -r ts job event details; do
    printf "%-16s %-8s %-20s %.60s\n" "$ts" "$job" "$event" "$details"
  done
}

cmd_help() {
  cat << 'EOF'
job-tracker - CRUD CLI for Job Applications Tracker

COMMANDS:
  add       Add a new job to tracker
  log       Add activity log entry for a job
  update    Update job fields
  delete    Delete a job (clears row, preserves logs)
  show      Show detailed view of a job
  list      List jobs with optional filters
  search    Search jobs by text (regex or fuzzy)
  logs      View activity logs
  next-id   Get next available job ID
  schema    Show column schema and valid values
  help      Show this help

EXAMPLES:
  # Add a new job
  job-tracker add --company "Morgan Stanley" --role "AI Architect" \
    --source LinkedIn --salary "\$200k" --location "NYC"

  # Add with Google Contacts links
  job-tracker add --company "Citi" --role "VP AI" \
    --contacts "https://contacts.google.com/person/c123456789"

  # Allow non-Google Contacts (bypass validation)
  job-tracker add --company "Test" --role "Engineer" \
    --contacts "recruiter@example.com" --no-strict-contacts

  # Log an event
  job-tracker log JOB002 --event interview_scheduled \
    --details "3rd round Monday 10am with VP Engineering"

  # Update status (auto-normalizes to Title Case)
  job-tracker update JOB002 --status interview --salary "\$180k-\$220k"

  # Delete a job (with confirmation)
  job-tracker delete JOB002

  # Delete without confirmation
  job-tracker delete JOB002 --force

  # Show job details
  job-tracker show JOB002

  # List by status
  job-tracker list --status discovered
  job-tracker list --status interview --json

  # Search
  job-tracker search "citi" --columns company
  job-tracker search "AI.*Architect" --regex --columns role
  job-tracker search "morgan" --fuzzy

  # View logs
  job-tracker logs JOB002 --limit 5
  job-tracker logs --limit 50

VALID STATUSES (Title Case):
  Discovered, Applied, Screening, Interview, Karat Test Scheduled,
  Offer, Rejected, Withdrawn, Accepted, Closed

VALID EVENT TYPES (lowercase):
  discovered, applied, recruiter_contact, user_reply,
  interview_scheduled, interview_completed, test_scheduled,
  test_completed, offer_received, rejection, follow_up,
  status_change, note, historical_note

CONTACTS VALIDATION:
  By default, --contacts must be Google Contacts links:
    https://contacts.google.com/person/c[alphanumeric]
  
  Multiple links can be separated by commas, semicolons, or spaces.
  Use --no-strict-contacts to bypass validation.

SEARCH COLUMNS:
  our_job_id, employer_job_id, company, role, location, salary,
  source, url, status, applied_date, contacts, next_action,
  next_date, resume, cover_letter

  Multiple columns: --columns "company,role,contacts"
EOF
}

# === Main ===

# Delete a job (clears the row, preserves activity logs)
cmd_delete() {
  local job_id="" force=false
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force|-f) force=true; shift ;;
      JOB*) job_id="$1"; shift ;;
      *) err "Unknown option: $1" ;;
    esac
  done
  
  [[ -z "$job_id" ]] && err "Required: job_id (e.g., JOB002)"
  
  local row
  row=$(find_job_row "$job_id")
  [[ "$row" == "0" ]] && err "Job not found: $job_id"
  
  # Get job details for confirmation
  local job_data company role
  job_data=$(gog sheets get "$SPREADSHEET_ID" "${JOBS_TAB}!A${row}:D${row}" --plain)
  company=$(echo "$job_data" | awk -F'\t' '{print $3}')
  role=$(echo "$job_data" | awk -F'\t' '{print $4}')
  
  if [[ "$force" != "true" ]]; then
    echo "About to delete: $job_id - $role at $company"
    echo "This will clear the job row but preserve activity logs."
    read -r -p "Continue? [y/N] " confirm
    [[ "${confirm,,}" != "y" ]] && { echo "Cancelled."; exit 0; }
  fi
  
  # Clear the row (preserves row structure for sheet formulas)
  gog sheets clear "$SPREADSHEET_ID" "${JOBS_TAB}!A${row}:P${row}" > /dev/null
  
  info "Deleted $job_id: $role at $company"
}

main() {
  local cmd="${1:-help}"
  shift || true
  
  case "$cmd" in
    add)     cmd_add "$@" ;;
    log)     cmd_log "$@" ;;
    update)  cmd_update "$@" ;;
    delete)  cmd_delete "$@" ;;
    show)    cmd_show "$@" ;;
    list)    cmd_list "$@" ;;
    search)  cmd_search "$@" ;;
    logs)    cmd_logs "$@" ;;
    next-id) cmd_next_id ;;
    schema)  cmd_schema ;;
    help|-h|--help) cmd_help ;;
    *) err "Unknown command: $cmd. Run 'job-tracker help' for usage." ;;
  esac
}

main "$@"
