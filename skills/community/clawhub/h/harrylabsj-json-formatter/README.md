# json-formatter-pro

A JSON formatting and validation tool for OpenClaw.

## Overview

**json-formatter** is a utility skill that formats JSON files with proper indentation and validates JSON syntax. It supports reading from files or stdin, and can output to files or stdout.

## Installation

1. Clone or copy the skill to your OpenClaw skills directory:
```bash
~/.openclaw/skills/json-formatter/
```

2. Ensure Python 3 is installed on your system.

3. The skill is ready to use - no additional dependencies required.

## Usage

```bash
python ~/.openclaw/skills/json-formatter/json_formatter.py <command> <input> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `format` | Pretty-print JSON with proper indentation |
| `validate` | Check if JSON is valid without formatting output |

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Specify output file (default: stdout) |
| `-i, --indent` | Number of spaces for indentation (default: 2) |
| `--sort-keys` | Sort JSON keys alphabetically |

## Examples

### Example 1: Format a JSON file with custom indentation

Format a JSON file with 4-space indentation and save to a new file:

```bash
python ~/.openclaw/skills/json-formatter/json_formatter.py format data.json -i 4 -o formatted.json
```

**Input (data.json):**
```json
{"name":"John","age":30,"city":"New York"}
```

**Output (formatted.json):**
```json
{
    "name": "John",
    "age": 30,
    "city": "New York"
}
```

### Example 2: Validate JSON and sort keys

Validate a JSON file and format it with sorted keys:

```bash
python ~/.openclaw/skills/json-formatter/json_formatter.py format config.json --sort-keys
```

**Input (config.json):**
```json
{"z_key": 1, "a_key": 2, "m_key": 3}
```

**Output:**
```json
{
  "a_key": 2,
  "m_key": 3,
  "z_key": 1
}
```

### Additional Usage

```bash
# Validate JSON syntax
python ~/.openclaw/skills/json-formatter/json_formatter.py validate config.json
# Output: Valid JSON

# Read from stdin
python ~/.openclaw/skills/json-formatter/json_formatter.py format -
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Invalid JSON syntax |
| `2` | File not found or permission error |
| `3` | Other error |
