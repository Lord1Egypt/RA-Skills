#!/usr/bin/env python3
"""
Xiaomi MiMo-V2-TTS - Text-to-Speech synthesis script.

API: https://api.xiaomimimo.com/v1/chat/completions
Model: mimo-v2-tts

MiMo TTS uses Chat Completions format with special requirements:
  - No system role allowed
  - Must include assistant role (text to synthesize)
  - user role = style instructions
  - assistant role = text to be spoken
  - Returns base64 audio in choices[0].message.audio.data

Usage:
    python3 mimo_tts.py --text "Hello world" --output /tmp/output.mp3
    python3 mimo_tts.py --text "Today is great" --output /tmp/output.mp3 --style "cheerful tone"
    python3 mimo_tts.py --text "Twinkle twinkle" --output /tmp/output.mp3 --style "sing it"
"""

import argparse
import base64
import json
import os
import sys

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


BASE_URL = "https://api.xiaomimimo.com/v1"
DEFAULT_FORMAT = "mp3"
DEFAULT_SPEED = 1.0


def get_api_key(cli_key: str = None) -> str:
    """Get API key from CLI arg or MIMO_API_KEY env var."""
    if cli_key:
        return cli_key
    key = os.environ.get("MIMO_API_KEY")
    if key:
        return key
    print("Error: No API key found.")
    print("  Set MIMO_API_KEY env var or pass --api-key")
    print("  Get your key at: https://platform.xiaomimimo.com")
    sys.exit(1)


def synthesize_speech(
    text: str,
    output_path: str,
    api_key: str,
    style: str = None,
    speed: float = DEFAULT_SPEED,
    response_format: str = DEFAULT_FORMAT,
) -> str:
    """
    Call MiMo-V2-TTS API to synthesize speech.

    Args:
        text: Text to synthesize
        output_path: Path to save the audio file
        api_key: MiMo API key
        style: Optional style description (natural language)
        speed: Speech rate 0.5-2.0
        response_format: Audio format (mp3/wav/pcm/opus/flac)

    Returns:
        Path to the saved audio file
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []

    # Style control via user message
    if style:
        messages.append({"role": "user", "content": style})
    else:
        messages.append({"role": "user", "content": "Please read the following aloud"})

    # Text to synthesize goes in assistant message
    messages.append({"role": "assistant", "content": text})

    payload = {
        "model": "mimo-v2-tts",
        "messages": messages,
    }

    # Audio parameters
    audio_params = {"format": response_format}
    if speed != 1.0:
        audio_params["speed"] = speed
    payload["audio"] = audio_params

    url = f"{BASE_URL}/chat/completions"
    text_preview = text[:80] + ("..." if len(text) > 80 else "")
    print(f"Synthesizing: {text_preview}")
    if style:
        print(f"  Style: {style}")
    print(f"  Format: {response_format}")

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)

        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices", [])
            if not choices:
                print(f"Error: Empty choices in response")
                sys.exit(1)

            msg = choices[0].get("message", {})
            audio = msg.get("audio", {})
            audio_data = audio.get("data")

            if audio_data:
                audio_bytes = base64.b64decode(audio_data)
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
                size_kb = len(audio_bytes) / 1024
                audio_id = audio.get("id", "unknown")

                usage = data.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)

                print(f"Success! Saved to {output_path} ({size_kb:.1f} KB)")
                if total_tokens:
                    print(f"  Tokens used: {total_tokens}")
                return output_path
            else:
                content = msg.get("content", "")
                if content:
                    print(f"Warning: Got text instead of audio: {content[:200]}")
                else:
                    print(f"Error: No audio data in response")
                sys.exit(1)

        else:
            error_text = resp.text[:500]
            print(f"Error ({resp.status_code}): {error_text}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("Error: Request timed out (120s). Try shorter text.")
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Xiaomi MiMo-V2-TTS text-to-speech synthesis"
    )
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--output", required=True, help="Output audio file path")
    parser.add_argument(
        "--style",
        default=None,
        help="Style description in natural language (e.g. 'cheerful tone', 'sing it')",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help=f"Speech rate 0.5-2.0 (default {DEFAULT_SPEED})",
    )
    parser.add_argument(
        "--format",
        dest="audio_format",
        default=DEFAULT_FORMAT,
        choices=["mp3", "wav", "pcm", "opus", "flac"],
        help=f"Output format (default {DEFAULT_FORMAT})",
    )
    parser.add_argument("--api-key", default=None, help="MiMo API Key")

    args = parser.parse_args()
    api_key = get_api_key(args.api_key)

    synthesize_speech(
        text=args.text,
        output_path=args.output,
        api_key=api_key,
        style=args.style,
        speed=args.speed,
        response_format=args.audio_format,
    )


if __name__ == "__main__":
    main()
