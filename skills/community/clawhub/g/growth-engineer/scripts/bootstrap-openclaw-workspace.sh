#!/usr/bin/env bash
# Copy growth-engineer runtime from an installed skill into the active workspace root
# so `node scripts/openclaw-growth-start.mjs` works (paths match docs + agent runs).
#
# Typical layout after installing a bundled growth runtime skill:
#   <workspace>/skills/<skill-slug>/scripts/*.mjs
# Hermes normally installs into ~/.hermes/skills/<skill-slug>/, so the target
# workspace is the current working directory unless OPENCLAW_GROWTH_WORKSPACE is set.
# This script creates:
#   <workspace>/scripts/*.mjs
#   <workspace>/data/openclaw-growth-engineer/*.json
#
# Idempotent. Safe to re-run after skill updates.
set -euo pipefail

run_after=""
declare -a wizard_args=()
declare -a start_args=()
wizard_has_mode=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --wizard|wizard)
      run_after="wizard"
      shift
      ;;
    --connectors|--connector-setup|--recover-connectors|--restore-connectors|--connector-recovery)
      run_after="wizard"
      wizard_has_mode=1
      wizard_args+=("$1")
      shift
      if [[ $# -gt 0 && "$1" != --* ]]; then
        wizard_args+=("$1")
        shift
      fi
      ;;
    --start|start)
      run_after="start"
      shift
      ;;
    --config)
      if [[ $# -lt 2 ]]; then
        echo "bootstrap-openclaw-workspace.sh: --config requires a path" >&2
        exit 1
      fi
      OPENCLAW_GROWTH_CONFIG_PATH="$2"
      export OPENCLAW_GROWTH_CONFIG_PATH
      wizard_args+=("--config" "$2")
      start_args+=("--config" "$2")
      shift 2
      ;;
    --no-run|--no-wizard)
      run_after=""
      shift
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        wizard_args+=("$1")
        shift
      done
      ;;
    *)
      wizard_args+=("$1")
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

skill_slug="$(basename "${SKILL_ROOT}")"
if [[ "${skill_slug}" != "growth-engineer" && "${skill_slug}" != "product-manager-skill" && "${skill_slug}" != "ai-product-manager" && "${skill_slug}" != "openclaw-growth-engineer" ]]; then
  echo "bootstrap-openclaw-workspace.sh: expected to live under skills/growth-engineer/scripts/, skills/openclaw-growth-engineer/scripts/, or a legacy ai-product-manager/product-manager-skill alias (ClawHub install)." >&2
  echo "In the Agentic Analytics monorepo, scripts already live at repo root; nothing to copy." >&2
  exit 0
fi

if [[ -n "${OPENCLAW_GROWTH_WORKSPACE:-}" ]]; then
  WORKSPACE="$(cd "${OPENCLAW_GROWTH_WORKSPACE}" && pwd)"
elif [[ -n "${HOME:-}" && "${SKILL_ROOT}" == "${HOME}/.hermes/skills/"* ]]; then
  WORKSPACE="$(pwd)"
else
  WORKSPACE="$(cd "${SKILL_ROOT}/../.." && pwd)"
fi

if [[ ( "${skill_slug}" == "growth-engineer" || "${skill_slug}" == "openclaw-growth-engineer" ) && -f "${SKILL_ROOT}/.clawhub/origin.json" && "${OPENCLAW_GROWTH_DISABLE_SELF_UPDATE:-}" != "1" && "${OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE:-}" != "1" ]]; then
  if command -v clawhub >/dev/null 2>&1; then
    (cd "${WORKSPACE}" && clawhub --no-input --dir skills update "${skill_slug}" --force) || true
  elif command -v npx >/dev/null 2>&1; then
    (cd "${WORKSPACE}" && npx -y clawhub --no-input --dir skills update "${skill_slug}" --force) || true
  fi
fi

if [[ "${OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE:-}" != "1" ]]; then
  if ! command -v analyticscli >/dev/null 2>&1 || ! analyticscli feedback summary --help >/dev/null 2>&1; then
    if [[ -x "${SCRIPT_DIR}/install-analyticscli-cli.sh" ]]; then
      echo "Ensuring AnalyticsCLI CLI supports feedback summaries..." >&2
      bash "${SCRIPT_DIR}/install-analyticscli-cli.sh" || {
        echo "AnalyticsCLI CLI update failed; continuing bootstrap, but feedback summary source may stay unavailable." >&2
      }
    fi
  fi
fi

mkdir -p "${WORKSPACE}/scripts" "${WORKSPACE}/data/openclaw-growth-engineer"

shopt -s nullglob
for f in "${SCRIPT_DIR}/"*.mjs "${SCRIPT_DIR}/"*.py; do
  base="$(basename "$f")"
  if [[ "${base}" == "bootstrap-openclaw-workspace.sh" ]]; then
    continue
  fi
  cp "${f}" "${WORKSPACE}/scripts/${base}"
done

for f in "${SKILL_ROOT}/data/openclaw-growth-engineer/"*.json; do
  cp "${f}" "${WORKSPACE}/data/openclaw-growth-engineer/$(basename "${f}")"
done

heartbeat_path="${WORKSPACE}/HEARTBEAT.md"
heartbeat_config_path="data/openclaw-growth-engineer/config.json"
if [[ -n "${OPENCLAW_GROWTH_CONFIG_PATH:-}" ]]; then
  heartbeat_config_path="${OPENCLAW_GROWTH_CONFIG_PATH}"
elif [[ -n "${HOME:-}" && -f "${HOME}/data/openclaw-growth-engineer/config.json" && -f "${HOME}/data/openclaw-growth-engineer/state.json" ]]; then
  heartbeat_config_path="${HOME}/data/openclaw-growth-engineer/config.json"
elif [[ ! -f "${WORKSPACE}/data/openclaw-growth-engineer/config.json" && -n "${HOME:-}" && -f "${HOME}/data/openclaw-growth-engineer/config.json" ]]; then
  heartbeat_config_path="${HOME}/data/openclaw-growth-engineer/config.json"
fi
heartbeat_state_path="${OPENCLAW_GROWTH_STATE_PATH:-$(dirname "${heartbeat_config_path}")/state.json}"
heartbeat_block="$(cat <<'EOF'
<!-- openclaw-growth-engineer:start -->
tasks:

- name: openclaw-growth-engineer-run
  interval: 6h
  prompt: "Run `node scripts/openclaw-growth-runner.mjs --config __OPENCLAW_GROWTH_CONFIG_PATH__ --state __OPENCLAW_GROWTH_STATE_PATH__` from the workspace if the config and runtime files exist. The runner owns schedule.cadences, connectorHealthCheckIntervalMinutes, skipIfNoDataChange, and skipIfIssueSetUnchanged. ASC/App Store Connect is a Growth Engineer local CLI connector, not a chat tool. If asked whether ASC analytics access is available, never inspect loaded chat/MCP tools and never answer no because no Apple tool is callable. Answer from `node scripts/openclaw-growth-status.mjs --config __OPENCLAW_GROWTH_CONFIG_PATH__ --json --only-connectors asc` or the latest connector setup result. If ASC reports connected/pass/healthy, or setup just finished successfully, answer exactly: Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup. If it reports connector-health alerts, production crashes, generated issues, or actionable growth findings, summarize only the action and evidence. If setup files are missing, tell the user to run `npx -y @analyticscli/growth-engineer wizard --connectors --config __OPENCLAW_GROWTH_CONFIG_PATH__`. If there is no actionable output, reply HEARTBEAT_OK."

# Keep this section small. Do not put secrets in HEARTBEAT.md.
<!-- openclaw-growth-engineer:end -->
EOF
)"
heartbeat_block="${heartbeat_block//__OPENCLAW_GROWTH_CONFIG_PATH__/${heartbeat_config_path}}"
heartbeat_block="${heartbeat_block//__OPENCLAW_GROWTH_STATE_PATH__/${heartbeat_state_path}}"

HEARTBEAT_PATH="${heartbeat_path}" HEARTBEAT_BLOCK="${heartbeat_block}" node <<'NODE'
const fs = require('node:fs');

const path = process.env.HEARTBEAT_PATH;
const block = process.env.HEARTBEAT_BLOCK;
const markerPattern = /<!-- openclaw-growth-engineer:start -->[\s\S]*?<!-- openclaw-growth-engineer:end -->/;

let existing = '';
try {
  existing = fs.readFileSync(path, 'utf8');
} catch {
  existing = '';
}

const hasWork = existing
  .split(/\r?\n/)
  .map((line) => line.trim())
  .some((line) => line && !line.startsWith('#') && !line.startsWith('<!--') && !line.startsWith('-->'));

const next = markerPattern.test(existing)
  ? existing.replace(markerPattern, block)
  : hasWork
    ? `${existing.trimEnd()}\n\n${block}\n`
    : `# OpenClaw heartbeat checklist\n\n${block}\n`;

if (next !== existing) {
  fs.writeFileSync(path, next, 'utf8');
}
NODE

echo "Copied ${skill_slug} runtime into workspace:"
echo "  ${WORKSPACE}/scripts"
echo "  ${WORKSPACE}/data/openclaw-growth-engineer"
echo "  ${WORKSPACE}/HEARTBEAT.md"

if [[ "${run_after}" == "wizard" ]]; then
  if [[ "${wizard_has_mode}" == "0" ]]; then
    wizard_args=("--connectors" "${wizard_args[@]}")
  fi
  if [[ " ${wizard_args[*]} " != *" --config "* ]]; then
    wizard_args+=("--config" "${heartbeat_config_path}")
  fi
  echo "Starting Growth Engineer wizard..."
  cd "${WORKSPACE}"
  exec node scripts/openclaw-growth-wizard.mjs "${wizard_args[@]}"
elif [[ "${run_after}" == "start" ]]; then
  if [[ " ${start_args[*]} " != *" --config "* ]]; then
    start_args+=("--config" "${heartbeat_config_path}")
  fi
  echo "Starting Growth Engineer..."
  cd "${WORKSPACE}"
  exec node scripts/openclaw-growth-start.mjs "${start_args[@]}"
else
  echo "Next:"
  echo "  cd ${WORKSPACE} && npx -y @analyticscli/growth-engineer wizard --connectors --config ${heartbeat_config_path}"
fi
