# AGENTS.md

## Purpose

This repository contains `oc-guard`, a Python CLI guard for OpenClaw config changes.
Agentic coding agents should use this file as the default operating guide.

---

## Repository Scope

- Main executable: `scripts/oc-guard`
- Docs:
  - `README.md`
  - `SKILL.md`
  - `docs/SAFETY.md`
  - `CHANGELOG.md`
- Template:
  - `templates/proposal.template.json`

There is no multi-package layout and no separate library module yet.

---

## Tooling Status (Important)

This repo currently does **not** define:
- `pyproject.toml`
- `requirements.txt`
- `package.json`
- CI workflow files for lint/test

So commands below are based on what is actually present today.

---

## Build / Lint / Test Commands

### 1) Syntax check (closest thing to build)

- Validate CLI script syntax:
  - `python3 -m py_compile scripts/oc-guard`

### 2) Runtime smoke checks

- Help output:
  - `scripts/oc-guard --help`
- Plan with bundled template:
  - `scripts/oc-guard plan --proposal templates/proposal.template.json`

### 3) Apply flow smoke check (high-risk gate)

- Should be blocked without confirm:
  - `scripts/oc-guard apply --proposal templates/proposal.template.json`
- Explicit apply:
  - `scripts/oc-guard apply --confirm --proposal templates/proposal.template.json`

### 4) Lint / format

No repo-pinned linter or formatter is configured.
Do not introduce a new formatter/linter unless requested.

If needed for local checks only:
- `python3 -m py_compile scripts/oc-guard`

### 5) Tests

There is currently no committed test suite in this repository.

If tests are added later with pytest:
- Run all tests:
  - `python3 -m pytest -q`
- Run a single file:
  - `python3 -m pytest tests/test_xxx.py -q`
- Run a single test case:
  - `python3 -m pytest tests/test_xxx.py::test_case_name -q`

When adding tests, prefer deterministic unit tests around:
- path mutation helpers
- validation logic
- risk classification
- receipt formatting/signature behavior

---

## Command Behavior Expectations

`oc-guard` supports:
- `plan`
- `apply`
- `--proposal`
- `--confirm`
- `--config`
- `--help`

Expected output contract:
- `【执行回执 | Execution Receipt】`
- executor / operation / request id / status / signature
- `【本次内容 | Details】`

Agents must preserve this contract when changing output behavior.

If `plan` proposal generation fails, inspect `/tmp/oc-guard-last-opencode-output.txt` for local diagnostics.

---

## Environment and Paths

Default behavior is environment-aware:
- `OPENCLAW_HOME`
- `OCGUARD_CONFIG_PATH`
- `OCGUARD_BACKUP_DIR`
- `OCGUARD_OPENCLAW_BIN`
- `OCGUARD_OPENCODE_BIN`
- `OCGUARD_RECEIPT_SECRET`
- `OCGUARD_RECEIPT_SECRET_FILE`

Do not hardcode user-specific paths.
Prefer environment variables + safe fallback logic.

Canonical CLI entrypoint should resolve to this repo script: `scripts/oc-guard`.

---

## Code Style Guidelines

### Imports

- Use standard library imports only unless explicitly required.
- Group imports in this order:
  1. standard library
  2. third-party (if ever introduced)
  3. local imports
- Keep one import per line where practical.
- Avoid wildcard imports.

### Formatting

- Follow existing style in `scripts/oc-guard`:
  - 4-space indentation
  - readable line wrapping
  - explicit intermediate variables for clarity
- Keep functions small and focused.
- Prefer early validation and explicit failure paths.

### Types

- Add type hints for public/helper functions where practical.
- Keep consistency with current style (`-> None`, typed params on key funcs).
- Avoid overengineering with heavy typing abstractions.

### Naming

- Constants: `UPPER_SNAKE_CASE`
- Functions/variables: `snake_case`
- Exceptions/classes: `PascalCase`
- Prefer descriptive names over short abbreviations.

### Error handling

- Use explicit validation and clear error messages.
- Preserve `GuardError` + receipt-based failure reporting behavior.
- Do not swallow exceptions silently.
- Keep rollback paths explicit and auditable.

### Logging and observability

- Use existing log files and conventions.
- Avoid printing sensitive values.
- Mask secrets in user-facing change details.

### Security

- Never commit real secrets or local runtime data.
- Maintain path allowlist checks for config mutation.
- Keep high-risk operations gated by confirmation.
- Preserve backup-before-apply and rollback-on-failure.
- If `oc-guard` returns failed/blocked, do not bypass guard by directly editing `~/.openclaw/openclaw.json`.

### Backward compatibility

- Do not break existing CLI flags/output contract without request.
- If changing output format, update docs and mention migration impact.

---

## Config Mutation Rules

When touching mutation logic:
- Keep `ALLOWED_PATH_PREFIXES` policy explicit.
- Maintain strict validation before apply.
- Ensure reference integrity checks remain in place:
  - channels
  - bindings
  - agents
  - provider/model references

When adding new channels/providers:
- update validation plugin logic
- keep risk classification consistent
- add/update docs and examples

---

## Documentation Rules

If behavior changes, update:
- `README.md`
- `docs/SAFETY.md`
- `CHANGELOG.md`

Use bilingual phrasing where repository already does so.

---

## Cursor / Copilot Rules Check

Checked locations:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

Result:
- No Cursor rules found.
- No Copilot instructions file found.

If these files are added later, treat them as higher-priority repository guidance.

---

## PR / Commit Guidance for Agents

- Keep changes minimal and focused.
- Include rationale in commit messages.
- Avoid bundling unrelated refactors.
- Prefer safe defaults and explicit migration notes for behavior changes.

---

## Quick Agent Checklist

Before finishing:
1. `python3 -m py_compile scripts/oc-guard`
2. `scripts/oc-guard --help`
3. `scripts/oc-guard plan --proposal templates/proposal.template.json`
4. `scripts/oc-guard plan` (without requirement; should be blocked and include `【模型说明-未执行】`)
5. Confirm no secret leakage in output/docs
6. Update docs/changelog if behavior changed
