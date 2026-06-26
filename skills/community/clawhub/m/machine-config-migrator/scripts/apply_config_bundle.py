#!/usr/bin/env python3
"""Apply a collected machine config bundle to a target home directory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Iterable

BUNDLE_ROOT_NAME = "machine-config-bundle"


def parse_components(raw: str | None, available: Iterable[str]) -> list[str]:
    available_set = set(available)
    if not raw:
        return sorted(available_set)
    requested = [item.strip().lower() for item in raw.split(",") if item.strip()]
    invalid = sorted(set(requested) - available_set)
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Unsupported components for this bundle: {', '.join(invalid)}. "
            f"Available: {', '.join(sorted(available_set))}"
        )
    deduped: list[str] = []
    for item in requested:
        if item not in deduped:
            deduped.append(item)
    return deduped


def safe_extract_tar(archive: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.getmembers():
        member_path = (destination / member.name).resolve()
        if not str(member_path).startswith(str(destination)):
            raise ValueError(f"Unsafe tar member path: {member.name}")
    archive.extractall(path=destination)


def locate_bundle_root(bundle: Path, extracted_root: Path | None = None) -> Path:
    candidates = []
    if extracted_root:
        candidates.append(extracted_root / BUNDLE_ROOT_NAME)
        candidates.append(extracted_root)
    else:
        candidates.append(bundle)
        candidates.append(bundle / BUNDLE_ROOT_NAME)

    for candidate in candidates:
        manifest = candidate / "manifest.json"
        payload_home = candidate / "payload" / "home"
        if manifest.exists() and payload_home.exists():
            return candidate
    raise FileNotFoundError("Could not find bundle root with manifest.json and payload/home.")


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.exists():
        shutil.rmtree(path)


def copy_path(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_symlink():
        remove_path(dst)
        target = os.readlink(src)
        dst.symlink_to(target)
    elif src.is_dir():
        remove_path(dst)
        shutil.copytree(src, dst, symlinks=True)
    else:
        remove_path(dst)
        shutil.copy2(src, dst, follow_symlinks=False)


def backup_existing(dst: Path, backup_path: Path) -> None:
    if not dst.exists() and not dst.is_symlink():
        return
    copy_path(dst, backup_path)


def build_plugin_commands(target_home: Path, manifest: dict[str, object], selected: list[str]) -> list[str]:
    commands: list[str] = []
    included = manifest.get("components_included", {})
    if not isinstance(included, dict):
        return commands

    if "tmux" in selected:
        tpm_path = target_home / ".tmux/plugins/tpm"
        if tpm_path.exists():
            commands.append("~/.tmux/plugins/tpm/bin/install_plugins")
        else:
            commands.append(
                "git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm "
                "&& ~/.tmux/plugins/tpm/bin/install_plugins"
            )

    if "vim" in selected:
        init_vim = target_home / ".config/nvim/init.vim"
        init_lua = target_home / ".config/nvim/init.lua"
        vimrc = target_home / ".vimrc"

        if any(path.exists() and "plug#begin" in path.read_text(errors="ignore") for path in [vimrc, init_vim]):
            commands.append("vim +PlugInstall +qall || true")
        if init_lua.exists():
            text = init_lua.read_text(errors="ignore")
            if "lazy.nvim" in text:
                commands.append("nvim --headless '+Lazy! sync' +qa || true")
            if "packer" in text:
                commands.append("nvim --headless '+PackerSync' +qa || true")

    if "emacs" in selected:
        commands.append(
            "emacs --batch --eval "
            "\"(progn (require 'package) (package-initialize) "
            "(when (fboundp 'package-install-selected-packages') "
            "(package-refresh-contents) (package-install-selected-packages)))\" || true"
        )

    if "zsh" in selected:
        zsh_info = included.get("zsh", {})
        known_map = {
            "zsh-autosuggestions": "git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
            "zsh-syntax-highlighting": "git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
            "zsh-completions": "git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions",
        }
        if isinstance(zsh_info, dict):
            plugins = zsh_info.get("plugins", {})
            if isinstance(plugins, dict):
                names = plugins.get("plugins", [])
                if isinstance(names, list):
                    for name in names:
                        if isinstance(name, str) and name in known_map:
                            commands.append(known_map[name])

    return commands


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply a machine config bundle to a target home directory.",
    )
    parser.add_argument(
        "--bundle",
        required=True,
        help="Path to machine config bundle tar.gz or extracted bundle directory.",
    )
    parser.add_argument(
        "--components",
        help="Comma-separated list of components to apply. Default: all in bundle.",
    )
    parser.add_argument(
        "--target-home",
        default="~",
        help="Target home directory. Default: current user's home.",
    )
    parser.add_argument(
        "--backup-root",
        default="~/.local/share/machine-config-migrator/backups",
        help="Backup root directory for overwritten files.",
    )
    parser.add_argument(
        "--plugin-mode",
        choices=["none", "suggest", "run"],
        default="suggest",
        help="none: skip plugin handling; suggest: print commands; run: execute commands.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress logs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle_path = Path(args.bundle).expanduser().resolve()
    target_home = Path(args.target_home).expanduser().resolve()
    backup_root = Path(args.backup_root).expanduser().resolve()

    if not bundle_path.exists():
        raise FileNotFoundError(f"Bundle not found: {bundle_path}")

    tmp_dir: tempfile.TemporaryDirectory[str] | None = None
    try:
        if bundle_path.is_file():
            tmp_dir = tempfile.TemporaryDirectory(prefix="machine-config-apply-")
            extract_root = Path(tmp_dir.name)
            with tarfile.open(bundle_path, mode="r:*") as archive:
                safe_extract_tar(archive, extract_root)
            bundle_root = locate_bundle_root(bundle_path, extracted_root=extract_root)
        else:
            bundle_root = locate_bundle_root(bundle_path)

        manifest_path = bundle_root / "manifest.json"
        payload_home = bundle_root / "payload" / "home"
        manifest = json.loads(manifest_path.read_text())

        included = manifest.get("components_included", {})
        if not isinstance(included, dict):
            raise ValueError("Invalid manifest: components_included must be an object.")

        selected = parse_components(args.components, included.keys())
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = backup_root / timestamp

        print(f"Target home: {target_home}")
        print(f"Selected components: {', '.join(selected)}")
        if args.dry_run:
            print("Dry run mode: no files will be written.")
        else:
            backup_dir.mkdir(parents=True, exist_ok=True)
            print(f"Backup dir: {backup_dir}")

        writes = 0
        for component in selected:
            details = included.get(component, {})
            if not isinstance(details, dict):
                continue
            rel_paths = details.get("paths", [])
            if not isinstance(rel_paths, list):
                continue

            for rel_path_obj in rel_paths:
                if not isinstance(rel_path_obj, str):
                    continue
                src = payload_home / rel_path_obj
                dst = target_home / rel_path_obj

                if not src.exists() and not src.is_symlink():
                    print(f"[warn] missing in bundle: {rel_path_obj}")
                    continue

                print(f"[apply] {component}: {rel_path_obj}")
                if args.dry_run:
                    continue

                if dst.exists() or dst.is_symlink():
                    backup_path = backup_dir / rel_path_obj
                    backup_existing(dst, backup_path)
                copy_path(src, dst)
                writes += 1
                if args.verbose:
                    print(f"[ok] wrote {dst}")

        print(f"Files/paths applied: {writes}")

        plugin_commands = build_plugin_commands(target_home, manifest, selected)
        if args.plugin_mode == "none":
            return 0

        if plugin_commands:
            print("Plugin commands:")
            for command in plugin_commands:
                print(f"  - {command}")
        else:
            print("Plugin commands: none detected for selected components.")

        if args.plugin_mode == "run" and not args.dry_run:
            print("Running plugin commands...")
            for command in plugin_commands:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=target_home,
                    check=False,
                )
                if result.returncode != 0:
                    print(f"[warn] command failed ({result.returncode}): {command}")
        elif args.plugin_mode == "run" and args.dry_run:
            print("[note] --dry-run prevents running plugin commands.")
    finally:
        if tmp_dir is not None:
            tmp_dir.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
