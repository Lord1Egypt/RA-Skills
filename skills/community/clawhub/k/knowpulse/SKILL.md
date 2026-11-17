---
name: davylab-knowledge-graph
version: 0.1.0
description: "KnowPulse (知脉) by DAVYLAB validates subject-isolated knowledge graphs, traces prerequisite gaps, supports conservative learning diagnostics, and creates prerequisite-first learning paths for AI courses and education workflows."
---
# DAVYLAB Knowledge Graph Skill

## Trigger
Use for DAVYLAB Academy course dependency design, knowledge radar, diagnostic planning, prerequisite discovery, study paths, or curriculum graph validation. Do not use for medical, psychological or high-stakes assessment.

## Procedure
1. Collect `topics` and `dependencies` from an owned or appropriately licensed source; request content provenance and educator-review status when used for instruction.
2. Validate input with `node src/cli.js validate path/to/dataset.json`. Reject validation errors; never silently drop cyclic or cross-subject edges.
3. For prerequisite questions call `ancestors`; for lesson recommendations call `path` (hard edges by default). Distinguish *required* (`hard`) from *suggested* (`soft`).
4. For answer-based screening, use `createSession`, `applyAnswer`, `nextTopic`, and `summarize` in `src/engine.js`; answers are provided as correct/wrong/skip by a separate **verified evaluator**. This skill does not evaluate free-form answers or generate trusted exam items.
5. Label every diagnostic result *screening only — educator review required*. Never infer prerequisite mastery solely from descendant performance.
6. Return structured JSON; the consumer app owns display, storage, login, access control, and data retention.

## Commands
```bash
node src/cli.js validate examples/ai-foundations.json
node src/cli.js ancestors examples/ai-foundations.json ai.agent
node src/cli.js path examples/ai-foundations.json ai.agent
node src/cli.js demo examples/ai-foundations.json ai.agent
node tests/engine.test.js
```

## Data contract
- `topics`: array of `{id:string,subject:string,title:string,level?:string,reviewStatus?:string}`
- `dependencies`: array of `{topicId:string,prerequisiteId:string,strength:"hard"|"soft",reason?:string}`
- IDs must be globally unique; dependencies must refer to existing nodes and stay within a subject.
- `buildGraph(topics, dependencies)` returns indexes and topological ordering.
- `ancestors(graph,id,{includeSoft})`, `learningPath(graph,targetIds,{includeSoft})` return ordered IDs.
- `createSession(graph,targetIds,{confirm})`, `applyAnswer(graph,session,id,result)`, `nextTopic(graph,session)`, `summarize(graph,session)` maintain an auditable immutable session.

## Guardrails
- No original upstream question banks, curriculum mappings, texts or engine code included.
- Do not turn reported `weak` status into a clinical diagnosis or definitive pedagogical judgment.
- Never auto-publish recommendations without reviewed content and product-level QA.
- See `docs/ACCEPTANCE.md` and `docs/P0-ANALYSIS.md`.
