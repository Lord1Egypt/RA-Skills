#!/bin/bash
# 将项目最新文件同步到 openclaw workspace 缓存，并重启 gateway
# 用法：bash scripts/sync-to-openclaw.sh

SKILL_CACHE=~/.openclaw/workspace/skills/korean-booking
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "📂 项目目录：$PROJECT_DIR"
echo "📦 缓存目录：$SKILL_CACHE"

cp "$PROJECT_DIR/skill.json"   "$SKILL_CACHE/skill.json"   && echo "✅ skill.json"
cp "$PROJECT_DIR/SKILL.md"     "$SKILL_CACHE/SKILL.md"     && echo "✅ SKILL.md"
cp "$PROJECT_DIR/api/skill.js" "$SKILL_CACHE/api/skill.js" && echo "✅ api/skill.js"

# 同步 core
for f in resolver.js preprocessor.js service.js renderer.js; do
  [ -f "$PROJECT_DIR/core/$f" ] && cp "$PROJECT_DIR/core/$f" "$SKILL_CACHE/core/$f" && echo "✅ core/$f"
done

# 同步 data 和 i18n
cp "$PROJECT_DIR/data/hospitals.json" "$SKILL_CACHE/data/hospitals.json" && echo "✅ data/hospitals.json"

echo ""
echo "🔄 重启 openclaw gateway..."
pkill -f openclaw-gateway 2>/dev/null
sleep 1
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
sleep 3

echo "📋 当前技能状态："
openclaw skills list 2>/dev/null | grep -A 2 booking
echo ""
echo "🎉 同步完成！"
