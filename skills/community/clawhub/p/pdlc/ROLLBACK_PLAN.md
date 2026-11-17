# Rollback & Incident Response Plan

**Version:** 0.1.0-beta.1
**Scope:** AI-* Family published repository

---

## If Users Report a Critical Issue

### Severity Classification

| Severity | Example | Response |
|----------|---------|----------|
| **Critical** | Package produces harmful/insecure instructions | Immediate patch + advisory |
| **High** | Core workflow broken (can't complete first stage) | Patch within 24 hours |
| **Medium** | Incorrect cross-reference, confusing instruction | Fix in next point release |
| **Low** | Typo, cosmetic formatting issue | Batch into next release |

### Response Process

1. **Acknowledge** — Reply to the issue within 24 hours
2. **Triage** — Classify severity, identify affected package(s)
3. **Isolate** — Determine if the issue is package-specific or systemic
4. **Fix** — Create fix on a branch, verify locally
5. **Release** — Tag as patch (`v0.1.1-beta.1`), push, close issue

### Rollback Options

| Scenario | Action |
|----------|--------|
| Single file is broken | Push a corrective commit fixing that file |
| Entire package has structural issues | Revert to previous known-good tag for that package |
| Repository-wide problem (leaked content, wrong license) | Force-push cleaned state (fresh repo = no damaging history) |
| Need to unpublish entirely | Archive repo (GitHub settings → Danger Zone → Archive) |

### Point Release Strategy

```
v0.1.0-beta.1  ← Initial release
v0.1.1-beta.1  ← First patch (critical/high fixes)
v0.1.2-beta.1  ← Second patch
v0.2.0-beta.1  ← Minor (new content, non-breaking improvements)
```

Patches are cumulative — each includes all previous fixes.

---

## Pre-Publication Safety Net

Since we chose **Decision D3 = Fresh repo** (clean `git init`), the published repo has no history to leak. Worst case recovery is always: delete and re-push from source.

The source of truth remains the build workspace (`{build_workspace}/`). The published repo is a derived artifact.

---

## Contact for Emergencies

- GitHub Issues (primary)
- Email: mohammad.maheri.work@gmail.com
- LinkedIn: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)

---

*Created: 2026-06-13*
