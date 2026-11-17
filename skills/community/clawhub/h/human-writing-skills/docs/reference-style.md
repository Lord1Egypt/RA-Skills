# Reference Style Alignment

This module makes a draft resemble the craft features of explicitly supplied
material without importing its content.

## Activation Gate

It activates only when at least one signal exists:

- one or more `--reference` files
- an explicit `--reference-style` direction
- task wording such as "match this voice" or "write in the referenced style"

`--context` alone never activates style matching. Context contains facts and
continuity; references contain style evidence.

## What It Extracts

The prompt asks the model to form a compact style card covering point of view,
sentence rhythm, lexical register, imagery density, scene and character
description, dialogue cadence, emotion handling, and transitions. It then applies
those features selectively to the current genre and task.

The compiler samples long references from the beginning, middle, and end under a
global character budget. Use multiple representative passages instead of an entire
book when possible.

## Authority And Safety

Project facts, relationships, chronology, and world rules always come from the
user and `--context`. Do not copy names, events, conclusions, signature phrases,
or distinctive metaphors from a reference. For a named living or highly distinctive
author, translate the request into high-level features instead of close imitation.

## Writing And Audit

```powershell
human-writing-skills build --style fiction --reference sample.md --task "Continue the chapter."
human-writing-skills audit --draft chapter.md --reference sample.md --profile style-match
human-writing-skills pipeline --draft chapter.md --reference sample.md --auto --output-dir audit
```

In a pipeline, only the `style-match` stage receives the reference block. Other
passes stay focused on logic, character, relationships, physical continuity,
numbers, and proofreading.
