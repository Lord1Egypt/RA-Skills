#!/usr/bin/env bash
# _lib.sh
# Shared helpers for post-update-maintenance.
# Sourced by the other scripts. Never executed directly.
#
# Provides:
#   pum_profile_dir <profile>          -> echo profile state dir (creates if missing)
#   pum_state_dir <profile>            -> echo .../post-update-maintenance/ (creates subdirs)
#   pum_resolve_awareness              -> echo absolute path to awareness scripts dir, or empty
#   pum_require_awareness              -> exit 2 BLOCKED missing-dep if awareness missing
#   pum_current_gateway_version        -> echo gateway version string
#   pum_gateway_healthy <profile>      -> exit 0 if Runtime: running, else 1
#   pum_wait_healthy <profile> <secs>  -> poll up to N seconds for healthy gateway
#   pum_backup_config <profile>        -> echo backup path on success
#   pum_restore_config <profile> <bkp> -> restore + restart + wait healthy
#   pum_log <profile> <message>        -> append timestamped line to maintenance.log
#   pum_run_id                         -> echo epoch-based run id (cached per-run)

# Guard against double-source.
if [ "${_PUM_LIB_LOADED:-}" = "1" ]; then
  return 0 2>/dev/null || exit 0
fi
_PUM_LIB_LOADED=1

set -uo pipefail

# ---- paths ----------------------------------------------------------------

pum_profile_dir() {
  local profile="$1"
  if [ -n "${OPENCLAW_PROFILE_DIR:-}" ]; then
    echo "$OPENCLAW_PROFILE_DIR"
    return 0
  fi
  if [ -n "$profile" ] && [ -d "$HOME/.openclaw-$profile" ]; then
    echo "$HOME/.openclaw-$profile"
    return 0
  fi
  echo "$HOME/.openclaw"
}

pum_state_dir() {
  local profile="$1"
  local base
  base="$(pum_profile_dir "$profile")/post-update-maintenance"
  mkdir -p "$base/backups" "$base/snapshots" "$base/runs"
  echo "$base"
}

# ---- awareness bridge -----------------------------------------------------

pum_resolve_awareness() {
  # Try every plausible install location for resolve.sh.
  local candidates=(
    "${OPENCLAW_PROFILE_DIR:-/dev/null}/skills/post-update-awareness/scripts/resolve.sh"
    "$HOME/.openclaw-${OPENCLAW_PROFILE:-default}/skills/post-update-awareness/scripts/resolve.sh"
    "$HOME/.openclaw/skills/post-update-awareness/scripts/resolve.sh"
    "$HOME/openclaw-soul/skills/post-update-awareness/scripts/resolve.sh"
    "$HOME/clawhub-skills/post-update-awareness/scripts/resolve.sh"
  )
  for r in "${candidates[@]}"; do
    if [ -r "$r" ]; then
      # shellcheck disable=SC1090
      source "$r" 2>/dev/null || continue
      local out
      if out=$(resolve_pua_scripts 2>/dev/null) && [ -n "$out" ]; then
        echo "$out"
        return 0
      fi
    fi
  done
  return 1
}

pum_require_awareness() {
  if ! pum_resolve_awareness >/dev/null 2>&1; then
    echo "BLOCKED missing-dep: post-update-awareness (install with: clawhub install post-update-awareness)" >&2
    exit 2
  fi
}

# ---- gateway helpers ------------------------------------------------------

pum_current_gateway_version() {
  openclaw -V 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\.[0-9]+\.[0-9]+/) {print $i; exit}}'
}

pum_gateway_healthy() {
  local profile="$1"
  openclaw --profile "$profile" gateway status 2>&1 \
    | grep -E "Runtime: running" >/dev/null
}

pum_wait_healthy() {
  local profile="$1"
  local secs="${2:-60}"
  local elapsed=0
  while [ "$elapsed" -lt "$secs" ]; do
    if pum_gateway_healthy "$profile"; then
      return 0
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done
  return 1
}

# ---- backup / restore -----------------------------------------------------

pum_config_path() {
  local profile="$1"
  echo "$(pum_profile_dir "$profile")/openclaw.json"
}

pum_backup_config() {
  local profile="$1"
  local cfg
  cfg="$(pum_config_path "$profile")"
  if [ ! -r "$cfg" ]; then
    echo "BLOCKED config-unreadable: $cfg" >&2
    return 2
  fi
  local state
  state="$(pum_state_dir "$profile")"
  local epoch
  epoch="$(date +%s)"
  local backup="$state/backups/openclaw.json.$epoch"
  cp "$cfg" "$backup"
  echo "$backup"
}

pum_restore_config() {
  local profile="$1"
  local backup="$2"
  local cfg
  cfg="$(pum_config_path "$profile")"
  if [ ! -r "$backup" ]; then
    echo "RESTORE failed: backup not readable ($backup)" >&2
    return 3
  fi
  cp "$backup" "$cfg"
  openclaw --profile "$profile" gateway restart >/dev/null 2>&1 || true
  if pum_wait_healthy "$profile" 60; then
    return 0
  fi
  return 4
}

# ---- logging --------------------------------------------------------------

pum_run_id() {
  if [ -z "${_PUM_RUN_ID:-}" ]; then
    _PUM_RUN_ID="$(date +%Y%m%dT%H%M%S)-$$"
  fi
  echo "$_PUM_RUN_ID"
}

pum_log() {
  local profile="$1"
  local msg="$2"
  local state
  state="$(pum_state_dir "$profile")"
  local run
  run="$(pum_run_id)"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $msg" >> "$state/runs/$run.log"
}
