<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Architecture Vision & Principles

## Stage: 3 of 13
## Phase: 🔵 FOUNDATION
## Execution: ALWAYS

---

## Purpose

Define the architectural north star — a vision statement, guiding principles, constraints, and quality attribute priorities that will govern ALL subsequent design decisions. This document becomes the constitution of the architecture: every recommendation in later stages must be traceable to a principle or driver defined here.

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS stage, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in principles that CONSTRAIN the solution space — each principle eliminates options; if it doesn't, it's decoration
- Define the architectural north star as a boundary: what the system WILL be and (equally) what it WILL NOT be
- Trace every principle to at least one driver or constraint from Stage 2 — orphan principles are opinions, not architecture
- Prioritize quality attributes against each other — everything can't be #1; force-rank the trade-offs

### Anti-Patterns for This Stage
- Do NOT define principles that can't be violated (they're truisms, not constraints)
- Do NOT skip the trade-off conversation — "availability AND consistency AND partition-tolerance" is impossible; name the sacrifice

### Quality Check
A good output at this stage sounds like:
- "7 principles, each traced to a driver; QA trade-off: availability > consistency for this system; 4 constraints that eliminate specific technology options..."

---

## Depth Adaptation

| Depth | Vision & Principles Behavior |
|-------|------------------------------|
| **Minimal** | 3-5 principles. Brief constraint table. Quality attributes as a priority list only. Stakeholder mapping optional. |
| **Standard** | 5-8 principles with rationale. Full constraint table with impact analysis. Quality attributes with targets. Stakeholder concern mapping. |
| **Comprehensive** | 8-12 principles with detailed implications. Constraints cross-referenced to options eliminated. Quality attributes with measurable targets and trade-off analysis. Full stakeholder mapping with architecture responses. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Architecture Requirements Summary (Stage 2 output — in state file)
2. Top architecture drivers (prioritized list from Stage 2)
3. Constraints (from Stage 2 extraction)
4. Quality attributes (from Stage 2 extraction)
5. Team context (size, skills, maturity)

---

### Step 2: Draft Architecture Vision Statement

Produce a 2-4 sentence statement answering:
- What is being built?
- What does the architecture optimize for? (primary quality)
- What is the key architectural challenge?
- What is the deployment/operational model?

**Format:**

```markdown
## Architecture Vision Statement

{Statement — concise, specific, opinionated. Not generic "build a good system" but specific to THIS system's unique challenges.}

The architecture must optimise for:
- **{Quality 1}** — {why this is the top priority}
- **{Quality 2}** — {why}
- **{Quality 3}** — {why}
- **{Quality 4}** — {why}
```

**Rules:**
- Derived from the top architecture drivers (Stage 2)
- Should be specific enough that two architects would produce similar designs from it
- Should make clear what is PRIORITIZED (not everything can be #1)
- Use "optimise for" not "must have" — this is about trade-off priorities

---

### Step 3: Define Guiding Principles

Principles are opinionated architectural guidelines that constrain the design space. Each principle answers: "When in doubt, prefer X over Y."

**Produce 7-12 principles (Standard depth). 5-7 for Minimal, 10-15 for Comprehensive.**

**Principle format:**

```markdown
### P{n}: {Principle Name}

{One-sentence principle statement — clear, actionable, opinionated.}

**Rationale:** {Why this principle matters for THIS system — 1-2 sentences.}

**Implication:** {What this means in practice — what you'd do/not do because of this principle.}
```

**Principle derivation sources:**

| Source | Typical Principles |
|--------|-------------------|
| Deployment constraint | "On-Premises Sovereignty" — no cloud dependencies |
| Scale requirement | "Design for Scale, Deploy for Today" — scalable architecture, right-sized deployment |
| Multi-tenancy | "Tenant Context is Non-Negotiable" — every operation carries tenant identity |
| Team size | "Modular Monolith First" — microservices only when justified |
| Security | "Security by Default" — encryption, RBAC, audit from day one |
| API-first | "API-First, UI-Second" — UI is a consumer, not a privileged path |
| Maintainability | "Convention Over Configuration" — developers shouldn't need to remember |
| Operability | "Observable by Default" — health checks, metrics, structured logging |
| Cost | "Open-Source Only" — no proprietary dependencies |
| AI/ML | "Progressive Enhancement" — AI is additive, never in the critical path |
| Branding/White-label | "First-Class Concern" — not a CSS override but an architectural subsystem |
| Extensibility | "Modular and Pluggable" — new modules without core refactoring |

**Ask user to review principles:**

```markdown
### Review: Guiding Principles

I've drafted {n} architectural principles based on your requirements and constraints.

**Principles defined:**
{Numbered list of principle names with 1-line summaries}

**Questions:**
1. Are any of these wrong or need rewording?
2. Are there principles you'd add?
3. Should any be removed or combined?
4. Are the priorities correct (listed in importance order)?

**Your response:** _[Approve / Modify / Add]_
```

---

### Step 4: Document Architectural Constraints

Formalize constraints from Stage 2 into a structured table:

```markdown
## Key Architectural Constraints

| # | Constraint | Source | Impact on Design |
|---|-----------|--------|------------------|
| C1 | {constraint statement} | {where it comes from — PRD, Charter, regulation, business} | {What this eliminates or mandates in the design space} |
| C2 | {constraint} | {source} | {impact} |
```

**Constraint rules:**
- Constraints are NON-NEGOTIABLE (unlike principles which guide, constraints BLOCK)
- Every constraint must have a source (not invented by the architect)
- Impact column explains what design options are eliminated
- If a constraint conflicts with another, flag immediately for resolution

**Common constraint categories:**
- Deployment (where it runs)
- Technology (what can/can't be used)
- Compliance (regulations that apply)
- Performance (hard SLA/SLO targets)
- Budget (license cost limits)
- Integration (must connect to X)
- Localization (languages, RTL support)
- Accessibility (WCAG level)

---

### Step 4b: Brownfield Constraints (IF MODE D ACTIVE)

**Execute IF:** Requirements Ingestion detected brownfield input (Mode D).
**Skip IF:** Greenfield project.

When the project extends, modernizes, or replaces an existing system, additional constraints emerge that are unique to brownfield scenarios. These MUST be captured alongside standard constraints because they limit the design space in ways greenfield projects never encounter.

**Brownfield-specific constraints to elicit:**

| Category | Questions to Ask | Constraint Pattern |
|----------|-----------------|-------------------|
| **Backward Compatibility** | "Must existing API consumers continue working unchanged?" | C{n}: All existing API endpoints must remain operational during transition (no breaking changes to live consumers) |
| **Data Coexistence** | "Will new and old systems share a database? For how long?" | C{n}: Shared database during transition — schema changes must be backward-compatible |
| **Deployment Coupling** | "Can the new system deploy independently of the legacy?" | C{n}: {Independent / Coupled} deployment — new module {can / cannot} release without legacy coordination |
| **Technology Constraints** | "Are you locked into any technology from the existing system?" | C{n}: Must integrate with {existing tech} — replacement not possible in scope |
| **Transition Duration** | "How long will old and new coexist?" | C{n}: Parallel operation period: {duration} — both systems must be maintainable simultaneously |
| **Feature Parity** | "Must new system reach feature parity before legacy decommission?" | C{n}: {Full parity / Partial parity / No parity required} before cutover |
| **Knowledge Constraints** | "How well does the team know the legacy system?" | Informs risk register and characterization testing depth |

**Add to Constraints Table:**

```markdown
### Brownfield-Specific Constraints

| # | Constraint | Source | Impact on Design |
|---|-----------|--------|------------------|
| C{n} | Existing {system} API must remain operational during transition | Business continuity | Requires anti-corruption layer; new system cannot modify legacy interfaces |
| C{n} | Shared database with {system} for {duration} | Deployment topology | Schema must support both systems; migrations must be backward-compatible |
| C{n} | Zero-downtime transitions between phases | Operational requirement | Blue-green or canary deployment; feature flags for routing |
| C{n} | Legacy {component} is undocumented | Team reality | Requires characterization testing phase before any changes |
```

**Produce Brownfield Strategy ADR:**

If brownfield mode is active and the "extend vs. replace vs. strangler-fig" decision hasn't been made, produce it NOW using template `templates/brownfield-strategy-adr.md`. This ADR must be accepted before proceeding to Decomposition — because the brownfield strategy fundamentally shapes system boundaries, container design, and integration architecture.

**Principles that typically emerge in brownfield:**
- "Characterize Before Changing" — never modify what you don't understand
- "Anti-Corruption Layer" — new system defines its own model; translates at boundary
- "Reversible Transitions" — each phase must be rollback-safe
- "Progressive Migration" — value delivered at each phase, not only at completion

---

### Step 5: Prioritize Quality Attributes

Produce a ranked table of architectural quality attributes:

```markdown
## Architectural Qualities (Prioritized)

| Priority | Quality Attribute | Measure / Target | Trade-Off Accepted |
|:--------:|------------------|-----------------|-------------------|
| Critical | {attribute} | {how measured — specific metric if available} | {what we sacrifice for this} |
| High | {attribute} | {measure} | {trade-off} |
| Medium | {attribute} | {measure} | {trade-off} |
| Low | {attribute} | {measure} | {trade-off} |
```

**Priority definitions:**
- **Critical** — Architecture fails if this isn't met. Non-negotiable.
- **High** — Architecture is significantly degraded without this. Strong investment.
- **Medium** — Important but acceptable to compromise slightly. Balanced investment.
- **Low** — Nice to have. Will not drive architectural complexity.

**Trade-off transparency:**
Every prioritization implies a trade-off. State them explicitly:
- "We prioritize security over development speed"
- "We prioritize maintainability over cutting-edge performance"
- "We prioritize operational simplicity over deployment flexibility"

**Ask if priorities are unclear:**

```markdown
### Q-FND-06: Quality Attribute Priorities

**Context:** Architecture is the art of trade-offs. I need to know what matters MOST when choices conflict.

**Rank these by importance for your system (1 = most important):**

- [ ] Performance (speed, responsiveness)
- [ ] Security (data protection, access control)
- [ ] Scalability (handling growth)
- [ ] Availability (uptime, resilience)
- [ ] Maintainability (ease of change, readability)
- [ ] Extensibility (adding features later)
- [ ] Operability (ease of deployment, monitoring)
- [ ] Cost efficiency (minimal infrastructure/licensing)

**Your ranking:** _[top 4 is sufficient — I'll infer the rest]_
```

---

### Step 6: Map Stakeholder Concerns

Connect each key stakeholder to their primary architectural concern:

```markdown
## Stakeholder Concerns Mapping

| Stakeholder | Primary Concern | Architecture Response |
|-------------|----------------|---------------------|
| {role/name} | {what they care about most} | {how the architecture addresses it} |
```

**Purpose:** Ensures the architecture serves ALL stakeholders, not just developers. When a design decision is contested, this table shows who benefits and who is impacted.

---

### Step 7: Assemble Vision Document

Using template `templates/architecture-vision.md`, compile:

1. Architecture Vision Statement
2. Guiding Principles (P1-Pn)
3. Key Architectural Constraints (table)
4. Quality Attributes (prioritized table)
5. Stakeholder Concerns Mapping
6. Metadata (status, version, date, author)

**Validate per `common/content-validation.md`:**
- [ ] Vision is specific to this system (not generic)
- [ ] Every principle has rationale and implication
- [ ] Constraints have sources (not invented)
- [ ] Quality priorities are explicitly ranked (not all "High")
- [ ] No contradictions between principles and constraints
- [ ] Trade-offs are stated honestly

---

### Step 8: Store in State File

Update state file with:
- Architecture Principles section (ID + name + 1-line summary per principle)
- Key Constraints section (full table)
- Quality priorities (top 4)

This ensures principles and constraints are available for consistency checking in ALL future stages without re-reading the full document.

---

### Step 9: Present for Review

```markdown
## Review: Architecture Vision — {system_name}

I've produced the Architecture Vision document.

**Vision:** {1-sentence summary of the vision statement}

**Principles defined ({n}):**
1. P1: {name} — {1-line}
2. P2: {name} — {1-line}
3. P3: {name} — {1-line}
{...}

**Constraints ({n}):**
- {Top 3 most impactful constraints}

**Quality priorities:**
- Critical: {attribute}
- High: {attribute}, {attribute}
- Medium: {attribute}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Vision and principles are right; proceed to System Context
- (b) **Adjust principles** — Some need rewording or reordering
- (c) **Add constraints** — Missing constraints I need to state
- (d) **Change priorities** — Quality attribute ranking needs adjustment
- (e) **Rethink vision** — The overall direction needs discussion
```

---

### Step 10: Log and Transition

1. Update state: Stage 3 = ✅ Done; Current Phase = DECOMPOSITION; Current Stage = 4
2. Update Architecture Workbook:
   - Session log: "Stage 3 complete. {n} principles, {m} constraints defined. Vision approved."
3. Note in workbook if any principles generated discussion (for future reference)

Display:

```
✅ Stage 3: Architecture Vision & Principles — Complete

📐 Principles: {n} defined | Constraints: {m} | Quality priorities set
📄 Saved to: {file_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ FOUNDATION PHASE COMPLETE (Stages 1-3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context loaded. Vision set. Constraints locked.
Now we design the system shape.

Next → DECOMPOSITION PHASE
Stage 4: System Context (C4 Level 1)

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/01_Architecture_Vision.md`
- Phase folders: `{output_root}/foundation/Architecture_Vision.md`

---

## Principle Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Actionable | Each principle enables a concrete design decision |
| Opinionated | Principle takes a SIDE (not "balance X and Y" but "prefer X over Y when...") |
| Non-obvious | Doesn't state what any competent architect would assume anyway |
| Traceable | Each connects to a requirement, constraint, or architecture driver |
| Consistent | No two principles contradict each other |
| Testable | You could ask "does this design follow P3?" and get a yes/no answer |
| Memorable | Short name that the team can reference in discussions ("that violates P5") |
