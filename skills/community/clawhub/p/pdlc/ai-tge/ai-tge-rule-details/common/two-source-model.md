<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Two-Source Derivation Model

## Purpose

AI-TGE derives test requirements from TWO independent sources — project-specific architecture decisions AND universal baseline expectations. This document defines the complete derivation logic, resolution rules when sources overlap or conflict, and the baseline requirement catalog.

This model ensures that even if an Architecture Package is thin or absent on a topic, the project still receives minimum test governance on that topic.

---

## The Two Sources

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SOURCE 1: ARCHITECTURE PACKAGE (project-specific, from AI-ADLC)         │
│  ────────────────────────────────────────────────────────────────────────│
│  What: API contracts, component designs, ADRs, security decisions,       │
│        integration maps, data models, NFR commitments                    │
│  Result: Tailored test requirements linked to specific commitments       │
│  If absent: No architecture-specific tests (only baseline)               │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  SOURCE 2: BUILT-IN TEST GOVERNANCE BASELINE (universal minimums)        │
│  ────────────────────────────────────────────────────────────────────────│
│  What: Universal test expectations that apply to ANY project              │
│  Result: Tests that should exist regardless of what the AP says          │
│  If AP silent on topic: Baseline provides minimum coverage               │
│  If AP provides more: Baseline is enriched (both apply)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Resolution Logic

When both sources apply to the same component/concern, resolution follows these rules:

### Decision Tree

```
FOR each component/concern in the project:

  1. Does the AP explicitly define a commitment for this?
     ├── YES → Derive specific test requirements from AP
     │         AND apply relevant baseline rules (ADDITIVE)
     │         Register entries: Source = "Architecture" + Source = "Baseline"
     │
     └── NO  → Does this component fit a baseline category?
               ├── YES → Apply baseline rules only
               │         Register entries: Source = "Baseline"
               │         Flag as "baseline-only coverage" in register
               │
               └── NO  → No auto-derived requirement
                         (can be manually registered by user)
```

### Resolution Rules Table

| Scenario | Architecture Source | Baseline Source | Result |
|----------|-------------------|----------------|--------|
| AP defines API contract + baseline requires contract tests | Specific contract tests per endpoint | Generic "every API needs contract test" | AP tests take precedence; baseline satisfied implicitly |
| AP defines security ADR + baseline requires security tests | Specific auth flow tests from ADR | Generic "every auth flow needs security test" | Both apply — AP provides specifics, baseline ensures nothing missed |
| AP is silent on error handling + baseline requires error tests | Nothing | "Every error handler needs a negative test" | Baseline applies alone; flagged as "baseline-only" |
| AP defines performance SLA + baseline has no performance rule | Specific performance tests per SLA | Nothing | AP tests apply; no baseline enrichment needed |
| AP explicitly states "no tests needed for X" | Exclusion noted | Baseline would normally apply | User decision overrides baseline; marked as "Override" |

### Key Principle: Additive, Never Replacement

Baseline NEVER replaces architecture-derived requirements. It only ADDS to them:

```
Architecture-derived tests = {specific tests from AP commitments}
Baseline tests            = {universal minimums for component type}
Final register            = Architecture-derived ∪ Baseline (union, not intersection)
```

**Exception:** If an architecture-derived test is MORE specific than the baseline for the same concern, the baseline entry is marked "satisfied by" the architecture entry (not duplicated).

---

## Built-In Baseline Catalog

### Baseline Requirements (Always Applied)

These represent universal test expectations that every well-governed project should meet, regardless of what the Architecture Package explicitly states.

| ID | Component Type | Required Test | Level | Type | Sub-Type | Rationale |
|:--:|---------------|--------------|:-----:|:----:|:--------:|-----------|
| BASE-API-01 | Any API endpoint | Contract test (request schema validation) | Integration | Functional | Contract | API promises must be verifiable — consumers depend on schema |
| BASE-API-02 | Any API endpoint | Contract test (response schema validation) | Integration | Functional | Contract | Response shape must match documentation |
| BASE-API-03 | Any API endpoint | Error response test (at least 400, 401, 404, 500) | Integration | Functional | Error Handling | Error paths are often the most fragile code paths |
| BASE-SEC-01 | Any auth flow | Authentication verification (valid credentials succeed) | System | Non-Functional | Security | Auth must work correctly — business-critical |
| BASE-SEC-02 | Any auth flow | Authentication rejection (invalid credentials fail) | System | Non-Functional | Security | Negative auth is often overlooked but critical |
| BASE-SEC-03 | Any auth flow | Authorization enforcement (role-based access) | Integration | Non-Functional | Security | Wrong-role access attempts must be blocked |
| BASE-DATA-01 | Any data mutation | Write → read → verify cycle | Integration | Functional | Data Integrity | Data corruption is catastrophic and often silent |
| BASE-DATA-02 | Any data mutation | Validation on invalid input (reject bad data) | Unit | Functional | Boundary | Garbage-in must not produce garbage-stored |
| BASE-INT-01 | Any external integration | Connectivity test (can reach external system) | Integration | Functional | Contract | External dependencies fail — verify they work |
| BASE-INT-02 | Any external integration | Error handling test (external system unavailable) | Integration | Functional | Error Handling | Graceful degradation when dependency is down |
| BASE-INT-03 | Any external integration | Timeout handling test | Integration | Non-Functional | Reliability | Hanging connections must not block the system |
| BASE-BL-01 | Any business rule | Unit test (rule logic produces correct output) | Unit | Functional | Business Logic | Business logic is the core value of the system |
| BASE-BL-02 | Any business rule | Boundary test (edge cases of rule) | Unit | Functional | Boundary | Edge cases are where bugs hide |
| BASE-WF-01 | Any user-facing workflow | Happy path acceptance test (end-to-end) | Acceptance | Functional | Workflow | Primary user experience must work |
| BASE-WF-02 | Any user-facing workflow | Error path test (user makes mistakes) | System | Functional | Error Handling | Users will make mistakes — system must handle gracefully |
| BASE-ERR-01 | Any error handler | Negative test (error path verification) | Unit | Functional | Error Handling | Error handlers that are never tested often don't work |
| BASE-ERR-02 | Any error handler | No data corruption on error (state preserved) | Integration | Functional | Data Integrity | Failed operations must not leave corrupt state |
| BASE-CFG-01 | Any configuration | Valid input acceptance test | Unit | Functional | Boundary | Good config must be accepted |
| BASE-CFG-02 | Any configuration | Invalid input rejection test | Unit | Functional | Boundary | Bad config must fail clearly, not silently |
| BASE-CFG-03 | Any configuration | Default value test (missing config uses defaults) | Unit | Functional | Boundary | Missing config should not crash the system |

---

## Baseline Application Rules

### When to Apply Each Baseline

| Baseline ID | Apply When | Skip When |
|:-----------:|-----------|-----------|
| BASE-API-* | ANY endpoint exists (detected from AP or codebase) | No API endpoints in project |
| BASE-SEC-* | ANY authentication/authorization exists | Public-only system with no auth |
| BASE-DATA-* | ANY write operation to a data store | Read-only system (unlikely) |
| BASE-INT-* | ANY external system integration | Fully self-contained (no external calls) |
| BASE-BL-* | ANY business rule identified | Pure CRUD with no domain logic (rare) |
| BASE-WF-* | ANY user-facing workflow | Backend-only with no user interaction |
| BASE-ERR-* | ANY error handling code | (Always applies — every system has error paths) |
| BASE-CFG-* | ANY configurable parameters | Hardcoded system with no configuration (anti-pattern) |

### Detection Rules (How to Identify Components)

| Component Type | Detection Method |
|---------------|-----------------|
| API endpoint | AP has API Architecture document, OR endpoint definitions found in code |
| Auth flow | AP has Security Architecture document mentioning authentication, OR auth middleware found |
| Data mutation | AP has Data Architecture with entities, OR write operations to any data store |
| External integration | AP has Integration Architecture listing externals, OR HTTP/gRPC/message clients found |
| Business rule | AP Component Design identifies domain logic, OR non-trivial logic in service layer |
| User-facing workflow | AP has user stories with multi-step flows, OR UI routes/pages defined |
| Error handler | Always present (every system handles errors) |
| Configuration | Environment variables, config files, or feature flags exist |

---

## Enrichment Pattern (Architecture + Baseline)

When the AP provides specifics AND baseline applies, the register contains BOTH:

### Example: API Endpoint `/users`

**From Architecture (AP defines contract):**
| Commitment ID | Test Name | Source |
|:-------------:|-----------|:------:|
| API-USERS-01 | POST /users returns 201 with valid UserCreateDTO | Architecture |
| API-USERS-02 | POST /users validates email format (returns 422 on invalid) | Architecture |
| API-USERS-03 | GET /users/{id} returns 404 for non-existent user | Architecture |
| API-USERS-04 | GET /users requires Bearer token (returns 401 without) | Architecture |

**From Baseline (universal for any API endpoint):**
| Commitment ID | Test Name | Source | Satisfied By |
|:-------------:|-----------|:------:|:------------:|
| BASE-API-01 | POST /users request schema matches spec | Baseline | API-USERS-01 ✓ |
| BASE-API-02 | POST /users response schema matches spec | Baseline | — (register separately) |
| BASE-API-03 | POST /users returns appropriate error codes | Baseline | API-USERS-02 ✓ (partial) |

**Resolution:** BASE-API-01 is marked "satisfied by API-USERS-01" (architecture is more specific). BASE-API-02 is registered separately (architecture didn't explicitly test response schema). BASE-API-03 is partially satisfied — architecture tests 422 but not 400/500.

---

## Baseline-Only Mode

When NO Architecture Package is available (Brownfield mode or minimal input):

1. Scan workspace for component types (API files, auth middleware, data models, etc.)
2. Apply all matching baseline rules
3. Mark ALL register entries as `Source: Baseline`
4. Flag in coverage report: "Architecture-derived coverage: 0% — only baseline governance active"
5. Recommend: "For tailored test governance, provide an Architecture Package"

### Baseline Coverage Report View

```markdown
## Coverage Report — Baseline Only

⚠️ No Architecture Package available. Coverage is baseline-only.

| Component Type | Found | Baseline Rules Applied | Tests Existing | Tests Missing |
|---------------|:-----:|:---------------------:|:--------------:|:-------------:|
| API Endpoints | 12 | 36 (3 per endpoint) | 18 | 18 |
| Auth Flows | 2 | 6 (3 per flow) | 4 | 2 |
| Data Mutations | 8 | 16 (2 per entity) | 10 | 6 |
| External Integrations | 3 | 9 (3 per integration) | 3 | 6 |
| Business Rules | 15 | 30 (2 per rule) | 20 | 10 |
| Workflows | 4 | 8 (2 per workflow) | 2 | 6 |
| Error Handlers | 20 | 40 (2 per handler) | 12 | 28 |
| Configuration | 5 | 15 (3 per config) | 5 | 10 |

**Total baseline coverage: 74/160 = 46%**

To improve governance precision, provide an Architecture Package.
This enables commitment-specific test derivation (API contracts → exact
schema tests, security ADRs → specific auth flow tests, etc.)
```

---

## User Override Rules

Users can override baseline requirements:

### Override Process

1. User says "I don't need {baseline requirement} for {component}"
2. AI-TGE asks for rationale: "Why is this test not needed?"
3. User provides rationale
4. Register entry updated:
   - Status: `Overridden`
   - Override Rationale: {user's explanation}
   - Override Date: {timestamp}
5. Entry excluded from coverage calculations
6. Entry REMAINS in register (audit trail — never deleted)

### Valid Override Reasons

| Reason | Example |
|--------|---------|
| Component is deprecated / being removed | "This endpoint is being retired next sprint" |
| Risk is mitigated by other means | "This is behind a feature flag that's always off in production" |
| Test exists but in different form | "We test this through a broader integration test, not in isolation" |
| Regulatory/compliance exception | "External audit approved this gap with compensating control" |
| Prototype / throwaway code | "This module is a spike — not going to production" |

### Invalid Override Reasons (Challenge User)

| Reason | Why It's Invalid | Correct Response |
|--------|-----------------|-----------------|
| "We don't have time" | Time pressure doesn't remove risk | "Noted as test debt. Priority: {risk score}. Shall I log it for next sprint?" |
| "It's too simple to test" | Simple code still breaks | "The simplicity makes it fast to test. Shall I keep it as Low priority?" |
| "Nobody tests that" | Industry norm doesn't justify risk | "The baseline exists because this is a common failure point. Override at your own risk?" |
| "The framework handles it" | Framework bugs exist | "Even framework-handled concerns benefit from verification. Reduce to Low priority instead?" |

---

## Maintenance Rules

1. **Baseline catalog is version-controlled** — changes to baseline requirements affect ALL projects using AI-TGE
2. **Never remove a baseline rule** — deprecate it (mark as `Deprecated` with rationale)
3. **New baselines must have rationale** — "Why does EVERY project need this?" must have a clear answer
4. **Baseline rules are technology-agnostic** — they say WHAT to test, not HOW (no framework references)
5. **Baseline rules are additive to architecture** — they never contradict or override AP-derived requirements
6. **"Satisfied by" is a soft link** — if the architecture entry is removed, the baseline entry re-activates automatically
