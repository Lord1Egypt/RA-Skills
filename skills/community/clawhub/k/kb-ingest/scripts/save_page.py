from __future__ import annotations

import argparse
from pathlib import Path

import gitea_api as g
from path_utils import sanitize_filename


FOLDERS = {
    "concept": "concepts",
    "resource": "resources",
    "review": "reviews",
    "import": "imports",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--kind", required=True, choices=sorted(FOLDERS))
    parser.add_argument("--name", required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    path = f"{FOLDERS[args.kind]}/{sanitize_filename(args.name)}.md"
    g.put_file(args.owner, args.repo, path, Path(args.file).read_text(encoding="utf-8"), f"research-kb {args.kind}: {args.name}")
    print({"success": True, "path": path})


if __name__ == "__main__":
    main()
