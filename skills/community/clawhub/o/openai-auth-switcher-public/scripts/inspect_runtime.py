#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

from auth_file_lib import get_openai_default_profile, load_auth_profiles_file
from paths import detect_runtime
from probe_lib import find_recent_session_files, probe_gateway_status, probe_openclaw_status

JsonDict = Dict[str, Any]
ERROR_PATTERNS = [
    ('usage_limit', re.compile(r'usage limit', re.I)),
    ('rate_limit', re.compile(r'rate limit', re.I)),
    ('unauthorized', re.compile(r'unauthori[sz]ed|401|403', re.I)),
    ('auth_error', re.compile(r'auth(entication)? (failed|error|expired|invalid)', re.I)),
]


def load_models() -> JsonDict:
    runtime = detect_runtime()
    models_path = runtime.get('models_path')
    if not models_path:
        raise FileNotFoundError('models.json path not discovered')
    with Path(models_path).open('r', encoding='utf-8') as f:
        return json.load(f)


def extract_openai_provider(models: JsonDict) -> JsonDict:
    provider = (models.get('providers') or {}).get('openai-codex') or {}
    return {
        'base_url': provider.get('baseUrl'),
        'api': provider.get('api'),
        'models': provider.get('models', []),
    }


def summarize_recent_session_errors(limit: int = 3) -> list[JsonDict]:
    results: list[JsonDict] = []
    for path in find_recent_session_files(limit):
        try:
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()[-300:]
        except OSError:
            continue
        for line in reversed(lines):
            for kind, pattern in ERROR_PATTERNS:
                if pattern.search(line):
                    results.append({'file': str(path), 'kind': kind, 'sample': line[:220]})
                    break
            if len(results) >= 10:
                return list(reversed(results))
    return list(reversed(results))


def build_result(args: argparse.Namespace) -> JsonDict:
    auth_data = load_auth_profiles_file()
    openai_auth = get_openai_default_profile(auth_data)
    models = load_models()
    runtime = detect_runtime()

    result: JsonDict = {
        'ok': True,
        'paths': {
            'openclaw_root': runtime.get('openclaw_root'),
            'workspace': runtime.get('workspace'),
            'agent_root': runtime.get('agent_root'),
            'auth_profiles': runtime.get('auth_profiles_path'),
            'models': runtime.get('models_path'),
            'sessions': runtime.get('session_root'),
        },
        'openai_auth': {
            'profile_key': 'openai-codex:default',
            'provider': openai_auth.get('provider'),
            'type': openai_auth.get('type'),
            'account_id': openai_auth.get('accountId'),
            'expires': openai_auth.get('expires'),
            'last_used': ((auth_data.get('usageStats') or {}).get('openai-codex:default') or {}).get('lastUsed'),
            'error_count': ((auth_data.get('usageStats') or {}).get('openai-codex:default') or {}).get('errorCount'),
        },
        'provider': extract_openai_provider(models),
        'recent_errors': [],
    }

    if args.include_status:
        result['gateway'] = probe_gateway_status()
        result['status'] = probe_openclaw_status()

    if args.include_sessions:
        result['recent_errors'] = summarize_recent_session_errors(args.session_limit)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', dest='json_output')
    parser.add_argument('--include-sessions', action='store_true')
    parser.add_argument('--include-status', action='store_true')
    parser.add_argument('--session-limit', type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_result(args)
    except Exception as e:
        result = {'ok': False, 'error': str(e)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
