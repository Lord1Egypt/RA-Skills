#!/bin/bash
# fast-whisper 快速识别脚本
# 用法：./fast-whisper-fast.sh <音频文件>
# 支持用户自定义目录配置

# 使用国内镜像源
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
    # 默认使用技能目录下的 .venv
    if [ -f "${SCRIPT_DIR}/../.venv/bin/python" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/../.venv/bin/python"
    else
        echo "错误：未找到虚拟环境，请运行 ./scripts/install.sh"
        exit 1
    fi
fi

# 模型目录（支持自定义，默认：$HOME/.fast-whisper-models）
MODEL_DIR="${FAST_WHISPER_MODEL_DIR:-${HOME}/.fast-whisper-models}"

if [ -z "$1" ]; then
    echo "用法：$0 <音频文件>"
    exit 1
fi

AUDIO_FILE="$1"

if [ ! -f "$AUDIO_FILE" ]; then
    echo "错误：文件不存在 - $AUDIO_FILE"
    exit 1
fi

"$VENV_PYTHON" << EOF
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root="$MODEL_DIR")
segments, info = model.transcribe("$AUDIO_FILE", language="zh")

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
EOF
