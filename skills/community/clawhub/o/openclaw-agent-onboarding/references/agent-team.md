# Agent Team Profiles

## Single-agent mode

```text
main-agent: main assistant/controller
```

Use for beginners and lightweight tasks.

## Three-agent mode

```text
architect → executor → auditor
```

- `architect`: decomposition, planning, architecture boundaries.
- `executor`: implementation, file operations, coding.
- `auditor`: review, tests, validation.

## Six-agent mode

```text
pm → architect → reasoner → coder → auditor → monitor
```

- `pm`: requirements, task board, acceptance criteria.
- `architect`: system design, boundaries, risk.
- `reasoner`: complex reasoning/root cause.
- `coder`: implementation.
- `auditor`: security/quality review.
- `monitor`: tests, logs, health, validation.

## Rules

- Do not force multi-agent mode for beginners.
- Planner does not write code.
- Executor does not change requirements unilaterally.
- Auditor does not replace executor.
- Monitor validates and reports, not scope-creeps.
