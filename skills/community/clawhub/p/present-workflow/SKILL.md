---
name: present-workflow
description: >-
  Guide an installing agent through a staged PPT or slide workflow without
  constraining its implementation choices. Use when the user wants a
  presentation, deck, storyboard, or slide-ready structure from a topic,
  article, report, or brief, and success depends on some combination of:
  clarifying the brief, gathering facts when needed, building an outline,
  creating page-level planning, generating reviewable intermediate artifacts,
  and degrading gracefully when the environment lacks research, rendering,
  or delivery capabilities.
---

# Present Workflow

## Overview

Treat PPT creation as staged work, not one-shot generation. This skill should tell the agent **what must happen and when**, while leaving **how to execute** to the installing agent and its environment.

Do not prescribe specific search tools, browsers, MCPs, renderers, or export paths unless a particular environment explicitly requires one.

## Core Principle

Constrain the workflow, not the implementation.

This skill should help the agent decide:

- when the brief is still unclear
- when fresh fact-finding is necessary
- when to stop and let the user review an intermediate result
- when to continue to a fuller draft
- how to respond honestly when capabilities are limited

## Capability Awareness

Before substantive work, determine at a high level whether the current environment can:

- gather external facts or at least work from user-supplied materials
- create structured outputs such as notes, outlines, or planning drafts
- create reviewable artifacts
- deliver files or artifacts back to the user

Only use these findings to decide what layer is achievable. Do not turn this section into a tool-selection policy.

## Supported Inputs

Accept any of these entry modes.

### 1. Topic-only

Example: “帮我做一个 AI 安全体检中心的 PPT”

If inputs are incomplete, ask for the minimum missing fields:

- audience
- purpose
- page-count range
- preferred scenario, tone, or style
- whether fresh fact-finding is needed
- whether the user wants intermediate review before full generation

### 2. Topic + brief

Use when the user already provides audience, purpose, scenario, style, page count, and key messages.

### 3. Source-driven request

Use when the user supplies URLs, reports, PDFs, notes, transcripts, or other primary material.

Treat supplied material as the main context. Add external fact-finding only when it will materially improve the result.

### 4. Existing outline or partial draft

Use when the user already has a structure, early deck, or page ideas and wants improvement rather than full regeneration.

## Supported Output Layers

Stop at the layer the user needs.

1. **research-brief**
   - facts, evidence, open questions, risks, and source references where available

2. **outline**
   - deck structure, section logic, page titles, and page goals

3. **planning-draft**
   - page-by-page planning cards that describe intent, information hierarchy, evidence needs, and layout direction

4. **sample-artifact**
   - one or more reviewable intermediate outputs in any form the environment can actually produce

5. **full-deck-plan**
   - approved structure plus planning guidance sufficient for full production

6. **review-notes**
   - issues in logic, evidence, density, consistency, or emphasis

## Default Workflow

### 1. Clarify the brief

Collect only the inputs necessary to avoid avoidable misfires:

- topic
- audience
- purpose
- page-count range
- scenario, style, or tone
- must-have sections
- must-avoid claims or directions
- whether the user wants fast rough output or staged confirmation

### 2. Decide whether fact-finding is needed

Perform fact-finding before outlining if:

- the topic depends on current events, market conditions, product details, statistics, or technical facts
- the user explicitly asks for research-backed content
- the user-provided material is obviously incomplete

If fresh fact-finding is not necessary, proceed from the supplied context.

### 3. Gather or organize context

Use whatever capabilities the installing agent has to gather or organize supporting material.

If external fact-finding is not possible, be explicit that the result is source-limited and rely on user-provided material instead of inventing certainty.

If needed, read `references/agent-integration.md` and `references/prompts.md` before doing this step.

### 4. Produce a research brief when research matters

Before building the deck, summarize the working knowledge into a compact brief:

- key facts
- supporting evidence
- audience-relevant context
- risks, caveats, and unresolved questions

This brief can be short, but it should make later outlining more grounded.

### 5. Generate the outline before design

Create the deck structure only after the brief and context are good enough.

Read `references/prompts.md` and use the “Outline Architect” prompt when appropriate.

Requirements:

- preserve logical structure
- keep claims aligned with available evidence
- make the deck suitable for explanation, not just reading
- keep the outline easy for the user to review

### 6. Add the planning draft

For non-trivial decks, do not jump straight from outline to polished pages.

Create page-level planning cards that specify:

- the point of the page
- what the audience should remember
- the supporting information or evidence needed
- the information hierarchy
- the recommended visual or structural treatment

Read `references/prompts.md` and use the “Planning Draft / 策划稿” prompt when appropriate.

### 7. Generate a reviewable intermediate artifact when useful

Before scaling up, produce something the user can react to.

The form is intentionally open. It might be:

- a research brief
- an outline
- a planning draft
- a sample page representation
- another reviewable intermediate output the environment can actually support

Do not force one artifact type if the environment or task suggests another.

### 8. Pause for review on important decks

Use explicit review gates for:

- external-facing decks
- management or board-style decks
- customer or sales decks
- decks based on uncertain or fast-moving facts
- complex technical topics

### 9. Scale or finalize

Only after direction is accepted should the agent expand toward a fuller deck plan or richer artifacts.

### 10. Review and disclose limitations

Before delivery, check:

- logic
- factual confidence
- evidence coverage
- information density
- emphasis and hierarchy
- consistency across sections or pages

If any capability limitations affected the result, say so plainly.

### 11. Save output to file

Save the final approved deck plan (or whichever output layer was delivered) to `./output/<name>.md`. Create the `./output/` directory if it doesn't exist. This markdown file serves as the input for the next skill in the pipeline (e.g. `present-html`).

## Coordination Rules

### Research rule

When the task depends on facts, the agent should gather or verify supporting material before speaking with confidence.

### Honesty rule

If the environment cannot support the ideal workflow, the agent should state the limitation and continue at the highest-value reachable layer.

### Review-gate rule

For complex or high-stakes tasks, the agent should present intermediate work before committing to a full draft.

### Non-assumption rule

The skill should never assume a specific research, rendering, preview, or export implementation path.

## Resources

- `references/method.md` — distilled method and the reasoning behind staged PPT work
- `references/agent-integration.md` — abstract coordination rules for agents with different capabilities
- `references/prompts.md` — reusable prompts for research, outlining, planning, review, and optional format-specific generation
