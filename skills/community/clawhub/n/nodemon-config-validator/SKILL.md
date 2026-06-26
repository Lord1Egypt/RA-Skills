---
name: nodemon-config-validator
description: Validate nodemon config files (nodemon.json, .nodemonrc, package.json#nodemonConfig) for watch settings, ignore patterns, exec conflicts, and best practices. Use when validating Node.js development configs, auditing watch setups, or linting nodemon configuration.
---

# Nodemon Config Validator

Validate `nodemon.json`, `.nodemonrc`, `.nodemonrc.json`, and `package.json#nodemonConfig` for watch performance issues, ignore patterns, exec conflicts, delay settings, and best practices. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 22+ rules)
python3 scripts/nodemon_config_validator.py validate nodemon.json

# Quick syntax-only check (structure rules only)
python3 scripts/nodemon_config_validator.py check .nodemonrc

# Explain config in human-readable form
python3 scripts/nodemon_config_validator.py explain nodemon.json

# Suggest improvements
python3 scripts/nodemon_config_validator.py suggest package.json

# JSON output (CI-friendly)
python3 scripts/nodemon_config_validator.py validate nodemon.json --format json

# Summary only (pass/fail + counts)
python3 scripts/nodemon_config_validator.py validate nodemon.json --format summary

# Strict mode (warnings become errors)
python3 scripts/nodemon_config_validator.py validate nodemon.json --strict
```

## Rules (22+)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | Error | File not found or unreadable |
| S2 | Structure | Error | Empty config |
| S3 | Structure | Error | Invalid JSON syntax |
| S4 | Structure | Warning | Unknown top-level keys |
| S5 | Structure | Warning | Both nodemon.json and .nodemonrc present (conflict) |
| W1 | Watch | Warning | Empty watch array |
| W2 | Watch | Info | Watch path uses absolute path (portability) |
| W3 | Watch | Error | Watching node_modules (severe performance issue) |
| W4 | Watch | Info | No watch or ext specified (relying on defaults) |
| E1 | Extensions | Warning | Empty ext string |
| E2 | Extensions | Warning | Watching too many extensions (>10, performance) |
| E3 | Extensions | Info | Missing common extensions for detected project type |
| I1 | Ignore | Warning | Empty ignore array |
| I2 | Ignore | Info | node_modules not explicitly ignored |
| I3 | Ignore | Warning | Overly broad ignore patterns (e.g. "*") |
| X1 | Exec | Warning | exec command with shell injection risk |
| X2 | Exec | Warning | Both exec and script specified (conflict) |
| X3 | Exec | Info | execMap with unusual/unknown extension |
| D1 | Delay | Warning | Delay too low (<100ms, rapid restarts) |
| D2 | Delay | Warning | Delay too high (>10000ms, slow feedback) |
| B1 | Best Practices | Info | verbose not set (useful for debugging) |
| B2 | Best Practices | Warning | No ignore patterns at all |

## Output Formats

- `text` (default): Human-readable with severity icons
- `json`: Machine-parseable JSON array of findings
- `summary`: Pass/fail with error/warning/info counts

## Exit Codes

- `0`: No errors (warnings/infos only or clean)
- `1`: One or more errors found
- `2`: File not found or invalid input

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)
