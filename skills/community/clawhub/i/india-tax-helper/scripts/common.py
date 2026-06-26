#!/usr/bin/env python3
import json
import sys
from pathlib import Path


class RulesError(Exception):
    pass


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump(data):
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write('\n')


def load_rules(path: str | None):
    if not path:
        raise RulesError('No verified rules file provided')
    p = Path(path)
    if not p.exists():
        raise RulesError(f'Rules file not found: {path}')
    data = load_json(str(p))
    if not data.get('verified'):
        raise RulesError('Rules file is not marked verified=true')
    return data


def blocked(reason: str, missing=None):
    return {
        'status': 'blocked_unverified_rules',
        'reason': reason,
        'missing': missing or [],
    }


def estimate_payload(kind: str, inputs: dict, assumptions: list[str], result: dict, missing=None):
    return {
        'status': 'estimate' if assumptions else 'exact',
        'kind': kind,
        'inputs': inputs,
        'assumptions': assumptions,
        'missing': missing or [],
        'result': result,
    }
