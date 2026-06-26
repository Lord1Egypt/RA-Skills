"""
openclaw.json read/write helpers.
Handles safe reading, merging, and writing of the OpenClaw configuration.
"""

import json
from pathlib import Path


DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def read_config(config_path=None):
    """Read and parse openclaw.json. Returns empty dict if not found."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_config(data, config_path=None):
    """Write config dict to openclaw.json with pretty formatting."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def merge_config(updates, config_path=None):
    """Deep-merge updates into existing config and write."""
    existing = read_config(config_path)
    merged = _deep_merge(existing, updates)
    write_config(merged, config_path)
    return merged


def _deep_merge(base, override):
    """Recursively merge override into base dict."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def get_persona_config(config_path=None):
    """Get the persona section from config."""
    config = read_config(config_path)
    return config.get("persona", {})


def set_persona_config(persona_data, config_path=None):
    """Set the persona section in config."""
    return merge_config({"persona": persona_data}, config_path)


def set_tts_config(tts_data, config_path=None):
    """Set the messages.tts section in config."""
    return merge_config({"messages": {"tts": tts_data}}, config_path)


def extract_persona_config_no_secrets(config_path=None):
    """Extract persona config with API keys removed (for export)."""
    persona = get_persona_config(config_path)
    cleaned = json.loads(json.dumps(persona))
    # Remove any keys that look like API keys/secrets
    _strip_secrets(cleaned)
    return cleaned


def _strip_secrets(d):
    """Recursively remove keys that look like secrets."""
    secret_patterns = {"apiKey", "api_key", "apikey", "secret", "token",
                       "password", "credential"}
    if not isinstance(d, dict):
        return
    keys_to_remove = []
    for key in d:
        lower = key.lower()
        if any(pat in lower for pat in secret_patterns):
            keys_to_remove.append(key)
        elif isinstance(d[key], dict):
            _strip_secrets(d[key])
    for key in keys_to_remove:
        del d[key]
