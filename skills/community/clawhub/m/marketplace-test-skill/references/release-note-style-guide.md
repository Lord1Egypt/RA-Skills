# Release Note Style Guide

Use this guide when converting raw technical changes into release notes.

## Category Guidance

- `Added`: New user-visible capabilities, new integrations, new commands, new supported formats.
- `Changed`: Behavior changes, UI changes, API contract changes, performance changes, compatibility updates.
- `Fixed`: Bugs, regressions, incorrect outputs, crashes, broken links, confusing states.
- `Removed`: Deleted behavior, removed flags, deprecated APIs that are no longer available.
- `Security`: Vulnerability fixes, permission changes, authentication changes, secret handling improvements.
- `Internal`: Build, test, refactor, dependency, and documentation changes that do not need user-facing release notes.

## Rewrite Patterns

Convert implementation-first notes into user-facing outcomes.

```text
Before: feat: add CSV parser in src/import/csv.ts
After: Added CSV import support.
```

```text
Before: fix: null pointer in payment callback
After: Fixed a payment callback crash when the provider returned an empty response.
```

```text
Before: chore: bump vite and update lockfile
After: Internal dependency updates. Omit from public notes unless requested.
```

```text
Before: refactor auth service
After: Omit unless the refactor changes behavior, reliability, performance, or migration requirements.
```

## Quality Checklist

- State what changed from the user's perspective.
- Keep one idea per bullet.
- Use past tense for release notes: `Added`, `Fixed`, `Improved`, `Removed`.
- Mention affected surfaces when helpful: API, CLI, dashboard, import flow, mobile app.
- Include migration notes for breaking changes, config changes, renamed options, or data migrations.
- Do not invent severity, metrics, customer impact, or compatibility guarantees.
