# json-formatter-pro

Format and validate JSON files with pretty-printing and validation modes.

## Description

A utility skill for formatting JSON files with proper indentation and validating JSON syntax. Supports reading from files or stdin, outputting to files or stdout.

## Usage

```bash
# Format a JSON file (pretty-print to stdout)
python ~/.openclaw/skills/json-formatter/json_formatter.py format input.json

# Format and save to a new file
python ~/.openclaw/skills/json-formatter/json_formatter.py format input.json -o output.json

# Validate JSON syntax without formatting
python ~/.openclaw/skills/json-formatter/json_formatter.py validate input.json

# Read from stdin, format and output to stdout
cat input.json | python ~/.openclaw/skills/json-formatter/json_formatter.py format -

# Validate JSON from stdin
cat input.json | python ~/.openclaw/skills/json-formatter/json_formatter.py validate -
```

## Options

- `format`: Pretty-print JSON with proper indentation
- `validate`: Check if JSON is valid without formatting output
- `-o, --output`: Specify output file (default: stdout)
- `-i, --indent`: Number of spaces for indentation (default: 2)
- `--sort-keys`: Sort JSON keys alphabetically

## Examples

```bash
# Format with 4-space indentation
python ~/.openclaw/skills/json-formatter/json_formatter.py format data.json -i 4

# Format and sort keys
python ~/.openclaw/skills/json-formatter/json_formatter.py format data.json --sort-keys

# Validate a JSON file
python ~/.openclaw/skills/json-formatter/json_formatter.py validate config.json
# Output: Valid JSON or error message with line number
```

## Exit Codes

- `0`: Success
- `1`: Invalid JSON syntax
- `2`: File not found or permission error
- `3`: Other error
