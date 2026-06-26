#!/bin/bash
# Reading Notes Skill 发布脚本
# 创建时间: 2026-03-16

SKILL_DIR="/root/.openclaw/workspace/skills/reading-notes"
SLUG="reading-notes"
NAME="Reading Notes"
VERSION="1.2.0"
CHANGELOG="Initial release: structured reading notes with table formatting, 5 Whys internalization, and daily 21:00 reminders"

echo "正在发布 ${NAME}@${VERSION}..."
clawhub publish "${SKILL_DIR}" \
  --slug "${SLUG}" \
  --name "${NAME}" \
  --version "${VERSION}" \
  --changelog "${CHANGELOG}"

if [ $? -eq 0 ]; then
  echo "✅ 发布成功！"
else
  echo "❌ 发布失败，请检查错误信息"
fi
