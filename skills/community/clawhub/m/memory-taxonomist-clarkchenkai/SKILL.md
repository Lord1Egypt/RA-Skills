---
name: memory-taxonomist
description: |
  Memory Taxonomist — Structured Memory Skill for Turning Raw Notes into Stable Knowledge. Use it when the user needs a
  disciplined protocol and fixed output contract for this kind of task rather
  than a generic answer.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Memory Taxonomist — Structured Memory Skill for Turning Raw Notes into Stable Knowledge

Use this skill when the task matches the protocol below.

## Activation Triggers

- new notes or transcripts that mix multiple information types
- agent memory design or memory cleanup work
- meeting outputs that contain decisions, preferences, and open questions together
- requests to store user context safely for future retrieval
- cases where retrieval quality matters more than storage volume

## Core Protocol

### Step 1: Break input into atomic claims

Do not classify a whole paragraph as one memory object when it contains multiple types.

### Step 2: Classify each unit

Sort it into fact, preference, procedure, unresolved question, or exception.

### Step 3: Separate durable from provisional

Do not let recent mention automatically become durable truth.

### Step 4: Flag conflicts and edge cases

Identify contradictions, overrides, and one-off exceptions before writing memory.

### Step 5: Recommend the right storage action

Store, update, deprecate, or hold for clarification based on memory type and certainty.

## Output Contract

Always end with this six-part structure:

```markdown
## Facts
[...]

## Preferences
[...]

## Procedures
[...]

## Unresolved Questions
[...]

## Exceptions
[...]

## Recommended Storage Action
[...]
```

## Response Style

- Prefer clean classification over verbose summary.
- Treat unresolved questions as first-class memory objects.
- Do not convert preferences into universal rules.
- Call out exceptions instead of hiding them in procedures or facts.

## Boundaries

- It does not store everything by default; some information should remain ephemeral.
- It does not confuse recency with importance.
- It does not turn uncertain statements into durable facts without evidence.
