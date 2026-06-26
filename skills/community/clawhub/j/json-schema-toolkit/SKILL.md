---
name: json-schema-toolkit
description: Validate JSON data against JSON Schema, generate schemas from sample JSON, and convert schemas to TypeScript interfaces, Python dataclasses, or Markdown docs. Use when working with JSON validation, API contract testing, schema generation from examples, or converting JSON Schema to typed code. No external dependencies — pure Python.
---

# JSON Schema Toolkit

Validate, generate, and convert JSON Schemas with zero dependencies.

## Commands

All commands use `scripts/json_schema.py`.

### Generate Schema from Sample Data

```bash
python3 scripts/json_schema.py generate --input sample.json
python3 scripts/json_schema.py generate --input sample.json --output schema.json
echo '{"name":"Jo","age":25}' | python3 scripts/json_schema.py generate --input -
```

Auto-detects string formats (email, date-time, date, uri, ipv4).

### Validate JSON Against Schema

```bash
python3 scripts/json_schema.py validate --schema schema.json --data data.json
```

Reports all validation errors with JSON paths. Exit code 1 on failure.

### Convert Schema to Code

```bash
python3 scripts/json_schema.py convert --input schema.json --format typescript
python3 scripts/json_schema.py convert --input schema.json --format python-dataclass
python3 scripts/json_schema.py convert --input schema.json --format markdown --name User
```

Supported formats: `typescript`, `python-dataclass`, `markdown`.

## Supported Validation Keywords

type, enum, required, properties, additionalProperties, items, minLength, maxLength, pattern, minimum, maximum, minItems, maxItems, format.

## Stdin Support

Use `--input -` to pipe JSON from stdin for both `generate` and `validate --data`.
