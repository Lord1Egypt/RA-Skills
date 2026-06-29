from __future__ import annotations

import argparse
import json

import gitea_api as g


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    items = []
    for item in g.list_tree(args.owner, args.repo):
        path = item.get("path", "")
        if path.endswith(".md") or path.endswith(".markdown"):
            items.append({"path": path, "size": item.get("size", 0), "sha": item.get("sha", "")})
    print(json.dumps({"success": True, "items": items}, ensure_ascii=False))


if __name__ == "__main__":
    main()
