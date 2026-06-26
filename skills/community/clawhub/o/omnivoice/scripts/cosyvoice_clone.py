#!/usr/bin/env python3
"""CosyVoice2 TTS with voice cloning via SiliconFlow API.

Usage:
    # With preset voice:
    python cosyvoice_clone.py --text "你好" --voice alex

    # With voice cloning (reference audio):
    python cosyvoice_clone.py --text "你好" --ref /path/to/reference.wav --ref-text "参考音频中说的话"

    # With voice cloning (URL):
    python cosyvoice_clone.py --text "你好" --ref-url "https://example.com/voice.wav" --ref-text "参考音频中说的话"

Requires: SF_API_KEY environment variable
"""

import argparse
import base64
import os
import sys
import json
import requests
from pathlib import Path


PRESET_VOICES = [
    "alex", "anna", "bella", "benjamin", "charles", "claire", "david", "diana"
]

MODEL = "FunAudioLLM/CosyVoice2-0.5B"
API_URL = "https://api.siliconflow.cn/v1/audio/speech"


def parse_args():
    parser = argparse.ArgumentParser(description="CosyVoice2 TTS with voice cloning")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--voice", default=None, choices=PRESET_VOICES,
                        help="Preset voice name (mutually exclusive with --ref)")
    parser.add_argument("--ref", default=None, help="Path to reference audio file for voice cloning")
    parser.add_argument("--ref-url", default=None, help="URL to reference audio for voice cloning")
    parser.add_argument("--ref-text", default="", help="Transcript of the reference audio")
    parser.add_argument("--output", default="/tmp/mimo-v2-tts/cosyvoice_output.wav",
                        help="Output wav path")
    parser.add_argument("--format", default="wav", choices=["mp3", "opus", "wav", "pcm"],
                        help="Output audio format")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed (0.25-4.0)")
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("SF_API_KEY")
    if not api_key:
        print("SF_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "input": args.text,
        "response_format": args.format,
        "stream": False,
        "speed": args.speed,
    }

    # Voice cloning via reference audio
    if args.ref or args.ref_url:
        if args.ref:
            audio_path = Path(args.ref)
            if not audio_path.exists():
                print(f"Reference audio not found: {args.ref}", file=sys.stderr)
                sys.exit(1)
            audio_bytes = audio_path.read_bytes()
            # Detect mime type
            suffix = audio_path.suffix.lower().lstrip(".")
            if suffix in ("wav", "wave"):
                mime = "wav"
            elif suffix == "mp3":
                mime = "mp3"
            elif suffix == "opus":
                mime = "opus"
            elif suffix in ("m4a", "aac"):
                mime = "m4a"
            else:
                mime = "wav"
            audio_b64 = f"data:audio/{mime};base64,{base64.b64encode(audio_bytes).decode()}"
            payload["references"] = [{"audio": audio_b64, "text": args.ref_text}]
        else:
            payload["references"] = [{"audio": args.ref_url, "text": args.ref_text}]
    elif args.voice:
        payload["voice"] = f"{MODEL}:{args.voice}"
    else:
        # Default voice
        payload["voice"] = f"{MODEL}:alex"

    resp = requests.post(API_URL, headers=headers, json=payload, stream=True, timeout=120)

    if resp.status_code != 200:
        print(f"API error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)

    print(output_path)


if __name__ == "__main__":
    main()
