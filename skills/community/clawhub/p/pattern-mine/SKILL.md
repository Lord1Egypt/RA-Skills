---
name: pattern-mine
version: 1.0.0
description: >
  Discovers recurring patterns buried in your codebase — similar logic
  written three different ways, duplicated validation in five controllers,
  the same error handling copy-pasted across twelve files. Surfaces what
  should be shared but isn't, and what IS shared but shouldn't be. The
  difference between a codebase that grew and one that was cultivated.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - patterns
  - duplication
  - refactoring
  - code-quality
metadata:
  openclaw:
    emoji: "⛏️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - refactoring
---

# Pattern Mine

> "A pattern isn't repeated code. It's a repeated *decision* — and every repeated decision is a decision that should have been made once."

## What It Does

Your codebase has patterns. Some are intentional (design patterns, conventions, shared utilities). Most are *accidental* — the same logic independently invented by different developers at different times, slightly different each time, all slowly diverging.

Pattern Mine excavates these buried patterns and brings them to the surface:

1. **Convergent patterns**: Different code doing the same thing (should be unified)
2. **Divergent patterns**: Same code doing different things (should be separated)
3. **Emerging patterns**: A pattern forming but not yet crystallized (candidate for abstraction)
4. **Fossilized patterns**: Old patterns still followed long after the reason died

## The Four Mining Operations

### Operation 1: Convergent Pattern Detection
*"Three developers independently wrote the same thing"*

Not just copy-paste detection (your linter does that). Pattern Mine finds **semantically equivalent code with different syntax** — code that does the same thing but looks different.

```
EXAMPLE — Found: 3 independent implementations of "retry with backoff"

LOCATION 1: src/api/client.ts:45
async function fetchWithRetry(url, attempts = 3) {
  for (let i = 0; i < attempts; i++) {
    try { return await fetch(url); }
    catch (e) { await sleep(1000 * Math.pow(2, i)); }
  }
  throw new Error('Failed after retries');
}

LOCATION 2: src/services/payment.ts:112
const retry = async (fn, max = 3) => {
  let lastError;
  for (let attempt = 1; attempt <= max; attempt++) {
    try { return await fn(); }
    catch (err) { lastError = err; await delay(attempt * 2000); }
  }
  throw lastError;
};

LOCATION 3: src/workers/email.ts:67
function withRetry(operation, retries = 5) {
  return operation().catch(err => {
    if (retries <= 0) throw err;
    return new Promise(r => setTimeout(r, 1000))
      .then(() => withRetry(operation, retries - 1));
  });
}

ANALYSIS:
├── All three implement retry-with-backoff
├── Different: max attempts (3, 3, 5), backoff strategy (exp, linear, fixed)
├── Different: error handling (generic throw, preserve last, re-throw)
├── None are configurable enough to replace the others
└── RECOMMENDATION: Extract shared retry utility with configurable
    attempts, backoff strategy, and error handling
```

### Operation 2: Divergent Pattern Detection
*"Same abstraction, different behavior — the abstraction is lying"*

Finds code that *looks* like it follows a pattern but actually deviates in meaningful ways:

```
EXAMPLE — Found: UserValidator diverges from pattern

PATTERN: All validators in src/validators/ follow:
├── validate(input) → { valid: boolean, errors: string[] }
├── Throw on null input
├── Return empty errors array on success

DIVERGENCE: UserValidator
├── validate() returns { isValid: boolean, messages: string[] }
│   └── Different property names: 'valid'→'isValid', 'errors'→'messages'
├── Returns null on null input (doesn't throw)
├── Returns undefined errors on success (not empty array)
└── Every consumer of UserValidator has special-case handling

RECOMMENDATION: Align UserValidator with the common pattern.
Estimated consumer cleanup: 8 files.
```

### Operation 3: Emerging Pattern Detection
*"This is about to become a pattern — should it be one?"*

Finds code that is repeated 2-3 times but hasn't yet become an abstraction. This is the sweet spot for extraction — enough repetition to justify it, but not yet so much that extraction requires touching dozens of files.

```
EXAMPLE — Emerging: Permission check + audit log (2 occurrences, likely growing)

src/routes/admin.ts:
if (!user.hasRole('admin')) {
  auditLog.write({ action: 'ADMIN_ACCESS_DENIED', userId: user.id });
  throw new ForbiddenError('Admin access required');
}

src/routes/billing.ts:
if (!user.hasRole('billing')) {
  auditLog.write({ action: 'BILLING_ACCESS_DENIED', userId: user.id });
  throw new ForbiddenError('Billing access required');
}

ANALYSIS:
├── Pattern: role check → audit denied access → throw forbidden
├── Occurrences: 2 (and a third route is being written this sprint)
├── Variation: only the role name and audit action differ
└── RECOMMENDATION: Extract requireRole(user, role) middleware
    before the third copy appears
```

### Operation 4: Fossilized Pattern Detection
*"Everyone follows this pattern. Nobody remembers why."*

Finds patterns that are consistently followed but serve no current purpose:

```
EXAMPLE — Fossilized: Defensive null checks after non-nullable call

PATTERN FOUND IN 23 LOCATIONS:
const user = await getUser(id);  // getUser now always returns User or throws
if (!user) {                      // This branch is unreachable
  throw new NotFoundError();      // getUser throws NotFoundError itself
}

HISTORY:
├── getUser() used to return null for missing users (pre-2024)
├── Rewritten to throw NotFoundError directly (commit a8f3d2e, 2024-03)
├── Null checks were not removed after rewrite
└── New code copied the pattern from old code (cargo cult)

RECOMMENDATION: Remove 23 unreachable null checks.
Safe to remove: YES (getUser's contract guarantees non-null return).
```

## The Mining Process

```
Phase 1: EXTRACTION
├── Parse all source files into structural representations
├── Identify functional blocks (functions, methods, handlers, middleware)
├── For each block, extract:
│   ├── Input/output signature
│   ├── Core operations performed
│   ├── Error handling strategy
│   ├── Side effects
│   └── Dependencies
└── Build a similarity matrix between all blocks

Phase 2: CLUSTERING
├── Group blocks by semantic similarity (not just syntactic)
├── For each cluster:
│   ├── How many instances? (2-3 = emerging, 4+ = established)
│   ├── How consistent? (identical = convergent, varied = divergent)
│   ├── How old? (all recent = emerging, all old = fossilized)
│   └── Trend? (growing = emerging, stable = established, declining = fossilized)
└── Filter noise: single-line patterns, framework boilerplate, trivial duplication

Phase 3: ANALYSIS
├── For convergent patterns:
│   ├── What's the canonical form? (most common variant)
│   ├── What are the meaningful variations? (configurable vs. copy-paste error)
│   ├── Extraction difficulty (how coupled is each instance?)
│   └── Extraction benefit (how much code eliminated × frequency of change)
├── For divergent patterns:
│   ├── Which instance is "wrong"? (or is the pattern itself wrong?)
│   ├── Impact of divergence (confuses developers? causes bugs?)
│   └── Alignment difficulty
├── For emerging patterns:
│   ├── Is abstraction justified yet? (rule of three)
│   ├── What would the interface look like?
│   └── Will this pattern keep growing?
└── For fossilized patterns:
    ├── When did the justification die?
    ├── Is removal safe?
    └── How many instances to clean up?

Phase 4: MINE REPORT
├── Patterns discovered, by type
├── Extraction/cleanup recommendations, prioritized by:
│   ├── Bug risk (divergent patterns first)
│   ├── Development velocity (most-duplicated convergent patterns)
│   ├── Code health (fossilized patterns for cleanup)
│   └── Timeliness (emerging patterns before they spread)
└── Estimated effort for each recommendation
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                      PATTERN MINE                           ║
║           Codebase: acme-platform                           ║
║           Files scanned: 347 / Patterns found: 18           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CONVERGENT (should unify): 6 patterns                       ║
║  ├── Retry with backoff ........... 3 variants, 3 files     ║
║  │   Extraction saves: ~45 lines, unifies behavior           ║
║  ├── API response formatting ...... 4 variants, 12 files     ║
║  │   Extraction saves: ~120 lines, fixes 2 inconsistencies   ║
║  ├── Input sanitization ........... 3 variants, 8 files      ║
║  │   ⚠ One variant misses XSS case (security risk)          ║
║  ├── Date parsing from API ........ 2 variants, 6 files      ║
║  ├── Pagination parameter handling  3 variants, 9 files      ║
║  └── Cache key generation ......... 2 variants, 4 files      ║
║                                                              ║
║  DIVERGENT (should align): 3 patterns                        ║
║  ├── Validator return types ....... UserValidator deviates    ║
║  ├── Error response shape ........ /admin routes differ      ║
║  └── Logging level usage ......... warn vs error inconsistent║
║                                                              ║
║  EMERGING (watch / extract soon): 4 patterns                 ║
║  ├── Role check + audit log ....... 2 locations (growing)    ║
║  ├── Optimistic lock + retry ...... 2 locations              ║
║  ├── Feature flag gating .......... 3 locations (new pattern)║
║  └── Webhook dispatch + logging ... 2 locations              ║
║                                                              ║
║  FOSSILIZED (safe to remove): 5 patterns                     ║
║  ├── Null check after non-nullable  23 locations, 0 risk     ║
║  ├── IE11 polyfill conditionals ... 7 locations, 0 risk      ║
║  ├── Legacy encoding detection .... 4 locations, 0 risk      ║
║  ├── Manual promise wrapping ...... 3 locations (use async)  ║
║  └── Explicit bind(this) in arrow   12 locations (no-op)     ║
║                                                              ║
║  TOP RECOMMENDATION:                                         ║
║  Extract API response formatter (12 files, 4 variants).      ║
║  Highest ROI: most duplicated × most frequently changed.     ║
║  Estimated effort: 3 hours. Eliminates 120 lines + 2 bugs.  ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- **Before any refactoring effort** — know what patterns exist before restructuring
- When onboarding (understand the codebase's actual patterns, not just the documented ones)
- During sprint planning for cleanup work (prioritized extraction targets)
- When a code review reveals "we have this pattern everywhere"
- After a new developer joins and writes code that *almost* matches existing patterns
- Quarterly, as a health check (are patterns converging or diverging?)

## Why It Matters

Unmined patterns are a hidden tax on every developer who reads, writes, or modifies the code. Every time someone writes retry logic from scratch because they didn't know a retry utility exists (or because the existing three retry utilities are all slightly different), the codebase gets a little bigger, a little more inconsistent, and a little harder to understand.

Pattern Mine doesn't tell you to DRY everything. It tells you **where DRY matters** and where it doesn't — so you abstract the right things at the right time.

Zero external dependencies. Zero API calls. Pure structural and semantic analysis.
