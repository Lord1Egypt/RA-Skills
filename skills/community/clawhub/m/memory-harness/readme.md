---
name: memory-harness
description: Runtime-enforced memory harness for OpenClaw. Implements 3-stage recall (session preflight, triggered recall, pre-execution gate) with intent classification, entity detection, memory compression, and status tracking. This harness runs automatically at the right times - NOT relying on SKILL.md text alone.
---

# Memory Harness

A reliable memory harness that makes byterover recall happen at the right times without running heavy recall on every turn.

## Architecture

```
user_input
  -> intent classification
  -> session preflight (if new session)
  -> conditional targeted recall
  -> planning
  -> pre-execution recall gate (if execution-like)
  -> execution or response
  -> optional writeback
```

## 3-Stage Harness

### Stage 1: Session Preflight

Runs ONLY at the start of a new session.

Fetches:
- active project
- pinned facts
- unresolved items
- recent important entities
- recent session summary

Does NOT fetch:
- full raw history
- large raw memory dumps
- low-signal old notes

Output: compact `session_digest` (hard capped)

### Stage 2: Triggered Recall

Runs targeted byterover recall only when needed.

**Trigger conditions:**
- Continuation words: 続き, 前回, 再開, 引き継ぎ, continue, resume, previous work
- Known entity/project name: ClawHub, OpenClaw, Agent-OS, BOSS-memory-loop, etc.
- Task requires user-specific/project-specific context
- Implementation / modification / design / planning request
- Ambiguous task likely depending on prior context

**Skip conditions:**
- Generic factual Q&A
- Small self-contained questions
- Casual short exchange
- Clearly answerable without prior context

**Recall modes:**
- `preflight_query`: start-of-session only
- `entity_query`: when named entities detected
- `continuation_query`: for previous-session continuation
- `constraint_query`: when advice depends on prior rules
- `pre_execution_query`: immediately before execution

### Stage 3: Pre-Execution Recall Gate

MANDATORY before:
- file edits
- code generation
- architecture proposals
- configuration changes
- planning depending on prior project state
- any meaningful change suggestion

Checks for:
- prior constraints
- unresolved issues
- conflicting past decisions
- project-specific conventions
- safety-sensitive context

## Memory Shaping

Never inject raw byterover results directly.

Pipeline:
1. retrieve
2. rank
3. dedupe
4. compress
5. inject bounded digest

**Hard limits:**
- max_memory_items: 5
- max_digest_lines: 8
- prefer recent + high-signal + tagged items

## Status Tracking

Every recall records one of:
- `not_needed`
- `queried_no_hits`
- `queried_low_confidence`
- `queried_success`
- `query_failed`

## Scripts

### intent-classifier.js

Classifies turn intent as one of:
- `generic_qa`
- `casual`
- `continuation`
- `entity_reference`
- `user_specific_context`
- `implementation_request`
- `design_request`
- `execution_request`

### entity-detector.js

Detects known entities in user input:
- Scans for known entity/project names
- Maps aliases to canonical names
- Returns matched entities for recall routing

### session-preflight.sh

Runs lightweight recall at session start:
- Fetches pinned facts, active project, unresolved items
- Creates compact session_digest
- Hard capped length

### targeted-recall.sh

Runs targeted recall based on intent:
- Takes intent, entities, session state
- Chooses appropriate recall mode
- Returns compressed digest

### pre-execution-gate.sh

Runs before execution-like actions:
- Checks for constraints, conflicts, safety issues
- Returns go/no-go with relevant context

### memory-compress.js

Compresses and dedupes raw memory:
- Ranks by relevance and recency
- Dedupes repeated items
- Hard caps output size

### writeback.sh

Writes high-signal info back to memory:
- Only for important decisions/outcomes
- Skips trivial chat and low-value text

## Configuration

```json
{
  "memory_policy": {
    "preflight_on_session_start": true,
    "preflight_depth": "light",
    "pre_execution_recall": true,
    "max_memory_items": 5,
    "max_digest_lines": 8,
    "trigger_query_if": [
      "mentions_known_project",
      "asks_to_continue_previous_work",
      "requires_user_specific_context",
      "requests_code_design_or_change",
      "contains_known_entity"
    ],
    "skip_query_if": [
      "generic_qa",
      "casual_chat",
      "self_contained_question"
    ]
  }
}
```

## Logging

Structured logs for observability:
- `turn_id`
- `session_id`
- `intent`
- `recall_trigger`
- `recall_mode`
- `recall_status`
- `recall_item_count`
- `injected_item_count`
- `pre_execution_gate`
- `elapsed_ms`

## Known Entities

Default entity list (expandable):
- ClawHub
- OpenClaw
- Agent-OS
- BOSS-memory-loop
- ByteRover
- MISO
- Obsidian
- Telegram

## Continuation Triggers

Japanese: 続き, 前回, 再開, 引き継ぎ, 前の, さっきの
English: continue, resume, previous, earlier, last time, back to

## Success Criteria

- Reliable recall when turn depends on context
- Generic turns stay lightweight
- Execution actions always get constraint check
- Behavior inspectable in logs
- No reliance on SKILL.md text alone
