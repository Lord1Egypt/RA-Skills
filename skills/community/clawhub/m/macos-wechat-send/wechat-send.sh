#!/bin/bash
# 微信发送消息快捷脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 使用 Python 脚本
VENV_DIR="$SCRIPT_DIR/wxbot"

# 检查虚拟环境是否存在（可能是符号链接）
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    VENV_DIR="/Users/sincere/.openclaw/workspace/wxbot/wxbot"
fi

if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "错误：虚拟环境未找到"
    exit 1
fi

source "$VENV_DIR/bin/activate"

# 如果只有 1 个参数，从 stdin 读取消息（支持多行和特殊字符）
if [ $# -eq 1 ]; then
    CONTACT="$1"
    MESSAGE=$(cat)
    python "$SCRIPT_DIR/wechat-send.py" "$CONTACT" "$MESSAGE"
# 如果有 2 个参数，正常发送单条消息
elif [ $# -eq 2 ]; then
    python "$SCRIPT_DIR/wechat-send.py" "$@"
# 如果有 3+ 个参数，第一个是联系人，后面都是消息（支持连续发送多条）
elif [ $# -ge 3 ]; then
    CONTACT="$1"
    shift
    python "$SCRIPT_DIR/wechat-send.py" "$CONTACT" "$@"
else
    echo "用法："
    echo "  wechat-send <联系人> <消息>           # 单条消息"
    echo "  wechat-send <联系人> <消息 1> <消息 2> ...  # 多条消息"
    echo "  echo '消息' | wechat-send <联系人>    # 从 stdin 读取"
    exit 1
fi
