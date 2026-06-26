"""MiniMax Provider 实现"""

import json
import urllib.request
from typing import Optional

from music_studio.providers.base import MusicAPIBase


class MiniMaxProvider(MusicAPIBase):
    """MiniMax 音乐 API"""

    BASE_URL = "https://api.minimaxi.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.BASE_URL}{path}"
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())

    def lyrics_generation(
        self,
        prompt: str = "",
        *,
        mode: str = "write_full_song",
        lyrics: Optional[str] = None,
        title: Optional[str] = None,
    ) -> dict:
        payload: dict = {"mode": mode}
        if prompt:
            payload["prompt"] = prompt
        if lyrics:
            payload["lyrics"] = lyrics
        if title:
            payload["title"] = title
        return self._post("/lyrics_generation", payload)

    def music_cover_preprocess(
        self,
        model: str,
        *,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
    ) -> dict:
        payload: dict = {"model": model}
        if audio_url:
            payload["audio_url"] = audio_url
        if audio_base64:
            payload["audio_base64"] = audio_base64
        return self._post("/music_cover_preprocess", payload)

    def music_generation(
        self,
        model: str,
        prompt: str,
        *,
        lyrics: Optional[str] = None,
        is_instrumental: bool = False,
        lyrics_optimizer: bool = False,
        output_format: str = "url",
        sample_rate: int = 44100,
        bitrate: int = 256000,
        reference_audio_url: Optional[str] = None,
        reference_audio_base64: Optional[str] = None,
        cover_feature_id: Optional[str] = None,
    ) -> dict:
        payload: dict = {
            "model": model,
            "prompt": prompt,
            "output_format": output_format,
            "audio_setting": {
                "sample_rate": sample_rate,
                "bitrate": bitrate,
                "format": "mp3",
            },
        }
        if lyrics:
            payload["lyrics"] = lyrics
        if is_instrumental:
            payload["is_instrumental"] = True
        if lyrics_optimizer:
            payload["lyrics_optimizer"] = True
        if cover_feature_id:
            payload["cover_feature_id"] = cover_feature_id
        else:
            if reference_audio_url:
                payload["audio_url"] = reference_audio_url
            if reference_audio_base64:
                payload["audio_base64"] = reference_audio_base64
        return self._post("/music_generation", payload)

    def raise_on_error(self, resp: dict) -> None:
        code = resp.get("base_resp", {}).get("status_code", 0)
        if code != 0:
            msg = resp.get("base_resp", {}).get("status_msg", "未知错误")
            raise RuntimeError(f"API 错误 (code={code}): {msg}")
