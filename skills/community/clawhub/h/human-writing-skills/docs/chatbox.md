# Using Advanced Human Writing & AI Humanizer in Chatbox

This guide explains how to use Advanced Human Writing & AI Humanizer with Chatbox while reducing context loss during long writing sessions.

Chatbox can use this project because the project outputs plain text prompt packs. You do not need a plugin integration. Generate a prompt pack with the CLI, then paste it into Chatbox as a system prompt or as the first message of a new conversation.

## Why Context Can Still Be Lost

Chatbox context contains three parts:

- system prompt
- chat history
- current question

In long conversations, older messages may fall outside the model's context window or be excluded by Chatbox's maximum context message setting. This project handles that by keeping a compact continuity ledger that can be pasted back into the active context.

## Recommended Chatbox Setup

1. Choose a model with a large context window.
2. Increase Chatbox's maximum context messages for long writing sessions.
3. Create a new conversation for each project, book, article series, or major chapter.
4. Put the compiled Advanced Human Writing & AI Humanizer prompt pack in the system prompt when possible.
5. If the UI you use does not expose a system prompt field, paste the prompt pack as the first message and ask the model to treat it as standing instructions.
6. Keep a separate continuity ledger and update it after each major output.

## Generate a Chatbox Prompt Pack

Fiction example:

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --module controlled-drift `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --module cultural-anchors `
  --review `
  --context examples/story-ledger.md `
  --task "Use these as standing instructions for this Chatbox writing session. Do not draft yet. Wait for my scene task."
```

Self-media example:

```powershell
python -m humanwriting.cli build `
  --style self-media `
  --module imperfect-prose `
  --module cultural-anchors `
  --module vocal-rhythm `
  --review `
  --context examples/article-brief.md `
  --task "Use these as standing instructions for this Chatbox writing session. Do not draft yet. Wait for my article task."
```

## No-Loss Context Routine

Use this routine every 3 to 5 substantial turns, or whenever the conversation becomes long.

### 1. Ask for a Ledger Update

Paste this into Chatbox:

```text
Update the continuity ledger only. Do not continue the draft.

Keep:
- Fixed facts
- Active threads
- Relationship state
- Current audience, possible overhearers, and public/private setting
- Public stance, private stance, and information permissions
- Who may mention whom, allowed tone, forbidden leaks, and exception motives
- Voice anchors
- Stable speaker baseline, knowledge/role constraints, disclosure habits, and audience shifts
- Current dialogue contract: purpose, desired outcomes, protected information, response tactics, and intended state change
- Open interaction debt: consequential lines or actions awaiting uptake, refusal, interruption, consequence, or delayed payoff
- Spatial positions and seat/standing locations
- Physical resource modes, capacity, and occupants
- Clothing, shoes, injuries, and prop state
- Movement transitions already shown on-page
- Transformation gates already shown on-page, such as folded seats, cleared tables, or opened beds
- Current scene or section state
- Beat bridge: previous residue, entry pressure, micro-turn, exit pressure
- Newly true facts from the latest output
- Newly exposed secrets, suspicions, alliance changes, and mention-policy changes
- Open questions and unresolved pressure

Remove:
- repeated wording
- discarded options
- generic summaries
- anything not needed for future continuity
```

### 2. Save the Updated Ledger

Copy the ledger into a local Markdown file, for example:

```text
my-novel-ledger.md
```

### 3. Rebuild the Prompt Pack

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --module controlled-drift `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --review `
  --context my-novel-ledger.md `
  --task "Continue from the current scene state. Preserve all fixed facts and unresolved threads."
```

### 4. Start a Fresh Chatbox Thread When Needed

Start a new Chatbox conversation when:

- the thread exceeds 20 to 30 rounds
- the model repeats itself
- old facts start drifting
- you change chapter, article, or writing goal

Paste the rebuilt prompt pack at the start of the new conversation.

## Auditing an Existing Draft in Chatbox

When you need to review an already-written chapter, generate an audit pack:

```powershell
python -m humanwriting.cli audit `
  --draft my-chapter.md `
  --context my-novel-ledger.md
```

Paste the output into Chatbox. It instructs the model to extract evidence first, then check seats, barriers, reach/contact, clothing, shoes, props, and injuries.

For false precision review:

```powershell
python -m humanwriting.cli audit `
  --draft my-chapter.md `
  --profile numbers
```

It asks the model to list each exact number and decide whether to keep, soften, or delete it.

### Running the Multi-Stage Pipeline in Chatbox

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --auto `
  --output-dir chapter-audit
```

Open a fresh Chatbox conversation for every generated stage and paste that stage's Markdown prompt. Do not run all stages in one conversation, because earlier judgments can bias later passes. Reconcile duplicate findings and repair order only after every stage finishes.

## Copyable Chatbox Opening Message

```text
Treat the following as standing instructions for this writing session.

Rules:
- Keep the continuity ledger active.
- Before every draft, check fixed facts, active threads, voice anchors, and current state.
- Before dialogue, check speaker -> listener/audience -> referenced party together with
  baseline voice, current goal, knowledge/role constraints, response linkage, mention
  policy, and information permissions; do not substitute occupation for personality.
- Before shifting away from a consequential line or action, show verbal, physical,
  silently legible, interrupted, or deliberately deferred uptake without forcing every
  sentence into mechanical ping-pong.
- In cars, rooms, elevators, dining areas, beds, stools, aircraft, motorcycles, or other physical spaces, check positions, resource capacity, transformations, reach, clothing, props, and movement gates before drafting.
- Do not overwrite established facts for convenience.
- If context is missing, make the smallest possible assumption and mark it.
- After each long draft, output a short "Ledger Update" section only when I ask for it.
- If I type "更新账本", update the ledger instead of continuing the draft.

I will now paste the compiled Advanced Human Writing & AI Humanizer prompt pack.
```

## Practical Limits

This workflow reduces context loss, but it cannot make a model remember infinite text. For long novels, serialized fiction, research reports, or article series, the continuity ledger is the source of truth.

When the model forgets, do not argue with the chat history. Rebuild the prompt pack from the latest ledger and continue from there.
