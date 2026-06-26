# Cortex Memory Agent Manual

## Goal

Use Cortex Memory as a long-term memory layer in OpenClaw. This manual is for agents operating from the independent `cortex-memory` skill folder.

## Phase 1: Plugin Availability Check

Run:

```bash
openclaw plugins list
openclaw plugins inspect openclaw-cortex-memory
```

If plugin exists and is enabled, continue to Phase 3.

If plugin is missing or disabled, go to Phase 2.

## Phase 2: Install and Enable Plugin

Preferred install path (README default):

```bash
openclaw plugins install clawhub:openclaw-cortex-memory
openclaw plugins enable openclaw-cortex-memory
```

Fallback install path:

```bash
npm pack openclaw-cortex-memory@0.1.0-Alpha.34
openclaw plugins install ./openclaw-cortex-memory-0.1.0-Alpha.34.tgz
openclaw plugins enable openclaw-cortex-memory
rm ./openclaw-cortex-memory-0.1.0-Alpha.34.tgz
```

Then verify:

```bash
openclaw plugins list
openclaw plugins inspect openclaw-cortex-memory
```

If config is not ready, apply the baseline from `configuration.md`.

Exclusive memory mode pre-install check (must be completed before running install commands, including `openclaw plugins install ./openclaw-cortex-memory-0.1.0-Alpha.34.tgz`):

- Before install, do not manually set `plugins.slots.memory` to `openclaw-cortex-memory`.
- Before install, disable `memory-core` and `memory-lancedb` under `plugins.entries` to avoid mixed backends.
- After install, the installer may set `plugins.slots.memory` to `openclaw-cortex-memory` automatically; this is expected.

If the user asks for "system prompt rules", use `{baseDir}/references/system-prompt-template.md`.

## Phase 3: Runtime Workflow

### Retrieval-first answers

1. `search_memory` with the user query.
2. `query_graph` when relationship/path reasoning is needed.
3. If `query_graph` returns `conflict_hint`, run `list_graph_conflicts` and confirm with user before `resolve_graph_conflict`.
4. Respond with evidence first, reasoning second.

### Persistence

Use `store_event` only for durable information:

- stable preferences
- project decisions
- long-lived constraints

Avoid persisting ephemeral chatter.

### Maintenance

- `sync_memory` for historical import
- `reflect_memory` for rule extraction
- `backfill_embeddings` for vector repair
- `export_graph_view` for status-aware graph snapshots
- `lint_memory_wiki` for projection consistency checks
- `cortex_diagnostics` (or `diagnostics` alias) when anything looks inconsistent

## Failure Handling

If plugin tools are unavailable:

1. Run `openclaw plugins inspect openclaw-cortex-memory` and `openclaw plugins list`.
2. If `cortex_diagnostics` is visible, run it for detailed checks.
3. Explain the issue clearly (plugin disabled, config incomplete, endpoint unavailable, or API key missing).
4. Provide immediate next action with exact command.

If install or enable flow reports `memory-core` / `memory-lancedb` requirements, keep both disabled in `plugins.entries`.  
If the host still requests a `memory-lancedb` schema block, add:

```json
"memory-lancedb": {
  "enabled": false,
  "config": {
    "embedding": {
      "apiKey": "${MEMORY_LANCEDB_API_KEY}",
      "model": "text-embedding-3-small"
    },
    "dbPath": "~/.openclaw/memory/lancedb",
    "autoRecall": true,
    "autoCapture": false,
    "captureMaxChars": 500
  }
}
```

## Operator Commands Cheat Sheet

```bash
openclaw plugins install clawhub:openclaw-cortex-memory
openclaw plugins enable openclaw-cortex-memory
openclaw plugins inspect openclaw-cortex-memory
npm pack openclaw-cortex-memory@0.1.0-Alpha.34
openclaw plugins install ./openclaw-cortex-memory-0.1.0-Alpha.34.tgz
openclaw plugins enable openclaw-cortex-memory
rm ./openclaw-cortex-memory-0.1.0-Alpha.34.tgz
openclaw skills info cortex-memory
openclaw skills check
```
