#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Validate structured content output against required fields.")
    parser.add_argument("--schema", required=True)
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    schemas = load_json(base / "config" / "output_schemas.json")
    if args.schema not in schemas:
        print(f"Unknown schema: {args.schema}", file=sys.stderr)
        sys.exit(2)

    data = load_json(Path(args.input_file))
    required = schemas[args.schema].get("required", [])
    missing = [field for field in required if field not in data]

    if missing:
        print(json.dumps({"ok": False, "missing_fields": missing}, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps({"ok": True, "schema": args.schema, "checked_fields": required}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
