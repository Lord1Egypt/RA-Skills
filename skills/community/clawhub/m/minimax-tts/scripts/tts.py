#!/usr/bin/env python3
"""
MiniMax TTS Script — HTTP REST API
Usage: uv run python tts.py --text "Hello" --voice English_expressive_narrator --model speech-2.8-hd --output hello.mp3
"""

import argparse
import os
import sys
import subprocess
import tempfile
import requests
import json

DEFAULT_API_URL = "https://api.minimax.io/v1/t2a_v2"
MODEL_DEFAULTS = {
    "model": "speech-2.8-hd",
    "voice_id": "English_expressive_narrator",
    "speed": 1.0,
    "vol": 1,
    "pitch": 0,
    "language_boost": "auto",
    "output_format": "hex",
    "audio_format": "mp3",
    "sample_rate": 32000,
    "bitrate": 128000,
}


def parse_args():
    p = argparse.ArgumentParser(description="MiniMax TTS via HTTP REST API")
    p.add_argument("--text", required=True, help="Text to synthesize")
    p.add_argument("--model", default=MODEL_DEFAULTS["model"], help=f"Model (default: {MODEL_DEFAULTS['model']})")
    p.add_argument("--voice", dest="voice_id", default=MODEL_DEFAULTS["voice_id"], help=f"Voice ID (default: {MODEL_DEFAULTS['voice_id']})")
    p.add_argument("--speed", type=float, default=MODEL_DEFAULTS["speed"], help="Speed 0.5-2.0 (default: 1.0)")
    p.add_argument("--pitch", type=float, default=MODEL_DEFAULTS["pitch"], help="Pitch -3 to 3 (default: 0)")
    p.add_argument("--vol", type=float, default=MODEL_DEFAULTS["vol"], help="Volume 0-10 (default: 1)")
    p.add_argument("--language_boost", default=MODEL_DEFAULTS["language_boost"], help="Language boost (default: auto)")
    p.add_argument("--stream", action="store_true", help="Enable streaming mode")
    p.add_argument("--output_format", default=MODEL_DEFAULTS["output_format"], choices=["hex", "raw"], help="Output format: hex or raw bytes (default: hex)")
    p.add_argument("--format", dest="audio_format", default=MODEL_DEFAULTS["audio_format"], choices=["mp3", "wav", "pcm"], help=f"Audio format (default: {MODEL_DEFAULTS['audio_format']})")
    p.add_argument("--sample_rate", type=int, default=MODEL_DEFAULTS["sample_rate"], choices=[16000, 24000, 32000, 48000], help=f"Sample rate (default: {MODEL_DEFAULTS['sample_rate']})")
    p.add_argument("--bitrate", type=int, default=MODEL_DEFAULTS["bitrate"], choices=[32000, 64000, 128000], help=f"Bitrate (default: {MODEL_DEFAULTS['bitrate']})")
    p.add_argument("--output", default="minimax_tts_output.mp3", help="Output file path")
    p.add_argument("--api_url", default=DEFAULT_API_URL, help=f"API URL (default: {DEFAULT_API_URL})")
    p.add_argument("--api_key", help="API key (reads MINIMAX_API_KEY env if not set)")
    return p.parse_args()


def get_api_key(key):
    if key:
        return key
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        raise ValueError("No API key: set --api_key or MINIMAX_API_KEY env var")
    return key


def build_payload(args):
    return {
        "model": args.model,
        "text": args.text,
        "stream": args.stream,
        "language_boost": args.language_boost,
        "output_format": args.output_format,
        "voice_setting": {
            "voice_id": args.voice_id,
            "speed": args.speed,
            "vol": args.vol,
            "pitch": args.pitch,
        },
        "audio_setting": {
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "format": args.audio_format,
            "channel": 1,
        },
    }


def hex_to_file(hex_str, output_path):
    audio_bytes = bytes.fromhex(hex_str)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)


def raw_to_file(data, output_path):
    with open(output_path, "wb") as f:
        f.write(data)


def synthesize(args):
    api_key = get_api_key(args.api_key)
    payload = build_payload(args)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"[MiniMax TTS] Model: {args.model} | Voice: {args.voice_id} | Format: {args.audio_format} | Sample Rate: {args.sample_rate}")
    print(f"[MiniMax TTS] Text ({len(args.text)} chars): {args.text[:80]}{'...' if len(args.text) > 80 else ''}")

    resp = requests.post(args.api_url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

    if args.stream:
        # SSE stream — collect hex chunks and decode
        chunks = []
        for line in resp.text.strip().split("\n"):
            if not line.startswith("data:"):
                continue
            try:
                data = json.loads(line[5:].strip())
                if data.get("data", {}).get("audio"):
                    chunks.append(data["data"]["audio"])
                if data.get("is_final"):
                    break
            except (json.JSONDecodeError, KeyError):
                continue

        if not chunks:
            raise RuntimeError("No audio chunks received in stream response")
        hex_str = "".join(chunks)
        print(f"[MiniMax TTS] Received {len(chunks)} chunks")
    else:
        result = resp.json()
        if result.get("base_resp", {}).get("status_code") != 0:
            raise RuntimeError(f"API error: {result.get('base_resp')}")
        audio_data = result.get("data", {}).get("audio")
        if not audio_data:
            raise RuntimeError("No audio in response")
        hex_str = audio_data
        extra = result.get("extra_info", {})
        print(f"[MiniMax TTS] Audio size: {extra.get('audio_size', '?')} bytes | Duration: {extra.get('audio_length', '?')}ms | Chars: {extra.get('usage_characters', '?')}")

    output_path = args.output
    hex_to_file(hex_str, output_path)
    print(f"[MiniMax TTS] Saved: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path


if __name__ == "__main__":
    try:
        args = parse_args()
        path = synthesize(args)
        print(f"Done: {path}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
