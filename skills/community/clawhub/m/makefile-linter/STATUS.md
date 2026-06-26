# makefile-linter — Status

**Status:** Ready
**Price:** $49
**Created:** 2026-04-09

## Features

- 12 lint rules covering errors, warnings, and info-level issues
- Detects tab/space recipe indentation errors
- Flags missing `.PHONY` declarations for common targets
- Detects unused and undefined variables (excludes built-in Make vars)
- Warns on hardcoded absolute paths in recipes
- Detects bash-specific syntax without `SHELL := /bin/bash`
- Reports recursive make usage (`$(MAKE) -C`)
- Checks for missing `all` and `clean` targets
- Flags duplicate target definitions
- Reports long lines and trailing whitespace
- `targets` command lists all targets with descriptions from comments
- `vars` command lists all variable definitions
- `audit` command combines lint + targets + vars in one pass
- Output in text, JSON, or Markdown formats
- `--strict` flag for CI/CD exit-code enforcement
- `--ignore` flag to suppress specific rules
- `--min-severity` filter for error/warning/info thresholds
- Pure Python 3 stdlib — zero external dependencies
