---
name: openclaw-siliconflow-memory
description: Configure OpenClaw semantic memory to use SiliconFlow embeddings through the OpenAI-compatible API, especially `BAAI/bge-m3`. Use when enabling or repairing `memory_search`, replacing a broken embedding provider, switching `agents.defaults.memorySearch` to SiliconFlow, validating `openclaw memory status/index/search`, or adding curated `extraPaths` from external Markdown knowledge bases.
---

# OpenClaw SiliconFlow Memory

## Goal

Configure OpenClaw `memory_search` to use SiliconFlow embeddings reliably, then verify indexing and retrieval.

Use this skill to:

- switch memory embeddings to SiliconFlow
- standardize on `BAAI/bge-m3`
- set `fallback: "none"` for clearer debugging
- add curated external Markdown paths to semantic memory
- diagnose failed indexing or failed retrieval

## Workflow

### 1. Inspect the memory config surface first

Before changing config, inspect the relevant schema paths:

- `agents.defaults.memorySearch`
- `agents.defaults.memorySearch.remote`
- `agents.defaults.memorySearch.extraPaths`

Then inspect the current config with `gateway config.get` so the patch is based on the latest hash.

Important:

- Configure memory under `agents.defaults.memorySearch`, not top-level `memorySearch`.
- For OpenAI-compatible embedding endpoints, set `remote.apiKey` explicitly.

### 2. Apply the recommended memorySearch config

Use `gateway config.patch` and keep the configuration explicit.

Recommended baseline:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "BAAI/bge-m3",
      fallback: "none",
      remote: {
        baseUrl: "https://api.siliconflow.cn/v1/",
        apiKey: "YOUR_SILICONFLOW_API_KEY"
      }
    }
  }
}
```

Why this baseline works well:

- `provider: "openai"` matches SiliconFlow's OpenAI-compatible embeddings API
- `model: "BAAI/bge-m3"` is a strong default for mixed Chinese/English Markdown recall
- `fallback: "none"` avoids silently switching providers during debugging
- explicit `remote.baseUrl` and `remote.apiKey` remove ambiguity

### 3. Add external knowledge paths conservatively

When indexing a local knowledge base, prefer curated paths instead of adding the entire repo at once.

Good first candidates:

- source notes
- concepts
- project overviews
- indexes
- README-style top-level knowledge summaries

Avoid adding these in the first pass unless the user explicitly wants them indexed:

- inbox or capture folders
- daily journals
- templates
- archives
- noisy exports or generated files

Example:

```json5
agents: {
  defaults: {
    memorySearch: {
      extraPaths: [
        "D:/Knowledge/README.md",
        "D:/Knowledge/Notes/02-Sources",
        "D:/Knowledge/Notes/03-Concepts",
        "D:/Knowledge/Notes/05-Projects",
        "D:/Knowledge/Notes/09-Indexes"
      ]
    }
  }
}
```

### 4. Validate in this order

After config reload/restart, validate in a fixed order:

1. `openclaw memory status --deep`
2. `openclaw memory index --force`
3. `openclaw memory search "<known phrase from indexed docs>"`
4. tool-layer `memory_search` with the same query

Success signs:

- `Embeddings: ready`
- `Indexed: N/N files` increases as expected
- `Dirty: no`
- retrieval returns snippets from the intended external paths

### 5. Use known text for verification

Do not validate with vague keywords only.

Prefer a phrase that appears verbatim in the indexed notes, such as:

- a README opening sentence
- a project title
- a section heading
- a unique domain phrase

This makes it easier to distinguish:

- indexing failure
- retrieval quality issues
- query mismatch

## Common failures

### `404 page not found`

Interpret this as: the endpoint likely does not provide embeddings at the configured route.

Typical cause:

- using a chat/completions proxy that does not expose `/embeddings`

Action:

- switch to SiliconFlow's embeddings endpoint
- confirm `remote.baseUrl` is `https://api.siliconflow.cn/v1/`
- confirm the embedding model name is valid

### `fetch failed`

Interpret this as: the request could not complete at all.

Typical causes:

- bad API key
- unreachable endpoint
- transient network issue
- provider auto-detection picked the wrong backend

Action:

- make `provider`, `model`, `remote.baseUrl`, and `remote.apiKey` explicit
- retry `openclaw memory status --deep`

### `EBUSY: resource busy or locked`

Interpret this as: the SQLite memory store is locked during reindex.

Action order:

1. retry the index once after current memory operations settle
2. restart OpenClaw and retry
3. if the lock persists, reboot the machine and retry

Do not assume config is wrong just because reindex failed with `EBUSY`.

## Recommended operating style

- keep the embedding provider explicit
- keep `fallback: "none"` during setup and debugging
- add knowledge paths in small batches
- validate with both CLI and tool-layer retrieval
- prefer high-signal Markdown sources over raw dumps

## Completion checklist

Before declaring success, confirm all of the following:

- SiliconFlow API key is configured
- `BAAI/bge-m3` is active
- `openclaw memory status --deep` shows `Embeddings: ready`
- reindex succeeds
- indexed file count reflects the intended extra paths
- at least one query returns a result from the external knowledge base
