#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, Tuple

MIDDLEWARES = {"redis", "mongo", "mysql"}


def _load_new_shape(data: dict, profile: str) -> Tuple[dict, dict]:
    """
    New shape:
    {
      "redis": [{"env":"local","alias":"main",...}],
      "mongo": [],
      "mysql": []
    }

    profile format: <middleware>.<env-or-alias>
    example: redis.local / redis.main / mysql.dev / mongo.test
    """
    if "." not in profile:
        raise ValueError(
            f"Invalid profile '{profile}'. Use '<middleware>.<env-or-alias>', e.g. redis.local or redis.main"
        )

    middleware, selector = profile.split(".", 1)
    middleware = middleware.strip().lower()
    selector = selector.strip()

    if middleware not in MIDDLEWARES:
        raise ValueError(f"Unsupported middleware in profile: {middleware}")

    entries = data.get(middleware, []) or []
    if not isinstance(entries, list):
        raise ValueError(f"Invalid config: '{middleware}' must be an array")

    for item in entries:
        if not isinstance(item, dict):
            continue
        env = str(item.get("env", "")).strip()
        alias = str(item.get("alias", "")).strip()
        if selector == env or selector == alias:
            return item, {
                "source": "middleware-list",
                "requested_profile": profile,
                "resolved_profile": f"{middleware}.{selector}",
                "middleware": middleware,
                "environment": env or None,
                "alias": alias or None,
            }

    raise ValueError(
        f"No config matched profile '{profile}'. Expected selector to match env/alias under '{middleware}'"
    )


def _load_env_alias_shape(data: dict, profile: str) -> Tuple[dict, dict]:
    aliases: Dict[str, str] = data.get("aliases", {}) or {}
    target = aliases.get(profile, profile)

    if "." not in target:
        raise ValueError(
            f"Invalid profile '{profile}' -> '{target}'. Use '<middleware>.<env>' or define alias to that format."
        )

    middleware, env = target.split(".", 1)
    envs = data.get("environments", {})
    if env not in envs:
        raise ValueError(f"Environment not found: {env}")

    env_conf = envs[env] or {}
    if middleware not in env_conf:
        raise ValueError(f"Middleware '{middleware}' not configured in env '{env}'")

    conf = env_conf[middleware]
    if not isinstance(conf, dict):
        raise ValueError(f"Invalid config at environments.{env}.{middleware}")

    return conf, {
        "source": "env-alias",
        "requested_profile": profile,
        "resolved_profile": f"{middleware}.{env}",
        "middleware": middleware,
        "environment": env,
    }


def load_profile(conn_file: str, profile: str) -> Tuple[dict, dict]:
    p = Path(conn_file)
    if not p.exists():
        raise ValueError(f"Connection file not found: {conn_file}")

    data = json.loads(p.read_text(encoding="utf-8"))

    # New middleware-list shape (preferred)
    if any(k in data for k in MIDDLEWARES) and isinstance(data.get("redis", []), list):
        return _load_new_shape(data, profile)

    # Previous env + alias shape
    if "environments" in data:
        return _load_env_alias_shape(data, profile)

    # Legacy flat shape
    if profile not in data:
        raise ValueError(f"Profile not found: {profile}")
    return data[profile], {"source": "legacy", "profile": profile}
