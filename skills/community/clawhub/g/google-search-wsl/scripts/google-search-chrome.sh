#!/usr/bin/env bash
# Google Search Chrome 启动脚本
# 在 WSL 中启动带 CDP 的 Chrome 用于 browser 工具控制
set -euo pipefail

PORT="${GOOGLE_SEARCH_CHROME_PORT:-9222}"
DATA_DIR="${GOOGLE_SEARCH_CHROME_DATA:-$HOME/.openclaw/chrome-debug-profile}"
TIMEOUT="${GOOGLE_SEARCH_CHROME_TIMEOUT:-10}"

# 检查是否已运行
if curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1; then
    echo "Chrome 已在端口 $PORT 运行"
    exit 0
fi

# 创建数据目录
mkdir -p "$DATA_DIR"

# WSL 特定标志
WSL_FLAGS=()
if [[ -r /proc/version ]] && grep -qiE 'microsoft|wsl' /proc/version; then
    # 检查 WSLg
    if [[ -S /mnt/wslg/.X11-unix/X0 ]]; then
        export DISPLAY=:0
    fi
    if [[ "${GOOGLE_SEARCH_DISABLE_GPU:-1}" != "0" ]]; then
        WSL_FLAGS+=(--disable-gpu)
    fi
    WSL_FLAGS+=(--disable-dev-shm-usage)
fi

# 查找 Chrome
CHROME_BIN=""
for bin in google-chrome-stable google-chrome chromium chromium-browser; do
    if command -v "$bin" &>/dev/null; then
        CHROME_BIN="$bin"
        break
    fi
done

if [[ -z "$CHROME_BIN" ]]; then
    echo "错误：未找到 Chrome/Chromium" >&2
    echo "安装：sudo apt install google-chrome-stable" >&2
    exit 1
fi

echo "启动 Chrome ($CHROME_BIN) 在端口 $PORT..."

# 启动 Chrome
"$CHROME_BIN" \
    --remote-debugging-port="$PORT" \
    --remote-allow-origins='*' \
    --user-data-dir="$DATA_DIR" \
    --lang="${GOOGLE_SEARCH_LANG:-zh-CN}" \
    "${WSL_FLAGS[@]}" \
    "$@" &

CHROME_PID=$!

# 等待 Chrome 启动
echo "等待 Chrome 启动..."
for i in $(seq 1 "$TIMEOUT"); do
    if curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1; then
        echo "Chrome 已启动 (PID: $CHROME_PID)"
        echo "CDP 地址: http://127.0.0.1:$PORT"
        exit 0
    fi
    sleep 1
done

echo "警告：Chrome 启动超时，但进程仍在运行 (PID: $CHROME_PID)" >&2
exit 0