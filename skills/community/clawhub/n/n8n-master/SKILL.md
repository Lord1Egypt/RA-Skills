---
name: n8n-master
description: Answers n8n questions and builds n8n workflows, node configurations, Code node JavaScript, HTTP Request setups, API integrations, toolbox-assisted API tests, and importable workflow JSON. Use when the user asks about n8n concepts, workflow design, node behavior, expressions, debugging, external API integration, automation architecture, or production hardening.
---

# n8n Master

## Purpose

Use this skill to answer n8n questions and produce practical n8n artifacts: workflow designs, node configurations, Code node JavaScript, HTTP Request setups, external API integrations, and importable workflow JSON.

Do not invent node parameters, API fields, permissions, or response paths. Prefer local references first, then official source files. If the references do not support an answer, say what is missing.

## Routing

Start with the narrowest relevant index:

- n8n concepts: `references/wiki/index/ALL-Concepts.md`, then `references/wiki/concepts/`.
- n8n nodes: `references/wiki/index/ALL-Nodes.md`, then `references/wiki/nodes/`.
- External APIs: `references/wiki/index/ALL-APIs.md`, then `references/wiki/api-cards/`.
- Workflow patterns: `references/wiki/index/ALL-Recipes.md`, then `references/wiki/recipes/`.
- Useful Q&A: `references/wiki/index/ALL-QAs.md`, then `references/wiki/qa/`.
- Source index: `references/wiki/index/ALL-Sources.md`. This release is wiki-only and does not bundle raw source corpora.
- Document compilation: `references/compiler/ai-document-compiler.md` when the user asks to absorb, compile, update, or learn from docs.
- Toolbox operations: `references/toolbox/` only when the user explicitly asks to test an API, inspect/create Feishu Base fields, or ingest online docs.

If an index is missing or incomplete, use `rg` over `references/wiki/`. If the user adds new raw docs later, place them under `references/source/` and run the AI compiler workflow.

## Answer Modes

### Concept or Debugging Question

1. Search the relevant index and card.
2. Check source files for fragile details.
3. Answer with source file paths.
4. Separate confirmed facts from inference.

### HTTP Request Node

Use `references/templates/http-node-output.md`.

Include method, URL, auth, headers, query params, body, response paths, and common failure checks. Do not include real secrets. Use credential names or environment variable placeholders.

### Code Node

Use `references/templates/code-node-output.md`.

State the assumed input item structure and execution mode. Return valid n8n items, usually an array of `{ json: ... }` objects for "Run Once for All Items". Avoid unsupported globals unless a local source confirms them.

### Workflow JSON

Use `references/templates/workflow-json-output.md`.

Only output full workflow JSON when the user asks for importable/copy-paste workflow JSON. Keep `active: false`. Use placeholder credential names. Mention that credentials must be bound in n8n after import.

### Production Hardening

Use hardening recipes when the user asks for reliability, auditability, retries, idempotency, human review, safe reruns, or "no silent failure".

Add only the hardening needed for the workflow:

- dedup key and idempotent writes
- run_id and status logging
- retries/backoff for safe operations
- final failure notification
- human review queue for risky failures
- runbook when the workflow is meant to operate long-term

### Toolbox

Toolbox scripts are not part of normal answering. Use them only when explicitly helpful:

- `scripts/toolbox/api_tester.py`: lightweight Postman-like API test and n8n HTTP Request draft.
- `scripts/toolbox/feishu_get_bitable_schema.py`: read Feishu Base field schema.
- `scripts/toolbox/feishu_create_bitable_fields.py`: create Feishu Base fields; default dry-run.
- `scripts/toolbox/firecrawl_ingest_docs.py`: ingest online docs into `references/source/`.

Before running a toolbox script that may touch the network, preserve the local proxy environment. Before write operations, dry-run first unless the user clearly requests execution.

### Document Compilation

When the user adds new docs or asks this skill to learn from source files, do not rely on a script to generate final knowledge. Use `references/compiler/ai-document-compiler.md`.

The AI compiler must read source files, classify them, write compact wiki cards, update `references/wiki/index/ALL-*.md`, and append to `references/wiki/index/Compilation-Log.md`. Scripts may only help with mechanical inventory and hashes.

## Source And Safety Rules

- Never write real tokens, cookies, app secrets, or API keys into outputs, workflow JSON, references, source files, logs, or examples.
- For Feishu tools, use `FEISHU_APP_ID` and `FEISHU_APP_SECRET` from the environment; never print them.
- For Firecrawl, use `FIRECRAWL_API_KEY` from the environment; never print it.
- For writes, deletes, batch updates, external messages, or customer/financial data, prefer dry-run and explicit confirmation.
- If source documents disagree, cite the conflict and avoid pretending it is resolved.
- Keep answers copy-paste practical; avoid long tutorials unless the user asks.
