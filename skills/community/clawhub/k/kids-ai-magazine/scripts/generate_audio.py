#!/usr/bin/env python3
"""
Generate TTS audio for each story using edge-tts (Microsoft Azure free TTS).
Usage: python3 generate_audio.py --voice zh-CN-XiaoxiaoNeural --output-dir ./output
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys

def generate_audio(text, output_path, voice="zh-CN-XiaoxiaoNeural"):
    """Generate audio using edge-tts CLI."""
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--text", text,
        "--write-media", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error generating {output_path}: {result.stderr}")
        return False
    size = os.path.getsize(output_path)
    print(f"  ✅ {output_path} ({size} bytes)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio for kids magazine stories")
    parser.add_argument("--stories", required=True, help="Path to stories JSON file")
    parser.add_argument("--voice", default="zh-CN-XiaoxiaoNeural", help="Edge-TTS voice name")
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.stories, "r", encoding="utf-8") as f:
        stories = json.load(f)

    print(f"Generating audio for {len(stories)} stories with voice: {args.voice}")
    for i, story in enumerate(stories, 1):
        title = story.get("title", f"Story {i}")
        text = story.get("tts_text", story.get("text", ""))
        if not text:
            print(f"  ⚠️ Story {i} ({title}) has no text, skipping")
            continue
        output_path = os.path.join(args.output_dir, f"story{i}.mp3")
        print(f"  📖 Story {i}: {title}")
        generate_audio(text, output_path, args.voice)

    print(f"\n✅ Done! Audio files in {args.output_dir}")

if __name__ == "__main__":
    main()
