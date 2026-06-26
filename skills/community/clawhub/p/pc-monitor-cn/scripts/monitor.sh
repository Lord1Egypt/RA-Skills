#!/bin/bash
# 系统监控脚本 - 快速查看系统状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_PY="$SCRIPT_DIR/monitor.py"

# 检查 Python 依赖
if ! command -v python3 &> /dev/null; then
    echo "错误：需要 Python3"
    exit 1
fi

# 检查 psutil 是否安装
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "正在安装 psutil..."
    pip3 install psutil -q
fi

# 运行监控脚本
python3 "$MONITOR_PY" "$@"
