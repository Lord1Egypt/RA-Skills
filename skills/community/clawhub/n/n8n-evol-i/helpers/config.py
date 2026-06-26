import os
from pathlib import Path
from typing import Any

import yaml


def load_env(env_name: str, workspace: Path) -> dict:
    """Load .env.<env> from workspace/n8n-config/ into os.environ. Returns loaded dict."""
    env_file = workspace / "n8n-config" / f".env.{env_name}"
    loaded = {}
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip()
                if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                    val = val[1:-1]
                os.environ[key] = val
                loaded[key] = val
    return loaded


def load_yaml(env_name: str, workspace: Path) -> dict:
    """Read n8n-config/<env>.yml and validate required keys."""
    yaml_file = workspace / "n8n-config" / f"{env_name}.yml"
    if not yaml_file.exists():
        raise FileNotFoundError(
            f"No environment config at {yaml_file}. "
            f"Run `python3 <harness>/helpers/bootstrap_env.py --env {env_name}` first."
        )
    with open(yaml_file) as f:
        data = yaml.safe_load(f) or {}
    _validate_env_yaml(data, yaml_file)
    return data


def _validate_env_yaml(data: dict, path: Path) -> None:
    for key in ("name", "displayName", "n8n"):
        if key not in data:
            raise ValueError(f"Missing required key '{key}' in {path}")
    if "instanceName" not in data.get("n8n", {}):
        raise ValueError(f"Missing required key 'n8n.instanceName' in {path}")


def load_common(workspace: Path) -> dict:
    """Read n8n-config/common.yml. Returns {} if absent; raises only on YAML parse error."""
    common_file = workspace / "n8n-config" / "common.yml"
    if not common_file.exists():
        return {}
    with open(common_file) as f:
        return yaml.safe_load(f) or {}


def get_config_value(config: dict, dot_path: str) -> Any:
    """Look up a dot-notation path in a nested dict. Raises KeyError if not found."""
    parts = dot_path.split(".")
    current = config
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            raise KeyError(f"Path '{dot_path}' not found in config (missing key '{part}')")
        current = current[part]
    return current


def flatten_config(config: dict, prefix: str = "") -> dict:
    """Flatten a nested dict to dot-path keys."""
    result = {}
    for key, val in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict):
            result.update(flatten_config(val, full_key))
        else:
            result[full_key] = val
    return result
