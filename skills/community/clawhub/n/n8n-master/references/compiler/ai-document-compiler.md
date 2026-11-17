# AI Document Compiler

Use this prompt when the user asks to add, absorb, compile, update, or reorganize documentation for `n8n-master`.

The compiler is an AI workflow. Scripts may create inventories and hashes, but they must not decide what a document means or silently generate final wiki knowledge.

## When To Use

- The user adds new docs under `references/source/`.
- The user asks to ingest online API docs with Firecrawl and then compile them.
- The user asks why a card is missing and wants the Skill to learn from source docs.
- Official docs were refreshed and the wiki layer needs updating.
- A real Q&A revealed a reusable node pattern, API detail, or workflow recipe.

## Source First

Before writing any wiki file:

1. Identify the exact source files.
2. Read enough of the source to understand the object model, limits, parameters, and examples.
3. Record the source path in the compiled card.
4. If source material is unclear, mark the compiled card `status: draft` and name the uncertainty.
5. Never invent node parameters, API fields, credentials, permissions, response paths, or limits.

## Classification

Classify each source into one primary output type:

| Source kind | Compile to | Examples |
|---|---|---|
| n8n node docs | `references/wiki/nodes/` | HTTP Request, Webhook, Google Sheets, Slack Trigger |
| n8n concept docs | `references/wiki/concepts/` | expressions, item linking, binary data, queue mode |
| external API docs | `references/wiki/api-cards/` | Feishu Base add record, Stripe create payment link |
| reusable workflow | `references/wiki/recipes/` | webhook to Base, API pagination, human review queue |
| useful Q&A | `references/wiki/qa/` | real solved issue, verified troubleshooting answer |
| raw-only material | keep in `references/source/` | release notes, large archive, docs not yet understood |

If a document covers multiple concerns, write one primary card and link to follow-up cards instead of stuffing everything into one long file.

## Card Rules

Every compiled wiki card should include:

```yaml
---
title: Short title
type: node-card | concept-card | api-card | recipe | qa
status: draft | stable
updated: YYYY-MM-DD
source: official-doc | source-doc | local-verification | qa
tags: [...]
---
```

Body order:

1. `# Title`
2. `## 何时读取`
3. `## 核心要点`
4. Task-specific sections:
   - Node card: parameters, operations, credentials, input/output, common issues.
   - API card: endpoint, auth, params, body, n8n HTTP Request config, response paths, permissions/pitfalls.
   - Concept card: definition, decision rules, examples, common mistakes.
   - Recipe: node chain, data contract, key expressions, error handling, source cards.
5. `## 来源`

Keep cards compact. Link back to source files for full detail.

## Index Updates

After writing or changing cards, update the relevant index:

- `references/wiki/index/ALL-Nodes.md`
- `references/wiki/index/ALL-Concepts.md`
- `references/wiki/index/ALL-APIs.md`
- `references/wiki/index/ALL-Recipes.md`
- `references/wiki/index/ALL-QAs.md`

Also append a short entry to:

- `references/wiki/index/Compilation-Log.md`

Do not create platform-specific duplicate indexes such as `ALL-APIs-Feishu.md`. Use tags and table columns inside the single `ALL-APIs.md` instead.

## Future Source Ingestion

When the user provides new docs:

1. Put original files under `references/source/<doc-set>/` or `references/source/api-packs/<platform>/raw/`.
2. If files came from Firecrawl, keep the generated `manifest.json`.
3. Run or update a source inventory only to detect files and hashes.
4. AI reads the new/changed source files.
5. AI writes or updates wiki cards.
6. AI updates indexes and compilation log.
7. AI reports what is compiled, what remains source-only, and what is uncertain.

## Compilation Prompt

Use this exact working prompt internally:

```text
You are the n8n-master documentation compiler.

Goal: turn source documentation into compact, source-grounded wiki cards for future n8n workflow building.

Rules:
- Read the source files first.
- Do not invent parameters, fields, credentials, endpoints, response paths, limits, or examples.
- Prefer several small cards over one large card.
- Keep source files unchanged.
- Mark uncertain content as draft.
- Update all relevant indexes.
- Append to Compilation-Log.md.
- If a source is not worth compiling yet, record it as source-only and explain why.

For each source file or source group:
1. Classify it as node, concept, API, recipe, Q&A, or source-only.
2. Extract only durable operational knowledge.
3. Write the correct wiki card.
4. Include local source paths.
5. Update indexes.
6. Report compiled files and gaps.
```
