<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Test Taxonomy

## Purpose

AI-TGE uses a structured, standards-based test taxonomy to classify every test requirement in the register. This document defines the classification system, mapping rules from architecture artifacts to test types, and the vocabulary used throughout all TGE outputs.

The taxonomy is based on **ISTQB (International Software Testing Qualifications Board)** standards, adapted for architecture-driven test governance.

---

## Classification Dimensions

Every test requirement in the register is classified on THREE dimensions:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST CLASSIFICATION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Dimension 1: TEST LEVEL (scope of what's verified)              │
│  ─────────────────────────────────────────────────               │
│  Unit → Integration → System → Acceptance                        │
│                                                                  │
│  Dimension 2: TEST TYPE (focus of verification)                  │
│  ─────────────────────────────────────────────                   │
│  Functional / Non-Functional / Structural                        │
│                                                                  │
│  Dimension 3: TEST TECHNIQUE (how it's derived)                  │
│  ──────────────────────────────────────────────                  │
│  Architecture-Derived / Baseline / Story-Derived / Manual        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dimension 1: Test Level

Test levels define the **scope** of what a test verifies — from a single function to an entire user workflow.

| Level | What It Verifies | Scope | Typical Owner |
|-------|-----------------|-------|---------------|
| **Unit** | Individual function, method, or class logic in isolation | Single component/module | Developer |
| **Integration** | Interaction between 2+ components or services | Component boundaries | Developer / QA |
| **System** | End-to-end behavior of the complete system under realistic conditions | Full stack (all layers) | QA Engineer |
| **Acceptance** | Business requirements met from user/stakeholder perspective | User workflow (business value) | QA / Product Owner |

### Level Hierarchy

```
Acceptance  ─── Does the system deliver business value?
    │
System      ─── Does the full system work end-to-end?
    │
Integration ─── Do components work together correctly?
    │
Unit        ─── Does each piece work in isolation?
```

### Level Selection Rules

| If the commitment involves... | Level = |
|------------------------------|---------|
| A single business rule or calculation | Unit |
| Two components communicating (API call, DB query, message) | Integration |
| A complete user-facing flow through multiple layers | System |
| A business requirement with acceptance criteria | Acceptance |
| A contract between services (schema validation) | Integration |
| Performance under load (response times, throughput) | System |
| Security of a single auth mechanism | Integration |
| Security of the full authentication flow | System |

---

## Dimension 2: Test Type

Test types define the **focus** of what a test verifies — correctness, quality attributes, or internal structure.

### Functional Tests

Verify that the system **does what it's supposed to do** (correct behavior).

| Sub-Type | Focus | Examples |
|----------|-------|---------|
| **Business Logic** | Core domain rules produce correct results | Calculation accuracy, workflow state transitions, validation rules |
| **Contract** | API request/response matches defined schema | Endpoint returns correct status codes, payload structure matches OpenAPI spec |
| **Data Integrity** | Write → read → verify cycle maintains correctness | CRUD operations preserve data, referential integrity held, migrations reversible |
| **Workflow** | Multi-step processes complete correctly end-to-end | Order flow (create → pay → fulfill → complete), approval chains |
| **Error Handling** | System responds correctly to invalid/unexpected input | Graceful degradation, meaningful error messages, no data corruption on failure |
| **Boundary** | Edge cases and limits handled correctly | Max values, empty inputs, concurrent access, overflow scenarios |

### Non-Functional Tests

Verify **quality attributes** (how well the system performs, not what it does).

| Sub-Type | Focus | Examples |
|----------|-------|---------|
| **Performance** | Response times and throughput under expected load | API latency ≤ 200ms at p95, throughput ≥ 1000 req/s |
| **Load** | Behavior under peak/sustained load | System handles 10x normal traffic without degradation |
| **Security** | Protection against threats and unauthorized access | Authentication bypass attempts fail, authorization enforced, injection prevented |
| **Reliability** | System recovers from failures gracefully | Auto-reconnect on DB failure, retry mechanisms work, circuit breakers trip |
| **Scalability** | System handles growth (data, users, throughput) | Horizontal scaling works, no single-point bottlenecks |
| **Accessibility** | Usable by people with disabilities | WCAG 2.1 AA compliance, screen reader compatibility |
| **Compatibility** | Works across environments/browsers/versions | Cross-browser rendering, API backward compatibility |

### Structural Tests

Verify **internal code quality** and architecture conformance.

| Sub-Type | Focus | Examples |
|----------|-------|---------|
| **Coverage** | Code paths exercised by tests | Branch coverage ≥ 80%, critical paths 100% |
| **Architecture Conformance** | Code structure matches designed architecture | Module boundaries respected, no circular dependencies |
| **Complexity** | Code maintainability metrics within thresholds | Cyclomatic complexity ≤ 10, coupling below threshold |

---

## Dimension 3: Test Technique (Derivation Source)

How the test requirement was identified — important for traceability.

| Technique | Source | Traceability |
|-----------|--------|-------------|
| **Architecture-Derived** | Specific AP artifact (API contract, ADR, component design, integration map) | Links to commitment ID in AP |
| **Baseline** | Universal built-in requirement (every API needs contract tests, every auth needs security tests) | Links to baseline rule in two-source-model.md |
| **Story-Derived** | User story acceptance criteria from aidlc-docs | Links to story ID |
| **Manual** | User explicitly added a test requirement not derivable from other sources | Links to user decision (timestamp + rationale) |

---

## Architecture-to-Test Mapping

### Primary Mapping Table

This is the master reference for deriving test requirements from AP artifacts:

| AP Artifact | Test Level | Test Type | Sub-Type | Register Entry Pattern |
|-------------|-----------|-----------|----------|----------------------|
| API contract (endpoint definition) | Integration | Functional | Contract | Contract test per endpoint (request schema + response schema + status codes) |
| API contract (error responses) | Integration | Functional | Error Handling | Negative test per documented error case |
| Security decision (ADR — authentication) | System | Non-Functional | Security | Auth flow verification (valid credentials succeed, invalid fail, expired handled) |
| Security decision (ADR — authorization) | Integration | Non-Functional | Security | Role-based access test per role × resource combination |
| Component design (business logic) | Unit | Functional | Business Logic | Unit test per business rule identified in component |
| Component design (state machine) | Unit | Functional | Workflow | State transition test per valid/invalid transition |
| Integration map (external system) | Integration | Functional | Contract | Integration test per external system (connectivity + error handling + timeout) |
| Integration map (async messaging) | Integration | Functional | Workflow | Message publish/consume test (delivery + ordering + dead-letter) |
| Data model (entity definition) | Integration | Functional | Data Integrity | CRUD test per entity (create → read → update → delete → verify) |
| Data model (migration) | Integration | Functional | Data Integrity | Migration up/down test (apply → verify → rollback → verify) |
| NFR commitment (performance SLA) | System | Non-Functional | Performance | Performance test per stated SLA (latency, throughput, concurrency) |
| NFR commitment (reliability SLA) | System | Non-Functional | Reliability | Resilience test per stated recovery target (failover, retry, degradation) |
| NFR commitment (scalability target) | System | Non-Functional | Load | Load test at stated scale target (users, data volume, request rate) |
| Multi-tenancy architecture | Integration | Non-Functional | Security | Tenant isolation test (cross-tenant data leak prevention) |
| Multi-tenancy architecture | Integration | Functional | Data Integrity | Tenant data segregation test (queries scoped correctly) |
| User story (acceptance criteria) | Acceptance | Functional | Workflow | Acceptance test per criterion (one test per "given-when-then") |
| Configuration (feature flags, env vars) | Unit | Functional | Boundary | Config validation test (valid inputs accepted, invalid rejected, defaults work) |

### Mapping Rules

1. **One AP artifact can produce MULTIPLE test requirements** — an API endpoint may need a contract test (happy path), error tests (each error code), and a security test (auth required)
2. **Test level is determined by scope** — if it crosses a component boundary, it's Integration minimum
3. **Test type is determined by focus** — if it's about "does it work?" = Functional; "how well?" = Non-Functional
4. **Sub-type is determined by the specific quality concern** — narrow the focus
5. **Never derive the same test twice** — if an API endpoint already has a contract test from the API contract, don't create a duplicate from the component design

---

## Test Pyramid Guidance

AI-TGE recommends test distribution aligned with the test pyramid:

```
        ╱╲
       ╱  ╲        Acceptance (5-10%)
      ╱────╲       Broad, expensive, slow — verify business value
     ╱      ╲
    ╱  Sys   ╲     System (10-20%)
   ╱──────────╲    End-to-end, realistic — verify full stack
  ╱            ╲
 ╱ Integration  ╲   Integration (20-30%)
╱────────────────╲  Component boundaries — verify interactions
╱                  ╲
╱       Unit        ╲  Unit (40-60%)
╱────────────────────╲  Fast, isolated — verify logic
```

### Pyramid Ratios by Depth Level

| Depth Level | Unit | Integration | System | Acceptance |
|-------------|:----:|:-----------:|:------:|:----------:|
| Minimal | 60% | 25% | 10% | 5% |
| Standard | 50% | 25% | 15% | 10% |
| Comprehensive | 40% | 30% | 20% | 10% |

**Note:** These are TARGET ratios for the register. Actual coverage may vary based on architecture complexity. A system with many integrations will naturally skew toward Integration tests.

---

## Register Entry Classification Format

Every entry in the test register uses this classification:

```markdown
| Commitment ID | Test Level | Test Type | Sub-Type | Test Name | Source | Risk Score | Status |
```

**Example entries:**

| Commitment ID | Level | Type | Sub-Type | Test Name | Source | Risk | Status |
|:-------------:|:-----:|:----:|:--------:|-----------|:------:|:----:|:------:|
| API-001 | Integration | Functional | Contract | POST /users returns 201 with valid payload | Architecture | 225 | Missing |
| API-001 | Integration | Functional | Error Handling | POST /users returns 400 on invalid email | Architecture | 75 | Exists |
| SEC-001 | System | Non-Functional | Security | JWT auth rejects expired tokens | Architecture | 500 | Missing |
| BL-003 | Unit | Functional | Business Logic | Discount calculation applies tier correctly | Architecture | 150 | Exists |
| BASE-API-01 | Integration | Functional | Contract | Every endpoint responds to OPTIONS (CORS) | Baseline | 50 | Missing |
| STORY-012-AC3 | Acceptance | Functional | Workflow | User can complete checkout with saved card | Story | 300 | Missing |

---

## Vocabulary Reference

### Status Values

| Status | Meaning |
|--------|---------|
| **Required** | Derived from source; not yet checked against codebase |
| **Exists** | Matching test found in test directory |
| **Missing** | No matching test found; gap flagged |
| **Failing** | Test exists but is currently failing |
| **Deprecated** | Commitment removed/changed; test no longer required |
| **Overridden** | User explicitly declined this requirement (with rationale) |

### Risk Score Interpretation

| Score Range | Bucket | Action Required |
|:-----------:|--------|----------------|
| 400-625 | **Critical** | Test immediately — high risk of production failure |
| 150-399 | **High** | Test within current sprint — significant exposure |
| 50-149 | **Medium** | Test within next 2 sprints — manageable risk |
| 1-49 | **Low** | Test when convenient — minimal exposure |

### Source Values

| Source | What It Means |
|--------|---------------|
| Architecture | Derived from a specific AP artifact (commitment ID links to AP) |
| Baseline | Applied from built-in universal requirement (see two-source-model.md) |
| Story | Derived from user story acceptance criteria |
| Manual | User explicitly added (not auto-derived) |
| Reconciliation | Added during AP reconciliation (new commitment detected) |

---

## Taxonomy Consistency Rules

1. **Never mix levels in one register entry** — a test is ONE level (Unit OR Integration, not both)
2. **Never assign a type without a sub-type** — "Functional" alone is too vague; always specify (Contract, Business Logic, etc.)
3. **Source must be traceable** — every entry links back to its derivation point (commitment ID, baseline rule, or story ID)
4. **Risk score is ALWAYS calculated** — even for existing tests (they may have different priority for maintenance)
5. **Deprecated ≠ Deleted** — deprecated entries stay in the register for audit trail; just excluded from coverage calculations
6. **One commitment can produce many tests** — but one test entry maps to exactly ONE commitment (if a test covers multiple, split into separate entries)
