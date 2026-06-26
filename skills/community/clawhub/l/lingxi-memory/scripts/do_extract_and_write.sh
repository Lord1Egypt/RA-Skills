#!/bin/bash
# 会话提炼 + 写入脚本 - 最终完善版（新架构：一次完成所有工作）
# 功能: 从会话文件中提炼记忆，agent 直接提炼 + 写入 L2-L4 + 发通知
# 特点: 
# - 无行数限制，完整读取会话
# - 只有过滤不通过或异常时才通知用户
# - 完整的异常处理流程
# - 明确的非0返回值界定，可靠的AI调用失败检测
# - 增加超时等待，区分空输出和延迟输出
# - 新架构：bash 调用 agent，agent 直接完成提炼 + 写入 + 通知，省去队列
# - 安全改进：trap 确保临时文件 always 清理，避免敏感信息残留

# 配置
WORKSPACE="/root/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
EXTRACTED_FILE="$WORKSPACE/memory/.extracted_sessions"
# 所有飞书资源ID从环境变量读取，必须配置
# 在 .env 文件中设置以下环境变量：
# - FEISHU_USER_OPEN_ID: 你的飞书 open_id
# - L2_APP_TOKEN: L2 任务看板 多维表格 app_token
# - L2_TABLE_ID: L2 任务看板 多维表格 table_id
# - L3_DOC_ID: L3 项目日志 飞书文档 doc_id
# - L4_DOC_ID: L4 知识沉淀 飞书文档 doc_id
USER_OPEN_ID="${FEISHU_USER_OPEN_ID}"
L2_APP_TOKEN="${L2_APP_TOKEN}"
L2_TABLE_ID="${L2_TABLE_ID}"
L3_DOC_ID="${L3_DOC_ID}"
L4_DOC_ID="${L4_DOC_ID}"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 返回值界定
# 0: 成功（提炼通过 OR 过滤跳过）
# 1: AI调用失败（退出码非0 或 输出包含错误 或 超时）
# 2: AI返回为空
# 3: 队列格式解析失败

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# 发送通知（直接用 openclaw CLI 发送）
send_notification() {
    local message="$1"
    log "通知: $message"
    
    # 用 openclaw CLI 发送消息
    # target 格式: user:ou_xxx
    if command -v openclaw &>/dev/null; then
        log "使用 openclaw CLI 发送消息到: user:$USER_OPEN_ID"
        openclaw message send --channel feishu --target "user:$USER_OPEN_ID" --message "$message" 2>&1 || {
            log "警告: openclaw CLI 发送失败"
        }
    else
        log "警告: openclaw CLI 不可用，无法发送通知"
    fi
}

# 检查参数
if [ $# -eq 0 ]; then
    log "用法: $0 <session_file>"
    exit 1
fi

# 检查必需环境变量
if [ -z "$FEISHU_USER_OPEN_ID" ] || [ -z "$L2_APP_TOKEN" ] || [ -z "$L2_TABLE_ID" ] || [ -z "$L3_DOC_ID" ] || [ -z "$L4_DOC_ID" ]; then
    log "错误: 必需环境变量未配置"
    log "请配置: FEISHU_USER_OPEN_ID, L2_APP_TOKEN, L2_TABLE_ID, L3_DOC_ID, L4_DOC_ID"
    exit 1
fi

SESSION_FILE="$1"
SESSION_ID=$(basename "$SESSION_FILE" | sed -E 's/\.jsonl(\..*)?$//')

if [ ! -f "$SESSION_FILE" ]; then
    log "错误: 会话文件不存在: $SESSION_FILE"
    send_notification "❌ 会话 $SESSION_ID 提炼失败：文件不存在"
    exit 1
fi

log "开始处理会话: $SESSION_FILE (Session ID: $SESSION_ID)"

# ========== 读取会话文件并统计 ==========

log "完整读取会话文件..."
USER_MESSAGE_COUNT=0
TOTAL_CONTENT_LENGTH=0
HAS_KEYWORD="false"

# 关键词列表（扩展版）
KEYWORDS=("记忆" "提炼" "报告" "问题" "错误" "完成" "成功" "创建" "修改" "更新" "删除" "项目" "任务" "工作" "学习" "思考" "讨论" "解决" "方案" "计划" "todo" "task" "project" "fix" "bug" "feature")

# 完整遍历会话文件
while IFS= read -r line; do
    # 跳过空行
    [ -z "$line" ] && continue
    
    # 解析JSON（支持 .message.role 和 .message.content[0].text 格式）
    ROLE=$(echo "$line" | python3 -c "
import sys, json
data = json.load(sys.stdin)
# 优先从 message.role 读取
if 'message' in data:
    print(data['message'].get('role', ''))
else:
    print(data.get('role', ''))
" 2>/dev/null)
    CONTENT=$(echo "$line" | python3 -c "
import sys, json
data = json.load(sys.stdin)
content = ''
# 优先从 message.content 读取
if 'message' in data:
    msg_content = data['message'].get('content', '')
    if isinstance(msg_content, list):
        # 如果是数组，提取第一个 text 类型的内容
        for item in msg_content:
            if isinstance(item, dict) and item.get('type') == 'text':
                content = item.get('text', '')
                break
    else:
        content = str(msg_content)
else:
    # 老格式：直接从 content 读取
    raw_content = data.get('content', '')
    if isinstance(raw_content, list):
        for item in raw_content:
            if isinstance(item, dict) and item.get('type') == 'text':
                content = item.get('text', '')
                break
    else:
        content = str(raw_content)
print(content)
" 2>/dev/null)
    
    # 统计用户消息
    if [ "$ROLE" = "user" ]; then
        USER_MESSAGE_COUNT=$((USER_MESSAGE_COUNT + 1))
        TOTAL_CONTENT_LENGTH=$((TOTAL_CONTENT_LENGTH + ${#CONTENT}))
        
        # 检查关键词
        for keyword in "${KEYWORDS[@]}"; do
            if [[ "$CONTENT" == *"$keyword"* ]]; then
                HAS_KEYWORD="true"
                break
            fi
        done
    fi
done < "$SESSION_FILE"

log "用户消息数: $USER_MESSAGE_COUNT"
log "内容长度: $TOTAL_CONTENT_LENGTH"
log "有关键词: $HAS_KEYWORD"

# ========== 过滤条件检查 ==========

# 过滤条件（优化版）
FILTER_PASS="true"
FILTER_REASON=""

if [ "$USER_MESSAGE_COUNT" -lt 1 ]; then
    FILTER_PASS="false"
    FILTER_REASON="用户消息数太少 ($USER_MESSAGE_COUNT < 1)"
elif [ "$TOTAL_CONTENT_LENGTH" -lt 20 ]; then
    FILTER_PASS="false"
    FILTER_REASON="内容长度太短 ($TOTAL_CONTENT_LENGTH < 20)"
fi

# 过滤不通过时通知用户，返回0（标记为已处理）
if [ "$FILTER_PASS" = "false" ]; then
    log "过滤跳过: $FILTER_REASON"
    send_notification "ℹ️ 会话 $SESSION_ID 过滤跳过：$FILTER_REASON"
    # 标记为已提炼
    echo "agent:main:session:${SESSION_ID}" >> "$EXTRACTED_FILE"
    log "返回0（标记为已处理）"
    exit 0
fi

log "过滤通过，开始提炼..."

# ========== 准备 AI 提炼 prompt ==========
# 使用 heredoc 定义，避免双引号解析问题
read -r -d '' EXTRACT_PROMPT << 'EOF'
你是灵曦的记忆提炼助手。请分析这个会话文件，提取有价值的记忆内容。

会话文件: __SESSION_FILE__
Session ID: __SESSION_ID__
用户消息数: __USER_MESSAGE_COUNT__
内容长度: __TOTAL_CONTENT_LENGTH__
有关键词: __HAS_KEYWORD__

请按以下格式输出（纯文本，不要Markdown）：

【提炼结果】
===
L2|任务名|项目名|优先级
L3|项目名|类型|内容|原因|结果
L4|成功经验|成果|关键步骤|成功因素|可复用要点
L4|踩坑记录|问题现象|错误信息|排查过程|解决方案|如何规避
===

提炼完成后，请你：
1. 按照你输出的提炼结果，**直接调用对应的 OpenClaw 工具** 将内容写入记忆空间：
   - L2 任务：调用 feishu_bitable_app_table_record 写入 L2 看板（app_token=$L2_APP_TOKEN, table_id=$L2_TABLE_ID）
     ⚠️ **重要**：L2 任务必须包含「创建时间」字段！使用当前北京时间（Asia/Shanghai），格式：年月日（如 2026/03/24）
   - L3 项目：调用 feishu_update_doc 写入 L3 项目文档（doc_id=$L3_DOC_ID），mode=append
   - L4 知识：调用 feishu_update_doc 写入 L4 知识文档（doc_id=$L4_DOC_ID），mode=append

**⚠️ 非常重要 - 时区要求：** 生成时间戳时，请**必须**使用 **Asia/Shanghai 时区（GMT+8 / 北京时间）**，**绝对不要**使用 UTC 时间！当前北京时间是 $(date +"%Y-%m-%d %H:%M:%S") 请参考这个时间，格式：`YYYY-MM-DD HH:MM:SS`

2. 所有写入完成后，调用 message 工具发送通知给我：
   - 参数：action=send, channel=feishu, target="user:$USER_OPEN_ID", message="消息内容"
   - 如果提炼成功且有内容写入，发送格式：

## 提炼结果

- **L2 任务**: X 条
- **L3 项目**: X 条
- **L4 知识**: X 条

   - 如果提炼成功但没有内容：发送 "ℹ️ 会话 __SESSION_ID__ 提炼完成，无内容需要写入"
3. 最后，输出 "DONE" 表示完成

注意：
- 没有内容的层级可以省略
- L2优先级可选：高/中/低
- L3类型可选：开发/配置/学习/讨论/问题排查
- 只提炼有价值的内容，不要逐字重复
- 【提炼结果】和===标记必须严格保留
- 工具调用必须正确，参数必须完整

开始分析：
EOF

# 替换占位符
# 使用 | 作为分隔符，避免 $SESSION_FILE 包含 / 导致 sed 错误
EXTRACT_PROMPT=$(echo "$EXTRACT_PROMPT" \
    | sed "s|__SESSION_FILE__|$SESSION_FILE|g" \
    | sed "s|__SESSION_ID__|$SESSION_ID|g" \
    | sed "s|__USER_MESSAGE_COUNT__|$USER_MESSAGE_COUNT|g" \
    | sed "s|__TOTAL_CONTENT_LENGTH__|$TOTAL_CONTENT_LENGTH|g" \
    | sed "s|__HAS_KEYWORD__|$HAS_KEYWORD|g")

# ========== 调用 openclaw agent 进行 AI 提炼 ==========

# 临时文件
AI_OUTPUT_FILE="/tmp/ai_extract_${SESSION_ID}_$$.txt"
PROMPT_FILE="/tmp/ai_prompt_${SESSION_ID}_$$.txt"
rm -f "$AI_OUTPUT_FILE" "$PROMPT_FILE"

# 清理陷阱：确保无论脚本如何退出（成功/失败/超时/中断），都删除临时文件
# 避免敏感信息（凭证、会话内容）残留在 /tmp
cleanup() {
    rm -f "$AI_OUTPUT_FILE" "$PROMPT_FILE"
}
trap cleanup EXIT INT TERM

# 把 prompt 写到临时文件（解决多行文本和特殊字符参数解析问题）
echo "$EXTRACT_PROMPT" > "$PROMPT_FILE"

# 调用 openclaw agent（后台运行，超时等待）
# 从临时文件读取 prompt，解决多行文本参数解析问题
log "调用 openclaw agent 进行 AI 提炼（后台运行，最多等待 180 秒）... prompt 大小: $(wc -c < "$PROMPT_FILE") bytes"
openclaw agent --agent main --session-id "extract_${SESSION_ID}" --message "$(cat "$PROMPT_FILE")" --local 2>&1 > "$AI_OUTPUT_FILE" &
AI_PID=$!
log "AI进程ID: $AI_PID"

# 等待AI完成（最多等待 300 秒 = 5分钟，适应大会话）
WAIT_TIME=0
MAX_WAIT=300
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    # 检查进程是否还在运行
    if ! kill -0 $AI_PID 2>/dev/null; then
        log "AI进程已结束"
        break
    fi
    
    # 每 10 秒打印一次等待进度
    if [ $((WAIT_TIME % 10)) -eq 0 ] && [ $WAIT_TIME -gt 0 ]; then
        log "已等待 ${WAIT_TIME}秒，AI仍在运行..."
    fi
    
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

# 如果超时，强制杀死进程
if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    log "AI调用超时（${MAX_WAIT}秒），强制终止"
    kill -9 $AI_PID 2>/dev/null
    wait $AI_PID 2>/dev/null
    send_notification "❌ 会话 $SESSION_ID 提炼失败：AI调用超时（${MAX_WAIT}秒）"
    exit 1
fi

# 等待进程完全结束并获取退出码
wait $AI_PID 2>/dev/null
OPENCLAW_EXIT_CODE=$?
log "AI进程退出码: $OPENCLAW_EXIT_CODE"

# 读取输出
EXTRACT_RESULT=$(cat "$AI_OUTPUT_FILE" 2>/dev/null)

# ========== 检查 AI 调用结果 ==========

# 检查1：退出码非0 → AI调用失败
if [ $OPENCLAW_EXIT_CODE -ne 0 ]; then
    log "AI调用失败 (退出码: $OPENCLAW_EXIT_CODE): $EXTRACT_RESULT"
    send_notification "❌ 会话 $SESSION_ID 提炼失败：AI调用失败（退出码：$OPENCLAW_EXIT_CODE）"
    exit 1
fi

# 检查2：输出为空 → AI返回为空
if [ -z "$EXTRACT_RESULT" ]; then
    log "AI返回为空（已等待${WAIT_TIME}秒，确认为空输出）"
    send_notification "❌ 会话 $SESSION_ID 提炼失败：AI返回为空"
    exit 2
fi

# ========== 提炼完成，agent 已经完成所有写入和通知 ==========

# 检查 agent 是否输出了 "DONE" → DONE 输出代表成功
if echo "$EXTRACT_RESULT" | grep -q "DONE"; then
    log "提炼完成，agent 已完成所有写入"
    # 标记为已提炼
    echo "agent:main:session:${SESSION_ID}" >> "$EXTRACTED_FILE"
    log "会话 $SESSION_ID 提炼完成，已标记为已提炼"
    exit 0
else
    # 如果没有 DONE，再检查是否有错误关键词（只检查 AI 的实际输出，不检查插件日志）
    if echo "$EXTRACT_RESULT" | grep -q -i "error\|fail\|exception\|无法\|失败"; then
        log "AI返回包含错误信息: $EXTRACT_RESULT"
        send_notification "❌ 会话 $SESSION_ID 提炼失败：AI返回错误信息"
        exit 1
    fi
    # 没有 DONE 也没有明显错误 → 视为失败
    log "AI 没有输出 DONE，可能提炼失败"
    send_notification "❌ 会话 $SESSION_ID 提炼失败：AI 没有完成写入"
    exit 3
fi

# 正常完成
exit 0
