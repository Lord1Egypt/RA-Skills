---
name: openclaw-knowledge-runtime
description: Build a standalone layered knowledge runtime with typed links across knowledge entries, entities, memories, and reusable assets. Use when designing or implementing agent memory, knowledge retrieval, memory layers, entity linking, or stable write-back after successful runs.
---

# OpenClaw Knowledge Runtime

## What This Skill Does
Use this skill to design or implement a standalone knowledge runtime that can:

1. Read layered memory and knowledge sources.
2. Retrieve the most relevant knowledge for the current role, objective, and signals.
3. Link knowledge to entities, genes, tasks, and prior events.
4. Write stable findings back after successful runs.

## Why Install It
This skill is useful when an agent already has memories, logs, tasks, and reusable assets, but they are still scattered across unrelated files or stores.

Use it to:

- turn scattered memory into a layered runtime
- add typed links between knowledge, entities, events, and reusable assets
- return a compact retrieval bundle for prompts, ranking, and observability
- keep write-back strict so the store stays durable instead of noisy

## Quick Start
Follow this default sequence:

1. Define the two-axis memory model with layers and scopes.
2. Store `knowledge_entry`, `knowledge_link`, and `entity` records.
3. Build a query from role, objective, direction, and recent signals.
4. Rank candidates, expand one hop through typed links, and trim results.
5. Expose a small output bundle to prompts, task ranking, and dashboards.
6. Write back only stable findings after successful runs.

## Memory Model
Use two axes.

- Layers: `working`, `episodic`, `semantic`, `procedural`, `policy`
- Scopes: `session`, `shared`, `published`

Default placement rules:

- `gene`, `capsule`, `skill`, and reusable playbooks belong to `procedural`.
- Event logs, task outcomes, and run histories belong to `episodic`.
- Stable conclusions and research briefs belong to `semantic`.
- User constraints and system rules belong to `policy`.

## Core Records
The runtime should center on three record types:

- `knowledge_entry`: the main unit of stored knowledge
- `knowledge_link`: a typed relationship between records
- `entity`: the canonical form of a repo, module, topic, paper, person, org, or asset

## Storage
Default files:

- `memory/knowledge/knowledge_store.jsonl`
- `memory/knowledge/knowledge_links.jsonl`
- `memory/knowledge/knowledge_index.json`
- `memory/knowledge/entity_index.json`

## Retrieval Flow
When retrieval is needed:

1. Build the current query from role, objective, direction, query bundle, and signals.
2. Retrieve candidate knowledge from layered sources.
3. Expand one hop through typed links.
4. Return a compact bundle with:
   - `knowledge_hits`
   - `knowledge_bias_tags`
   - `linked_entities`
   - `linked_genes`
   - `memory_layers`
   - `knowledge_context_preview`

## Typed Links
Recommended relations:

- `mentions_entity`
- `supports_gene`
- `derived_from_event`
- `abstracts_task`
- `contradicts`
- `supersedes`
- `same_topic_as`
- `evidence_for`
- `used_by_cycle`

## Write-Back Rule
Only write back stable, high-signal findings.

- Good: validated findings, repeated problem patterns, reusable research summaries
- Bad: raw logs, speculative notes, temporary scratch content

## Adapter Surfaces
Keep the runtime decoupled from any one agent loop. Plug it into host systems through generic adapters:

- `query_builder`: turns role, objective, and signals into a retrieval query
- `retrieval_selector`: ranks hits and prepares the runtime output bundle
- `task_ranker`: adds knowledge relevance into task or action scoring
- `prompt_context`: injects a compact knowledge block into prompts
- `write_back`: records durable findings after successful runs
- `observability`: exposes hit counts, linked entities, and layer coverage to reports or dashboards

## Additional Resources
Use these files:

- `README.md`: overview, use cases, and integration checklist
- `examples.md`: example retrieval, ranking, and write-back flows
- `reference.md`: record schemas, output shape, and adapter details
