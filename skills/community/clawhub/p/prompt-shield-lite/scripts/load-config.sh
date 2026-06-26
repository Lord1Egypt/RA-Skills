#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Preserve caller-provided env (runtime override should win over files)
OVR_PSL_ROOT_DIR="${PSL_ROOT_DIR-}"
OVR_PSL_RULES_DIR="${PSL_RULES_DIR-}"
OVR_PSL_LOG_PATH="${PSL_LOG_PATH-}"
OVR_PSL_RL_STATE_PATH="${PSL_RL_STATE_PATH-}"
OVR_PSL_MODE="${PSL_MODE-}"
OVR_PSL_RL_MAX_REQ="${PSL_RL_MAX_REQ-}"
OVR_PSL_RL_WINDOW_SEC="${PSL_RL_WINDOW_SEC-}"
OVR_PSL_RL_ACTION="${PSL_RL_ACTION-}"
OVR_PSL_ALLOW_ANY_LOG_PATH="${PSL_ALLOW_ANY_LOG_PATH-}"

# Load only .env (local/private runtime config)
# .env.example is template-only and must NOT be sourced at runtime.
if [[ -f "$SKILL_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$SKILL_ROOT/.env"
  set +a
fi

# Re-apply runtime overrides
[[ -n "${OVR_PSL_ROOT_DIR}" ]] && PSL_ROOT_DIR="$OVR_PSL_ROOT_DIR"
[[ -n "${OVR_PSL_RULES_DIR}" ]] && PSL_RULES_DIR="$OVR_PSL_RULES_DIR"
[[ -n "${OVR_PSL_LOG_PATH}" ]] && PSL_LOG_PATH="$OVR_PSL_LOG_PATH"
[[ -n "${OVR_PSL_RL_STATE_PATH}" ]] && PSL_RL_STATE_PATH="$OVR_PSL_RL_STATE_PATH"
[[ -n "${OVR_PSL_MODE}" ]] && PSL_MODE="$OVR_PSL_MODE"
[[ -n "${OVR_PSL_RL_MAX_REQ}" ]] && PSL_RL_MAX_REQ="$OVR_PSL_RL_MAX_REQ"
[[ -n "${OVR_PSL_RL_WINDOW_SEC}" ]] && PSL_RL_WINDOW_SEC="$OVR_PSL_RL_WINDOW_SEC"
[[ -n "${OVR_PSL_RL_ACTION}" ]] && PSL_RL_ACTION="$OVR_PSL_RL_ACTION"
[[ -n "${OVR_PSL_ALLOW_ANY_LOG_PATH}" ]] && PSL_ALLOW_ANY_LOG_PATH="$OVR_PSL_ALLOW_ANY_LOG_PATH"

# Computed defaults (can all be overridden in .env / runtime env).
# Path defaults still fall back to skill-local root when not configured.
: "${PSL_ROOT_DIR:=$SKILL_ROOT}"
: "${PSL_RULES_DIR:=$PSL_ROOT_DIR/rules}"
: "${PSL_LOG_PATH:=$PSL_ROOT_DIR/memory/security-log.jsonl}"
: "${PSL_RL_STATE_PATH:=$PSL_ROOT_DIR/memory/psl-rate-limit.json}"
: "${PSL_MODE:=balanced}"
: "${PSL_RL_MAX_REQ:=30}"
: "${PSL_RL_WINDOW_SEC:=60}"
: "${PSL_RL_ACTION:=block}"
: "${PSL_ALLOW_ANY_LOG_PATH:=0}"

export PSL_ROOT_DIR PSL_RULES_DIR PSL_LOG_PATH PSL_RL_STATE_PATH
export PSL_MODE PSL_RL_MAX_REQ PSL_RL_WINDOW_SEC PSL_RL_ACTION
export PSL_ALLOW_ANY_LOG_PATH
