from __future__ import annotations

import argparse
import json

import summary_templates as templates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type_key", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_path", default="")
    parser.add_argument("--save_to", default="")
    args = parser.parse_args()
    data = {
        "type_key": args.type_key,
        "title": args.title,
        "rules": templates.COMMON_RULES,
        "sections": templates.sections_for(args.type_key),
        "source_id": args.source_id,
        "source_path": args.source_path,
    }
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.save_to:
        open(args.save_to, "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
