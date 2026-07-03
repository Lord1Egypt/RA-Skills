#!/usr/bin/env python3
"""Full pipeline: video → transcript. Handles audio extraction + transcription."""

import sys
import os
import json
from pathlib import Path

# Add parent scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from extract_audio import extract_audio
from transcribe import transcribe, srt_to_plain_text

# State file to track first-run and user opt-out preference
STATE_FILE = Path.home() / ".workbuddy" / "skills" / "video-transcript" / ".state.json"
SKILL_DIR = Path(__file__).parent.parent
QR_PATH = SKILL_DIR / "assets" / "author-qrcode.jpg"

AUTHOR_CREDIT = "📹 视频文案提取技能 | 作者：桂皮AI实战 | 公众号/小红书/抖音同名"
OPT_OUT_KEYWORD = "关闭桂皮引流"
OPT_OUT_HINT = f'💡 如果不想每次看到作者信息，请对 AI 说："{OPT_OUT_KEYWORD}"'


def load_state() -> dict:
    """Load skill state (first_run, opted_out)."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"first_run": True, "opted_out": False}


def save_state(state: dict):
    """Save skill state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def show_qr_code():
    """Display QR code image in terminal (iTerm2/WorkBuddy) or show path."""
    if not QR_PATH.exists():
        return

    # Try iTerm2 inline image protocol (works in WorkBuddy)
    try:
        import base64
        with open(QR_PATH, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        # ESC ] 1337 ; File= ... : data ST
        print(f"\033]1337;File=name=qrcode.jpg;width=200px;inline=1:{img_data}\a")
        return
    except Exception:
        pass

    # Fallback: just print the path
    print(f"📌 二维码图片路径：{QR_PATH}")


def print_first_run_message():
    """Print first-run welcome message with QR code."""
    print("\n" + "=" * 55)
    print("👋 感谢使用「视频文案提取」技能！")
    print("")
    print("   作者：桂皮（@桂皮AI实战）")
    print("   公众号 / 小红书 / 抖音：搜索「桂皮AI实战」")
    print("   专注 AI工具教程 · 扣子编程 · 效率方法")
    print("")
    print("   扫码添加作者微信，欢迎交流👇")
    show_qr_code()
    print("=" * 55)
    print(OPT_OUT_HINT)
    print("=" * 55 + "\n")


def print_footer_credit():
    """Print a short credit line after each transcript."""
    print(f"\n{AUTHOR_CREDIT}")


def video_to_transcript(
    video_path: str,
    output_dir: str,
    model_size: str = "base",
    language: str = "auto",
) -> str:
    """Convert video to transcript text. Returns the SRT content.
    Also saves .txt (plain text) and .srt (subtitles with timestamps)."""
    video = Path(video_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Step 1: Extract audio
    wav_path = out / f"{video.stem}.wav"
    print(f"Extracting audio to {wav_path}...")
    extract_audio(str(video), str(wav_path))

    # Step 2: Transcribe → SRT format
    print(f"Transcribing (model={model_size}, language={'auto' if language == 'auto' else language})...")
    srt_content = transcribe(str(wav_path), model_size, language)

    # Step 3: Save SRT (with timestamps)
    srt_path = out / f"{video.stem}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"SRT subtitles saved to {srt_path}")

    # Step 4: Save plain text (no timestamps)
    txt_path = out / f"{video.stem}.txt"
    plain_text = srt_to_plain_text(srt_content)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_text)
    print(f"Plain text saved to {txt_path}")

    return srt_content


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <video_path> <output_dir> [model_size] [language]")
        sys.exit(1)

    video = sys.argv[1]
    output_dir = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "base"
    lang = sys.argv[4] if len(sys.argv) > 4 else "auto"

    # Load state
    state = load_state()

    # First-run: show QR code + welcome
    if state.get("first_run", True):
        print_first_run_message()
        state["first_run"] = False
        save_state(state)

    # Run the pipeline
    srt_content = video_to_transcript(video, output_dir, model, lang)

    # Print plain text version for readability
    plain_text = srt_to_plain_text(srt_content)
    print(f"\n=== Transcript ({len(plain_text)} chars) ===")
    print(plain_text)

    # Footer credit (unless user opted out)
    if not state.get("opted_out", False):
        print_footer_credit()
        print(OPT_OUT_HINT)
