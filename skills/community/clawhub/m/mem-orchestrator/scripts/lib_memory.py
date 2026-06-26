#!/usr/bin/env python3
import json
import os

try:
    import yaml
except Exception:
    yaml = None


def simple_yaml_load(text: str):
    data = {}
    current_key = None
    current_subkey = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith('  - ') and current_key:
            data.setdefault(current_key, [])
            data[current_key].append(line[4:].strip().strip('"'))
            continue
        if line.startswith('    - ') and current_key and current_subkey:
            data.setdefault(current_key, {})
            data[current_key].setdefault(current_subkey, [])
            data[current_key][current_subkey].append(line[6:].strip().strip('"'))
            continue
        if line.startswith('  ') and ': ' in line and current_key:
            subkey, value = line.strip().split(': ', 1)
            data.setdefault(current_key, {})
            data[current_key][subkey.strip()] = value.strip().strip('"')
            current_subkey = subkey.strip()
            continue
        if ': ' in line:
            key, value = line.split(': ', 1)
            current_key = key.strip()
            current_subkey = None
            data[current_key] = value.strip().strip('"')
            continue
        if line.endswith(':'):
            current_key = line[:-1].strip()
            current_subkey = None
            if current_key not in data:
                data[current_key] = []
    return data


def load_yaml_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    if yaml is not None:
        try:
            return yaml.safe_load(text) or {}
        except Exception:
            pass
    return simple_yaml_load(text)


def dump_yaml_fallback(data):
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f'{key}:')
            for item in value:
                lines.append(f'  - {item}')
        elif isinstance(value, dict):
            lines.append(f'{key}:')
            if not value:
                lines[-1] += ' {}'
            else:
                for k, v in value.items():
                    if isinstance(v, list):
                        lines.append(f'  {k}:')
                        for item in v:
                            lines.append(f'    - {item}')
                    else:
                        lines.append(f'  {k}: {v}')
        else:
            encoded = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else value
            lines.append(f'{key}: {encoded}')
    return '\n'.join(lines) + '\n'
