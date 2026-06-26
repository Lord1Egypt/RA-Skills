# OpenClaw Integration

## Goal

Use this skill inside an OpenClaw workspace without requiring a separate external service.

## Recommended Integration Pattern

### 1. Local file memory as system of record
Store durable memory in workspace files under `memory/`.

### 2. Use the skill as an operating procedure
The skill tells the agent when and how to:
- classify input
- write memory events
- do summary-first recall
- reflect and compress

### 3. Optional helper scripts
Use the bundled scripts for deterministic parts:
- event extraction
- file creation/update
- retrieval packaging
- reflection summaries

### 4. Use `memory_search` only as one recall path
OpenClaw's `memory_search` is still useful for semantic recall over MEMORY.md and memory/*.md, but for this system it should not be the only index. The skill's own topic/object layout should shape what is searched and read.

## Suggested Runtime Flow

1. User message arrives
2. Run classifier
3. If message contains durable info, run WAL capture
4. If recall is needed, run summary-first retrieval
5. Answer
6. Periodically run reflection script out of band or during heartbeat/maintenance turns

## Safe Adoption Path

### Phase 1
- Create topic cards
- Create object directories
- Start writing daily logs and session state
- Use retrieval script manually

### Phase 2
- Add reflection job
- Add relation inference
- Add manifest/index generation

### Phase 3
- Add embeddings/vector backend if desired
- Add stronger reranking and cross-domain analogies

## Important Constraint

Do not let memory architecture force verbose answers. The user explicitly prefers concise responses and does not want low-value daily reports.
