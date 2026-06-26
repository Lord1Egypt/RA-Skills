#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


DEFAULT_PATHS = [
    Path("/home/z/Github/gstack"),
    Path.home() / "Github" / "gstack",
    Path.cwd() / "gstack",
]


def find_gstack() -> Path | None:
    for path in DEFAULT_PATHS:
        if (path / "README.md").exists() and (path / "plan-ceo-review" / "SKILL.md").exists():
            return path
    return None


def skill_files(root: Path) -> list[dict[str, str]]:
    files = []
    for skill in sorted(root.glob("*/SKILL.md")):
        files.append({"name": skill.parent.name, "path": str(skill)})
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Locate a local gstack clone and list upstream skill files.")
    parser.add_argument("--summary", action="store_true", help="Print a concise human-readable summary.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = find_gstack()
    payload = {
        "found": root is not None,
        "root": str(root) if root else None,
        "skills": skill_files(root) if root else [],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        if not root:
            print("gstack clone not found. Expected /home/z/Github/gstack or ~/Github/gstack.")
            return 1
        print(f"gstack: {root}")
        if args.summary:
            for item in payload["skills"]:
                print(f"- {item['name']}: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
