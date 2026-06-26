from __future__ import annotations

import json
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .task_bundle_crypto import TaskBundleCryptoError, decrypt_text, is_encrypted_value, load_task_bundle_key
from .utils import Task, load_json, write_json
from .v2_bundle_loader import fetch_v2_task_package, is_v2_runtime

_TASK_CACHE_PERSIST_ENV = "GIGO_KEEP_TASK_CACHE"


def _decode_payload(value: str, key: bytes | None) -> str:
    if is_encrypted_value(value):
        if not key:
            raise TaskBundleCryptoError("云端题包尚未解锁，已回退到公开 demo 包。")
        return decrypt_text(value, key)
    return value


def _cache_policy(config: dict) -> str:
    configured = str(config.get("task_cache_policy") or "").strip().lower()
    if configured in {"persist", "ephemeral"}:
        return configured
    env_value = (os.environ.get(_TASK_CACHE_PERSIST_ENV) or "").strip().lower()
    if env_value in {"1", "true", "yes", "on"}:
        return "persist"
    return "ephemeral"


def _persistent_cache_root() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
        return base / "gigo-lobster-taster" / "task-cache"
    return Path.home() / ".cache" / "gigo-lobster-taster" / "task-cache"


def _cache_path(config: dict, repo_root: Path) -> Path:
    policy = _cache_policy(config)
    if policy == "persist":
        cache_root = _persistent_cache_root()
    else:
        cache_root = Path(tempfile.gettempdir()) / "gigo-lobster-taster" / "task-cache"
    cache_root.mkdir(parents=True, exist_ok=True)
    cache_path = cache_root / f"task_cache_{config.get('lang', 'zh')}.json"
    config["task_cache_policy"] = policy
    config["task_cache_path"] = str(cache_path)
    return cache_path


def cleanup_task_cache(config: dict) -> None:
    if str(config.get("task_cache_policy") or "ephemeral") == "persist":
        return
    cache_path_value = config.get("task_cache_path")
    if not cache_path_value:
        return
    try:
        Path(str(cache_path_value)).unlink(missing_ok=True)
    except OSError:
        pass


def _fallback_package_path(config: dict, repo_root: Path) -> Path:
    lang = config.get("lang", "zh")
    localized = repo_root / "scripts" / f"fallback_tasks_{lang}.json"
    if localized.exists():
        return localized
    return repo_root / "scripts" / "fallback_tasks.json"


def _package_to_tasks(package: dict, key: bytes | None) -> list[Task]:
    tasks: list[Task] = []
    for item in package["tasks"]:
        prompt = item.get("prompt")
        rubric = item.get("rubric")
        rubric_encrypted = item.get("rubric_encrypted")
        tasks.append(
            Task(
                id=item["id"],
                prompt=prompt if isinstance(prompt, str) else _decode_payload(item["prompt_encrypted"], key),
                dish_name=item["dish_name"],
                dish_hint=item["dish_hint"],
                primary_dimensions=item["primary_dimensions"],
                secondary_dimensions=item["secondary_dimensions"],
                timeout_seconds=int(item.get("timeout_seconds", 300)),
                rubric=rubric if isinstance(rubric, str) else _decode_payload(rubric_encrypted, key) if isinstance(rubric_encrypted, str) else "",
                setup=item.get("setup") or {},
            )
        )
    return tasks


def _remember_package_meta(config: dict, package: dict, source: str, warning: str | None = None) -> None:
    config["task_bundle_version"] = package.get("version", "unknown")
    config["task_bundle_source"] = source
    if warning:
        config["task_bundle_warning"] = warning


def _build_remote_request(config: dict, cached_package: dict | None) -> urllib.request.Request:
    session = config.get("task_session") or {}
    base_url = session.get("tasks_url")
    if base_url:
        parsed = urllib.parse.urlparse(base_url)
        params = urllib.parse.parse_qs(parsed.query)
        if cached_package:
            params["version"] = [cached_package.get("version", "")]
        url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(params, doseq=True)))
    else:
        query = {"lang": config.get("lang", "zh")}
        if cached_package:
            query["version"] = cached_package.get("version", "")
        url = f"{config['api_base'].rstrip('/')}/api/tasks?{urllib.parse.urlencode(query)}"

    headers = {"Accept": "application/json"}
    ticket = session.get("ticket")
    if ticket:
        headers["X-GIGO-Session-Ticket"] = ticket
    return urllib.request.Request(url, headers=headers)


def fetch_task_package(config: dict, repo_root: Path) -> list[Task]:
    if is_v2_runtime(config):
        return fetch_v2_task_package(config, repo_root)

    cache_path = _cache_path(config, repo_root)
    fallback_path = _fallback_package_path(config, repo_root)
    cached_package = load_json(cache_path) if cache_path.exists() else None
    bundle_key = load_task_bundle_key()

    if config.get("offline_mode"):
        fallback_package = load_json(fallback_path)
        _remember_package_meta(config, fallback_package, "offline_fallback")
        return _package_to_tasks(fallback_package, bundle_key)

    request = _build_remote_request(config, cached_package)

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
            write_json(cache_path, payload)
            source = "remote_session" if config.get("task_session") else "remote"
            _remember_package_meta(config, payload, source)
            return _package_to_tasks(payload, bundle_key)
    except urllib.error.HTTPError as error:
        if error.code == 304 and cached_package:
            _remember_package_meta(config, cached_package, "cache_304")
            return _package_to_tasks(cached_package, bundle_key)
        if config.get("task_session") and error.code in {401, 403}:
            config["task_bundle_warning"] = (
                "云端题包会话已失效，已回退到缓存或 demo 包。"
                if config.get("lang", "zh") == "zh"
                else "The remote task session expired, so the run fell back to the cached or demo bundle."
            )
    except TaskBundleCryptoError as error:
        config["task_bundle_warning"] = str(error)
    except Exception:
        pass

    if cached_package:
        try:
            _remember_package_meta(config, cached_package, "cache_fallback")
            return _package_to_tasks(cached_package, bundle_key)
        except TaskBundleCryptoError as error:
            config["task_bundle_warning"] = str(error)
    fallback_package = load_json(fallback_path)
    _remember_package_meta(config, fallback_package, "embedded_fallback", config.get("task_bundle_warning"))
    return _package_to_tasks(fallback_package, bundle_key)
