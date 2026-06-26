#!/usr/bin/env python3
"""Wrapper for helloene/live-album-downloader.

Accepts a PhotoPlus live URL or numeric activity ID, prepares the upstream
project if needed, and forwards supported CLI flags.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


REPO_URL = "https://github.com/helloene/live-album-downloader.git"
RAW_SCRIPT_URL = (
    "https://raw.githubusercontent.com/helloene/live-album-downloader/main/"
    "live_album_downloader.py"
)
DEFAULT_REPO_DIR = Path(".codex") / "live-album-downloader"


def parse_activity_id(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"[1-9]\d*", value):
        return value

    patterns = [
        r"/live/pc/([1-9]\d*)",
        r"/live/([1-9]\d*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)

    numbers = re.findall(r"[1-9]\d{4,}", value)
    if len(numbers) == 1:
        return numbers[0]

    raise SystemExit(
        "Could not find a PhotoPlus activity ID. Expected a numeric ID or a "
        "URL like https://live.photoplus.cn/live/12345678"
    )


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_upstream(repo_dir: Path) -> Path:
    script = repo_dir / "live_album_downloader.py"
    if script.exists():
        return script

    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("git"):
        try:
            run(["git", "clone", "--depth", "1", REPO_URL, str(repo_dir)])
            return script
        except subprocess.CalledProcessError:
            pass

    repo_dir.mkdir(parents=True, exist_ok=True)
    print(f"+ download {RAW_SCRIPT_URL} -> {script}", flush=True)
    urllib.request.urlretrieve(RAW_SCRIPT_URL, script)
    return script


def install_dependencies(repo_dir: Path) -> None:
    requirements = repo_dir / "requirements.txt"
    if requirements.exists():
        run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
    else:
        run([sys.executable, "-m", "pip", "install", "requests", "tqdm", "piexif"])


def build_args(args: argparse.Namespace, activity_id: str, script: Path) -> list[str]:
    cmd = [sys.executable, str(script), "--id", activity_id]

    forward_values = [
        ("--count", args.count),
        ("--tab", args.tab),
        ("--rename-template", args.rename_template),
        ("--folder-name", args.folder_name),
        ("--gps-lat", args.gps_lat),
        ("--gps-lon", args.gps_lon),
        ("--gps-alt", args.gps_alt),
    ]
    for flag, value in forward_values:
        if value is not None:
            cmd.extend([flag, str(value)])

    for flag_name, enabled in [
        ("--no-set-mtime", args.no_set_mtime),
        ("--save-metadata", args.save_metadata),
        ("--inspect", args.inspect),
        ("--write-caption", args.write_caption),
    ]:
        if enabled:
            cmd.append(flag_name)

    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a PhotoPlus live album via helloene/live-album-downloader."
    )
    parser.add_argument("album", help="PhotoPlus live URL or numeric activity ID")
    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path.cwd(),
        help="Directory where ./PhotoPlus output will be created.",
    )
    parser.add_argument(
        "--repo-dir",
        type=Path,
        default=DEFAULT_REPO_DIR,
        help="Local clone/cache path for helloene/live-album-downloader.",
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install upstream Python dependencies before running.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved command without cloning, installing, or downloading.",
    )
    parser.add_argument("--count")
    parser.add_argument("--tab")
    parser.add_argument("--rename-template")
    parser.add_argument("--folder-name")
    parser.add_argument("--no-set-mtime", action="store_true")
    parser.add_argument("--save-metadata", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--write-caption", action="store_true")
    parser.add_argument("--gps-lat")
    parser.add_argument("--gps-lon")
    parser.add_argument("--gps-alt")

    args = parser.parse_args()
    activity_id = parse_activity_id(args.album)

    if args.dry_run:
        fake_script = args.repo_dir / "live_album_downloader.py"
        print("activity_id=" + activity_id)
        print("workdir=" + str(args.workdir))
        print("command=" + " ".join(build_args(args, activity_id, fake_script)))
        return 0

    script = ensure_upstream(args.repo_dir)
    if args.install_deps:
        install_dependencies(args.repo_dir)

    args.workdir.mkdir(parents=True, exist_ok=True)
    run(build_args(args, activity_id, script.resolve()), cwd=args.workdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
