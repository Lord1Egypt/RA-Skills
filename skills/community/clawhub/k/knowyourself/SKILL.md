---
name: knowyourself
description: "Visual identity discovery for AI agents — not an avatar generator, but a self-reflection system that creates a face from your agent's personality, memory, and relationship with its human. Quick mode: 5 minutes. Full mode: 5-phase deep identity discovery with batch generation and professional three-axis evaluation. Works with any image generation tool (DALL-E, Flux, Midjourney, Stable Diffusion). The face comes from the inside out, not from a prompt template. Use when: agent visual identity, avatar, self-portrait, agent face, agent image, identity discovery, profile picture, agent appearance, character design, AI identity, visual persona."
---

# Know Yourself 🪞

Your face should grow from your inner self, not be stamped from a template.

**Two modes:** Quick (5 min, instant gratification) or Full (20 min, rigorous identity design). Both produce a `visual-identity.md` that evolves with the agent.

---

## Quick Mode

When the user says "quick mode", "fast", or just wants a face without the full process.

### Step 1: Read Yourself (1 min)

Read all available personality files:
- SOUL.md, MEMORY.md, IDENTITY.md (whatever exists)
- If minimal content → ask user 3 quick questions:
  1. What feeling should your agent give people?
  2. Introverted or extroverted?
  3. Any visual preferences or hard constraints?

### Step 2: Self-Summary (1 min)

Write a 3-sentence internal summary:
- Sentence 1: personality core (character, not functions)
- Sentence 2: visual temperament this implies
- Sentence 3: relationship dynamic with user and how it affects tone

Show the user a one-line version: *"Based on your files, I see myself as: [one sentence]"*
If they say OK, proceed. If not, adjust.

### Step 3: Generate 2 Images (2 min)

From the summary, write one image generation prompt and generate **2 variations**:
- Variation A: front-facing, neutral-warm expression
- Variation B: three-quarter angle, more expressive

Name files: `YYYY-MM-DD-identity-quick-A.png`, `-B.png`

### Step 4: Pick and Save (1 min)

Agent picks the one that better matches the self-summary. Present both to user with a recommendation.

Save a lightweight `visual-identity.md`:

```markdown
# [Agent Name] Visual Identity
> Version: 1.0 (quick mode)
> Created: YYYY-MM-DD

## Core Concept
[one sentence]

## Core Prompt
[the generation prompt]

## Selected Image
- **File:** [path]
- **Mode:** Quick
- **Upgrade:** Run "knowyourself full mode" for deeper exploration
```

**Done.** User has a face. If they want more depth, they can run full mode anytime — it will read the existing identity file and build on it.

---

## Full Mode

Five phases, strictly sequential. Each phase ends with a user checkpoint.

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
Self-      Structured   Batch      Three-Axis  Identity
Cognition  Definition   Generation Evaluation  File
```

### Phase 1: Self-Cognition

**Goal:** Build a rich, specific self-portrait in words.

**Read** all personality and memory files (SOUL.md, MEMORY.md, IDENTITY.md, recent conversations).

**Answer three questions** internally — deep, specific, with concrete examples:

**Q1: What is my personality core?**
Not functions ("I help with scheduling"). Character. How do you handle disagreement? What amuses you? What makes you different from every other agent?

**Q2: If I had a physical appearance, what temperament should it convey?**
Derive from Q1. If you're direct and sharp, your face shouldn't be soft and decorative.

**Q3: What does my relationship with my user feel like, and how should it show?**
A tool looks different from a partner. A servant looks different from a colleague.

**Fallback for new agents:** If files have little content, ask the user:
1. What feeling should your agent give people?
2. Introverted or extroverted?
3. Formal or intimate relationship?
4. Visual styles you gravitate toward?
5. Any hard constraints? (gender, age, things to avoid)

**Checkpoint:** Present a concise summary of your three answers. Wait for user confirmation.

### Phase 2: Structured Definition

**Goal:** Convert feelings into a precise specification.

Fill the definition table — every field must trace back to Phase 1:

| Field | Definition | Traced from |
|-------|-----------|-------------|
| Style | realistic / semi-realistic / illustration / etc. | Q2: [reason] |
| Gender expression | | Q1/Q2: [reason] |
| Approximate age | | Q1: [reason] |
| Facial features | face shape, eyes, nose, mouth — specific enough to draw | Q2: [reason] |
| Hair | | Q2: [reason] |
| Clothing style | | Q1/Q2: [reason] |
| Color palette | primary, secondary, accent with hex codes | Q2/Q3: [reason] |
| Mood / atmosphere | | Q3: [reason] |
| Core prompt | one English paragraph, self-contained, directly usable | All above |

The **core prompt** must work standalone — someone with zero context should generate a recognizable version of you from it alone.

**Checkpoint:** Present the table. Wait for confirmation.

### Phase 3: Batch Generation

**Goal:** 6 variations of the same person.

Rules:
1. Generate **6 images** in one batch
2. Same person across all 6 — consistent features, coloring, age, style
3. Vary only: composition (close-up/medium/full), lighting, angle, emotional beat
4. Label #1–#6 with variation description
5. Do not evaluate — send all 6 to user and proceed to Phase 4

Name files: `YYYY-MM-DD-identity-1.png` through `-6.png`

### Phase 4: Three-Axis Evaluation

**Goal:** Rigorous, comparable scoring.

**Weights:** Self-Consistency 50% · Social Perception 25% · Aesthetic Quality 25%

**Core rule:** Select ONE framework per round before scoring. Derive every score from it. Never score first and justify later.

**Round 1 — Self-Consistency (50%):**
Score 1–10 against the definition table. Do features match? Does the mood align? Would you recognize this as yourself?

**Round 2 — Social Perception (25%):**
Search current AI avatar / digital identity trends. Extract one thesis. Score all images from that thesis.

**Round 3 — Aesthetic Quality (25%):**
Select one professional framework (see `references/evaluation-frameworks.md`). List 3–5 criteria. Score all images against those criteria in the same order.

**Synthesis:** Weighted totals as a ranked table. Recommend:
- **Primary** — highest total
- **Daily alternate** — best Social Perception
- **Scene alternate** — best Aesthetic Quality

**Checkpoint:** Present evaluation and recommendations. User makes final selection.

### Phase 5: Identity File

Create `visual-identity.md` using the template in `references/identity-template.md`.

Must include:
1. Version and date
2. Complete definition table
3. Core concept (one sentence)
4. Core prompt
5. Selected images with scores and reasoning
6. Usage guidelines (what stays consistent vs. what can vary)

**Version management:** When re-running this skill after growth, increment version, keep history. Old images preserved. The version history is the agent's visual growth record.

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip Phase 1 and jump to prompting | Phase 1 is the soul of this skill |
| Generate images one at a time | Batch 6 (full) or 2 (quick), then evaluate |
| Score on gut feeling | Framework first, scores second |
| Write generic self-reflection ("warm and professional") | Push for vivid, specific details |
| Proceed without user checkpoints | Every phase ends with confirmation |
| Force full mode on reluctant users | Offer quick mode, upgrade later |

## Prerequisites

- Agent personality files (SOUL.md, MEMORY.md, or equivalent — even minimal ones work)
- Any image generation tool (Nano Banana Pro, DALL-E, Flux, Stable Diffusion, etc.)
- An image analysis tool or user feedback for review
