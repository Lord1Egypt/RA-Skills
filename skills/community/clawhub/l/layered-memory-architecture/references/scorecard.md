# Memory System Scorecard

Use this rubric when comparing a layered memory architecture against a generic persistent-memory system.

## 1) Architecture quality
Ask:
- Are there explicit memory layers?
- Is hot memory bounded?
- Are durable doctrine and raw notes separated?

High score:
- multiple clear memory layers with strong rules

Low score:
- one store plus loose tags/categories

## 2) Retrieval clarity
Ask:
- Does retrieval start from the right layer?
- Can the system avoid searching irrelevant memory classes?
- Can it distinguish canon from raw history?

High score:
- layer-first retrieval with scoped reads

Low score:
- broad search over everything

## 3) Truthfulness about live state
Ask:
- Are operational snapshots separated from long-term memory?
- Can temporary status be mistaken for durable truth?
- Are summaries treated as derived state?

High score:
- explicit canon vs live-summary separation

Low score:
- alerts/status/logs mixed directly into durable memory

## 4) Token efficiency
Ask:
- Is the hot layer small?
- Are detailed docs loaded only on demand?
- Are summaries used before raw logs?

High score:
- bounded hot memory + selective load order

Low score:
- always search/read the growing memory store

## 5) Long-term maintainability
Ask:
- Does the system support promotion and demotion?
- Is there dedupe discipline?
- Can old detail cool off without polluting the hot path?

High score:
- memory ages gracefully and remains searchable

Low score:
- append-only memory landfill

## 6) Ease of use
Ask:
- Can operators write and retrieve memory simply?
- Are helper tools obvious and low-friction?
- Is it easy to explain the workflow?

High score:
- simple write/retrieve helpers and clear conventions

Low score:
- strong design but too much manual judgment

## 7) Demo friendliness
Ask:
- Can the system be explained in under a minute?
- Is the value visible quickly?
- Does it produce a compelling before/after story?

High score:
- easy to demonstrate and narrate

Low score:
- valuable but structurally complex to explain

## 8) Project scoping
Ask:
- Can project memory stay isolated from global canon?
- Are project artifacts kept out of hot memory by default?
- Can cross-project doctrine still be promoted upward?

High score:
- explicit project layer with promotion boundaries

Low score:
- one global memory with project tags only

## 9) Operator trust
Ask:
- Will the system confidently retrieve stale nonsense?
- Can users trace why a memory was treated as important?
- Does the system keep authority boundaries visible?

High score:
- scoped, trustworthy retrieval and clear authority boundaries

Low score:
- plausible but muddy recall

## Video-friendly summary line
- Most persistent-memory systems optimize for remembering more.
- Layered memory architecture optimizes for remembering the right things in the right places.
