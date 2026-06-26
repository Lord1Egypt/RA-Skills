# Quality Gates v2

Every auto-executed change must pass these gates before commit.

---

## Gate 1: Syntax Check

```bash
# Python: Must compile without errors
python3 -m py_compile <file.py>
```

**Failure:** Block commit.

---

## Gate 2: Git Status Check

```bash
# No untracked sensitive files
git status --porcelain | grep -v "^\?\?" || true
```

**Failure:** Block commit if sensitive files detected.

---

## Gate 3: Test Execution (if tests exist)

```bash
# Run unit tests for the changed module
python3 -m pytest tests/ -v --tb=short || true
```

**Note:** Test failures are warnings, not blockers (existing test suites may be incomplete).

---

## Gate 4: Documentation Sync

```bash
# If code changed, SKILL.md must reflect new features
# If CLI command added, help text must match
```

**Failure:** Warning + note in report.

---

## Pre-Commit Checklist

- [ ] `py_compile` passes for all changed .py files
- [ ] No untracked secret files
- [ ] SKILL.md reflects new features (if any)
- [ ] CHANGELOG updated (if applicable)
- [ ] Commit message follows convention

---

## Quality Gate Summary

| Gate | Must Pass | Failure Action |
|------|-----------|----------------|
| Syntax | ✅ | Block commit |
| Git Status | ✅ | Block commit |
| Tests | ⚠️ | Warning only |
| Docs Sync | ⚠️ | Warning + note |

---

## Optimization Findings

Proactive scan findings are classified separately:

| Finding | Risk | Action |
|---------|------|--------|
| TODO/FIXME/XXX | Low | Flag in plan |
| Duplicate code | Low | Flag in plan |
| Long function (>100 lines) | Medium | Flag in plan |
| Missing test coverage | Medium | Flag in plan |
| Pinned dependency | Low | Flag in plan |

These are **not auto-executed** — they are flagged for manual review and approval.
