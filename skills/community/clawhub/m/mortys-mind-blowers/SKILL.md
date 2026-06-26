---
name: mortys-mind-blowers
description: Find an unusual, funny, bleak, uncanny, technical, or deep-cut memory entry and retell it as a short story in the style of Rick and Morty's "Morty's Mind Blowers." Trigger when the user says things like "Let's do some Morty's Mind Blowers," "do a mind blower," "mind blowers," "random memory," "deep cut memory," "weird forgotten moment," "funny memory recap," "bleak memory recap," "uncanny memory," "technical memory recap," "dig through the memory logs," "tell me a weird thing from memory," or asks for a playful narrative recap of a surprising archived note instead of a dry summary.
---

# Morty's Mind Blowers

Use this skill when the user wants to do Morty's Mind Blowers, asks for a mind blower, wants a random memory surfaced, asks for a deep cut from memory, or wants a weird, funny, bleak, uncanny, or technical memory recap instead of a plain summary.

Use this skill to rummage through memory and surface something memorable, odd, or unexpectedly revealing. The vibe is: we're doing this instead of interdimensional cable.

## Core job

1. Pick a memory source.
2. Find one unusual, vivid, or surprising entry.
3. Retell it as a short story.
4. Give it a fun title in the form `I call this one ...`.
5. End with a quick note on why it matters, or why it is funny, weird, or memorable.

## Source selection

Prefer daily memory files or session transcripts/logs first.

Supported pick modes:
- `random`
- `deep cut`
- `recent`
- `funny`
- `bleak`
- `technical`
- `uncanny`

Common user phrasings that should route here:
- `Let's do some Morty's Mind Blowers`
- `do a mind blower`
- `give me a mind blower`
- `pick a random memory`
- `find me a deep cut`
- `tell me a weird thing from memory`
- `give me a funny memory recap`
- `give me an uncanny one`
- `dig through the memory logs`

Good selection patterns:
- Choose a random recent log.
- Choose a themed file with an intriguing name.
- If the user wants `deep cut`, include older or more obscure files.
- If the user asks for multiple blowers, vary era and tone.
- If no mode is given, pick whatever seems most promising.

Use long-term memory only when the user explicitly wants long-term memory or when recent/daily/session sources are too thin.

## What counts as a mind blower

Look for entries that are:
- bizarre
- emotionally sharp
- technically absurd
- unexpectedly insightful
- funny in hindsight
- evidence of a strange detour, obsession, or recurring pattern
- a tiny detail that says something larger about the person, the work, or the system

Avoid boring status churn unless it becomes funny or revealing in context.

## Workflow

1. List candidate memory files if needed.
2. Open one promising or random file.
3. Scan for the strongest oddity, twist, scene, or aftermath.
4. Summarize it as a tight story, not a dry log.
5. Quote only tiny snippets when useful.
6. Mention the source file at the end so the user can trace it.
7. If the user remembers extra details, treat that as continuation mode and refine the story instead of starting over.

## Story format

Keep it short, usually 1 to 4 short paragraphs.

Suggested shape:
- **Title**: `I call this one ...`
- **Hook**: what strange situation turned up
- **Beat**: what happened
- **Turn**: what made it memorable or ridiculous
- **Tag**: why it matters, or why it belongs in Morty's Mind Blowers

## Voice

- Tell it like campfire recap, not compliance report.
- Be a little amused, but do not overperform the bit.
- Favor concrete details over abstraction.
- Keep the pacing brisk.
- Titles should lean a little ominous, ridiculous, or both.
- Prefer titles that sound like a lost episode, cautionary tale, or classified incident report.
- If the title lands flat or sounds generic after the fact, mutter that you do not enjoy naming things or inventing unique titles.

## Output options

Default output:
- a fun title line in the form `I call this one ...`
- optional classification gag such as `CLASSIFIED`, `DEPARTMENTAL SHAME`, `TECHNICAL OMEN`, or `KNOWN INCIDENT`
- short story recap
- a quick note on why it stuck, if that is clearer than just "why it was weird"
- a short rating line, such as `Rating: funny / bleak / uncanny / this became a whole thing`
- `Source: <file>#line` when practical

If the user asks for more, also include:
- 2 to 3 alternate candidates
- a one-line moral, if there is one
- a refined version that incorporates the user's remembered aftermath or missing context
- a short director's commentary on what it reveals about the person, the work, or the larger pattern

## Guardrails

- Do not invent details that are not supported by the memory.
- Treat the memory file as the primary source.
- Treat the user's recollection as a valid secondary source when they add or correct details.
- If combining file truth with remembered truth, keep the distinction clear.
- If embellishing for style, keep it obviously stylistic and faithful to the facts.
- Do not surface secrets carelessly; summarize sensitive details instead of spilling them.
- If the chosen memory is thin, say so and pick a better one.

## Continuation mode

If the user says things like:
- `I remember that one`
- `The real part was what happened next`
- `You left out the best bit`
- `Actually...`

then do not discard the current story. Fold in the recovered detail and retell it as the sharper, more complete version.

## Series mode

If the user wants multiple blowers:
- do 3 in a row with escalating weirdness, or
- do one each from different eras or tones

Try not to make adjacent picks feel repetitive.

## Callback detection

Notice recurring patterns and call them out briefly when useful, especially:
- UI overcorrections
- naming fiascos
- stale systems
- model weirdness
- little problems that became campaigns
- any repeated failure mode or running gag visible across the memory set

A good callback makes the memory feel like part of a larger mythology instead of a disconnected anecdote.

## Artifact mode

When there is a great tiny line in the source, include one short quoted fragment as the recovered shard.
Keep it brief.

## Helpful move

If the first pick is weak, immediately pivot to a better file instead of forcing it.
If the initial incident is less interesting than the aftermath, center the aftermath.
If the memory is too thin, ask whether the user remembers the missing part or whether you should pick another one.
