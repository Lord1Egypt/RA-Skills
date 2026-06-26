#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "manifest.json"
SKILL_PATH = REPO_ROOT / "SKILL.md"

REQUIRED_FIELDS = ["install", "filesystem_writes", "capabilities", "network_access"]


def _load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_skill_required_fields() -> dict:
    text = SKILL_PATH.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    front_matter = parts[1]
    data: dict[str, object] = {}
    for line in front_matter.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in REQUIRED_FIELDS and value:
            data[key] = json.loads(value)
    return data


def main() -> int:
    manifest = _load_manifest()
    skill = _load_skill_required_fields()

    missing = []
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            missing.append(f"manifest missing {field}")
        if field not in skill:
            missing.append(f"SKILL.md missing {field}")

    mismatches = []
    for field in REQUIRED_FIELDS:
        if field in manifest and field in skill and manifest[field] != skill[field]:
            mismatches.append(
                f"{field} mismatch: manifest={manifest[field]} skill={skill[field]}"
            )

    if missing or mismatches:
        for item in missing + mismatches:
            print(item)
        return 1

    print("metadata validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
