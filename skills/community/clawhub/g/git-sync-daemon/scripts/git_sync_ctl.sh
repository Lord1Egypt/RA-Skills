#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAEMON_SCRIPT="${SCRIPT_DIR}/git_sync_daemon.sh"

STATE_DIR="${GIT_SYNC_STATE_DIR:-$HOME/.config/git-sync-daemon}"
REPO_FILE="${GIT_SYNC_REPO_FILE:-$STATE_DIR/repos.conf}"
LOG_FILE="${GIT_SYNC_LOG_FILE:-$STATE_DIR/git-sync-daemon.log}"
INTERVAL="${GIT_SYNC_INTERVAL:-60}"
TIMEOUT_SECS="${GIT_SYNC_GIT_TIMEOUT:-45}"
LABEL="${GIT_SYNC_LAUNCHD_LABEL:-com.samwei12.git-sync-daemon}"
PLIST_PATH="${GIT_SYNC_LAUNCHD_PLIST:-$HOME/Library/LaunchAgents/${LABEL}.plist}"
SYSTEMD_UNIT="${GIT_SYNC_SYSTEMD_UNIT:-git-sync-daemon.service}"

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

ensure_state() {
  mkdir -p "$STATE_DIR"
  mkdir -p "$(dirname "$LOG_FILE")"
  touch "$LOG_FILE"
  if [[ ! -f "$REPO_FILE" ]]; then
    cat > "$REPO_FILE" <<EOF
# git-sync-daemon repo list
# format:
# /absolute/path/to/repo|remote=origin|branch=main|enabled=1
EOF
  fi
}

usage() {
  cat <<EOF
Usage: $(basename "$0") <command> [args]

Commands:
  init
  add-repo <repo_path> [branch] [remote]
  remove-repo <repo_path>
  list-repos
  run-once
  status
  install-launchd
  uninstall-launchd
  install-systemd
  uninstall-systemd
EOF
}

normalize_repo() {
  local input="$1"
  if [[ ! -d "$input" ]]; then
    echo "repo path does not exist: $input" >&2
    exit 1
  fi
  if ! git -C "$input" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "not a git repository: $input" >&2
    exit 1
  fi
  (cd "$input" && pwd -P)
}

upsert_repo_line() {
  local repo="$1"
  local branch="$2"
  local remote="$3"
  local newline="$repo|remote=$remote|branch=$branch|enabled=1"
  local tmp
  tmp="$(mktemp)"
  local found=0

  while IFS= read -r line || [[ -n "$line" ]]; do
    local clean candidate
    clean="$(trim "${line%%#*}")"
    if [[ -z "$clean" ]]; then
      printf '%s\n' "$line" >> "$tmp"
      continue
    fi
    candidate="$(trim "${clean%%|*}")"
    if [[ "$candidate" == "$repo" ]]; then
      printf '%s\n' "$newline" >> "$tmp"
      found=1
    else
      printf '%s\n' "$line" >> "$tmp"
    fi
  done < "$REPO_FILE"

  if [[ "$found" -eq 0 ]]; then
    printf '%s\n' "$newline" >> "$tmp"
  fi
  mv "$tmp" "$REPO_FILE"
}

remove_repo_line() {
  local repo="$1"
  local tmp
  tmp="$(mktemp)"
  while IFS= read -r line || [[ -n "$line" ]]; do
    local clean candidate
    clean="$(trim "${line%%#*}")"
    if [[ -z "$clean" ]]; then
      printf '%s\n' "$line" >> "$tmp"
      continue
    fi
    candidate="$(trim "${clean%%|*}")"
    if [[ "$candidate" != "$repo" ]]; then
      printf '%s\n' "$line" >> "$tmp"
    fi
  done < "$REPO_FILE"
  mv "$tmp" "$REPO_FILE"
}

cmd_init() {
  ensure_state
  echo "initialized"
  echo "state_dir: $STATE_DIR"
  echo "repo_file: $REPO_FILE"
  echo "log_file: $LOG_FILE"
}

cmd_add_repo() {
  ensure_state
  local repo_path="${1:-}"
  local branch="${2:-}"
  local remote="${3:-origin}"
  if [[ -z "$repo_path" ]]; then
    echo "missing repo_path" >&2
    usage
    exit 1
  fi

  local repo_abs
  repo_abs="$(normalize_repo "$repo_path")"
  if [[ -z "$branch" ]]; then
    branch="$(git -C "$repo_abs" symbolic-ref --quiet --short HEAD || true)"
  fi
  if [[ -z "$branch" ]]; then
    echo "cannot detect branch for repo: $repo_abs" >&2
    exit 1
  fi

  upsert_repo_line "$repo_abs" "$branch" "$remote"
  echo "repo added/updated: $repo_abs (remote=$remote branch=$branch)"
}

cmd_remove_repo() {
  ensure_state
  local repo_path="${1:-}"
  if [[ -z "$repo_path" ]]; then
    echo "missing repo_path" >&2
    usage
    exit 1
  fi
  local repo_abs
  repo_abs="$(normalize_repo "$repo_path")"
  remove_repo_line "$repo_abs"
  echo "repo removed: $repo_abs"
}

cmd_list_repos() {
  ensure_state
  awk 'BEGIN{n=0}
    /^[[:space:]]*#/ {next}
    /^[[:space:]]*$/ {next}
    {n++; printf "%d. %s\n", n, $0}
    END{if(n==0) print "(empty)"}' "$REPO_FILE"
}

cmd_run_once() {
  ensure_state
  GIT_SYNC_INTERVAL="$INTERVAL" \
  GIT_SYNC_REPO_FILE="$REPO_FILE" \
  GIT_SYNC_LOG_FILE="$LOG_FILE" \
  GIT_SYNC_GIT_TIMEOUT="$TIMEOUT_SECS" \
  /bin/bash "$DAEMON_SCRIPT" --once
}

cmd_install_launchd() {
  ensure_state
  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "install-launchd only works on macOS" >&2
    exit 1
  fi

  mkdir -p "$HOME/Library/LaunchAgents"
  cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${DAEMON_SCRIPT}</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>GIT_SYNC_INTERVAL</key>
    <string>${INTERVAL}</string>
    <key>GIT_SYNC_REPO_FILE</key>
    <string>${REPO_FILE}</string>
    <key>GIT_SYNC_LOG_FILE</key>
    <string>${LOG_FILE}</string>
    <key>GIT_SYNC_GIT_TIMEOUT</key>
    <string>${TIMEOUT_SECS}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${LOG_FILE}</string>
  <key>StandardErrorPath</key>
  <string>${LOG_FILE}</string>
</dict>
</plist>
EOF

  plutil -lint "$PLIST_PATH" >/dev/null
  local uid
  uid="$(id -u)"
  launchctl bootout "gui/${uid}" "$PLIST_PATH" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/${uid}" "$PLIST_PATH"
  launchctl enable "gui/${uid}/${LABEL}" >/dev/null 2>&1 || true
  launchctl kickstart -k "gui/${uid}/${LABEL}"
  echo "launchd installed: $LABEL"
}

cmd_uninstall_launchd() {
  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "uninstall-launchd only works on macOS" >&2
    exit 1
  fi
  local uid
  uid="$(id -u)"
  launchctl disable "gui/${uid}/${LABEL}" >/dev/null 2>&1 || true
  launchctl bootout "gui/${uid}" "$PLIST_PATH" >/dev/null 2>&1 || true
  rm -f "$PLIST_PATH"
  echo "launchd removed: $LABEL"
}

cmd_install_systemd() {
  ensure_state
  if [[ "$(uname -s)" != "Linux" ]]; then
    echo "install-systemd only works on Linux" >&2
    exit 1
  fi
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "install-systemd requires root" >&2
    exit 1
  fi

  local unit_path
  unit_path="/etc/systemd/system/${SYSTEMD_UNIT}"
  cat > "$unit_path" <<EOF
[Unit]
Description=Git Sync Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$(id -un)
Environment=GIT_SYNC_INTERVAL=${INTERVAL}
Environment=GIT_SYNC_REPO_FILE=${REPO_FILE}
Environment=GIT_SYNC_LOG_FILE=${LOG_FILE}
Environment=GIT_SYNC_GIT_TIMEOUT=${TIMEOUT_SECS}
ExecStart=/bin/bash ${DAEMON_SCRIPT}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable --now "$SYSTEMD_UNIT"
  echo "systemd installed: $SYSTEMD_UNIT"
}

cmd_uninstall_systemd() {
  if [[ "$(uname -s)" != "Linux" ]]; then
    echo "uninstall-systemd only works on Linux" >&2
    exit 1
  fi
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "uninstall-systemd requires root" >&2
    exit 1
  fi

  systemctl disable --now "$SYSTEMD_UNIT" >/dev/null 2>&1 || true
  rm -f "/etc/systemd/system/${SYSTEMD_UNIT}"
  systemctl daemon-reload
  echo "systemd removed: $SYSTEMD_UNIT"
}

cmd_status() {
  ensure_state
  echo "state_dir: $STATE_DIR"
  echo "repo_file: $REPO_FILE"
  echo "log_file: $LOG_FILE"
  echo "repos:"
  cmd_list_repos
  echo "-----"

  if [[ "$(uname -s)" == "Darwin" ]]; then
    local uid
    uid="$(id -u)"
    launchctl print "gui/${uid}/${LABEL}" 2>/dev/null | sed -n '1,90p' || echo "launchd job not loaded: ${LABEL}"
  elif [[ "$(uname -s)" == "Linux" ]]; then
    systemctl status "$SYSTEMD_UNIT" --no-pager --lines=20 2>/dev/null || echo "systemd unit not active: ${SYSTEMD_UNIT}"
  fi

  echo "----- log tail -----"
  tail -n 40 "$LOG_FILE" 2>/dev/null || true
}

command="${1:-}"
shift || true

case "$command" in
  init) cmd_init ;;
  add-repo) cmd_add_repo "$@" ;;
  remove-repo) cmd_remove_repo "$@" ;;
  list-repos) cmd_list_repos ;;
  run-once) cmd_run_once ;;
  install-launchd) cmd_install_launchd ;;
  uninstall-launchd) cmd_uninstall_launchd ;;
  install-systemd) cmd_install_systemd ;;
  uninstall-systemd) cmd_uninstall_systemd ;;
  status) cmd_status ;;
  *)
    usage
    exit 1
    ;;
esac
