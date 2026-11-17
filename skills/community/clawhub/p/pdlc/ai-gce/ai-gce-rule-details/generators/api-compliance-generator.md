<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# API Compliance — Derivation Logic

## Purpose

Derives API-first compliance rules (GOV-API-*) from `api-standards.md` and optionally `api-versioning.md`. 100% steering-derived — no built-in baseline for this category (API patterns are entirely project-specific).

---

## MANDATORY: Stage Sub-Role — API Designer

During THIS activity, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think contract-first: the API spec (OpenAPI/Swagger) is the source of truth — code implements the contract, never the reverse
- Treat contract-before-code as 🔴 Critical: an endpoint without a contract is an undocumented commitment
- Derive URL conventions, error formats, and pagination from api-standards.md — these are design decisions, not arbitrary rules
- Consider versioning lifecycle: breaking changes without version bumps break consumers
- Ensure file patterns target controller/endpoint files specifically (where API behavior is defined)

### Anti-Patterns for This Activity
- Do NOT generate API rules if api-standards.md is missing (this category is 100% steering-derived)
- Do NOT conflate API style rules (URL format, error shape) with API security rules (auth, CORS)
- Do NOT create versioning rules unless api-versioning.md explicitly exists

### Quality Check
A good output from this activity sounds like:
- "GOV-API-001: Contract MUST exist before controller implementation. Severity: 🔴 Critical. Enforced by api-contract-check.json (fileCreated on controller files). Pattern: `src/modules/*/presentation/**/*.controller.ts`."
- "api-versioning.md exists → API-VER-01/02/03 generated. Breaking change = mandatory version increment. Tier 2."

---

## Source Steering Files

| File | What to Extract | Conditional? |
|------|----------------|:------------:|
| `api-standards.md` | REST conventions, URL patterns, error format, pagination, spec format, auth approach | Always |
| `api-versioning.md` | Version lifecycle, breaking change rules, deprecation process | IF exists |

---

## Extraction → Rule Transformation

### From `api-standards.md`

| Steering Section | Generated Rules |
|-----------------|----------------|
| Spec format (e.g., "OpenAPI 3.1") | GOV-API-001: Contract MUST exist before controller implementation |
| URL conventions (e.g., "kebab-case, /api/v1/{resource}") | GOV-API-004: URL format compliance |
| Error format (e.g., "RFC 7807 Problem Details") | GOV-API-005: Error responses MUST follow stated format |
| Pagination (e.g., "cursor-based, envelope response") | GOV-API-006: All list endpoints MUST include pagination |
| Authentication (e.g., "Bearer JWT on all endpoints") | GOV-API-007: Auth header required on all non-public endpoints |

### From `api-versioning.md` (Conditional)

| Steering Section | Generated Rules |
|-----------------|----------------|
| "Breaking changes require version bump" | API-VER-01: Breaking change = mandatory version increment |
| "Deprecation: mark deprecated, support 2 versions" | API-VER-02: Deprecated endpoints maintained for stated period |
| "Version in URL path: /api/v{n}/" | API-VER-03: Version number in URL prefix |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `api-contract-check.json` | fileCreated (controller files) | GOV-API-001: contract before implementation |
| `pre-pr-checklist.json` | userTriggered | GOV-API-001/004/005/006 (full API check) |

---

## File Pattern Derivation

The api-contract-check hook watches for NEW controller/endpoint files:

| Technology | Pattern |
|-----------|---------|
| NestJS | `src/modules/*/presentation/**/*.controller.ts` |
| Django | `**/views.py`, `**/viewsets.py` |
| ASP.NET | `**/Presentation/**/*Controller.cs`, `**/*Endpoints.cs` |
| Spring Boot | `**/controller/*Controller.java` |

---

## Severity Assignment

| Rule Type | Severity |
|-----------|:--------:|
| Contract-before-code (API-001) | 🔴 Critical |
| Breaking change without version bump | 🔴 Critical |
| Error format non-compliance | 🟠 High |
| Missing pagination | 🟠 High |
| URL convention violation | 🟡 Medium |

---

## Tier Assignment

All GOV-API-* rules: **Tier 1** (API-first is a foundational principle active from Day 0).
API-VER-* rules: **Tier 2** (versioning matters when multiple versions coexist).
