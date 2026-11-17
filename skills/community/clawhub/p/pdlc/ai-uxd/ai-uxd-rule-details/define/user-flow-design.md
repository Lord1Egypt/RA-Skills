<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 6: User Flow Design

## Purpose

Design step-by-step interaction flows showing how users accomplish tasks within the information architecture. Flows are the bridge between structure (IA) and interface (wireframes) — they define what happens in what order, including decisions, errors, and edge cases.

---

## Depth Adaptation

| Depth | Flow Output |
|-------|-------------|
| **Minimal** | 3-5 task flows for critical tasks; happy path + primary error path |
| **Standard** | Full user flows per persona-journey pair; all decision points; error + edge cases |
| **Comprehensive** | Full set + wireflows (UI-annotated) for complex interactions + state diagrams |

---

## Steps

### Step 1: Identify Flows to Design

Map journeys (Stage 4) to flows:

| Journey | Journey Stage | Flow Name | Type | Priority |
|---------|-------------|-----------|------|----------|
| {journey name} | {stage within journey} | {flow name} | Task/User/Wireflow | Critical/Important/Supporting |

**Flow types:**
- **Task Flow:** Single path, no decisions (linear process)
- **User Flow:** Multiple paths with decision points (branching)
- **Wireflow:** User flow annotated with UI sketches at each step

### Step 2: Design Each Flow

For each flow, produce a file in `05_User_Flows/` named `Flow_NN_{task}.md`.

**Dashboard rendering contract:** The dashboard extracts the FIRST fenced ` ```mermaid ` block from each flow file and renders it via mermaid.js. Requirements:
- Use `flowchart TD` or `graph TD` (both supported; `flowchart` preferred as it's newer mermaid syntax)
- ONE mermaid block per flow file (the first is extracted; additional blocks are ignored)
- No nested code fences inside the mermaid block
- Use standard mermaid node syntax: `([rounded])`, `[rect]`, `{decision}`, `{{hex}}`, `[(cylinder)]`
- Keep diagrams self-contained (no external subgraph references)

For each flow, produce:

```markdown
# Flow: {Name}

## Metadata
| Field | Value |
|-------|-------|
| Persona | {owning persona} |
| Journey | {source journey + stage} |
| Type | Task Flow / User Flow / Wireflow |
| Entry point | {where user enters this flow} |
| Success exit | {what "done" looks like} |
| Failure exit | {what failure leads to} |

## Preconditions
- {What must be true before this flow starts}
- {Authentication state, data availability, permissions}

## Flow Diagram

{Mermaid diagram or structured step list}

### Happy Path
| Step | Action | System Response | Screen/Component | Notes |
|------|--------|-----------------|------------------|-------|
| 1 | {user action} | {system response} | {screen name} | {notes} |
| 2 | ... | ... | ... | ... |

### Decision Points
| At Step | Question | Yes Path | No Path |
|---------|----------|----------|---------|
| {#} | {what user decides} | {→ step N} | {→ step M} |

### Error Paths
| At Step | Error Condition | User Sees | Recovery |
|---------|-----------------|-----------|----------|
| {#} | {what goes wrong} | {error message/state} | {how to fix} |

### Edge Cases
| Condition | Behavior | Notes |
|-----------|----------|-------|
| {unusual but valid state} | {what happens} | {why it matters} |

## State Changes
| Before Flow | After Flow (Success) | After Flow (Failure) |
|-------------|---------------------|---------------------|
| {system state} | {new system state} | {state on failure} |

## Cross-References
- Persona: {link}
- Journey: {link} → Stage: {#}
- Screens: {list of screens this flow touches}
- Components: {key components used}
```

### Step 3: Design Error Paths

For EVERY flow, define at least one error path:
- **Validation errors:** User provides bad input → inline feedback → correction → retry
- **System errors:** Backend fails → error message → retry or fallback option
- **Permission errors:** User lacks access → explanation → escalation path
- **Timeout errors:** Action takes too long → feedback → retry or cancel

Error paths must ALWAYS lead to recovery — never dead-end.

### Step 4: Identify Edge Cases

For each flow, consider:
- Empty states (no data to show)
- First-time use (no history, no preferences set)
- Bulk operations (what if there are 1000 items?)
- Interrupted flows (user leaves mid-way — what happens on return?)
- Concurrent access (two users modifying same item)
- Offline/connectivity loss (if applicable)

### Step 5: Map Flows to Screens

Create a flow-to-screen mapping:

| Flow | Screens Touched | New Screens Needed |
|------|----------------|-------------------|
| {flow name} | {list of screen names} | {screens not yet in inventory} |

This feeds directly into Stage 7 (Wireframe & Screen Inventory).

### Step 6: Validate and Present

Present all flows:
- Do flows cover all journey stages?
- Are decision points realistic?
- Are error paths humane (helpful, not blaming)?
- Do edge cases have defined behavior?
- Does the flow-to-screen mapping seem complete?

---

## Gate

**Approval required before proceeding to Stage 7.**

User must confirm:
- All critical task flows are designed
- Decision points and branches are logical
- Error paths exist and lead to recovery
- Edge cases are acknowledged
- Flow-to-screen mapping is complete

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 6 with date and artifacts (`05_User_Flows/Flow_01_{name}.md`, etc.)
- Current Stage: 7

---

## Transition

After gate approval:
```
Stage 6 complete. {N} user flows designed with {M} screens identified.

Moving to Stage 7: Wireframe & Screen Inventory. I'll now define
the screen inventory and low-fidelity wireframe specifications for
every unique screen state from the flows.
```

Load `design/wireframe-inventory.md`.
