# R3 Business-Logic Review Report Template

**Reviewer:** @reviewer (independent logic review)  
**Date:** YYYY-MM-DD  
**Target:** <file/function>  
**Reference:** <original buggy implementation>

---

## Summary
**Verdict: <CLEAN / BLOCKED> — <one-line summary of findings>**  
<Brief description of what was fixed and whether it passes.>

---

## R3 Checklist Results

| Check | Severity | Finding |
|-------|----------|---------|
| **Authorization** | | <Does it grant extra rights on any edge condition?> |
| **Permission checks before action** | | <Are permission checks applied BEFORE the action, no bypass path?> |
| **Boundaries (null/empty/huge)** | | <Behavior on null, empty string, negative, very large input?> |
| **Idempotency** | | <Does retry/double-click create duplicates?> |
| **Unknown-user path** | | <Does it leak info via timing or error messages?> |
| **Lockout reset** | | <Does success clear failure counter?> |

---

## Detailed Findings

### 1. Authorization — <SEVERITY>
- <Details>
- **Fix needed:** <Yes/No - what to do>

### 2. Permission Checks — <SEVERITY>
- <Details>
- **Fix needed:** <Yes/No - what to do>

### 3. Boundary Inputs — <SEVERITY>
| Input | Behavior | Risk |
|-------|----------|------|
| `<example>` | `<result>` | `<assessment>` |

- **Suggested fix:** <what to add>

### 4. Idempotency — <SEVERITY>
- <Details>

### 5. Unknown-User Path — <SEVERITY>
- <Details>

### 6. Lockout Reset — <SEVERITY>
- <Details>

---

## Security Fix Verification (R1/R2)

| Vulnerability | Old Code | New Code | Status |
|---------------|----------|----------|--------|
| <e.g., SQL Injection> | `<vulnerable pattern>` | `<fixed pattern>` | ✅ FIXED |

---

## Recommendations

### Must-Fix (CRITICAL/HIGH)
- <List any blocking issues>

### Tech Debt (MEDIUM)
- <List items to log in todo for follow-up>

### Nice-to-Have (LOW)
- <List optional improvements>

---

## Decision
**<APPROVED for commit / BLOCKED - fix required>.** <Rationale.>