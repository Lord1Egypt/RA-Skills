# AI-DWG — User Guide

**Package:** AI-DWG (AI-Driven Workspace Generator)
**Version:** 1.0.0
**Audience:** Tech Leads, DevOps Engineers, Senior Developers, Architects setting up new projects

---

## What is AI-DWG?

AI-DWG is a one-time generator that composes a complete, ready-to-code development workspace from one or more design-time peer inputs — an Architecture Package (from AI-ADLC), a Product Backlog Package (from AI-POLC), and/or a UX Design Package (from AI-UXD). Any non-empty combination works; none is privileged. It generates steering files, project structure, configurations, and operational documents so developers can start contributing from day one.

**In one sentence:** AI-DWG transforms design-time packages into a governed development workspace — the launchpad where coding begins.

---

## When to Use AI-DWG

| Scenario | AI-DWG helps you... |
|----------|---------------------|
| Architecture is complete, time to set up the workspace | Generate everything developers need to start coding |
| Architecture changed after initial setup | Reconcile workspace without losing team customizations |
| Setting up a monorepo or multi-module project | Generate structure that matches your C4 containers/components |
| Need consistent governance across the workspace | Produce prescriptive steering files (MUST/MUST NOT rules) |
| Onboarding developers to a new project | Day-1 productivity — zero additional setup guidance needed |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Provide inputs** — Have your Architecture Package ready (+ optional PBP and UXP)
3. **Start generation** — Say: *"Using AI-DWG, generate the development workspace from my architecture package"*
4. **Answer 2-3 config questions** — AI-DWG confirms technology stack and workspace preferences
5. **Get your workspace** — A complete, ready-to-code development workspace in one pass

---

## Input Sources

AI-DWG reads structured documents and generates from them. The three inputs are **equal-impact peers** — provide any non-empty combination:

| Input | Source | Required? | What It Contributes |
|-------|--------|:---------:|---------------------|
| Architecture Package (AP) | AI-ADLC | Peer¹ | Tech cluster: system structure, containers, components, tech stack, ADRs, security model, src folder structure |
| Product Backlog Package (PBP) | AI-POLC | Peer¹ | Product cluster: vision document, DoR/DoD, epic structure, sprint governance, scope & risks |
| UX Design Package (UXP) | AI-UXD | Peer¹ | UX cluster: design system + tokens, component specs, UI implementation spec, accessibility baseline |

> ¹ **Peer inputs — at least ONE required.** No single input is mandatory on its own. Each unlocks its own output cluster. When fewer than all three are present, AI-DWG discloses the quality impact (which clusters it cannot produce) and asks you to approve before proceeding. The more inputs you provide, the richer the generated workspace.

---

## Operating Modes

AI-DWG is NOT a lifecycle — it's a generator with two modes:

| Mode | When to Use | What Happens |
|------|-------------|--------------|
| **Full Generation** | First time — no workspace exists yet | One-shot creation of entire workspace from architecture docs |
| **Delta Reconciliation** | Architecture changed after initial generation | Incremental update — adds/modifies only what changed; preserves team customizations |

### Delta Reconciliation Rules

- Detects what changed in the AP since last generation
- Preserves anything marked `<!-- custom -->` (team additions)
- Updates only net-new or changed items
- Never destroys team customizations
- Produces a reconciliation report showing what was added/changed/preserved

---

## What It Generates

| Category | Examples | Count |
|----------|---------|:-----:|
| Steering files (always) | Domain context, tech stack rules, coding standards, API conventions | 19 |
| Steering files (conditional) | Multi-tenancy, DDD patterns, event sourcing, feature flags | Up to 8 |
| Operational documents | README, contributing guide, ADR index, onboarding guide | 6 |
| Planning templates | Sprint template, release checklist, retrospective format | 3 |
| Config files | CI/CD, linting, testing, environment setup | 5 |
| Source structure | Folders matching C4 L3 modules | Per architecture |

### Conditional Generation

AI-DWG only generates files justified by the architecture. No multi-tenancy in the AP? No tenancy steering file. No DDD patterns opted in? No DDD rules. Zero bloat.

---

## Extension Awareness

AI-DWG detects AI-ADLC v1.1 extensions in the AP and generates corresponding workspace rules:

| Extension Detected | Workspace Rules Generated |
|-------------------|--------------------------|
| DDD Tactical | Aggregate boundaries, domain event naming, ACL patterns |
| Microservices | Service isolation, distributed tracing, saga conventions |
| BFF Pattern | BFF routing, client-specific API conventions |
| Event Sourcing + CQRS | Event store patterns, projection rules, command/query separation |
| Resilience Patterns | Circuit breaker config, bulkhead rules, graceful degradation |
| Feature Flags | Flag naming, lifecycle, evaluation order |

No extension detected = no related output generated.

---

## Technology Adaptation

Generated output varies based on your tech stack:

| Stack | Adapted For |
|-------|-------------|
| Node.js / TypeScript | ESLint, Jest/Vitest, npm/pnpm, tsconfig patterns |
| Python | Ruff/Black, pytest, requirements/poetry, type hints |
| .NET / C# | dotnet conventions, xUnit, NuGet, solution structure |
| Java | Maven/Gradle, JUnit, Spring conventions |
| Generic | Language-agnostic rules for unlisted stacks |

---

## The Relationship with Connected Packages

```
AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► Development Workspace ──► AI-GCE + AI-DLC v1
```

> In the sequential flow (POLC→UXD→ADLC→DWG), all three peer inputs are guaranteed present by the time DWG starts. ADLC is the terminal predecessor.

| Direction | What Flows |
|-----------|-----------|
| POLC → DWG | Product Backlog Package (DoR/DoD, governance rules) |
| UXD → DWG | UX Design Package (tokens, component specs, accessibility) |
| ADLC → DWG | Architecture Package (system structure, tech stack, ADRs) |
| DWG → GCE | Development Workspace (for compliance engine derivation) |
| DWG → DLC | Development Workspace (for development lifecycle) |

---

## Session Continuity

AI-DWG is a one-shot generator, not a multi-session lifecycle. However:
- Generation state is tracked in `dwg-state.md`
- Reconciliation mode remembers what was previously generated
- Provenance metadata in every generated file traces back to source AP documents
- You can re-run reconciliation as many times as architecture evolves

---

## What You Get (Output Artifacts)

| Artifact | Purpose |
|----------|---------|
| `dwg-state.md` | Generation state + chain marker |
| `rules/*.md` | Prescriptive rules for the development workspace |
| `src/` or module folders | Source structure matching architecture containers/components |
| `docs/` | Operational documents (README, onboarding, ADR index) |
| Config files | CI/CD, linting, testing, environment configs |
| Planning templates | Sprint, release, and retrospective templates |
| Provenance metadata | Every file traces to its AP source document |

---

## Quick Start Examples

**Full generation (first time):**
```
Using AI-DWG, generate the development workspace from my architecture package.
```

**With all three inputs (richest):**
```
Using AI-DWG, generate the development workspace.
I have an Architecture Package, Product Backlog Package, and UX Design Package.
```

**Delta reconciliation (architecture changed):**
```
Using AI-DWG, reconcile the workspace — the API architecture changed
and we added a new container for notifications.
```

---

## Tips for Best Results

1. **Complete your AP first** — AI-DWG derives from architecture. Incomplete AP = incomplete workspace.
2. **Include PBP and UXP if you have them** — They enrich governance rules and design system integration.
3. **Don't manually edit generated files without `<!-- custom -->`** — Unmarked edits may be overwritten during reconciliation.
4. **Run reconciliation when architecture evolves** — Don't manually patch; let AI-DWG do incremental updates.
5. **Check provenance comments** — Every generated rule cites its source. Use this for traceability.
6. **Review conditional files** — If something was generated that shouldn't be, check if the AP accidentally implies it.

---

## What AI-DWG Is NOT

- NOT a lifecycle — it's a one-shot generator (with reconciliation for updates)
- NOT architecture design (that's AI-ADLC)
- NOT code generation (that's AI-DLC v1)
- NOT compliance enforcement (that's AI-GCE — which reads DWG's output)
- NOT product backlog management (that's AI-POLC)
- NOT a build tool or CI/CD system

AI-DWG is the **Workspace Builder** — it answers *"Given this architecture, what should the development workspace look like?"*

---

## Platform Support

AI-DWG works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-DWG v1.0.0 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*
