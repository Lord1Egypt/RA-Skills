#!/bin/bash
# LinkFox Agent 任务执行器
# 用法: bash run_task.sh '任务提示词' [超时秒数]
# 输出: STATUS / SHARE_URL / REPORT_1 / REPORT_2 等纯文本行
# 零 LLM 开销，纯脚本解析

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK="$1"
TIMEOUT="${2:-600}"

if [ -z "$TASK" ]; then
    echo "用法: bash run_task.sh '任务提示词' [超时秒数]"
    exit 1
fi

# 用临时文件避免变量中的引号问题
TMPFILE=$(mktemp /tmp/linkfox_output_XXXXXX.json)
trap "rm -f $TMPFILE" EXIT

# 执行 linkfox.py，JSON 格式输出到临时文件
python3 "$SCRIPT_DIR/linkfox.py" --wait --timeout "$TIMEOUT" --format json "$TASK" > "$TMPFILE" 2>/dev/null
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: linkfox.py exited with code $EXIT_CODE"
    cat "$TMPFILE" 2>/dev/null
    exit 1
fi

# Python 提取关键信息
python3 << 'PYEOF' "$TMPFILE"
import json, sys

with open(sys.argv[1]) as f:
    data = json.load(f)

status = data.get('status', 'unknown')
chat_id = data.get('chatId', '')
message_id = data.get('messageId', '')
share_url = data.get('shareUrl', '')
reflection = data.get('reflection', '')
results = data.get('results', [])

print(f'STATUS: {status}')
print(f'SHARE_URL: {share_url}')
print(f'CHAT_ID: {chat_id}')
print(f'MESSAGE_ID: {message_id}')
print(f'REFLECTION: {reflection[:500]}')
print(f'RESULTS_COUNT: {len(results)}')

# 提取 HTML 报告链接
html_idx = 1
for r in results:
    if r.get('type') == 'html':
        content = r.get('content', '')
        if content and content.startswith('http'):
            # content 本身就是 URL
            print(f'REPORT_{html_idx}: {content}')
        elif chat_id and message_id:
            # 兜底：从 chatId/messageId 拼接
            # 需要从 shareUrl 提取 user path
            # shareUrl 格式: https://agent.linkfox.com/share/{chatId}
            # 报告格式: https://agent-files.linkfox.com/user/{userId}/chat/{chatId}/{messageId}/{idx}.html
            # 但 userId 无法从返回数据获取，所以用 text 模式的 URL 更靠谱
            print(f'REPORT_{html_idx}: NEED_MANUAL_URL (chatId={chat_id}, messageId={message_id}, idx={html_idx})')
        html_idx += 1
PYEOF
