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

async def main():
    TEXT = """$TEXT"""
    OUTPUT = "$OUTPUT"
    
    # 中文女声
    communicate = edge_tts.Communicate(TEXT, "zh-CN-XiaoxiaoNeural")
    await communicate.save(OUTPUT)
    print(f"语音生成完成：{OUTPUT}")

asyncio.run(main())
EOF

echo "$OUTPUT"
