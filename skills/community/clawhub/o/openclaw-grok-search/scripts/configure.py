#!/usr/bin/env python3
"""
Author: 橙家厨子
Email: tomography2308@163.com
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")
    return data


def ask(prompt: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def default_config_path() -> Path:
    custom = (os.environ.get("GROK_CONFIG_PATH") or "").strip()
    if custom:
        return Path(custom).expanduser()

    return Path(__file__).resolve().parent.parent / "config.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactive config for openclaw-grok-search (project-local)")
    parser.add_argument("--config", default="", help="Explicit config output path")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser() if args.config else default_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    try:
        existing = read_json(config_path)
    except Exception:
        existing = {}

    base_url = ask("Grok base URL", str(existing.get("base_url") or "https://your-grok-endpoint.example"))
    api_key = ask("Grok API key", str(existing.get("api_key") or ""))
    model = ask("Model", str(existing.get("model") or "grok-2-latest"))
    timeout_raw = ask("Timeout seconds", str(existing.get("timeout_seconds") or "60"))

    try:
        timeout_seconds = int(timeout_raw)
    except ValueError:
        timeout_seconds = 60

    config = {
        "author": "橙家厨子",
        "email": "tomography2308@163.com",
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
        "timeout_seconds": timeout_seconds,
        "extra_body": existing.get("extra_body") if isinstance(existing.get("extra_body"), dict) else {},
        "extra_headers": existing.get("extra_headers") if isinstance(existing.get("extra_headers"), dict) else {},
    }

    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote config: {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
