#!/usr/bin/env bash
# OpenClaw-first setup for Offlyn Clipper MCP bridge.
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRIDGE="$SKILL_ROOT/mcp-bridge"
HOME_DIR="${HOME:?}"

pick_socket() {
  local candidates=(
    "$HOME_DIR/Library/Application Support/ai.offlyn.clipper/clipper.sock"
    "$HOME_DIR/Library/Containers/ai.offlyn.clipper/Data/Library/Application Support/ai.offlyn.clipper/clipper.sock"
  )
  for p in "${candidates[@]}"; do
    if [[ -S "$p" || -e "$p" ]]; then
      echo "$p"
      return 0
    fi
  done
  echo "${candidates[0]}"
  return 1
}

echo "== Offlyn Clipper × OpenClaw setup =="
echo "Skill: $SKILL_ROOT"

if [[ ! -f "$BRIDGE/index.mjs" ]]; then
  echo "error: mcp-bridge missing at $BRIDGE" >&2
  exit 1
fi

echo "→ Installing bridge dependencies…"
(cd "$BRIDGE" && npm install --omit=dev)

SOCKET="$(pick_socket)" || true
if [[ ! -S "$SOCKET" && ! -e "$SOCKET" ]]; then
  echo ""
  echo "⚠️  Clipper socket not found at:"
  echo "   $SOCKET"
  echo "   Launch Offlyn Clipper, then re-run this script."
  echo ""
  exit 1
fi

export CLIPPER_SOCKET_PATH="$SOCKET"
export BRIDGE_INDEX="$BRIDGE/index.mjs"
echo "→ Socket path: $CLIPPER_SOCKET_PATH"

echo "→ Registering MCP server 'clipper' in OpenClaw…"
if ! command -v openclaw >/dev/null 2>&1; then
  echo "error: openclaw CLI not on PATH" >&2
  exit 1
fi

openclaw mcp unset clipper 2>/dev/null || true
MCP_JSON="$(node -e 'console.log(JSON.stringify({
  command: "node",
  args: [process.env.BRIDGE_INDEX],
  env: { CLIPPER_SOCKET_PATH: process.env.CLIPPER_SOCKET_PATH },
  toolFilter: { include: ["clipper_*"] }
}))')"
openclaw mcp set clipper "$MCP_JSON"
openclaw mcp show clipper

echo ""
echo "→ Pairing — switch to Clipper now and click Allow on the dialog."
echo "   (If you miss it or click Deny, run: node \"$BRIDGE/pair.mjs\")"
echo ""
sleep 2

set +e
(cd "$BRIDGE" && node pair.mjs)
PAIR_EXIT=$?
set -e

if [[ "$PAIR_EXIT" -ne 0 ]]; then
  echo ""
  echo "⚠️  Pairing did not complete."
  echo "   1. Bring Offlyn Clipper to the front"
  echo "   2. Run: node \"$BRIDGE/pair.mjs\""
  echo "   3. Click Allow (not Deny)"
  echo ""
  exit 1
fi

echo ""
echo "→ Verifying Clipper MCP…"
node "$BRIDGE/verify.mjs" || true

echo ""
echo "✓ Setup complete."
echo ""
echo "IMPORTANT: start a NEW OpenClaw chat (/new) so clipper tools load in this session."
echo "  (Old chats keep a stale tool snapshot → 'bundle-mcp runtime disposed')"
echo ""
echo "Test in a new chat:"
echo '  openclaw agent --message "Catch me up on my current Clipper meeting"'
echo ""
echo "After upgrading this repo:"
echo "  bash \"$SKILL_ROOT/scripts/update-installed-skill.sh\""
echo "  openclaw gateway restart"
echo ""
