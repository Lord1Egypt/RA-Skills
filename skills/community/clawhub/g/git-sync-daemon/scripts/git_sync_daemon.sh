#!/usr/bin/env bash
set -u

# Keep PATH resilient for daemon environments (launchd/systemd).
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"

INTERVAL="${GIT_SYNC_INTERVAL:-60}"
REPO_FILE="${GIT_SYNC_REPO_FILE:-$HOME/.config/git-sync-daemon/repos.conf}"
LOG_FILE="${GIT_SYNC_LOG_FILE:-$HOME/.config/git-sync-daemon/git-sync-daemon.log}"
DEFAULT_REMOTE="${GIT_SYNC_DEFAULT_REMOTE:-origin}"
GIT_TIMEOUT="${GIT_SYNC_GIT_TIMEOUT:-45}"
COMMIT_PREFIX="${GIT_SYNC_COMMIT_PREFIX:-chore(auto-sync)}"

ONCE=0
if [[ "${1:-}" == "--once" ]]; then
  ONCE=1
fi

mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"

ts() {
  date '+%Y-%m-%d %H:%M:%S %z'
}

log() {
  printf '[%s] %s\n' "$(ts)" "$*" >> "$LOG_FILE"
}

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

expand_home() {
  local p="$1"
  if [[ "$p" == "~" ]]; then
    printf '%s' "$HOME"
    return
  fi
  if [[ "$p" == "~/"* ]]; then
    printf '%s' "${HOME}/${p#~/}"
    return
  fi
  printf '%s' "$p"
}

run_git() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$GIT_TIMEOUT" git "$@"
    return
  fi
  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$GIT_TIMEOUT" git "$@"
    return
  fi
  git "$@"
}

parse_bool_enabled() {
  case "$1" in
    0|false|False|FALSE|no|No|NO|off|OFF) return 1 ;;
    *) return 0 ;;
  esac
}

sync_repo() {
  local repo="$1"
  local remote="$2"
  local branch="$3"
  local enabled="$4"

  if ! parse_bool_enabled "$enabled"; then
    log "INFO repo=${repo} skip: disabled"
    return 0
  fi

  repo="$(expand_home "$repo")"
  if [[ ! -d "$repo" ]]; then
    log "WARN repo=${repo} skip: path missing"
    return 0
  fi

  if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    log "WARN repo=${repo} skip: not a git repository"
    return 0
  fi

  local lock_id lock_dir
  lock_id="$(printf '%s' "$repo" | shasum -a 1 | awk '{print $1}')"
  lock_dir="/tmp/git-sync-daemon-${lock_id}.lock"
  if ! mkdir "$lock_dir" 2>/dev/null; then
    log "INFO repo=${repo} skip: lock busy"
    return 0
  fi

  (
    trap 'rmdir "$lock_dir" >/dev/null 2>&1 || true' EXIT
    cd "$repo" || {
      log "ERROR repo=${repo} cd failed"
      return 0
    }

    if [[ -n "$(git rev-parse --git-path MERGE_HEAD 2>/dev/null)" ]] && [[ -f "$(git rev-parse --git-path MERGE_HEAD 2>/dev/null)" ]]; then
      log "WARN repo=${repo} skip: merge in progress"
      return 0
    fi
    if [[ -d "$(git rev-parse --git-path rebase-merge 2>/dev/null)" ]] || [[ -d "$(git rev-parse --git-path rebase-apply 2>/dev/null)" ]]; then
      log "WARN repo=${repo} skip: rebase in progress"
      return 0
    fi

    if [[ -z "$branch" ]]; then
      branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
    fi
    if [[ -z "$branch" ]]; then
      log "WARN repo=${repo} skip: detached HEAD"
      return 0
    fi

    if [[ -f .git/hooks/pre-push ]] && grep -q "git-lfs" .git/hooks/pre-push 2>/dev/null; then
      if ! command -v git-lfs >/dev/null 2>&1; then
        log "ERROR repo=${repo} git-lfs required by pre-push hook but missing in PATH"
        return 0
      fi
    fi

    log "INFO repo=${repo} remote=${remote} branch=${branch} start"

    local dirty remote_ahead local_ahead upstream
    upstream="${remote}/${branch}"
    remote_ahead=0
    local_ahead=0
    dirty=0

    if git diff --quiet && git diff --cached --quiet && [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
      dirty=0
    else
      dirty=1
    fi

    if ! run_git fetch --prune "$remote" >> "$LOG_FILE" 2>&1; then
      log "ERROR repo=${repo} fetch failed"
      return 0
    fi

    if run_git show-ref --verify --quiet "refs/remotes/${upstream}"; then
      read -r remote_ahead local_ahead < <(run_git rev-list --left-right --count "${upstream}...HEAD" 2>/dev/null || printf '0 0\n')
    else
      local_ahead=1
    fi

    if [[ "$dirty" -eq 1 ]]; then
      run_git add -A >> "$LOG_FILE" 2>&1 || {
        log "ERROR repo=${repo} git add failed"
        return 0
      }
      if ! run_git diff --cached --quiet; then
        if run_git commit -m "${COMMIT_PREFIX}: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1; then
          log "INFO repo=${repo} committed local changes"
        else
          log "ERROR repo=${repo} commit failed"
          return 0
        fi
      fi
    fi

    if [[ "$remote_ahead" -gt 0 ]]; then
      if run_git pull --rebase --autostash "$remote" "$branch" >> "$LOG_FILE" 2>&1; then
        log "INFO repo=${repo} pull --rebase ok"
      else
        log "ERROR repo=${repo} pull --rebase failed"
        run_git rebase --abort >> "$LOG_FILE" 2>&1 || true
        return 0
      fi
    fi

    remote_ahead=0
    local_ahead=0
    if run_git show-ref --verify --quiet "refs/remotes/${upstream}"; then
      read -r remote_ahead local_ahead < <(run_git rev-list --left-right --count "${upstream}...HEAD" 2>/dev/null || printf '0 0\n')
    else
      local_ahead=1
    fi

    if [[ "$local_ahead" -gt 0 ]]; then
      if run_git push "$remote" "$branch" >> "$LOG_FILE" 2>&1; then
        log "INFO repo=${repo} push ok"
      else
        log "ERROR repo=${repo} push failed"
        return 0
      fi
    else
      log "INFO repo=${repo} no push needed"
    fi

    log "INFO repo=${repo} done"
  )
}

run_cycle() {
  if [[ ! -f "$REPO_FILE" ]]; then
    log "WARN repo file missing: $REPO_FILE"
    return 0
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    local clean repo remote branch enabled token key val
    clean="$(trim "${line%%#*}")"
    [[ -z "$clean" ]] && continue

    repo=""
    remote="$DEFAULT_REMOTE"
    branch=""
    enabled="1"

    IFS='|' read -r -a parts <<< "$clean"
    repo="$(trim "${parts[0]}")"
    for ((i=1; i<${#parts[@]}; i++)); do
      token="$(trim "${parts[$i]}")"
      [[ -z "$token" ]] && continue
      key="${token%%=*}"
      val="${token#*=}"
      key="$(trim "$key")"
      val="$(trim "$val")"
      case "$key" in
        remote) remote="$val" ;;
        branch) branch="$val" ;;
        enabled) enabled="$val" ;;
      esac
    done

    if [[ -n "$repo" ]]; then
      sync_repo "$repo" "$remote" "$branch" "$enabled"
    fi
  done < "$REPO_FILE"
}

log "INFO daemon start interval=${INTERVAL}s repo_file=${REPO_FILE} log_file=${LOG_FILE}"

if [[ "$ONCE" -eq 1 ]]; then
  run_cycle
  log "INFO daemon exit once-mode"
  exit 0
fi

while true; do
  run_cycle
  sleep "$INTERVAL"
done
