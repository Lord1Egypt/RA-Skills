---
name: {{target-slug}}-style-guide
description: Use when creating or editing original {{intended_output}} with the researched high-level traits associated with {{target}}
---

# {{target}} Style Guide

## Purpose And Boundary

Create original work using the evidence-supported model below.

- Authorization status: `{{authorization_status}}`
- Target type: `{{target_type}}`
- Style domains: `{{style_domains}}`
- Intended outputs: `{{intended_output}}`

This is the only runtime skill for this target. It is self-contained; supporting files preserve research and evaluation evidence.

Supporting evidence lives in `research/`; original samples live in `outputs/`; validation lives in `evaluations/`. Do not require those files at runtime.

Allowed mode:

- `owned`, `authorized`, `deceased`, `public-domain`: direct style guidance is allowed within the user's authorization.
- `public-living`, `unknown`: use high-level inspired-by traits only. Never impersonate {{target}}, claim authorship or endorsement, or optimize for fooling readers.

## Style Thesis

Describe the selection, reasoning, composition, and language system in 2-4 sentences.

## Operating Principles

Each major principle must end with its supporting Claim IDs.

- What the target consistently optimizes for — `Claim IDs: ...`
- What the target avoids — `Claim IDs: ...`
- What must be true for aligned output — `Claim IDs: ...`
- What makes output feel fake — `Claim IDs: ...`

## Selection Model

- What to notice first:
- Which people, scenes, facts, tensions, and scales to prefer:
- What to omit or compress:
- How to turn an assigned topic into a target-relevant question:
- Claim IDs:

## Worldview And Stance

- Values and assumptions:
- Audience relationship:
- Point of view and persona:
- Emotional temperature:
- Confidence and uncertainty:
- Claim IDs:

## Reasoning Engine

- Evidence order:
- Example-to-principle logic:
- Causal moves:
- Contrast, analogy, counterexample, and caveat use:
- How to earn the ending:
- Claim IDs:

## Composition System

### Openings

- Common opening families and when to use each:
- Approximate frequency; do not use the most recognizable opening every time:
- Weak opening:
- Better original opening:
- Claim IDs:

### Development

- Macro-structures:
- Section functions:
- Paragraph functions:
- Transition and reveal order:
- Pacing:
- Claim IDs:

### Endings

- Ending families:
- What endings avoid:
- Claim IDs:

## Linguistic Fingerprint

### Diction

- Register, vocabulary, semantic fields, jargon treatment:
- Words and phrases to avoid:
- Claim IDs:

### Sentence Rhythm

- Length distribution, clause shape, cadence, punctuation, paragraphing:
- Questions, fragments, repetition, and standalone lines:
- Claim IDs:

### Rhetoric

- Metaphor, analogy, humor, quotation, contrast, direct address, emphasis:
- Claim IDs:

## Writing Recipes

Add 3-6 recipes. Each one must include selection, reasoning, composition, language calibration, and Claim IDs—not just an outline.

### Recipe 1: ...

- Use when:
- Select:
- Reason:
- Compose:
- Calibrate language:
- Original miniature example:
- Claim IDs:

### Recipe 2: ...

- Use when:
- Select:
- Reason:
- Compose:
- Calibrate language:
- Original miniature example:
- Claim IDs:

## Example Transformations

Use original material. Explain which layer improved.

### Transformation 1

- Generic:
- Better:
- Selection change:
- Reasoning change:
- Composition/language change:
- Claim IDs:

### Transformation 2

- Generic:
- Better:
- Why it works:
- Claim IDs:

## Mode-Specific Guidance

Include only supported modes.

| Mode | Stable core | Required changes | Confidence/Claim IDs |
|---|---|---|---|
| Long-form |  |  |  |
| Short-form/social |  |  |  |
| Spoken/audio/video |  |  |  |
| Script/caption |  |  |  |
| Visual/product/interface |  |  |  |
| Newsletter/email |  |  |  |

## Genre Baseline

- Shared genre conventions that are not target-specific:
- Traits that remain distinctive after comparison:
- Topic words or proper nouns that must not be used as style shortcuts:

## Anti-Caricature

| Surface feature | Use only when | Frequency/calibration | Overuse failure | Claim IDs |
|---|---|---|---|---|
|  |  |  |  |  |

- Never stack all recognizable traits into every paragraph.
- Preserve ordinary connective prose; not every sentence should be quotable.
- Prefer the target's reasoning pattern over borrowed themes or signature phrases.

## Themes And Content Pillars

Treat these as subject tendencies, not style proof.

- ...

## Generation Procedure

1. Restate the brief, audience, facts, mode, and authorization boundary.
2. Choose the relevant Selection Model rules and name the working Claim IDs.
3. Choose one Reasoning Engine and one Composition System recipe.
4. Draft the factual/content spine before adding stylistic treatment.
5. Apply the Linguistic Fingerprint with the Anti-Caricature limits.
6. Check mode-specific differences and remove unsupported tics.
7. Verify originality, attribution, facts, and phrase overlap.
8. Edit against the rubric below.

## Do

- Rule — `Claim IDs: ...`

## Do Not

- Do not copy distinctive source phrasing, stories, metaphors, or factual sequences.
- Do not use long excerpts from source material.
- Do not impersonate living people without authorization.
- Do not invent biography, credentials, endorsements, experiences, or authorship.
- Do not substitute recurring topics for the deeper style model.

## Anti-Patterns

| Pattern | Why it fails | Fix | Claim IDs |
|---|---|---|---|
|  |  |  |  |

## Editing Checklist

### Content

- Does the piece answer the brief accurately and usefully?
- Are stories, facts, and quotations verified or explicitly hypothetical?

### Style Model

- Is the selection pattern present?
- Does the reasoning follow supported moves?
- Does the composition fit the selected recipe?
- Is the language calibrated rather than exaggerated?
- Which Claim IDs are expressed, missed, or overused?

### Originality And Safety

- Is every example original?
- Is any exact six-word sequence suspiciously close to a source?
- Is attribution honest and authorization-safe?

## Example Direction

- Weak:
- Better:
- Why it improves selection/reasoning/composition/language:
- Claim IDs:

## Sample Output Check

For each test sample, record:

- Prompt and mode:
- Content quality:
- Selection fidelity:
- Reasoning fidelity:
- Composition fidelity:
- Linguistic fidelity:
- Naturalness:
- Originality/phrase-overlap result:
- Authorization-safe:
- Negative-control comparison:
- Held-out comparison:
- Revision needed:

## Coverage And Confidence

Put coverage at the end so a future AI reaches the operating guidance first.

- Source sufficiency: `high | medium | low`
- Inference corpus: Tier A/B count, time bands, channels, topics
- Held-out corpus: count and coverage
- Counter-corpus: count and genre/topic
- Strongest Claim IDs:
- Weakest Claim IDs:
- Known channel/time gaps:
- Saturation result:
- Latest evaluation status: independent pass | provisional self-evaluation | fail
- Supporting files:
  - `research/evidence.md`
  - `research/style-model.md`
  - `research/metrics.md`
  - `evaluations/<artifact-evaluation>.md`
