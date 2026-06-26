---
name: prettierrc-validator
description: Validate and lint Prettier configuration files (.prettierrc, .prettierrc.json, .prettierrc.yaml, .prettierrc.toml, package.json#prettier) for structure, invalid options, deprecated fields, override conflicts, and best practices. 22 rules across 5 categories.
---

# Prettier Config Validator

Validate `.prettierrc` config files for correctness, deprecated options, conflicting overrides, and best practices. Supports JSON, YAML, TOML, and `package.json#prettier` field. JS configs are detected but not statically validated.

## Commands

```bash
# Full lint (all rules)
python3 scripts/prettierrc_validator.py lint .prettierrc.json

# Check enum values, ranges, type conflicts only
python3 scripts/prettierrc_validator.py options .prettierrc.json

# Check deprecated/removed options only
python3 scripts/prettierrc_validator.py deprecated .prettierrc.json

# Validate 'overrides' array only
python3 scripts/prettierrc_validator.py overrides .prettierrc.json

# Validate structure/syntax only
python3 scripts/prettierrc_validator.py validate .prettierrc.json

# JSON output (for CI / tooling)
python3 scripts/prettierrc_validator.py lint .prettierrc.json --format json

# Summary line only
python3 scripts/prettierrc_validator.py lint .prettierrc.json --format summary
```

## Supported files
- `.prettierrc` (JSON or YAML auto-detected)
- `.prettierrc.json` / `.prettierrc.json5`
- `.prettierrc.yaml` / `.prettierrc.yml`
- `.prettierrc.toml`
- `package.json` — validates the `"prettier"` field
- `.prettierrc.js` / `prettier.config.js` — detected but not validated statically

## Rules (22)

### Structure (5)
- Invalid JSON / YAML / TOML syntax
- Unknown top-level options
- Wrong type for option (boolean, int, string, array expected)
- Empty config file
- `package.json` with missing or invalid `prettier` field

### Options (7)
- Invalid enum value (quoteProps, trailingComma, arrowParens, proseWrap, htmlWhitespaceSensitivity, endOfLine, embeddedLanguageFormatting)
- `printWidth` out of reasonable range (< 20 or > 320)
- `tabWidth` invalid (0 or negative, > 16 warning)
- `parser` name not a known built-in parser
- `requirePragma` + `insertPragma` both true (conflict)
- `rangeStart` > `rangeEnd` (inverted range)
- Unknown parser name (plugin-assumed)

### Deprecated (2)
- `jsxBracketSameLine` → use `bracketSameLine` (Prettier 2.4+)
- Removed options (`useFlowParser`, `tabs`) with replacement guidance

### Overrides (5)
- Override missing `files` field
- `files` empty array or wrong type
- Override missing `options` (no effect)
- Unknown option inside override
- Duplicate glob pattern across overrides (precedence bug)

### Best Practices (3)
- Missing `endOfLine` setting (cross-platform advice)
- Missing `trailingComma` (default changed in Prettier v3)
- `printWidth` very short (< 40) — may cause awkward line breaks
- `useTabs: true` without explicit `tabWidth`
- Invalid / empty plugin entries

## Output Formats
- **text** (default): human-readable with severity icons
- **json**: machine-readable list of issues (file, path, rule, severity, message, category)
- **summary**: single line of counts

## Exit Codes
- 0: No errors (warnings/info allowed)
- 1: Errors found
- 2: Invalid input (file not found, unparseable, unsupported format)

## Requirements
- Python 3.8+
- Optional: `PyYAML` (better YAML parsing — falls back to a minimal parser for simple configs)
- Optional: `tomli` (only for Python 3.10 and below; Python 3.11+ has `tomllib` built in)

## Examples

### Broken config
```json
{ "printWidth": "100", "trailingComma": "some", "jsxBracketSameLine": true }
```
```
✗ ERROR   wrong-type          [printWidth] must be an integer
✗ ERROR   invalid-enum-value  [trailingComma] invalid value 'some' (valid: all, es5, none)
⚠ WARNING deprecated-option   [jsxBracketSameLine] use 'bracketSameLine'
```

### Good CI gate
```bash
python3 scripts/prettierrc_validator.py lint .prettierrc.json --format summary
# exit 1 on any error — fails the CI step
```
