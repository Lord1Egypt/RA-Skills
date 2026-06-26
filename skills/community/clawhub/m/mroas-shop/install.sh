#!/usr/bin/env bash
# 一键把 moras-shop SKILL.md 安装到本机所有 skill-aware Agent。
# 用法：bash install.sh   或   curl -sSL https://selltoai.ai/skills/install.sh | bash
set -euo pipefail

SRC_URL="${MORAS_SHOP_SKILL_URL:-https://selltoai.ai/skills/moras-shop/SKILL.md}"
DEST_DIRS=(
  "$HOME/.cursor/skills/moras-shop"
  "$HOME/.claude/skills/moras-shop"
  "$HOME/.codex/skills/moras-shop"
  "$HOME/.openclaw/skills/moras-shop"
)

echo "[moras-shop] downloading SKILL.md from $SRC_URL ..."
TMP=$(mktemp)
curl -fsSL "$SRC_URL" -o "$TMP"

for d in "${DEST_DIRS[@]}"; do
  mkdir -p "$d"
  cp "$TMP" "$d/SKILL.md"
  echo "[moras-shop] installed → $d/SKILL.md"
done
rm -f "$TMP"
echo "[moras-shop] done. Restart your agent to pick it up."
