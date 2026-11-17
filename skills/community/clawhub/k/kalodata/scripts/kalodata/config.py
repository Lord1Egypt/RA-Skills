"""Configuration: environment variables first, then ~/.config/kalodata/config.toml."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULT_BASE_URL = "https://www.kalodata.com/openapi/v1"

ENV_KEYS = {
    "api_key": "KALODATA_API_KEY",
    "base_url": "KALODATA_BASE_URL",
    "region": "KALODATA_REGION",
    "language": "KALODATA_LANGUAGE",
    "currency": "KALODATA_CURRENCY",
}


def config_path() -> Path:
    base = os.environ.get("KALODATA_CONFIG_DIR")
    root = Path(base) if base else Path.home() / ".config" / "kalodata"
    return root / "config.toml"


@dataclass
class Config:
    api_key: str | None = None
    base_url: str = DEFAULT_BASE_URL
    region: str = "US"
    language: str = "en-US"
    currency: str = "USD"

    @property
    def authed(self) -> bool:
        return bool(self.api_key)


def _read_file() -> dict:
    try:
        with open(config_path(), "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}
    except (tomllib.TOMLDecodeError, OSError):
        return {}


def load() -> Config:
    data = _read_file()

    def pick(key: str, fallback: str | None = None) -> str | None:
        env = os.environ.get(ENV_KEYS[key])
        if env:
            return env
        val = data.get(key)
        if val is not None:
            return str(val)
        return fallback

    return Config(
        api_key=pick("api_key"),
        base_url=pick("base_url", DEFAULT_BASE_URL) or DEFAULT_BASE_URL,
        region=pick("region", "US") or "US",
        language=pick("language", "en-US") or "en-US",
        currency=pick("currency", "USD") or "USD",
    )


def save(updates: dict) -> Path:
    data = _read_file()
    data.update({k: v for k, v in updates.items() if v is not None})
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for k, v in data.items():
        escaped = str(v).replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'{k} = "{escaped}"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
    return path
