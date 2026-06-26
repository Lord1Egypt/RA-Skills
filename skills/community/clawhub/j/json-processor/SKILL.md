---
name: json-processor
description: "JSON query, validate, diff, transform, format, flatten, and stats toolkit with a jq-like interface. Uses Python stdlib only — no external dependencies. Use when Codex needs to: (1) Query JSON with JSONPath expressions ($.key[*].sub), (2) Validate JSON against a schema, (3) Diff two JSON files for changes, (4) Transform JSON with jq-like expressions, (5) Pretty-print or flatten deeply nested JSON, (6) Analyze JSON structure statistics."
---

# JSON Processor (json-processor)

Query, validate, diff, transform, and analyze JSON — all with Python stdlib.

## Quick start

```bash
# Query
python3 skills/json-processor/scripts/json_processor.py query data.json "$.store.book[*].title"

# Validate
python3 skills/json-processor/scripts/json_processor.py validate data.json --schema schema.json

# Diff
python3 skills/json-processor/scripts/json_processor.py diff old.json new.json

# Transform (jq-like)
python3 skills/json-processor/scripts/json_processor.py transform data.json --jq '{names: .[].name}'

# Pretty-print
python3 skills/json-processor/scripts/json_processor.py format data.json --indent 2

# Flatten nested JSON
python3 skills/json-processor/scripts/json_processor.py flatten data.json

# Stats
python3 skills/json-processor/scripts/json_processor.py stats data.json
```

## Commands

### query — JSONPath-style query

```bash
python3 json_processor.py query data.json "$.store.book[*].title"
python3 json_processor.py query data.json "$.store.bicycle.color"
python3 json_processor.py query data.json "$[0].name"
```

Supports: `$.key`, `.key.sub`, `[0]`, `[*]`, mixed like `.store.book[*].title`

### validate — JSON Schema validation

```bash
python3 json_processor.py validate data.json --schema schema.json
```

Conforms to JSON Schema draft-07 subset: type, enum, pattern, min/maxLength, min/maximum, required, properties, items, additionalProperties.

### diff — Recursive JSON diff

```bash
python3 json_processor.py diff old.json new.json
```

Output:
```
📋 Differences (3):
  $.name: "Old App" → "New App"
  $.version: added → "2.0.0"
  $.features[1]: "logging" → "telemetry"
```

### transform — jq-like transform

```bash
python3 json_processor.py transform data.json --jq '.name'
python3 json_processor.py transform data.json --jq '{persons: .[].name}'
python3 json_processor.py transform data.json --jq '.[].items[0]'
```

### format — Pretty-print JSON

```bash
python3 json_processor.py format data.json
python3 json_processor.py format data.json --indent 4 --sort-keys
python3 json_processor.py format data.json --compact
python3 json_processor.py format data.json --output pretty.json
cat data.json | python3 json_processor.py format -
```

### flatten — Flatten nested JSON to dot-notation

```bash
python3 json_processor.py flatten data.json
# {"user.name": "Alice", "user.age": 30, "tags[0]": "admin"}
```

### stats — JSON structure statistics

```bash
python3 json_processor.py stats data.json
# 📊 JSON Statistics
#   Total nodes:     142
#   Max depth:       5
#   Types:           dict: 28, list: 6, str: 80, int: 22, bool: 6
#   Top keys:        name: 15, id: 15, type: 12
```

## Requirements

- Python 3.6+ (stdlib only — no pip install needed)
- No external dependencies
- Works on Linux, macOS, Windows
