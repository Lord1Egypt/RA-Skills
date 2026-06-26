from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILES = [ROOT_DIR / '.env.local', ROOT_DIR / '.env']


def load_dotenv() -> None:
    for env_file in ENV_FILES:
        if not env_file.exists():
            continue
        for raw in env_file.read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_required(key: str) -> str:
    load_dotenv()
    value = os.environ.get(key, '').strip()
    if not value:
        raise RuntimeError(f'缺少配置：{key}。请先在本机环境变量中设置，或在 skill 根目录写入 .env.local')
    return value


def get_optional(key: str, default: str) -> str:
    load_dotenv()
    return os.environ.get(key, default).strip() or default
