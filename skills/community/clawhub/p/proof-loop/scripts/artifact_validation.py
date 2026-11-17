"""Fail-closed validation of the JSON Schema subset used by bundled artifacts.

This checks artifact structure, not the truth of evidence or verifier identity.
"""
import re
from datetime import datetime


def validate(data, schema, path="artifact"):
    supported = {"$schema", "title", "description", "type", "required", "properties", "items", "enum", "minItems", "minLength", "pattern", "format", "additionalProperties"}
    unknown = set(schema) - supported
    if unknown:
        return [f"{path}: unsupported schema keywords {sorted(unknown)}"]
    errors = []
    kind = schema.get("type")
    types = {"object": dict, "array": list, "string": str}
    if kind is not None and (kind not in types or not isinstance(data, types[kind])):
        return [f"{path}: expected {kind}"]
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: invalid value {data!r}")
    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}: missing required key {key}")
        props = schema.get("properties", {})
        for key, value in data.items():
            if key in props:
                errors.extend(validate(value, props[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected key {key}")
    if isinstance(data, list):
        if len(data) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        for i, value in enumerate(data):
            if "items" in schema:
                errors.extend(validate(value, schema["items"], f"{path}[{i}]"))
    if isinstance(data, str):
        if len(data.strip()) < schema.get("minLength", 0):
            errors.append(f"{path}: empty or too short")
        if "pattern" in schema and not re.search(schema["pattern"], data):
            errors.append(f"{path}: invalid pattern")
        if schema.get("format") == "date-time":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", data):
                    raise ValueError()
                if datetime.fromisoformat(data.replace("Z", "+00:00")).tzinfo is None:
                    raise ValueError()
            except ValueError:
                errors.append(f"{path}: invalid date-time")
        elif "format" in schema:
            errors.append(f"{path}: unsupported format")
    return errors
