<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: DDD Tactical Patterns

## When This Extension Applies

Your system likely needs DDD tactical patterns if:

- You chose "Domain-Driven Design" as decomposition strategy (Stage 12)
- Multiple bounded contexts with complex business logic
- Domain entities have complex lifecycle rules and invariants
- Business events drive cross-domain workflows
- You need Anti-Corruption Layers between domains or external systems

## Opt-In Question

```
### Would you like to apply DDD Tactical Patterns?

This extension adds detailed guidance for:
- Aggregate design rules (consistency boundaries, transaction scope)
- Domain Events catalog (naming, payload, handling patterns)
- Value Objects vs. Entities (identification rules)
- Anti-Corruption Layers (translation between bounded contexts)
- Domain Services (logic that doesn't belong to a single entity)
- Repository patterns (aggregate persistence rules)

(a) Yes — Apply DDD tactical patterns to component design
(b) No — Standard module design is sufficient for this system

Recommended for: Complex domain logic, multiple bounded contexts, event-driven flows
Skip if: Simple CRUD operations, data-centric application, thin business logic layer
```

## Status: ✅ Available (v1.1)
