#!/usr/bin/env bash
set -euo pipefail

contract="references/contracts/mcp/graymatter_mcp_tools_v1.json"

jq -e '.version == "v1"' "$contract" >/dev/null
jq -e '.tools | length >= 7' "$contract" >/dev/null
jq -e '.tools | map(.name) | sort == ["memory_get","memory_health","memory_link","memory_put","memory_put_batch","memory_query","memory_replay_deferred"]' "$contract" >/dev/null
jq -e '.tools[] | .errors | length >= 1' "$contract" >/dev/null
jq -e '.tools[] | .errors[] | has("code") and has("retryable")' "$contract" >/dev/null

echo "portable MCP contract surface checks passed"
