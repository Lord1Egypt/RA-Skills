#!/bin/bash
# fast-whisper 快速识别脚本
# 用法：./fast-whisper-fast.sh <音频文件>
# 支持用户自定义目录配置

# 使用国内镜像源
export HF_ENDPOINT=https://hf-mirror.com

# 日志配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${LOG_DIR:-/tmp/openclaw}"
LOG_FILE="${LOG_DIR}/whisper-$(date +%Y-%m-%d).log"
mkdir -p "$LOG_DIR"

# 日志函数（输出到日志文件和 stderr）
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" >> "$LOG_FILE"
    echo "$msg" >&2
}

# 加载用户配置的环境变量
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
        log "错误：未找到虚拟环境，请运行 ./scripts/install.sh"
        exit 1
    fi
fi

# 模型目录（支持自定义，默认：$HOME/.fast-whisper-models）
MODEL_DIR="${FAST_WHISPER_MODEL_DIR:-${HOME}/.fast-whisper-models}"

# 模型名称（从环境变量读取，默认：tiny）
WHISPER_MODEL="${WHISPER_MODEL:-tiny}"

if [ -z "$1" ]; then
    echo "用法：$0 <音频文件>" >&2
    exit 1
fi

AUDIO_FILE="$1"

if [ ! -f "$AUDIO_FILE" ]; then
    log "错误：文件不存在 - $AUDIO_FILE"
    exit 1
fi

log "开始语音识别：$AUDIO_FILE (模型：$WHISPER_MODEL)"

# 只输出识别结果到 stdout（供调用者使用）
"$VENV_PYTHON" << EOF
import sys
import logging
from faster_whisper import WhisperModel

# 配置日志输出到 stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
_logger = logging.getLogger(__name__)

try:
    model = WhisperModel("$WHISPER_MODEL", device="cpu", compute_type="int8", download_root="$MODEL_DIR")
    segments, info = model.transcribe("$AUDIO_FILE", language="zh")
    
    # 只输出识别文本到 stdout（不带时间戳）
    for segment in segments:
        print(segment.text.strip(), flush=True)
    
    _logger.info(f"识别完成：{info.language} {info.duration:.2f}s (模型：$WHISPER_MODEL)")
except Exception as e:
    _logger.error(f"识别失败：{e}")
    sys.exit(1)
EOF

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    log "识别成功"
else
    log "识别失败 (exit code: $EXIT_CODE)"
fi
