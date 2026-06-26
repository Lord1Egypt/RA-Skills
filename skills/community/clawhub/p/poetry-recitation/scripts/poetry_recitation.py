#!/usr/bin/env python3
"""
Poetry Recitation Video Generator
Synthesizes a poem using a cloned or system voice, creates a video with starry background + subtitles.

Usage:
    python poetry_recitation.py --poem "床前明月光\n疑是地上霜\n举头望明月\n低头思故乡" --title "静夜思"
    python poetry_recitation.py --poem "..." --title "静夜思" --voice 章彦博
    python poetry_recitation.py --poem "..." --title "静夜思" --voice chelsie
"""

import argparse
import json
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, AudioFileClip

# Paths
TTS_SCRIPT = os.path.expanduser("~/.openclaw/skills/tts-gen-pipeline/scripts/generate.py")
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
DEFAULT_AUDIO_DIR = os.path.expanduser("~/.openclaw/workspace/audio/")
VOICES_FILE = os.path.expanduser("~/.openclaw/skills/tts-gen-pipeline/scripts/voices.json")

W, H = 1920, 1080

# Known system voices
SYSTEM_VOICES = {
    "cherry", "serena", "lihua", "xiaoyun", "xiaogang",
    "ethan", "asher", "chelsie", "xiaoming",
    "aria", "bella", "noah", "liam",
    "cantonese_female", "cantonese_male", "shanghai_female",
}


def load_voices():
    """Load voice name mapping from voices.json"""
    if os.path.exists(VOICES_FILE):
        with open(VOICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_default_voice():
    """Get first available cloned voice, or None"""
    voices = load_voices()
    if voices:
        return list(voices.keys())[0]
    return None


def detect_voice_type(voice_name):
    """Detect if voice is cloned, system, or direct voice ID."""
    voices = load_voices()
    if voice_name in voices:
        return "cloned", voices[voice_name]
    if voice_name in SYSTEM_VOICES:
        return "system", voice_name
    if voice_name.startswith("qwen-tts-vc-"):
        return "cloned", voice_name
    if voice_name.startswith("qwen-tts-vd-"):
        return "designed", voice_name
    # Assume system voice as fallback
    return "system", voice_name


def add_pacing(text):
    """Add pacing markers to slow down recitation rhythm."""
    lines = text.strip().split("\n")
    paced = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) <= 10 and len(line) >= 4:
            mid = len(line) // 2
            line = line[:mid] + "……" + line[mid:]
        elif len(line) > 10:
            chunks = []
            for i in range(0, len(line), 5):
                chunk = line[i:i+5]
                if len(chunk) >= 2:
                    chunks.append(chunk)
            line = "，".join(chunks)
        paced.append(line)
    return "\n".join(paced)


def gen_background():
    """Generate a dark starry sky background image."""
    img = Image.new("RGB", (W, H), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    random.seed(42)
    for _ in range(300):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        b = random.randint(60, 220)
        sz = 1 if random.random() > 0.1 else 2
        draw.ellipse((x, y, x + sz, y + sz), fill=(b, b, min(255, b + 30)))
    cx, cy = W // 2, H // 2
    pixels = np.array(img, dtype=np.float32)
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            f = max(0, 1.0 - d / (W * 0.55))
            pixels[y, x, 0] += f * 12
            pixels[y, x, 1] += f * 5
            pixels[y, x, 2] += f * 25
    return np.clip(pixels, 0, 255).astype("uint8")


BG = gen_background()


def synthesize_poem(poem_text, voice_name, output_audio_path):
    """Call TTS script to synthesize the poem."""
    vtype, vid = detect_voice_type(voice_name)
    print(f"🎤 声音类型: {vtype} ({vid})")

    if vtype == "system":
        # System voices use flash-realtime model
        model = "flash-realtime"
    else:
        # Cloned/designed voices use vc-realtime, auto-detect
        model = "auto"

    cmd = [
        "python3", TTS_SCRIPT, "generate",
        "--text", poem_text,
        "--voice", vid,
        "--model", model,
        "--output", output_audio_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ TTS 合成失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"✅ 语音合成完成")
    return output_audio_path


def create_video(audio_path, poem_lines, title, output_path):
    """Create video with starry background + subtitles, one line at a time."""
    audio = AudioFileClip(audio_path)
    total_dur = audio.duration
    print(f"🎵 音频时长: {total_dur:.2f}s")

    font = ImageFont.truetype(FONT_PATH, 56)
    font_small = ImageFont.truetype(FONT_PATH, 28)

    display_lines = [l.strip() for l in poem_lines if l.strip()]
    n_lines = len(display_lines)
    print(f"📝 共 {n_lines} 行字幕")

    duration_per_line = total_dur / n_lines

    def make_frame(t):
        frame = BG.copy()
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Subtle star twinkle
        rng = random.Random(int(t * 10) % 1000)
        for _ in range(20):
            x = rng.randint(0, W - 1)
            y = rng.randint(0, H - 1)
            b = int(150 + 80 * np.sin(t * 3 + x * 0.01))
            img.putpixel((x, y), (b, b, min(255, b + 20)))

        # Title at top
        if title:
            bbox_t = draw.textbbox((0, 0), title, font=font_small)
            tw = bbox_t[2] - bbox_t[0]
            draw.text(((W - tw) // 2, 60), title, font=font_small, fill=(180, 160, 140))

        # Current line
        line_idx = min(int(t / duration_per_line), n_lines - 1)
        text = display_lines[line_idx]

        line_start = line_idx * duration_per_line
        line_end = (line_idx + 1) * duration_per_line
        fade_in = min(1.0, (t - line_start) / 0.3)
        fade_out = min(1.0, (line_end - t) / 0.3)
        alpha = int(min(fade_in, fade_out) * 255)

        r = int(245 * alpha / 255)
        g = int(222 * alpha / 255)
        b = int(179 * alpha / 255)
        color = (r, g, b)
        sr = int(20 * alpha / 255)
        sg = int(15 * alpha / 255)
        sb = int(10 * alpha / 255)
        shadow = (sr, sg, sb)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) // 2
        y = H - 180

        draw.text((x + 4, y + 4), text, font=font, fill=shadow)
        draw.text((x, y), text, font=font, fill=color)

        return np.array(img)

    video = VideoClip(make_frame, duration=total_dur)
    video = video.with_fps(24)
    video = video.with_audio(audio)

    print("🎬 正在渲染视频...")
    video.write_videofile(
        output_path, codec="libx264", audio_codec="aac",
        fps=24, preset="medium", logger="bar",
    )
    print(f"✅ 视频已保存: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Poetry Recitation Video Generator")
    parser.add_argument("--poem", required=True, help="Poem text (use \\n for line breaks)")
    parser.add_argument("--title", default="", help="Poem title (shown at top)")
    parser.add_argument("--voice", default=None, help="Voice: cloned name or system voice (cherry/serena/ethan/chelsie)")
    parser.add_argument("--output", default=None, help="Output video path")
    args = parser.parse_args()

    # Determine voice
    voice = args.voice
    if not voice:
        voice = get_default_voice()
        if not voice:
            print("❌ 没有可用的克隆声音，请先用 TTS 技能克隆声音", file=sys.stderr)
            sys.exit(1)
        print(f"🎤 使用默认声音: {voice}")

    # Normalize \n literals to actual newlines
    poem_text = args.poem.replace("\\n", "\n")

    # Output path
    os.makedirs(DEFAULT_AUDIO_DIR, exist_ok=True)
    safe_title = args.title or "poem"
    safe_title = "".join(c for c in safe_title if c.isalnum() or c in " _-") or "poem"
    output = args.output or os.path.join(DEFAULT_AUDIO_DIR, f"{safe_title}_朗诵.mp4")

    # Step 1: Synthesize audio with pacing
    paced_text = add_pacing(poem_text)
    audio_path = os.path.join(DEFAULT_AUDIO_DIR, f"{safe_title}_朗诵.wav")
    print(f"🔊 正在合成语音 (声音: {voice})...")
    synthesize_poem(paced_text, voice, audio_path)

    # Step 2: Create video with clean poem lines
    poem_lines = [l.strip() for l in poem_text.split("\n") if l.strip()]
    create_video(audio_path, poem_lines, args.title, output)
    print(f"\n🎉 完成！视频: {output}")


if __name__ == "__main__":
    main()
