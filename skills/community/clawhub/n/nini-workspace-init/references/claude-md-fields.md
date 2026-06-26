# CLAUDE.md Placeholder Fields

Reference for replacing placeholders in the dev-config-template CLAUDE.md.

## Placeholder Mapping

| Placeholder | Section | Collected From | Example |
|-------------|---------|----------------|---------|
| `[ROLE: e.g., ...]` | 0 - User Context | User role question | `a backend developer` |
| `[LEVEL: e.g., ...]` | 0 - User Context | Experience level question | `learning while developing` |
| `[YOUR_LANGUAGE: e.g., ...]` | 5.1 - Language Conventions (x2) | Language preference question | `简体中文` |
| `[YOUR_FORMAT_COMMAND]` | 5.3 - Development Commands | Tech stack + confirmation | `ruff format .` |
| `[YOUR_LINT_COMMAND]` | 5.3 - Development Commands | Tech stack + confirmation | `ruff check .` |
| `[YOUR_TYPE_CHECK_COMMAND]` | 5.3 - Development Commands | Tech stack + confirmation | `mypy .` |
| `[YOUR_TEST_COMMAND]` | 5.3 - Development Commands | Tech stack + confirmation | `pytest` |
| `[PROJECT_STYLE_GUIDE: e.g., ...]` | 5.2 - Coding Standards | Tech stack | `PEP 8` |
| `[ADD YOUR CONVENTIONS HERE]` | 5.2 - Coding Standards | (leave empty or ask user) | -- |
| `[ADD YOUR PROJECT RESOURCES HERE]` | 9 - Resources | (leave empty or ask user) | -- |
| Repository table in section 1 | 1 - Workspace Structure | Sub-repo collection | Generated from repos list |

## Tech Stack Defaults

### Python

| Tool | Default | Alternatives |
|------|---------|-------------|
| Formatter | `ruff format .` | `black .`, `autopep8` |
| Linter | `ruff check .` | `flake8`, `pylint` |
| Type checker | `mypy .` | `pyright`, `pytype` |
| Test runner | `pytest` | `unittest`, `nose2` |
| Style guide | `PEP 8` | -- |

### TypeScript

| Tool | Default | Alternatives |
|------|---------|-------------|
| Formatter | `prettier --write .` | `biome format .` |
| Linter | `eslint .` | `oxlint`, `biome lint .` |
| Type checker | `tsc --noEmit` | -- |
| Test runner | `vitest` | `jest`, `mocha` |
| Style guide | `Google TypeScript Style Guide` | `Airbnb` |

### Mixed (Python + TypeScript)

List both sets of commands in section 5.3, separated by comments:

```bash
# Python
ruff format .
ruff check .
mypy .
pytest

# TypeScript
prettier --write .
eslint .
tsc --noEmit
vitest
```

## Repository Table Format

Replace the example table in section 1 with:

```markdown
| Repo | Description |
|------|-------------|
| `repos/{name}` | {description} |
| `repos/{name}` | {description} |
```

Also update the venv activation example to use the first repo name.
