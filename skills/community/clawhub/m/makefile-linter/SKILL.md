---
name: makefile-linter
description: Lint Makefiles for common issues — tabs, .PHONY, unused vars, portability, and best practices.
version: 1.0.0
---

# makefile-linter

A pure-Python 3 (stdlib only) Makefile linter. Detects common issues including tab/space errors, missing `.PHONY` declarations, unused/undefined variables, hardcoded paths, shell portability problems, and more.

## Commands

### `lint FILE`

Lint a Makefile and report issues.

```bash
python3 scripts/makefile-linter.py lint Makefile
python3 scripts/makefile-linter.py lint /path/to/Makefile
echo -e "all:\n\techo hello" | python3 scripts/makefile-linter.py lint /dev/stdin
```

### `targets FILE`

List all targets with line numbers, phony status, prerequisites, and inline comment descriptions.

```bash
python3 scripts/makefile-linter.py targets Makefile
python3 scripts/makefile-linter.py targets Makefile --format json
```

### `vars FILE`

List all variable definitions with line numbers and values.

```bash
python3 scripts/makefile-linter.py vars Makefile
python3 scripts/makefile-linter.py vars Makefile --format markdown
```

### `audit FILE`

Full audit combining lint results, targets list, and variables summary.

```bash
python3 scripts/makefile-linter.py audit Makefile
python3 scripts/makefile-linter.py audit Makefile --format json
```

## Options

| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: `text`) |
| `--strict` | Exit code 1 on any reported issue |
| `--ignore RULE` | Ignore a specific rule (repeatable) |
| `--min-severity error\|warning\|info` | Minimum severity to report (default: `info`) |

## Lint Rules

| Rule | Severity | Description |
|------|----------|-------------|
| `spaces-not-tabs` | error | Recipe lines must use tabs, not spaces |
| `duplicate-targets` | error | Same target defined more than once |
| `missing-phony` | warning | Common phony target not in `.PHONY` |
| `unused-variables` | warning | Variable defined but never referenced |
| `undefined-variables` | warning | Variable referenced but never defined |
| `hardcoded-paths` | warning | Absolute paths in recipes |
| `trailing-whitespace` | warning | Lines ending with spaces or tabs |
| `shell-portability` | warning | Bash-specific syntax without `SHELL := /bin/bash` |
| `recursive-make` | info | `$(MAKE) -C` or `make -C` detected |
| `missing-default-target` | info | No `all` target defined |
| `long-lines` | info | Lines over 120 characters |
| `missing-clean` | info | No `clean` target defined |

## Examples

```bash
# Report only errors and warnings
python3 scripts/makefile-linter.py lint Makefile --min-severity warning

# JSON output for CI integration
python3 scripts/makefile-linter.py lint Makefile --format json

# Fail CI on any issue
python3 scripts/makefile-linter.py lint Makefile --strict

# Ignore specific rules
python3 scripts/makefile-linter.py lint Makefile --ignore recursive-make --ignore missing-clean

# Full audit in Markdown (for PR comments)
python3 scripts/makefile-linter.py audit Makefile --format markdown

# Pipe from stdin
cat Makefile | python3 scripts/makefile-linter.py lint /dev/stdin
```
