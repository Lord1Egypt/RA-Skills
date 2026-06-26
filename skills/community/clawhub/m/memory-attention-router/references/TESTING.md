# Testing Guide

Use these tests to verify the optimized skill behavior after installation.

## 1. Install the skill

Place the skill folder at:

```text
<your-openclaw-workspace>/skills/memory-attention-router
```

If you are using this Git repo directly, copy the repo's `skills/` directory so that:

```text
<your-openclaw-workspace>/skills/memory-attention-router/SKILL.md
```

exists exactly at that path.

## 2. Set a clean test database

Use a fresh DB so test runs do not mix with old memory.

```bash
export OC_WS=<your-openclaw-workspace>
export ROUTER="$OC_WS/skills/memory-attention-router/scripts/memory_router.py"
export MAR_DB_PATH="/tmp/memory-attention-router-test.sqlite3"
rm -f "$MAR_DB_PATH"
python3 "$ROUTER" init
```

Pass condition:

- init succeeds
- DB is created at `$MAR_DB_PATH`

## 3. Scenario A: planner reuses durable preference

Add a durable preference:

```bash
python3 "$ROUTER" add --input-json '{
  "memory_type":"preference",
  "abstraction_level":3,
  "role_scope":"global",
  "session_id":"sess_test_a",
  "task_id":"task_test_a",
  "title":"Architecture response style",
  "summary":"Answer architecture explanations in concise English and focus on implementation detail.",
  "details":{"hard_constraint":["Use concise English","Focus on implementation detail"]},
  "keywords":["architecture","concise","implementation"],
  "tags":["preference","style"],
  "importance":0.90,
  "confidence":0.95,
  "success_score":0.90
}'
```

Route a planner packet:

```bash
python3 "$ROUTER" route --input-json '{
  "goal":"Plan backend architecture for an event-driven notification service",
  "step_role":"planner",
  "session_id":"sess_test_a",
  "task_id":"task_test_a",
  "user_constraints":[],
  "recent_failures":[],
  "unresolved_questions":[]
}'
```

Pass condition:

- `packet.hard_constraints` contains the durable style rule
- `packet.selected_memory_ids` is non-empty

## 4. Scenario B: executor preserves preference and procedure

Add a durable execution constraint:

```bash
python3 "$ROUTER" add --input-json '{
  "memory_type":"preference",
  "abstraction_level":3,
  "role_scope":"global",
  "session_id":"sess_test_b",
  "task_id":"task_test_b",
  "title":"Execution output constraint",
  "summary":"Always keep outputs under 3 bullets.",
  "details":{"hard_constraint":["Keep outputs under 3 bullets."]},
  "keywords":["bullets","constraint","output"],
  "tags":["preference","formatting"],
  "importance":0.95,
  "confidence":0.95,
  "success_score":0.95
}'
```

Add a reusable procedure:

```bash
python3 "$ROUTER" add --input-json '{
  "memory_type":"procedure",
  "abstraction_level":2,
  "role_scope":"executor",
  "session_id":"sess_test_b",
  "task_id":"task_test_b",
  "title":"Execution workflow",
  "summary":"Follow the execution workflow and validate the final output.",
  "keywords":["execution","workflow","validate"],
  "tags":["procedure"],
  "importance":0.80,
  "confidence":0.80,
  "success_score":0.85
}'
```

Route an executor packet:

```bash
python3 "$ROUTER" route --input-json '{
  "goal":"Execute the workflow and produce the final output",
  "step_role":"executor",
  "session_id":"sess_test_b",
  "task_id":"task_test_b",
  "user_constraints":[],
  "recent_failures":[],
  "unresolved_questions":[]
}'
```

Pass condition:

- `packet.hard_constraints` contains `Keep outputs under 3 bullets.`
- `packet.procedures_to_follow` contains the execution workflow
- both memories are represented in `packet.selected_memory_ids`

## 5. Scenario C: reflection generates reusable procedure memory

Create reflection plus procedure memory:

```bash
python3 "$ROUTER" reflect --input-json '{
  "session_id":"sess_test_c",
  "task_id":"task_test_c",
  "goal":"Build and verify a memory-routing workflow",
  "outcome":"completed",
  "what_worked":["Add durable memory","Route packet before planning","Inspect selected blocks"],
  "what_failed":["Raw memory dumping"],
  "lessons":["Prefer compact packets over flat retrieval"],
  "next_time":["Store reusable procedures after successful workflows"],
  "create_procedure":true,
  "source_refs":["manual-test"]
}'
```

Route an executor packet:

```bash
python3 "$ROUTER" route --input-json '{
  "goal":"Execute the same memory-routing workflow for a new task",
  "step_role":"executor",
  "session_id":"sess_test_c",
  "task_id":"task_test_c",
  "user_constraints":[],
  "recent_failures":[],
  "unresolved_questions":[]
}'
```

Pass condition:

- `procedures_to_follow` is non-empty
- `pitfalls_to_avoid` includes the reflection lesson or failure pattern

## 6. Scenario D: replacement retires stale preference

Add the old rule:

```bash
python3 "$ROUTER" add --input-json '{
  "memory_type":"preference",
  "abstraction_level":3,
  "role_scope":"global",
  "session_id":"sess_test_d",
  "task_id":"task_test_d",
  "title":"Old style rule",
  "summary":"Use concise English and implementation detail first.",
  "keywords":["style","architecture"],
  "tags":["preference","style"],
  "importance":0.80,
  "confidence":0.90,
  "success_score":0.80
}'
```

Add the replacement rule with `replaces_memory_id` set to the old memory ID.

Pass condition:

- the old memory becomes inactive
- `replaced_by_memory_id` is populated
- `retired_reason` is stored

Use these commands to inspect:

```bash
python3 "$ROUTER" list --limit 50
python3 "$ROUTER" inspect --memory-id <OLD_MEMORY_ID>
```

## 7. Scenario E: contradiction is directional

Add an old summary and a newer summary that contradicts it:

```bash
python3 "$ROUTER" add --input-json '{
  "memory_type":"summary",
  "abstraction_level":2,
  "role_scope":"planner",
  "session_id":"sess_test_e",
  "task_id":"task_test_e",
  "title":"Old routing rule",
  "summary":"Use typed packets for memory routing with compact packet composition.",
  "keywords":["memory","routing","packets","compact"],
  "tags":["summary"],
  "importance":0.95,
  "confidence":0.95,
  "success_score":0.70
}'
```

Then add a new summary with a contradiction edge to the old one.

Route a planner packet for the same task.

Pass condition:

- the newer memory ranks above the stale contradicted memory in `debug.selected_memories`

## 8. Scenario F: graph support helps borderline ranking

Create two similarly relevant procedures:

- one unsupported but with stronger raw importance
- one slightly weaker on metadata but supported by a reflection edge

Route a planner packet.

Pass condition:

- the supported procedure ranks first in `debug.selected_memories`
- the supported procedure appears in `packet.procedures_to_follow`

## 9. Compactness checks

For dense-memory scenarios, inspect:

- `packet.selected_memory_ids`
- `packet.hard_constraints`
- `packet.relevant_facts`
- `packet.procedures_to_follow`
- `packet.pitfalls_to_avoid`

Expected caps:

- selected memories <= 5
- hard constraints <= 4
- relevant facts <= 3
- procedures <= 3
- pitfalls <= 3

## 10. Debugging commands

List memories:

```bash
python3 "$ROUTER" list --limit 50
```

Inspect one memory:

```bash
python3 "$ROUTER" inspect --memory-id <MEMORY_ID>
```

Show recent packets:

```bash
python3 "$ROUTER" packets --limit 10
```

Inspect route trace fields when ranking looks wrong:

- `debug.selected_blocks`
- `debug.selected_memories`

## 11. Optional benchmark harness

If you are using the sibling autoresearch harness in this workspace, you can run the offline benchmark suite against this optimized export with:

```bash
cd /root/.openclaw/personal-assistant-workspace/projects/memory-attention-router-autoresearch
source .venv/bin/activate
python scripts/run_benchmarks.py --split all --router-path ./optimized-skill/skills/scripts/memory_router.py
```

Current expectation for the exported optimized skill:

- 11/11 cases passed
- 30/30 checks passed
