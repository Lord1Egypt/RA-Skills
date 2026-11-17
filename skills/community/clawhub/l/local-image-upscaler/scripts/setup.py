#!/usr/bin/env python3
"""Download and verify the portable image-upscaler runtime and models."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = SKILL_DIR / "assets" / "manifest.json"


def cache_root() -> Path:
    override = os.environ.get("IMAGE_UPSCALER_CACHE")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "image-upscaler"
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "image-upscaler"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def detect_platform() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "darwin":
        return "darwin-universal"
    if system == "windows" and machine in {"amd64", "x86_64"}:
        return "windows-x64"
    if system == "windows" and machine in {"arm64", "aarch64"}:
        raise RuntimeError(
            "Windows ARM is not supported by the pinned Vulkan runtime. "
            "Use an x64 Windows machine with a Vulkan-capable GPU."
        )
    raise RuntimeError(f"Unsupported platform: {system}/{machine}. Supported: macOS and Windows x64.")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mirror_prefixes(manifest: dict) -> list[str]:
    configured = os.environ.get("IMAGE_UPSCALER_MIRRORS", "")
    prefixes = [part.strip() for part in configured.split(",") if part.strip()]
    for prefix in manifest.get("default_mirror_prefixes", []):
        if prefix not in prefixes:
            prefixes.append(prefix)
    return prefixes


def candidate_urls(official_url: str, manifest: dict) -> list[str]:
    urls = []
    for prefix in mirror_prefixes(manifest):
        urls.append(prefix.replace("{url}", official_url) if "{url}" in prefix else prefix + official_url)
    urls.append(official_url)
    return list(dict.fromkeys(urls))


def download_verified(url: str, expected_hash: str, destination: Path, manifest: dict, offline: bool) -> None:
    if destination.exists() and sha256(destination) == expected_hash:
        print(f"Using verified cache: {destination}")
        return
    if offline:
        raise RuntimeError(f"Offline mode: verified cache is missing for {destination.name}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    errors = []
    for candidate in candidate_urls(url, manifest):
        temporary = destination.with_suffix(destination.suffix + ".part")
        try:
            if temporary.exists():
                temporary.unlink()
            print(f"Downloading: {candidate}")
            request = urllib.request.Request(candidate, headers={"User-Agent": "image-upscaler-skill/1.0"})
            with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
                shutil.copyfileobj(response, output, length=1024 * 1024)
            actual_hash = sha256(temporary)
            if actual_hash != expected_hash:
                raise RuntimeError(f"SHA-256 mismatch: expected {expected_hash}, got {actual_hash}")
            temporary.replace(destination)
            return
        except (OSError, urllib.error.URLError, RuntimeError) as exc:
            errors.append(f"{candidate}: {exc}")
            if temporary.exists():
                temporary.unlink()
    raise RuntimeError("All download sources failed:\n" + "\n".join(errors))


def safe_extract_zip(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if root != target and root not in target.parents:
                raise RuntimeError(f"Unsafe archive member: {member.filename}")
        bundle.extractall(destination)


def ensure_runtime(manifest: dict, platform_key: str, root: Path, offline: bool, force: bool) -> Path:
    spec = manifest["platforms"][platform_key]
    version = manifest["runtime_version"]
    runtime_dir = root / "runtime" / version / platform_key
    executable = runtime_dir / spec["archive_root"] / spec["executable"]
    if executable.exists() and not force:
        if sha256(executable) == spec["executable_sha256"]:
            print(f"Using verified runtime cache: {executable}")
            return executable
        print(f"Runtime cache failed executable verification; restoring: {executable}")

    archive = root / "downloads" / f"runtime-{version}-{platform_key}.zip"
    download_verified(spec["url"], spec["sha256"], archive, manifest, offline)
    safe_extract_zip(archive, runtime_dir)
    if not executable.exists():
        raise RuntimeError(f"Runtime archive did not contain {spec['executable']}")
    actual_executable_hash = sha256(executable)
    if actual_executable_hash != spec["executable_sha256"]:
        raise RuntimeError(
            "Extracted runtime executable failed SHA-256 verification: "
            f"expected {spec['executable_sha256']}, got {actual_executable_hash}"
        )
    if os.name != "nt":
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return executable


def ensure_model(manifest: dict, model_key: str, root: Path, offline: bool) -> tuple[Path, str]:
    spec = manifest["models"][model_key]
    model_dir = root / "models" / model_key
    for item in spec["files"]:
        download_verified(item["url"], item["sha256"], model_dir / item["name"], manifest, offline)
    return model_dir, spec["engine_name"]


def format_bytes(value: int) -> str:
    if value < 1024 * 1024:
        return f"{value / 1024:.1f} KiB"
    return f"{value / 1024 / 1024:.1f} MiB"


def model_is_cached(manifest: dict, model_key: str, root: Path) -> bool:
    spec = manifest["models"][model_key]
    model_dir = root / "models" / model_key
    return all((model_dir / item["name"]).exists() for item in spec["files"])


def model_catalog(manifest: dict, root: Path) -> list[dict]:
    profile_names: dict[str, list[str]] = {}
    for profile, spec in manifest.get("profiles", {}).items():
        profile_names.setdefault(spec["model"], []).append(profile)
    catalog = []
    for key, spec in manifest["models"].items():
        catalog.append({
            "model": key,
            "label": spec.get("label", key),
            "download_bytes": spec.get("download_bytes", 0),
            "cached": model_is_cached(manifest, key, root),
            "profiles": profile_names.get(key, []),
            "best_for": spec.get("best_for", ""),
            "tradeoff": spec.get("tradeoff", ""),
        })
    return catalog


def print_catalog(manifest: dict, root: Path, as_json: bool) -> None:
    catalog = model_catalog(manifest, root)
    if as_json:
        print(json.dumps({"cache": str(root), "models": catalog}, ensure_ascii=False, indent=2))
        return
    print(f"Cache: {root}")
    for item in catalog:
        status = "cached" if item["cached"] else f"download {format_bytes(item['download_bytes'])}"
        profiles = ", ".join(item["profiles"]) or "manual"
        print(f"- {item['model']} ({item['label']}): {status}; profiles={profiles}")
        print(f"  Best for: {item['best_for']}")
        print(f"  Trade-off: {item['tradeoff']}")


def parse_args(manifest: dict) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--model", choices=tuple(manifest["models"]), help="Install one low-level model")
    selection.add_argument("--profile", choices=tuple(manifest.get("profiles", {})), help="Install the model used by a profile")
    selection.add_argument("--all-models", action="store_true", help="Install every optional model")
    parser.add_argument("--platform", choices=("auto", "darwin-universal", "windows-x64"), default="auto")
    parser.add_argument("--offline", action="store_true", help="Forbid network access")
    parser.add_argument("--force", action="store_true", help="Re-extract the verified runtime")
    parser.add_argument("--download-only", action="store_true", help="Prepare files without executing the runtime")
    parser.add_argument("--list-models", action="store_true", help="Show model strengths, trade-offs, cache status, and download sizes")
    parser.add_argument("--json", action="store_true", help="Print machine-readable paths")
    return parser.parse_args()


def main() -> int:
    manifest = load_manifest()
    args = parse_args(manifest)
    root = cache_root()
    if args.list_models:
        print_catalog(manifest, root, args.json)
        return 0

    if args.all_models:
        model_keys = list(manifest["models"])
        selected_profile = None
    elif args.profile:
        model_keys = [manifest["profiles"][args.profile]["model"]]
        selected_profile = args.profile
    else:
        model_keys = [args.model or manifest["profiles"]["default"]["model"]]
        selected_profile = "default" if args.model is None else None

    additional_bytes = sum(
        manifest["models"][key].get("download_bytes", 0)
        for key in model_keys
        if not model_is_cached(manifest, key, root)
    )
    if not args.json:
        if selected_profile:
            print(f"Selected profile: {selected_profile} -> {model_keys[0]}")
        print(f"Additional model download: {format_bytes(additional_bytes)}")

    platform_key = detect_platform() if args.platform == "auto" else args.platform
    executable = ensure_runtime(manifest, platform_key, root, args.offline, args.force)
    installed_models = []
    for model_key in model_keys:
        model_dir, engine_name = ensure_model(manifest, model_key, root, args.offline)
        installed_models.append({
            "model": model_key,
            "model_dir": str(model_dir),
            "model_name": engine_name,
        })
    result = {
        "cache": str(root),
        "platform": platform_key,
        "runtime": str(executable),
        "profile": selected_profile,
        "models": installed_models,
        "download_only": args.download_only,
    }
    if len(installed_models) == 1:
        result["model_dir"] = installed_models[0]["model_dir"]
        result["model_name"] = installed_models[0]["model_name"]
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("Ready.")
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, zipfile.BadZipFile) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
