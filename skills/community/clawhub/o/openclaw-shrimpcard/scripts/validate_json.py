#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def fail(message):
    print("[FAIL] " + message)
    sys.exit(1)


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as exc:
        fail(f"Cannot read JSON from {path}: {exc}")


def validate(payload: dict, schema: dict):
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: list(error.absolute_path))
    if errors:
        first = errors[0]
        path = ".".join(str(part) for part in first.absolute_path) or "<root>"
        fail(f"{path}: {first.message}")


def main():
    parser = argparse.ArgumentParser(description="Validate a JSON file against a JSON schema")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("--schema", required=True, help="Path to the JSON schema file")
    args = parser.parse_args()

    payload = load_json(Path(args.json_file))
    schema = load_json(Path(args.schema))
    validate(payload, schema)
    print("[OK] JSON is valid")


if __name__ == "__main__":
    main()
