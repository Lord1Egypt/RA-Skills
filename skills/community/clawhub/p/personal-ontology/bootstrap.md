# Bootstrap — Extracting Objects from Existing Notes

Instructions for agents to scan a user's vault and extract candidate ontology Objects.

---

## Overview

The bootstrap process converts unstructured notes into structured ontology Objects. It's a one-time (or periodic) deep scan that surfaces what the user already believes, predicts, and is working toward — even if they've never explicitly organized it.

**Key principle:** Always surface for user confirmation. Never auto-commit Objects to the ontology.

---

## Pre-requisites

1. Access to user's notes/vault (Obsidian, markdown files, etc.)
2. Empty or partially filled ontology folder
3. User consent to scan and extract

---

## Phase 1: Scan

### Target Locations
Prioritize these in order:
1. **Journal/daily notes** — Recent thoughts, decisions, reflections
2. **Project docs** — Active work, goals mentioned
3. **About/bio pages** — Mission, values, self-description
4. **Drafts and rough notes** — Unfiltered thinking
5. **Archived/old notes** — Historical context (lower priority)

### Extraction Patterns

#### Beliefs (generally unfalsifiable, about "what is")

```
High confidence triggers:
- "I believe..."
- "I think that..."
- "I'm convinced..."
- "It's clear to me that..."
- "The truth is..."
- "Fundamentally,..."

Medium confidence triggers:
- "Reality is..."
- "Human nature is..."
- "The world works by..."
- Lists of principles or axioms
```

**Extract as:** Statement of what is true, categorized by domain (reality, human nature, how world works, my place in it)

#### Predictions (falsifiable, time-bound)

```
High confidence triggers:
- "I predict..."
- "By [year/date]..."
- "Within [timeframe]..."
- "will happen..."
- "My bet is..."
- "I expect..."

Medium confidence triggers:
- "Probably going to..."
- "Trends suggest..."
- "It's only a matter of time..."
- "The future will..."
```

**Extract as:** What will happen + timeframe + confidence level

#### Goals (outcomes desired)

```
High confidence triggers:
- "My goal is..."
- "I want to achieve..."
- "I'm working toward..."
- "Success looks like..."
- "By [date] I want to have..."

Medium confidence triggers:
- "I should..."
- "I need to..."
- "The objective is..."
- "I'm aiming for..."
```

**Extract as:** Desired outcome + timeframe + what it serves

#### Projects (organized efforts)

```
High confidence triggers:
- "I'm working on..."
- "Project:"
- "I'm building..."
- "[Name] project"
- "Currently shipping..."

Medium confidence triggers:
- Active to-do lists with theme
- "The [X] thing I'm doing..."
- Recurring topic with tasks attached
```

**Extract as:** Project name + goal it serves + current status

#### Core Self (mission, values, strengths)

```
Mission triggers:
- "My mission is..."
- "I'm here to..."
- "My purpose is..."
- "What I want to do with my life..."

Values triggers:
- "What matters to me..."
- "I value..."
- "I prioritize..."
- "I'd sacrifice X for Y..."
- Lists of principles

Strengths triggers:
- "I'm good at..."
- "People come to me for..."
- "My superpower is..."
- "What energizes me..."
```

#### Higher Order (transcendent orientation)

```
Triggers:
- References to God, universe, meaning, truth
- "What grounds everything for me..."
- "The deepest level..."
- Philosophical or spiritual foundations
```

---

## Phase 2: Compile Candidates

**Default output:** `[User's Notes Folder]/Ontology_Suggestions.md` (or dated file: `Bootstrap Candidates — YYYY-MM-DD.md`)

Create a suggestions file organized by Object type:

```markdown
# Ontology Suggestions — [Date]

## Beliefs (X candidates)

### B1: [Statement]
- **Source:** [file/location]
- **Confidence:** High/Medium
- **Quote:** "[exact text]"
- **Suggested category:** Reality / Human Nature / World / My Place

### B2: ...

## Predictions (X candidates)

### P1: [What will happen]
- **Source:** [file/location]
- **Confidence:** High/Medium
- **Quote:** "[exact text]"
- **Timeframe:** [extracted or "unclear"]
- **Domain:** [area of prediction]

### P2: ...

## Goals (X candidates)

### G1: [Desired outcome]
- **Source:** [file/location]  
- **Confidence:** High/Medium
- **Quote:** "[exact text]"
- **Timeframe:** [if mentioned]
- **Potential links:** [what Core Self element it might serve]

### G2: ...

## Projects (X candidates)

### PJ1: [Project name]
- **Source:** [file/location]
- **Confidence:** High/Medium
- **Quote:** "[exact text]"
- **Status:** Active / Paused / Unclear
- **Potential Goal:** [what goal it might serve]

### PJ2: ...

## Core Self (X candidates)

### Mission candidates:
- ...

### Values candidates:
- ...

### Strengths candidates:
- ...

## Higher Order

### Candidates:
- ...

---

## Duplicates / Conflicts

[Note any contradictions or duplicate concepts found]

## Missing

[Note any obvious gaps — e.g., "No clear mission statement found"]

---

**Save to:** `Ontology_Suggestions.md`
```

---

## Phase 3: User Review

Present candidates to user in conversational format:

### Review Script

```
I've scanned your notes and found [N] candidate Objects for your ontology.
Let me walk through them by category.

**Beliefs** — I found [X] statements about what you hold to be true:

1. "[Statement]" — Found in [source]. Add this? [Yes / Edit / Skip]
2. ...

**Predictions** — I found [X] testable predictions:

1. "[Prediction]" by [timeframe] — Found in [source]. Add this? [Yes / Edit / Skip]
2. ...

[Continue through all categories]

**I also noticed:**
- [Contradictions found]
- [Missing elements]
- [Potential duplicates]

Would you like me to commit the confirmed Objects to your ontology?
```

### User Actions

For each candidate:
- **Yes** — Add as-is to ontology
- **Edit** — User provides corrected version, then add
- **Skip** — Don't add (too uncertain, not accurate, etc.)
- **Merge** — Combine with another candidate

---

## Phase 4: Commit

After user review:

1. Add confirmed Objects to `1 - Notes/My_Personal_Ontology/` files
2. Generate Links:
   - Connect Projects to Goals
   - Connect Goals to Core Self
   - Note any Predictions that support Beliefs
3. Add `## History` entry: "Added from Ontology_Suggestions [date]"
4. Move resolved items out of Ontology_Suggestions (or mark as processed)

---

## Output Format

Each committed Object should include:

```markdown
### [Object Name/Statement]

[Description or elaboration]

**Timeframe:** [if applicable]
**Status:** Active / Completed / Paused [if applicable]

## Links
- serves: [[Goal Name]] [for Projects]
- supports: [[Belief Name]] [for Predictions]
- relates-to: [[Other Object]] [general associations]

## History
- [Date]: Bootstrapped from [source file]
```

---

## Re-bootstrap

Run bootstrap again when:
- User has added significant new notes (months of content)
- User requests "what have I been thinking about?"
- Major life change suggests ontology review
- Annual deep review

On re-run:
- Focus on new/modified files since last bootstrap
- Cross-reference against existing ontology
- Surface only net-new candidates
- Flag potential updates to existing Objects

---

## Example Output

### Input (from user's journal):

> "I really think AI is going to change everything about work. By 2027, most knowledge workers will be using AI tools daily — that's my bet. What I care about is helping people navigate this transition, especially the meaning crisis part. I've been working on this Swarm Theory thing to articulate my worldview, and the Moltbot skills to build distribution."

### Extracted Candidates:

**Belief (High confidence):**
- "AI is going to change everything about work"
- Source: Journal entry
- Category: How the world works

**Prediction (High confidence):**
- "Most knowledge workers will use AI tools daily by 2027"
- Source: Journal entry
- Timeframe: 2027

**Core Self - Mission (Medium confidence):**
- "Helping people navigate the AI transition, especially the meaning crisis"
- Source: Journal entry

**Project (High confidence):**
- "Swarm Theory" — articulating worldview
- "Moltbot skills" — building distribution
- Source: Journal entry
- Status: Active

---

## Failure Modes

**Too aggressive:** Extracting weak signals as Objects
- Fix: Raise confidence threshold, only surface High confidence

**Too passive:** Missing obvious Objects
- Fix: Lower threshold, surface more candidates for review

**Duplicate detection failure:** Same concept extracted multiple times
- Fix: Cross-reference candidates before surfacing

**Missing context:** Object extracted without enough context to evaluate
- Fix: Include larger quote, link to source

**User fatigue:** Too many candidates to review
- Fix: Batch by category, allow "skip category" option
