<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Event Sourcing + CQRS

## When This Extension Applies

Your system likely needs Event Sourcing / CQRS if:

- Full audit trail of ALL state changes is a hard requirement (regulatory, legal)
- Need to reconstruct state at any point in time (temporal queries)
- Complex domain with many state transitions (workflows, financial transactions)
- Read and write models have fundamentally different shapes or scale
- Event-driven architecture is the primary communication pattern

## Opt-In Question

```
### Would you like to apply Event Sourcing + CQRS patterns?

This extension adds detailed guidance for:
- Event store design (append-only, stream-per-aggregate, snapshots)
- Event schema design (versioning, upcasting, backward compatibility)
- Projection/read model design (how to build query-optimized views from events)
- CQRS separation (command side vs. query side; eventual consistency)
- Snapshot strategy (when to snapshot, performance optimization)
- Replay and rebuilding projections (disaster recovery, new read models)
- Saga/process manager patterns (long-running workflows across aggregates)

(a) Yes — Design with Event Sourcing and CQRS
(b) No — Standard CRUD data model is sufficient

Recommended for: Audit-critical systems, financial/legal domains, complex state machines
Skip if: Simple CRUD, no temporal query needs, team unfamiliar with event sourcing
⚠️ Warning: Event Sourcing adds significant complexity. Only adopt if the benefits clearly justify the cost.
```

## Status: ✅ Available (v1.1)
