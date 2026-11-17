<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Question Format Guide

## Purpose

AI-ADLC uses structured questions to collect architecture decisions from the user. This document defines formatting rules, interaction patterns, and ADR generation triggers specific to architecture design decisions.

---

## Question Types

### Type 1: Architecture Decision Question (ADR-Triggering)

Used when the workflow needs the user to choose between technology options or architectural patterns. **This type produces an ADR.**

**Format:**

```markdown
### Q-{phase_prefix}-{nn}: {Decision Title}

**Context:** {Why this decision matters now. What depends on it. What constraint or requirement drives it.}

**Decision Drivers:**
- {Driver 1 — what makes this choice important}
- {Driver 2}
- {Driver 3}

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **(a) {Name}** | {What this is — 1 sentence} | {Key advantages} | {Key disadvantages} |
| **(b) {Name}** | {What this is} | {Advantages} | {Disadvantages} |
| **(c) {Name}** | {What this is} | {Advantages} | {Disadvantages} |

**Recommended:** Option ({x}) — {Name}

**Rationale:** {Why this is the CTO recommendation. Reference to decision drivers, team context, constraint alignment, production track record. 3-5 sentences.}

**Consequences if chosen:**
- Positive: {What this enables}
- Negative: {What trade-off is accepted}
- Risk: {What could go wrong}

**Your Decision:** _[awaiting input]_

→ _This decision will generate ADR-{nnn}_
```

**Rules:**
- Always present options in a comparison table (not just bullets)
- Always include pros AND cons for each option (no strawmen)
- Always state consequences of the recommended option (honest about trade-offs)
- Flag that this produces an ADR
- Minimum 2 options, maximum 5
- "Do nothing" is only an option if the feature/component is genuinely optional

---

### Type 2: Design Confirmation Question

Used when the workflow needs to confirm an architectural approach that doesn't have meaningful alternatives (the "how" is clear, just confirming intent).

**Format:**

```markdown
### {Approach Statement}

Based on {requirements/constraints/decisions made}, I recommend:

{Brief description of the approach — 2-3 sentences}

**Key characteristics:**
- {Characteristic 1}
- {Characteristic 2}
- {Characteristic 3}

**Confirm:** [Approve / Challenge / Modify]
```

**Rules:**
- Use when there's really only one viable approach given constraints
- Does NOT produce an ADR (no meaningful alternatives existed)
- If user challenges → escalate to a Type 1 question with alternatives

---

### Type 3: Information Request

Used when the workflow needs factual input to make design decisions.

**Format:**

```markdown
### {What information is needed}

**Why this matters for architecture:** {How this input affects design decisions}

**What I need to know:**
1. {Specific question — e.g., "What's the expected peak concurrent users?"}
2. {Question}
3. {Question}

**If unknown:** I'll proceed with assumption: {stated assumption}. We can revise later.

**Your input:** _[awaiting input]_
```

**Rules:**
- Always state what you'll assume if the user doesn't know
- Group related information requests (max 5 per batch)
- Architecture-relevant only — don't ask project management questions

---

### Type 4: Review & Approve (Architecture Document)

Used when presenting a completed architecture document for approval.

**Format:**

```markdown
### Review: {Document Name}

I've produced the {document_name}. Architecture highlights:

**System shape:**
- {Key architectural decision 1}
- {Key architectural decision 2}
- {Key pattern/approach 3}

**Key numbers:**
- {n} components/containers/modules
- {n} external integrations
- {n} ADRs produced in this stage

**Diagram:** {Brief description of what the diagram shows}

**Full document:** Saved to `{file_path}`

**Your response:**
- (a) **Approve** — Design is sound; proceed to next stage
- (b) **Challenge a decision** — Specific architectural choices need discussion
- (c) **Request deeper detail** — Need more specifics in certain areas
- (d) **Rethink approach** — Fundamental direction needs reconsideration
```

---

## Question Numbering

| Phase | Prefix | Example |
|-------|--------|---------|
| Foundation | FND | Q-FND-01 |
| Decomposition | DEC | Q-DEC-01 |
| Decisions | DCS | Q-DCS-01 |
| Design | DSG | Q-DSG-01 |
| Assembly | ASM | Q-ASM-01 |
| Configuration | CFG | Q-CFG-01 |

---

## ADR Generation Rules

### When to Generate an ADR

| Condition | Generate ADR? |
|-----------|:-------------:|
| 2+ viable technology options evaluated | ✅ Yes |
| Pattern choice with 5+ year implications | ✅ Yes |
| Decision that contradicts common expectation | ✅ Yes |
| User overrides AI recommendation | ✅ Yes |
| Only one viable option given constraints | ❌ No (log in document only) |
| Configuration detail (not strategic) | ❌ No |
| Obvious industry standard choice | ❌ No (unless user asks "why?") |

### ADR from Question Response

When a Type 1 question is answered:

1. Immediately produce ADR file: `ADR/{ADR-nnn}_{Title_Slug}.md`
2. Use template `templates/adr-template.md`
3. Fill: Context, Decision Drivers, Options (from question), Decision (user's choice), Rationale (user's reason or accepted recommendation), Consequences
4. Update state file ADR register
5. Summarize decision in the parent architecture document

### ADR Numbering

- Sequential: ADR-001, ADR-002, ADR-003...
- Never skip numbers
- Never reuse numbers (superseded ADRs keep their number; new one gets next number)

---

## Batching Rules for Architecture

### When to batch questions

- Technology stack selection (Stage 6): related tech choices can be batched by category (backend, frontend, database, infrastructure)
- Maximum 3 architecture decisions per batch (decisions are weightier than PMO questions)

### When NOT to batch

- Decisions where choice A constrains choice B (e.g., language selection before framework selection)
- Multi-tenancy strategy (single focused decision)
- Security architecture (each concern is independent)

### Batch format for tech stack

```markdown
## Technology Decisions — {Category}

The following technology choices are needed for {category}. They are related and I'm presenting them together.

---

### Q-DCS-{nn}: {Decision 1}
{...full Type 1 format...}

---

### Q-DCS-{nn}: {Decision 2}
{...full Type 1 format...}

---

**Shortcut:** "Accept all recommendations" to approve the full batch.
```

---

## User Response Handling

| User Says | Interpretation |
|-----------|---------------|
| "a" or "(a)" | Selected option A |
| "Go with your recommendation" | Accept recommended option; produce ADR |
| "Accept all" | Accept all recommendations in batch; produce ADRs |
| "a, but we should also consider..." | Option A with noted caveat; log caveat in ADR |
| "None of these — we should use X" | Custom option; CTO evaluates; produce ADR with user's option added |
| "I need to discuss with the team" | Mark as pending; log in Workbook open questions; proceed with assumption |
| "Why not option B?" | Explain trade-offs of B vs recommendation; re-present for decision |
| "Let's revisit this later" | Defer; log assumption; proceed; return before Assembly |

### Handling "Why not X?"

This is a signal that the user wants deeper analysis. When this happens:
1. Provide a thorough comparison of the user's suggested option vs. the recommendation
2. Acknowledge valid strengths of their suggestion
3. Explain the specific reasons the recommendation was preferred
4. Offer to produce an ADR that documents both options regardless of final choice
5. Let the user decide — never argue past one explanation

---

## Architecture-Specific Question Quality

### Do:
- Present options that are ALL genuinely viable (no obvious losers)
- Include real-world production evidence for recommendations
- Acknowledge when you're recommending the "boring" choice over the "exciting" one
- Consider team context: what they know, what they can maintain
- Reference constraints explicitly: "Given constraint C3 (on-premises), option B is eliminated"

### Don't:
- Present options that violate stated constraints (waste of decision energy)
- Recommend bleeding-edge tech without acknowledging the risk
- Dismiss user suggestions without thorough consideration
- Ask architecture questions that the requirements already answer clearly
- Present more than 5 options (decision fatigue; 3 is ideal)
- Make decisions for the user without presenting them (even if "obvious")

---

## Decision Dependency Map

```
Q-FND-01 (System complexity) ──► Determines depth for all stages
Q-DEC-01 (System boundary) ──► Defines what's in scope for container design
Q-DCS-01 (Backend language) ──► Constrains framework, ORM, tooling choices
Q-DCS-02 (Database) ──► Constrains data architecture, multi-tenancy, search
Q-DCS-03 (Multi-tenancy model) ──► Constrains data, security, API, component design
Q-DCS-04 (Auth strategy) ──► Constrains API security, token handling
```

If a dependent decision hasn't been made:
- Ask the prerequisite first, OR
- State assumption explicitly and flag for revisit
