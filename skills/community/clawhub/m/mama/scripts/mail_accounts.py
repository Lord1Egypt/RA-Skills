#!/usr/bin/env python3
"""Mail account configuration loading and writing helpers."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_JSON_CONFIG = SCRIPT_DIR / "mail_config.json"
LEGACY_PY_CONFIG = SCRIPT_DIR / "mail_config.py"

_ACCOUNT_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")
_LEGACY_IMAP_VALUE_KEYS = ("imap_" + "conn_" + "param", "IMAP_" + "CONN_" + "PARAM")
_LEGACY_SMTP_VALUE_KEYS = ("smtp_" + "conn_" + "param", "SMTP_" + "CONN_" + "PARAM")


def make_account_id(user: str, fallback: str = "default") -> str:
    local = (user or "").split("@", 1)[0] or fallback
    return (_ACCOUNT_ID_RE.sub("-", local).strip("-_.") or fallback)[:48]


def _load_py_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("mail_config", str(path))
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {key: getattr(module, key) for key in dir(module) if key.isupper()}


def _load_json_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_raw_config(path: Path | str | None = None) -> dict[str, Any]:
    if path is not None:
        p = Path(path)
        if p.suffix.lower() == ".json":
            return _load_json_config(p)
        return _load_py_config(p)
    if DEFAULT_JSON_CONFIG.exists():
        return _load_json_config(DEFAULT_JSON_CONFIG)
    return _load_py_config(LEGACY_PY_CONFIG)


def _get(data: dict[str, Any], *names: str, default: Any = "") -> Any:
    for name in names:
        if name in data and data[name] not in (None, ""):
            return data[name]
    return default


def normalize_account(account_id: str, data: dict[str, Any]) -> dict[str, Any]:
    user = _get(data, "user", "mail_user", "MAIL_USER", "imap_user", "IMAP_USER")
    imap_value = _get(
        data, "imap_client_value", "IMAP_CLIENT_VALUE", *_LEGACY_IMAP_VALUE_KEYS
    )
    smtp_user = _get(data, "smtp_user", "SMTP_USER", default=user)
    smtp_value = _get(
        data,
        "smtp_client_value",
        "SMTP_CLIENT_VALUE",
        *_LEGACY_SMTP_VALUE_KEYS,
        default=imap_value,
    )
    return {
        "id": account_id,
        "provider": _get(data, "provider", "mail_provider", "MAIL_PROVIDER", default="custom"),
        "user": user,
        "imap_host": _get(data, "imap_host", "IMAP_HOST"),
        "imap_port": int(_get(data, "imap_port", "IMAP_PORT", default=993) or 993),
        "imap_client_value": imap_value,
        "smtp_host": _get(data, "smtp_host", "SMTP_HOST"),
        "smtp_port": int(_get(data, "smtp_port", "SMTP_PORT", default=465) or 465),
        "smtp_user": smtp_user,
        "smtp_client_value": smtp_value,
        "from_name": _get(data, "from_name", "FROM_NAME", default="邮箱智能体"),
    }


def load_accounts(path: Path | str | None = None) -> tuple[str, dict[str, dict[str, Any]]]:
    raw = load_raw_config(path)
    if not raw:
        return "", {}

    if isinstance(raw.get("accounts"), dict):
        accounts = {
            account_id: normalize_account(account_id, account_data)
            for account_id, account_data in raw["accounts"].items()
            if isinstance(account_data, dict)
        }
        default_id = raw.get("default_account") or next(iter(accounts), "")
        return default_id, accounts

    legacy_id = make_account_id(_get(raw, "MAIL_USER", "IMAP_USER"))
    return legacy_id, {legacy_id: normalize_account(legacy_id, raw)}


def select_account(
    account_id: str = "", path: Path | str | None = None
) -> dict[str, Any]:
    default_id, accounts = load_accounts(path)
    selected = account_id or default_id
    if not selected and accounts:
        selected = next(iter(accounts))
    if selected not in accounts:
        available = ", ".join(accounts) or "无"
        raise ValueError(f"未找到邮箱账号配置：{selected or '(默认)'}；可用账号：{available}")
    return accounts[selected]


def write_accounts_config(
    path: Path,
    default_account: str,
    accounts: dict[str, dict[str, Any]],
) -> None:
    path.write_text(
        json.dumps(
            {
                "version": 2,
                "default_account": default_account,
                "accounts": accounts,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
