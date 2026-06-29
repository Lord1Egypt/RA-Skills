from __future__ import annotations

import argparse
import json

import catalog


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--source_file_id", default="")
    parser.add_argument("--source_path", default="")
    args = parser.parse_args()
    cat = catalog.read(args.owner, args.repo)
    for doc in cat.get("documents", []):
        if args.source_file_id and doc.get("source_file_id") == args.source_file_id:
            print(json.dumps({"duplicate": True, "path": doc.get("file"), "reason": "same_source_file_id"}, ensure_ascii=False))
            return
        if args.source_path and doc.get("source_path") == args.source_path:
            print(json.dumps({"duplicate": True, "path": doc.get("file"), "reason": "same_source_path"}, ensure_ascii=False))
            return
    print(json.dumps({"duplicate": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
