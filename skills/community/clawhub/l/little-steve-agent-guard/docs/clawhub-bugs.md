# ClawHub Platform Issues (Pending)

Record of issues found during little-steve-agent-guard publishing.
To be filed as bugs/feature requests when ready.

## 1. `requires.bins` not exposed in registry API

**Severity**: Medium
**Status**: Unresolved (platform-side)

SKILL.md frontmatter correctly declares:
```yaml
requires:
  bins:
    - jq
```

But `clawhub inspect <slug> --json` returns no `requires` field in the response.
The security scanner compares registry metadata (no bins) with SKILL.md content (jq declared),
flags the mismatch as "inconsistency", and contributes to a "Suspicious" rating.

**Affected skills**: little-steve-agent-guard, little-steve-content-inbox (both declare jq)

**Expected behavior**: `clawhub publish` should extract `requires.bins` from frontmatter
and expose it in the registry API so the security scanner sees a consistent declaration.

## 2. Security scanner lacks "cross-skill" category awareness

**Severity**: Low
**Status**: Design feedback

Skills like agent-guard are inherently cross-skill (read other skills' files for analysis).
The scanner flags this as "broad filesystem scope" even though it's declared and documented.

A "guard" or "meta-skill" category could let the scanner apply different evaluation criteria
for skills whose stated purpose is to inspect/wrap other skills.

## 3. Runbook emergency procedures always flagged

**Severity**: Low
**Status**: Design feedback

Any skill with operational documentation (circuit-break, rollback, manual override)
gets flagged for "bypass commands that disable protections". This is inherent to
any security tooling that includes a runbook.

The scanner could distinguish between:
- Bypass procedures documented for human operators (expected)
- Scripts that programmatically disable security (suspicious)
