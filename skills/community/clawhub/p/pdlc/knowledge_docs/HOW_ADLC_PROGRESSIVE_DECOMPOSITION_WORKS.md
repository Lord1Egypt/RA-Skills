# How AI-ADLC Progressive Decomposition Works

**Purpose:** Explains how AI-ADLC uses the C4 model to progressively decompose system architecture — from boundaries to internals — and why this discipline prevents premature detail.

---

## What Progressive Decomposition Means

AI-ADLC follows a strict C4-model decomposition discipline: define boundaries before internals. You cannot discuss component internals until container boundaries are stable. You cannot define containers until the system context is agreed.

```
C4 LEVEL 1: SYSTEM CONTEXT                    (Phase: Decomposition)
┌─────────────────────────────────────────────────────────────────────┐
│  "What is inside vs. outside the system?"                            │
│   • System boundary defined                                          │
│   • External actors identified (people, external systems)            │
│   • Relationships mapped (who talks to whom, what protocol)          │
└────────────────────────────────────────┬────────────────────────────┘
                                         │ Gate: User confirms boundary
                                         ▼
C4 LEVEL 2: CONTAINERS                        (Phase: Decomposition)
┌─────────────────────────────────────────────────────────────────────┐
│  "What are the big deployable units?"                                │
│   • Applications (APIs, web apps, background workers)                │
│   • Data stores (databases, caches, search indexes)                  │
│   • Message infrastructure (queues, event buses)                     │
│   • Inter-container communication defined                            │
└────────────────────────────────────────┬────────────────────────────┘
                                         │ Gate: User confirms containers
                                         ▼
C4 LEVEL 3: COMPONENTS                        (Phase: Design)
┌─────────────────────────────────────────────────────────────────────┐
│  "What are the modules inside each container?"                       │
│   • Bounded contexts / modules identified                            │
│   • Services / use cases defined                                     │
│   • Key interfaces and dependency rules                              │
│   • Cross-cutting concerns (logging, monitoring, error handling)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why This Order Matters

| Anti-Pattern | What Goes Wrong |
|-------------|-----------------|
| Designing component internals before containers | Module boundaries shift when containers change — rework |
| Choosing technologies before understanding boundaries | Tech choices get locked before constraints are known |
| Detailing security before knowing the system shape | Security design for modules that don't exist yet |
| Jumping to API design before knowing containers | APIs defined for wrong service boundaries |

AI-ADLC's CTO persona enforces this discipline: "Never detail component internals before container boundaries are defined and stable."

---

## The Five Phases and How Decomposition Threads Through

| Phase | C4 Activity | Other Activities |
|-------|-------------|-----------------|
| 🔵 Foundation (Stages 1-3) | — (context loading, no C4 yet) | Requirements ingestion, architecture vision + principles |
| 🟠 Decomposition (Stages 4-5) | **L1 + L2** | System context → Container design |
| 🟡 Decisions (Stages 6-8) | — (decisions, not decomposition) | Tech stack, multi-tenancy, security architecture |
| 🟢 Design (Stages 9-12) | **L3** | Data, API, integration, component design |
| 🚀 Assembly (Stage 13) | Cross-reference check | Package consolidation + integrity audit |

The Decisions phase sits between L2 and L3 because technology and pattern decisions must be made AFTER containers are known but BEFORE internal components are designed.

---

## How Each C4 Level Works in AI-ADLC

### Level 1: System Context (Stage 4)

**Question:** "What is inside vs. outside?"

The AI (as CTO) works with the user to:
1. Define the system boundary — what's "ours" vs. "external"
2. Identify all external actors (users, administrators, operators)
3. Identify all external systems (integrations, SaaS providers, legacy systems)
4. Define relationships — who communicates with whom, what protocol, what data flows
5. Produce a C4 Level 1 diagram (Mermaid)

**Gate:** User confirms the system boundary and external landscape are correct.

**What's locked after this gate:** The external interface is fixed. Adding or removing external systems after this point requires backtracking with justification.

### Level 2: Container Design (Stage 5)

**Question:** "What are the big deployable pieces?"

With the boundary established, the AI decomposes into containers:
1. Identify application containers (APIs, SPAs, workers, BFFs)
2. Identify data stores (RDBMS, caches, search, blob storage)
3. Identify message infrastructure (queues, event buses, topics)
4. Define container responsibilities (single responsibility per container)
5. Map inter-container communication (sync/async, protocol, data format)
6. Produce a C4 Level 2 diagram (Mermaid)

**Gate:** User confirms container decomposition is correct.

**What's locked after this gate:** Container boundaries are stable. Technology choices and internal design build on top of these. Changing a container boundary after this point cascades to everything below.

### Level 3: Component Design (Stage 12)

**Question:** "What's inside each container?"

After Decisions (tech stack, security, data) are made:
1. For each container, decompose into modules/bounded contexts
2. Define services/use cases per module
3. Define key interfaces and dependency rules (what depends on what)
4. Define shared kernel (if applicable)
5. Map cross-cutting concerns (logging, monitoring, tenant context propagation)
6. Produce C4 Level 3 diagram(s)

**Depth adaptation:**
- Minimal: Module list with responsibilities and dependencies
- Standard: Module diagram + interface contracts + dependency rules
- Comprehensive: Detailed internals, sequence diagrams for key flows, DDD tactical patterns

---

## ADR Integration with Decomposition

Architecture Decision Records (ADRs) are produced throughout the workflow when decisions arise. The decomposition phases generate ADRs when:

- Multiple viable container topologies exist (L2)
- Multiple valid module boundaries are possible (L3)
- Technology selection has 2+ genuinely viable options (Decisions phase)
- A future architect would ask "why did we choose this structure?"

ADRs are numbered sequentially (ADR-001, ADR-002, ...) and stored in `{output}/ADR/`.

---

## Extension System (v1.1)

AI-ADLC supports 6 opt-in architectural extensions that enrich decomposition with specialized patterns:

| Extension | Enriches | When Activated |
|-----------|----------|----------------|
| DDD Tactical | L3 (aggregate boundaries, domain events) | When domain complexity justifies tactical patterns |
| Microservices | L2 + L3 (service decomposition, sagas) | When architecture is distributed microservices |
| BFF Pattern | L2 (BFF containers, aggregation rules) | When frontend needs a backend-for-frontend |
| Event Sourcing/CQRS | L3 (event stores, projections, read models) | When state must be event-sourced |
| Resilience Patterns | L2 + L3 (circuit breakers, bulkheads) | When distributed reliability is critical |
| Feature Flags | L3 (flag architecture, rollout strategies) | When progressive rollout is a requirement |

Extensions are opt-in: they activate only when the architecture justifies them. Once active, their rules become blocking constraints — not optional suggestions.

---

## Downstream Impact

AI-ADLC's decomposition output directly shapes AI-DWG's generation:

| AI-ADLC Produces | AI-DWG Derives |
|-------------------|----------------|
| C4 L1 (system context) | `scope-and-risks.md` (boundary context) |
| C4 L2 (containers) | High-level folder structure, `module-structure.md` |
| C4 L3 (components) | Detailed folder structure, `CODEOWNERS`, `domain-context.md` |
| Technology Stack + ADRs | `tech-stack.md`, `.gitignore`, `docker-compose.yml` |
| Security Architecture | `security-rules.md` |
| API Architecture | `api-standards.md` |

The decomposition discipline ensures that by the time AI-DWG generates the workspace, module boundaries are stable and well-defined — not guessed.

---

## Related Documents

| Document | Location |
|----------|----------|
| Core workflow | `ai-adlc/ai-adlc-rules/core-workflow.md` |
| Diagram standards | `ai-adlc/ai-adlc-rule-details/common/diagram-standards.md` |
| Container design stage | `ai-adlc/ai-adlc-rule-details/decomposition/container-design.md` |
| Component design stage | `ai-adlc/ai-adlc-rule-details/design/component-design.md` |
| Extensions README | `ai-adlc/ai-adlc-rule-details/extensions/README.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
