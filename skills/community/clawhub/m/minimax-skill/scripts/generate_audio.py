#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import requests

API_URL = "https://api.minimaxi.com/v1/t2a_v2"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate audio with MiniMax T2A HTTP API")
    parser.add_argument("--text", required=True)
    parser.add_argument("--model", default="speech-2.8-turbo")
    parser.add_argument("--output", required=True)
    parser.add_argument("--voice-id", default=None)
    parser.add_argument("--output-format", default="hex", choices=["hex", "url"])
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise SystemExit("MINIMAX_API_KEY is required")

    payload = {
        "model": args.model,
        "text": args.text,
        "output_format": args.output_format,
    }
    if args.voice_id:
        payload["voice_setting"] = {"voice_id": args.voice_id}

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    audio_hex = data.get("data", {}).get("audio")
    if not audio_hex:
        raise SystemExit(f"No audio returned: {json.dumps(data, ensure_ascii=False)}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(bytes.fromhex(audio_hex))
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
