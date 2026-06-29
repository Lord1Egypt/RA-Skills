# ModelBound MCP — Tool Index

All tools are invoked with the same JSON-RPC shape:

```json
{ "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": { "name": "<tool>", "arguments": { ... } } }
```

## Library

- `library.list` — list libraries you can read.
- `library.get` — fetch one library's metadata.

## Skills

- `skills.list` — list `SKILL.md` files in scope.
- `skills.get` — fetch a skill by id or slug.
- `skills.proposeDraft` — propose an edit; returns a `review_url`. **Use instead of `skills.update`.**
- `skills.history` — version history for a skill.

## Rules / Prompts

- `rules.list`, `rules.get` — agent rules (`.cursorrules`, `AGENTS.md`).
- `prompts.list`, `prompts.get` — system / regular prompts.

## Corpus (RAG knowledge base)

- `corpus.list` — list knowledge bases.
- `corpus.search` — hybrid (FTS + reranker) search inside one corpus.
- `corpus.ask` — Q&A with citations.
- `corpus.upload` — add a document (write; confirm first).

## Files (generic accessor)

- `files.list`, `files.get` — works across skills, rules, prompts, corpora.

## Search

- `search.all` — hybrid search across all resource types in scope.
- `search.summary` — reranked top-N answer.

## Agents

- `agents.list`, `agents.get` — saved agent configs.
- `agents.run` — execute an agent (write; confirm first).

## Evals

- `evals.list`, `evals.get`, `evals.run` (write).

## Export / Deploy

- `export.bedrock`, `export.openai`, `export.digitalocean` (write).

## Optimization

- `optimize.tokenAudit` — flag bloated tools.
- `optimize.modelAdvisor` — cheaper-model suggestions.

## Audit

- `audit.recent` — recent events for the active workspace.

## Gateway / Meta

- `gateway.setWorkspace` — scope to a team or repo slug.
- `modelbound.listTools` — list every tool with scope.
- `modelbound.callTool` — invoke any tool by name.
- `help` — plain-English description.
