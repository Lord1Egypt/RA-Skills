#!/usr/bin/env bash
# parking_query skill 自動更新腳本
# 由 OpenClaw 每週維護 cron 呼叫，或手動執行

SKILL_DIR="$HOME/.openclaw/skills/parking_query"
REPO_URL="https://github.com/Harperbot/openclaw-parking-query"
CURRENT="$SKILL_DIR/parking_query.py"
REMOTE="$REPO_URL/raw/main/parking_query.py"

echo "[parking_query] 檢查更新..."

# 取遠端版本號（第一行 # version: x.x.x）
REMOTE_VER=$(curl -sf "$REMOTE" | grep -m1 '# version:' | awk '{print $3}')
LOCAL_VER=$(grep -m1 '# version:' "$CURRENT" 2>/dev/null | awk '{print $3}')

if [ -z "$REMOTE_VER" ]; then
  echo "[parking_query] ⚠️ 無法取得遠端版本，跳過"
  exit 0
fi

if [ "$LOCAL_VER" = "$REMOTE_VER" ]; then
  echo "[parking_query] ✅ 已是最新版（$LOCAL_VER）"
  exit 0
fi

echo "[parking_query] 發現新版本：$LOCAL_VER → $REMOTE_VER，開始更新..."
curl -sf "$REPO_URL/raw/main/parking_query.py" -o "$CURRENT.tmp" && \
  mv "$CURRENT.tmp" "$CURRENT" && \
  curl -sf "$REPO_URL/raw/main/skill.yml" -o "$SKILL_DIR/skill.yml.tmp" && \
  mv "$SKILL_DIR/skill.yml.tmp" "$SKILL_DIR/skill.yml"

echo "[parking_query] ✅ 更新完成（$REMOTE_VER）"
