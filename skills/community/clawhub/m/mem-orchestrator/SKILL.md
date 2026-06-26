---
name: memory-orchestrator
description: Layered memory orchestration for OpenClaw conversations. Use when implementing or maintaining a memory system that must classify user input by domain, capture preferences/decisions during chat, organize long-term knowledge objects, do summary-first recall, and periodically reflect/compress memory for better future retrieval. Triggers on requests about memory architecture, recall strategy, progressive disclosure, long-term context, cross-topic association, user preference capture, or building an OpenClaw skill/plugin for persistent memory.
---

# Memory Orchestrator

Implement a layered memory system that remembers the right things, loads the least necessary context, and improves over time through reflection.

## Core Model

Represent memory in five layers:

1. **Session state** — current task, active domains, active objects, constraints
2. **Daily raw log** — important interactions and memory-worthy events from the day
3. **Topic index** — summary cards for broad domains. Seed topics like technology/career/investing/research/life/meta are only defaults, not a fixed ontology.
4. **Object store** — durable objects such as papers, concepts, frameworks, decisions, preferences, open questions, notes, people, projects, or any future type that proves useful
5. **Reflection output** — compressed updates that merge duplicates, raise abstraction, and add cross-topic links

Do not use one giant memory file as the primary operating model.

## Default Directory Layout

Use this layout inside the workspace unless the user specifies another storage backend. Treat it as a readable default, not a rigid schema:

```text
memory/
  session-state.yaml
  working-buffer.md
  daily/
    YYYY-MM-DD.md
  topics/
    technology.yaml
    career.yaml
    investing.yaml
    research.yaml
    life.yaml
    meta.yaml
  objects/
    papers/
    concepts/
    frameworks/
    decisions/
    preferences/
    open-questions/
  reflections/
    YYYY-MM-DD.md
  indexes/
    manifest.json
```

## Cost Control Model

Do not run the full memory pipeline on every message.

Use three levels:

1. **Gate only** — cheap check for whether the message is memory-relevant at all
2. **Conditional recall/write** — only when the gate says the message is likely to benefit from memory
3. **Low-frequency reflection** — background/manual maintenance, never every turn

Use `scripts/should_trigger_memory.py` or `scripts/memory_cli.py turn ...` for the default low-cost path.

## Workflow

### 1. Gate the incoming message

Skip memory work for lightweight messages like acknowledgements, simple confirmations, or operational noise.

### 2. Classify the incoming message

Estimate:
- intent: ask | compare | decide | reflect | write-report | update-preference
- domains: one or more of technology/career/investing/research/life/meta
- whether memory recall is needed
- whether the message contains a memory-worthy event

Use `scripts/classify_memory_input.py` for a deterministic rule-based baseline.

### 2. Capture write-ahead events before responding

Before composing the answer, extract memory-worthy events such as:
- explicit preferences
- corrections
- decisions
- stable background facts
- new high-value objects
- relations between known objects

Write them immediately to:
- `memory/session-state.yaml`
- `memory/daily/YYYY-MM-DD.md`

Use `scripts/extract_memory_events.py` and `scripts/apply_memory_events.py`.

### 3. Recall with progressive disclosure

Do not load full memory by default.

Recall in this order:
1. Topic cards only
2. Matching object summaries only
3. Full object details only if needed
4. Adjacent associated objects only if they improve the answer

Use `scripts/recall_memory.py`.

Default retrieval budget:
- topics: top 1-2
- object summaries: top 3-5
- full detail expansions: top 1-2
- associative expansions: top 0-2

### 4. Answer using the smallest sufficient context

Prefer answers grounded in:
- active topic summary
- the best matching object summaries
- any critical stable preferences

Do not stuff the answer prompt with raw daily logs unless the user is explicitly asking for chronology.

### 5. Reflect and compress

Periodically review recent daily logs and update the durable layers.

Reflection should:
- merge duplicate objects
- promote repeated facts into preferences or decisions
- update topic summaries
- infer relations like `similar_to`, `contrasts_with`, `applies_to`, `extends`
- lower the weight of stale or one-off material

Use `scripts/reflect_memory.py`.

## Extensibility Rules

- Do not assume the default topics are exhaustive.
- Add a new topic card when a recurring theme cannot be cleanly routed through existing topics.
- Do not assume the default object types are exhaustive.
- Add a new object subtype directory when repeated objects share a stable shape and retrieval value.
- Prefer human-readable expansion over hidden abstraction.
- When extending the ontology, also update the memory index and README files so the user can inspect the new structure.

## Data Shapes

### Topic card

```yaml
id: research
name: 科研 / 论文 / 方法论
summary: 用户会围绕论文研读、研究方法、观点对比进行持续讨论。
subtopics:
  - llm
  - evaluation
recent_objects:
  - paper/constitutional-ai
linked_topics:
  - technology
  - career
stable_preferences:
  - 先讲核心问题，再展开细节
priority_rules:
  - 当问题涉及论文、方法、实验时优先激活
```

### Object

```yaml
id: paper/constitutional-ai
type: paper
domain: research
title: Constitutional AI
summary: 一篇关于用 AI feedback 替代部分人工 feedback 的论文。
why_it_matters: 对齐训练与偏好学习的重要参照。
tags:
  - alignment
  - preference-learning
status: discussed
confidence: high
last_discussed: 2026-03-30
relations:
  similar_to:
    - paper/rlhf-overview
user_takeaways:
  - 用户更关心训练范式差异而不是宣传式总结
```

### Session state

```yaml
session_id: auto
active_domains:
  - research
active_objects:
  - paper/constitutional-ai
current_goal: 比较方法差异
recent_constraints:
  - 当前回答要技术向
last_updated: 2026-03-30T01:00:00+08:00
```

## Retrieval Rules

Use a mixed ranking score:

```text
final_score =
  0.35 * semantic_similarity
+ 0.20 * domain_match
+ 0.15 * recency_score
+ 0.15 * relation_score
+ 0.10 * user_preference_match
+ 0.05 * stability_score
```

If no semantic model is available, approximate with:
- keyword overlap
- explicit domain routing
- recency decay
- relation count
- preference/tag overlap

## Engineering Rules

- Write first, answer second, when the user reveals durable information.
- Keep topic cards short; they are routing objects, not full notebooks.
- Keep object summaries decisive enough for summary-first retrieval.
- Do not promote every casual message into durable memory.
- Prefer merging and restructuring over endless append-only growth.
- Treat daily logs as raw material, not as the primary retrieval layer.
- Use associative recall only when it materially improves the answer.

## When to create or update objects

Create or update an object when one of these is true:
- the user returns to the same concept across multiple conversations
- the item will likely matter again for future reasoning
- the user asks for comparison, planning, or decision support around it
- the object captures a persistent preference, framework, paper, or decision

Do not create durable objects for:
- one-off factual lookups with no reuse value
- shallow chit-chat
- ephemeral administrative noise

## Scripts

### `scripts/should_trigger_memory.py`
Run a very cheap gate to decide whether the current message should trigger memory work at all.

### `scripts/classify_memory_input.py`
Classify raw user text into intent/domains and whether recall/write is likely needed.

### `scripts/extract_memory_events.py`
Extract structured memory events from a single message or turn transcript.

### `scripts/apply_memory_events.py`
Apply events to session state and daily log, and optionally update topics/objects.

### `scripts/recall_memory.py`
Perform summary-first retrieval across topics and objects, returning a compact JSON payload.

### `scripts/reflect_memory.py`
Read recent daily logs and produce compressed updates for topics, objects, and relations.

### `scripts/memory_cli.py`
Provide a unified entry point for bootstrap, gate, turn, capture, recall, reflect, and creating new topics/objects.

## References

Read these references when implementing or extending the system:
- `references/file-layout.md` for storage conventions and field semantics
- `references/retrieval-strategy.md` for ranking, recall budgets, and expansion rules
- `references/reflection.md` for compression and promotion rules
- `references/openclaw-integration.md` for how to wire this into OpenClaw workflows
- `references/object-models.md` for current topic/object/session schemas and extension rules

For broader maintainability, also read:
- `ARCHITECTURE.md`
- `ROADMAP.md`
- `EXAMPLES.md`
