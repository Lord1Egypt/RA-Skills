# How to Design Architecture

**Purpose:** Practical guide for using AI-ADLC to transform project requirements into a complete, development-ready Architecture Package (AP) — the structural blueprint that AI-DWG uses to generate your workspace.

---

## Who This Is For

Technical leads, solution architects, or senior developers who need to design a system's architecture before implementation begins. You want C4-level decomposition, formal ADRs, API contracts, and security architecture — produced through guided conversation rather than blank-page struggle.

---

## Before You Start

**You need:**
- AI-ADLC installed in your AI workspace (see `ai-adlc/setup/INSTALL.md`)
- Input — ANY of the following:
  - A PIP from AI-PILC (ideal — richest context)
  - A requirements document + project charter
  - A verbal description of what you're building
  - An existing architecture you're extending (brownfield)

**You do NOT need:**
- Prior architecture documents
- Technology decisions already made
- A complete understanding of all components (that's what ADLC helps you discover)

---

## The Process (13 Stages, 5 Phases)

### Phase 1: Foundation — "What's the context?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 1. Workspace Setup | Detect predecessor output, set depth, create workspace | Confirm output location and depth level |
| 2. Requirements Ingestion | Read PIP or raw input, extract architectural drivers | Validate that key requirements are captured |
| 3. Architecture Vision | Define high-level system purpose, key quality attributes, architectural principles | Approve vision statement and guiding principles |

**Gate:** Vision approved → decomposition can begin.

### Phase 2: Decomposition — "What are the pieces?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 4. System Context (C4 L1) | Define system boundaries, external actors, integrations | Confirm what's inside vs. outside the system |
| 5. Container Design (C4 L2) | Identify major deployable units, their responsibilities, communication | Approve container boundaries and API surfaces |

**Gate:** L2 boundaries stable → decisions and detailed design proceed.

### Phase 3: Decisions — "What technology and patterns?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 6. Technology Stack | Evaluate and select technologies (framework, language, DB, messaging) | Choose from options with trade-off analysis |
| 7. Multi-Tenancy Model | Define isolation strategy (if applicable) | Choose tenant isolation pattern |
| 8. Security & Identity | Design auth model, data protection, trust boundaries | Approve security architecture |

**Gate:** Major technology and security decisions locked → design proceeds.

### Phase 4: Design — "How do the internals work?"

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 9. Data Architecture | Design data model, storage strategy, consistency patterns | Approve data model and persistence choices |
| 10. API Architecture | Define contracts, versioning, error handling standards | Approve API contracts |
| 11. Integration Design | Map all integration points, data flows, failure modes | Confirm integration landscape |
| 12. Component Design (C4 L3) | Define internal building blocks within each container | Approve component responsibilities and interfaces |

**Gate:** All designs reviewed → ready for assembly.

### Phase 5: Assembly — "Package it all together."

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| 13. Architecture Package | Consolidate all artifacts into the final AP | Final review and approval |

---

## Extensions (Opt-In Advanced Patterns)

At Stage 4 (or whenever architecture justifies it), you can activate extensions:

| Extension | Activate When | What It Adds |
|-----------|--------------|-------------|
| **DDD Tactical** | Complex domain logic, multiple bounded contexts | Aggregate design, domain events, repository patterns |
| **Microservices** | ≥3 independently deployable services | Service mesh, discovery, distributed tracing |
| **BFF Pattern** | Multiple frontend channels (web, mobile, partner) | Backend-for-frontend design, API gateway routing |
| **Event Sourcing / CQRS** | Audit-critical or temporal data requirements | Event stores, projections, command/query separation |
| **Resilience Patterns** | ≥3 external integrations or high-availability needs | Circuit breakers, bulkheads, retry policies, fallbacks |
| **Feature Flags** | Gradual rollout, A/B testing, trunk-based delivery | Flag taxonomy, evaluation strategy, lifecycle rules |

Extensions are additive — once activated, their rules become blocking constraints at relevant stages. Multiple extensions compose without conflict.

---

## Choosing Your Depth Level

| Depth | Best For | Stages Active | ADR Detail |
|-------|----------|:-------------:|-----------|
| **Minimal** | Small services, proof-of-concepts | Stages 1-5 + 13 (skip detailed design) | Lightweight: decision + rationale only |
| **Standard** | Most projects — recommended | All 13 stages | Full: context, options, consequences |
| **Comprehensive** | Enterprise systems, regulated environments | All 13 + deep extension analysis | Extended: risk analysis, migration paths, sunset criteria |

---

## What You Get (The Architecture Package)

```
{your-output-folder}/
├── adlc-state.md                      ← Marker file (chain handoff + session resume)
├── 01_Architecture_Vision.md          ← Principles, quality attributes, constraints
├── 02_System_Context.md               ← C4 L1 + external actors + integrations
├── 03_Container_Architecture.md       ← C4 L2 + responsibilities + communication
├── 04_Technology_Stack.md             ← Selected technologies with rationale
├── 05_Security_Architecture.md        ← Auth model, trust boundaries, data protection
├── 06_Data_Architecture.md            ← Data model, storage, consistency
├── 07_API_Architecture.md             ← Contracts, versioning, error standards
├── 08_Integration_Architecture.md     ← Integration points, data flows, failures
├── 09_Component_Architecture.md       ← C4 L3 per container
├── 10_Multi_Tenancy.md                ← Isolation strategy (if applicable)
├── 11_Architecture_Decisions/         ← ADR folder
│   ├── ADR-001_Framework_Selection.md
│   ├── ADR-002_Database_Strategy.md
│   └── ...
├── architecture_workbook.md           ← Open questions, assumptions, constraints
└── management_framework/              ← Governance registers
    ├── Decision_Register.md
    ├── Change_Register.md
    ├── Issue_Register.md
    └── Lessons_Learned.md
```

---

## Tips for Better Architecture Sessions

1. **State constraints early.** "We must use AWS." "Budget is $X/month." "Team knows Java, not Go." Constraints narrow the solution space productively — they're not limitations, they're design inputs.

2. **Challenge the first option.** AI-ADLC presents technology options with trade-offs. Don't accept the first suggestion — ask "what's the alternative?" The ADR process is designed for comparing options.

3. **Don't skip L1 for L3.** Progressive decomposition exists because component decisions depend on container boundaries, which depend on system context. Jumping to implementation details before boundaries are stable creates rework.

4. **Use extensions wisely.** "We might need microservices" isn't a reason to activate the extension. Activate when architecture REQUIRES the pattern — not when it might be nice. Each extension adds constraints.

5. **Brownfield is different.** If you're extending an existing system, say so at Stage 2. AI-ADLC will focus on the delta — new components, changed integrations, extension points — not redesigning what already works.

---

## What Happens Next

Your AP feeds downstream packages:

| Next Package | What It Reads from AP |
|-------------|---------------------|
| **AI-DWG** | All architecture artifacts → generates workspace structure, steering files, governance templates |
| **AI-GCE** | (via AI-DWG's steering files) architectural constraints → derives enforcement rules |
| **AI-POLC** | Architecture boundaries → informs story decomposition and technical dependencies |

The handoff is automatic — AI-DWG detects `adlc-state.md` and reads the AP.

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
