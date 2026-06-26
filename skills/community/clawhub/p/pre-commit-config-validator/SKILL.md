---
name: pre-commit-config-validator
description: Validate .pre-commit-config.yaml files for structure, repository entries, hook definitions, local hooks, and best practices. 23 rules across 5 categories.
---

# Pre-Commit Config Validator

Validate `.pre-commit-config.yaml` files for correctness, completeness, and best practices.

## Commands

```bash
# Full validation (all rules)
python3 scripts/precommit_validator.py validate .pre-commit-config.yaml

# Repository/rev validation only
python3 scripts/precommit_validator.py repos .pre-commit-config.yaml

# Hook definitions only
python3 scripts/precommit_validator.py hooks .pre-commit-config.yaml

# Best practices only
python3 scripts/precommit_validator.py lint .pre-commit-config.yaml

# JSON output
python3 scripts/precommit_validator.py validate .pre-commit-config.yaml --format json

# Summary only
python3 scripts/precommit_validator.py validate .pre-commit-config.yaml --format summary

# Treat warnings as errors
python3 scripts/precommit_validator.py validate .pre-commit-config.yaml --strict

# Multiple files
python3 scripts/precommit_validator.py validate file1.yaml file2.yaml
```

## Rules (23)

### Structure (5)

- **S1** Invalid YAML syntax
- **S2** Missing required top-level key `repos`
- **S3** `repos` is not a list
- **S4** Empty `repos` list (warning)
- **S5** Unknown top-level keys (warning; known: repos, default_language_version, default_stages, ci, minimum_pre_commit_version, exclude, fail_fast, files)

### Repository Entries (6)

- **R1** Missing `repo` key in entry
- **R2** Missing `rev` for non-local/non-meta repos
- **R3** Missing or invalid `hooks` list
- **R4** Empty `hooks` list (warning)
- **R5** `rev` using a branch name instead of tag/SHA (warning: main, master, develop, dev, trunk, HEAD)
- **R6** Floating `rev` without pinning (warning: no semver pattern or SHA)

### Hook Definitions (6)

- **H1** Missing `id` in hook
- **H2** Duplicate hook IDs within the same repo (warning)
- **H3** Unknown hook keys (warning; known: id, name, entry, language, files, exclude, types, types_or, stages, additional_dependencies, args, always_run, pass_filenames, require_serial, minimum_pre_commit_version, verbose, log_file, description)
- **H4** Invalid `stages` values (known: commit, merge-commit, push, prepare-commit-msg, commit-msg, post-checkout, post-commit, post-merge, post-rewrite, manual, pre-push, pre-rebase, pre-merge-commit)
- **H5** `args` is not a list
- **H6** `additional_dependencies` is not a list

### Local Hooks (3)

- **L1** Local hook missing `entry` (required for repo: local)
- **L2** Local hook missing `language`
- **L3** Invalid `language` value (warning; known: python, node, ruby, rust, golang, docker, docker_image, dotnet, lua, perl, r, swift, system, pygrep, script, fail)

### Best Practices (3)

- **B1** repo: meta without check-hooks-apply or check-useless-excludes (warning)
- **B2** Rev does not match semver or SHA pattern (warning)
- **B3** Duplicate repo URLs (warning)
- **B4** `fail_fast: true` may hide issues (info)

## Output Formats

- **text** (default): Human-readable with severity icons and rule codes
- **json**: Machine-readable with file, diagnostics array, and counts
- **summary**: One-line counts by severity

## Exit Codes

- 0: No issues (or warnings/info only without --strict)
- 1: Errors found (or warnings with --strict)
- 2: Parse error or file not found
