<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Requirements Ingestion

## Stage: 2 of 13
## Phase: 🔵 FOUNDATION
## Execution: ALWAYS (Adaptive — behavior depends on input mode)

---

## Purpose

Extract everything architecturally relevant from the available input — regardless of format. Produce an **Architecture Requirements Summary** that captures the drivers, constraints, quality attributes, scale targets, and integration landscape that will shape all design decisions.

This stage does NOT produce an architecture. It produces the INPUT to architecture.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Extract architecturally relevant elements from ANY input format — decompose before synthesizing
- Separate concerns: drivers vs. constraints vs. quality attributes vs. assumptions vs. unknowns
- Probe for what's architecturally significant but unstated — scale expectations, regulatory context, integration landscape
- Trace every extraction back to a source line or flag it as inferred (assumption)

### Anti-Patterns for This Stage
- Do NOT start designing solutions — this stage produces INPUT to architecture, not architecture itself
- Do NOT skip extraction categories because the source is silent — silence is a gap, not absence of need

### Quality Check
A good output at this stage sounds like:
- "6 architectural drivers extracted (3 explicit, 3 inferred — flagged as assumptions); 4 hard constraints identified; 8 quality attributes prioritized; 5 gaps flagged for probing..."

---

## Depth Adaptation

| Depth | Ingestion Behavior |
|-------|-------------------|
| **Minimal** | Extract key drivers only (top 3-5). Minimal gap-filling questions (3-5 max). Brief Architecture Requirements Summary. Skip detailed domain decomposition. |
| **Standard** | Full extraction framework (all 6 categories). Up to 10 gap-filling questions. Complete Architecture Requirements Summary with complexity scoring. |
| **Comprehensive** | Deep extraction with follow-up probing per domain. Multiple question rounds. Detailed domain analysis with architecture significance flags. Formal complexity scoring with factor-by-factor breakdown. |

---

## Adaptive Behavior

| Input Mode | Behavior | Effort |
|-----------|----------|--------|
| **PIP (AI-PILC output)** | Load and synthesize from structured artifacts. Minimal questions. | Low — mostly extraction |
| **Requirements Document** | Analyze PRD/spec for architecture-relevant content. Some questions. | Medium — extraction + gap-filling |
| **Verbal Description** | Interview the user with structured questions. | High — full elicitation |
| **Brownfield (existing architecture)** | Load existing docs; identify what's changing; focus on deltas. | Variable — depends on change scope |

---

## Step-by-Step Execution

### Step 1: Load Input Based on Mode

#### Mode A: PIP (Project Initiation Package)

Load and extract from these PIP artifacts:

| PIP Artifact | What to Extract for Architecture |
|-------------|----------------------------------|
| **Requirement Intake Form** | Functional requirements (feature list), NFRs, constraints, scale estimates |
| **Project Charter** | Objectives (measurable), scope boundaries (in/out), constraints, approach |
| **Scope Statement** | Detailed in-scope items, WBS structure, deliverables, acceptance criteria |
| **Feasibility Assessment** | Technical feasibility score + comments (signals about tech risk) |
| **Risk Register** | Technical risks (R-xxx with category=Technical) |
| **Resource Plan** | Team size and skills (informs technology choices) |
| **Stakeholder Register** | Technical stakeholders (Tech Lead, Security Lead, Infra Lead) |

**After loading, confirm with user:**

```markdown
### PIP Loaded — Architecture Context Extracted

From the Project Initiation Package, I've extracted:
- **Functional scope:** {n} capabilities across {m} domains
- **NFRs:** {n} non-functional requirements
- **Constraints:** {n} hard constraints
- **Scale targets:** {summary — users, tenants, transactions}
- **Technical risks:** {n} identified
- **Team context:** {size} FTE, {key skills noted}

**Key architecture drivers I identified:**
1. {Driver 1 — e.g., "Multi-tenant isolation is critical"}
2. {Driver 2 — e.g., "On-premises only — no cloud services"}
3. {Driver 3 — e.g., "API-first with full UI/API parity"}

Is this complete, or are there additional architecture-relevant inputs I should know about?
```

#### Mode B: Requirements Document (PRD/Spec)

1. Read the document fully
2. Extract architecture-relevant content using the extraction framework (Step 2)
3. Identify gaps — what's missing that architecture needs
4. Ask targeted questions to fill gaps (Step 3)

#### Mode C: Verbal Description

1. Present structured interview questions (Step 3 — full set)
2. Synthesize responses into the Architecture Requirements Summary format
3. Confirm with user
4. Save to `{output_root}/__input/architecture_brief.md`

#### Mode D: Brownfield (Existing Architecture)

1. Load existing architecture documents
2. Ask: "What is changing? What's the new requirement or problem?"
3. Identify which stages need full re-execution vs. update-only
4. Focus ingestion on the DELTA — new requirements or changed constraints
5. Note in state: "Brownfield — extending existing architecture"

#### Peer Input: AI-UXD (UXP) — if `uxd-state.md` present (any mode)

AI-UXD is a same-layer peer (both Project layer). When a UXP is detected (Stage 1 peer scan), extract its **UX→Architecture feed** — the UX decisions that become real technical drivers and constraints. This is additive on top of whichever mode (A–D) is active:

| UXP element | Extract as | Becomes |
|-------------|-----------|---------|
| User flows / interaction complexity | Interaction & latency drivers | Architecture driver (responsiveness, real-time/SSE/WebSocket needs) |
| Client / platform / device needs (web, mobile, offline, real-time) | Frontend/client constraints | Container & BFF drivers (C4 L2), API shaping |
| Screen inventory / data-on-screen volume | Read/aggregation patterns | Data & API architecture drivers |
| **Accessibility target (WCAG level)** | **Quality attribute** | **NFR (Accessibility row in 2b) + UI framework selection constraint** |
| Design system / component framework (if chosen) | Frontend tech signal | Cross-check with Technology Stack (flag conflict, don't auto-resolve) |

Feed these into the **Key Architecture Drivers** (Step 5 §8) and the relevant extraction tables. **Standalone-safe:** if `uxd-state.md` is absent, skip this block entirely — architecture proceeds from PIP/document/verbal as today.

**Reconciliation re-entry (UXD often completes after ADLC).** If the AP already exists and `uxd-state.md` later appears or its UX-relevant content changes, offer a **non-destructive** review: surface which drivers/NFRs the new UX content affects (especially the accessibility NFR and any client/real-time interaction needs) and propose targeted updates — never auto-rewrite the AP. Track the last-seen UXP state so a change is detectable (reuse the brownfield/reconciliation pattern,).

---

### Step 2: Architecture Requirements Extraction Framework

For ANY input source, extract into these categories:

#### 2a: Functional Scope (What the system does)

```markdown
### Functional Domains

| # | Domain | Key Capabilities | Architecture Significance |
|---|--------|-----------------|--------------------------|
| 1 | {domain name} | {bullet list of capabilities} | {Why this matters for architecture — e.g., "complex workflow", "real-time", "heavy integration"} |
```

**Architecture significance flags:**
- Real-time requirements → WebSocket/SSE architecture needed
- Complex workflows → Workflow engine consideration
- Heavy integrations → Integration layer design needed
- Large data volumes → Search/indexing strategy needed
- Multi-tenant → Isolation architecture critical
- AI/ML → Async processing pipeline needed
- Reporting → Analytics/aggregation strategy needed

#### 2b: Non-Functional Requirements (Architecture Qualities)

```markdown
### Quality Attributes

| Quality | Requirement | Target | Architecture Impact |
|---------|------------|--------|---------------------|
| Performance | {statement} | {metric — e.g., "p95 < 500ms"} | {What this demands — caching, query optimization, etc.} |
| Scalability | {statement} | {target — e.g., "50 tenants, 100K users"} | {Horizontal scaling, connection pooling, etc.} |
| Availability | {statement} | {target — e.g., "99.9%"} | {HA design, redundancy, failover} |
| Security | {statement} | {standard — e.g., "OWASP Top 10, AES-256"} | {Security layers, encryption, audit} |
| Accessibility | {statement} | {standard — e.g., "WCAG 2.1 AA"} | {UI framework selection constraint} |
```

#### 2c: Constraints (Hard Boundaries)

```markdown
### Architectural Constraints

| # | Constraint | Source | Architecture Impact |
|---|-----------|--------|---------------------|
| 1 | {constraint — e.g., "On-premises only"} | {where this comes from} | {What this eliminates from design space} |
```

**Common constraint categories:**
- Deployment model (cloud, on-prem, hybrid, air-gapped)
- Technology restrictions (open-source only, specific language mandate, no-X)
- Compliance/regulatory (GDPR, HIPAA, data residency)
- Budget/licensing (no commercial licenses, cost ceiling)
- Team skills (must use tech team already knows)
- Timeline (MVP by X date — constrains scope of architecture)
- Integration mandates (must integrate with system X)

#### 2d: Scale Targets

```markdown
### Scale Parameters

| Dimension | Target (v1) | Growth Expectation | Architecture Implication |
|-----------|:----------:|:------------------:|--------------------------|
| Users (concurrent) | {n} | {growth rate} | {Connection handling, session management} |
| Tenants/Organizations | {n} | {growth rate} | {Isolation model, provisioning} |
| Data volume | {size} | {growth rate} | {Storage strategy, archival, indexing} |
| API requests/sec | {n} | {growth rate} | {Rate limiting, caching, horizontal scaling} |
| Transactions/day | {n} | {growth rate} | {Database capacity, queue throughput} |
```

#### 2e: Integration Landscape

```markdown
### External Systems

| # | System | Direction | Protocol | Data Exchanged | Criticality |
|---|--------|:---------:|----------|----------------|:-----------:|
| 1 | {system name} | {In/Out/Both} | {REST/LDAP/SMTP/etc.} | {What flows} | {Critical/Important/Nice-to-have} |
```

#### 2f: Team Context

```markdown
### Development Team Profile

| Factor | Value | Architecture Implication |
|--------|-------|--------------------------|
| Team size | {n} FTE | {Monolith vs. microservices decision influence} |
| Primary language skills | {languages} | {Technology stack constraint} |
| Experience level | {Junior/Mid/Senior mix} | {Framework complexity tolerance} |
| DevOps maturity | {Low/Medium/High} | {Deployment complexity tolerance} |
| Domain expertise | {Low/Medium/High} | {How much guidance the architecture needs to encode} |
```

---

### Step 3: Gap-Filling Questions

If extraction reveals gaps, ask targeted questions. Group by priority:

#### Critical (Block Architecture)

```markdown
### Q-FND-01: Deployment Model

**Context:** Architecture fundamentally differs between cloud-native, on-premises, and hybrid. I need to know where this runs.

**Options:**
- (a) **Cloud (managed services)** — AWS/Azure/GCP managed offerings (RDS, SQS, S3, etc.)
- (b) **On-premises (self-hosted)** — All infrastructure in your data center; no cloud dependency
- (c) **Hybrid** — Core on-prem; some cloud services for specific needs (CDN, email, etc.)
- (d) **Cloud-agnostic containers** — Containerized; runs anywhere (cloud or on-prem)

**Why this matters:** This single decision eliminates or enables 50%+ of technology options.

**Your Decision:** _[awaiting input]_
```

```markdown
### Q-FND-02: Multi-Tenancy Requirement

**Context:** Does this system serve multiple customers/organizations from a single deployment?

**Options:**
- (a) **Multi-tenant** — One deployment serves many isolated customers
- (b) **Single-tenant** — One deployment per customer
- (c) **Multi-org within one customer** — Departments/teams with separation but shared ownership
- (d) **No isolation needed** — Single user group

**Why this matters:** Multi-tenancy is a foundational architectural pattern that affects every layer.

**Your Decision:** _[awaiting input]_
```

```markdown
### Q-FND-03: Scale Targets

**Context:** I need to size the architecture appropriately. Over-engineering wastes effort; under-engineering causes rework.

**Questions:**
1. Expected concurrent users at launch: ___
2. Growth over 2 years: ___
3. Number of separate organizations/tenants: ___
4. Expected data volume per year: ___

**If unknown:** I'll design for moderate scale (~1K concurrent users) with horizontal scaling capability for growth.

**Your input:** _[awaiting input]_
```

#### Important (Influence Major Decisions)

```markdown
### Q-FND-04: Team Profile

**Context:** Technology choices should match what the team can build and maintain long-term.

**Questions:**
1. Primary programming language(s) the team knows: ___
2. Approximate team size: ___
3. DevOps/infrastructure maturity (1-5): ___
4. Are there technology preferences or mandates from leadership? ___

**Your input:** _[awaiting input]_
```

```markdown
### Q-FND-05: Integration Requirements

**Context:** External system integrations significantly shape the architecture boundary.

**Questions:**
1. What external systems must this integrate with? (List them)
2. Are there existing APIs we must conform to?
3. Real-time requirements? (events, webhooks, streaming)
4. Authentication federation? (SSO, LDAP, SAML)

**Your input:** _[awaiting input]_
```

---

### Step 4: Determine Workflow Depth

Based on extracted information, assess complexity:

| Factor | Score 1 (Simple) | Score 2 (Moderate) | Score 3 (Complex) |
|--------|-----------------|-------------------|-------------------|
| Component count (estimated) | <5 | 5-15 | >15 |
| Integration points | 0-2 | 3-6 | >6 |
| Multi-tenancy | None | Simple isolation | Complex multi-tenant |
| Security requirements | Standard auth | Compliance-driven | Regulated/classified |
| Scale | <1K users | 1K-100K users | >100K users |
| Team familiarity with domain | High | Medium | Low |
| Novelty of approach | All proven patterns | Some new patterns | Novel/unproven |

**Complexity Score:** Sum / 21

| Score Range | Depth |
|:-----------:|-------|
| 7-10 | Minimal |
| 11-15 | Standard |
| 16-21 | Comprehensive |

---

### Step 5: Produce Architecture Requirements Summary

Compile all extracted information into a single concise document:

```markdown
# Architecture Requirements Summary — {system_name}

## Date: {date}
## Input Source: {mode — PIP / Document / Verbal / Brownfield}
## Complexity Assessment: {score}/21 — {depth level}

---

## 1. System Purpose
{1-2 sentence description of what the system does and for whom}

## 2. Functional Domains
{Table from 2a}

## 3. Quality Attributes
{Table from 2b}

## 4. Constraints
{Table from 2c}

## 5. Scale Targets
{Table from 2d}

## 6. Integration Landscape
{Table from 2e}

## 7. Team Context
{Table from 2f}

## 8. Key Architecture Drivers (Top 5)
1. {Most important thing that shapes the architecture}
2. {Second}
3. {Third}
4. {Fourth}
5. {Fifth}

## 9. Workflow Depth Recommendation: {Minimal / Standard / Comprehensive}
**Rationale:** {Why this depth — reference complexity factors}
```

---

### Step 6: Present for Confirmation

```markdown
## Stage 2: Requirements Ingestion — Summary

I've analyzed your input and extracted the architecture requirements.

**Key findings:**
- **Functional domains:** {n}
- **Quality attributes:** {n} defined
- **Constraints:** {n} hard boundaries
- **Integrations:** {n} external systems
- **Complexity:** {score}/21 — {level}
- **Recommended depth:** {depth}

**Top architecture drivers:**
1. {Driver 1}
2. {Driver 2}
3. {Driver 3}

**Full summary:** Saved to `{file_path}`

---

**Your response:**
- (a) **Confirm** — Proceed to Architecture Vision (Stage 3)
- (b) **Add more context** — I have additional information
- (c) **Adjust depth** — I want {more/less} rigor than recommended
- (d) **Challenge drivers** — The top drivers are wrong; here's what matters most
```

---

### Step 7: Log and Transition

1. Update state file:
   - Stage 2: ✅ Done
   - Workflow Depth: {confirmed depth}
   - Current Stage: 3
2. Update Architecture Workbook:
   - Session log: "Stage 2 complete. Input mode: {mode}. Depth: {level}. {n} drivers identified."
3. Log any assumptions made during extraction

Display:

```
✅ Stage 2: Requirements Ingestion — Complete

📄 Input: {mode} | Complexity: {level} | Depth: {depth}
🎯 Top driver: {#1 driver}

Next → Stage 3: Architecture Vision & Principles
I'll now define the architectural vision, guiding principles, and constraints.

Proceeding...
```

---

## Output File

Save Architecture Requirements Summary to:
- Numbered: Not saved as a numbered document (it's a working input, not a deliverable). Stored in state file context.
- If user requests it saved: `{output_root}/00_Architecture_Requirements_Summary.md`

---

## Quality Rules

1. **Never invent requirements** — extract only what's stated or directly implied
2. **Flag gaps explicitly** — "No performance targets stated; assuming p95 < 1s" is better than silently guessing
3. **Constraints are sacred** — if a constraint is stated, it limits the design space absolutely
4. **Architecture drivers are prioritized** — not everything is equally important; rank them
5. **Team context matters** — a perfect architecture the team can't build is a bad architecture
