# OpenClaw Knowledge Runtime

A standalone skill for designing layered agent knowledge systems with typed links, compact retrieval, and stable write-back.

## When To Use It
Use this skill when you need to:

- build agent memory beyond a single chat transcript
- connect knowledge to entities, tasks, events, genes, or reusable assets
- rank the most relevant knowledge for the current run
- inject a small, prompt-safe knowledge context into downstream actions
- keep observability and write-back consistent across runs

## Core Idea
The runtime uses two axes:

- layer: `working`, `episodic`, `semantic`, `procedural`, `policy`
- scope: `session`, `shared`, `published`

This lets a host system distinguish temporary context from durable conclusions and reusable operating knowledge.

## Main Outputs
The runtime should return a small downstream bundle:

- `knowledge_hits`
- `knowledge_bias_tags`
- `linked_entities`
- `linked_genes`
- `memory_layers`
- `knowledge_context_preview`

## Typical Integration Pattern
Use the runtime as a standalone capability and plug it into a host through adapters:

1. Build a query from role, objective, and recent signals.
2. Retrieve and rank candidate entries.
3. Expand one hop through typed links.
4. Return a compact bundle for prompt building, action ranking, and reporting.
5. Write back only stable findings after a successful run.

## Design Principles

- Prefer canonical entities over raw path fragments or URL fragments.
- Keep raw stores append-friendly and indexes rebuildable.
- Use typed links to connect evidence instead of relying on implicit string overlap.
- Keep retrieval lightweight before introducing heavier infrastructure.
- Treat noisy write-back and noisy entity extraction as retrieval regressions.

## Files

- `SKILL.md`: concise skill instructions
- `examples.md`: example usage patterns
- `reference.md`: record schemas and adapter contract details
