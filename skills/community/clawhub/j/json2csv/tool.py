#!/usr/bin/env python3
import argparse
import json
import csv
import sys
from typing import Any, Dict, List

def flatten_json(nested_json: Dict[Any, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested json object.
    """
    out = {}

    def flatten(obj: Any, name: str = ''):
        if type(obj) is dict:
            for key in obj:
                flatten(obj[key], f"{name}{key}{separator}")
        elif type(obj) is list:
            for i, item in enumerate(obj):
                flatten(item, f"{name}{i}{separator}")
        else:
            out[name[:-1]] = obj

    flatten(nested_json)
    return out

def json_to_csv(json_file: str, csv_file: str):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        print("JSON input must be a list or object")
        sys.exit(1)

    # Flatten all records
    flat_data = [flatten_json(item) for item in data]

    if not flat_data:
        print("No data to write.")
        sys.exit(1)

    # Get all unique headers
    fieldnames = set()
    for item in flat_data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_data)
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON file to CSV with flattened nested structures.")
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument("output", help="Output CSV file path")
    args = parser.parse_args()

    json_to_csv(args.input, args.output)
    print(f"Converted {args.input} to {args.output}")

if __name__ == "__main__":
    main()
