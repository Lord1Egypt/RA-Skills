#!/bin/bash
# OpenCode 自动回调脚本 - 简化版
# 用法: ./opencode-auto-callback.sh <session_key> <task_description> <opencode_args...>
# 示例: ./opencode-auto-callback.sh "agent:main:qqbot:direct:xxx" "修复bug" "修复登录问题"

SESSION_KEY="$1"
TASK_DESC="$2"
shift 2  # 移除前两个参数，剩下的都是 opencode 参数

if [ -z "$SESSION_KEY" ] || [ -z "$TASK_DESC" ]; then
  echo "用法: $0 <session_key> <task_description> <opencode_args...>"
  echo ""
  echo "示例:"
  echo "  $0 agent:main:qqbot:direct:xxx '修复bug' '修复登录问题'"
  echo "  $0 agent:main:qqbot:direct:xxx '添加功能' -m opencode/mimo-v2-pro-free '添加用户认证'"
  exit 1
fi

# 创建结果目录
RESULT_DIR="$HOME/.openclaw/task-results"
mkdir -p "$RESULT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RESULT_FILE="$RESULT_DIR/task-${TIMESTAMP}.txt"
LOG_FILE="$RESULT_DIR/task-${TIMESTAMP}.log"
JSON_OUTPUT="$RESULT_DIR/task-${TIMESTAMP}.jsonl"

echo "🚀 启动 OpenCode 任务"
echo "📝 任务描述: $TASK_DESC"
echo "🔑 Session: $SESSION_KEY"
echo "📁 结果文件: $RESULT_FILE"

# 发送开始通知
/home/root1/.openclaw/scripts/task-callback.sh "$SESSION_KEY" "🔄 任务已开始: $TASK_DESC" &

# 记录开始信息
echo "=== 任务开始 ===" > "$LOG_FILE"
echo "开始时间: $(date)" >> "$LOG_FILE"
echo "任务描述: $TASK_DESC" >> "$LOG_FILE"
echo "参数: $@" >> "$LOG_FILE"
echo "=== 执行输出 ===" >> "$LOG_FILE"

# 执行 opencode 命令，使用 JSON 格式输出
opencode run --format json "$@" > "$JSON_OUTPUT" 2>>"$LOG_FILE"
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