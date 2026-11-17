<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 3: Persona Definition

## Purpose

Transform research synthesis into evidence-backed personas — behavioral archetypes that represent user segments. These personas are the foundation of every downstream design decision and flow to AI-POLC for product prioritization.

---

## Depth Adaptation

| Depth | Persona Output |
|-------|---------------|
| **Minimal** | 2-3 personas; core structure only (goals, pain points, context) |
| **Standard** | 3-5 personas; full structure including JTBD, scenarios, and accessibility considerations |
| **Comprehensive** | 5-8 personas; full structure + empathy maps per persona + inclusion personas (users with disabilities) |

---

## Steps

### Step 1: Map Segments to Personas

From the research synthesis (Stage 2), map each confirmed user segment to a persona:

| Segment | Persona Name | Priority | Justification |
|---------|-------------|----------|---------------|
| {segment from research} | {human name + role} | Primary / Secondary / Tertiary | {why this priority} |

**Naming rules:**
- Give each persona a realistic human name (makes them memorable)
- Add their role/context: "Sarah, Healthcare Administrator" not just "Sarah"
- Primary personas = most design decisions serve them first
- Secondary = served where possible without compromising primary
- Tertiary = aware of, design doesn't harm them

### Step 2: Build Persona Structure

For each persona, produce:

```markdown
# Persona: {Name}, {Role/Context}

## Quick Reference
| Field | Value |
|-------|-------|
| Priority | Primary / Secondary / Tertiary |
| Segment | {from research} |
| Age Range | {range, not exact — avoids demographic stereotyping} |
| Tech Comfort | Low / Medium / High |
| Access Context | {device, environment, time pressure} |

## Goals (Outcomes, Not Features)
1. {Outcome-oriented goal: "Complete patient intake in under 5 minutes"}
2. {Goal 2}
3. {Goal 3 — minimum 2, maximum 5}

## Pain Points
1. {Current frustration: what blocks them today}
2. {Pain point 2}
3. {Pain point 3 — minimum 2}

## Behaviors & Patterns
- {How they currently approach the task}
- {Tools they use today}
- {Workarounds they've developed}
- {Information-seeking behavior}

## Jobs-to-be-Done
> "When {situation/trigger}, I want to {motivation/action}, so I can {expected outcome}."

### Primary JTBD:
When {situation}, I want to {action}, so I can {outcome}.

### Secondary JTBD:
When {situation}, I want to {action}, so I can {outcome}.

## Scenarios (Key Usage Situations)
1. **{Scenario name}:** {Brief narrative of a typical usage situation}
2. **{Scenario name}:** {Another situation — ideally includes an edge case}

## Accessibility Considerations
- {Any access needs: screen reader user, motor impairment, low vision, cognitive load sensitivity}
- {If none identified: "No specific access needs identified for this segment — universal accessibility baseline applies"}

## Quoted Need
> "{A statement this persona would say that captures their core frustration or desire}"
```

### Step 3: Empathy Maps (Comprehensive Depth Only)

For each primary persona at Comprehensive depth, produce an empathy map:

```markdown
## Empathy Map: {Persona Name}

### Thinks
- {What occupies their mind during the task}
- {Concerns, calculations, planning}

### Feels
- {Emotional state during the experience}
- {Frustrations, anxieties, satisfactions}

### Says
- {Actual quotes or paraphrases from research}
- {How they describe their experience to others}

### Does
- {Observable behaviors and actions}
- {Workarounds, shortcuts, help-seeking}

### Key Insight
{One sentence that captures the empathy map's core revelation}
```

### Step 4: Inclusion Personas (Comprehensive Depth)

At Comprehensive depth, define at least one inclusion persona representing users with disabilities:

- A screen reader user (blind or low vision)
- A keyboard-only user (motor impairment)
- A user with cognitive/attention constraints
- A user in a challenging context (noisy, bright, one-handed)

These ensure accessibility is designed FOR someone, not just checked against criteria.

### Step 5: Validate and Present

Present all personas to the user:
- Confirm behavioral accuracy (do these ring true?)
- Confirm priority ordering
- Check for missing segments (is anyone important not represented?)
- Verify JTBD framing captures the right motivation

---

## Gate

**Approval required before proceeding to Stage 4.**

User must confirm:
- Personas accurately represent the user base
- Priority ordering is correct
- JTBD statements capture the right motivations
- No critical user segment is missing
- Accessibility considerations are noted where relevant

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 3 with date and artifacts (`02_Personas/Persona_01_{Name}.md`, etc.)
- Current Stage: 4

---

## Transition

After gate approval:
```
Stage 3 complete. {N} personas defined and approved.

Moving to Stage 4: Journey Mapping. I'll now map how each primary
persona moves through the product experience — identifying touchpoints,
emotions, and design opportunities along the way.
```

Load `define/journey-mapping.md`.
