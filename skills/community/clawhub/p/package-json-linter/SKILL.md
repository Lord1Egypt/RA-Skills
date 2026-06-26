---
name: package-json-linter
description: Lint and validate package.json files for common mistakes, missing fields, security issues, and best practices. Use when asked to lint, validate, audit, or check package.json files, Node.js project configs, or npm package metadata. Triggers on "lint package.json", "check package", "validate npm", "audit package.json", "package issues".
---

# Package JSON Linter

Lint package.json files for missing fields, dependency issues, security risks, and best practices violations.

## Commands

All commands use the bundled Python script at `scripts/package_json_linter.py`.

### 1. Lint a package.json file

```bash
python3 scripts/package_json_linter.py lint <file-or-directory> [--strict] [--format text|json|markdown]
```

Runs all lint rules against one or more package.json files. If given a directory, scans for `package.json` files recursively (excluding `node_modules`).

**Flags:**
- `--strict` — exit code 1 on any warning (not just errors)
- `--format` — output format: `text` (default), `json`, `markdown`

### 2. Audit for security issues

```bash
python3 scripts/package_json_linter.py security <file-or-directory> [--format text|json|markdown]
```

Checks for supply chain risks: `postinstall`/`preinstall`/`install` scripts, and scripts containing `curl`, `wget`, `eval`, or piping to shell.

### 3. Analyze scripts section

```bash
python3 scripts/package_json_linter.py scripts <file-or-directory> [--format text|json|markdown]
```

Analyzes the `scripts` section for missing common scripts (`test`, `start`, `build`), placeholder test scripts, dependency issues, and deprecated packages.

### 4. Validate required fields and structure

```bash
python3 scripts/package_json_linter.py validate <file-or-directory> [--strict] [--format text|json|markdown]
```

Validates required fields (`name`, `version`, `description`), semver format, npm naming rules, dependency issues, and best practice fields.

## Lint Rules (22 rules)

### Required Fields (5 rules)
| Rule | Severity | Description |
|------|----------|-------------|
| `missing-name` | error | No `name` field |
| `missing-version` | error | No `version` field |
| `invalid-name` | error | Name doesn't match npm naming rules |
| `invalid-version` | error | Version not valid semver |
| `missing-description` | warning | No `description` field |

### Dependencies (6 rules)
| Rule | Severity | Description |
|------|----------|-------------|
| `wildcard-dependency` | error | Version is `*`, empty, or `latest` |
| `git-dependency` | warning | Points to git URL (fragile) |
| `file-dependency` | warning | Uses `file:` protocol |
| `pinned-dependency` | info | All deps pinned to exact versions |
| `duplicate-dependency` | warning | Same package in deps and devDeps |
| `deprecated-package` | warning | Known deprecated package (~20 tracked) |

### Security (4 rules)
| Rule | Severity | Description |
|------|----------|-------------|
| `postinstall-script` | warning | Supply chain risk |
| `preinstall-script` | warning | Supply chain risk |
| `install-script` | warning | Supply chain risk |
| `suspicious-script` | warning | Contains curl/wget/eval/pipe-to-shell |

### Best Practices (7 rules)
| Rule | Severity | Description |
|------|----------|-------------|
| `missing-license` | warning | No `license` field |
| `missing-repository` | info | No `repository` field |
| `missing-engines` | info | No `engines` field |
| `missing-keywords` | info | No `keywords` field |
| `missing-main` | info | No `main` or `exports` field |
| `missing-scripts` | info | No `scripts` section |
| `non-https-url` | warning | URLs not using HTTPS |

## Exit Codes

- `0` — no errors found
- `1` — errors found (or warnings in `--strict` mode)

## Output Formats

- `text` — human-readable, one issue per line (default)
- `json` — structured JSON with summary counts
- `markdown` — table format for reports and PRs
