# Phase Guide — Analysis Heuristics & Design Criteria

This file contains the "how to think" instructions for each phase. The output format (table structures, Mermaid templates) is in [ddd-design-template.md](ddd-design-template.md).

---

## Phase 0: Event Storming

### How to Extract from PRD

1. **Identify Actors**: Scan for roles, users, systems, schedulers mentioned in the PRD
2. **Identify Commands**: Look for actions — "user can...", "system shall...", "when X clicks..."
3. **Commands belong to Application layer**, not Domain. Entity never sees a Command
4. **Command Specs**: Extract preconditions from "must be", "required", "only if" — but only for Command input parameters. Domain type invariants are NOT Command specs
5. **Domain Events**: Look for "after X happens...", "when Y is completed...", state changes
6. **Policies**: "When event X occurs, automatically do Y" — reactive rules
7. **External Systems**: Any API, service, database mentioned → Gateway interface

### Color Coding for Mermaid

Actor (gold), Command (blue), Event (orange), Aggregate (yellow), Policy (purple), Read Model (green), External System (pink), Spec (light yellow).

---

## Phase 1: Domain Discovery

### PRD Text → Domain Model Extraction Rules

| PRD Signal | Domain Candidate |
|-----------|-----------------|
| Nouns with unique identity / lifecycle | Entity |
| Nouns defined purely by attributes (no identity) | Value Object |
| Verbs / state transitions | Domain Event or Command |
| "Must", "should", "cannot", "only if" | Domain Rule / Invariant |
| Calculations, formulas | Domain Logic (method) |
| Closed set of named values | Enum |

### Rule Classification

| Type | Definition | Where to Enforce |
|------|-----------|-----------------|
| **Invariant** | Must always hold | Inside entity/aggregate |
| **Precondition** | Must hold before operation | Method entry check |
| **Policy** | Business rule that may vary | Strategy pattern |

---

## Phase 2: Strategic Design

### Bounded Context Identification Heuristics

- Different teams or departments → likely different contexts
- Different data ownership → separate contexts
- Same term with different meaning in different context → context boundary
- Different rate of change → separate contexts

### Context Mapping Relationship Types

| Type | When to Use |
|------|------------|
| Partnership | Two teams cooperate on shared model |
| Shared Kernel | Small shared model between contexts |
| Customer-Supplier | Upstream serves downstream's needs |
| Conformist | Downstream adopts upstream's model as-is |
| Anti-Corruption Layer (ACL) | Translate between incompatible models |
| Open Host Service (OHS) | Upstream provides well-defined API |
| Published Language | Shared standard format (e.g., JSON schema) |

---

## Phase 3: Tactical Design

### Entity vs Value Object Decision

| Criterion | Entity | Value Object |
|-----------|--------|-------------|
| Has unique business identity? | Yes | No |
| Has lifecycle / state transitions? | Yes | No |
| Mutable? | Yes | No (immutable) |
| Compared by? | Identity | Attribute values |
| Contains behavior? | Must have (avoid anemic) | Optional |

### Aggregate Design Rules

1. Single aggregate root per aggregate
2. External access only through root
3. Children modified only through root methods
4. Consistency boundary = transaction boundary
5. Keep aggregates small — prefer references by ID across aggregates
6. One repository per aggregate (named after root)

### Inheritance Hierarchy

If entities share common structure via inheritance:
- Document the hierarchy tree
- Create a **polymorphic method comparison table** showing how each subclass implements abstract methods differently
- This table consolidates behavior differences that would otherwise be scattered across files

---

## Phase 4: ER Modeling

### ER Diagram Rules

- **Only show PK/FK fields** — full attributes are in Phase 3 entity/VO tables
- Show aggregate boundaries with `%% ========== Aggregate: Name ==========` comments
- Cross-aggregate references use dashed lines (`}o..||`) with ID-only
- Add note: "ER 图只展示实体间关系和标识字段（PK/FK），完整属性参见 Section 5/6"

---

## Phase 4.5: Database Schema

### Mapping Strategies

| Strategy | When to Use |
|----------|------------|
| **One-to-one** | Entity maps directly to a table |
| **Embedded** | VO columns merged into parent entity's table (simple, single-valued) |
| **Separate table** | VO in its own table (multi-valued or complex) |

### Design Decisions to Document

- Value Object storage: embedded columns vs separate table
- Soft delete vs hard delete
- JSON column vs normalized tables
- ID generation strategy (AUTO_INCREMENT, UUID, Snowflake)
- Sharding / partitioning (if applicable)

---

## Phase 5: Domain Logic Placement

### Placement Decision Table

```
Logic depends on...                → Place in...
─────────────────────────────────────────────────
Own entity attributes only         → Entity method
Aggregate internal state           → Aggregate root method
Multiple aggregates/entities       → DomainService
External API / remote call         → Gateway (interface in domain)
Persistence / data retrieval       → Repository (interface in domain)
Use-case orchestration             → ApplicationService
DTO ↔ domain conversion            → Assembler / Converter
```

### Gateway & Repository Rules (Project Conventions)

- One gateway interface per logical data concern (ISP)
- One adapter per gateway in infrastructure
- Repository interface in domain, implementation in infrastructure
- Facade gateway for orchestrating multiple load gateways

### Complex Domain Service Documentation

For complex Domain Services, expand with:
- **Collaboration tree**: show delegation to sub-builders/calculators
- **Design decision table**: choice, rationale, rejected alternatives
- **Input/output contracts**: method → input → output → guarantees
- **Polymorphic behavior**: cross-reference Entity inheritance hierarchy (don't duplicate)

---

## Phase 5.5: Cross-Layer Contracts

### What to Define per Layer

| Layer | What to Specify |
|-------|----------------|
| **Adapter** | REST endpoints: HTTP method, URL, Controller, method name, request/response body |
| **Client** | API interfaces (service contracts), Requests (fields + validation), Responses (fields + source), Shared DTOs |
| **Application** | AppService public methods: input (Command/param), output (DTO), orchestration summary |
| **Infrastructure** | Gateway interface → Adapter class → Converter → External client mapping |

### Key Principles

- `Orchestration Summary` uses step descriptions: `validate → load → process → save`
- Single primitive parameter → no Command object needed
- API Interface in `client.api` package; Controller implements it

---

## Phase 6: Behavior Modeling

### Diagram Type Selection

| Diagram | Use When | DDD Layer |
|---------|----------|-----------|
| State Machine | Entity has lifecycle states | Entity |
| Sequence Diagram | Show use case orchestration flow | Application |
| Flowchart | Method has 2+ branching paths | Entity / Domain Service |
| Domain Event Flow | Events trigger cross-aggregate actions | Cross-layer |

### Scope Rules

- **Sequence diagrams**: Only show Application Service scope (Controller → AppService → DomainService → Repo → Gateway). Do NOT show entity internal methods
- **Flowcharts**: Only for complex branching. Skip for simple CRUD or linear calls
- **State machines**: Only for entities with explicit lifecycle status field
