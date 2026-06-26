#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TZ).replace(microsecond=0).isoformat()


def storage_root() -> Path:
    root = os.environ.get('PET_COMPANION_HOME', '~/.pet-companion')
    p = Path(root).expanduser()
    for child in ['pets', 'records', 'reminders', 'media', 'reports']:
        (p / child).mkdir(parents=True, exist_ok=True)
    return p


def slugify(text: str) -> str:
    text = re.sub(r'\s+', '-', text.strip().lower())
    text = re.sub(r'[^a-z0-9\-\u4e00-\u9fff]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text or 'pet'


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def load_pet(pet_id: str) -> Dict[str, Any]:
    path = storage_root() / 'pets' / f'{pet_id}.json'
    data = read_json(path)
    if not data:
        raise SystemExit(f'Pet not found: {pet_id}')
    return data


def list_pets() -> List[Dict[str, Any]]:
    root = storage_root() / 'pets'
    pets = []
    for p in sorted(root.glob('*.json')):
        data = read_json(p)
        if data:
            pets.append(data)
    return pets


def make_record_id(prefix: str = 'rec') -> str:
    return f"{prefix}_{datetime.now(TZ).strftime('%Y%m%d%H%M%S')}"


def record_dir(dt: datetime | None = None) -> Path:
    dt = dt or datetime.now(TZ)
    root = storage_root() / 'records' / dt.strftime('%Y') / dt.strftime('%m')
    root.mkdir(parents=True, exist_ok=True)
    return root


def write_record(frontmatter: Dict[str, Any], body: str) -> Path:
    dt = datetime.fromisoformat(frontmatter['created_at'])
    file_name = f"{dt.strftime('%Y-%m-%d')}-{frontmatter['type']}-{frontmatter['record_id']}.md"
    path = record_dir(dt) / file_name
    content = '---\n' + json.dumps(frontmatter, ensure_ascii=False) + '\n---\n\n' + body.strip() + '\n'
    path.write_text(content, encoding='utf-8')
    return path


def parse_record(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'Invalid record format: {path}')
    _, rest = text.split('---\n', 1)
    fm_raw, body = rest.split('\n---\n', 1)
    fm = json.loads(fm_raw)
    fm['body'] = body.strip()
    fm['path'] = str(path)
    return fm
