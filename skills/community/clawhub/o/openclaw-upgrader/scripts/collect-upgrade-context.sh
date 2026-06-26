#!/usr/bin/env bash
set -euo pipefail

TARGET_VERSION="${1:-latest}"
OUT_JSON="${2:-}"

LOCK_DIR="${OPENCLAW_UPGRADER_LOCK_DIR:-$HOME/.openclaw/openclaw-upgrader.lock}"
LOCK_INFO_FILE="$LOCK_DIR/run.json"
RUN_ID="${OPENCLAW_UPGRADER_RUN_ID:-$(date +%Y%m%d-%H%M%S)-$$}"
LOCK_ACQUIRED=false

if [[ -z "$OUT_JSON" ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  OUT_JSON="$HOME/.openclaw/upgrade-context-$TS.json"
fi

cleanup_lock() {
  if [[ "$LOCK_ACQUIRED" == true && ! -f "$LOCK_INFO_FILE" ]]; then
    rmdir "$LOCK_DIR" >/dev/null 2>&1 || true
  fi
}
trap cleanup_lock EXIT

trim() {
  awk '{$1=$1;print}'
}

json_escape() {
  python3 - <<'PY' "$1"
import json,sys
print(json.dumps(sys.argv[1]))
PY
}

join_semicolon() {
  tr '\n' ';' | sed 's/;*$//'
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

first_match() {
  local pattern="$1"
  if have_cmd rg; then
    rg "$pattern" -N 2>/dev/null | head -n1 || true
  else
    grep -E "$pattern" 2>/dev/null | head -n1 || true
  fi
}

any_match_q() {
  local pattern="$1"
  if have_cmd rg; then
    rg -q "$pattern" 2>/dev/null
  else
    grep -Eq "$pattern" 2>/dev/null
  fi
}

extract_version() {
  first_match '[0-9]{4}\.[0-9]+\.[0-9]+' | sed -E 's/.*([0-9]{4}\.[0-9]+\.[0-9]+).*/\1/' | head -n1 || true
}

write_reentry_result() {
  local existing_lock_info="{}"
  if [[ -f "$LOCK_INFO_FILE" ]]; then
    existing_lock_info="$(cat "$LOCK_INFO_FILE" 2>/dev/null || printf '{}')"
  fi

  cat > "$OUT_JSON" <<JSON
{
  "target_version": $(json_escape "$TARGET_VERSION"),
  "run_id": $(json_escape "$RUN_ID"),
  "current_version": "unknown",
  "platform": "unknown",
  "config_path": "unknown",
  "state_dir": "unknown",
  "profile": "unknown",
  "install_method_hints": "unknown",
  "selected_agent": "none",
  "delegation_status": "rejected_reentry",
  "delegation_block_reason": "active_run_exists",
  "agent_checks": {
    "codex": {
      "installed": false,
      "authenticated": false,
      "preflight_ok": false
    },
    "claude_code": {
      "installed": false,
      "authenticated": false,
      "preflight_ok": false
    }
  },
  "service_model": "unknown",
  "service_identity": "unknown",
  "known_endpoint": "unknown",
  "auth_mode": "unknown",
  "auth_source": "unknown",
  "run_lock_path": $(json_escape "$LOCK_DIR"),
  "active_run": $existing_lock_info
}
JSON

  printf '%s\n' "$OUT_JSON"
}

mkdir -p "$(dirname "$OUT_JSON")"
mkdir -p "$(dirname "$LOCK_DIR")"

if mkdir "$LOCK_DIR" 2>/dev/null; then
  LOCK_ACQUIRED=true
  cat > "$LOCK_INFO_FILE" <<JSON
{
  "run_id": $(json_escape "$RUN_ID"),
  "pid": $$,
  "started_at": $(json_escape "$(date -u +%Y-%m-%dT%H:%M:%SZ)"),
  "target_version": $(json_escape "$TARGET_VERSION"),
  "holder": "collect-upgrade-context.sh"
}
JSON
else
  write_reentry_result
  exit 0
fi

CURRENT_VERSION="unknown"
if have_cmd openclaw; then
  CURRENT_VERSION="$(openclaw --version 2>/dev/null | extract_version | trim || true)"
  [[ -z "$CURRENT_VERSION" ]] && CURRENT_VERSION="unknown"
fi

OS_NAME="$(uname -s 2>/dev/null || echo unknown)"
ARCH="$(uname -m 2>/dev/null || echo unknown)"
PLATFORM="$OS_NAME/$ARCH"

CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-${CLAWDBOT_CONFIG_PATH:-${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}}}"
STATE_DIR="${OPENCLAW_STATE_DIR:-unknown}"
PROFILE="${OPENCLAW_PROFILE:-unknown}"

INSTALL_METHOD_HINTS=()
have_cmd npm && INSTALL_METHOD_HINTS+=("npm")
have_cmd pnpm && INSTALL_METHOD_HINTS+=("pnpm")
have_cmd yarn && INSTALL_METHOD_HINTS+=("yarn")
if [[ ${#INSTALL_METHOD_HINTS[@]} -eq 0 ]]; then
  INSTALL_METHOD_HINTS+=("unknown")
fi
INSTALL_HINTS_CSV="$(IFS=,; echo "${INSTALL_METHOD_HINTS[*]}")"

STATUS_TXT=""
if have_cmd openclaw; then
  STATUS_TXT="$(openclaw status 2>/dev/null || true)"
fi

SERVICE_MODEL="unknown"
SERVICE_IDENTITY="unknown"

if [[ -n "$STATUS_TXT" ]]; then
  if printf '%s\n' "$STATUS_TXT" | any_match_q 'LaunchAgent'; then
    SERVICE_MODEL="launchctl"
  elif printf '%s\n' "$STATUS_TXT" | any_match_q 'systemd|systemctl'; then
    SERVICE_MODEL="systemd"
  fi
fi

if [[ "$SERVICE_MODEL" == "unknown" ]]; then
  if [[ "$OS_NAME" == "Darwin" ]] && launchctl list >/dev/null 2>&1; then
    if launchctl list 2>/dev/null | any_match_q 'openclaw'; then
      SERVICE_MODEL="launchctl"
    fi
  elif have_cmd systemctl; then
    if systemctl list-units --type=service --all 2>/dev/null | any_match_q 'openclaw'; then
      SERVICE_MODEL="systemd"
    fi
  fi
fi

if [[ "$SERVICE_MODEL" == "launchctl" ]]; then
  UID_NOW="$(id -u 2>/dev/null || echo '')"
  if [[ -n "$UID_NOW" ]]; then
    if launchctl print "gui/$UID_NOW/ai.openclaw.gateway" >/dev/null 2>&1; then
      SERVICE_IDENTITY="ai.openclaw.gateway"
    fi
  fi
  if [[ -z "$SERVICE_IDENTITY" || "$SERVICE_IDENTITY" == "unknown" ]]; then
    SERVICE_IDENTITY="$(launchctl list 2>/dev/null | (first_match 'openclaw' || true) | join_semicolon || true)"
  fi
elif [[ "$SERVICE_MODEL" == "systemd" ]]; then
  SERVICE_IDENTITY="$(systemctl list-units --type=service --all 2>/dev/null | (first_match 'openclaw' || true) | join_semicolon || true)"
fi

if [[ -z "$SERVICE_IDENTITY" || "$SERVICE_IDENTITY" == "unknown" ]]; then
  PROC_MATCH="$(ps aux 2>/dev/null | (first_match 'openclaw(-gateway)?' || true) | join_semicolon || true)"
  if [[ -n "$PROC_MATCH" ]]; then
    SERVICE_IDENTITY="$PROC_MATCH"
    [[ "$SERVICE_MODEL" == "unknown" ]] && SERVICE_MODEL="manual"
  else
    SERVICE_IDENTITY="unknown"
  fi
fi

KNOWN_ENDPOINT="unknown"
AUTH_MODE="unknown"
AUTH_SOURCE="unknown"
if [[ -n "$STATUS_TXT" ]]; then
  ENDPOINT_LINE="$(printf '%s\n' "$STATUS_TXT" | first_match 'Gateway[[:space:]]' || true)"
  if [[ -n "$ENDPOINT_LINE" ]]; then
    KNOWN_ENDPOINT="$(printf '%s' "$ENDPOINT_LINE" | sed -nE 's/.*((ws|wss|http|https):\/\/[^ ]+).*/\1/p' | head -n1 || true)"
    [[ -z "$KNOWN_ENDPOINT" ]] && KNOWN_ENDPOINT="unknown"
    if printf '%s' "$ENDPOINT_LINE" | any_match_q 'auth token\+password|token\+password'; then
      AUTH_MODE="token+password"
      AUTH_SOURCE="openclaw status"
    elif printf '%s' "$ENDPOINT_LINE" | any_match_q 'auth token|token'; then
      AUTH_MODE="token"
      AUTH_SOURCE="openclaw status"
    elif printf '%s' "$ENDPOINT_LINE" | any_match_q 'password'; then
      AUTH_MODE="password"
      AUTH_SOURCE="openclaw status"
    fi
  fi
fi

probe_codex() {
  local installed=false
  local authenticated=false
  local preflight_ok=false

  if have_cmd codex; then
    installed=true
    if codex login status >/dev/null 2>&1; then
      authenticated=true
    fi
    if [[ "$authenticated" == true ]]; then
      local tmp_out tmp_err
      tmp_out="$(mktemp)" || { printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"; return; }
      tmp_err="$(mktemp)" || { rm -f "$tmp_out"; printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"; return; }
      if codex exec --skip-git-repo-check "reply exactly: ok" >"$tmp_out" 2>"$tmp_err"; then
        if grep -q '^ok$' "$tmp_out" 2>/dev/null; then
          preflight_ok=true
        fi
      fi
      rm -f "$tmp_out" "$tmp_err"
    fi
  fi

  printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"
}

probe_claude() {
  local installed=false
  local authenticated=false
  local preflight_ok=false

  if have_cmd claude; then
    installed=true
    if claude auth status >/dev/null 2>&1; then
      authenticated=true
    fi
    if [[ "$authenticated" == true ]]; then
      local tmp_out tmp_err
      tmp_out="$(mktemp)" || { printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"; return; }
      tmp_err="$(mktemp)" || { rm -f "$tmp_out"; printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"; return; }
      if claude -p "reply exactly: ok" >"$tmp_out" 2>"$tmp_err"; then
        if grep -q '^ok$' "$tmp_out" 2>/dev/null; then
          preflight_ok=true
        fi
      fi
      rm -f "$tmp_out" "$tmp_err"
    fi
  fi

  printf '%s;%s;%s\n' "$installed" "$authenticated" "$preflight_ok"
}

IFS=';' read -r CODEX_INSTALLED CODEX_AUTHENTICATED CODEX_PREFLIGHT_OK < <(probe_codex)
IFS=';' read -r CLAUDE_INSTALLED CLAUDE_AUTHENTICATED CLAUDE_PREFLIGHT_OK < <(probe_claude)

SELECTED_AGENT="none"
DELEGATION_STATUS="blocked"
DELEGATION_BLOCK_REASON="not_installed"

if [[ "$CODEX_INSTALLED" == true && "$CODEX_AUTHENTICATED" == true && "$CODEX_PREFLIGHT_OK" == true ]]; then
  SELECTED_AGENT="codex"
  DELEGATION_STATUS="started"
  DELEGATION_BLOCK_REASON="null"
elif [[ "$CLAUDE_INSTALLED" == true && "$CLAUDE_AUTHENTICATED" == true && "$CLAUDE_PREFLIGHT_OK" == true ]]; then
  SELECTED_AGENT="claude-code"
  DELEGATION_STATUS="started"
  DELEGATION_BLOCK_REASON="null"
else
  if [[ "$CODEX_INSTALLED" == false && "$CLAUDE_INSTALLED" == false ]]; then
    DELEGATION_BLOCK_REASON="not_installed"
  elif [[ ( "$CODEX_INSTALLED" == true && "$CODEX_AUTHENTICATED" == true && "$CODEX_PREFLIGHT_OK" == false ) || ( "$CLAUDE_INSTALLED" == true && "$CLAUDE_AUTHENTICATED" == true && "$CLAUDE_PREFLIGHT_OK" == false ) ]]; then
    DELEGATION_BLOCK_REASON="insufficient_capability"
  elif [[ ( "$CODEX_INSTALLED" == true && "$CODEX_AUTHENTICATED" == false ) || ( "$CLAUDE_INSTALLED" == true && "$CLAUDE_AUTHENTICATED" == false ) ]]; then
    DELEGATION_BLOCK_REASON="not_authenticated"
  else
    DELEGATION_BLOCK_REASON="unknown"
  fi
fi

cat > "$OUT_JSON" <<JSON
{
  "target_version": $(json_escape "$TARGET_VERSION"),
  "run_id": $(json_escape "$RUN_ID"),
  "current_version": $(json_escape "$CURRENT_VERSION"),
  "platform": $(json_escape "$PLATFORM"),
  "config_path": $(json_escape "$CONFIG_PATH"),
  "state_dir": $(json_escape "$STATE_DIR"),
  "profile": $(json_escape "$PROFILE"),
  "install_method_hints": $(json_escape "$INSTALL_HINTS_CSV"),
  "selected_agent": $(json_escape "$SELECTED_AGENT"),
  "delegation_status": $(json_escape "$DELEGATION_STATUS"),
  "delegation_block_reason": $(json_escape "$DELEGATION_BLOCK_REASON"),
  "agent_checks": {
    "codex": {
      "installed": $CODEX_INSTALLED,
      "authenticated": $CODEX_AUTHENTICATED,
      "preflight_ok": $CODEX_PREFLIGHT_OK
    },
    "claude_code": {
      "installed": $CLAUDE_INSTALLED,
      "authenticated": $CLAUDE_AUTHENTICATED,
      "preflight_ok": $CLAUDE_PREFLIGHT_OK
    }
  },
  "service_model": $(json_escape "$SERVICE_MODEL"),
  "service_identity": $(json_escape "$SERVICE_IDENTITY"),
  "known_endpoint": $(json_escape "$KNOWN_ENDPOINT"),
  "auth_mode": $(json_escape "$AUTH_MODE"),
  "auth_source": $(json_escape "$AUTH_SOURCE"),
  "run_lock_path": $(json_escape "$LOCK_DIR")
}
JSON

printf '%s\n' "$OUT_JSON"
