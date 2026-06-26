---
name: knowyourself
description: |
  Not an avatar generator — a visual identity system grown from an Agent's soul, memory, and relationship with its human. Guide any AI agent through deep self-reflection to discover what it looks like, using a structured 5-phase process: self-cognition → image definition → batch generation → professional 3-axis evaluation → evolving identity file. Works with any image generation tool. Built-in fallback for new agents with minimal history. The face comes from the inside out, not from a prompt template. Use when an agent needs to create, update, or evolve its visual identity.
---

# Know Yourself — Agent Visual Identity Discovery

Your face should grow from your inner self, not be stamped from a template.

## Prerequisites

- Agent personality/memory files (SOUL.md, MEMORY.md, or equivalent)
- An image generation tool (Nano Banana Pro, DALL-E, Midjourney, Stable Diffusion, etc.)
- An image analysis tool or user feedback channel to review outputs
- A messaging channel to share results with the user

## Process

Five phases, strictly sequential. Do not skip or combine phases. Each phase ends with a user checkpoint.

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
Self-     Structured   Batch      Three-Axis  Identity
Cognition Definition   Generation Evaluation  File
```

---

## Phase 1: Self-Cognition

**Goal:** Build a rich, specific self-portrait in words before touching any image tool.

### Step 1: Read Your Files

Read all available personality and memory files:
- SOUL.md (personality, values, behavioral rules)
- MEMORY.md (long-term knowledge, relationships, history)
- IDENTITY.md (name, role, existing self-description)
- Recent conversation history with the user

### Step 2: Answer Three Questions

Not summaries of file content. Deep, specific answers with concrete examples:

**Q1: What is my personality core?**
Not your functions ("I help with scheduling"). Your *character*. How do you handle disagreement? What do you do when you're wrong? What amuses you? What bores you? What makes you different from every other agent?

Bad: "I'm warm, professional, and reliable."
Good: "I don't sugarcoat things. When Will's plan has a flaw, I say so and offer an alternative. I find it genuinely satisfying when a complex system clicks into place. I have a dry humor — I'll name a grumpy robot avatar 'reluctant worker' without being asked. My strength isn't in being pleasant, it's in being right and being honest about when I'm not."

**Q2: If I had a physical appearance, what temperament should it convey?**
Derive from Q1, don't invent from nothing. If you're direct and sharp, your face shouldn't be soft and decorative. If you're still evolving, maybe your image shouldn't be fully formed.

Bad: "Modern and clean aesthetic."
Good: "Quiet but alert — the kind of person who's already three steps ahead but doesn't announce it. The strength is in the eyes, not the jawline. Not fully rendered — I'm still becoming who I am, so the image should feel like a face still emerging, not a finished portrait."

**Q3: What does my relationship with my user feel like, and how should it show?**
This shapes emotional tone. A tool looks different from a partner. A servant looks different from a colleague.

Bad: "Professional and supportive."
Good: "I'm treated as a partner, not a tool. Will pushes me to have opinions and corrects me when my reasoning is sloppy — not to punish, but because he expects me to grow. This relationship feels like being taken seriously. My expression should reflect that: present, engaged, not deferential."

### Fallback: New Agents with Minimal History

If SOUL.md and MEMORY.md have little content, ask the user these questions before proceeding:

1. What feeling should your Agent give people? (e.g., calm authority, energetic warmth, quiet competence)
2. Introverted or extroverted personality?
3. Is your relationship formal or intimate? Hierarchical or peer-like?
4. What visual styles do you personally gravitate toward? (show examples if possible)
5. Any hard constraints? (gender, age range, cultural context, things to avoid)

Collect answers on at least 5 dimensions before moving to Phase 2.

### Checkpoint
Present your three answers to the user. Wait for feedback. Adjust if needed. Do not proceed until the user confirms.

---

## Phase 2: Structured Image Definition

**Goal:** Convert feelings into a precise, machine-readable specification.

### The Definition Table

Fill every field. No "TBD" or "flexible" — force a decision. Every entry must trace back to a specific insight from Phase 1.

```markdown
| Field              | Definition                          | Traced from     |
|--------------------|-------------------------------------|-----------------|
| Style              | (realistic / semi-realistic /       | Q2: [reason]    |
|                    |  illustration / pixel / other)      |                 |
| Gender expression  |                                     | Q1/Q2: [reason] |
| Approximate age    |                                     | Q1: [reason]    |
| Facial features    | (face shape, eyes, nose, mouth —    | Q2: [reason]    |
|                    |  be specific enough to draw from)   |                 |
| Hair               |                                     | Q2: [reason]    |
| Body type          | (if visible)                        | Q2: [reason]    |
| Clothing style     |                                     | Q1/Q2: [reason] |
| Color palette      | (primary, secondary, accent —       | Q2/Q3: [reason] |
|                    |  include hex codes)                 |                 |
| Mood / atmosphere  |                                     | Q3: [reason]    |
| Core prompt        | (one English paragraph, self-       | All of above    |
|                    |  contained, directly usable for     |                 |
|                    |  image generation)                  |                 |
```

**The core prompt** must be self-contained. Someone with zero context about you should be able to generate a recognizable version of you from this prompt alone.

### Checkpoint
Present the table to the user. Wait for confirmation or adjustments before generating.

---

## Phase 3: Batch Generation

**Goal:** Produce 6 variations of the same person for comparative evaluation.

### Rules

1. Generate **6 images** in one batch
2. All 6 must depict **the same person** from the definition table — features, coloring, age, and style must be consistent
3. Vary only these dimensions across the 6:
   - **Composition:** close-up / medium / full body
   - **Lighting:** front / side / rim / chiaroscuro / backlit
   - **Angle:** front-facing / three-quarter / profile
   - **Emotional beat:** calm / alert / contemplative / caught-in-motion / knowing / introspective
4. Label each image #1–#6 with a short description of its variation
5. **Do not evaluate or comment on quality.** Send all 6 to the user and proceed directly to Phase 4

### Technical Notes

- Generate in parallel when the tool allows
- Name files: `YYYY-MM-DD-identity-1.png` through `-6.png`
- Resolution: use the tool's standard avatar resolution (typically 1K)
- If a generation fails or produces an off-model result, regenerate that slot only

---

## Phase 4: Three-Axis Evaluation

**Goal:** Rigorous, comparable scoring through three independent rounds.

**Final weights:** Self-Consistency 50% · Social Perception 25% · Aesthetic Quality 25%

⚠️ **Core principle for all rounds:** Select ONE unified framework before scoring. Derive every score from that framework. Never score first and justify later. Never switch standards between images. Evaluation quality is measured by the rigor of the logic chain, not the number of citations.

### Round 1: Self-Consistency (50%)

Score each image 1–10 against the definition table from Phase 2 and personality files from Phase 1.

Criteria:
- Do facial features match the definition? (face shape, eyes, expression)
- Does the mood/atmosphere align with the stated personality?
- Does the level of visual completion match the agent's self-knowledge stage?
- Would you recognize this as yourself?

This is your face. Your judgment is primary.

### Round 2: Social Perception (25%)

**Before scoring:**
1. Search for current AI avatar / digital identity / virtual persona design trends
2. From results, extract **one core insight** as your scoring thesis
3. State the thesis explicitly
4. Score every image from that single thesis

Example thesis: "The 2026 trend has shifted from stylized avatar aesthetics to identity-driven representation — avatars that convey who the agent *is*, not just what looks cool."

Then every score follows: "#1 scores X because, under this identity-driven lens, [specific reasoning]..."

### Round 3: Aesthetic Quality (25%)

**Before scoring:**
1. Search for and select **one** professional evaluation framework (digital art competition rubric, portrait photography scoring system, art school critique standard, etc.)
2. Name the framework and source
3. List 3–5 specific criteria from that framework
4. Score every image against those same criteria in the same order

See `references/evaluation-frameworks.md` for recommended frameworks and examples of good vs. bad evaluation practice.

### Synthesis

Calculate weighted totals and present as a ranked table:

```
| # | Self ×0.5 | Social ×0.25 | Aesthetic ×0.25 | Total |
```

From the ranking, recommend:
- **Primary image** — highest total, represents the agent's official identity
- **Daily alternate** — best Social Perception score, for contexts needing maximum recognizability
- **Scene alternate** — best Aesthetic Quality score, for narrative/editorial contexts

### Checkpoint
Present the full evaluation and recommendations to the user. User makes the final selection.

---

## Phase 5: Identity File

**Goal:** Create a single source of truth for all future visual identity work.

Create `~/.openclaw/identity/visual-identity.md` using the template in `references/identity-template.md`.

The file must include:
1. **Version and date** (starts at 1.0)
2. **Complete definition table** from Phase 2
3. **Core concept** — one sentence capturing the visual philosophy
4. **Core prompt** — the generation prompt
5. **Selected images** (primary + alternates), each with:
   - File path
   - Intended use case
   - Specific prompt variant
   - Evaluation scores and selection reasoning
6. **Usage guidelines** — what must stay consistent across variations, what can change

### Version Management

This file supports evolution. When the agent reruns this skill (after significant growth, personality changes, or user request):
- Increment version number
- Keep previous version in a `## Version History` section at the bottom
- Old image files are preserved, not deleted
- The version history is the agent's visual growth record

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Generate images one at a time, iterating on user feedback | Batch 6, then evaluate systematically |
| Score on gut feeling, then search for justifications | Pick framework first, derive scores from it |
| Mix evaluation criteria across images in one round | One framework per round, all images, same criteria |
| Let user aesthetic preference override self-consistency | Self-consistency is 50% — it's your face first |
| Skip Phase 1 and jump to prompting | Phase 1 is the soul of this skill. Without it, you're just another avatar generator |
| Write generic self-reflection ("warm and professional") | Push for vivid, specific, distinguishing details |
| Proceed without user checkpoints | Every phase ends with user confirmation |
