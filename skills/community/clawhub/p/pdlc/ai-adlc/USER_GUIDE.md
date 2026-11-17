# AI-ADLC — User Guide

**Package:** AI-ADLC (AI-Driven Architecture Design Life Cycle)
**Version:** 1.1.0
**Audience:** Architects, Tech Leads, CTOs, Senior Engineers, Development Managers

---

## What is AI-ADLC?

AI-ADLC is an injectable workflow that guides you through the complete process of designing a solution architecture — from project requirements to a professional, development-ready Architecture Package (AP). It reasons and writes as an experienced CTO/Chief Architect, following C4 progressive decomposition and producing ADR-driven decisions at every stage.

**In one sentence:** AI-ADLC turns requirements into a governed Architecture Package — the blueprint that drives everything built downstream.

---

## When to Use AI-ADLC

| Scenario | AI-ADLC helps you... |
|----------|---------------------|
| Starting architecture for a new system | Design from system context down to components (C4 L1→L3) |
| Have a PIP from AI-PILC | Convert project initiation into architecture decisions |
| Need technology selection with rationale | Produce ADRs with alternatives analysis |
| Designing security, data, or API architecture | Structured stages for each concern |
| Extending an existing system (brownfield) | Architecture with existing system integration as first-class |
| Complex patterns needed (DDD, microservices, etc.) | Opt-in extensions for advanced patterns |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"Using AI-ADLC, design the architecture for this system"*
3. **Provide your source** — A PIP, PRD, requirements doc, or verbal description
4. **Approve at gates** — Every stage produces deliverables that require your sign-off
5. **Get your AP** — A complete Architecture Package ready for AI-DWG or manual development

---

## Input Modes

AI-ADLC detects what you already have and adapts:

| What You Have | Mode | Behavior |
|---------------|------|----------|
| AI-PILC output (PIP) | Chain — full context | Reads pilc-state.md; extracts scope, constraints, stakeholders, risks. Minimal questions. |
| Raw PRD / requirements doc | Standard | Full ingestion + clarification before design begins |
| Verbal description | Conversational | Extended questioning to establish constraints and scope |
| Existing architecture (brownfield) | Extension | Designs with existing system integration as a constraint |
| None (exploratory) | Discovery | Guides you to articulate requirements before designing |

You do NOT need AI-PILC first. AI-ADLC works standalone — upstream enriches, absence doesn't block.

---

## The Workflow (5 Phases, 13 Stages)

### Phase 1: Foundation (Stages 1–3)

Load context, assess complexity, define vision and principles.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Workspace Detection | Detects upstream state files, determines mode + depth | Confirm mode (chain/standalone/brownfield) |
| 2 — Requirements Ingestion | Reads and structures input; identifies constraints | Confirm requirements are captured |
| 3 — Architecture Vision | Defines principles, quality attributes, architectural goals | Approve the architecture vision |

### Phase 2: Decomposition (Stages 4–5)

Define system boundaries and containers (C4 Level 1 + Level 2).

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 4 — System Context (C4 L1) | Maps system boundary, actors, external systems | Approve system context diagram |
| 5 — Container Design (C4 L2) | Defines containers (services, databases, queues, etc.) | Approve container architecture |

### Phase 3: Decisions (Stages 6–8)

Select technology, isolation patterns, security model.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 6 — Technology Stack | Evaluates options; produces ADRs for selections | Approve technology choices |
| 7 — Multi-Tenancy | Designs isolation model (if applicable) | Approve tenancy pattern |
| 8 — Security & Identity | Auth, authorization, encryption, trust boundaries | Approve security architecture |

### Phase 4: Design (Stages 9–12)

Detail data, API, integrations, infrastructure, and components (C4 Level 3).

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 9 — Data Architecture | Schema strategy, persistence patterns, migration approach | Approve data design |
| 10 — API Architecture | Contracts, versioning, rate limiting, documentation | Approve API design |
| 11 — Integration & Infrastructure | External integrations, deployment topology, observability | Approve integration/infra design |
| 12 — Component Design (C4 L3) | Internal component decomposition per container | Approve component-level design |

### Phase 5: Assembly (Stage 13)

Consolidate, cross-check, and produce final package.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 13 — Package Assembly | Cross-references all artifacts; produces AP README | Final approval — AP ready for downstream |

---

## Extensions (v1.1)

Extensions add advanced architectural patterns. They activate during the workflow when your system needs them. Once activated, extension rules become blocking constraints.

| Extension | Pattern | When Needed |
|-----------|---------|-------------|
| DDD Tactical | Aggregates, domain events, ACLs, bounded contexts | Complex domain logic |
| Microservices | Service mesh, distributed tracing, saga patterns | Distributed service architecture |
| BFF Pattern | Backend-for-Frontend | Multiple client types needing different API shapes |
| Event Sourcing + CQRS | Full event log, temporal queries, projections | Complete audit trail, event-driven state |
| Resilience Patterns | Circuit breaker, bulkhead, graceful degradation | High-availability requirements |
| Feature Flags | Controlled rollout, A/B testing, kill switches | Progressive delivery needs |

Say the pattern name during a session to activate: *"We'll need DDD tactical patterns for the domain layer"*

---

## The Relationship with AI-DWG

AI-ADLC's output (AP) is the primary input for AI-DWG:

```
AI-ADLC ──(Architecture Package)──► AI-DWG
                                     Generate the development workspace
```

AI-DWG reads the AP and generates a complete workspace — steering files, folder structure, configurations — all traced back to architecture decisions. The richer and more complete the AP, the more AI-DWG can derive automatically.

AI-ADLC also feeds AI-POLC (product ownership benefits from architecture constraints awareness) and AI-UXD (component boundaries inform UX component mapping).

---

## Adaptive Depth

AI-ADLC auto-calibrates based on system complexity:

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Simple system, few containers, clear technology | Streamlined AP — vision + context + containers + key ADRs |
| **Standard** | Typical complexity, multiple containers, some integration | Full AP with all stages and core ADRs |
| **Comprehensive** | Enterprise, multi-tenant, distributed, heavy compliance | All extensions suggested, detailed ADRs for every decision, full C4 L3 |

Override anytime: *"Change depth to Comprehensive"*

---

## Session Continuity

AI-ADLC saves progress in `adlc-state.md`. You can:
- Close your session at any time
- Resume later — AI-ADLC reads state and picks up where you left off
- Activate extensions mid-workflow
- Switch depth mid-workflow
- Skip conditional stages (e.g., multi-tenancy if not applicable)

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `adlc-state.md` | State tracking + chain marker |
| `architecture-vision.md` | Principles, quality attributes, goals |
| `system-context.md` | C4 Level 1 — boundary + actors |
| `container-diagram.md` | C4 Level 2 — containers + communication |
| `technology-stack.md` | Stack selection with ADR references |
| `multi-tenancy.md` | Isolation model (if applicable) |
| `security-architecture.md` | Auth, encryption, trust boundaries |
| `data-architecture.md` | Schema strategy, persistence |
| `api-architecture.md` | Contracts, versioning, documentation |
| `integration-architecture.md` | External systems + infrastructure |
| `component-design.md` | C4 Level 3 — per-container internals |
| `ADR-NNN.md` (multiple) | Architecture Decision Records |
| `architecture-workbook.md` | Cross-cutting concerns summary |
| `AP_README.md` | Package index + reading guide |

---

## Quick Start Examples

**From a PIP (richest context):**
```
Using AI-ADLC, design the architecture for this system.
I have a Project Initiation Package from AI-PILC.
```

**From a requirements document:**
```
Using AI-ADLC, design the architecture based on this PRD:
[paste or reference your requirements document]
```

**Brownfield (extending existing system):**
```
Using AI-ADLC, design architecture for a new module in our existing system.
Here are the current architecture constraints: [describe existing system]
```

---

## Tips for Best Results

1. **State constraints early** — Budget, team skills, timeline, existing infrastructure. AI-ADLC never recommends outside boundaries.
2. **Don't skip C4 progression** — L1 before L2 before L3. Boundaries must be stable before internals are detailed.
3. **Use ADRs actively** — Every major decision gets one. They're your architectural memory.
4. **Activate extensions only when needed** — Don't add DDD for a CRUD app. Extensions add rigor but also overhead.
5. **Approve at gates** — AI-ADLC won't auto-progress. Your sign-off ensures alignment.
6. **Feed the richest source** — A full PIP produces better architecture than a verbal sketch.

---

## What AI-ADLC Is NOT

- NOT project initiation (that's AI-PILC)
- NOT workspace/code generation (that's AI-DWG)
- NOT product backlog management (that's AI-POLC)
- NOT UX design (that's AI-UXD)
- NOT compliance enforcement (that's AI-GCE)
- NOT code implementation (that's AI-DLC v1)

AI-ADLC is the **Architect's companion** — it answers *"How should this system be structured, and why?"*

---

## Platform Support

AI-ADLC works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-ADLC v1.1.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*
