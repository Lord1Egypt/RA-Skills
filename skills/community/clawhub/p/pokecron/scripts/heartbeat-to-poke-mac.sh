#!/usr/bin/env bash
set -euo pipefail

# heartbeat-to-poke-mac.sh — macOS entry point for the heartbeat porting
# helper. Picks the right default openclaw.json location for macOS
# (~/Library/Application Support/openclaw/openclaw.json), then delegates to
# the cross-platform heartbeat-to-poke.sh next to it.
#
# Run only if you want to move off the native polling heartbeat. Use --apply
# to also disable the native heartbeat in openclaw.json (non-destructive
# default; off unless you opt in). Same flags as the Linux script:
#
#   --openclaw-config PATH | --heartbeat-md PATH | --heartbeat-state PATH
#   --agent AG | --channel CH | --target TGT
#   --active-hours (default) | --quiet-hours
#   --apply
#
# See `heartbeat-to-poke.sh --help` for the canonical list.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "heartbeat-to-poke-mac.sh: not running on macOS — use heartbeat-to-poke.sh instead." >&2
  exit 1
fi

# macOS default openclaw.json location, used only if the caller has not
# already set OPENCLAW_CONFIG_PATH / OPENCLAW_STATE_DIR.
if [[ -z "${OPENCLAW_CONFIG_PATH:-}" && -z "${OPENCLAW_STATE_DIR:-}" ]]; then
  default_cfg="${HOME}/Library/Application Support/openclaw/openclaw.json"
  if [[ -f "$default_cfg" ]]; then
    export OPENCLAW_CONFIG_PATH="$default_cfg"
  fi
fi

exec "${SCRIPT_DIR}/heartbeat-to-poke.sh" "$@"
