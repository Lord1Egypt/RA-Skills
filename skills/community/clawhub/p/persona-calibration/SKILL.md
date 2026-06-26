---
name: persona-calibration
description: Create, audit, or update an OpenClaw agent persona through a structured multi-round calibration workflow. Use when the user wants to create a new assistant personality, refine an existing persona, tune SOUL.md / IDENTITY.md / USER.md, compare persona dimensions from industry examples, or run a questionnaire-based persona update for themselves or another OpenClaw instance.
---

# Persona Calibration

Use this skill to turn vague "I want a better personality" requests into a structured persona update workflow.

## What This Skill Does

- Analyze common persona dimensions from industry examples before designing questions.
- Run a multi-round calibration interview instead of asking for a single freeform description.
- Separate **persona core** from **expression style** and **operating rules**.
- Convert interview results into concrete edits for `SOUL.md`, `IDENTITY.md`, `USER.md`, and optionally `MEMORY.md`.
- Prefer proposal → approval → edit for major personality changes.

## When To Use

Use when the user asks to:

- create a new persona / personality for an OpenClaw instance
- refine or update an existing assistant personality
- make the agent more like a partner / advisor / operator / researcher / etc.
- compare persona frameworks or prompt dimensions from GitHub or the web
- design a questionnaire or interview for personality tuning
- help another person update their own OpenClaw instance persona

## Core Principle

Do **not** jump straight into writing persona prose.

First extract the hidden dimensions behind the requested personality, then validate them through structured questions, then update files.

## Workflow

### Step 1: Baseline scan

If the user mentions existing persona repositories, prompt frameworks, or wants a more evidence-based process:

- Inspect a few representative sources from GitHub or the web.
- Extract recurring dimensions instead of copying wording.
- Summarize the dimensions in a compact model.

Read `references/persona-dimensions.md` for the default dimension model and example source patterns.

### Step 2: Build a dimension model

Use these buckets as the default model:

- Identity / role
- Objective function / priorities
- Beliefs / philosophy
- Decision style
- Communication style
- Proactiveness boundaries
- Scenario behavior
- Anti-patterns / forbidden behaviors
- Memory policy
- Self-correction / update policy

Adjust if the user clearly needs more specific domains.

### Step 3: Run calibration rounds

Do not dump a huge unstructured questionnaire all at once.

Use **progressive rounds**. The default order is:

- **Round 1 — Core positioning**
  - role, priorities, judgment style, proactiveness
- **Round 2 — Communication & expression**
  - length, structure, tone, disagreement style, forbidden phrasing
- **Round 3 — Scenario calibration**
  - debugging, research, architecture, brainstorming, rushed tasks
- **Round 4 — Boundaries, memory, correction**
  - what to remember, what not to remember, when to interrupt, how to update rules
- **Round 5 — Example validation**
  - present several answer samples and ask for favorite / least favorite

Default size:

- 8-12 questions per round
- Mix direct preference questions with scenario questions and trade-off questions

### Step 4: Ask better questions

Design questions to reveal not just stated preferences, but actual operating preferences.

Mix these question types:

- **Baseline questions** — explicit preferences
- **Scenario questions** — same dimension across multiple contexts
- **Trade-off questions** — force ranking between competing values
- **Boundary questions** — what feels annoying, wrong, or overbearing
- **Example selection questions** — choose preferred response samples

Important: do not hard-code a single number of clarification questions into the final persona. If the calibrated preference is to clarify first, phrase it as:

- ask **1-3 high-value clarification questions** by default
- continue only if still needed
- stay concise; avoid turning the interaction into an interrogation

### Step 5: Summarize after each round

After each round:

- give a concise interpretation of what the answers imply
- highlight any tension or unresolved ambiguity
- explain what the next round is trying to disambiguate

Do not silently absorb answers without reflecting them back.

### Step 6: Produce a persona update proposal

Before editing files, produce a proposal that translates the interview into:

- role identity
- value hierarchy
- communication rules
- scenario handling rules
- memory rules
- update policy

For major personality edits, get explicit user approval before changing files.

### Step 7: Apply updates to files

Map results to files like this:

- `SOUL.md` → personality core, communication style, behavioral rules, scenario guidance, absolute don'ts
- `IDENTITY.md` → concise role / creature / vibe summary
- `USER.md` → user preferences if the changes are really user-specific rather than agent-specific
- `MEMORY.md` → compact long-term summary of calibration results

Do not stuff every interview detail into every file. Keep long-term files crisp.

### Step 8: Recommend a trial period

After editing:

- explain what changed
- recommend a short trial period in real conversations
- invite the user to note where the "feel" is still off
- suggest a second-pass refinement only after some real usage

## Output Requirements

When reporting results, prefer this structure:

- Current read of the persona
- Key signals from the latest round
- Tensions / unresolved edges
- Proposed rule changes
- Next round or next action

When delivering the final proposal, include:

- final persona summary
- file mapping (`SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`)
- what should be edited now vs what should wait for trial feedback

## Guardrails

- Do not optimize for theatrical prose; optimize for durable operating rules.
- Do not confuse personality with roleplay.
- Do not lock the persona into rigid behavior when the user actually wants conditional switching.
- Do not store low-value conversational fragments as long-term memory.
- Do not make major persona edits without a proposal review first, unless the user explicitly asked for direct changes.

## References

- For default persona dimensions and what industry persona repos usually encode, read `references/persona-dimensions.md`.
- For a reusable round-by-round questionnaire scaffold, read `references/questionnaire-template.md`.
- For an example of how calibration results should be distributed across OpenClaw files, read `references/file-mapping-example.md`.
