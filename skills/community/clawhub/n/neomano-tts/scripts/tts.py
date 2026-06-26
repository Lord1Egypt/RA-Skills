#!/usr/bin/env python3
"""ElevenLabs TTS helper.

Writes an audio file (mp3 by default) using ElevenLabs Text-to-Speech API.

Env:
  ELEVENLABS_API_KEY (required)

Example:
  python3 tts.py --text "hola" --out /tmp/hola.mp3
"""

import argparse
import json
import os
import sys
import urllib.request

DEFAULT_VOICE_ID = None  # require --voice-id or ELEVENLABS_VOICE_ID
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID)
    ap.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    ap.add_argument("--stability", type=float, default=0.5)
    ap.add_argument("--similarity-boost", type=float, default=0.75)
    args = ap.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set", file=sys.stderr)
        return 2

    if not args.voice_id:
        print("ERROR: missing voice id (set ELEVENLABS_VOICE_ID or pass --voice-id)", file=sys.stderr)
        return 2

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}"

    payload = {
        "text": args.text,
        "model_id": args.model_id,
        "voice_settings": {
            "stability": args.stability,
            "similarity_boost": args.similarity_boost,
        },
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        },
    )

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            audio = resp.read()
    except Exception as e:
        print(f"ERROR: ElevenLabs request failed: {e}", file=sys.stderr)
        return 1

    with open(out_path, "wb") as f:
        f.write(audio)

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
