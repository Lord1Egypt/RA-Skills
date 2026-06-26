#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CACHE_DIR = Path('/root/.openclaw/tts/cache')
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_VOICE = os.environ.get('OPENCLAW_EDGE_TTS_VOICE', 'en-IE-ConnorNeural')
DEFAULT_RATE = os.environ.get('OPENCLAW_EDGE_TTS_RATE', '+0%')
DEFAULT_PITCH = os.environ.get('OPENCLAW_EDGE_TTS_PITCH', '+0Hz')
DEFAULT_VOLUME = os.environ.get('OPENCLAW_EDGE_TTS_VOLUME', '+0%')


def _cache_key(text: str, voice: str, rate: str, pitch: str, volume: str) -> Path:
    h = hashlib.sha256(f'{voice}\n{rate}\n{pitch}\n{volume}\n{text}'.encode('utf-8')).hexdigest()
    return CACHE_DIR / f'{h}.mp3'


async def _synthesize(text: str, out_path: Path, voice: str, rate: str, pitch: str, volume: str) -> None:
    sys.path.insert(0, '/root/.openclaw/tts/venv/lib/python3.11/site-packages')
    from edge_tts import Communicate
    communicate = Communicate(text=text, voice=voice, rate=rate, pitch=pitch, volume=volume)
    await communicate.save(str(out_path))


def text_to_speech(text: str, output_file: str | None = None, *, voice: str = DEFAULT_VOICE, rate: str = DEFAULT_RATE, pitch: str = DEFAULT_PITCH, volume: str = DEFAULT_VOLUME) -> str:
    if not text.strip():
        raise ValueError('text is empty')

    cache_path = _cache_key(text, voice, rate, pitch, volume)
    if cache_path.exists():
        if output_file:
            subprocess.run(['cp', str(cache_path), output_file], check=True)
            return output_file
        return str(cache_path)

    tmp_out = Path(output_file) if output_file else Path(tempfile.mktemp(suffix='.mp3', prefix='edge_tts_'))
    asyncio.run(_synthesize(text, tmp_out, voice, rate, pitch, volume))
    tmp_out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['cp', str(tmp_out), str(cache_path)], check=True)
    if output_file and Path(output_file) != cache_path:
        return str(output_file)
    return str(cache_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <text> [output_file] [voice]', file=sys.stderr)
        sys.exit(1)
    text = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    voice = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_VOICE
    print(text_to_speech(text, output_file, voice=voice))
