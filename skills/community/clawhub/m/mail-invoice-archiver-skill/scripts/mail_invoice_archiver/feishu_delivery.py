from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path


DEFAULT_PRIVATE_FEISHU_CONFIG = Path.home() / '.config' / 'openclaw' / 'mail_invoice_archiver' / 'feishu.config.yaml'


def _parse_simple_feishu_yaml(cfg_path: Path) -> dict[str, str]:
    lines = cfg_path.read_text(encoding='utf-8').splitlines()
    values: dict[str, str] = {}
    in_feishu = False
    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith('#'):
            continue
        if line.strip() == 'feishu:':
            in_feishu = True
            continue
        if in_feishu and line.startswith('  ') and ':' in line:
            key, value = line.strip().split(':', 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_feishu_config(skill_root: Path) -> dict[str, str]:
    env_app_id = os.environ.get('MAIL_INVOICE_ARCHIVER_FEISHU_APP_ID', '').strip()
    env_app_secret = os.environ.get('MAIL_INVOICE_ARCHIVER_FEISHU_APP_SECRET', '').strip()
    env_receive_id_type = os.environ.get('MAIL_INVOICE_ARCHIVER_FEISHU_RECEIVE_ID_TYPE', '').strip()

    legacy_in_skill_config = skill_root / 'config' / 'feishu' / 'config.yaml'
    if legacy_in_skill_config.exists():
        raise RuntimeError(
            'Unsafe in-skill Feishu config detected at '
            f'{legacy_in_skill_config}. Move real secrets to '
            f'{DEFAULT_PRIVATE_FEISHU_CONFIG} or use environment variables.'
        )

    if env_app_id and env_app_secret:
        return {
            'app_id': env_app_id,
            'app_secret': env_app_secret,
            'receive_id_type': env_receive_id_type or 'open_id',
        }

    candidate_paths = [
        Path(os.environ.get('MAIL_INVOICE_ARCHIVER_FEISHU_CONFIG', '')).expanduser()
        if os.environ.get('MAIL_INVOICE_ARCHIVER_FEISHU_CONFIG')
        else None,
        DEFAULT_PRIVATE_FEISHU_CONFIG,
    ]

    for cfg_path in candidate_paths:
        if not cfg_path or not cfg_path.exists():
            continue
        values = _parse_simple_feishu_yaml(cfg_path)
        app_id = values.get('app_id', '').strip()
        app_secret = values.get('app_secret', '').strip()
        if app_id and app_secret:
            return {
                'app_id': app_id,
                'app_secret': app_secret,
                'receive_id_type': values.get('receive_id_type', 'open_id').strip() or 'open_id',
            }

    return {
        'app_id': '',
        'app_secret': '',
        'receive_id_type': env_receive_id_type or 'open_id',
    }


def exchange_tenant_access_token(app_id: str, app_secret: str) -> str:
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        data=json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    token = data.get('tenant_access_token', '')
    if not token:
        raise RuntimeError(f"feishu token exchange failed: {data}")
    return token
