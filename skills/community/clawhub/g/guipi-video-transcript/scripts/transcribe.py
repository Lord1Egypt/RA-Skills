#!/usr/bin/env python3
"""
Transcribe audio using the best available engine for the current platform.

Strategy:
  - macOS: prefer whisper-cpp (brew, Metal GPU acceleration)
  - Windows / Linux / macOS fallback: use openai-whisper (pip)

This ensures the skill works on all platforms out of the box.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


# ── Model paths (for whisper-cpp) ──────────────────────────────────────────

MODEL_DIR = Path.home() / ".whisper-models"
MODELS = {
    "tiny": MODEL_DIR / "ggml-tiny.bin",
    "base": MODEL_DIR / "ggml-base.bin",
    "small": MODEL_DIR / "ggml-small.bin",
}

MODEL_URLS = {
    "tiny": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin",
    "base": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin",
    "small": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin",
}


# ── Whisper-cpp functions (macOS preferred) ─────────────────────────────────

def find_whisper_cli():
    """Find the whisper-cli binary. Returns None if not found."""
    candidates = []
    if platform.system() == "Darwin":
        candidates = [
            "/opt/homebrew/bin/whisper-cli",
            "/usr/local/bin/whisper-cli",
        ]
    elif platform.system() == "Linux":
        candidates = [
            "/usr/local/bin/whisper-cli",
            "/usr/bin/whisper-cli",
            os.path.expanduser("~/.local/bin/whisper-cli"),
        ]
    # Also try PATH
    candidates.append("whisper-cli")

    for p in candidates:
        if p == "whisper-cli":
            # Check via which/where
            try:
                result = subprocess.run(
                    ["which" if platform.system() != "Windows" else "where", p],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    return p
            except Exception:
                pass
        elif Path(p).exists():
            return p
    return None


def ensure_model(model_size: str = "base") -> str:
    """Ensure the whisper-cpp model file exists, download if needed."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS.get(model_size, MODELS["base"])

    if model_path.exists():
        return str(model_path)

    url = MODEL_URLS.get(model_size)
    if not url:
        raise ValueError(f"Unknown model size: {model_size}")

    print(f"Downloading whisper {model_size} model ({url})...")
    # Use curl on Unix, PowerShell on Windows
    if platform.system() == "Windows":
        ps_cmd = (
            f"Invoke-WebRequest -Uri '{url}' -OutFile '{model_path}'"
        )
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            ["curl", "-L", "-o", str(model_path), url],
            capture_output=True, text=True
        )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to download model:\n{result.stderr[-500:]}")
    print(f"Model saved to {model_path}")
    return str(model_path)


def transcribe_whisper_cpp(audio_path: str, model_size: str = "base", language: str = "auto") -> str:
    """Transcribe using whisper-cpp CLI. Returns the transcription text.
    Also generates SRT subtitle file alongside the text output."""
    whisper_bin = find_whisper_cli()
    if not whisper_bin:
        raise FileNotFoundError("whisper-cli not found")

    model_path = ensure_model(model_size)

    cmd = [whisper_bin, "-m", model_path, "-f", audio_path]
    if language and language != "auto":
        cmd.extend(["-l", language])
    # -osrt: output SRT subtitles to stdout (we capture and save)
    cmd.append("-osrt")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"whisper-cli failed:\n{result.stderr[-500:]}")

    return result.stdout.strip()


# ── OpenAI Whisper functions (Windows / fallback) ────────────────────────────

def ensure_openai_whisper():
    """Ensure openai-whisper is installed. Install if missing."""
    try:
        import whisper as _w  # noqa: F401
        return True
    except ImportError:
        pass

    print("Installing openai-whisper (first time, may take a few minutes)...")
    pip_cmd = [sys.executable, "-m", "pip", "install", "openai-whisper"]
    if os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY"):
        # Use proxy if configured
        pass
    result = subprocess.run(pip_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to install openai-whisper:\n{result.stderr[-500:]}\n"
            "Please install manually: pip install openai-whisper"
        )
    return True


def transcribe_openai_whisper(audio_path: str, model_size: str = "base", language: str = "auto") -> str:
    """Transcribe using Python openai-whisper package.
    Returns SRT-formatted subtitle text with timestamps."""
    ensure_openai_whisper()
    import whisper

    model = whisper.load_model(model_size)
    # language=None means auto-detect; only pass language if explicitly specified
    lang_param = None if (language == "auto" or not language) else language
    result = model.transcribe(audio_path, language=lang_param)

    # Convert segments to SRT format
    srt_lines = []
    for i, seg in enumerate(result.get("segments", []), 1):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        if text:
            srt_lines.append(str(i))
            srt_lines.append(format_srt_timestamp(start, end))
            srt_lines.append(text)
            srt_lines.append("")  # blank line between entries

    # If no segments, fall back to plain text
    if not srt_lines:
        return result.get("text", "").strip()

    return "\n".join(srt_lines)


def format_srt_timestamp(start_sec: float, end_sec: float) -> str:
    """Format start/end seconds into SRT timestamp: HH:MM:SS,mmm --> HH:MM:SS,mmm"""
    def _fmt(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int((sec % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{_fmt(start_sec)} --> {_fmt(end_sec)}"


def srt_to_plain_text(srt_content: str) -> str:
    """Extract plain text from SRT content, removing sequence numbers and timestamps."""
    lines = srt_content.strip().split("\n")
    text_lines = []
    for line in lines:
        # Skip sequence numbers (pure digits)
        if line.strip().isdigit():
            continue
        # Skip timestamp lines (contain -->)
        if "-->" in line:
            continue
        # Skip blank lines
        if not line.strip():
            continue
        text_lines.append(line.strip())
    return "".join(text_lines)


# ── Unified transcribe function ─────────────────────────────────────────────

def get_engine() -> str:
    """Determine the best transcription engine for the current platform.

    Returns: 'whisper-cpp' or 'openai-whisper'
    """
    # On macOS, prefer whisper-cpp (Metal GPU acceleration)
    if platform.system() == "Darwin" and find_whisper_cli():
        return "whisper-cpp"

    # On Windows, always use openai-whisper (no brew available)
    if platform.system() == "Windows":
        return "openai-whisper"

    # On Linux, try whisper-cpp first, fall back to openai-whisper
    if find_whisper_cli():
        return "whisper-cpp"

    return "openai-whisper"


def transcribe(audio_path: str, model_size: str = "base", language: str = "auto") -> str:
    """Transcribe audio using the best available engine.
    Returns SRT-formatted subtitle text with timestamps."""
    engine = get_engine()
    print(f"[video-transcript] Using engine: {engine} (platform: {platform.system()})")
    print(f"[video-transcript] Language: {'auto-detect' if language == 'auto' else language}")

    if engine == "whisper-cpp":
        return transcribe_whisper_cpp(audio_path, model_size, language)
    else:
        return transcribe_openai_whisper(audio_path, model_size, language)


# ── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <audio_wav_path> [model_size] [language]")
        print(f"  model_size: tiny|base|small (default: base)")
        print(f"  language: zh|en|ja|... (default: zh)")
        sys.exit(1)

    audio = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    lang = sys.argv[3] if len(sys.argv) > 3 else "auto"

    text = transcribe(audio, model, lang)
    print(text)