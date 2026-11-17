#!/usr/bin/env python3
"""Fail-closed release check for an omni-ecom package directory or ZIP."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from release_acceptance_guard import validate_receipt


ALLOWED_SUFFIXES = {".json", ".md", ".txt", ".png", ".py", ".yaml", ".yml"}
FORBIDDEN_NAMES = {".gitkeep"}
FORBIDDEN_PARTS = {"__pycache__"}
REQUIRED_AGENTS = {
    "omni-ecom-team-lead",
    "data-analyst",
    "platform-ops",
    "content-live-growth",
    "ad-profit-optimizer",
    "delivery-review",
}


def check_name(rel: str, errors: list[str]) -> None:
    path = PurePosixPath(rel)
    if path.name in FORBIDDEN_NAMES:
        errors.append(f"forbidden_file:{rel}")
    if any(part in FORBIDDEN_PARTS for part in path.parts):
        errors.append(f"forbidden_path:{rel}")
    suffix = path.suffix.casefold()
    if suffix == ".pyc":
        errors.append(f"forbidden_file_type:{rel}")
    elif suffix not in ALLOWED_SUFFIXES:
        errors.append(f"unsupported_file_type:{rel}")


def validate_manifest(manifest: dict[str, Any], version_info: dict[str, Any], files: set[str], prefix: str, errors: list[str], receipt: dict[str, Any] | None = None) -> str:
    version = str(manifest.get("version") or "")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?", version):
        errors.append("invalid_version")
    if str(version_info.get("team_version") or "") != version:
        errors.append("version_mismatch")
    if version_info.get('release_status')!='released' or version_info.get('release_ready') is not True:
        errors.append('release_not_ready')
    if '-' in version or not re.fullmatch(r'20\d{2}-\d{2}-\d{2}',str(version_info.get('release_date') or '')):
        errors.append('released_version_metadata_invalid')
    if version_info.get('release_status') == 'released' or version_info.get('release_ready') is True:
        if receipt is None:
            errors.append('release_acceptance_receipt_missing')
        else:
            errors.extend(validate_receipt(receipt, version))
    agents = manifest.get("agents") or []
    agent_ids = {PurePosixPath(str(item)).stem for item in agents}
    if agent_ids != REQUIRED_AGENTS:
        errors.append("agent_roster_mismatch")
    for rel in agents:
        normalized = str(PurePosixPath(prefix, str(rel).removeprefix("./")))
        if normalized not in files:
            errors.append(f"missing_agent:{rel}")
    members = {str(item.get("id")) for item in manifest.get("members", []) if isinstance(item, dict)}
    if members != REQUIRED_AGENTS:
        errors.append("member_roster_mismatch")
    return version


def validate_directory(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    if root.name != "omni-ecom":
        errors.append("root_folder_must_be_omni-ecom")
    paths = [path for path in root.rglob("*") if path.is_file()]
    files = {path.relative_to(root).as_posix() for path in paths}
    for rel in sorted(files):
        check_name(rel, errors)
    required = {"SKILL.md", ".codebuddy-plugin/plugin.json", "version-info.json"}
    for rel in sorted(required - files):
        errors.append(f"missing_required:{rel}")
    version = ""
    if not errors or required.issubset(files):
        try:
            manifest = json.loads((root / ".codebuddy-plugin" / "plugin.json").read_text(encoding="utf-8-sig"))
            version_info = json.loads((root / "version-info.json").read_text(encoding="utf-8-sig"))
            receipt = json.loads((root / "release-acceptance.json").read_text(encoding="utf-8-sig")) if "release-acceptance.json" in files else None
            version = validate_manifest(manifest, version_info, files, "", errors, receipt)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"metadata_unreadable:{exc}")
    return {
        "status": "PASS" if not errors else "FAIL",
        "target_type": "directory",
        "target": str(root),
        "root": root.name,
        "version": version,
        "file_count": len(files),
        "errors": sorted(set(errors)),
    }


def validate_zip(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    version = ""
    try:
        with zipfile.ZipFile(path) as archive:
            names = [name for name in archive.namelist() if not name.endswith("/")]
            roots = {PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts}
            if roots != {"omni-ecom"}:
                errors.append("zip_root_must_be_exactly_omni-ecom")
            files = set(names)
            for name in sorted(files):
                parts = PurePosixPath(name).parts
                check_name("/".join(parts[1:]) if len(parts) > 1 else name, errors)
            required = {
                "omni-ecom/SKILL.md",
                "omni-ecom/.codebuddy-plugin/plugin.json",
                "omni-ecom/version-info.json",
            }
            for rel in sorted(required - files):
                errors.append(f"missing_required:{rel}")
            if required.issubset(files):
                manifest = json.loads(archive.read("omni-ecom/.codebuddy-plugin/plugin.json").decode("utf-8-sig"))
                version_info = json.loads(archive.read("omni-ecom/version-info.json").decode("utf-8-sig"))
                receipt = json.loads(archive.read("omni-ecom/release-acceptance.json").decode("utf-8-sig")) if "omni-ecom/release-acceptance.json" in files else None
                version = validate_manifest(manifest, version_info, files, "omni-ecom", errors, receipt)
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"zip_unreadable:{exc}")
        files = set()
    return {
        "status": "PASS" if not errors else "FAIL",
        "target_type": "zip",
        "target": str(path),
        "root": "omni-ecom" if "omni-ecom" in {PurePosixPath(name).parts[0] for name in files if PurePosixPath(name).parts} else "",
        "version": version,
        "file_count": len(files),
        "errors": sorted(set(errors)),
    }


def validate(target: Path) -> dict[str, Any]:
    if target.is_dir():
        return validate_directory(target.resolve())
    if target.is_file() and target.suffix.casefold() == ".zip":
        return validate_zip(target.resolve())
    return {"status": "FAIL", "target": str(target), "errors": ["target_must_be_directory_or_zip"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an omni-ecom release directory or final ZIP")
    parser.add_argument("target", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output")
    args = parser.parse_args()
    result = validate(Path(args.target))
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(payload, end="")
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
