#!/usr/bin/env python3
"""Collect selected machine configs into a portable tar.gz bundle."""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

BUNDLE_ROOT_NAME = "machine-config-bundle"

COMPONENT_PATHS: dict[str, list[str]] = {
    "tmux": [
        ".tmux.conf",
        ".tmux",
        ".config/tmux/tmux.conf",
    ],
    "vim": [
        ".vimrc",
        ".vim",
        ".config/nvim",
    ],
    "emacs": [
        ".emacs",
        ".emacs.d",
        ".config/emacs",
    ],
    "zsh": [
        ".zshrc",
        ".zprofile",
        ".zshenv",
        ".zlogin",
        ".config/zsh",
        ".oh-my-zsh",
    ],
    "alfred": [
        "Library/Application Support/Alfred/Alfred.alfredpreferences",
    ],
    "git": [
        ".gitconfig",
        ".gitignore",
        ".gitignore_global",
    ],
    "ssh": [
        ".ssh/config",
        ".ssh/known_hosts",
    ],
}

TMUX_PLUGIN_RE = re.compile(r"@plugin\s+['\"]?([^'\"\s#]+)")
ZSH_PLUGINS_BLOCK_RE = re.compile(r"plugins=\((.*?)\)", re.DOTALL)
ZSH_WORD_RE = re.compile(r"[A-Za-z0-9._+-]+")
VIM_PLUG_RE = re.compile(r"(?:Plug|Plugin)\s*['\"]([^'\"]+)['\"]")
REPO_TOKEN_RE = re.compile(r"['\"]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)['\"]")
EMACS_USE_PACKAGE_RE = re.compile(r"\(use-package\s+([^\s\)]+)")
EMACS_PACKAGE_INSTALL_RE = re.compile(r"\(package-install\s+'([^\s\)]+)")


def parse_components(raw: str | None) -> list[str]:
    if not raw:
        return list(COMPONENT_PATHS.keys())
    requested = [item.strip().lower() for item in raw.split(",") if item.strip()]
    invalid = sorted(set(requested) - set(COMPONENT_PATHS))
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Unsupported components: {', '.join(invalid)}. "
            f"Valid components: {', '.join(COMPONENT_PATHS)}"
        )
    deduped: list[str] = []
    for item in requested:
        if item not in deduped:
            deduped.append(item)
    return deduped


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def normalize_items(values: Iterable[str]) -> list[str]:
    cleaned = {value.strip() for value in values if value and value.strip()}
    return sorted(cleaned)


def find_existing_paths(home: Path, rel_paths: Iterable[str]) -> list[str]:
    found: list[str] = []
    for rel_path in rel_paths:
        candidate = home / rel_path
        if candidate.exists():
            found.append(rel_path)
    return found


def copy_into_payload(source_home: Path, rel_path: str, payload_home: Path) -> None:
    src = source_home / rel_path
    dst = payload_home / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir() and not src.is_symlink():
        shutil.copytree(src, dst, symlinks=True, dirs_exist_ok=True)
    else:
        if dst.exists():
            dst.unlink()
        shutil.copy2(src, dst, follow_symlinks=False)


def discover_tmux_plugins(home: Path) -> dict[str, list[str]]:
    conf_candidates = [
        home / ".tmux.conf",
        home / ".config/tmux/tmux.conf",
    ]
    plugins: list[str] = []
    for candidate in conf_candidates:
        if not candidate.exists():
            continue
        plugins.extend(TMUX_PLUGIN_RE.findall(read_text(candidate)))
    return {"plugins": normalize_items(plugins)} if plugins else {}


def discover_vim_plugins(home: Path) -> dict[str, list[str]]:
    config_files: list[Path] = []
    for rel_path in [".vimrc", ".vim/vimrc", ".config/nvim/init.vim", ".config/nvim/init.lua"]:
        candidate = home / rel_path
        if candidate.exists() and candidate.is_file():
            config_files.append(candidate)

    lua_root = home / ".config/nvim/lua"
    if lua_root.exists():
        config_files.extend(sorted(lua_root.rglob("*.lua")))

    plugins: list[str] = []
    repos: list[str] = []
    for config in config_files:
        text = read_text(config)
        plugins.extend(VIM_PLUG_RE.findall(text))
        repos.extend(REPO_TOKEN_RE.findall(text))

    inventory = {}
    if plugins:
        inventory["plug_style"] = normalize_items(plugins)
    if repos:
        inventory["repos"] = normalize_items(repos)
    return inventory


def discover_emacs_plugins(home: Path) -> dict[str, list[str]]:
    config_files = [
        home / ".emacs",
        home / ".emacs.d/init.el",
        home / ".emacs.d/early-init.el",
        home / ".config/emacs/init.el",
    ]
    packages: list[str] = []
    for config in config_files:
        if not config.exists() or not config.is_file():
            continue
        text = read_text(config)
        packages.extend(EMACS_USE_PACKAGE_RE.findall(text))
        packages.extend(EMACS_PACKAGE_INSTALL_RE.findall(text))
    return {"packages": normalize_items(packages)} if packages else {}


def discover_zsh_plugins(home: Path) -> dict[str, list[str]]:
    candidates = [
        home / ".zshrc",
        home / ".config/zsh/.zshrc",
        home / ".config/zsh/zshrc",
    ]
    plugins: list[str] = []
    for candidate in candidates:
        if not candidate.exists() or not candidate.is_file():
            continue
        text = read_text(candidate)
        for block in ZSH_PLUGINS_BLOCK_RE.findall(text):
            plugins.extend(ZSH_WORD_RE.findall(block))
    return {"plugins": normalize_items(plugins)} if plugins else {}


def discover_alfred_plugins(home: Path) -> dict[str, object]:
    base = home / "Library/Application Support/Alfred/Alfred.alfredpreferences"
    workflows_dir = base / "workflows"
    if not workflows_dir.exists() or not workflows_dir.is_dir():
        return {}

    workflows: list[dict[str, str]] = []
    for wf_dir in sorted(workflows_dir.iterdir()):
        if not wf_dir.is_dir():
            continue
        info_path = wf_dir / "info.plist"
        name = wf_dir.name
        if info_path.exists():
            try:
                with info_path.open("rb") as handle:
                    plist = plistlib.load(handle)
                if isinstance(plist, dict) and isinstance(plist.get("name"), str):
                    name = plist["name"]
            except Exception:
                pass
        workflows.append({"id": wf_dir.name, "name": name})
    return {"workflow_count": len(workflows), "workflows": workflows}


def discover_plugins(component: str, home: Path) -> dict[str, object]:
    if component == "tmux":
        return discover_tmux_plugins(home)
    if component == "vim":
        return discover_vim_plugins(home)
    if component == "emacs":
        return discover_emacs_plugins(home)
    if component == "zsh":
        return discover_zsh_plugins(home)
    if component == "alfred":
        return discover_alfred_plugins(home)
    return {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect machine configuration into a portable bundle.",
    )
    parser.add_argument(
        "--bundle",
        required=True,
        help="Output tar.gz file path, e.g. ~/machine-config-bundle.tar.gz",
    )
    parser.add_argument(
        "--components",
        help="Comma-separated list of components. Default: all supported.",
    )
    parser.add_argument(
        "--home",
        default="~",
        help="Source home directory. Default: current user's home.",
    )
    parser.add_argument(
        "--no-plugin-scan",
        action="store_true",
        help="Skip plugin inventory discovery.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress logs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    components = parse_components(args.components)
    source_home = Path(args.home).expanduser().resolve()
    bundle_path = Path(args.bundle).expanduser().resolve()
    bundle_path.parent.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "bundle_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_home": str(source_home),
        "components_requested": components,
        "components_included": {},
        "notes": [
            "ssh component intentionally excludes private keys.",
            "Run apply_config_bundle.py with --dry-run before writing on target machine.",
        ],
    }

    with tempfile.TemporaryDirectory(prefix="machine-config-bundle-") as tmp:
        tmp_root = Path(tmp) / BUNDLE_ROOT_NAME
        payload_home = tmp_root / "payload" / "home"
        payload_home.mkdir(parents=True, exist_ok=True)

        included_count = 0
        for component in components:
            existing_paths = find_existing_paths(source_home, COMPONENT_PATHS[component])
            if not existing_paths:
                if args.verbose:
                    print(f"[skip] {component}: no supported paths found")
                continue

            for rel_path in existing_paths:
                copy_into_payload(source_home, rel_path, payload_home)
                if args.verbose:
                    print(f"[copy] {component}: {rel_path}")

            component_info: dict[str, object] = {"paths": existing_paths}
            if not args.no_plugin_scan:
                plugin_inventory = discover_plugins(component, source_home)
                if plugin_inventory:
                    component_info["plugins"] = plugin_inventory
                    if args.verbose:
                        print(f"[plugins] {component}: inventory captured")

            manifest["components_included"][component] = component_info
            included_count += 1

        manifest_path = tmp_root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with tarfile.open(bundle_path, mode="w:gz") as archive:
            archive.add(tmp_root, arcname=BUNDLE_ROOT_NAME)

    print(f"Bundle written: {bundle_path}")
    print(f"Components included: {included_count}")
    print("Included keys:", ", ".join(sorted(manifest["components_included"].keys())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
