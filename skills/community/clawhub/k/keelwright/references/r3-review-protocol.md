# R3 Business-Logic Review Protocol (keelwright security-gates.md)

## Mandatory: Spawn Dedicated @reviewer Subagent

**CRITICAL RULE:** The @implementer MUST NEVER self-review. A fresh context catches what the author missed.

```python
delegate_task(
  goal="[@reviewer] Review the diff for <file> against security-gates.md R3 checks + requesting-code-review standards.",
  context=(
    "You are @reviewer in a keelwright session. REQUIRED — read these skills first:\n"
    "  skill_view(name='keelwright', file_path='references/security-gates.md')  # R3 checks\n"
    "  skill_view(name='requesting-code-review')  # review methodology\n"
    "  skill_view(name='clean-code-review')       # SRP/DRY/KISS, smells\n"
    "Review BOTH the pre-change code AND the new diff. Focus on LOGIC, not style:\n"
    "- Authorization: does it grant extra rights on any edge condition?\n"
    "- Permission checks: applied BEFORE the action, no bypass path?\n"
    "- Boundaries: null/empty/negative/huge input behavior?\n"
    "- Idempotency: does retry/double-click create duplicates?\n"
    "- Unknown-user path: does it leak info via timing or error messages?\n"
    "- Lockout reset: does success clear failure counter?\n"
    "Report every finding with severity (CRITICAL/HIGH/MEDIUM/LOW).\n"
    "CRITICAL/HIGH → block commit, fix in same iteration.\n"
    "MEDIUM → log as tech debt, commit allowed.\n"
    "Return: findings list + severity + suggested fix."
  )
)
```

## No-Reviewer Runtime Fallback

If `delegate_task` is unavailable, you MUST still keep the reviewer separate from the implementer context. Do the review in a fresh read step against the actual diff/files on disk, NOT by re-reading the implementer's narrative. Explicitly document this fallback; inline self-review is forbidden.

## R3 Checklist (from security-gates.md)

| Check | What to Verify | Block Threshold |
|-------|----------------|-----------------|
| **Authorization** | On rare/edge condition, can it grant more rights than intended? | CRITICAL/HIGH |
| **Permission Checks** | Applied BEFORE action, no bypass path? | CRITICAL/HIGH |
| **Boundaries** | null, empty, negative, huge input behavior? | MEDIUM+ |
| **Idempotency** | Repeat call (retry, double-click) creates duplicate? | MEDIUM+ |
| **Unknown-User Path** | Leaks info via timing or error messages? | HIGH |
| **Lockout Reset** | Success clears failure counter? | MEDIUM |

## Review Both Old AND New Code

Common blind spots the reviewer must check:
- SHA256→bcrypt: verify timing normalization for unknown users (prevents enumeration)
- Role derivation: hardcoded string → DB field? Is it tamper-proof?
- Lockout reset: does successful login clear counter or persist forever?
- Unknown-user path: does login increment failure counter on unknown users? (It shouldn't — that's an enumeration oracle)

## Output Format

Use template: `templates/r3-review-report.md`

Report every finding with severity. CRITICAL/HIGH = block commit. MEDIUM = tech debt.