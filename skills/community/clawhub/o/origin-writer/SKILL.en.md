---
name: origin-writer
description: Million-word novel writing engine that turns long-form fiction into transactional writing. Each chapter is committed as a semantic transaction (prose + state changes); gates re-check every item (forbidden zones / foreshadowing state machine / prose-vs-state cross-check) before anything hits disk. Characters never use information they cannot have, items never change hands out of thin air, a hook is never re-planted after it has been paid off. New sessions recover instantly: one `state` command returns the full world state. Use when writing long novels, continuing serialized fiction, maintaining worldbuilding consistency, or managing foreshadowing / character state / timelines. (中文版见 SKILL.md)
version: 1.1.1
slug: origin-writer
license: Apache-2.0
displayName: OriginWriter — Million-Word Novel Writing Engine
summary: Turns long-form writing into transactional writing — one semantic transaction per chapter, five gates before commit, character/foreshadowing/world state verifiable end to end.
metadata:
  openclaw:
    runtime: node >= 18
    tags: [writing, novel, story, world-state, consistency]
---

# OriginWriter · Million-Word Novel Writing Engine

Long novels fail the same way for one reason: **the world state lives only in the
model's context window.** By chapter 30, the model has forgotten the foreshadowing
planted in chapter 3, the wound taken in chapter 9, and who learned what, when.
Context gets lost; state doesn't — provided it is persisted, and every change passes
a gate.

OriginWriter turns long-form writing into **transactional writing**: each chapter is
committed as a semantic transaction (prose + declared state changes). All five gates
must pass before anything is written; on failure, nothing is written and you get a
reason you can rewrite against.

## Install

```bash
# The Benxiang protocol repo (engine, world spec, self-tests):
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# Verify the engine:
node adapters/story/selftest.mjs        # 42 assertions
```

## Usage

```bash
# 1. Build a writing package from a world spec (world replayed up to ch.10; you write from ch.11)
node adapters/story/cli.mjs init <specDir> <pkg.origin> --until 10

# 2. First thing in any new session: project the world state (instant recovery)
node adapters/story/cli.mjs state <pkg.origin>

# 3. The AI writes a chapter and commits it as a transaction (prose + state changes)
node adapters/story/cli.mjs submit <pkg.origin> ch11.json

# 4. Hook graph / chapter ledger / transaction watermark
node adapters/story/cli.mjs hooks <pkg.origin>
node adapters/story/cli.mjs outline <pkg.origin>
node adapters/story/cli.mjs seq <pkg.origin>
```

Transaction file shape (ch11.json):

```json
{
  "chapter": 11,
  "transaction_id": "ch11-s01",
  "text": "…the chapter's prose…",
  "state_changes": [
    { "object": "obj:black-key", "field": "holder", "from": "char:zhao-qi", "to": "char:lin-zheng", "basis": ["scene:11-07"] }
  ],
  "assertions": ["zhao-qi-alive", "gate-not-opened", "betrayal-undisclosed"],
  "hooks": [{ "id": "hook:new-mystery", "summary": "…", "status": "planted_unresolved", "setup": { "chapter": 11 } }]
}
```

## The five gates (all must pass before commit)

| # | Gate | What it catches |
|---|---|---|
| ① | Non-empty prose | A writing transaction with no prose is not work |
| ② | Structure / references / snapshot isolation | Unknown objects, missing fields, wrong "previous value" (downgraded to a warning; accumulates into the "model memory-drift rate") |
| ③ | Forbidden-zone constraints | Zones declared in the world spec (the key must not be used, a key character must not die, the protagonist must not learn secret X…) |
| ④ | Foreshadowing state machine | Illegal hook states; payoffs with no basis (hook-payoff check) |
| ⑤ | Prose-vs-state cross-check | Prose details that contradict state — "swings the knife left-handed", "opens the gate at noon" (CED rule scan) |

Plus **model self-reported assertion review**: the `assertions` in a transaction are
the AI's signed receipts ("I guarantee Zhao Qi is alive", "I guarantee the key was
never used") — each one is machine-verified.

## World spec (specDir) conventions

```
specDir/
├── canon/*.jsonl              # initial objects: characters / locations / objects / factions (id prefix = type)
├── narrative/foreshadowing.jsonl  # hooks: id / summary / setup.chapter / payoff.chapter
├── timeline/state-changes.jsonl   # replay history: object / field / from / to / chapter / evidence
└── tasks/*.json               # forbidden_zones (machine_check = machine-decidable constraints)
```

`--until N`: the world is replayed up to chapter N; everything after that is committed
by the author, chapter by chapter, as transactions. Replay history flows into
provenance — `origin why <pkg> obj.field` answers "why is this value what it is".

## Verification

```bash
node adapters/story/selftest.mjs    # 42 assertions
node adapters/story/demo.mjs        # full demo: build package → recover → submit → forbidden-zone rejection → hook graph
```

## Related

- ShadowBench-W: the million-word continuation benchmark (benchmark/shadowbench-w/);
  OriginWriter is that benchmark turned into an engine.
- Benxiang protocol (benxiang-protocol): a persistent object representation layer for
  AI work (Origin IR + semantic transactions + evidence chains).
- Shadow Memory (benxiang-memory): MCP server for project-state persistence — long-form
  writing is one special case of world-state persistence; general project management is another.

---
