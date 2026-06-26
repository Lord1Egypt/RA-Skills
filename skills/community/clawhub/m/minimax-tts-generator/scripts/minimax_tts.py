#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax TTS (Text-to-Speech) Tool

Supports two TTS APIs:
- speech-2.6 series: OpenAI-compatible /v1/audio/speech endpoint (simple: model/input/voice)
- speech-2.8-hd: MiniMax native /v1/t2a_v2 endpoint (complex: voice_setting/audio_setting)

Usage:
    python3 minimax_tts.py "your text"                         # basic TTS
    python3 minimax_tts.py "text" --voice female-shaonv       # with voice
    python3 minimax_tts.py "text" --speed 1.5                 # with speed
    python3 minimax_tts.py "text" --output speech.mp3          # save to file
    python3 minimax_tts.py --list-voices                       # list all voices
    python3 minimax_tts.py --segments segments.json --output combined.mp3
    python3 minimax_tts.py tools
"""

import os
import sys
import json
import argparse
import base64
import time
import shutil
import subprocess
import requests

API_HOST = 'api.minimaxi.com'
ENDPOINT_SIMPLE = '/v1/audio/speech'   # speech-2.6 series (OpenAI-compatible)
ENDPOINT_NATIVE = '/v1/t2a_v2'        # speech-2.8-hd series

# Default save directory
DEFAULT_SAVE_DIR = os.path.expanduser('~/.openclaw/workspace/tmp')

# Built-in voice list (verified for speech-2.8-hd)
# Note: Different models use different voice ID formats
# speech-2.8-hd / speech-02-hd: uses these IDs
# speech-2.6 series: uses same IDs but API endpoint is different
BUILTIN_VOICES = {
    'female-tianmei': '甜美女声',
    'female-shaonv': '少女音',
    'female-yujie': '御姐音色',
    'female-chengshu': '成熟女性',
    'male-qn-qingse': '青年男声（青涩）',
    'male-qn-jingying': '青年男声（精英）',
    'male-qn-badao': '青年男声（霸道）',
    'male-qn-daxuesheng': '青年大学生',
}


def get_api_key():
    """Get API key from environment or skill config."""
    key = os.environ.get('MINIMAX_API_KEY')
    if key:
        return key

    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            entries = config.get('skills', {}).get('entries', {})
            key = entries.get('minimax-tts', {}).get('apiKey')
            if key:
                return key
        except Exception:
            pass
    return None


def get_api_host():
    """Get API host from environment variable."""
    return os.environ.get('MINIMAX_API_HOST', f'https://{API_HOST}')


def make_request_simple(data: dict) -> bytes:
    """Make request to MiniMax TTS speech-2.6 API (OpenAI-compatible). Returns binary audio."""
    key = get_api_key()
    if not key:
        raise Exception(
            'MINIMAX_API_KEY not set. '
            'Set via environment or openclaw config: '
            'openclaw config set skills.entries.minimax-tts.apiKey "sk-your-key"'
        )

    host = get_api_host()
    url = f'{host}{ENDPOINT_SIMPLE}'
    headers = {
        'Authorization': f'Bearer {key}'
    }
    response = requests.post(url, json=data, headers=headers, timeout=120)
    response.raise_for_status()

    # speech-2.6 returns binary audio directly
    if response.headers.get('Content-Type', '').startswith('audio/'):
        return response.content

    # If JSON, check for error
    resp_json = response.json()
    base_resp = resp_json.get('base_resp', {})
    status_code = base_resp.get('status_code', 0)
    if status_code != 0:
        raise Exception(f"API error {status_code}: {base_resp.get('status_msg', 'Unknown error')}")

    raise Exception('Unexpected response format from speech-2.6 API')


def make_request_native(data: dict) -> dict:
    """Make request to MiniMax TTS speech-2.8 API (native format). Returns JSON response."""
    key = get_api_key()
    if not key:
        raise Exception(
            'MINIMAX_API_KEY not set. '
            'Set via environment or openclaw config: '
            'openclaw config set skills.entries.minimax-tts.apiKey "sk-your-key"'
        )

    host = get_api_host()
    url = f'{host}{ENDPOINT_NATIVE}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}'
    }
    response = requests.post(url, json=data, headers=headers, timeout=120)
    response.raise_for_status()
    resp_json = response.json()

    base_resp = resp_json.get('base_resp', {})
    status_code = base_resp.get('status_code', 0)
    if status_code != 0:
        raise Exception(f"API error {status_code}: {base_resp.get('status_msg', 'Unknown error')}")

    return resp_json


def generate_speech(
    text: str,
    model: str = "speech-2.8-hd",
    voice: str = "female-tianmei",
    speed: float = 1.0,
    pitch: int = 0,
    audio_format: str = "mp3",
    output_path: str = None
) -> dict:
    """
    Generate speech from text using MiniMax TTS API.

    Supports two model series:
    - speech-2.6-hd / speech-2.6-turbo: OpenAI-compatible API (simpler, Coding Plan key NOT supported)
    - speech-2.8-hd: MiniMax native API with voice_setting/audio_setting
    """
    if not text:
        return {'error': 'Missing required parameter: text'}

    if len(text) > 10000:
        return {'error': 'Text exceeds 10000 character limit per request'}

    # Determine which API to use based on model
    if model.startswith('speech-2.6'):
        audio_bytes = _generate_speech_simple(text, model, voice, speed, audio_format)
    else:
        audio_bytes = _generate_speech_native(text, model, voice, speed, pitch, audio_format)

    # Determine save path
    if not output_path:
        os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)
        timestamp = int(time.time() * 1000)
        output_path = os.path.join(DEFAULT_SAVE_DIR, f"tts_{timestamp}.mp3")

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    # Save to file
    with open(output_path, 'wb') as f:
        f.write(audio_bytes)

    return {
        'success': True,
        'file': output_path,
        'model': model,
        'voice': voice,
        'speed': int(speed),
        'text_chars': len(text),
        'audio_format': audio_format,
    }


def _generate_speech_simple(text: str, model: str, voice: str, speed: float, audio_format: str) -> bytes:
    """Use OpenAI-compatible speech-2.6 API."""
    data = {
        'model': model,
        'input': text,
        'voice': voice,
    }
    return make_request_simple(data)


def _generate_speech_native(text: str, model: str, voice: str, speed: float, pitch: int, audio_format: str) -> bytes:
    """Use MiniMax native speech-2.8 API."""
    data = {
        'model': model,
        'text': text,
        'voice_setting': {
            'voice_id': voice,
            'speed': int(speed),
            'vol': 1,
            'pitch': int(pitch),
        },
        'audio_setting': {
            'sample_rate': 32000,
            'bitrate': 128000,
            'format': audio_format,
            'channel': 1,
        },
        'stream': False,
        'subtitle_enable': False,
        'output_format': 'hex',
    }

    response = make_request_native(data)
    resp_data = response.get('data', {})
    if isinstance(resp_data, dict):
        hex_data = resp_data.get('audio', '')
    else:
        hex_data = response.get('audio', '') or str(resp_data)
    if not hex_data:
        raise Exception('No audio data in API response')

    return bytes.fromhex(hex_data)


def generate_speech_from_segments(
    segments: list,
    model: str = "speech-2.8-hd",
    audio_format: str = "mp3",
    output_path: str = None,
    crossfade_ms: int = 200
) -> dict:
    """Generate audio from multiple segments (for multi-voice content)."""
    if not segments:
        return {'error': 'No segments provided'}

    try:

        os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)
        temp_files = []

        for i, seg in enumerate(segments):
            text = seg.get('text', '')
            voice = seg.get('voice', 'female-tianmei')
            speed = seg.get('speed', 1.0)

            if not text:
                continue

            print(f"Generating segment {i + 1}/{len(segments)}: {text[:50]}...")

            result = generate_speech(
                text=text,
                model=model,
                voice=voice,
                speed=speed,
                pitch=0,
                audio_format='wav',
                output_path=None
            )

            if not result.get('success'):
                return {'error': f"Segment {i + 1} failed: {result.get('error')}"}

            temp_files.append(result['file'])

        # Merge audio files
        if len(temp_files) == 1:
            final_path = output_path or os.path.join(
                DEFAULT_SAVE_DIR, f"tts_{int(time.time()*1000)}.{audio_format}"
            )
            shutil.copy(temp_files[0], final_path)
            os.remove(temp_files[0])
        else:
            final_path = output_path or os.path.join(
                DEFAULT_SAVE_DIR, f"tts_{int(time.time()*1000)}.{audio_format}"
            )

            try:
                concat_file = os.path.join(DEFAULT_SAVE_DIR, 'concat_list.txt')
                with open(concat_file, 'w') as f:
                    for tf in temp_files:
                        f.write(f"file '{tf}'\n")

                if audio_format == 'mp3':
                    subprocess.run(
                        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
                         '-codec:a', 'libmp3lame', '-q:a', '2', final_path],
                        check=True, capture_output=True
                    )
                else:
                    subprocess.run(
                        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, final_path],
                        check=True, capture_output=True
                    )

                os.remove(concat_file)
                for tf in temp_files:
                    if os.path.exists(tf):
                        os.remove(tf)

            except FileNotFoundError:
                return {
                    'error': 'ffmpeg not found. Install ffmpeg to merge audio segments, or use single-segment TTS.'
                }
            except subprocess.CalledProcessError as e:
                return {'error': f'Failed to merge audio: {e.stderr.decode() if e.stderr else str(e)}'}

        return {
            'success': True,
            'file': final_path,
            'segments_count': len(segments),
            'model': model,
            'audio_format': audio_format,
        }

    except Exception as e:
        return {'error': str(e)}


def list_voices() -> dict:
    """List all available voices."""
    return {
        'success': True,
        'voices': BUILTIN_VOICES,
        'note': 'This is a partial list. Use --list-voices from the MiniMax platform for full list.'
    }


def list_tools() -> dict:
    """Return available tools in OpenClaw skill format."""
    return {
        'tools': [
            {
                'name': 'minimax_tts',
                'description': 'Text-to-speech generation using MiniMax API - converts text into natural-sounding speech',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'text': {
                            'type': 'string',
                            'description': 'Text to convert to speech (max 10000 chars per request)'
                        },
                        'model': {
                            'type': 'string',
                            'enum': ['speech-2.8-hd', 'speech-2.6-hd', 'speech-02-hd'],
                            'default': 'speech-2.8-hd',
                            'description': 'TTS model: speech-2.8-hd (recommended), speech-2.6-hd (Coding Plan NOT supported), speech-02-hd (compact HD)'
                        },
                        'voice': {
                            'type': 'string',
                            'default': 'female-tianmei',
                            'description': 'Voice ID: female-tianmei, female-shaonv, female-yujie, female-chengshu, male-qn-qingse, male-qn-jingying, male-qn-badao, male-qn-daxuesheng'
                        },
                        'speed': {
                            'type': 'number',
                            'default': 1.0,
                            'minimum': 0.5,
                            'maximum': 2.0,
                            'description': 'Speech speed, range 0.5-2.0'
                        },
                        'pitch': {
                            'type': 'number',
                            'default': 0,
                            'minimum': -12,
                            'maximum': 12,
                            'description': 'Pitch adjustment, range -12 to 12 (speech-2.8 models)'
                        },
                        'audio_format': {
                            'type': 'string',
                            'enum': ['mp3', 'wav', 'pcm'],
                            'default': 'mp3',
                            'description': 'Output audio format'
                        },
                        'output_path': {
                            'type': 'string',
                            'description': 'Save audio to this file path'
                        }
                    },
                    'required': ['text']
                }
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description='MiniMax Text-to-Speech Generation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "你好，世界"
  %(prog)s "Hello world" --voice female-shaonv
  %(prog)s "快速播报" --speed 1.5 --output speech.mp3
  %(prog)s --list-voices
  %(prog)s --segments segments.json --output combined.mp3
  %(prog)s tools

Models:
  speech-2.8-hd    - Recommended, high quality with emotion control (native API)
  speech-2.6-hd    - OpenAI-compatible API (Coding Plan key NOT supported for 2.6)
  speech-02-hd     - Compact HD voice (native API)
        '''
    )

    parser.add_argument('text', nargs='?', help='Text to convert to speech')
    parser.add_argument('--model', '-m', default='speech-2.8-hd',
                        choices=['speech-2.8-hd', 'speech-2.6-hd', 'speech-02-hd'],
                        help='TTS model (default: speech-2.8-hd)')
    parser.add_argument('--voice', '-v', default='female-tianmei',
                        help='Voice ID (default: female-tianmei)')
    parser.add_argument('--speed', type=float, default=1.0,
                        help='Speech speed 0.5-2.0 (default: 1.0)')
    parser.add_argument('--pitch', type=float, default=0,
                        help='Pitch adjustment -12 to 12 (default: 0, speech-2.8 only)')
    parser.add_argument('--audio-format', default='mp3',
                        choices=['mp3', 'wav', 'pcm'],
                        help='Output audio format (default: mp3)')
    parser.add_argument('--output', '-o',
                        help='Save audio to this file path')
    parser.add_argument('--list-voices', action='store_true',
                        help='List all available voices')
    parser.add_argument('--segments',
                        help='Path to segments.json for multi-segment generation')
    parser.add_argument('--crossfade', type=int, default=200,
                        help='Crossfade duration in ms between segments (default: 200)')
    parser.add_argument('--tools', action='store_true',
                        help='List available tools in JSON format')

    args = parser.parse_args()

    if args.tools:
        print(json.dumps(list_tools(), ensure_ascii=False, indent=2))
        return

    if args.list_voices:
        print(json.dumps(list_voices(), ensure_ascii=False, indent=2))
        return

    if args.segments:
        if not os.path.exists(args.segments):
            print(f"Error: segments file not found: {args.segments}")
            sys.exit(1)
        with open(args.segments) as f:
            segments = json.load(f)
        result = generate_speech_from_segments(
            segments=segments,
            model=args.model,
            audio_format=args.audio_format,
            output_path=args.output,
            crossfade_ms=args.crossfade
        )
    elif args.text:
        result = generate_speech(
            text=args.text,
            model=args.model,
            voice=args.voice,
            speed=args.speed,
            pitch=args.pitch,
            audio_format=args.audio_format,
            output_path=args.output
        )
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == '__main__':
    main()
