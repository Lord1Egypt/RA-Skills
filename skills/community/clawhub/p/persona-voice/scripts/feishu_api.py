from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import requests

from config import get_optional, get_required


class FeishuClient:
    def __init__(self) -> None:
        self.base_url = get_optional('FEISHU_BASE_URL', 'https://open.feishu.cn').rstrip('/')
        self.app_id = get_required('FEISHU_APP_ID')
        self.app_secret = get_required('FEISHU_APP_SECRET')

    def tenant_access_token(self) -> str:
        resp = requests.post(
            f'{self.base_url}/open-apis/auth/v3/tenant_access_token/internal',
            headers={'Content-Type': 'application/json; charset=utf-8'},
            json={'app_id': self.app_id, 'app_secret': self.app_secret},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        token = (data.get('tenant_access_token') or '').strip()
        if not token:
            raise RuntimeError(f'获取 tenant_access_token 失败: {data}')
        return token

    def upload_audio(self, opus_path: str | Path) -> str:
        token = self.tenant_access_token()
        path = Path(opus_path)
        with path.open('rb') as f:
            files = {'file': (path.name, f, 'audio/ogg')}
            data = {'file_type': 'opus', 'file_name': path.name}
            resp = requests.post(
                f'{self.base_url}/open-apis/im/v1/files',
                headers={'Authorization': f'Bearer {token}'},
                data=data,
                files=files,
                timeout=60,
            )
        resp.raise_for_status()
        body = resp.json()
        file_key = (((body.get('data') or {}).get('file_key')) or '').strip()
        if not file_key:
            raise RuntimeError(f'飞书上传音频失败: {body}')
        return file_key

    def send_audio_message(self, chat_id: str, file_key: str) -> dict:
        token = self.tenant_access_token()
        resp = requests.post(
            f'{self.base_url}/open-apis/im/v1/messages',
            params={'receive_id_type': 'chat_id'},
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'},
            json={'receive_id': chat_id, 'msg_type': 'audio', 'content': json.dumps({'file_key': file_key}, ensure_ascii=False)},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        if body.get('code', 0) != 0:
            raise RuntimeError(f'飞书发送语音消息失败: {body}')
        return body


def resolve_ffmpeg_binary() -> str:
    ffmpeg_path = get_optional('FFMPEG_PATH', '').strip()
    return ffmpeg_path or 'ffmpeg'


def ensure_ffmpeg(ffmpeg_bin: str) -> None:
    try:
        proc = subprocess.run([ffmpeg_bin, '-version'], capture_output=True, text=True, check=False, timeout=10)
    except FileNotFoundError as e:
        raise RuntimeError(
            '未找到 ffmpeg。请先安装：brew install ffmpeg，或设置环境变量 FFMPEG_PATH=/opt/homebrew/bin/ffmpeg'
        ) from e
    if proc.returncode != 0:
        raise RuntimeError(f'ffmpeg 不可用: {proc.stderr.strip()}')


def convert_to_opus(input_audio: str | Path, output_opus: str | Path | None = None) -> Path:
    ffmpeg_bin = resolve_ffmpeg_binary()
    ensure_ffmpeg(ffmpeg_bin)
    src = Path(input_audio)
    if output_opus is None:
        tmp_dir = Path(tempfile.mkdtemp(prefix='feishu-opus-'))
        output = tmp_dir / f'{src.stem}.opus'
    else:
        output = Path(output_opus)
        output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg_bin, '-y', '-i', str(src), '-c:a', 'libopus', '-b:a', '32k', '-vbr', 'on', '-ar', '48000', str(output)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(f'音频转 OPUS 失败: {proc.stderr.strip()}')
    return output
