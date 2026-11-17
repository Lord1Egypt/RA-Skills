#!/usr/bin/env bash
# 单向同步：harness 演读DECK/ 真身 → 本 skill 可移植副本
# 用法：bash scripts/sync-from-harness.sh /path/to/hekouwang-content-harness/演读DECK
set -euo pipefail

HARNESS_DECK="${1:-}"
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ -z "$HARNESS_DECK" ] || [ ! -f "$HARNESS_DECK/publish.py" ]; then
  echo "用法: $0 <harness/演读DECK 绝对路径>"
  echo "例:  $0 ~/Dashboard/Github/hekouwang-content-harness/演读DECK"
  exit 1
fi

cp "$HARNESS_DECK/publish.py" "$SKILL_ROOT/scripts/publish.py"
cp "$HARNESS_DECK/home.html" "$SKILL_ROOT/assets/templates/home.html"

# 留言板后端与 D1 模板（有则同步，无则跳过）
for f in wrangler.toml schema.sql; do
  [ -f "$HARNESS_DECK/$f" ] && cp "$HARNESS_DECK/$f" "$SKILL_ROOT/assets/templates/$f"
done
if [ -f "$HARNESS_DECK/functions/api/comments.js" ]; then
  mkdir -p "$SKILL_ROOT/assets/functions/api"
  cp "$HARNESS_DECK/functions/api/comments.js" "$SKILL_ROOT/assets/functions/api/comments.js"
fi

# 副本是公开分发的：真身里的账号绑定值不能带进来
LEAKS="$(grep -nE '"token": "[0-9a-f]{32}"|"npm", "i", "-g"|^CF_PROJECT = "[a-z0-9-]+"' "$SKILL_ROOT/scripts/publish.py" || true)"
if [ -n "$LEAKS" ]; then
  echo "✗ publish.py 含账号绑定值或自动全局安装，副本不能这样发布："
  echo "$LEAKS"
  echo "  先让真身改为读 YANDU_CF_BEACON_TOKEN / YANDU_CF_PROJECT 环境变量，再重新同步。"
  exit 1
fi

echo "OK: 已从真身同步 → $SKILL_ROOT"
echo "  scripts/publish.py"
echo "  assets/templates/home.html"
[ -f "$SKILL_ROOT/assets/templates/wrangler.toml" ] && echo "  assets/templates/wrangler.toml (+ schema/comments 如有)"
