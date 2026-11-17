#!/usr/bin/env python3
"""Shared profile storage and resolution for the OData skills."""

from __future__ import annotations

import json
import os
import re
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
CONFIG_ENV = "ODATA_SKILL_CONFIG"
PROFILE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
HEADER_NAME = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
PROFILE_KEYS = {
    "service_root",
    "odata_version",
    "bearer_env",
    "basic_user_env",
    "basic_password_env",
    "headers_from_env",
}


def default_config_path() -> Path:
    override = os.environ.get(CONFIG_ENV)
    return Path(override).expanduser() if override else Path.home() / ".config" / "odata-skill" / "services.json"


def config_path(value: str | None = None) -> Path:
    return Path(value).expanduser() if value else default_config_path()


def validate_service_root(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("service root must be an absolute HTTP(S) URL")
    if parsed.query or parsed.fragment or parsed.username is not None or parsed.password is not None:
        raise ValueError("service root must not contain a query, fragment, or embedded credentials")
    return value.rstrip("/") + "/"


def validate_env_name(value: str, field: str) -> str:
    if not ENV_NAME.fullmatch(value):
        raise ValueError(f"{field} must name an environment variable, not contain a credential")
    return value


def validate_profile(name: str, profile: dict[str, Any]) -> dict[str, Any]:
    if not PROFILE_NAME.fullmatch(name):
        raise ValueError(f"invalid profile name {name!r}")
    unknown = set(profile) - PROFILE_KEYS
    if unknown:
        raise ValueError(f"profile {name!r} has unsupported fields: {sorted(unknown)}")
    result: dict[str, Any] = {
        "service_root": validate_service_root(str(profile.get("service_root", ""))),
        "odata_version": str(profile.get("odata_version", "4.0")),
    }
    if result["odata_version"] not in {"4.0", "4.01"}:
        raise ValueError(f"profile {name!r} has unsupported OData version")
    for field in ("bearer_env", "basic_user_env", "basic_password_env"):
        value = profile.get(field)
        if value:
            result[field] = validate_env_name(str(value), field)
    if result.get("bearer_env") and (result.get("basic_user_env") or result.get("basic_password_env")):
        raise ValueError(f"profile {name!r} cannot combine bearer and basic authentication")
    if bool(result.get("basic_user_env")) != bool(result.get("basic_password_env")):
        raise ValueError(f"profile {name!r} requires both basic-auth environment-variable names")
    raw_headers = profile.get("headers_from_env", {})
    if not isinstance(raw_headers, dict):
        raise ValueError(f"profile {name!r} headers_from_env must be an object")
    headers: dict[str, str] = {}
    for header, env_name in raw_headers.items():
        if not isinstance(header, str) or not HEADER_NAME.fullmatch(header):
            raise ValueError(f"profile {name!r} contains an invalid header name")
        headers[header] = validate_env_name(str(env_name), f"header {header}")
    if headers:
        result["headers_from_env"] = headers
    return result


def empty_config() -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "default_profile": None, "profiles": {}}


def load_config(path: Path, require: bool = False) -> dict[str, Any]:
    if not path.exists():
        if require:
            raise ValueError(f"OData profile config not found: {path}; run odata_config.py set first")
        return empty_config()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read OData profile config {path}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported OData profile config schema in {path}")
    raw_profiles = raw.get("profiles")
    if not isinstance(raw_profiles, dict):
        raise ValueError(f"profiles must be an object in {path}")
    profiles = {name: validate_profile(name, value) for name, value in raw_profiles.items() if isinstance(value, dict)}
    if len(profiles) != len(raw_profiles):
        raise ValueError(f"every profile must be an object in {path}")
    default = raw.get("default_profile")
    if default is not None and default not in profiles:
        raise ValueError(f"default profile {default!r} does not exist in {path}")
    return {"schema_version": SCHEMA_VERSION, "default_profile": default, "profiles": profiles}


def save_config(path: Path, value: dict[str, Any]) -> None:
    validated_profiles = {
        name: validate_profile(name, profile) for name, profile in value.get("profiles", {}).items()
    }
    default = value.get("default_profile")
    if default is not None and default not in validated_profiles:
        raise ValueError(f"default profile {default!r} does not exist")
    rendered = json.dumps(
        {"schema_version": SCHEMA_VERSION, "default_profile": default, "profiles": validated_profiles},
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
        try:
            os.chmod(temp_name, 0o600)
        except OSError:
            pass
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def resolve_profile_args(args: Any) -> None:
    if getattr(args, "service_root", None) and getattr(args, "profile", None):
        raise ValueError("choose either --service-root or --profile, not both")
    if getattr(args, "service_root", None):
        args.service_root = validate_service_root(args.service_root)
        args.odata_version = args.odata_version or "4.0"
        return
    path = config_path(getattr(args, "config", None))
    value = load_config(path, require=True)
    name = getattr(args, "profile", None) or value.get("default_profile")
    if not name:
        raise ValueError(f"no profile selected and no default profile is configured in {path}")
    profile = value["profiles"].get(name)
    if profile is None:
        raise ValueError(f"OData profile {name!r} does not exist in {path}")
    args.service_root = profile["service_root"]
    args.odata_version = args.odata_version or profile.get("odata_version", "4.0")
    for field in ("bearer_env", "basic_user_env", "basic_password_env"):
        if not getattr(args, field, None):
            setattr(args, field, profile.get(field))
    configured_headers = [f"{name}={env_name}" for name, env_name in profile.get("headers_from_env", {}).items()]
    args.header_env = configured_headers + list(getattr(args, "header_env", []))


def public_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a display-safe profile; profiles contain variable names, never secret values."""
    return dict(profile)
