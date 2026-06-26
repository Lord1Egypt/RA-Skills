#!/usr/bin/env python3
"""
MeetMind — 本地 Whisper 转录脚本（venv 版）
用法: python3 transcribe.py <audio_file_path>
输出: 纯文本转录结果（stdout）

使用 ~/meetmind-env（已安装 openai-whisper + ffmpeg）
首次运行自动下载模型（small ≈ 488MB），之后完全离线。
"""

import json
import os
import sys
import subprocess
from pathlib import Path

# ── 自动重定向到 meetmind-env ─────────────────────
VENV_PYTHON = Path.home() / "meetmind-env" / "bin" / "python3.11"


def restart_in_venv():
    """如果当前不在 meetmind-env 中，重新用 venv 执行"""
    if VENV_PYTHON.exists() and sys.executable != str(VENV_PYTHON):
        cmd = [str(VENV_PYTHON), __file__] + sys.argv[1:]
        result = subprocess.run(cmd, capture_output=False)
        sys.exit(result.returncode)


# 在导入 whisper 之前重定向
restart_in_venv()

# 现在在 venv 中，可以安全导入
import time
import whisper

# ── 配置加载 ─────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
MODEL_CACHE_DIR = Path.home() / ".cache" / "whisper"


def load_config():
    defaults = {"model": "small", "language": "zh"}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            user = json.load(f)
    else:
        user = {}
    return {**defaults, **user}


# ── 文件校验 ─────────────────────────────────────
SUPPORTED_FORMATS = {".mp3", ".m4a", ".wav", ".aac", ".mp4",
                      ".mpeg", ".mpga", ".oga", ".ogg", ".webm", ".flac"}


def validate_file(filepath: str) -> Path:
    path = Path(filepath).expanduser().resolve()
    if not path.exists():
        print(json.dumps({"error": f"文件不存在: {filepath}"}))
        sys.exit(1)
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        print(json.dumps({
            "error": f"不支持的音频格式: {path.suffix}",
            "supported": sorted(SUPPORTED_FORMATS)
        }))
        sys.exit(1)
    return path


# ── 本地 Whisper 转录 ───────────────────────────
def transcribe(filepath: Path, config: dict) -> str:
    model_name = config["model"]
    language = config.get("language") or None

    # 输出进度到 stderr（不污染 stdout 的转录结果）
    sys.stderr.write(f"⏳ 加载模型 {model_name}（首次下载约需 1-3 分钟）...\n")

    try:
        model = whisper.load_model(
            model_name,
            download_root=str(MODEL_CACHE_DIR)
        )
    except Exception as e:
        print(json.dumps({
            "error": f"模型加载失败: {str(e)}",
            "hint": "检查网络连接（首次需下载模型），或尝试切换 model 为 'tiny'"
        }))
        sys.exit(1)

    sys.stderr.write(f"🎙️ 转录中...\n")

    t0 = time.time()
    try:
        result = model.transcribe(
            str(filepath),
            language=language,
            verbose=False
        )
        elapsed = time.time() - t0
        text = result["text"].strip()

        sys.stderr.write(f"✅ 转录完成（{elapsed:.1f}s，{len(text)} 字符）\n")
        return text

    except Exception as e:
        print(json.dumps({
            "error": f"转录失败: {str(e)}",
            "hint": "尝试减小文件、切换模型（如 tiny）或检查音频是否损坏"
        }))
        sys.exit(1)


# ── 主入口 ───────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少参数",
            "usage": "python3 transcribe.py <audio_file_path> [--model tiny|base|small|medium|large]",
            "models": {
                "tiny": "75MB，最快，适合快速测试",
                "base": "145MB，基础精度",
                "small": "488MB，推荐（中文效果好）",
                "medium": "1.5GB，高精度",
                "large": "3GB，最高精度（v3 用 large-v3）"
            },
            "note": "使用 ~/meetmind-env，无需 API Key"
        }))
        sys.exit(1)

    filepath = validate_file(sys.argv[1])
    config = load_config()

    # 命令行参数覆盖 config
    args = iter(sys.argv[2:])
    for arg in args:
        if arg == "--model":
            config["model"] = next(args, config["model"])
        elif arg == "--language":
            config["language"] = next(args, config["language"])

    transcript = transcribe(filepath, config)
    print(transcript)
