#!/usr/bin/env python3
"""
MOSS-TTS: Text-to-Speech via MOSI Studio API

Usage:
  python3 mosi_tts.py --text "Text to synthesize" --voice-id VOICE_ID --output output.wav
  python3 mosi_tts.py --text "Text to synthesize" --output output.wav  # Use default voice
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library required. Run: pip install requests")
    sys.exit(1)

API_BASE = "https://studio.mosi.cn"
TTS_ENDPOINT = f"{API_BASE}/api/v1/audio/speech"

# Default public voice (阿树 - relaxed, natural)
DEFAULT_VOICE_ID = "2001257729754140672"


def text_to_speech(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: str = None,
    expected_duration: float = None,
    temperature: float = 1.7,
    top_p: float = 0.8,
    top_k: int = 25,
    output: str = "output.wav",
) -> dict:
    """
    Convert text to speech using MOSS-TTS API
    
    Args:
        text: Text to synthesize
        voice_id: Voice ID (public or custom)
        api_key: MOSI API Key (can be set via MOSI_API_KEY env var)
        expected_duration: Expected duration in seconds (0.5-1.5x normal speech rate)
        temperature: Sampling temperature, default 1.7
        top_p: Top-p sampling, default 0.8
        top_k: Top-k sampling, default 25
        output: Output file path
    
    Returns:
        dict: Contains duration_s, usage, etc.
    """
    if not api_key:
        api_key = os.environ.get("MOSI_TTS_API_KEY")

    if not api_key:
        raise ValueError(
            "API key required. "
            "Set MOSI_TTS_API_KEY env var or pass --api-key"
        )
    
    payload = {
        "model": "moss-tts",
        "text": text,
        "voice_id": voice_id,
        "sampling_params": {
            "max_new_tokens": 512,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        },
        "meta_info": True,
    }
    
    if expected_duration:
        payload["expected_duration_sec"] = expected_duration
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    resp = requests.post(TTS_ENDPOINT, json=payload, headers=headers, timeout=120)
    
    if resp.status_code != 200:
        error = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {"error": resp.text}
        raise RuntimeError(f"TTS API error ({resp.status_code}): {error}")
    
    result = resp.json()
    audio_b64 = result.get("audio_data")
    
    if not audio_b64:
        raise RuntimeError("No audio_data in response")
    
    # Write to file
    output_path = Path(output)
    output_path.write_bytes(base64.b64decode(audio_b64))
    
    return {
        "output_file": str(output_path.absolute()),
        "duration_s": result.get("duration_s"),
        "usage": result.get("usage"),
    }


def main():
    parser = argparse.ArgumentParser(description="MOSS-TTS Text-to-Speech")
    parser.add_argument("--text", "-t", required=True, help="Text to synthesize")
    parser.add_argument("--voice-id", "-v", default=DEFAULT_VOICE_ID, help=f"Voice ID (default: {DEFAULT_VOICE_ID})")
    parser.add_argument(
        "--api-key", "-k",
        help="MOSI API Key (or set MOSI_TTS_API_KEY env)"
    )
    parser.add_argument(
        "--output", "-o",
        default=os.path.expanduser(
            "~/.openclaw/workspace/tts_output.wav"
        ),
        help="Output file path (default: ~/.openclaw/workspace/tts_output.wav)",
    )
    parser.add_argument("--expected-duration", "-d", type=float, help="Expected duration in seconds")
    parser.add_argument("--temperature", type=float, default=1.7, help="Sampling temperature")
    parser.add_argument("--top-p", type=float, default=0.8, help="Top-p sampling")
    parser.add_argument("--top-k", type=int, default=25, help="Top-k sampling")
    
    args = parser.parse_args()
    
    try:
        result = text_to_speech(
            text=args.text,
            voice_id=args.voice_id,
            api_key=args.api_key,
            expected_duration=args.expected_duration,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            output=args.output,
        )
        print(f"Audio saved to: {result['output_file']}")
        print(f"Duration: {result['duration_s']}s")
        if result.get("usage"):
            print(f"Cost: {result['usage'].get('credit_cost', 'N/A')} credits")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
