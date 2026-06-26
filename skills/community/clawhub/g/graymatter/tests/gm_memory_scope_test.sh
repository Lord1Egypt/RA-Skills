#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp "$ROOT_DIR/scripts/gm-write" "$TMP_DIR/gm-write"
cp "$ROOT_DIR/scripts/gm-query" "$TMP_DIR/gm-query"
chmod +x "$TMP_DIR/gm-write" "$TMP_DIR/gm-query"

cat > "$TMP_DIR/graymatter_api.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "${3:-}"
EOF
chmod +x "$TMP_DIR/graymatter_api.sh"

AUTOMATION_MEMORY="/tmp/codex-home/.codex/automations/mcp-and-skill-hunter/memory.md"

WRITE_OUTPUT="$(
  "$TMP_DIR/gm-write" context "Research complete; publish blocked" \
    --scope-path "$AUTOMATION_MEMORY" \
    --user codex-user
)"

jq -e '.sourceChannel == "codex:automation:mcp-and-skill-hunter"' <<<"$WRITE_OUTPUT" >/dev/null
jq -e '.text | contains("[graymatter-scope]")' <<<"$WRITE_OUTPUT" >/dev/null
jq -e '.text | contains("scope: automation")' <<<"$WRITE_OUTPUT" >/dev/null
jq -e '.text | contains("automationId: mcp-and-skill-hunter")' <<<"$WRITE_OUTPUT" >/dev/null
jq -e '.text | contains("artifactPath: /tmp/codex-home/.codex/automations/mcp-and-skill-hunter/memory.md")' <<<"$WRITE_OUTPUT" >/dev/null
jq -e '.text | contains("Research complete; publish blocked")' <<<"$WRITE_OUTPUT" >/dev/null

QUERY_OUTPUT="$("$TMP_DIR/gm-query" "publish blocked" 5 context --scope-path "$AUTOMATION_MEMORY")"

jq -e '.q == "publish blocked"' <<<"$QUERY_OUTPUT" >/dev/null
jq -e '.maxResults == 5' <<<"$QUERY_OUTPUT" >/dev/null
jq -e '.type == "context"' <<<"$QUERY_OUTPUT" >/dev/null
jq -e '.source == "codex:automation:mcp-and-skill-hunter"' <<<"$QUERY_OUTPUT" >/dev/null

CHAT_OUTPUT="$(
  "$TMP_DIR/gm-write" decision "Use sourceChannel for scoped retrieval" \
    --chat-key "thread-42" \
    --workspace-key "2026-05-12/scan-the-internet-for-lhe-best"
)"

jq -e '.sourceChannel == "codex:chat:thread-42"' <<<"$CHAT_OUTPUT" >/dev/null
jq -e '.text | contains("workspaceKey: 2026-05-12/scan-the-internet-for-lhe-best")' <<<"$CHAT_OUTPUT" >/dev/null

echo "gm_memory_scope_test: PASS"
