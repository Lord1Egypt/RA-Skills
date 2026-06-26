#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import yaml


REF_DIR = Path(__file__).resolve().parents[1] / 'references'
ENUM_PATH = REF_DIR / 'enum.yaml'


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f'invalid yaml root: {path}')
    return data


_ENUMS = _load_yaml(ENUM_PATH)


def enum_values(name: str) -> list[Any]:
    node = _ENUMS.get(name)
    if not isinstance(node, dict):
        raise KeyError(f'enum not found: {name}')
    values = node.get('enum')
    if not isinstance(values, list):
        raise KeyError(f'enum values missing: {name}')
    return values


def enum_varnames(name: str) -> list[Any]:
    node = _ENUMS.get(name)
    if not isinstance(node, dict):
        raise KeyError(f'enum not found: {name}')
    values = node.get('x-enum-varnames')
    if not isinstance(values, list):
        raise KeyError(f'enum varnames missing: {name}')
    return values


def ensure_enum(name: str, value: Any) -> Any:
    values = enum_values(name)
    if value not in values:
        raise ValueError(f'{value!r} is not a valid {name}; allowed={values}')
    return value


def ensure_enum_varname(name: str, value: Any) -> Any:
    values = enum_varnames(name)
    if value not in values:
        raise ValueError(f'{value!r} is not a valid {name} varname; allowed={values}')
    return value


def first_enum(name: str) -> Any:
    values = enum_values(name)
    if not values:
        raise ValueError(f'empty enum: {name}')
    return values[0]


def normalize_sort_dir(ascending: bool) -> str:
    return ensure_enum('SortDir', 'ASCEND' if ascending else 'DESCEND')
