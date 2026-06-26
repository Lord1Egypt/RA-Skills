---
name: knowledge-forge
description: >-
  Transform raw personal experience, case studies, business documents, or draft
  content into transferable cognitive assets -- structured knowledge that others
  can understand, remember, and apply. Use this skill when users want to turn
  experience or case studies into teachable content, redesign presentations for
  maximum retention, create course outlines from domain expertise, crystallize
  knowledge into shareable documents or knowledge cards, convert know-how into
  teachable answers, or any scenario where experience must become portable and
  transferable.
---

# Knowledge Forge

Forge raw experience into transferable cognitive assets using a 4-step conversion engine.

## Core Concept

Experience is abundant. Answers are scarce.

Most experts are strong inside their own world. But when they open a document or step on stage, others can't follow. The problem is not lack of experience -- it's that experience has not been **modeled**.

A modeled experience is one that has been abstracted into a structure that transfers across contexts. This skill performs that transformation.

## Conversion Engine

When the user provides raw material (a case study, personal summary, business document, draft speech, or any form of experience narrative), execute these 4 steps sequentially:

### Step 1: Perspective Flip -- "My experience" -> "Your challenge"

Identify what the user accomplished, then reframe it as a **universal challenge** the audience faces.

- Extract the core problem the user solved
- Abstract it away from domain-specific details
- Restate it as a challenge the target audience recognizes in their own work
- The audience should think "yes, I face this too" -- not "interesting, but that's your job"

**Key question to answer:** "What struggle does the audience already have that this experience speaks to?"

For modeling patterns and examples, see [modeling-patterns.md](references/modeling-patterns.md).

### Step 2: Experience Modeling -- Specific story -> Transferable structure

The raw experience is a story. Transform it into a **model** -- an abstraction that works across scenarios.

- Find the structural pattern hidden in the specific case
- Name it with a memorable, compact label (e.g., "The 100->10->1 Funnel")
- Validate: does the model apply to at least 2-3 other domains the audience cares about?

**Key question to answer:** "What is the underlying structure that makes this experience work -- independent of the specific domain?"

For modeling archetypes and before/after examples, see [modeling-patterns.md](references/modeling-patterns.md).

### Step 3: Narrative Reconstruction

Rebuild the narrative using this sequence:

1. **Challenge alignment** -- Present the universal challenge so the audience enters the tension. Spend substantial space here. Make old/obvious answers visibly insufficient.
2. **Model reveal** -- Introduce the abstracted model as the new lens. Emphasize the shift in thinking (role change, mental model upgrade), NOT tool details or step-by-step procedures.
3. **Evidence from experience** -- Use the original story as proof that the model works, not as the centerpiece.

**Principle:** Present the "Dao" (the judgment behind decisions), not the "Shu" (the operational steps). Tools and procedures are forgettable; the cognitive shift is what transfers.

For techniques on designing cognitive gaps, see [challenge-design.md](references/challenge-design.md).

### Step 4: Anchor Design -- The one sentence they carry away

Design a single, specific, portable judgment -- the **anchor**.

Requirements for a good anchor:
- **Specific** -- not a vague platitude ("work smarter") but a concrete reframing ("AI doesn't save you time -- it changes which game you're playing")
- **Sticky** -- compact enough to remember and repeat
- **Generative** -- triggers new thinking when applied to the audience's own context

**Key question to answer:** "If the audience forgets everything else, what is the ONE sentence that, by itself, changes how they think?"

Place the anchor at the structural climax of the output. It must feel earned -- a culmination of the challenge and model, not a disconnected slogan.

## Output

After completing the 4 steps internally, produce the final output.

### Determining Output Format

If the user specifies a format, use it. Otherwise, infer from context:

| Signal | Format |
|--------|--------|
| "presentation", "talk", "speech", "share" | Presentation Script |
| "course", "training", "teach", "workshop" | Course Outline |
| "article", "post", "essay", "document" | Article / Document |
| "summary", "card", "one-pager", "memo" | Knowledge Card |
| Ambiguous or unspecified | Knowledge Card (default) |

For output templates and structural guidance, see [output-formats.md](references/output-formats.md).

### Output Structure

Every output, regardless of format, must contain these elements:

1. **The Challenge** -- The universal problem, stated in the audience's language
2. **The Model** -- The transferable structure, with a memorable label
3. **The Evidence** -- The original experience, reframed as proof of the model
4. **The Anchor** -- The one sentence to carry away

### Transformation Log

After the main output, append a brief `## Transformation Log` showing the key decisions made during conversion:

```
## Transformation Log

- **Perspective Flip**: [Original framing] -> [Audience-facing challenge]
- **Model Extracted**: [Model name and one-line description]
- **Narrative Shift**: [What was de-emphasized vs. elevated]
- **Anchor**: "[The one sentence]"
```

This log helps the user understand and iterate on the transformation.
