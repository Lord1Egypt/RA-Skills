<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 4: Journey Mapping

## Purpose

Map end-to-end user journeys for each primary persona — capturing stages, actions, touchpoints, emotions, and design opportunities. These journeys are the bridge between "who the user is" (personas) and "how they navigate the product" (flows).

---

## Depth Adaptation

| Depth | Journey Output |
|-------|---------------|
| **Minimal** | 1-2 journeys (primary persona only); core happy path + one error path |
| **Standard** | 1 journey per primary persona + 1 per secondary; includes onboarding journey; error/edge cases per journey |
| **Comprehensive** | Full set + service blueprints (frontstage + backstage) + emotional intensity mapping |

---

## Steps

### Step 1: Identify Journeys to Map

For each primary persona, identify their key journeys:

| Persona | Journey | Type | Priority |
|---------|---------|------|----------|
| {name} | {goal-oriented journey name} | Core / Onboarding / Recovery | High/Medium |

**Journey types:**
- **Core:** The main task they came to accomplish
- **Onboarding:** First-time experience (how they learn the product)
- **Recovery:** What happens when things go wrong (error recovery)
- **Return:** Coming back after absence (re-engagement)

### Step 2: Define Journey Structure

For each journey, define:

```markdown
# Journey: {Persona} — {Goal}

## Metadata
| Field | Value |
|-------|-------|
| Persona | {name} |
| Goal | {what they're trying to achieve} |
| Starting trigger | {what initiates this journey} |
| End state (success) | {what "done" looks like} |
| End state (failure) | {what failure looks like} |
| Estimated duration | {time span} |
| Frequency | {daily/weekly/monthly/one-time} |

## Journey Stages

| # | Stage | Actions | Touchpoint | Emotion | Intensity | Opportunity |
|---|-------|---------|------------|---------|-----------|-------------|
| 1 | {Awareness/Trigger} | {what user does} | {where/how} | 😊/😐/😟 | 1-5 | {design opportunity} |
| 2 | {Consideration} | ... | ... | ... | ... | ... |
| 3 | {Action} | ... | ... | ... | ... | ... |
| 4 | {Completion} | ... | ... | ... | ... | ... |

## Error / Edge-Case Paths

| At Stage | What Goes Wrong | User Reaction | Recovery Path |
|----------|-----------------|---------------|---------------|
| {#} | {failure scenario} | {emotion + action} | {how they recover} |

## Opportunities Summary
1. {Opportunity}: Stage {N} — {brief description of design intervention}
2. ...

## Cross-References
- Persona: {link to persona document}
- Feeds flows: {list of Stage 6 flows this journey will generate}
```

### Step 3: Map Onboarding Journey

Every product needs an explicit onboarding journey (even at Minimal depth):
- How does a new user discover what the product does?
- What's the minimum path to first value ("aha moment")?
- What can be deferred vs. what must be set up immediately?
- How do we avoid overwhelming the user on first visit?

### Step 4: Map Error/Edge-Case Paths

For EACH journey, explicitly map at least one error path:
- What's the most common failure point?
- What does the user see/feel when it fails?
- How do they recover? (The recovery path is a design decision)
- What information do they need to fix the problem?

### Step 5: Service Blueprints (Comprehensive Only)

At Comprehensive depth, extend key journeys into service blueprints:

```markdown
## Service Blueprint: {Journey Name}

| Layer | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|-------|---------|---------|---------|---------|
| **User actions** | {visible} | ... | ... | ... |
| **Frontstage** | {touchpoints} | ... | ... | ... |
| **Line of visibility** | ─────── | ─────── | ─────── | ─────── |
| **Backstage** | {internal processes} | ... | ... | ... |
| **Support processes** | {systems, databases} | ... | ... | ... |
```

### Step 6: Validate and Present

Present all journey maps to the user:
- Are the stages accurate and complete?
- Are the emotions realistic (not assumed positive)?
- Are error paths realistic (not just "everything works")?
- Do opportunities align with business goals?
- Is the onboarding journey realistic for a new user?

---

## Gate

**Approval required before proceeding to Stage 5.**

User must confirm:
- Journey stages are accurate and complete
- Emotional mapping is realistic
- Error paths are identified
- Opportunities are actionable
- Onboarding journey is defined

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 4 with date and artifacts (`03_Journey_Maps/Journey_01_{name}.md`, etc.)
- Current Stage: 5

---

## Transition

After gate approval:
```
Stage 4 complete. {N} journey maps defined and approved.

Moving to Stage 5: Information Architecture. I'll now define how
the product's content and features are organized so users can find
what they need without thinking about it.
```

Load `define/information-architecture.md`.
