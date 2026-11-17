#!/bin/bash

# 每日积分日报 - 定时任务脚本
# 每天早上 7 点执行，生成日报并发送到飞书群

set -e

# 设置时区为 Asia/Shanghai
export TZ="Asia/Shanghai"

WORKSPACE="/home/wang/.openclaw/agents/kids-study/workspace"
SCRIPT="$WORKSPACE/skills/kids-points/scripts/generate-daily-report.js"
OUTPUT_FILE="/tmp/kids-points-daily-report.json"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成每日积分日报..."

# 运行日报生成脚本
cd "$WORKSPACE"
TZ="Asia/Shanghai" node "$SCRIPT" > /tmp/kids-points-report-output.txt 2>&1

# 提取 JSON 输出
sed -n '/JSON_OUTPUT_START/,/JSON_OUTPUT_END/p' /tmp/kids-points-report-output.txt | \
  grep -v 'JSON_OUTPUT' > "$OUTPUT_FILE"

# 检查是否成功
if [ ! -s "$OUTPUT_FILE" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 日报生成失败"
  cat /tmp/kids-points-report-output.txt
  exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 日报生成成功"

# 提取飞书消息内容和 TTS 文案（使用 node 代替 jq）
FEISHU_MESSAGE=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$OUTPUT_FILE', 'utf8')).feishuMessage)")
TTS_CONTENT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$OUTPUT_FILE', 'utf8')).ttsContent)")
REPORT_DATE=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$OUTPUT_FILE', 'utf8')).date)")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📤 准备发送到飞书..."
echo "消息内容:"
echo "$FEISHU_MESSAGE"
echo ""
echo "🔊 TTS 语音文案:"
echo "$TTS_CONTENT"

# 通过 OpenClaw 发送飞书消息
# 使用 sessions_send 发送到 kids-study agent 会话
# 注意：这里需要通过 OpenClaw 的消息系统发送
# 由于这是在 cron 中运行，我们使用 message 工具

# 创建临时消息文件
MESSAGE_FILE="/tmp/kids-points-feishu-message.txt"
echo "$FEISHU_MESSAGE" > "$MESSAGE_FILE"

# 使用 OpenClaw message 工具发送
# 注意：需要确保 OpenClaw 正在运行
cd /home/wang/.openclaw/agents/kids-study/workspace

# 通过 openclaw 命令发送消息（如果可用）
FEISHU_CHAT_ID="chat:oc_7d968e918766825eb21d51ce45d7e043"

if command -v openclaw &> /dev/null; then
  # 使用 openclaw message 命令
  openclaw message send --channel feishu --target "$FEISHU_CHAT_ID" --message "$FEISHU_MESSAGE" 2>&1 && {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 消息已发送到飞书"
  } || {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ 消息发送失败"
  }
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ openclaw 命令不可用"
fi

# 生成并播放 TTS 语音（使用 SenseAudio TTS，童声）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔊 正在生成语音播报..."
TTS_SCRIPT="$WORKSPACE/skills/kid-point-voice-component/scripts/tts.py"
python3 "$TTS_SCRIPT" --voice child_0001_a --play "$TTS_CONTENT" 2>&1 && {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 语音播报完成"
} || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ 语音播报失败"
}

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 日报任务完成"
