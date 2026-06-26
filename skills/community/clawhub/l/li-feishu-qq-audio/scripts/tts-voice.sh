#!/bin/bash
# TTS 语音生成脚本
# 用法：./tts-voice.sh "文本内容" [输出文件.mp3]
# 支持用户自定义目录配置

export HF_ENDPOINT=https://hf-mirror.com

# 加载用户配置的环境变量
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
    source "${SCRIPT_DIR}/.env"
fi

# 使用虚拟环境（支持自定义目录）
if [ -n "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
    VENV_PYTHON="$VENV_DIR/bin/python"
else
    if [ -f "${SCRIPT_DIR}/../.venv/bin/python" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/../.venv/bin/python"
    else
        echo "错误：未找到虚拟环境，请运行 ./scripts/install.sh"
        exit 1
    fi
fi

if [ -z "$1" ]; then
    echo "用法：$0 \"文本内容\" [输出文件.mp3]"
    exit 1
fi

TEXT="$1"

# 输出文件（支持自定义临时目录）
TEMP_DIR="${TEMP_DIR:-/tmp}"
OUTPUT="${2:-${TEMP_DIR}/tts-output-$(date +%s).mp3}"

"$VENV_PYTHON" << EOF
import asyncio
import edge_tts
import sys
import logging

# 配置日志输出到 stderr（不干扰 stdout）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
_logger = logging.getLogger(__name__)

async def main():
    TEXT = """$TEXT"""
    OUTPUT = "$OUTPUT"
    
    try:
        # 中文女声
        communicate = edge_tts.Communicate(TEXT, "zh-CN-XiaoxiaoNeural")
        await communicate.save(OUTPUT)
        # 只输出文件路径到 stdout（供调用者使用）
        print(OUTPUT, flush=True)
    except Exception as e:
        _logger.error(f"TTS 合成失败：{e}")
        sys.exit(1)

asyncio.run(main())
EOF

# 捕获 Python 输出（文件路径）
TTS_OUTPUT=$("$VENV_PYTHON" 2>&1)
TTS_EXIT_CODE=$?

# 输出日志到 stderr（不干扰返回值）
echo "$TTS_OUTPUT" >&2

if [ $TTS_EXIT_CODE -eq 0 ]; then
    # 从输出中提取文件路径（最后一行非日志行）
    FILE_PATH=$(echo "$TTS_OUTPUT" | grep -v "^20" | grep -v "^Traceback" | tail -1)
    echo "$FILE_PATH"
    exit 0
else
    exit 1
fi
