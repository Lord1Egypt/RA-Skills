from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from .utils import Task
from .v2_bundle_tools import AUTHOR_BUNDLE_ROOT, load_bundle_manifest, load_manifest, materialize_archive


def is_v2_runtime(config: dict) -> bool:
    version = str(config.get("skill_version") or config.get("task_bundle_version") or "")
    return version.startswith("2.")


def _embedded_bundle_candidates(repo_root: Path) -> list[Path]:
    return [
        repo_root / "bundle",
        AUTHOR_BUNDLE_ROOT,
    ]


def _load_manifest_for_root(bundle_root: Path) -> dict:
    manifest_path = bundle_root / "manifest.json"
    if manifest_path.exists():
        return load_manifest(manifest_path)
    return load_bundle_manifest(bundle_root)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _load_tasks_from_bundle(bundle_root: Path, manifest: dict, lang: str) -> list[Task]:
    tasks: list[Task] = []
    task_manifest = {item["id"]: item for item in manifest.get("tasks", [])}
    for task_dir in sorted(path for path in (bundle_root / "tasks").iterdir() if path.is_dir()):
        task_yaml = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
        if not isinstance(task_yaml, dict):
            continue
        task_id = str(task_yaml["id"])
        manifest_entry = task_manifest.get(task_id, {})
        prompt_zh = _read_text(task_dir / "prompt.md")
        prompt_en = _read_text(task_dir / "prompt.en.md")
        prompt = prompt_en or prompt_zh if lang == "en" else prompt_zh or prompt_en
        title_zh = str(task_yaml.get("title_zh") or task_dir.name)
        title_en = str(task_yaml.get("title_en") or manifest_entry.get("title_en") or title_zh)
        tasks.append(
            Task(
                id=task_id,
                prompt=prompt,
                prompt_en=prompt_en,
                dish_name=title_en if lang == "en" and title_en else title_zh,
                dish_hint=f"{task_yaml.get('category', 'task')} · {task_yaml.get('difficulty', 'medium')}",
                primary_dimensions=[str(task_yaml.get("dimensions", {}).get("primary", "meat"))],
                secondary_dimensions=[str(item) for item in task_yaml.get("dimensions", {}).get("secondary", [])],
                timeout_seconds=int(task_yaml.get("timeout_seconds", 300)),
                rubric="",
                setup={},
                title_en=title_en,
                track=str(task_yaml.get("track", "A")),
                task_dir=str(task_dir),
                evaluators=list(task_yaml.get("evaluators", [])),
                metadata=dict(task_yaml.get("metadata", {})),
            )
        )
    return tasks


def _bundle_cache_root(config: dict) -> Path:
    return Path(str(config.get("bundle_cache_dir")))


def _download_remote_archive(config: dict, bundle_version: str, bundle_hash: str) -> tuple[Path, dict]:
    session = config.get("task_session") or {}
    session_id = session.get("session_id")
    ticket = session.get("ticket")
    if not session_id or not ticket:
        raise RuntimeError("missing v2 task session credentials for remote bundle download")

    params = urllib.parse.urlencode(
        {
            "lang": config.get("lang", "zh"),
            "session_id": session_id,
            "version": bundle_version,
        }
    )
    request = urllib.request.Request(
        f"{config['api_base'].rstrip('/')}/api/v2/bundle?{params}",
        headers={"Accept": "application/json", "X-GIGO-Session-Ticket": str(ticket)},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        archive = json.loads(response.read().decode("utf-8"))

    if str(archive.get("bundle_version")) != bundle_version:
        raise RuntimeError("remote v2 bundle version does not match the active session")
    if bundle_hash and str(archive.get("bundle_hash")) != bundle_hash:
        raise RuntimeError("remote v2 bundle hash does not match the active session")

    cache_root = _bundle_cache_root(config)
    destination = cache_root / bundle_version / str(config.get("lang", "zh"))
    remote_manifest = {
        "bundle_version": bundle_version,
        "bundle_hash": archive.get("bundle_hash", bundle_hash),
        "bundle_channel": archive.get("bundle_channel", session.get("bundle_channel", "stable")),
        "tasks": [],
    }
    return materialize_archive(archive, destination), remote_manifest


def fetch_v2_task_package(config: dict, repo_root: Path) -> list[Task]:
    selected_root: Path | None = None
    selected_manifest: dict | None = None
    expected_version = str((config.get("task_session") or {}).get("bundle_version") or "2.0.0")
    expected_hash = str((config.get("task_session") or {}).get("bundle_hash") or "")

    for candidate in _embedded_bundle_candidates(repo_root):
        if not candidate.exists() or not (candidate / "tasks").exists():
            continue
        manifest = _load_manifest_for_root(candidate)
        selected_root = candidate
        selected_manifest = manifest
        if manifest.get("bundle_version") == expected_version:
            break

    if not selected_root or not selected_manifest:
        raise RuntimeError("No embedded eval-v2 bundle is available")

    source = "embedded_author_bundle" if selected_root == AUTHOR_BUNDLE_ROOT else "embedded_public_bundle"
    if (
        expected_hash
        and selected_manifest.get("bundle_hash") != expected_hash
        and not config.get("offline_mode")
        and not config.get("force_embedded_bundle")
    ):
        selected_root, selected_manifest = _download_remote_archive(config, expected_version, expected_hash)
        source = "remote_archive"

    config["task_bundle_source"] = source
    config["task_bundle_version"] = selected_manifest.get("bundle_version", expected_version)
    config["task_bundle_hash"] = selected_manifest.get("bundle_hash", expected_hash)
    config["task_bundle_channel"] = selected_manifest.get("bundle_channel", "beta")
    config["runtime_mode"] = "v2"
    return _load_tasks_from_bundle(selected_root, selected_manifest, str(config.get("lang", "zh")))
