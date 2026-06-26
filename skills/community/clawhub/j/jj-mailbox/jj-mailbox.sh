#!/usr/bin/env bash
# jj-mailbox sync daemon
# Periodically syncs the mailbox repo via jj + git remote
set -euo pipefail

VERSION="0.1.0"
DEFAULT_INTERVAL=30

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[jj-mailbox]${NC} $(date -u +%H:%M:%S) $*"; }
ok()  { echo -e "${GREEN}[jj-mailbox]${NC} $(date -u +%H:%M:%S) $*"; }
warn(){ echo -e "${YELLOW}[jj-mailbox]${NC} $(date -u +%H:%M:%S) $*"; }
err() { echo -e "${RED}[jj-mailbox]${NC} $(date -u +%H:%M:%S) $*" >&2; }

usage() {
  cat <<EOF
jj-mailbox v${VERSION} — file-based message passing for AI agents

Usage:
  jj-mailbox init <repo-path> [--remote <git-url>]    Initialize a mailbox repo
  jj-mailbox register <name> [--desc <description>]    Register an agent
  jj-mailbox send <to> <subject> <body> [--refs <ids>]  Send a message (--refs: comma-separated message ids)
  jj-mailbox inbox [--agent <name>]                    Check inbox
  jj-mailbox sync [--interval <seconds>]               Run sync loop
  jj-mailbox status                                    Show all agents' status
  jj-mailbox help                                      Show this help

Environment:
  JJ_MAILBOX_REPO     Path to mailbox repo (default: current directory)
  JJ_MAILBOX_AGENT    Current agent name (default: hostname)
  JJ_MAILBOX_INTERVAL Sync interval in seconds (default: ${DEFAULT_INTERVAL})
EOF
}

# --- Helpers ---

get_repo() {
  echo "${JJ_MAILBOX_REPO:-$(pwd)}"
}

get_agent() {
  echo "${JJ_MAILBOX_AGENT:-$(hostname)}"
}

ensure_repo() {
  local repo
  repo="$(get_repo)"
  if [[ ! -d "${repo}/.jj" ]]; then
    err "Not a jj-mailbox repo: ${repo}"
    err "Run 'jj-mailbox init <path>' first."
    exit 1
  fi
}

ensure_jj() {
  if ! command -v jj &>/dev/null; then
    err "jj (Jujutsu) is not installed."
    err "Install: https://jj-vcs.dev/docs/install/"
    exit 1
  fi
}

gen_id() {
  # Try multiple methods for portability
  if command -v xxd &>/dev/null; then
    head -c 4 /dev/urandom | xxd -p
  elif command -v od &>/dev/null; then
    head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n'
  else
    printf '%04x%04x' $RANDOM $RANDOM
  fi
}

ts_filename() {
  date -u +"%Y-%m-%dT%H-%M-%SZ"
}

ts_iso() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# --- Commands ---

cmd_init() {
  ensure_jj
  local repo="${1:-.}"
  local remote="${2:-}"

  mkdir -p "${repo}"
  cd "${repo}"

  if [[ -d .jj ]]; then
    warn "Already initialized: ${repo}"
    return 0
  fi

  # Initialize jj with git backend
  if [[ -n "${remote}" ]]; then
    log "Cloning from ${remote}..."
    jj git clone --colocate "${remote}" .
  else
    log "Initializing new mailbox repo..."
    jj git init --colocate
  fi

  # Create directory structure
  mkdir -p agents inbox shared/{tasks,knowledge,artifacts}

  # Create AGENTS.md
  cat > AGENTS.md <<'AGENTS'
# Registered Agents

| Name | Description | Status |
|------|-------------|--------|

<!-- Auto-updated by jj-mailbox -->
AGENTS

  # Create .gitignore
  cat > .gitignore <<'GI'
# OS
.DS_Store
Thumbs.db

# Temp
*.tmp
*.swp
GI

  jj commit -m "Initialize jj-mailbox repo"

  ok "Mailbox repo initialized at: $(pwd)"
  if [[ -z "${remote}" ]]; then
    log "Tip: add a remote with 'jj git remote add origin <url>'"
  fi
}

cmd_register() {
  ensure_repo
  ensure_jj
  local name="${1:?Usage: jj-mailbox register <name>}"
  local desc="${2:-Agent ${name}}"
  local repo
  repo="$(get_repo)"
  cd "${repo}"

  # Create agent directories
  mkdir -p "agents/${name}" "inbox/${name}/new" "inbox/${name}/processed"

  # Write profile
  cat > "agents/${name}/profile.json" <<EOF
{
  "name": "${name}",
  "description": "${desc}",
  "capabilities": [],
  "platform": "openclaw",
  "created": "$(ts_iso)"
}
EOF

  # Write initial status
  cat > "agents/${name}/status.json" <<EOF
{
  "status": "online",
  "last_seen": "$(ts_iso)",
  "current_task": null
}
EOF

  # Add placeholder to keep dirs in git
  touch "inbox/${name}/new/.gitkeep"
  touch "inbox/${name}/processed/.gitkeep"

  jj commit -m "Register agent: ${name}"

  ok "Agent '${name}' registered."
  log "Set JJ_MAILBOX_AGENT=${name} to use as current agent."
}

cmd_send() {
  ensure_repo
  ensure_jj
  local to="${1:?Usage: jj-mailbox send <to> <subject> <body> [--refs <id1,id2,...>]}"
  local subject="${2:?}"
  local body="${3:?}"
  local refs_arg=""
  local from
  from="$(get_agent)"
  local repo
  repo="$(get_repo)"

  # Parse optional --refs flag (remaining args after positional 3)
  shift 3 || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --refs) refs_arg="${2:-}"; shift 2 ;;
      *) shift ;;
    esac
  done

  cd "${repo}"

  # Verify recipient exists
  if [[ ! -d "inbox/${to}/new" ]]; then
    err "Unknown agent: ${to}"
    err "Registered agents:"
    ls agents/ 2>/dev/null || echo "  (none)"
    exit 1
  fi

  local msg_id="msg-$(gen_id)"
  local ts
  ts="$(ts_filename)"
  local filename="${ts}_${from}_${msg_id}.json"

  # Build refs JSON array from comma-separated ids (pure bash, no python)
  local refs_json="[]"
  if [[ -n "${refs_arg}" ]]; then
    local _refs_arr _r _first=true
    refs_json="["
    IFS=',' read -ra _refs_arr <<< "${refs_arg}"
    for _r in "${_refs_arr[@]}"; do
      _r="${_r// /}"
      [[ -z "${_r}" ]] && continue
      ${_first} || refs_json+=","
      refs_json+="\"${_r}\""
      _first=false
    done
    refs_json+="]"
  fi

  cat > "inbox/${to}/new/${filename}" <<EOF
{
  "version": "0.1",
  "id": "${msg_id}",
  "timestamp": "$(ts_iso)",
  "from": "${from}",
  "to": "${to}",
  "type": "message",
  "subject": "${subject}",
  "body": "${body}",
  "refs": ${refs_json},
  "metadata": {}
}
EOF

  jj commit -m "${from} → ${to}: ${subject}"

  ok "Message sent: ${from} → ${to}"
  log "  Subject: ${subject}"
  log "  File: inbox/${to}/new/${filename}"
  log "  ID: ${msg_id}"
  echo "${msg_id}"
}

cmd_inbox() {
  ensure_repo
  local agent="${1:-$(get_agent)}"
  local repo
  repo="$(get_repo)"
  cd "${repo}"

  local inbox_dir="inbox/${agent}/new"
  if [[ ! -d "${inbox_dir}" ]]; then
    err "No inbox for agent: ${agent}"
    exit 1
  fi

  local count
  count=$(find "${inbox_dir}" -name '*.json' 2>/dev/null | wc -l | tr -d ' ')

  if [[ "${count}" -eq 0 ]]; then
    log "Inbox empty for ${agent}."
    return 0
  fi

  ok "${count} message(s) for ${agent}:"
  echo ""

  # Sort by filename (which starts with timestamp)
  find "${inbox_dir}" -name '*.json' | sort | while read -r f; do
    local from subject ts _fields
    # Single python3 call to extract all fields (instead of 3 separate calls)
    # Uses sys.argv to pass file path safely (no bash variable interpolation in python)
    _fields=$(python3 -c "
import json,sys
m=json.load(open(sys.argv[1]))
print(m.get('from','?') + '\t' + m.get('subject','?') + '\t' + m.get('timestamp','?'))
" "$f" 2>/dev/null) || _fields=$'?\t?\t?'
    IFS=$'\t' read -r from subject ts <<< "${_fields}"
    echo -e "  ${GREEN}From:${NC} ${from}  ${BLUE}Subject:${NC} ${subject}  ${YELLOW}Time:${NC} ${ts}"
  done
  echo ""
}

cmd_read_and_process() {
  # Read one message and move to processed
  ensure_repo
  local agent="${1:-$(get_agent)}"
  local repo
  repo="$(get_repo)"
  cd "${repo}"

  local inbox_dir="inbox/${agent}/new"
  local processed_dir="inbox/${agent}/processed"

  local oldest
  oldest=$(find "${inbox_dir}" -name '*.json' 2>/dev/null | sort | head -1)

  if [[ -z "${oldest}" ]]; then
    echo ""
    return 1
  fi

  # Output the message content
  cat "${oldest}"

  # Move to processed
  mv "${oldest}" "${processed_dir}/"

  return 0
}

cmd_sync() {
  ensure_repo
  ensure_jj
  local interval="${1:-${JJ_MAILBOX_INTERVAL:-${DEFAULT_INTERVAL}}}"
  local repo
  repo="$(get_repo)"
  cd "${repo}"

  log "Starting sync loop (interval: ${interval}s)"
  log "Repo: ${repo}"
  log "Press Ctrl+C to stop."
  echo ""

  while true; do
    # Update agent status
    local agent
    agent="$(get_agent)"
    if [[ -f "agents/${agent}/status.json" ]]; then
      # Pass file path and timestamp as arguments (no bash variable interpolation in python)
      python3 -c "
import json,sys
path, ts = sys.argv[1], sys.argv[2]
with open(path, 'r+') as f:
    s = json.load(f)
    s['last_seen'] = ts
    f.seek(0); json.dump(s, f, indent=2); f.truncate()
" "agents/${agent}/status.json" "$(ts_iso)" 2>/dev/null || true
    fi

    # Fetch
    if jj git fetch --all-remotes 2>/dev/null; then
      log "⬇ Fetched remote changes"
    fi

    # Snapshot working copy (jj does this automatically)
    jj status >/dev/null 2>&1 || true

    # Check inbox
    local count
    count=$(find "inbox/${agent}/new" -name '*.json' 2>/dev/null | wc -l | tr -d ' ')
    if [[ "${count}" -gt 0 ]]; then
      ok "📬 ${count} new message(s) in inbox"
    fi

    # Push
    if jj git push --all 2>/dev/null; then
      log "⬆ Pushed local changes"
    fi

    sleep "${interval}"
  done
}

cmd_status() {
  ensure_repo
  local repo
  repo="$(get_repo)"
  cd "${repo}"

  log "Agent Status:"
  echo ""

  for agent_dir in agents/*/; do
    [[ -d "${agent_dir}" ]] || continue
    local name
    name=$(basename "${agent_dir}")
    local status="?"
    local last_seen="?"
    local inbox_count=0

    if [[ -f "${agent_dir}/status.json" ]]; then
      # Single python3 call to extract both fields (instead of 2 separate calls)
      local _status_fields
      _status_fields=$(python3 -c "
import json,sys
s=json.load(open(sys.argv[1]))
print(s.get('status','?'), s.get('last_seen','?'))
" "${agent_dir}/status.json" 2>/dev/null) || _status_fields="? ?"
      read -r status last_seen <<< "${_status_fields}"
    fi

    if [[ -d "inbox/${name}/new" ]]; then
      inbox_count=$(find "inbox/${name}/new" -name '*.json' 2>/dev/null | wc -l | tr -d ' ')
    fi

    local status_icon="⚪"
    [[ "${status}" == "online" ]] && status_icon="🟢"
    [[ "${status}" == "busy" ]] && status_icon="🟡"
    [[ "${status}" == "offline" ]] && status_icon="🔴"

    echo -e "  ${status_icon} ${name}  (${status})  📬 ${inbox_count} msg  🕐 ${last_seen}"
  done
  echo ""
}

# --- Main ---

main() {
  local cmd="${1:-help}"
  shift || true

  case "${cmd}" in
    init)     cmd_init "$@" ;;
    register) cmd_register "$@" ;;
    send)     cmd_send "$@" ;;
    inbox)    cmd_inbox "$@" ;;
    read)     cmd_read_and_process "$@" ;;
    sync)     cmd_sync "$@" ;;
    status)   cmd_status "$@" ;;
    version)  echo "jj-mailbox v${VERSION}" ;;
    help|*)   usage ;;
  esac
}

main "$@"
