#!/usr/bin/env python3
"""
Speech-to-Text transcription via SkillBoss API Hub.

Uses SkillBoss API Hub /v1/pilot for automatic STT model routing.

Authentication:
- Set SKILLBOSS_API_KEY environment variable

Usage:
    python transcribe.py <audio_file>

Supports: audio/ogg (opus), audio/mp3, audio/wav, audio/m4a
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.heybossai.com/v1"

SUPPORTED_EXTENSIONS = {
    ".ogg": "audio/ogg",
    ".opus": "audio/ogg",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
}


def get_mime_type(file_path: str) -> str:
    """Determine MIME type from file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    return SUPPORTED_EXTENSIONS.get(ext, "audio/ogg")


def transcribe(file_path: str) -> str:
    """
    Transcribe an audio file using SkillBoss API Hub STT.

    Args:
        file_path: Path to the audio file

    Returns:
        Transcribed text

    Raises:
        FileNotFoundError: If audio file doesn't exist
        RuntimeError: If API call fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    api_key = os.environ.get("SKILLBOSS_API_KEY")
    if not api_key:
        raise RuntimeError("No authentication available. Set SKILLBOSS_API_KEY environment variable.")

    with open(file_path, "rb") as f:
        audio_data = f.read()

    audio_b64 = base64.b64encode(audio_data).decode("utf-8")
    filename = os.path.basename(file_path)

    payload = {
        "type": "stt",
        "inputs": {
            "audio_data": audio_b64,
            "filename": filename,
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        req = urllib.request.Request(
            f"{API_BASE}/pilot",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["result"]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP Error {e.code}: {error_body}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response format: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using SkillBoss API Hub STT"
    )
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    args = parser.parse_args()

    try:
        text = transcribe(args.audio_file)
        print(text)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
