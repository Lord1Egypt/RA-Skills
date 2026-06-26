"""Load `.env` and merge `config.json` into environment (shell env wins)."""

from __future__ import annotations

import json
import os
from pathlib import Path


def load_dotenv(skill_root: Path) -> None:
    """Load `{skill_root}/.env` into os.environ if key not already set (shell env wins)."""
    path = skill_root / ".env"
    if not path.is_file():
        return
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError:
        return
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("export "):
            s = s[7:].strip()
        if "=" not in s:
            continue
        key, _, val = s.partition("=")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        if not key:
            continue
        if os.environ.get(key, "").strip():
            continue
        os.environ[key] = val


def load_config_json(skill_root: Path) -> None:
    """Merge non-secret defaults from skill `config.json` (env vars always win)."""
    candidates: list[Path] = []
    override = os.environ.get("KEPLERJAI_OSS_CONFIG", "").strip()
    if override:
        candidates.append(Path(override))
    candidates.append(skill_root / "config.json")

    for path in candidates:
        if not path.is_file():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        oss = data.get("staticOSS")
        if not isinstance(oss, dict):
            continue

        def set_env(name: str, value: object) -> None:
            if value is None or value == "":
                return
            if os.environ.get(name, "").strip():
                return
            os.environ[name] = str(value).strip()

        if oss.get("endPoint") is not None:
            set_env("KEPLERJAI_OSS_ENDPOINT", oss.get("endPoint"))
        if oss.get("endpoint") is not None:
            set_env("KEPLERJAI_OSS_ENDPOINT", oss.get("endpoint"))
        set_env("KEPLERJAI_OSS_BUCKET", oss.get("bucket"))
        set_env("KEPLERJAI_OSS_BIND_HOST", oss.get("bindHost"))
        set_env("KEPLERJAI_OSS_HOST", oss.get("host"))
        set_env("KEPLERJAI_OSS_UPLOAD_DIR", oss.get("uploadDir"))
        set_env("KEPLERJAI_OSS_NAME_ALPHABET", oss.get("base64Table"))
        if oss.get("objectLifecycleExpireDays") is not None:
            set_env(
                "KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS",
                str(oss.get("objectLifecycleExpireDays")).strip(),
            )
        set_env("KEPLERJAI_OSS_LIFECYCLE_RULE_ID", oss.get("lifecycleRuleId"))
        break
