#!/usr/bin/env bash
# detect-drift.sh <profile>
#
# Thin wrapper around post-update-awareness/scripts/check-plugin-drift.sh.
# Exists so callers of post-update-maintenance don't have to know about the
# awareness layout.
#
# Output (stdout): one DRIFT line per drifted plugin, or empty.
# Exit: always 0 (advisory tool).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_lib.sh
source "$SCRIPT_DIR/_lib.sh"

PROFILE="${1:-}"
if [ -z "$PROFILE" ]; then
  echo "usage: detect-drift.sh <profile>" >&2
  exit 2
fi

pum_require_awareness

AWARENESS_SCRIPTS="$(pum_resolve_awareness)"
GW="$(pum_current_gateway_version)"

if [ -z "$GW" ]; then
  echo "BLOCKED no-gateway-version: openclaw -V returned nothing parseable" >&2
  exit 2
fi

# Invoke via bash because clawhub install does not preserve exec bits.
bash "$AWARENESS_SCRIPTS/check-plugin-drift.sh" "$GW" "$PROFILE"
