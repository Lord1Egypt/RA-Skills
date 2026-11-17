#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path


PACKAGE_NAME = "maybeai-sheet-cli"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLI_REPO = ROOT.parent / "maybeai-sheet-cli"


def _read_cli_version(cli_repo: Path) -> str:
    pyproject_path = cli_repo / "pyproject.toml"
    init_path = cli_repo / "src" / "maybeai_sheet" / "__init__.py"
    if not pyproject_path.exists():
        raise SystemExit(f"Missing CLI pyproject.toml: {pyproject_path}")
    if not init_path.exists():
        raise SystemExit(f"Missing CLI __init__.py: {init_path}")

    with pyproject_path.open("rb") as file:
        metadata = tomllib.load(file)
    pyproject_version = str(metadata.get("project", {}).get("version") or "")
    init_text = init_path.read_text()
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', init_text, re.MULTILINE)
    init_version = match.group(1) if match else ""
    if not pyproject_version or not init_version:
        raise SystemExit("Could not read both CLI version fields.")
    if pyproject_version != init_version:
        raise SystemExit(
            f"CLI version mismatch: pyproject.toml={pyproject_version}, __init__.py={init_version}"
        )
    return pyproject_version


def _check_pypi_version(version: str) -> None:
    url = f"https://pypi.org/pypi/{PACKAGE_NAME}/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise SystemExit(f"{PACKAGE_NAME} {version} is not published on PyPI yet.")
        raise SystemExit(f"PyPI check failed with HTTP {error.code}: {url}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"PyPI check failed: {error}") from error
    published_version = str(payload.get("info", {}).get("version") or "")
    if published_version != version:
        raise SystemExit(f"PyPI returned version {published_version!r}, expected {version!r}.")


def _update_skill_version(version: str) -> bool:
    skill_path = ROOT / "SKILL.md"
    text = skill_path.read_text()
    updated, count = re.subn(r"(?m)^version:\s*.+$", f"version: {version}", text, count=1)
    if count != 1:
        raise SystemExit("Could not update SKILL.md frontmatter version.")
    if updated == text:
        return False
    skill_path.write_text(updated)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync this skill after maybeai-sheet-cli is published to PyPI."
    )
    parser.add_argument(
        "--cli-repo",
        type=Path,
        default=DEFAULT_CLI_REPO,
        help="Path to the maybeai-sheet-cli repository.",
    )
    parser.add_argument(
        "--version",
        help="Expected published CLI version. Defaults to the version in the CLI repo.",
    )
    parser.add_argument(
        "--skip-pypi-check",
        action="store_true",
        help="Update from local CLI metadata without verifying PyPI publication.",
    )
    args = parser.parse_args()

    cli_repo = args.cli_repo.expanduser().resolve()
    cli_version = _read_cli_version(cli_repo)
    expected_version = args.version or cli_version
    if expected_version != cli_version:
        raise SystemExit(f"Expected {expected_version}, but CLI repo metadata says {cli_version}.")
    if not args.skip_pypi_check:
        _check_pypi_version(expected_version)

    changed = _update_skill_version(expected_version)
    status = "updated" if changed else "already current"
    print(f"{PACKAGE_NAME} skill version {status}: {expected_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
