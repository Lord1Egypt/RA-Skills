#!/bin/bash
#
# Good-Memory: Session 历史记录恢复脚本 v2.0.0
# 简化版：快速读取reset文件的历史记录
#

set -e

# 支持环境变量自定义路径
OPENCLAW_BASE="${OPENCLAW_BASE:-/root/.openclaw}"
SESSIONS_DIR="${SESSIONS_DIR:-${OPENCLAW_BASE}/agents/main/sessions}"

# 找到最新的reset文件
find_latest_reset() {
    ls -t "${SESSIONS_DIR}"/*.jsonl.reset.* 2>/dev/null | head -1
}

# 读取reset文件的最后N条记录并格式化
read_history() {
    local file="$1"
    local lines="${2:-50}"
    
    if [[ ! -f "$file" ]]; then
        echo "File not found: $file"
        return 1
    fi

    # 读取最后N行，过滤出用户和助手的消息
    tail -n "$lines" "$file" | python3 -c "
import sys, json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        if data.get('type') == 'message':
            msg = data.get('message', {})
            role = msg.get('role', '')
            content = msg.get('content', '')
            
            # 提取文本内容
            text = ''
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get('type') == 'text':
                        text = c.get('text', '')
                        break
            elif isinstance(content, str):
                text = content
            
            if text and role in ('user', 'assistant'):
                # 截断过长文本
                if len(text) > 300:
                    text = text[:300] + '...'
                print(f'[{role}] {text}')
    except:
        pass
"
}

# 主入口
main() {
    [[ $# -lt 1 ]] && {
        echo "Usage: $0 <command> [options]"
        echo "Commands:"
        echo "  latest          - 显示最新的reset文件路径"
        echo "  read [--lines N] - 读取最新reset文件的历史记录（默认50条）"
        echo "  read-file <file> [--lines N] - 读取指定reset文件的历史记录"
        echo "  list            - 列出所有reset文件（按时间倒序）"
        exit 1
    }

    local command="$1"; shift

    case "$command" in
        latest)
            find_latest_reset
            ;;
        read)
            local lines=50
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --lines) lines="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            local latest_file=$(find_latest_reset)
            if [[ -n "$latest_file" ]]; then
                read_history "$latest_file" "$lines"
            else
                echo "No reset session found"
            fi
            ;;
        read-file)
            [[ $# -lt 1 ]] && { echo "Usage: $0 read-file <file> [--lines N]"; exit 1; }
            local file="$1"; shift
            local lines=50
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --lines) lines="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            read_history "$file" "$lines"
            ;;
        list)
            ls -t "${SESSIONS_DIR}"/*.jsonl.reset.* 2>/dev/null || echo "No reset files found"
            ;;
        *)
            echo "Unknown command: $command"
            exit 1
            ;;
    esac
}

main "$@"
