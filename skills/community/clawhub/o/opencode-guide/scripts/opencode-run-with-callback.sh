#!/bin/bash
# OpenCode 自动回调包装脚本
# 用法: ./opencode-run-with-callback.sh <session_key> <task_description> <opencode_command>
# 示例: ./opencode-run-with-callback.sh "agent:main:qqbot:direct:xxx" "修复bug" "opencode run '修复登录问题'"

SESSION_KEY="$1"
TASK_DESC="$2"
OPENCODE_CMD="$3"
TIMEOUT="${4:-3600}"  # 默认超时 1 小时

if [ -z "$SESSION_KEY" ] || [ -z "$TASK_DESC" ] || [ -z "$OPENCODE_CMD" ]; then
  echo "用法: $0 <session_key> <task_description> <opencode_command> [timeout]"
  echo ""
  echo "参数说明:"
  echo "  session_key      - openclaw session key"
  echo "  task_description - 任务描述"
  echo "  opencode_command - opencode 命令（如: 'opencode run \"任务\"'）"
  echo "  timeout          - 超时时间（秒），默认 3600"
  echo ""
  echo "示例:"
  echo "  $0 agent:main:qqbot:direct:xxx '修复bug' 'opencode run \"修复登录问题\"'"
  exit 1
fi

# 创建结果目录
RESULT_DIR="$HOME/.openclaw/task-results"
mkdir -p "$RESULT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RESULT_FILE="$RESULT_DIR/task-${TIMESTAMP}.txt"
LOG_FILE="$RESULT_DIR/task-${TIMESTAMP}.log"

echo "🚀 启动 OpenCode 任务"
echo "📝 任务描述: $TASK_DESC"
echo "🔑 Session: $SESSION_KEY"
echo "⏱️  超时时间: ${TIMEOUT}秒"
echo "📁 结果文件: $RESULT_FILE"
echo "📋 日志文件: $LOG_FILE"

# 发送开始通知
/home/root1/.openclaw/scripts/task-callback.sh "$SESSION_KEY" "🔄 任务已开始: $TASK_DESC" &

# 创建临时文件存储 JSON 输出
JSON_OUTPUT="$RESULT_DIR/task-${TIMESTAMP}.jsonl"
touch "$JSON_OUTPUT"

# 执行 opencode 命令，使用 JSON 格式输出
echo "=== 任务开始 ===" > "$LOG_FILE"
echo "开始时间: $(date)" >> "$LOG_FILE"
echo "命令: $OPENCODE_CMD" >> "$LOG_FILE"
echo "=== 执行输出 ===" >> "$LOG_FILE"

# 使用 timeout 执行命令，捕获 JSON 输出
timeout "$TIMEOUT" bash -c "$OPENCODE_CMD --format json 2>&1" > "$JSON_OUTPUT" 2>>"$LOG_FILE"
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "=== 任务结束 ===" >> "$LOG_FILE"
echo "结束时间: $(date)" >> "$LOG_FILE"
echo "退出码: $EXIT_CODE" >> "$LOG_FILE"

# 解析 JSON 输出，提取结果
RESULT_TEXT=""
if [ -f "$JSON_OUTPUT" ]; then
  # 提取所有 text 类型的内容
  RESULT_TEXT=$(grep '"type":"text"' "$JSON_OUTPUT" | \
    sed 's/.*"text":"\([^"]*\)".*/\1/' | \
    tr -d '\\' | head -c 2000)
fi

# 保存结果到文件
echo "$RESULT_TEXT" > "$RESULT_FILE"

# 构建通知消息
if [ $EXIT_CODE -eq 0 ]; then
  NOTIFY_MSG="✅ 任务完成: $TASK_DESC"
else
  if [ $EXIT_CODE -eq 124 ]; then
    NOTIFY_MSG="⏰ 任务超时: $TASK_DESC"
  else
    NOTIFY_MSG="❌ 任务失败: $TASK_DESC (退出码: $EXIT_CODE)"
  fi
fi

# 发送完成通知
/home/root1/.openclaw/scripts/task-callback.sh "$SESSION_KEY" "$NOTIFY_MSG" "$RESULT_FILE"

echo "✅ 通知已发送到 session: $SESSION_KEY"
exit $EXIT_CODE