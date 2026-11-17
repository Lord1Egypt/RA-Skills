# Binding — Python (Windows/MSYS)

Engine (SKILL.md + phases/security-gates/writing-code/stability/match) stays same. This file covers Python-specific commands and Windows/MSYS tool paths.

## Tool paths on Windows

`npx`, `jscpd`, `lizard` CLI may not resolve in bash. Use these forms:

| Concern | Tool | Command |
|---------|------|---------|
| Duplication | jscpd | `"$APPDATA/npm/jscpd.cmd" --threshold 10 --reporters json <.py file>` (sync with dup>10% ceiling) |
| Complexity | lizard | `python3.14 -m lizard <.py file>` (if installed) or Python API |
| Cycles + layer boundaries | import-linter (BSD-2) | `lint-imports` with a `.importlinter` contract (`forbidden`/`layers`); blocks circular imports + boundary violations |
| Dead code | vulture (MIT) | `vulture <pkg>/ --min-confidence 80` — unused functions/vars/imports |

jscpd JSON report saved to `report/jscpd-report.json` (relative cwd).

### Lizard via Python API (avoids CLI subprocess issues)

```python
import lizard
stats = lizard.analyze_file("calculator.py")
for func in stats.function_list:
    print(f"{func.name}: CCN={func.cyclomatic_complexity}, NLOC={func.nloc}, LOC={func.length}")
max_ccn = max(f.cyclomatic_complexity for f in stats.function_list)
avg_ccn = sum(f.cyclomatic_complexity for f in stats.function_list) / len(stats.function_list)
```

### jscpd JSON parsing

```python
import json
with open("report/jscpd-report.json") as f:
    d = json.load(f)
dup_pct = d["statistics"]["total"]["percentage"]
```

## Python version awareness

| Python | Path | Has lizard? | Notes |
|--------|------|------------|-------|
| `python` (3.11) | agent runtime venv | no (managed) | avoid modifying — use `python3.14`/uv for tools |
| `python3.14` | Chocolatey | yes (pip install) | best for tools |
| `python3.11` | uv-managed | no | `--break-system-packages` needed to modify |

## Test/lint/typecheck

| Gate | Command |
|------|---------|
| Tests | `python -m pytest -q` |
| Lint | `ruff check <.py>` |
| Typecheck | `mypy <.py>` |

## Semgrep on Windows — workaround for PYTHONPATH collision

agent venv's `pydantic_core` shadows Semgrep's bundled one. Always run with `PYTHONPATH=` prefix:

```bash
PYTHONPATH= semgrep scan --config=auto --error ./src
```

## Date arithmetic pitfalls

`date.replace(day=d.day + 1)` raises `ValueError: day is out of range for month` at end-of-month boundaries, including transitions like June 30 → July 1. During A/B QA or discriminating-test work this is a common hidden trap because the simple case passes while the month-boundary test crashes.

**Preferred pattern:** use `date + timedelta(days=1)` instead of `replace(day=...)`, or `datetime.timedelta` itself.

## Inclusive vs exclusive end semantics

For QA tasks around `count_working_days`-style functions, the spec may intend `[start, end]` inclusive off-by-one behavior. The default tests should assert inclusive semantics. If an implementation instead walks `[start, end)`, the discriminating cases below catch the off-by-one drop.

### Discriminating cases for inclusive-end off-by-one

- Single-day span with different dates (`2026-07-01` → `2026-07-02`) must count 1 weekday.
- Full week Monday to Sunday must count 5.
- Weekend-only Sunday-to-Monday must count 1.
- Month-boundary end-of-month to next day must succeed and count 1.
- Friday-to-Monday must count 1.
- Two-week span must count 10.

## Pre-commit checks (MANDATORY before commit)

| Check | Command |
|-------|---------|
| Syntax | `python -m py_compile <file>` |
| Lint | `ruff check <file>` |
| Typecheck | `mypy <file>` |

Run ALL three before every commit in Phase 3. The Verification Gate (phases.md step 8a) requires these to pass.

## Pre-commit hook template

A ready-to-use `.pre-commit-config.yaml` is available at `templates/pre-commit-config.yaml` in the skill directory. Copy it to your project root and run:

```bash
pre-commit install
```

This hooks Gitleaks, Ruff, MyPy, jscpd, Lizard, and syntax check into every commit — exactly the gates the keelwright requires.

## Semgrep note (Python logging rules)

Rule `python.lang.security.audit.logging.logger-credential-leak.python-logger-credential-disclosure`
triggers on format-string parameter names containing `auth_code`, `secret`, `password`, `token`,
`key`, etc. — even when the value is masked.

**Do NOT log secrets — not even truncated.** The correct fix is to remove the value from the
log call entirely, not to rename the parameter to evade the rule. Renaming `auth_code` → `ac`
while still printing `auth_code[:8] + "..."` is rule evasion and leaks the first 8 chars of a
secret. If you must record that an auth step happened, log a constant with no value:

```python
# Correct: no secret material leaves the process
logger.info("auth step completed (token not logged)")
```

This satisfies the rule without weakening auditability and without leaking anything.
