#!/usr/bin/env python3
"""JSON Schema Toolkit — validate JSON against schemas, generate schemas from samples, and convert between formats.

Usage:
  python3 json_schema.py validate --schema schema.json --data data.json
  python3 json_schema.py generate --input sample.json [--output schema.json]
  python3 json_schema.py convert --input schema.json --format <typescript|python-dataclass|markdown>
  echo '{"name":"Jo"}' | python3 json_schema.py generate --input -
"""

import argparse
import json
import sys
import os
from collections import OrderedDict


def infer_type(value):
    """Infer JSON Schema type from a Python value."""
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        schema = {"type": "string"}
        if value and len(value) > 0:
            # Detect common string formats
            import re
            if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', value):
                schema["format"] = "date-time"
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                schema["format"] = "date"
            elif re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
                schema["format"] = "email"
            elif re.match(r'^https?://', value):
                schema["format"] = "uri"
            elif re.match(r'^\d{1,3}(\.\d{1,3}){3}$', value):
                schema["format"] = "ipv4"
        return schema
    if isinstance(value, list):
        if not value:
            return {"type": "array", "items": {}}
        item_schemas = [infer_type(item) for item in value]
        # If all items have the same type, use that
        types_seen = set()
        for s in item_schemas:
            types_seen.add(json.dumps(s, sort_keys=True))
        if len(types_seen) == 1:
            return {"type": "array", "items": item_schemas[0]}
        else:
            return {"type": "array", "items": {"oneOf": item_schemas}}
    if isinstance(value, dict):
        return generate_object_schema(value)
    return {}


def generate_object_schema(obj):
    """Generate JSON Schema for a dict object."""
    properties = OrderedDict()
    required = []
    for key, val in obj.items():
        properties[key] = infer_type(val)
        if val is not None:
            required.append(key)
    schema = {
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required
    return schema


def generate_schema(data):
    """Generate a full JSON Schema document from sample data."""
    inner = infer_type(data)
    schema = OrderedDict()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema.update(inner)
    return schema


def validate_json(schema, data):
    """Validate JSON data against a schema using a basic recursive validator."""
    errors = []
    _validate(schema, data, "$", errors)
    return errors


def _validate(schema, data, path, errors):
    """Recursive schema validation (covers common JSON Schema keywords)."""
    if not schema or not isinstance(schema, dict):
        return

    # Handle $ref (not supported in basic mode)
    if "$ref" in schema:
        return  # Skip refs in basic validation

    # Type check
    schema_type = schema.get("type")
    if schema_type:
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }
        if schema_type in type_map:
            expected = type_map[schema_type]
            if not isinstance(data, expected):
                # int passes for number
                if schema_type == "number" and isinstance(data, (int, float)) and not isinstance(data, bool):
                    pass
                else:
                    errors.append(f"{path}: expected type '{schema_type}', got '{type(data).__name__}'")
                    return

    # Enum
    if "enum" in schema:
        if data not in schema["enum"]:
            errors.append(f"{path}: value {data!r} not in enum {schema['enum']}")

    # String constraints
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: string length {len(data)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: string length {len(data)} > maxLength {schema['maxLength']}")
        if "pattern" in schema:
            import re
            if not re.search(schema["pattern"], data):
                errors.append(f"{path}: string does not match pattern '{schema['pattern']}'")

    # Number constraints
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: {data} < minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: {data} > maximum {schema['maximum']}")

    # Object validation
    if isinstance(data, dict):
        props = schema.get("properties", {})
        required = schema.get("required", [])
        additional = schema.get("additionalProperties", True)

        for req in required:
            if req not in data:
                errors.append(f"{path}: missing required property '{req}'")

        for key, val in data.items():
            child_path = f"{path}.{key}"
            if key in props:
                _validate(props[key], val, child_path, errors)
            elif additional is False:
                errors.append(f"{child_path}: additional property not allowed")
            elif isinstance(additional, dict):
                _validate(additional, val, child_path, errors)

    # Array validation
    if isinstance(data, list):
        items_schema = schema.get("items", {})
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: array length {len(data)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(f"{path}: array length {len(data)} > maxItems {schema['maxItems']}")
        for i, item in enumerate(data):
            _validate(items_schema, item, f"{path}[{i}]", errors)


def schema_to_typescript(schema, name="Root", indent=0):
    """Convert JSON Schema to TypeScript interface."""
    pad = "  " * indent
    lines = []
    schema_type = schema.get("type", "any")

    if schema_type == "object":
        lines.append(f"{pad}interface {name} {{")
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        for key, prop in props.items():
            opt = "" if key in required else "?"
            ts_type = _ts_type(prop)
            lines.append(f"{pad}  {key}{opt}: {ts_type};")
        lines.append(f"{pad}}}")
    else:
        lines.append(f"{pad}type {name} = {_ts_type(schema)};")

    return "\n".join(lines)


def _ts_type(schema):
    """Map JSON Schema type to TypeScript type."""
    t = schema.get("type", "any")
    if t == "string":
        return "string"
    if t == "integer" or t == "number":
        return "number"
    if t == "boolean":
        return "boolean"
    if t == "null":
        return "null"
    if t == "array":
        items = schema.get("items", {})
        return f"{_ts_type(items)}[]"
    if t == "object":
        props = schema.get("properties", {})
        if not props:
            return "Record<string, unknown>"
        parts = []
        required = set(schema.get("required", []))
        for k, v in props.items():
            opt = "" if k in required else "?"
            parts.append(f"{k}{opt}: {_ts_type(v)}")
        return "{ " + "; ".join(parts) + " }"
    return "unknown"


def schema_to_python_dataclass(schema, name="Root"):
    """Convert JSON Schema to Python dataclass."""
    lines = ["from dataclasses import dataclass", "from typing import Optional, List, Any", "", ""]

    def _py_type(s):
        t = s.get("type", "Any")
        if t == "string":
            return "str"
        if t == "integer":
            return "int"
        if t == "number":
            return "float"
        if t == "boolean":
            return "bool"
        if t == "null":
            return "None"
        if t == "array":
            items = s.get("items", {})
            return f"List[{_py_type(items)}]"
        if t == "object":
            return "dict"
        return "Any"

    if schema.get("type") == "object":
        lines.append("@dataclass")
        lines.append(f"class {name}:")
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        if not props:
            lines.append("    pass")
        for key, prop in props.items():
            py_t = _py_type(prop)
            if key not in required:
                lines.append(f"    {key}: Optional[{py_t}] = None")
            else:
                lines.append(f"    {key}: {py_t}")

    return "\n".join(lines)


def schema_to_markdown(schema):
    """Convert JSON Schema to Markdown documentation."""
    lines = ["# Schema Documentation", ""]
    _md_props(schema, lines, depth=0)
    return "\n".join(lines)


def _md_props(schema, lines, depth=0):
    prefix = "  " * depth
    schema_type = schema.get("type", "unknown")
    if schema_type == "object":
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        for key, prop in props.items():
            req = " **(required)**" if key in required else ""
            fmt = f" (format: {prop['format']})" if "format" in prop else ""
            prop_type = prop.get("type", "unknown")
            lines.append(f"{prefix}- **{key}** (`{prop_type}`){req}{fmt}")
            if prop_type == "object":
                _md_props(prop, lines, depth + 1)
            elif prop_type == "array":
                items = prop.get("items", {})
                if items.get("type") == "object":
                    _md_props(items, lines, depth + 1)
    elif schema_type == "array":
        items = schema.get("items", {})
        lines.append(f"{prefix}- Array of `{items.get('type', 'unknown')}`")
        if items.get("type") == "object":
            _md_props(items, lines, depth + 1)


def load_json(path):
    """Load JSON from a file path or stdin (-)."""
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="JSON Schema Toolkit — validate, generate, and convert JSON schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s validate --schema schema.json --data data.json
  %(prog)s generate --input sample.json
  %(prog)s generate --input - < sample.json
  %(prog)s convert --input schema.json --format typescript
  %(prog)s convert --input schema.json --format python-dataclass
  %(prog)s convert --input schema.json --format markdown
"""
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # validate
    val_p = sub.add_parser("validate", help="Validate JSON data against a schema")
    val_p.add_argument("--schema", required=True, help="Path to JSON Schema file")
    val_p.add_argument("--data", required=True, help="Path to JSON data file (or - for stdin)")

    # generate
    gen_p = sub.add_parser("generate", help="Generate JSON Schema from sample data")
    gen_p.add_argument("--input", required=True, help="Path to sample JSON file (or - for stdin)")
    gen_p.add_argument("--output", help="Output file path (default: stdout)")

    # convert
    conv_p = sub.add_parser("convert", help="Convert JSON Schema to other formats")
    conv_p.add_argument("--input", required=True, help="Path to JSON Schema file")
    conv_p.add_argument("--format", required=True, choices=["typescript", "python-dataclass", "markdown"],
                        help="Output format")
    conv_p.add_argument("--name", default="Root", help="Name for the generated type/class (default: Root)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate":
        try:
            schema = load_json(args.schema)
            data = load_json(args.data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading files: {e}", file=sys.stderr)
            sys.exit(1)

        errors = validate_json(schema, data)
        if errors:
            print(f"❌ Validation failed with {len(errors)} error(s):")
            for err in errors:
                print(f"  • {err}")
            sys.exit(1)
        else:
            print("✅ Validation passed — data matches schema.")

    elif args.command == "generate":
        try:
            data = load_json(args.input)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading input: {e}", file=sys.stderr)
            sys.exit(1)

        schema = generate_schema(data)
        output = json.dumps(schema, indent=2)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output + "\n")
            print(f"✅ Schema written to {args.output}")
        else:
            print(output)

    elif args.command == "convert":
        try:
            schema = load_json(args.input)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading schema: {e}", file=sys.stderr)
            sys.exit(1)

        if args.format == "typescript":
            print(schema_to_typescript(schema, name=args.name))
        elif args.format == "python-dataclass":
            print(schema_to_python_dataclass(schema, name=args.name))
        elif args.format == "markdown":
            print(schema_to_markdown(schema))


if __name__ == "__main__":
    main()
