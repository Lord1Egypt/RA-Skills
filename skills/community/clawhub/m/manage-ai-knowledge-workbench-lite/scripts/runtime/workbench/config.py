"""Configuration, path-safety, and atomic JSON persistence."""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable

from . import __version__


PRODUCT_ID = "ai-knowledge-workbench"
SCHEMA_VERSION = 1
INTERNAL_DIR = ".ai-workbench"
CONFIG_NAME = "workbench.json"
STATE_NAME = "state.json"
MANIFEST_REL = Path("manifests/install.json")
KNOWLEDGE_DIR = "AI-Knowledge"
DASHBOARD_DIR = "AI-Dashboard"

KNOWLEDGE_SUBDIRS = (
    "10-索引",
    "20-主题",
    "30-项目",
    "40-行动",
    "80-待审核",
    "99-系统",
)


class ConfigError(ValueError):
    """Raised when a runtime config is missing, malformed, or unsafe."""


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalized(path: Path | str) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def is_within(root: Path, candidate: Path) -> bool:
    root = normalized(root)
    candidate = normalized(candidate)
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def default_config_path(workspace: Path) -> Path:
    return normalized(workspace) / INTERNAL_DIR / CONFIG_NAME


def resolve_config_path(workspace: Path, requested: Path | None) -> Path:
    workspace = normalized(workspace)
    path = normalized(requested) if requested else default_config_path(workspace)
    if not is_within(workspace, path):
        raise ConfigError("Config path must stay inside the selected workspace.")
    return path


def reserved_paths(workspace: Path) -> dict[str, Path]:
    workspace = normalized(workspace)
    internal = workspace / INTERNAL_DIR
    return {
        "internal": internal,
        "config": internal / CONFIG_NAME,
        "state": internal / STATE_NAME,
        "manifest": internal / MANIFEST_REL,
        "cache": internal / "cache",
        "logs": internal / "logs",
        "knowledge": workspace / KNOWLEDGE_DIR,
        "dashboard": workspace / DASHBOARD_DIR,
        "dashboard_assets": workspace / DASHBOARD_DIR / "assets",
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path = normalized(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(normalized(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"File not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ConfigError(f"Expected a JSON object in {path}")
    return payload


def load_config(path: Path, *, expected_workspace: Path | None = None) -> dict[str, Any]:
    payload = load_json(path)
    if payload.get("product") != PRODUCT_ID:
        raise ConfigError("Config product identifier is missing or incorrect.")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("Unsupported config schema version.")
    required = ("workspace", "mode", "privacy_mode", "paths", "sources")
    missing = [key for key in required if key not in payload]
    if missing:
        raise ConfigError(f"Config is missing required keys: {', '.join(missing)}")
    workspace = normalized(payload["workspace"])
    if expected_workspace is not None and workspace != normalized(expected_workspace):
        raise ConfigError("Config workspace does not match the selected workspace.")
    paths = payload.get("paths")
    if not isinstance(paths, dict):
        raise ConfigError("Config paths must be a JSON object.")
    missing_paths = [key for key in ("internal", "knowledge", "dashboard") if key not in paths]
    if missing_paths:
        raise ConfigError(f"Config is missing required paths: {', '.join(missing_paths)}")
    for key in ("internal", "knowledge", "dashboard"):
        if not is_within(workspace, normalized(paths[key])):
            raise ConfigError(f"Configured {key} path must stay inside the selected workspace.")
    return payload


def source_entries(sources: Iterable[Path]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for index, source in enumerate(sources, start=1):
        source = normalized(source)
        entries.append(
            {
                "id": f"source-{index}",
                "label": source.name or f"Source {index}",
                "root": str(source),
                "include": ["**/*"],
                "exclude": [
                    f"{INTERNAL_DIR}/**",
                    f"{KNOWLEDGE_DIR}/**",
                    f"{DASHBOARD_DIR}/**",
                ],
                "sensitivity": "internal",
            }
        )
    return entries


def make_config(
    *,
    workspace: Path,
    sources: list[Path],
    mode: str,
    privacy_mode: str,
    port: int,
) -> dict[str, Any]:
    workspace = normalized(workspace)
    paths = reserved_paths(workspace)
    return {
        "product": PRODUCT_ID,
        "product_version": __version__,
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "workspace": str(workspace),
        "mode": mode,
        "privacy_mode": privacy_mode,
        "content_access": "local-parse",
        "model_transport": "none",
        "dashboard_body_embedded": False,
        "sources": source_entries(sources),
        "paths": {
            "internal": str(paths["internal"]),
            "knowledge": str(paths["knowledge"]),
            "dashboard": str(paths["dashboard"]),
        },
        "server": {
            "host": "127.0.0.1",
            "port": port,
            "read_only": True,
        },
        "update": {
            "mode": "manual",
            "poll_seconds": 10,
        },
        "scan": {
            "max_files": 50_000,
            "max_file_bytes": 5 * 1024 * 1024,
        },
    }


def relative_to_workspace(workspace: Path, paths: Iterable[Path]) -> list[str]:
    workspace = normalized(workspace)
    values: list[str] = []
    for path in paths:
        resolved = normalized(path)
        if not is_within(workspace, resolved):
            raise ConfigError(f"Generated path escaped workspace: {resolved}")
        values.append(resolved.relative_to(workspace).as_posix())
    return values
