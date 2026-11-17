#!/usr/bin/env bash
# 环境准备（一次性）—— 受限沙箱里装通 faster-whisper 的完整解法
#
# 三个必须绕过的坑:
#   1. 系统 Python 是 PEP 668 externally-managed → 用 venv /opt/wenv
#   2. huggingface.co 直连不可达 → 用 hf-mirror.com
#   3. XET CAS (cas-server.xethub.hf.co) 返回 401 → HF_HUB_DISABLE_XET=1
set -euo pipefail

python3 -m venv /opt/wenv
/opt/wenv/bin/pip install -q --upgrade pip
/opt/wenv/bin/pip install -q faster-whisper

# 模型下载（首次运行 whisper_word_gen.py 时自动拉取，此处可预热）
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_XET=1
/opt/wenv/bin/python - <<'PY'
from faster_whisper import WhisperModel
WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")   # 预热下载
print("whisper 模型就绪")
PY

# 校验工具
command -v ffmpeg >/dev/null && echo "ffmpeg OK"
fc-list :lang=zh | head -1
