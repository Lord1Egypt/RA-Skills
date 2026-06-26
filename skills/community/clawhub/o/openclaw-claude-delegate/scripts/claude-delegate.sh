#!/bin/bash
set -euo pipefail

SOURCE_PATH="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SOURCE_PATH="$(readlink -f "$SOURCE_PATH")"
fi
SCRIPT_DIR="$(cd "$(dirname "$SOURCE_PATH")" && pwd)"
SKILL_ROOT="${SCRIPT_DIR%/scripts}"
PROFILE_WRAPPER="$SCRIPT_DIR/cc-profile.sh"
ORCHESTRATOR="$SCRIPT_DIR/cc-orchestrator.sh"
RUN_TASK="$SCRIPT_DIR/run-task.sh"

default_runner_user=""
if [ "$(id -u)" = "0" ] && id ccbot >/dev/null 2>&1 && [ -d /home/ccbot ]; then
  default_runner_user="ccbot"
fi

export CLAUDE_RUNNER_USER="${CLAUDE_RUNNER_USER:-$default_runner_user}"
if [ -n "$CLAUDE_RUNNER_USER" ]; then
  export CLAUDE_RUNNER_HOME="${CLAUDE_RUNNER_HOME:-/home/$CLAUDE_RUNNER_USER}"
  export CLAUDE_BIN="${CLAUDE_BIN:-$CLAUDE_RUNNER_HOME/.local/bin/claude}"
else
  export CLAUDE_RUNNER_HOME="${CLAUDE_RUNNER_HOME:-$HOME}"
  export CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude 2>/dev/null || true)}"
fi
export CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-bypassPermissions}"
export CLAUDE_BACKEND="${CLAUDE_BACKEND:-cli}"
export CLAUDE_DELEGATE_PROFILES="${CLAUDE_DELEGATE_PROFILES:-$SKILL_ROOT/profiles.json}"
export CLAUDE_DELEGATE_BOOTSTRAP="${CLAUDE_DELEGATE_BOOTSTRAP:-1}"
export CLAUDE_DELEGATE_DOC_BASENAME="${CLAUDE_DELEGATE_DOC_BASENAME:-CLAUDE.delegate.md}"
default_oauth_env="$HOME/.claude/.oauth-token.env"
if [ "$(id -u)" = "0" ] && [ -f /root/.claude/.oauth-token.env ]; then
  default_oauth_env="/root/.claude/.oauth-token.env"
fi
export CLAUDE_OAUTH_ENV_FILE="${CLAUDE_OAUTH_ENV_FILE:-$default_oauth_env}"

if [ -f "$CLAUDE_OAUTH_ENV_FILE" ]; then
  # shellcheck disable=SC1090
  . "$CLAUDE_OAUTH_ENV_FILE"
fi

usage() {
  cat <<'EOF'
Usage:
  claude-delegate.sh dispatch <profile> <budget> <model> <label> "<task>" [cc-profile options]
  claude-delegate.sh poll <task-id>
  claude-delegate.sh result [--text|--raw] <task-id>
  claude-delegate.sh resume <task-id> <budget> "<follow-up>" [resume options]
  claude-delegate.sh list [--running|--done|--failed|--all]
  claude-delegate.sh cancel <task-id>
  claude-delegate.sh costs [--today|--all]
  claude-delegate.sh cleanup
  claude-delegate.sh doctor
  claude-delegate.sh profile <raw cc-profile args...>
  claude-delegate.sh orchestrator <raw cc-orchestrator args...>
  claude-delegate.sh run-task <raw run-task args...>
EOF
}

doctor() {
  local acpx_bin="${CLAUDE_RUNNER_HOME}/.local/share/clawd/vendor/acpx"
  local runner_env=(HOME="$CLAUDE_RUNNER_HOME")
  local -a runner_cmd root_cmd
  if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    runner_env+=(CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN")
  fi
  if [ -n "${CLAUDE_RUNNER_USER:-}" ]; then
    runner_cmd=(sudo -u "$CLAUDE_RUNNER_USER" -H env "${runner_env[@]}" "${CLAUDE_BIN:-claude}")
  else
    runner_cmd=(env "${runner_env[@]}" "${CLAUDE_BIN:-claude}")
  fi
  root_cmd=("${CLAUDE_BIN:-claude}")
  if [ -x /root/.local/bin/claude ]; then
    root_cmd=(/root/.local/bin/claude)
  elif command -v claude >/dev/null 2>&1; then
    root_cmd=(claude)
  fi
  cat <<EOF
runner_user=$CLAUDE_RUNNER_USER
runner_home=$CLAUDE_RUNNER_HOME
claude_bin=$CLAUDE_BIN
backend=$CLAUDE_BACKEND
permission_mode=$CLAUDE_PERMISSION_MODE
profiles_file=$CLAUDE_DELEGATE_PROFILES
acpx_cache_root=$acpx_bin
delegate_bootstrap=$CLAUDE_DELEGATE_BOOTSTRAP
delegate_doc_basename=$CLAUDE_DELEGATE_DOC_BASENAME
oauth_env_file=$CLAUDE_OAUTH_ENV_FILE
oauth_token_loaded=$( [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && echo yes || echo no )
EOF
  echo
  echo "[current/root claude auth status]"
  "${root_cmd[@]}" auth status || true
  echo
  echo "[runner claude auth status]"
  "${runner_cmd[@]}" auth status || true
  echo
  echo "[runner live probe]"
  timeout 30 "${runner_cmd[@]}" -p "Reply with exactly CLAUDE-DELEGATE-PROBE-OK" || true
}

cmd="${1:-}"
shift || true

case "$cmd" in
  dispatch)
    profile="${1:-}"
    [ -n "$profile" ] || { usage >&2; exit 1; }
    shift
    exec bash "$PROFILE_WRAPPER" "$profile" dispatch "$@"
    ;;
  poll|result|resume|list|cancel|costs|cleanup)
    exec bash "$ORCHESTRATOR" "$cmd" "$@"
    ;;
  doctor)
    doctor
    ;;
  profile)
    exec bash "$PROFILE_WRAPPER" "$@"
    ;;
  orchestrator)
    exec bash "$ORCHESTRATOR" "$@"
    ;;
  run-task)
    exec bash "$RUN_TASK" "$@"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 1
    ;;
esac
