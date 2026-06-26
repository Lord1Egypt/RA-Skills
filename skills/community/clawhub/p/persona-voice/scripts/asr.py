from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from config import get_optional, get_required


class SenseAudioASR:
    def __init__(self) -> None:
        base_url = get_optional('SENSEAUDIO_BASE_URL', 'https://api.senseaudio.cn').rstrip('/')
        self.api_url = f'{base_url}/v1/audio/transcriptions'
        self.api_key = get_required('SENSEAUDIO_API_KEY')
        self.model = get_optional('SENSEAUDIO_ASR_MODEL', 'sense-asr')

    def transcribe(self, audio_path: str | Path, language: str | None = 'zh') -> dict[str, Any]:
        path = Path(audio_path)
        with path.open('rb') as f:
            files = {'file': (path.name, f)}
            data: dict[str, Any] = {'model': self.model, 'response_format': 'json'}
            if language and self.model != 'sense-asr-deepthink':
                data['language'] = language
            resp = requests.post(
                self.api_url,
                headers={'Authorization': f'Bearer {self.api_key}'},
                data=data,
                files=files,
                timeout=120,
            )
        resp.raise_for_status()
        result = resp.json()
        if 'text' not in result:
            raise RuntimeError(f'ASR 返回异常: {result}')
        return result
