#!/usr/bin/env python3
"""
Validiert Tool-Outputs gegen ein Pydantic-Schema.
Für OpenClaw Tool-Call-Validierung.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    from pydantic import BaseModel, Field, create_model
except ImportError:
    print("Error: pydantic not installed", file=sys.stderr)
    sys.exit(1)

from json_processor import parse_and_validate, JSONValidationError


def create_dynamic_model(schema: dict) -> type:
    """Erstellt ein dynamisches Pydantic-Modell aus einem JSON-Schema."""
    fields = {}
    
    for field_name, field_info in schema.get("properties", {}).items():
        field_type = str  # Default
        
        json_type = field_info.get("type", "string")
        if json_type == "integer":
            field_type = int
        elif json_type == "number":
            field_type = float
        elif json_type == "boolean":
            field_type = bool
        elif json_type == "array":
            field_type = list
        elif json_type == "object":
            field_type = dict
            
        default = field_info.get("default", ...)
        if field_name not in schema.get("required", []):
            default = field_info.get("default", None)
            field_type = Optional[field_type]
        
        fields[field_name] = (field_type, Field(default=default, description=field_info.get("description", "")))
    
    return create_model("DynamicToolOutput", **fields)


def main():
    parser = argparse.ArgumentParser(description="Validate tool output against schema")
    parser.add_argument("json_input", help="JSON string or file path")
    parser.add_argument("--schema", "-s", required=True, help="JSON schema file")
    parser.add_argument("--file", "-f", action="store_true", help="Input is a file")
    parser.add_argument("--repair", "-r", action="store_true", default=True)
    parser.add_argument("--strict", action="store_true", help="Strict validation")
    
    args = parser.parse_args()
    
    # Lade Schema
    try:
        schema = json.loads(Path(args.schema).read_text())
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Lade Input
    try:
        if args.file:
            raw_input = Path(args.json_input).read_text()
        else:
            raw_input = args.json_input
    except Exception as e:
        print(f"Error loading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Erstelle dynamisches Modell und validiere
    try:
        model_class = create_dynamic_model(schema)
        result = parse_and_validate(raw_input, model_class, repair=args.repair, strict=args.strict)
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
    except JSONValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
