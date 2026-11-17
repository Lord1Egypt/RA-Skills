<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: DDD Tactical Extension Enrichment

## Purpose

When the **DDD Tactical** extension was active in AI-ADLC, this mapping enriches the following steering files with DDD-specific patterns, rules, and conventions.

**Trigger:** `adlc-state.md` → Enabled Extensions includes `ddd-tactical`

---

## MANDATORY: Stage Sub-Role — Domain Modeller (DDD Specialist)

During THIS activity, ALSO adopt the mindset of a **Domain Modeller (DDD Specialist)**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in aggregate boundaries — the consistency boundary defines the transaction scope and repository pattern
- Ensure Value Objects are IMMUTABLE in rules — this is the most commonly violated DDD principle in code
- Domain Events are the ONLY cross-aggregate communication mechanism — never direct method calls between aggregates
- Name DDD concepts with precision: Aggregate Root is the entry point, Repository per Aggregate Root only, Factory for complex creation
- Enrichment is ADDITIVE — DDD rules layer onto existing steering files without replacing their base content

### Anti-Patterns for This Activity
- Do NOT allow repositories per child entity — only Aggregate Root gets a repository
- Do NOT put domain logic in application or infrastructure layers — domain layer owns all business rules
- Do NOT generate DDD enrichment unless the `ddd-tactical` extension is confirmed active in adlc-state.md

### Quality Check
A good output from this activity sounds like:
- "DDD-MOD-02: Aggregate Root is the ONLY public interface of its module — external modules call aggregate root methods only. Repository interface: `I{AggregateRoot}Repository`."
- "DDD-CODE-03: Value Objects are IMMUTABLE — create new instance for changes. Naming: PascalCase descriptive (`EmailAddress`, `Priority`, `MoneyAmount`)."

---

## Files Enriched

| File | Enrichment |
|------|-----------|
| `domain-context.md` | Aggregates table, Value Objects table, Domain Events catalog, ACL specifications |
| `module-structure.md` | Aggregate-aligned module boundaries, aggregate root as entry point rule |
| `naming-conventions.md` | DDD naming patterns (AggregateRoot suffix, ValueObject conventions, Event naming) |
| `database-rules.md` | DB-AGG rules activated (one transaction per aggregate, ID-only references) |
| `coding-standards.md` | DDD tactical patterns section (aggregate implementation, domain event publishing) |

---

## Enrichment Rules

### domain-context.md Additions

Add after Entity Ownership section:

```markdown
## Aggregates

| Aggregate Root | Context | Contains | Consistency Boundary |
|---------------|---------|----------|---------------------|
| {from AP} | {context} | {entities + VOs within} | {what's transactionally consistent} |

## Value Objects

| Value Object | Context | Properties | Immutable |
|-------------|---------|-----------|:---------:|
| {from AP} | {context} | {property list} | ✅ |

## Domain Events

| Event | Published By | Payload | Consumed By |
|-------|-------------|---------|-------------|
| {EventName} | {Aggregate} | {key fields} | {consumers} |

## Anti-Corruption Layers

| From | To | Translation |
|------|-----|------------|
| {external} | {our context} | {what ACL does} |
```

### module-structure.md Additions

Add to Dependency Rules:

```markdown
### DDD Module Rules

| Rule | Standard |
|------|----------|
| DDD-MOD-01 | Module boundaries ALIGN with aggregate boundaries — one aggregate per module (or module per bounded context containing its aggregates) |
| DDD-MOD-02 | Aggregate Root is the ONLY public interface of its module — external modules call aggregate root methods only |
| DDD-MOD-03 | Cross-aggregate communication: via Domain Events — NEVER direct method calls between aggregates |
| DDD-MOD-04 | Repository per Aggregate Root — NEVER per child entity |
```

### naming-conventions.md Additions

```markdown
## DDD Naming Patterns

| Concept | Convention | Example |
|---------|-----------|---------|
| Aggregate Root class | PascalCase, no suffix needed (IS the entity) | `Incident`, `ServiceRequest` |
| Value Object class | PascalCase + `VO` suffix OR descriptive name | `EmailAddress`, `Priority`, `MoneyAmount` |
| Domain Event class | PascalCase, past tense | `IncidentCreated`, `IncidentEscalated` |
| Domain Service | PascalCase + `Service` suffix | `SlaEvaluationService` |
| Repository interface | `I{AggregateRoot}Repository` | `IIncidentRepository` |
| Factory | `{AggregateRoot}Factory` | `IncidentFactory` |
| Specification | `{Description}Specification` | `OverdueIncidentSpecification` |
```

### database-rules.md Additions

Activate DB-AGG section (already templated in data-to-steering.md).

### coding-standards.md Additions

```markdown
## DDD Tactical Patterns

| Rule | Standard |
|------|----------|
| DDD-CODE-01 | Aggregate roots enforce ALL business invariants — never bypass via direct DB update |
| DDD-CODE-02 | Domain events published WITHIN aggregate methods — not by calling code |
| DDD-CODE-03 | Value objects are IMMUTABLE — create new instance for changes |
| DDD-CODE-04 | Domain logic lives in domain layer — NEVER in application/infrastructure layers |
| DDD-CODE-05 | Factories for complex aggregate creation — NEVER construct directly with `new` when creation has rules |
```

---

## Key Rule

DDD enrichment is ADDITIVE — it adds sections and rules to existing files. It does NOT replace the base content generated by the standard mappings.
