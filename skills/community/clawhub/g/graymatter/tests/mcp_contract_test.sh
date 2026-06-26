#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEGACY_CONTRACT="${ROOT}/references/mcp/memory-tool-contract.v1.json"
PORTABLE_CONTRACT="${ROOT}/references/contracts/mcp/graymatter_mcp_tools_v1.json"

jq -e '.version == "v1"' "$LEGACY_CONTRACT" >/dev/null
jq -e '.errors.AUTH_REQUIRED and .errors.UPSTREAM_UNAVAILABLE' "$LEGACY_CONTRACT" >/dev/null

jq -e '.version == "v1"' "$PORTABLE_CONTRACT" >/dev/null
for t in memory_query memory_get memory_put memory_put_batch memory_link memory_health memory_replay_deferred; do
  jq -e --arg t "$t" '.tools[] | select(.name==$t)' "$PORTABLE_CONTRACT" >/dev/null
done

jq -e '.tools | map(.name) | sort == ["memory_get","memory_health","memory_link","memory_put","memory_put_batch","memory_query","memory_replay_deferred"]' < <("${ROOT}/scripts/gm-mcp-contract") >/dev/null
jq -e '.tools | length > 0' < <("${ROOT}/scripts/gm-mcp-contract" --mode=portable --validate) >/dev/null
jq -e '.errors.AUTH_REQUIRED and .errors.UPSTREAM_UNAVAILABLE' < <("${ROOT}/scripts/gm-mcp-contract" legacy) >/dev/null
jq -e '.errors.AUTH_REQUIRED and .errors.UPSTREAM_UNAVAILABLE' < <("${ROOT}/scripts/gm-mcp-contract" --mode=legacy --validate) >/dev/null

echo "mcp_contract_test: ok"
