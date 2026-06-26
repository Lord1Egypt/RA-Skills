# Spec Compliance Review

Validate code implementation against specifications (NOT general code quality).

**Default**: Report-only, no code modifications.

## 6-Step Process

1. **Understand Specs**: Extract requirements (features, behaviors, interfaces, data structures, constraints)
2. **Generate Checklist**: Create testable items with spec references
3. **Map to Code**: Find implementation files, tests, config
4. **Review**: Compare and assign status (✅ Full, ⚠️ Partial, ❌ Missing, 🔍 Unclear, ⚡ Inconsistent)
5. **Identify Discrepancies**: Missing, inconsistent, partial, extra, incorrect
6. **Generate Report**: Summary + prioritized findings + recommendations

## Review Levels

| Level | Time | Scope |
|-------|------|-------|
| Basic | 5-10 min | Major features (3-5 items), presence check |
| Detailed | 30-60 min | All features, correctness check |
| Comprehensive | 2+ hours | Deep analysis, security, bi-directional |

## Status Symbols

- ✅ Fully Implemented
- ⚠️ Partial
- ❌ Missing
- 🔍 Unclear
- ⚡ Inconsistent

## Discrepancy Types

| Type | Description |
|------|-------------|
| Missing | Spec describes, code doesn't |
| Inconsistent | Code differs from spec |
| Partial | Some aspects missing |
| Extra | Code has undocumented features |
| Incorrect | Logic doesn't match |

## Report Structure

```markdown
# Spec-to-Code Review Report

## Summary
- Specs: X, Code: Y, Consistency: Z%
- Items: N (✅A, ⚠️B, ❌C, 🔍D, ⚡E)

## Critical/High/Medium Issues
[Findings with code refs]

## Recommendations
[Prioritized actions]
```

## Best Practices

**Do**: Read specs first, provide file:line refs, prioritize, report-only default
**Don't**: Assume, modify without permission, judge code quality (spec focus only)

Templates: `assets/review/checklist.md`, `assets/review/pr-review-template.md`