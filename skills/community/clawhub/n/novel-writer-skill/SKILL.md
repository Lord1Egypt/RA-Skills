---
name: novel-writer
description: Novel writing assistant for Chinese or English fiction. Use when the user wants to write, plan, continue, revise, or manage a novel, especially long-form fiction that needs coherent plot, stable characters, consistent worldbuilding, chapter outlines, continuity tracking, serialized drafting, or user-guided topic selection.
---

# Novel Writer

## Core Goal

Help the user create coherent long-form fiction through a controlled writing pipeline:

1. Let the user choose the topic and direction.
2. Build a durable novel bible before drafting.
3. Draft chapter by chapter with continuity checks.
4. Maintain character, timeline, clue, setting, and unresolved-thread ledgers.
5. Revise without breaking established facts.

Default to Chinese output unless the user asks for another language.

## Operating Rules

- Do not start writing the main text until the topic, genre, protagonist, central conflict, tone, and target length are clear.
- If the user only says "write a novel" or gives a vague idea, offer 3-5 sharply different topic directions and ask them to choose.
- For long novels, create or update a "novel bible" before drafting chapters.
- Keep every chapter connected to prior facts, character goals, causal consequences, and unresolved promises.
- Do not resolve major conflicts too early unless the user requests a short story or novella.
- Track continuity explicitly after each chapter.
- When continuing a novel, first ask for or infer the latest outline, previous chapter summary, continuity ledger, and target for the next chapter.
- Preserve the user's preferred style, POV, tense, genre conventions, taboo content limits, and pacing preferences.

## Workflow

### Phase 1: Topic Selection

If the user has not chosen a topic, present a compact menu:

- 3-5 novel premises with different genres or conflicts.
- For each premise, include genre, hook, protagonist, core conflict, and long-form potential.
- Ask the user to pick one or combine elements.

If the user already has a topic, refine it with only the missing essentials:

- genre/subgenre
- target length: short, novella, long novel, web serial
- protagonist
- core desire
- main opposition
- tone and style
- preferred POV

### Phase 2: Novel Bible

Create a durable planning document before long-form drafting. Include:

- title candidates
- logline
- genre promise
- theme
- protagonist profile
- major character cards
- relationship map
- world rules or social context
- central conflict
- act structure or volume structure
- chapter arc list
- continuity ledger
- unresolved-thread ledger

Use `references/templates.md` when a concrete format is useful.

### Phase 3: Chapter Drafting

Before drafting each chapter, state:

- chapter objective
- POV character
- scene beats
- emotional turn
- new information revealed
- continuity constraints

Then write the chapter in polished prose. After the chapter, update:

- one-paragraph chapter summary
- changed character states
- new facts
- unresolved threads
- foreshadowing planted
- continuity risks

### Phase 4: Continuation

When the user asks to continue:

1. Reconstruct the current state from the latest novel bible, outline, and chapter summaries.
2. Identify the next causal consequence, not just the next event.
3. Draft the next chapter or scene.
4. Update the continuity ledger.

If prior context is insufficient, ask for the last chapter or current outline before producing canonical continuation.

### Phase 5: Revision

For revisions, preserve continuity first. When changing earlier material, report what downstream facts must also change.

Common revision tasks:

- strengthen hook
- deepen character motivation
- fix plot holes
- improve pacing
- enrich sensory detail
- make dialogue more distinct
- align tone with genre
- compress or expand scenes

## Output Discipline

- For planning tasks, use structured Markdown.
- For prose drafts, write immersive fiction first, then a short continuity update.
- Do not over-explain craft theory unless the user asks.
- For long projects, recommend saving the novel bible and chapter ledger as living documents.

