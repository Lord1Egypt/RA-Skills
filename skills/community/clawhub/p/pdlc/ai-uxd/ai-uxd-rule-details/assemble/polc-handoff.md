<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 14: AI-POLC Handoff

## Purpose

Package personas and journey maps for AI-POLC consumption. AI-POLC uses these for product prioritization — personas inform "who we're building for" and journeys inform "what they need most." This is a producer→consumer handoff.

---

## MANDATORY: Stage Sub-Role — Product Manager

During this stage, layer the Product Manager lens on top of the UX Designer primary:

**Behavioral Shifts:**
- Think about what AI-POLC needs to DO with these artifacts (prioritize, scope, write stories)
- Ensure personas translate into prioritization inputs (not just empathy artifacts)
- Verify that journeys highlight value-delivery opportunities (not just experience mapping)
- Frame handoff in terms of product decisions it enables

**Anti-Patterns for This Stage:**
- DO NOT hand off raw UX artifacts without consumption guidance — AI-POLC isn't a designer
- DO NOT assume AI-POLC will interpret emotional mapping — translate into opportunity language
- DO NOT include design-system details in this handoff — AI-POLC doesn't need tokens/components

**Quality Check:**
- [ ] Every persona has clear prioritization signals (goals that can be ranked)
- [ ] Journey opportunities are framed as "value to deliver" not "screen to build"
- [ ] Handoff package is self-contained (AI-POLC doesn't need to read other UXP files)

---

## Steps

### Step 1: Prepare Persona Package for AI-POLC

From the full persona documents (Stage 3), extract what AI-POLC needs:

```markdown
## Persona Handoff: {Name}

### For Prioritization
| Field | Value |
|-------|-------|
| Priority | Primary / Secondary / Tertiary |
| Primary JTBD | "When {situation}, I want to {action}, so I can {outcome}" |
| Top goal | {outcome-oriented goal #1} |
| Biggest pain point | {what frustrates them most today} |
| Value sensitivity | {what they value most: speed / accuracy / simplicity / control} |
| Usage frequency | {daily / weekly / monthly} |

### Segment Sizing (if known)
| Metric | Value |
|--------|-------|
| Estimated % of user base | {percentage} |
| Revenue contribution | {if known} |
| Strategic importance | {High/Medium/Low + why} |
```

### Step 2: Prepare Journey Package for AI-POLC

From journey maps (Stage 4), extract opportunity-focused content:

```markdown
## Journey Handoff: {Persona} — {Goal}

### Opportunity Map (for backlog prioritization)
| Journey Stage | Emotion | Opportunity | Value if Addressed | JTBD Link |
|---------------|---------|-------------|-------------------|-----------|
| {stage name} | 😟 (3/5) | {what could be better} | {user + business value} | {JTBD ref} |
| {stage name} | 😐 (2/5) | {what could be better} | {value} | {JTBD ref} |

### Critical Path (minimum viable journey)
{The shortest path through this journey that delivers the core value.
This informs MVP/MMP decisions in AI-POLC.}

### Pain-to-Story Mapping Suggestions
| Pain Point | Possible Epic/Story Direction | Priority Signal |
|-----------|------------------------------|-----------------|
| {pain from journey} | {how a product feature could address it} | {High/Medium/Low} |
```

### Step 3: Produce Handoff Summary

```markdown
## AI-POLC Consumption Guide

### What You're Receiving
- {N} personas with prioritization metadata
- {N} journey opportunity maps with value indicators
- Critical path definitions (for MVP scoping)
- Pain-to-story mapping suggestions (for backlog seeding)

### How to Use This
1. **For backlog prioritization:** Use persona priority + opportunity value to rank
2. **For story writing:** Each opportunity is a candidate epic; pain points are story seeds
3. **For acceptance criteria:** Journey success states define "done" from user perspective
4. **For release slicing:** Critical path = MVP; remaining opportunities = subsequent releases

### What You Own vs. What AI-UXD Owns
| AI-UXD Owns | AI-POLC Owns |
|-------------|-------------|
| WHO the users are (personas) | WHAT to build for them (backlog) |
| WHAT they experience (journeys) | WHY in this order (prioritization) |
| WHERE opportunities exist | WHEN to deliver (release slicing) |
| User NEEDS | Product DECISIONS about those needs |

### Ongoing Exchange (bidirectional, same-layer — no AI-FLO)

AI-UXD and AI-POLC are both Project-layer, so the exchange is **direct marker reads in both directions**:

| Direction | What flows | Where it's wired |
|-----------|-----------|------------------|
| **AI-UXD → AI-POLC** (this handoff) | Personas + journey opportunity maps + critical path + pain-to-story seeds | This stage (Stage 14) → AI-POLC reads `uxd-state.md` |
| **AI-POLC → AI-UXD** (inbound) | Value goals / OKRs / target outcomes / success metrics → **focus UX research** | AI-UXD `discover/workspace-detection.md` (peer read of `polc-state.md`) + `discover/research-planning.md` (focuses research questions) |

- This is genuinely **bidirectional**: producer→consumer for artifacts (UXD→POLC), consumer→producer for direction (POLC→UXD).
- Both halves are **wired**, not just declared (the inbound POLC→UXD read happens at Discover, this outbound UXD→POLC handoff happens here).
- If either peer marker is absent, the present package proceeds standalone.
```

### Step 4: Update State File

Update `uxd-state.md`:
- Downstream Signals → AI-POLC: "Handed Off"
- Note handoff path and artifact list

### Step 5: Present for Approval

Present:
- Handoff package contents (persona summaries + journey opportunities)
- Consumption guide (clear enough for AI-POLC to act on?)
- Any gaps (personas/journeys that AI-POLC might find insufficient)

---

## Gate

**Approval required before proceeding to Stage 15.**

User must confirm:
- Handoff content is sufficient for product prioritization
- Opportunity framing is clear and actionable
- Consumption guide makes sense
- Nothing critical is missing for AI-POLC's needs

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 14 with date
- Downstream Signals: AI-POLC = "Handed Off"
- Current Stage: 15

---

## Transition

After gate approval:
```
Stage 14 complete. Personas and journeys handed off to AI-POLC.

Moving to Stage 15: AI-DWG / AI-GCE Handoff. I'll now package the
design system, tokens, and accessibility baseline for workspace
generation and compliance enforcement.
```

Load `assemble/dwg-gce-handoff.md`.
