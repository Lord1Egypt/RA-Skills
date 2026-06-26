#!/usr/bin/env python3
"""
MiniMax TTS - Text-to-Speech via MiniMax API
"""

import os
import sys
import json
import argparse
import requests
import subprocess

API_BASE = "https://api.minimaxi.com"
DEFAULT_VOICE = "Chinese (Mandarin)_Warm_Girl"
DEFAULT_MODEL = "speech-2.8-turbo"
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
SKILL_DIR = os.path.join(WORKSPACE_DIR, "skills", "minimax-tts-cn")
DEFAULT_OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "generated", "tmp")
ENV_FILE = os.path.join(SKILL_DIR, ".env")

def load_env_file(path):
    """Load KEY=VALUE pairs from .env file (simple format only)."""
    env = {}
    if not os.path.exists(path):
        return env

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env[key] = value
    except Exception as e:
        print(f"Warning: Failed to read .env file: {e}", file=sys.stderr)

    return env


def get_api_key():
    """Get API Key: check env var first, then skill .env file."""
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key

    file_env = load_env_file(ENV_FILE)
    key = file_env.get("MINIMAX_API_KEY")
    if key:
        return key

    print("Error: MINIMAX_API_KEY not set", file=sys.stderr)
    print(f"Set the environment variable, or write MINIMAX_API_KEY=your-key in {ENV_FILE}", file=sys.stderr)
    sys.exit(1)

def get_voice_list(api_key):
    """Fetch and print available voice list."""
    url = f"{API_BASE}/v1/get_voice"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"voice_type": "all"}

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()

        print("Available voices:\n")

        if "system_voice" in result and result["system_voice"]:
            print("=== System Voices ===")
            for v in result["system_voice"]:
                print(f"  {v.get('voice_id')}: {v.get('voice_name')}")

        if "voice_cloning" in result and result["voice_cloning"]:
            print("\n=== Cloned Voices ===")
            for v in result["voice_cloning"]:
                print(f"  {v.get('voice_id')}")

        if "voice_generation" in result and result["voice_generation"]:
            print("\n=== Generated Voices ===")
            for v in result["voice_generation"]:
                print(f"  {v.get('voice_id')}")

    except Exception as e:
        print(f"Failed to fetch voice list: {e}", file=sys.stderr)
        sys.exit(1)

def text_to_speech(text, api_key, model=DEFAULT_MODEL, voice=DEFAULT_VOICE,
                   speed=1.0, format="mp3", output_file=None, pause=0):
    """Call TTS API and save audio to file."""
    url = f"{API_BASE}/v1/t2a_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Handle pause: insert silence markers between sentences
    if pause > 0:
        import re
        text = re.sub(r'([。！？\.])([^<])', r'\1<#' + str(pause) + '#>\2', text)

    data = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice,
            "speed": speed,
            "vol": 1,
            "pitch": 0
        },
        "audio_setting": {
            "format": format,
            "sample_rate": 32000,
            "bitrate": 128000,
            "channel": 1
        }
    }

    try:
        print(f"Generating speech...", file=sys.stderr)
        resp = requests.post(url, headers=headers, json=data, timeout=120)
        resp.raise_for_status()
        result = resp.json()

        if result.get("base_resp", {}).get("status_code") != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
            print(f"API error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        audio_data = result.get("data", {}).get("audio")
        if not audio_data:
            print("Error: No audio data received", file=sys.stderr)
            sys.exit(1)

        # Decode hex-encoded audio bytes
        audio_bytes = bytes.fromhex(audio_data)

        # Determine output file path
        if not output_file:
            os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
            output_file = os.path.join(DEFAULT_OUTPUT_DIR, f"tts_output.{format}")
        else:
            output_file = os.path.expanduser(output_file)
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        # Get audio info
        extra = result.get("extra_info", {})
        duration_ms = extra.get("audio_length", 0)
        duration_sec = duration_ms / 1000 if duration_ms else 0

        print(f"✅ Audio saved to: {output_file}", file=sys.stderr)
        print(f"   Duration: {duration_sec:.2f}s", file=sys.stderr)
        print(f"   Format: {format}", file=sys.stderr)

        return output_file

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="MiniMax TTS - Text to Speech")
    parser.add_argument("text", nargs="?", help="Text to synthesize")
    parser.add_argument("--list-voices", "-l", action="store_true", help="List all available voices")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, help=f"Voice ID (default: {DEFAULT_VOICE})")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="Speech speed (default: 1.0)")
    parser.add_argument("--pause", "-p", type=float, default=0, help="Pause between sentences in seconds (default: 0)")
    parser.add_argument("--format", "-f", default="mp3", help="Audio format (default: mp3)")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    api_key = get_api_key()

    if args.list_voices:
        get_voice_list(api_key)
        return

    if not args.text:
        parser.print_help()
        print("\nExamples:")
        print(f"  {sys.argv[0]} \"Hello world\"")
        print(f"  {sys.argv[0]} \"Test\" --voice Chinese_Female_Adult --output test.mp3")
        print(f"  {sys.argv[0]} -l  # List all voices")
        sys.exit(1)

    output_file = text_to_speech(
        text=args.text,
        api_key=api_key,
        model=args.model,
        voice=args.voice,
        speed=args.speed,
        format=args.format,
        output_file=args.output,
        pause=args.pause
    )

    # Output file path (for use by other tools)
    print(output_file)

if __name__ == "__main__":
    main()
