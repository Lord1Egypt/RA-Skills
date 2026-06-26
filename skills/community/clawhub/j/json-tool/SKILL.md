---
name: json-tool
description: Validate, format, and transform JSON data. Use when user needs to pretty print JSON, validate JSON syntax, minify JSON, extract JSON paths, or convert JSON to other formats.
---

# JSON Tool

Validate, format, and transform JSON data.

## Quick Start

```bash
# Format JSON
python scripts/json_tool.py data.json --format

# Validate JSON
python scripts/json_tool.py data.json --validate
```

## Usage

```bash
python scripts/json_tool.py [FILE] [OPTIONS]

Options:
  --format         Pretty print JSON
  --minify         Minify JSON
  --validate       Validate JSON syntax
  --query PATH     JSONPath query
  --convert FORMAT Convert to: yaml, csv, xml
  --sort-keys      Sort object keys
  --indent NUM     Indentation size
```

## Examples

```bash
# Pretty print
python scripts/json_tool.py data.json --format

# Minify
python scripts/json_tool.py data.json --minify

# Extract field
python scripts/json_tool.py data.json --query "items[0].name"

# Convert to YAML
python scripts/json_tool.py data.json --convert yaml

# Sort keys
python scripts/json_tool.py data.json --sort-keys
```

## Features

- Pretty printing
- Minification
- Validation
- JSONPath queries
- Format conversion (YAML, CSV, XML)
- Key sorting
