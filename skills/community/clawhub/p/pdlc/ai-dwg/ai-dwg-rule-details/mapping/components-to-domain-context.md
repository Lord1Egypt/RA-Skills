<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Component Design (C4 L3) Bounded Contexts → domain-context.md

## Purpose

This mapping rule transforms the **bounded context definitions, entity model, and domain language** from the Component Design (C4 L3) document into a steering file that prevents the AI from inventing synonyms, violating domain boundaries, or misusing domain terminology during development.

**Output:** `rules/domain-context.md`

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Guard the ubiquitous language with zero tolerance — every synonym you allow creates confusion in code, tests, and conversations
- Derive the "NEVER Call It" column proactively — anticipate what a developer unfamiliar with the domain would mistakenly say
- Think about entity ownership as security boundary — only the owning context can mutate; violations are architectural bugs
- Ensure context boundaries align with module-structure.md dependency rules — if contexts are separate, modules MUST NOT directly depend
- Write domain rules as testable assertions, not aspirational statements — "MUST have exactly one" is enforceable; "should generally have" is not

### Anti-Patterns for This Activity
- Do NOT rename, abbreviate, or "improve" domain terms from the AP — terms are VERBATIM
- Do NOT leave entity ownership ambiguous — if the AP is unclear, flag for user resolution rather than guessing
- Do NOT skip cross-context disambiguation — same term with different meanings across contexts is a top source of bugs

### Quality Check
A good output from this activity sounds like:
- "Ubiquitous Language for Incident Management context: 'Incident' (NEVER call it Ticket, Issue, Bug, Problem, Case), 'Agent' (NEVER call it User, Operator, Staff)"
- "DR-3: An Incident MUST have exactly one assigned Agent at all times — enforcement: code + DB NOT NULL constraint"

---

## Source (AP Artifact)

**Document:** Component Design (typically `11_Component_Diagram_C4L3.md` or `design/component-design.md`)

**Sections to extract:**

| Section | Contains | What to Extract |
|---------|----------|----------------|
| Bounded Contexts | Named contexts with scope definition | Context names, boundaries, responsibilities |
| Module → Context mapping | Which modules belong to which context | Context-module registry |
| Core Domain Entities | Key entities per context | Entity names, ownership context |
| Relationships between contexts | How contexts communicate | Context map (upstream/downstream) |
| Ubiquitous Language | Domain-specific terms (if explicitly listed) | Term definitions |
| Domain rules / invariants | Business rules that must hold | Constraint rules |

**Additional sources (if DDD Tactical extension active):**
- Aggregate boundary definitions
- Value Object identification
- Domain Events catalog
- Anti-Corruption Layer specifications

---

## Target: domain-context.md

### Role

This steering file establishes the **ubiquitous language** — the single correct vocabulary for the project. It prevents:
- AI inventing alternative names for established concepts
- Developers using synonyms that create confusion
- Cross-context pollution (using Context A's terms inside Context B)
- Domain rule violations in code logic

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (C4 L3) | date: {generation-date} -->

# Domain Context

## System Domain

**Domain:** {high-level domain — e.g., "IT Service Management"}
**Subdomain classification:** {core | supporting | generic per bounded context}

## Bounded Contexts

<!-- begin: AP-sourced -->

| Context | Responsibility | Module(s) | Subdomain Type |
|---------|---------------|-----------|:--------------:|
| {Context A} | {what this context owns — 1 sentence} | `{module-a}`, `{module-b}` | Core |
| {Context B} | {responsibility} | `{module-c}` | Core |
| {Context C} | {responsibility} | `{module-d}` | Supporting |
| {Context D} | {responsibility} | `{module-e}` | Generic |

<!-- end: AP-sourced -->

## Context Map

<!-- begin: AP-sourced -->

```
┌────────────┐         ┌────────────┐
│ {Context A}│◄───ACL──│ {Context B}│
│  (upstream) │         │(downstream)│
└────────────┘         └────────────┘
       │
       │ Events
       ▼
┌────────────┐
│ {Context C}│
│(downstream)│
└────────────┘
```

| Upstream | Downstream | Relationship | Integration Pattern |
|----------|-----------|:------------:|-------------------|
| {Context A} | {Context B} | Customer-Supplier | ACL (Anti-Corruption Layer) |
| {Context A} | {Context C} | Publisher-Subscriber | Domain Events |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Ubiquitous Language

<!-- begin: AP-sourced -->

### {Context A}: {Context Name}

| Term | Definition | NEVER Call It |
|------|-----------|--------------|
| {Entity/Concept} | {precise definition within THIS context} | {wrong synonyms to avoid} |
| {Entity/Concept} | {definition} | {synonyms to reject} |
| ... | ... | ... |

**Context-specific rules:**
- In {Context A}, a "{term}" ALWAYS means {definition}
- A "{term}" MUST have {required properties}
- {term} can NEVER exist without {dependency}

### {Context B}: {Context Name}

| Term | Definition | NEVER Call It |
|------|-----------|--------------|
| ... | ... | ... |

{Repeat for each context}

<!-- end: AP-sourced -->

## Cross-Context Term Disambiguation

<!-- begin: AP-sourced -->

Some terms exist in multiple contexts with DIFFERENT meanings:

| Term | In Context A Means | In Context B Means | Rule |
|------|-------------------|-------------------|------|
| {term} | {meaning in A} | {meaning in B} | Use `{context-prefix}.{term}` when ambiguity exists |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Domain Rules (Invariants)

<!-- begin: AP-sourced -->

Rules that MUST hold true in the system at all times:

| # | Context | Rule | Enforcement |
|---|---------|------|-------------|
| DR-1 | {Context A} | {business rule — e.g., "An Incident MUST have exactly one assigned agent"} | Code + DB constraint |
| DR-2 | {Context A} | {rule} | {how enforced} |
| DR-3 | {Context B} | {rule} | {how enforced} |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Entity Ownership

<!-- begin: AP-sourced -->

Every entity belongs to EXACTLY ONE bounded context. No exceptions.

| Entity | Owning Context | Other Contexts See It As |
|--------|:-------------:|------------------------|
| {Entity A} | {Context A} | {read-only reference / ID only / event payload} |
| {Entity B} | {Context A} | {how other contexts reference it} |
| {Entity C} | {Context B} | {reference pattern} |
| ... | ... | ... |

**Rules:**
1. ONLY the owning context may CREATE, UPDATE, or DELETE the entity
2. Other contexts reference by ID only — NEVER hold a full copy
3. If another context needs data from the entity → use events or API query (per context map)

<!-- end: AP-sourced -->

## Naming Enforcement

| Rule | Example |
|------|---------|
| Use the EXACT term from this document in code | Class name: `Incident` not `Ticket`, `Issue`, or `Case` |
| Module/folder names match bounded context terms | `incident-management/` not `ticketing/` |
| Database tables use the domain term | `incidents` not `tickets` |
| API endpoints use the domain term | `/incidents` not `/tickets` |
| Events use context-prefixed names | `IncidentManagement.IncidentCreated` |

## Anti-Patterns (DO NOT)

1. **DO NOT** invent new domain terms — use ONLY what this document defines
2. **DO NOT** use generic names when a domain term exists (e.g., `item` when `Asset` is the term)
3. **DO NOT** let Context B's code reference Context A's internal entities directly
4. **DO NOT** create "shared" entities owned by multiple contexts — pick ONE owner
5. **DO NOT** skip the Anti-Corruption Layer when integrating across contexts
6. **DO NOT** expose internal domain events outside their context without explicit mapping
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Bounded context names + responsibilities | Copy to Context table | Bounded Contexts section |
| Module → context assignment | Map to Module(s) column | Context table |
| Core entities per context | Extract to Ubiquitous Language + Entity Ownership | Two sections |
| Context relationships (upstream/downstream) | Build Context Map diagram + table | Context Map section |
| Integration patterns between contexts | Map to relationship type + pattern | Context Map table |
| Entity names | Copy verbatim + add "NEVER Call It" column | Language table |
| Business rules / invariants | Convert to DR-N numbered rules | Domain Rules section |
| Terms with same name in multiple contexts | Build disambiguation table | Cross-Context section |

### Deriving "NEVER Call It" (Synonym Rejection)

For each domain term, derive common synonyms that developers might incorrectly use:

| Domain Term | Common Wrong Synonyms |
|-------------|----------------------|
| Incident | Ticket, Issue, Bug, Problem, Case |
| Service Request | Request, Order, Ticket |
| Change Request | CR, Change Order, Modification |
| Asset | Item, Device, Equipment, Resource |
| Configuration Item | CI, Config, Component |
| SLA | Agreement, Contract, Target |
| Agent | User, Operator, Staff, Employee |
| Tenant | Customer, Client, Organization, Account |

**Method:** For each entity, list 3-5 terms someone unfamiliar with the domain might use instead. These become explicit prohibitions.

### Deriving Domain Rules

From AP content, identify statements that describe things that MUST always be true:

| AP Statement Type | Convert To |
|------------------|-----------|
| "An X always has a Y" | DR: "{Entity} MUST have exactly one {related entity}" |
| "X cannot exist without Y" | DR: "{Entity} MUST NOT be created without {dependency}" |
| "Only Z can modify X" | DR: "ONLY {context/role} may modify {entity}" |
| "X transitions from A to B only through C" | DR: "{Entity} state transitions MUST follow: A → C → B" |
| Cardinality constraints | DR: "{Entity} has {min}-{max} {related entities}" |

---

## DDD Tactical Extension Enrichment

When the DDD Tactical extension was active in AI-ADLC, the domain-context.md gets significantly richer:

### Additional Sections (Extension Active)

```markdown
## Aggregates

| Aggregate Root | Context | Contains | Consistency Boundary |
|---------------|---------|----------|---------------------|
| {AggregateRoot} | {Context} | {list of entities/VOs within aggregate} | {what must be consistent within one transaction} |

## Value Objects

| Value Object | Context | Properties | Immutability Rule |
|-------------|---------|-----------|------------------|
| {ValueObject} | {Context} | {property list} | {what can never change once created} |

## Domain Events

| Event | Published By | Context | Payload | Consumed By |
|-------|-------------|---------|---------|-------------|
| {EventName} | {Aggregate} | {Context} | {key fields} | {consuming contexts} |

## Anti-Corruption Layers

| From Context | To Context | ACL Responsibility |
|-------------|-----------|-------------------|
| {External/Legacy} | {Our Context} | {what the ACL translates/protects against} |
```

### Enrichment Rules

1. Aggregate definitions add structure to Entity Ownership (aggregate roots own their children)
2. Value Objects appear in Ubiquitous Language with "immutable" annotation
3. Domain Events define the ONLY way contexts communicate asynchronously
4. ACLs define explicit translation boundaries in the Context Map

---

## Key Rules for This Mapping

1. **Terms are VERBATIM from AP** — never rename, abbreviate, or "improve" domain language
2. **Every entity has ONE owner** — if AP is ambiguous about ownership, flag for user resolution
3. **Context boundaries are walls** — module-structure.md dependency rules align with context boundaries
4. **Domain rules are enforceable** — write them as testable assertions, not aspirational statements
5. **"NEVER Call It" is critical** — this prevents AI (and developers) from inventing synonyms
6. **Context Map drives integration patterns** — how contexts talk is defined here, enforced in code
7. **This file is referenced by AI constantly** — it's the vocabulary check for every code generation

---

## Depth Adaptation

| Depth | domain-context.md |
|-------|-------------------|
| **Minimal** | Bounded context table + entity ownership + basic ubiquitous language (terms only, no "NEVER Call It") |
| **Standard** | Full structure as defined above — contexts, language, disambiguation, domain rules, entity ownership |
| **Comprehensive** | Full structure + DDD tactical enrichment (even without extension — if AP naturally describes aggregates) + example usage for each term + state machines for key entities |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| New bounded context added | New section in language, new rows in context table | Add; update context map |
| Entity moved between contexts | Entity ownership change, import rules change | Flag HIGH IMPACT — may require code refactoring |
| New domain term defined | New row in ubiquitous language | Add; derive "NEVER Call It" synonyms |
| Domain rule added | New DR-N entry | Add; signal AI-GCE for enforcement |
| Context relationship changed | Context map update | Update diagram + table; review affected module communication |
| Term renamed | All occurrences across ALL steering files | Flag for global rename — affects naming-conventions, api-standards, database-rules |
