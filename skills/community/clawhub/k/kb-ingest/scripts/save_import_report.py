from __future__ import annotations

import argparse
from pathlib import Path

import gitea_api as g
from path_utils import sanitize_filename


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--report_file", required=True)
    args = parser.parse_args()
    path = f"imports/{sanitize_filename(args.title)}.md"
    g.put_file(args.owner, args.repo, path, Path(args.report_file).read_text(encoding="utf-8"), f"research-kb import report: {args.title}")
    print({"success": True, "path": path})


if __name__ == "__main__":
    main()
