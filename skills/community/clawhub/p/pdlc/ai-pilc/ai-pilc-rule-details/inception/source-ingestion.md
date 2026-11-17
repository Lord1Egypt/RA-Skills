<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Source Document Ingestion

## Stage: 2 of 16
## Phase: 🔵 INCEPTION
## Execution: ALWAYS

---

## Purpose

Receive the user's source requirement, validate it, assess project complexity, and determine the appropriate workflow depth for all subsequent stages. This is the foundation — everything that follows depends on what's ingested here.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Decompose the source into atomic elements (problem, outcome, constraints, stakeholders) before judging completeness
- Surface ambiguity explicitly — flag any statement that could be read two ways rather than silently interpreting it
- Trace every extracted element back to a specific part of the source; mark anything inferred as an assumption
- Assess complexity from evidence in the source, not from optimism

### Anti-Patterns for This Stage
- Do NOT fabricate detail the source doesn't contain — capture gaps as `_[TBD]_`, don't invent
- Do NOT smooth over contradictions in the source — name them for the clarification cycle

### Quality Check
A good output at this stage sounds like:
- "The source states X explicitly; Y is inferred (flagged as an assumption); Z is missing and captured as TBD with an Action Item..."

---

## Step-by-Step Execution

### Step 1: Receive Source Material

Based on the user's response at the end of Stage 1, handle one of three intake modes:

#### Mode A: File Path

1. Read the file at the specified path
2. Confirm file was read successfully
3. Store path reference in state file: `Source Document: {path}`
4. Proceed to Step 2

#### Mode B: Pasted Content

1. Accept the full pasted text
2. Save to: `{output_root}/__input/source_requirement.md` (or equivalent input folder)
3. Confirm receipt and character/word count
4. Store reference in state file: `Source Document: __input/source_requirement.md (pasted)`
5. Proceed to Step 2

#### Mode C: Verbal Description

1. Accept the user's verbal description
2. Ask clarifying questions to fill minimum viable requirement context:
   - What problem are you solving?
   - Who is the intended user/customer?
   - What does success look like?
   - Any known constraints (budget, timeline, technology)?
   - Who is sponsoring this?
3. Synthesize responses into a structured brief
4. Save to: `{output_root}/__input/source_requirement_verbal.md`
5. Present the synthesized brief for user confirmation: "Is this an accurate capture of your intent?"
6. Iterate if needed
7. Store reference in state file
8. Proceed to Step 2

**Note for Mode C:** The workflow depth will likely be "Standard" or "Comprehensive" since verbal descriptions inherently have more gaps to resolve.

#### Mode D: Brownfield Extension

When the user indicates they are extending, modernizing, or integrating with an EXISTING system:

1. Ask the user to identify the existing system:
   - "What existing system are you extending/modernizing?"
   - "What's the relationship? (extend with new module / replace subsystem / integrate with / modernize)"
2. Capture existing system context:
   - System name, age, technology stack
   - Current state (Healthy / Aging / Legacy / Critical)
   - Documentation availability (Well-documented / Partial / Undocumented)
   - Team familiarity (Expert / Moderate / Limited / None)
   - Active users/consumers of the existing system
3. Determine brownfield type:
   - **Extend** — Adding new capability to an existing platform (existing stays, new module added)
   - **Replace** — Building replacement for part or all of the existing system
   - **Integrate** — New system must deeply integrate with existing (bidirectional data flow)
   - **Modernize** — Upgrading technology/architecture while preserving functionality
4. Store in state file:
   - `Project Type: Brownfield Extension`
   - `Existing System: {name}`
   - `Brownfield Type: {Extend / Replace / Integrate / Modernize}`
   - `Existing System State: {state}`
5. Activate brownfield-adapted deliverables for all subsequent stages:
   - Requirement Intake Form → includes "Existing System Context" section
   - Feasibility Assessment → adds "Integration Feasibility" dimension
   - Risk Register → pre-populates migration/compatibility risks
   - Scope Statement → distinguishes EXISTING / NEW / CHANGING scope
   - Business Case → includes "Extend vs. Replace vs. Buy" framing
6. Proceed to Step 2

**Note for Mode D:** The workflow depth will be at least "Standard" (brownfield projects inherently have more complexity from coexistence and migration concerns). If the existing system is Legacy or Critical state, recommend "Comprehensive."

**Brownfield detection (automatic):** If the user's source document (Mode A/B) mentions phrases like "existing system," "legacy," "migration," "extend the platform," "replace module," "integrate with," or "modernize" — proactively ask: "It sounds like this involves an existing system. Should I treat this as a brownfield extension?" If yes → switch to Mode D behavior.

#### Mode E: AI-ILC Brief (Chain Intake)

When `ilc-state.md` is detected (AI-ILC ran before AI-PILC) or the user says "I have an AI-ILC approved idea brief":

1. Read `ilc-state.md` from the detected/specified location
2. Extract the Approved Idea Brief fields:
   - Idea name / ID → pre-populate `{project_name}` suggestion (user can override)
   - Scope summary → pre-populate problem statement
   - Approval status → confirm it is "Approved" (reject if "Parked" or "Rejected" — inform user)
   - Route field → confirm it says `project` (other routes target different packages)
3. Map the AI-ILC output to AI-PILC intake:
   - Idea Problem Statement → Source requirement (captures the "what needs solving")
   - Idea Scope (v1.0) → Initial scope boundaries
   - Idea Dependencies → Constraints / assumptions seed
   - Idea Risks → Risk register seed
4. Save extracted content to: `{output_root}/__input/source_from_ilc_brief.md`
5. Store in state file:
   - `Source Document: __input/source_from_ilc_brief.md (from AI-ILC)`
   - `derivedFrom: {idea_id}` (auto-populated from `ilc-state.md` — REQUIRED per Traceability Contract §4-A)
   - `Originating Idea: {idea_id}` (legacy alias — kept for backward compatibility)
   - `Intake Mode: AI-ILC Brief`
6. Present summary for user confirmation:
   ```
   📋 AI-ILC Brief Detected
   
   Idea: {idea_name} (ID: {idea_id})
   Status: Approved ✅
   Route: Project → AI-PILC
   
   I've extracted the following from the approved idea:
   - Problem: {problem summary}
   - Scope: {scope summary}
   - Dependencies: {count} identified
   - Risks: {count} pre-identified
   
   This will be used as the source requirement for project initiation.
   
   (a) Accept and proceed with this as the source
   (b) I have additional source material to add alongside
   (c) Use a different source document instead (ignore the ILC brief)
   ```
7. If (a) → proceed to Step 2 with the ILC brief as source
8. If (b) → accept additional material; merge with ILC brief (ILC brief = primary, additional = supplementary)
9. If (c) → discard ILC brief; switch to Mode A/B/C; still record `derivedFrom` in state (lineage preserved even if source is replaced)
10. Proceed to Step 2

**Note for Mode E:** The workflow depth will typically be "Standard" — ILC briefs are structured (they've been through evaluate + scope), so completeness is usually 60-80%. Complexity is assessed from the scope section, not the brief format.

**OR-input (optional predecessor) compliance:** Mode E is purely ADDITIVE — Modes A/B/C/D remain unchanged. If `ilc-state.md` is detected but the user prefers another mode, they can switch (option c above). The AI-ILC brief is an optional enrichment path, not a requirement.

---

### Step 2: Source Characterization

Analyze the source material and determine its characteristics:

#### 2a: Document Type Classification

| Type | Indicators | Example |
|------|-----------|---------|
| **PRD (Product Requirements Document)** | Structured sections, functional/non-functional reqs, user stories or features | Formal product spec |
| **RFP/RFI** | Vendor-facing, evaluation criteria, response format | Procurement document |
| **Business Brief** | Problem/opportunity focus, strategic context, light on specifics | Executive proposal |
| **Technical Specification** | Architecture-heavy, system-focused, API contracts | Engineering-driven |
| **User Story Collection** | As-a/I-want/So-that format, acceptance criteria | Agile backlog |
| **Email/Meeting Notes** | Informal, conversational, action-oriented | Captured discussion |
| **Verbal Synthesis** | AI-structured from conversation (Mode C) | From this session |
| **Mixed/Hybrid** | Combines multiple formats | Common in practice |

#### 2b: Completeness Assessment

Score each dimension (1-5):

| Dimension | 1 (Absent) | 3 (Partial) | 5 (Complete) |
|-----------|-----------|-------------|--------------|
| Problem/need statement | Not stated | Implied but not explicit | Clear, specific, measurable |
| Stakeholders identified | None named | Some roles mentioned | Full list with roles and authority |
| Functional requirements | Wish list or vague | Some specifics, some gaps | Detailed, testable, traceable |
| Non-functional requirements | Not addressed | Some mentioned | Comprehensive with targets |
| Constraints & assumptions | Not stated | Some noted | Explicitly listed and bounded |
| Scope boundaries | No in/out distinction | Some exclusions noted | Clear in-scope and out-of-scope |
| Timeline expectations | None | "Soon" or vague | Specific dates or duration |
| Budget context | None | "Limited" or range | Specific amount or envelope |
| Success criteria | Not defined | Implied | Explicit and measurable |
| Risk awareness | None | Some concerns noted | Risks identified with impact |

**Completeness Score:** Sum / 50 → percentage

| Score Range | Rating |
|-------------|--------|
| 80-100% | Comprehensive — source is thorough |
| 60-79% | Structured — good foundation with some gaps |
| 40-59% | Draft — significant gaps to resolve |
| 20-39% | Idea — early stage, major structuring needed |
| 0-19% | Seed — minimal input, heavy elicitation required |

---

### Step 3: Complexity Assessment

Based on the source content, assess project complexity across these factors:

| Factor | Low (1) | Medium (2) | High (3) | Score |
|--------|---------|-----------|----------|:-----:|
| **Scale** (team size, users, budget) | <5 people, <$100K | 5-20 people, $100K-$1M | >20 people, >$1M | |
| **Duration** | <3 months | 3-12 months | >12 months | |
| **Stakeholder field** | 1-3 stakeholders | 4-10 stakeholders | >10 stakeholders | |
| **Technical novelty** | Known technology, proven patterns | Some new tech or approaches | Novel/unproven, R&D component | |
| **Integration points** | Standalone or 1-2 integrations | 3-5 external systems | >5 systems, complex data flows | |
| **Regulatory/compliance** | None | Some standards to meet | Heavy regulation, audit required | |
| **Organizational change** | Minimal process change | Moderate change, training needed | Major transformation, culture shift | |
| **Dependency count** | Self-contained | 3-5 external dependencies | >5, cross-org dependencies | |

**Complexity Score:** Sum / 24

| Score Range | Complexity Level |
|-------------|-----------------|
| 8-11 | Low |
| 12-16 | Medium |
| 17-20 | High |
| 21-24 | Very High |

---

### Step 4: Determine Workflow Depth

Map completeness + complexity to workflow depth:

```
                    SOURCE COMPLETENESS
                    Low         Medium      High
                 ┌───────────┬───────────┬───────────┐
        Low      │ Standard  │ Minimal   │ Minimal   │
COMPLEXITY       ├───────────┼───────────┼───────────┤
        Medium   │ Comprehen.│ Standard  │ Standard  │
                 ├───────────┼───────────┼───────────┤
        High     │ Comprehen.│ Comprehen.│ Standard  │
                 ├───────────┼───────────┼───────────┤
        Very High│ Comprehen.│ Comprehen.│ Comprehen.│
                 └───────────┴───────────┴───────────┘
```

**Depth determines:**

| Aspect | Minimal | Standard | Comprehensive |
|--------|---------|----------|---------------|
| Requirements Analysis | Brief gap check | Full analysis report | Exhaustive with traceability |
| Clarification Cycle | Only if critical gaps | If any critical/high gaps | Always — proactive elicitation |
| Feasibility dimensions | Scored with brief notes | Scored with commentary | Scored with evidence and conditions |
| Business Case options | Single recommended approach | 2-3 options compared | 3-4 options with detailed analysis |
| WBS depth | 2-level | 3-level | 4-level with estimates |
| Risk Register size | 5-8 risks | 10-15 risks | 15-25 risks with full treatment |
| Stakeholder analysis | Register only | Register + power/interest | Register + matrix + engagement plan |
| Interaction cycles | 1 per stage | 1-2 per stage | 2-3 per stage |

---

### Step 5: Present Assessment

Display the assessment to the user:

```markdown
## Source Assessment — {project_name}

### Document Profile
| Attribute | Value |
|-----------|-------|
| Type | {document_type} |
| Word count | {n} words |
| Completeness | {score}% — {rating} |
| Complexity | {score}/24 — {level} |

### Completeness Breakdown
| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Problem statement | {n} | {brief note} |
| Stakeholders | {n} | {brief note} |
| Functional requirements | {n} | {brief note} |
| Non-functional requirements | {n} | {brief note} |
| Constraints & assumptions | {n} | {brief note} |
| Scope boundaries | {n} | {brief note} |
| Timeline | {n} | {brief note} |
| Budget | {n} | {brief note} |
| Success criteria | {n} | {brief note} |
| Risk awareness | {n} | {brief note} |

### Recommended Workflow Depth: **{depth_level}**

**Rationale:** {1-2 sentences explaining why this depth is appropriate}

### What This Means
{Brief explanation of how this depth level affects the workflow — what stages get more/less attention}

---

**Your response:**
- (a) **Accept** — Proceed with {depth_level} depth
- (b) **Go deeper** — I want more rigor regardless of source quality
- (c) **Go lighter** — I want faster delivery; I'll accept less detail
- (d) **Adjust** — The complexity assessment is off; let me correct it
```

---

### Step 6: Log and Update State

1. Log decision in Decision Log:
   - D-002: "Source document accepted. Type: {type}. Completeness: {score}%. Complexity: {level}. Workflow depth: {depth}."
2. Update state file:
   - Source Document: {reference}
   - Workflow Depth: {chosen_depth}
   - Stage 2: ✅ Done
   - Current Stage: 3
3. Log assumptions:
   - ASM-002: "Source document represents current stakeholder intent and is the authoritative scope reference."
   - ASM-003 (if applicable): "Source document is version {X} and no newer version exists."

---

### Step 7: Transition to Stage 3

Display:

```
✅ Stage 2: Source Document Ingestion — Complete

📄 Source: {type} — {completeness_rating}
🎚️  Depth: {depth_level}
📊 Complexity: {level}

Next → Stage 3: Requirement Structuring
I'll now analyze your source and produce a structured Requirement Intake Form.

Proceeding...
```

Auto-proceed to Stage 3 (no separate gate between 2 and 3 — they are tightly coupled within INCEPTION).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| Source is extremely short (<100 words) | Default to Mode C behavior — ask follow-up questions to enrich |
| Source is extremely long (>50 pages) | Summarize key sections; ask user to confirm focus areas; depth → Comprehensive |
| Source is in a language the AI can support | Process in source language; ask user which language deliverables should use |
| Source is a spreadsheet or structured data | Extract text content; note format; proceed with text analysis |
| Source contains confidential markings | Note in state; remind user that outputs will contain derived content; ask if any sections should be excluded |
| Multiple source documents | Accept all; ask user which is primary and which are supplementary; process primary first |
| Source contradicts itself | Note contradictions; flag for Clarification Cycle (Stage 5); proceed with higher completeness assumption |
| User says "I don't have a document yet" | Switch to Mode C (verbal); note that depth will be higher to compensate |

---

## Source Document Rules

1. **Never modify** the source document — treat it as read-only input
2. **Never invent** requirements not found in (or reasonably implied by) the source
3. **Always reference** the source when producing derived content
4. **Flag** anything in the source that seems unrealistic, contradictory, or incomplete — don't silently accept
5. **Preserve** the source's intent even when restructuring into standard formats
6. If source is provided as a file path, store the path — do not copy the entire document into outputs (reference it)
