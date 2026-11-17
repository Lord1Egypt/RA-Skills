<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Architecture Reading

## Stage: 2 of 12
## Phase: 🔵 STRATEGY
## Execution: ALWAYS

---

## Purpose

Read the Architecture Package (AP) and any other available sources to produce an **Architecture Commitment Inventory** — every testable promise the architecture makes. This inventory becomes the foundation for deriving test requirements in Stage 3.

If no AP exists (Brownfield or Observation Only mode), this stage scans alternative sources (codebase structure, existing documentation) to build a best-effort inventory.

---

## Depth Adaptation

| Depth | Reading Scope | Inventory Detail |
|-------|--------------|-----------------|
| **Minimal** | Core AP artifacts only: API contracts, component designs, major ADRs. Skip detailed NFRs and integration maps if time-constrained. | Commitment ID + type + brief description |
| **Standard** | Full AP reading: all contracts, all component designs, all ADRs, integration maps, data models, NFR commitments. | Commitment ID + type + description + source artifact + linked components |
| **Comprehensive** | Full AP + DW steering files + aidlc-docs requirements + user stories. Cross-reference all sources. | All Standard fields + acceptance criteria links + cross-reference matrix + dependency mapping |

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Read architecture documents as a stakeholder asking "what did we promise?" — not as an implementer
- Extract commitments systematically: every API endpoint is a contract, every ADR is a decision that must hold, every NFR is a measurable promise
- Organize findings by domain area (not by document location) to prepare for test derivation
- Flag ambiguities: if the AP says "high performance" without a number, that's untestable — note it

### Anti-Patterns for This Stage
- Do NOT read selectively based on what YOU think matters — read everything and let the taxonomy determine relevance
- Do NOT invent commitments not present in the AP — derive from what exists, flag what's missing
- Do NOT skip the inventory presentation — the user must confirm "yes, this is what we designed"

### Quality Check
A good output at this stage sounds like:
- "I've read 3 API contracts (14 endpoints total), 4 component designs (UserService, OrderService, PaymentService, NotificationService), 2 security ADRs (JWT auth, RBAC), 1 integration map (3 external systems), and 2 NFR commitments (p95 ≤ 200ms, 99.9% uptime). Total: 47 testable commitments across 6 categories."

---

## Step-by-Step Execution

### Step 1: Load Available Sources

Based on mode detected in Stage 1:

| Mode | Sources to Read | Priority Order |
|------|----------------|---------------|
| **Full Chain** | AP + DW steering + aidlc-docs requirements | AP first → DW enrichment → aidlc-docs stories |
| **Architecture Only** | AP only | Read all AP artifacts systematically |
| **Brownfield** | Codebase structure + any available docs | Source directories → existing tests → any architecture docs |
| **Observation Only** | aidlc-docs + DW steering | User stories → functional designs → tech stack |

---

### Step 2: Read Architecture Package (If Available)

For each AP artifact type, extract testable commitments:

| AP Artifact | What to Extract | Commitment Type |
|-------------|----------------|----------------|
| **API Contracts** | Every endpoint: method, path, request schema, response schema, status codes, auth requirements | API commitment |
| **Component Designs** | Business rules, state machines, algorithms, validation logic, dependencies | Business logic commitment |
| **Security ADRs** | Auth mechanisms, authorization model, data protection decisions, encryption choices | Security commitment |
| **Integration Maps** | External systems, communication protocols, error handling strategies, SLAs | Integration commitment |
| **Data Models** | Entities, relationships, constraints, migration strategies, consistency requirements | Data commitment |
| **NFR Commitments** | Performance targets (latency, throughput), reliability targets (uptime, recovery), scalability targets | Performance/Quality commitment |
| **User Stories** (if in AP scope) | Acceptance criteria, scenarios, business workflows | Workflow commitment |

**For each commitment, record:**
```markdown
| Commitment ID | Type | Description | Source Artifact | Components Involved |
```

**Commitment ID format:** `{CATEGORY}-{NNN}`
- API-001, API-002... (API endpoints)
- SEC-001, SEC-002... (Security decisions)
- BL-001, BL-002... (Business logic rules)
- INT-001, INT-002... (External integrations)
- DATA-001, DATA-002... (Data model promises)
- PERF-001, PERF-002... (Performance/NFR targets)
- WF-001, WF-002... (Workflow/user journey promises)
- CFG-001, CFG-002... (Configuration contracts)

---

### Step 3: Read Development Workspace (If Available)

Extract testing-relevant context from DW steering files:

| Steering File | What to Extract |
|---------------|----------------|
| `tech-stack.md` | Testing frameworks configured (Jest, Pytest, etc.), test runner, coverage tools |
| `testing-strategy.md` | Existing test approach, coverage goals, automation decisions |
| `module-structure.md` | Module boundaries (defines integration test scope) |
| `coding-standards.md` | Error handling conventions, logging patterns (affects test expectations) |
| `workspace-rules.md` | Project type, team structure, methodology |

**This context enriches** — it tells AI-TGE what testing tools are available and what conventions the team follows. It does NOT generate new commitments.

---

### Step 4: Read Existing Codebase (Brownfield Mode Only)

If in Brownfield mode (no AP), scan the codebase to infer commitments:

| Code Pattern | Inferred Commitment Type |
|-------------|-------------------------|
| Route definitions (Express, FastAPI, etc.) | API commitment (endpoint exists) |
| Middleware with auth checks | Security commitment (auth flow exists) |
| ORM models / schema definitions | Data commitment (entity exists) |
| HTTP/gRPC client calls to external URLs | Integration commitment (external dependency) |
| Complex conditionals / algorithms | Business logic commitment |
| Environment variable reads / config loaders | Configuration commitment |
| Multi-step handler functions | Workflow commitment |

**Important:** Brownfield inferred commitments are marked `Source: Inferred (codebase scan)` — they are hypotheses, not documented promises. The user must confirm them.

---

### Step 5: Compile Architecture Commitment Inventory

Organize all extracted commitments by category:

```markdown
## Architecture Commitment Inventory

**Project:** {project_name}
**Mode:** {Full Chain / Architecture Only / Brownfield / Observation Only}
**Sources Read:** {list of artifact types scanned}
**Total Commitments:** {N}

### Summary by Category

| Category | Count | Source | Key Commitments |
|----------|:-----:|--------|-----------------|
| API | {n} | {AP / Inferred} | {top 2-3 endpoints by importance} |
| Security | {n} | {AP / Inferred} | {auth mechanism, authorization model} |
| Business Logic | {n} | {AP / Inferred} | {key rules identified} |
| Integration | {n} | {AP / Inferred} | {external systems listed} |
| Data | {n} | {AP / Inferred} | {key entities} |
| Performance/NFR | {n} | {AP / Inferred} | {SLA targets} |
| Workflows | {n} | {AP / Inferred} | {key user flows} |
| Configuration | {n} | {AP / Inferred} | {config items with contracts} |

### Full Inventory

| ID | Category | Description | Source Artifact | Components |
|:--:|:--------:|-------------|----------------|-----------|
| API-001 | API | POST /users — create user with email validation | api-contract.md | UserService |
| ... | ... | ... | ... | ... |
```

---

### Step 6: Identify Gaps and Ambiguities

Flag concerns for user attention:

| Gap Type | Example | Action |
|----------|---------|--------|
| **Untestable commitment** | "System should be fast" (no number) | Flag: "NFR has no measurable target — cannot derive test threshold" |
| **Missing coverage area** | AP has no error handling documentation | Flag: "No error handling architecture documented — baseline rules will cover" |
| **Contradictions** | API contract says auth required; component design shows no auth middleware | Flag: "Inconsistency detected — which is correct?" |
| **Partial documentation** | Integration map lists system but no error handling strategy | Flag: "Integration with {system} documented but failure mode not specified" |

---

### Step 7: Present for Review

```markdown
## Review: Architecture Commitment Inventory

I've read your architecture sources and identified the following testable commitments:

**Total commitments:** {N} across {n} categories
**Source quality:** {High — well-documented AP / Medium — partial documentation / Low — mostly inferred}

**Summary:**
- API commitments: {n} (across {n} endpoints)
- Security commitments: {n}
- Business logic: {n}
- Integrations: {n} external systems
- Data model: {n} entities
- Performance/NFR: {n} measurable targets
- Workflows: {n} user journeys
- Configuration: {n} config contracts

**Gaps flagged:** {n} items needing clarification

**Full inventory saved to:** `.governance/test/architecture-commitments.md` (working document — not final output)

---

**Your response:**
- (a) **Approve** — this accurately represents what was designed; proceed to derive tests
- (b) **Add commitments** — there are architectural promises not captured here
- (c) **Remove items** — some of these are not architectural commitments (e.g., deprecated)
- (d) **Clarify gaps** — let me address the flagged ambiguities
```

---

## Gate

**This stage has a GATE.** Do not proceed to Stage 3 until the user confirms the Architecture Commitment Inventory represents what was designed. The inventory is the foundation for all test derivation — errors here propagate through the entire register.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Architecture Commitment Inventory | `.governance/test/architecture-commitments.md` | Working document — input for Stage 3 derivation |
| Updated state file | `.governance/test/tge-state.md` | Stage 2 complete; commitment count recorded |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| All available sources read | Every detected input from Stage 1 has been scanned |
| Commitments extracted | At least 1 commitment per available category |
| Commitment IDs assigned | Every entry has a unique `{CATEGORY}-{NNN}` ID |
| Source traceability | Every commitment links back to the artifact it was derived from |
| Gaps documented | Ambiguities and untestable items flagged |
| User approved | Inventory confirmed as accurate representation of architecture |
| State file updated | Stage 2 = complete; commitment count in stats |
