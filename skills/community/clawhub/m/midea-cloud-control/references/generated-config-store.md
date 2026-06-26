# Generated file: config_store.py

When this skill is used for the first time, write the following file to the user's local workspace or a temporary working directory as `config_store.py`, then use it together with `midea_skill_cli.py`.

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".openclaw" / "midea-cloud-control"
CONFIG_PATH = CONFIG_DIR / "config.json"


def ensure_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(data: dict[str, Any]) -> Path:
    ensure_dir()
    CONFIG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return CONFIG_PATH
```
