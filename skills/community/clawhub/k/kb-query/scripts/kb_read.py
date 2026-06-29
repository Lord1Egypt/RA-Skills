from __future__ import annotations

import argparse
import json
from pathlib import Path

import frontmatter
import gitea_api as g


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()
    content = g.read_text(args.owner, args.repo, args.path)
    print(json.dumps({
        "success": True,
        "path": args.path,
        "title": frontmatter.parse_title(content, Path(args.path).stem),
        "content": content,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
