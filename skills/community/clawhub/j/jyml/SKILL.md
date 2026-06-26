---
name: jyml
description: This skill should be used when the user asks to "convert YAML to JSON", "convert JSON to YAML", "transform YAML file", "transform JSON file", "convert config file format", or needs to switch between YAML and JSON formats.
---

# jyml - YAML ↔ JSON Converter

Zero-config CLI for converting between YAML and JSON formats. Pass a file, get the converted file. No flags required.

## Prerequisites

Ensure jyml is available:

```bash
# Check if installed
which jyml

# Install globally if needed
npm install -g jyml

# Or use npx for one-off conversions
npx jyml <file>
```

Requires Node.js 18 or later.

## Basic Usage

```bash
jyml <file> [options]
```

The CLI auto-detects the input format based on file extension and converts to the opposite format:

| Input Extension | Output Extension |
|-----------------|------------------|
| `.yaml`, `.yml` | `.json`          |
| `.json`         | `.yaml`          |

Output is written to the same directory with the swapped extension.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output <path>` | Custom output file path | Input file with swapped extension |
| `--json` | Print structured JSON to stdout (no file written) | — |
| `--indent <n>` | Indentation spaces | `2` |
| `-h, --help` | Show help | — |
| `-V, --version` | Show version | — |

## Common Workflows

### Convert a single file

```bash
# YAML to JSON
jyml config.yaml
# → writes config.json

# JSON to YAML
jyml settings.json
# → writes settings.yaml
```

### Convert with custom output path

```bash
jyml docker-compose.yml -o ./output/docker-compose.json
```

### Convert with custom indentation

```bash
jyml response.json --indent 4
```

### Extract data programmatically

Use `--json` to get structured output for piping to other tools:

```bash
# Get parsed content
jyml workflow.yml --json | jq '.content'

# Extract specific values
jyml .github/workflows/ci.yml --json | jq '.content.jobs'
```

### Batch conversion

Convert multiple files using shell patterns:

```bash
# Convert all YAML files in a directory
for f in configs/*.yaml; do jyml "$f"; done

# Convert all JSON files
for f in data/*.json; do jyml "$f"; done
```

## Output Modes

### Default mode (file output)

Writes converted content to a file, prints progress to stderr:

```bash
jyml config.yaml
# stderr: Converting config.yaml → config.json
# Creates: config.json
```

### Structured mode (`--json`)

Prints structured JSON to stdout, no file written:

```json
{
  "input": "/path/to/input.yaml",
  "format": "json",
  "output": "/path/to/input.json",
  "content": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `input` | `string` | Absolute path to the source file |
| `format` | `string` | Output format: `"json"` or `"yaml"` |
| `output` | `string` | Path where the file would be written |
| `content` | `object` | The parsed and converted data |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success |
| `1`  | Conversion error (invalid YAML/JSON, I/O failure) |
| `2`  | Invalid usage (missing file, bad arguments, unsupported extension) |

## Error Handling

Errors are printed to stderr with actionable context:

```
Error: File not found: config.yaml
Error: Unsupported file extension ".txt". Supported: .yaml, .yml, .json
Error: Invalid YAML: bad indentation of a mapping entry (1:11)
Error: Invalid JSON: Expected property name or '}' in JSON at position 2
```

When conversion fails, check:
1. File exists and is readable
2. File extension is `.yaml`, `.yml`, or `.json`
3. File contains valid YAML or JSON syntax

## Use Cases

### OpenAPI/Swagger specs

Convert specs between formats for different tools:

```bash
# Convert OpenAPI spec to JSON for code generators
jyml openapi.yaml

# Convert back to YAML for documentation
jyml openapi.json
```

### Configuration files

Switch config formats based on tool requirements:

```bash
# ESLint config to YAML
jyml .eslintrc.json

# Docker Compose to JSON
jyml docker-compose.yml
```

### GitHub Actions workflows

Parse workflow files for scripting:

```bash
# Extract job names from a workflow
jyml .github/workflows/ci.yml --json | jq '.content.jobs | keys'
```

### API response inspection

Convert JSON responses to readable YAML:

```bash
curl -s https://api.example.com/data > response.json
jyml response.json --indent 4
cat response.yaml
```
