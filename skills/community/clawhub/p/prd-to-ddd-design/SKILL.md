---
name: prd-to-ddd-design
description: Convert natural language requirements (PRD) into AI-friendly DDD domain design documents in Markdown. Use when the user provides a PRD, requirement doc, or business description and wants a DDD domain model, entity/aggregate design, ER diagram, domain logic placement, or sequence/flow diagrams. Produces structured output that AI agents can directly use for implementation.
---

# PRD to DDD Domain Design

Convert PRD / natural language requirements into a structured DDD design document.

## When to Use

- User provides a PRD, requirement document, or business description
- User asks: "把需求转成DDD设计" / "领域建模" / "domain modeling from requirement"
- Before implementation — this is the first step in the AI development workflow

## Relationship to Other Skills

- **design-to-plan**: After this skill produces the design doc → split into implementation plans
- **ddd-domain-model** / **ddd-cross-layer**: Implementation patterns → use after design is finalized

## Resources

| File | Role | When to Read |
|------|------|-------------|
| **This file (SKILL.md)** | Map — workflow, phases, output rules | Always (auto-loaded) |
| [phase-guide.md](phase-guide.md) | How-to — analysis heuristics, design criteria, identification rules | When executing each phase |
| [ddd-design-template.md](ddd-design-template.md) | Template — output section structure with table formats | When writing the design doc |

---

## Workflow

```
PRD / Natural Language
        │
        ▼
  Phase 0 → 1 → 2 → 3 → 4 → 4.5 → 5 → 5.5 → 6
        │
        ▼
  Output: docs/design/<feature>-ddd-design.md
```

## Phase Summary

| Phase | Name | What to Produce | Key Input |
|-------|------|----------------|-----------|
| 0 | Event Storming | Actor → Command → Aggregate → Event → Policy flow | PRD text |
| 1 | Domain Discovery | Ubiquitous language glossary, domain events, business rules | PRD nouns/verbs |
| 2 | Strategic Design | Bounded contexts, context mapping | Phase 0-1 results |
| 3 | Tactical Design | Entities, VOs, aggregates, relationships | Phase 1-2 results |
| 4 | ER Modeling | Mermaid ER diagram (PK/FK only) | Phase 3 entities |
| 4.5 | Database Schema | Table mapping, columns, indexes, constraints | Phase 3-4 entities |
| 5 | Logic Placement | Entity/VO logic, Gateway/Repo interfaces, Domain Services | Phase 3 + PRD rules |
| 5.5 | Cross-Layer Contracts | REST API, Client DTOs, AppService API, Infra adapters | Phase 5 results |
| 6 | Behavior Modeling | State machines, sequence diagrams, flowcharts, event flows | Phase 0 + 5 |

**For detailed instructions on each phase** (extraction rules, identification heuristics, design criteria), read [phase-guide.md](phase-guide.md).

---

## Execution Steps

1. **Read the PRD** document provided by user
2. **Read [phase-guide.md](phase-guide.md)** for analysis heuristics
3. **Execute phases 0-6 sequentially**, using [ddd-design-template.md](ddd-design-template.md) as the output structure
4. **Run the Quality Checklist** below before finalizing
5. **Save** to `docs/design/<feature-name>-ddd-design.md`

---

## Output Rules

- Pure Markdown with Mermaid diagrams
- Chinese for business descriptions, English for technical terms (class names, method signatures)
- Align naming and layer placement with `ddd-architecture` rule
- Align domain purity with `ddd-domain-layer` rule
- Every entity must have behaviors (no anemic model)
- Every aggregate must list invariants
- Every domain logic item must have placement rationale
- Database schema must map all entities/VOs to tables with complete columns
- Cross-layer contracts must be defined with input/output types

---

## Quality Checklist

Before finalizing the document, verify:

**Event Storming & Discovery (Phase 0-1)**
- [ ] All Actors, Commands, Specs, Events, Policies identified
- [ ] Command → Aggregate → Event mapping is complete
- [ ] All business nouns mapped to entities or value objects
- [ ] All business rules captured with rule IDs
- [ ] Ubiquitous language glossary includes Package column

**Tactical Design (Phase 2-3)**
- [ ] Aggregates are small with clear boundaries
- [ ] No cross-aggregate direct object references (use ID)
- [ ] Entity behaviors are rich (no anemic model)
- [ ] State machines documented for stateful entities
- [ ] Naming follows project DDD conventions

**Data & Logic (Phase 4-5)**
- [ ] ER diagram only shows PK/FK, consistent with entity/VO tables
- [ ] Entity → Table mapping covers all entities and value objects
- [ ] Table Detail includes all columns with type, nullable, default
- [ ] Indexes defined for FK columns, frequent queries, unique keys
- [ ] Domain logic placement has clear rationale for every item
- [ ] Domain Service design decisions documented with alternatives

**Cross-Layer & Behavior (Phase 5.5-6)**
- [ ] REST API endpoints listed with URL, HTTP method, request/response types
- [ ] Client DTOs (Request/Response) key fields defined
- [ ] AppService methods listed with Command input and DTO output
- [ ] Infrastructure adapter-to-gateway mapping is complete
- [ ] Sequence diagrams cover all core use cases
- [ ] Flowcharts cover complex branching rules (2+ paths)
