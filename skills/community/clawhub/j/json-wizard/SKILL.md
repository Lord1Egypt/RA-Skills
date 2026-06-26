---
name: json-formatter
description: JSON formatting, validation, and conversion tool. Format, compress, validate JSON, and convert between JSON and YAML.
metadata: { "openclaw": { "emoji": "📋", "requires": { "bins": ["python3"] } } }
---

# JSON Formatter

A simple JSON formatting, validation, and conversion tool.

## Features

- **Format/Beautify** - Make JSON readable with proper indentation
- **Compress/Minify** - Remove whitespace for compact JSON
- **Validate** - Check JSON syntax and report errors
- **Convert** - JSON ↔ YAML conversion

## Usage

```bash
python3 skills/json-formatter/scripts/json_formatter.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `format` | Format JSON with indentation |
| `compress` | Minify JSON (remove whitespace) |
| `validate` | Validate JSON syntax |
| `to-yaml` | Convert JSON to YAML |
| `from-yaml` | Convert YAML to JSON |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--input` | string | - | Input string or file path |
| `--indent` | int | 2 | Indentation spaces (for format) |
| `--file` | bool | false | Treat input as file path |

## Examples

```bash
# Format JSON
python3 skills/json-formatter/scripts/json_formatter.py format --input '{"name":"test","value":123}'

# Compress JSON
python3 skills/json-formatter/scripts/json_formatter.py compress --input '{"name": "test", "value": 123}'

# Validate JSON
python3 skills/json-formatter/scripts/json_formatter.py validate --input '{"name":"test"}'

# Convert to YAML
python3 skills/json-formatter/scripts/json_formatter.py to-yaml --input '{"name":"test","items":[1,2,3]}'

# From YAML to JSON
python3 skills/json-formatter/scripts/json_formatter.py from-yaml --input 'name: test'
```

## Use Cases

1. **Debug API responses** - Format and inspect JSON data
2. **Reduce file size** - Compress JSON for storage/transmission
3. **Validate config files** - Check JSON syntax before deployment
4. **Convert formats** - Switch between JSON and YAML for different tools

## Current Status

In development.
