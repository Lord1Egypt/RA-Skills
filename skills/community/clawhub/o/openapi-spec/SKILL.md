---
name: openapi-spec
description: Deep OpenAPI workflow—design-first vs code-first, reusable schemas, security schemes, errors, examples, linting, compatibility, and codegen. Use when documenting REST APIs or driving clients and gateways from a spec.
---

# OpenAPI Specification (Deep Workflow)

OpenAPI is the **contract** between teams and tools. Quality comes from **consistent schemas**, **realistic examples**, and **lint rules** that catch breaking changes early.

## When to Offer This Workflow

**Trigger conditions:**

- New REST API; **public** or **partner** surface
- **Codegen** for clients/servers; **API gateway** validation from spec
- **Drift** between docs and implementation

**Initial offer:**

Use **six stages**: (1) workflow choice & ownership, (2) info & versioning, (3) resources & operations, (4) schemas & components, (5) security & errors, (6) lint, compatibility & publish). Confirm **OpenAPI** 3.x and **style guide**.

---

## Stage 1: Workflow & Ownership

**Goal:** **Design-first** (spec → implement) vs **code-first** (annotations → export)—pick one per service and **enforce**.

### Ownership

- **Who** approves breaking changes; **where** spec lives in repo

**Exit condition:** Single source of truth for the API contract.

---

## Stage 2: Info & Versioning

**Goal:** `info.title`, **version** scheme aligned with **URL** or **header** versioning strategy.

### Practices

- **Deprecation** policy in description or extension fields

---

## Stage 3: Resources & Operations

**Goal:** **RESTful** naming where appropriate; **operationId** stable for codegen.

### Practices

- **Pagination** (`cursor`/`page`), **filtering**, **sort** documented
- **Idempotency** (`Idempotency-Key`) for unsafe retries when relevant

---

## Stage 4: Schemas & Components

**Goal:** **`components/schemas`** reused; **nullable** vs **optional** correct in JSON Schema sense.

### Practices

- **OneOf** discriminated unions for polymorphic payloads when needed
- **Examples** per schema for human and machine readers

---

## Stage 5: Security & Errors

**Goal:** **`securitySchemes`** (Bearer, OAuth2) applied per operation or globally.

### Errors

- **Problem Details** (`application/problem+json`) pattern with **stable** `type` URIs

---

## Stage 6: Lint, Compatibility & Publish

**Goal:** **Spectral** or **vacuum** rules in CI; **openapi-diff** on PRs.

### Publish

- **Docs** portal (Swagger UI, Redoc); **postman** collections optional

---

## Final Review Checklist

- [ ] Single ownership and design-first or code-first discipline
- [ ] Versioning and deprecation story clear
- [ ] Operations complete with pagination/errors as needed
- [ ] Reusable components and examples
- [ ] Security and error model consistent
- [ ] CI lint and breaking-change detection

## Tips for Effective Guidance

- **Examples** should be **copy-paste valid**—catch enum drift.
- **Nullable** in OpenAPI 3.1 aligns with JSON Schema—**mind** **3.0** differences when mixing.
- **Internal** APIs still benefit from the same rigor—**future** you is a partner team.

## Handling Deviations

- **GraphQL** elsewhere: OpenAPI for **REST** **edge** only—don’t force one doc for both.
