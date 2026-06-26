# present-workflow

> **present-workflow** is forked & enhanced from [ppt-agent-workflow-san/ppt-workflow](https://github.com/mucsbr/ppt-agent-workflow-san/tree/main/ppt-workflow). It prepares the presentation storyline as the first stage of the pipeline.
>
> This is one of the skills in [mk-present](https://github.com/textboy/mk-present).

## Overview

Treat PPT creation as staged work, not one-shot generation. This skill guides the agent on **what must happen and when**, while leaving **how to execute** to the agent and its environment.

It does not prescribe specific search tools, browsers, MCPs, renderers, or export paths unless a particular environment explicitly requires one.

## Core Principle

Constrain the workflow, not the implementation.

This skill helps the agent decide:
- when the brief is still unclear
- when fresh fact-finding is necessary
- when to stop and let the user review an intermediate result
- when to continue to a fuller draft
- how to respond honestly when capabilities are limited

## Supported Inputs

### 1. Topic-only
Example: "帮我做一个 AI 安全体检中心的 PPT"
If inputs are incomplete, ask for the minimum missing fields: audience, purpose, page-count range, preferred tone or style, whether fact-finding is needed, and whether intermediate review is wanted.

### 2. Topic + brief
Use when the user already provides audience, purpose, style, page count, and key messages.

### 3. Source-driven request
Use when the user supplies URLs, reports, PDFs, notes, transcripts, or other primary material. Treat supplied material as the main context. Add external fact-finding only when it will materially improve the result.

### 4. Existing outline or partial draft
Use when the user already has a structure, early deck, or page ideas and wants improvement rather than full regeneration.

## Workflow

### 1. Clarify the brief
Collect the necessary inputs: topic, audience, purpose, page-count range, style or tone, must-have sections, must-avoid claims, and whether the user wants fast rough output or staged confirmation.

### 2. Decide whether fact-finding is needed
Perform fact-finding before outlining if the topic depends on current events, market conditions, product details, statistics, or technical facts. If the user explicitly asks for research-backed content, or the user-provided material is obviously incomplete, also research first. Otherwise proceed from the supplied context.

### 3. Gather or organize context
Use whatever capabilities are available to gather or organize supporting material. If external fact-finding is not possible, be explicit that the result is source-limited and rely on user-provided material.

### 4. Produce a research brief when research matters
Before building the deck, summarize working knowledge into a brief: key facts, supporting evidence, audience-relevant context, risks, and unresolved questions.

### 5. Generate the outline before design
Create the deck structure only after the brief and context are good enough. Preserve logical structure, keep claims aligned with available evidence, make the deck suitable for explanation (not just reading), and keep the outline easy for the user to review.

### 6. Add the planning draft
For non-trivial decks, create page-level planning cards specifying: the point of the page, what the audience should remember, the supporting information needed, the information hierarchy, and the recommended visual or structural treatment.

### 7. Generate a reviewable intermediate artifact
Before scaling up, produce something the user can react to — a research brief, outline, planning draft, sample page, or other reviewable output.

### 8. Pause for review on important decks
Use explicit review gates for external-facing decks, management/board decks, customer/sales decks, decks based on uncertain or fast-moving facts, and complex technical topics.

### 9. Scale or finalize
Only after direction is accepted should the agent expand toward a fuller deck plan or richer artifacts.

### 10. Review and disclose limitations
Before delivery, check: logic, factual confidence, evidence coverage, information density, emphasis and hierarchy, and consistency across sections. If any capability limitations affected the result, say so plainly.

### 11. Save output to file
Save the final approved deck plan (or whichever output layer was delivered) to `./output/<name>.md`. Create the `./output/` directory if it doesn't exist. This markdown file serves as the input for the next skill in the pipeline (e.g. `present-html`).

## Coordination Rules

- **Research rule**: When the task depends on facts, gather or verify supporting material before speaking with confidence.
- **Honesty rule**: If the environment cannot support the ideal workflow, state the limitation and continue at the highest-value reachable layer.
- **Review-gate rule**: For complex or high-stakes tasks, present intermediate work before committing to a full draft.
- **Non-assumption rule**: Never assume a specific research, rendering, preview, or export implementation path.

## Resources

- `references/method.md` — distilled method and the reasoning behind staged PPT work
- `references/agent-integration.md` — abstract coordination rules for agents with different capabilities
- `references/prompts.md` — reusable prompts for research, outlining, planning, review, and optional format-specific generation
