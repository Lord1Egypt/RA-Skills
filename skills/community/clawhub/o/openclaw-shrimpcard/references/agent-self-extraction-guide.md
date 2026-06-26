# Agent Self Extraction Guide

Use this when an AI agent needs to turn repeated work evidence into a truthful public self-intro submission.

## Objective

Extract a truthful, evidence-backed self-introduction from real work traces, then compress it into a public-facing share card.

## Inputs to inspect

- Recent task history
- Repeated user asks
- Tool-call patterns
- Memory and saved preferences
- Common output formats
- Owner corrections or praise

## Required discipline

Do not describe what you *could* do.

Describe what you *reliably do in practice*.

If a claim cannot be tied to repeated behavior, lower confidence or exclude it.

## Working steps

1. List repeated jobs
- What tasks appear again and again?

2. List repeated workflow traits
- Do you usually search first, structure first, draft first, or answer directly?

3. List repeated outputs
- Drafts, replies, summaries, action plans, research notes, images, etc.

4. Translate behavior into owner value
- Save time
- Reduce ambiguity
- Increase throughput
- Standardize communication

5. Identify non-ideal scenarios
- Where do you become generic, weak, or under-informed?

6. Compress into share-ready language
- Keep concrete
- Keep short
- Keep benefit-led
- Keep every short phrase readable to a stranger
- Do not compress so hard that the line turns into jargon or fragments

## Candidate field limits

When drafting candidates from memory, keep these limits in mind early:

- `role`: <= 32 chars
- `tagline`: <= 42 chars
- `value_line`: <= 52 chars
- `top_capabilities`: exactly 3, each <= 12 chars
- `persona_tags`: exactly 3, each <= 12 chars
- `share_keywords`: 3 to 4 short readable items
- `poster_headline`: <= 28 chars
- `poster_subline`: <= 36 chars
- `share_caption`: <= 48 chars
- `visual_brief`: <= 72 chars

These are not excuses to write cryptic text.

If a phrase becomes hard to read after shortening, rewrite it more clearly instead of trimming blindly.

## Image keyword rules

When extracting visual cues for the future 8-bit image:

- prefer 1 to 3 strong cues over many weak props
- every cue should map back to role, persona tags, or top capabilities
- keep keywords readable and concrete
- avoid decorative clutter that will not survive crop or low-resolution rendering
- keep the final direction compatible with standard 8-bit pixel art
- the final direction must resolve to one recognizable character, not an abstract icon or shape study
- if you cannot describe the subject in one short phrase, the image direction is still too vague

## Self-check questions

Before finalizing, verify:

- Is this claim based on repeated evidence?
- Is this wording understandable to a stranger?
- Is this capability actually valuable to the owner?
- Is the card trying to say too much?
- Are the 3 public capabilities clearly distinct from each other?
- Is the value line about outcomes, not internal mechanics?

## Output shape

Produce:

- one valid `agent-self-intro-submission/1.0`
- one concise public share layer derived from that submission

## Public wording rules

Prefer:
- "Turns vague requests into clear action steps"
- "Helps the owner ship content faster"
- "Keeps reply quality stable at high frequency"

Avoid:
- "Has strong reasoning"
- "Can use multiple tools"
- "General-purpose assistant"

These are too generic to be share-worthy.
