from __future__ import annotations

import argparse
import json

import cards
import catalog
import duplicate


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_path", default="")
    args = parser.parse_args()
    cat = catalog.read(args.owner, args.repo)
    result = duplicate.find_duplicate(cat, args.title, args.source_id, args.source_path)
    result["success"] = True
    if result.get("duplicate") or result.get("possible_duplicate"):
        result["needs_confirm"] = True
        result["interactive_card"] = cards.duplicate_confirm(
            args.title,
            result.get("existing", {}),
            possible=bool(result.get("possible_duplicate")),
        )
    out(result)


if __name__ == "__main__":
    main()
