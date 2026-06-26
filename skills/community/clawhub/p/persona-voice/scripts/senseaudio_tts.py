from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from config import get_optional, get_required


class SenseAudioTTS:
    def __init__(self) -> None:
        base_url = get_optional('SENSEAUDIO_BASE_URL', 'https://api.senseaudio.cn').rstrip('/')
        self.api_url = f'{base_url}/v1/t2a_v2'
        self.api_key = get_required('SENSEAUDIO_API_KEY')
        self.model = get_optional('SENSEAUDIO_TTS_MODEL', 'SenseAudio-TTS-1.0')

    def synthesize(
        self,
        *,
        text: str,
        voice_id: str,
        output_path: str | Path,
        speed: float = 1.0,
        vol: float = 1.0,
        pitch: int = 0,
        audio_format: str = 'mp3',
        sample_rate: int = 32000,
    ) -> Path:
        payload: dict[str, Any] = {
            'model': self.model,
            'text': text,
            'stream': False,
            'voice_setting': {
                'voice_id': voice_id,
                'speed': speed,
                'vol': vol,
                'pitch': pitch,
            },
            'audio_setting': {
                'format': audio_format,
                'sample_rate': sample_rate,
            },
        }
        resp = requests.post(
            self.api_url,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=180,
        )
        resp.raise_for_status()
        result = resp.json()
        audio_hex = (((result.get('data') or {}).get('audio')) or '').strip()
        if not audio_hex:
            raise RuntimeError(f'TTS 返回异常: {result}')
        audio_bytes = bytes.fromhex(audio_hex)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(audio_bytes)
        return out
