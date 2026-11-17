<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Architecture Vision → workspace-rules.md + architecture-principles.md

## Purpose

This mapping rule transforms the **Architecture Vision & Principles** document (AP artifact) into two steering files:
1. `rules/workspace-rules.md` — The golden rules governing all development
2. `rules/architecture-principles.md` — Full principles reference

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think of workspace-rules.md as the constitution — every word carries enforcement weight across all future development
- Translate abstract principles into concrete developer behaviors (Golden Rules derivation)
- Prioritize ruthlessly — workspace-rules must fit on 2 screens; push details to architecture-principles.md
- Ensure constraints produce clear DON'T rules — ambiguous constraints produce unenforceable rules
- Cross-reference quality attribute priorities to resolve future conflicts before they arise

### Anti-Patterns for This Activity
- Do NOT paraphrase the architect's vision statement — copy verbatim
- Do NOT generate golden rules that are too abstract to enforce (e.g., "write good code")
- Do NOT include Medium/Low quality attributes in workspace-rules — they belong only in architecture-principles.md

### Quality Check
A good output from this activity sounds like:
- "Golden Rule 3: 'NEVER allow a query to return data from multiple tenants' — derived from Principle P2 (Tenant Isolation) + Constraint C1 (Data sovereignty regulation)"
- "Quality priority hierarchy: Security > Reliability > Performance > Maintainability — when two conflict, the higher-ranked attribute wins"

---

## Source (AP Artifact)

**Document:** Architecture Vision & Principles (typically `01_Architecture_Vision.md` or `foundation/architecture-vision.md`)

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| Vision Statement | 1-2 sentence architecture optimization target | `workspace-rules.md` → header identity |
| Guiding Principles (P1-Pn) | Named principles with statement + rationale | Both files |
| Architectural Constraints | Table: constraint, source, impact | `workspace-rules.md` → DON'T rules |
| Quality Attributes | Priority-ranked list (Critical/High/Medium/Low) | `workspace-rules.md` → quality priorities |
| Stakeholder Concerns | Concerns mapped to architecture responses | `workspace-rules.md` → awareness context |

---

## Target 1: workspace-rules.md

### Role

The single most important steering file. It defines the project's architectural identity and the non-negotiable rules that govern ALL development activity. Every other steering file elaborates on what this file establishes.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision | date: {generation-date} -->

# Workspace Rules

## Project Identity

**Project ID:** {project-id}
<!-- The immutable project correlation key. Read from adlc-state.md (or pilc-state.md at generation time). 
     Used by AI-GCE/AI-TGE for audit trail correlation. -->

## Architecture Identity

{Vision statement — verbatim from AP}

**System:** {system name}
**Architecture style:** {monolith | modular-monolith | microservices | hybrid}
**Primary technology:** {language + framework}
**Deployment model:** {on-premises | cloud | hybrid}

## Guiding Principles

<!-- begin: AP-sourced -->

| # | Principle | Statement | Implication for Development |
|---|-----------|-----------|---------------------------|
| P1 | {name} | {statement — verbatim from AP} | {what this means as a development rule} |
| P2 | {name} | {statement} | {implication} |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Constraints (Non-Negotiable)

<!-- begin: AP-sourced -->

These constraints are ABSOLUTE. They cannot be violated regardless of convenience or preference.

| Constraint | Rule | Source |
|-----------|------|--------|
| {constraint name} | {DO NOT / NEVER / MUST NOT statement} | {where it came from — PRD, legal, infrastructure} |
| ... | ... | ... |

<!-- end: AP-sourced -->

## Quality Priorities

Development decisions MUST prioritize quality attributes in this order:

<!-- begin: AP-sourced -->

1. **{Critical attribute}** — {what this means practically}
2. **{Critical attribute}** — {what this means practically}
3. **{High attribute}** — {what this means practically}
4. ...

<!-- end: AP-sourced -->

When two quality attributes conflict, the higher-priority attribute wins.

## Golden Rules

<!-- begin: AP-sourced -->

1. {Rule derived from P1 — prescriptive, actionable}
2. {Rule derived from P2 — prescriptive, actionable}
3. {Rule derived from constraints — what NEVER to do}
4. ...

<!-- end: AP-sourced -->

## Scope Awareness

This system includes: {module list from C4 L3 — brief}
This system does NOT include: {explicitly out-of-scope items from Vision}

## References

- Architecture Principles (full detail): `rules/architecture-principles.md`
- Technology Stack: `rules/tech-stack.md`
- Module Structure: `rules/module-structure.md`
```

### Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Vision statement | Copy verbatim | Architecture Identity section |
| Principle name + statement | Copy verbatim; ADD "Implication for Development" column | Principles table |
| Principle rationale | Compress into 1-sentence development implication | Implication column |
| Constraint (table row) | Convert to MUST NOT / NEVER / DO NOT rule | Constraints section |
| Quality attribute (Critical) | Convert to priority instruction: "prioritize X over Y" | Quality Priorities |
| Quality attribute (High) | Same treatment, listed after Critical | Quality Priorities |
| Quality attribute (Medium/Low) | Mentioned but not as override rules | Not in workspace-rules (goes to architecture-principles only) |

### Derivation: Golden Rules

Golden Rules are DERIVED from principles + constraints. They are the most important behavioral rules:

**Derivation method:**
1. For each principle, ask: "What does a developer MUST DO or MUST NOT DO to honor this?"
2. For each constraint, ask: "What specific action would violate this?"
3. Write each as a single imperative sentence
4. Limit to 8-12 golden rules (focus on highest impact)

**Examples of transformation:**

| Principle/Constraint | Derived Golden Rule |
|---------------------|-------------------|
| P: "API-First Design" | "Design and document API contracts BEFORE implementing business logic" |
| P: "Tenant Isolation" | "NEVER allow a query to return data from multiple tenants" |
| C: "On-premises deployment only" | "DO NOT use cloud-native services (SaaS databases, managed queues, serverless). All infrastructure must be self-hosted." |
| C: "Team of 6 developers" | "AVOID over-engineering. Choose simple, well-documented patterns over clever abstractions." |
| QA: "Security is Critical" | "Every PR MUST pass security review. No exceptions for 'quick fixes'." |

---

## Target 2: architecture-principles.md

### Role

The full principles reference with complete rationale. workspace-rules.md is the summary; this file is the detailed explanation. Developers read this when they need to understand WHY a rule exists.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision | date: {generation-date} -->

# Architecture Principles

## Vision

{Vision statement — verbatim}

## Principles

<!-- begin: AP-sourced -->

### P1: {Principle Name}

**Statement:** {verbatim from AP}

**Rationale:** {verbatim from AP}

**Implications:**
- {Development implication 1}
- {Development implication 2}
- {What this means for code review}

**Violations look like:**
- {Specific anti-pattern that violates this principle}
- {Another violation example}

---

### P2: {Principle Name}

... (repeat for each principle)

<!-- end: AP-sourced -->

## Quality Attributes

<!-- begin: AP-sourced -->

| Priority | Attribute | Target | Measurement |
|:--------:|-----------|--------|-------------|
| Critical | {attribute} | {specific target if stated} | {how to verify} |
| Critical | {attribute} | {target} | {verification} |
| High | {attribute} | {target} | {verification} |
| Medium | {attribute} | {target} | {verification} |
| Low | {attribute} | {target} | {verification} |

<!-- end: AP-sourced -->

## Constraints

<!-- begin: AP-sourced -->

| # | Constraint | Source | Impact on Architecture |
|---|-----------|--------|----------------------|
| C1 | {constraint} | {source} | {impact — verbatim from AP} |
| C2 | ... | ... | ... |

<!-- end: AP-sourced -->

## Stakeholder Concerns

<!-- begin: AP-sourced -->

| Stakeholder | Concern | Architecture Response |
|-------------|---------|---------------------|
| {role} | {concern} | {how architecture addresses it} |
| ... | ... | ... |

<!-- end: AP-sourced -->
```

### Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Principle (full: name, statement, rationale) | Copy verbatim; ADD "Implications" and "Violations" | Full principle block |
| Principle implications | Derive: "What does this mean for a developer day-to-day?" | Implications list |
| Principle violations | Derive: "What would violating this look like in code/design?" | Violations list |
| Quality Attributes table | Copy verbatim; add Measurement column if not present | Quality Attributes table |
| Constraints table | Copy verbatim | Constraints table |
| Stakeholder Concerns mapping | Copy verbatim | Stakeholder Concerns table |

---

## Key Rules for This Mapping

1. **Vision statement is ALWAYS verbatim** — never paraphrase the architect's vision
2. **Principle names and statements are verbatim** — these are formal declarations
3. **Constraints become DON'T rules** — every constraint must produce a clear prohibition
4. **Quality priorities create hierarchy** — Critical > High > Medium > Low; make this explicit
5. **Golden Rules are derived, not copied** — they translate principles into developer actions
6. **workspace-rules.md is concise** — fit on ~2 screens; details go to architecture-principles.md
7. **architecture-principles.md is comprehensive** — full rationale, implications, violation examples
8. **Provenance markers on all AP-sourced sections** — enables reconciliation
9. **NEVER leak planning-workspace concepts into generated content** — The generated workspace serves AI-DLC v1 (building software) + AI-GCE (compliance) + AI-TGE (testing). Content about AI-ILC, AI-PILC, AI-POLC, AI-UXD, AI-PPM, AI-FLO, or their internal mechanisms (`ilc-state.md`, `pilc-state.md`, `polc-state.md`, `uxd-state.md`, idea lifecycles, project initiation, product backlogs, UX design lifecycles, portfolio management, flow routing) must NEVER appear in generated steering files. These concepts belong to the planning workspace. If you find yourself writing about state-driven resumability of *planning packages* or referencing a `*-state.md` file from a planning package as a principle — STOP. That is builder context leaking into developer output. The only `*-state.md` relevant to the dev workspace is `adlc-state.md` (architecture source provenance) and `dwg-state.md` (generation record).
10. **All principles MUST come from the Architecture Vision document (AP)** — never from the AI-* package's own operational design. The Architecture Vision describes how the *target system* should be built, not how the *AI workflow* operates.

---

## Depth Adaptation

| Depth | workspace-rules.md | architecture-principles.md |
|-------|-------------------|---------------------------|
| **Minimal** | Principles table + constraints + 5-8 golden rules | Principles with brief rationale (no violations list) |
| **Standard** | Full structure as defined above | Full structure with implications + violations |
| **Comprehensive** | Full structure + cross-references to every other steering file | Full structure + decision context + trade-off analysis per principle |

---

## Reconciliation Behavior

When Architecture Vision changes (new principle added, constraint modified, quality priority shifted):

1. **New principle added** → Add to both files; derive new golden rule
2. **Principle statement changed** → Update verbatim in both files; review golden rules
3. **Constraint added** → Add DON'T rule to workspace-rules; add to constraints table
4. **Constraint removed** → Flag for user confirmation (constraint removal is significant)
5. **Quality priority changed** → Reorder priority list; flag if Critical attribute changed

**Always preserve team-added content** (anything outside `<!-- begin/end: AP-sourced -->` markers).
