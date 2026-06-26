from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VERSION_FILE = BASE_DIR / 'VERSION'


def get_public_version() -> str:
    try:
        text = VERSION_FILE.read_text(encoding='utf-8').strip()
        return text or '0.3.x-preview'
    except Exception:
        return '0.3.x-preview'
