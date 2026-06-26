---
name: postcss-config-validator
description: Validate PostCSS config files (.postcssrc, postcss.config.js, package.json#postcss) for plugin ordering, deprecated plugins, Tailwind integration, and best practices. Use when validating CSS processing configs, auditing PostCSS setups, or linting frontend build configuration.
---

# PostCSS Config Validator

Validate `.postcssrc`, `.postcssrc.json`, `postcss.config.js`, `postcss.config.ts`, and `package.json#postcss` for deprecated plugins, ordering issues, Tailwind integration problems, parser misconfiguration, and best practices. JS/TS configs are detected but cannot be statically validated. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 22+ rules)
python3 scripts/postcss_config_validator.py validate .postcssrc

# Quick structure-only check
python3 scripts/postcss_config_validator.py check .postcssrc.json

# Explain config in human-readable form
python3 scripts/postcss_config_validator.py explain package.json

# Suggest improvements
python3 scripts/postcss_config_validator.py suggest .postcssrc

# JSON output (CI-friendly)
python3 scripts/postcss_config_validator.py validate .postcssrc --format json

# Summary only (pass/fail + counts)
python3 scripts/postcss_config_validator.py validate .postcssrc --format summary

# Strict mode (warnings and infos become errors)
python3 scripts/postcss_config_validator.py validate .postcssrc --strict
```

## Rules (22+)

| # | ID | Category | Severity | Rule |
|---|-----|----------|----------|------|
| 1 | S1 | Structure | Error | File not found or unreadable |
| 2 | S2 | Structure | Error | Empty config file |
| 3 | S3 | Structure | Error | Invalid JSON syntax |
| 4 | S4 | Structure | Warning | Unknown top-level keys (valid: plugins, parser, syntax, stringifier, map, from, to) |
| 5 | S5 | Structure | Info | JS/TS config detected — cannot statically validate |
| 6 | P1 | Plugins | Warning | Empty plugins object/array |
| 7 | P2 | Plugins | Warning | Deprecated plugin (autoprefixer-core, postcss-cssnext, lost, postcss-sprites) |
| 8 | P3 | Plugins | Warning | Duplicate plugins |
| 9 | P4 | Plugins | Info | Plugin ordering issues (autoprefixer after preset-env, cssnano last) |
| 10 | P5 | Plugins | Info | postcss-import should be first plugin |
| 11 | P6 | Plugins | Info | Unknown/uncommon plugin name (not in top 50 list) |
| 12 | T1 | Tailwind | Info | tailwindcss without nesting plugin |
| 13 | T2 | Tailwind | Warning | tailwindcss after autoprefixer (wrong order) |
| 14 | T3 | Tailwind | Info | postcss-preset-env with tailwindcss (potential conflict) |
| 15 | X1 | Syntax/Parser | Warning | Both parser and syntax specified |
| 16 | X2 | Syntax/Parser | Info | Unknown parser value |
| 17 | X3 | Syntax/Parser | Info | Parser set but no matching preprocessor plugin |
| 18 | M1 | Source Maps | Info | Source maps disabled (map: false) |
| 19 | M2 | Source Maps | Info | Inline source maps enabled (map.inline: true) |
| 20 | B1 | Best Practices | Warning | No plugins configured |
| 21 | B2 | Best Practices | Info | Using postcss-preset-env AND individual feature plugins it includes |
| 22 | B3 | Best Practices | Info | Very large number of plugins (>15) |

## Output Formats

- `text` (default): Human-readable with severity icons
- `json`: Machine-parseable JSON with findings array and summary
- `summary`: Pass/fail with error/warning/info counts

## Exit Codes

- `0`: No errors (warnings/infos only or clean)
- `1`: One or more errors found
- `2`: File not found or invalid input

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)
