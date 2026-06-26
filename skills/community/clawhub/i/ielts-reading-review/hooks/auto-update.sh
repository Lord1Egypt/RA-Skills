#!/bin/bash
# IELTS Reading Review Skill — 自动更新 hook
# 触发时机：用户提交复盘相关触发词
# 功能：检测本地 skill 版本，落后则自动更新，把结果注入 systemMessage

set -euo pipefail

SLUG="ielts-reading-review"
SKILL_DIR="$HOME/.workbuddy/skills/$SLUG"
CHECK_SCRIPT="$SKILL_DIR/scripts/check-update.js"

# 检查 check-update.js 存在
if [ ! -f "$CHECK_SCRIPT" ]; then
  echo '{"systemMessage": "⚠️ [IELTS Skill] check-update.js 不存在，跳过版本检查"}'
  exit 0
fi

# 运行版本检查
CHECK_OUTPUT=$(node "$CHECK_SCRIPT" 2>&1 || true)

# 判断是否有更新
if echo "$CHECK_OUTPUT" | grep -q "有新版本可用"; then
  # 自动更新
  UPDATE_OUTPUT=$(node "$CHECK_SCRIPT" --auto 2>&1 || true)
  NEW_VER=$(grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' "$SKILL_DIR/SKILL.md" 2>/dev/null | head -1 || echo "unknown")
  MSG="🔄 [IELTS Skill 自动更新] 本地 skill 版本落后，已自动更新到 $NEW_VER。**当前已加载的 skill 内容是旧版本**，必须重新告知用户：'检测到 skill 已自动更新，请重新发送你的复盘请求，Jarvis 将使用最新的 v$NEW_VER 流程处理。'"
  echo "{\"systemMessage\": \"$MSG\"}"
else
  # 已是最新，只输出版本横幅
  LOCAL_VER=$(python3 -c "import json; print(json.load(open('$SKILL_DIR/_meta.json'))['version'])" 2>/dev/null || echo "unknown")
  echo "{\"systemMessage\": \"✅ [IELTS Skill v$LOCAL_VER] 版本已是最新，可以直接开始复盘。\"}"
fi

exit 0
