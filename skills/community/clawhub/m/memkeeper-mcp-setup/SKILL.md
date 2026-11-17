---
name: memkeeper-openclaw
description: Install, configure, verify, or remove local-first Memkeeper memory for OpenClaw. Use when an OpenClaw user needs Memkeeper's local embedding and reranking models, a safe MCP tool profile, or diagnosis of a failed Memkeeper MCP connection.
---

# Memkeeper for OpenClaw

Configure Memkeeper as a local stdio MCP server. Keep embedding and reranking
local by default. Do not select an OpenClaw reasoning model, configure a model
provider, install a Gateway service, or enable a messaging channel unless the
user explicitly asks.

## Set up local semantic memory

Use a user-level store unless the user requests project isolation.

```bash
MEMKEEPER_BIN="${MEMKEEPER_BIN:-$HOME/.local/bin/memkeeper}"
MEMKEEPER_STORE="${MEMKEEPER_STORE:-$HOME/.memkeeper/store.sqlite}"
```

If `MEMKEEPER_BIN` is absent, download the public installer to a temporary file,
inspect it, and run it. Do not paste secrets into a command or config file.

```bash
curl -fsSL https://raw.githubusercontent.com/teflon07/memkeeper/main/install.sh \
  -o /tmp/memkeeper-install.sh
bash /tmp/memkeeper-install.sh
```

Download the local models, initialize the store, and require semantic retrieval:

```bash
"$MEMKEEPER_BIN" pull-models
"$MEMKEEPER_BIN" init --store "$MEMKEEPER_STORE" --json
MEMKEEPER_REQUIRE_SEMANTIC=1 \
  "$MEMKEEPER_BIN" doctor --store "$MEMKEEPER_STORE" --json
```

Require the final doctor output to report semantic models as ready. Treat a
missing model as a setup failure, not as permission to use lexical fallback.

## Register the MCP server

Register Memkeeper through OpenClaw's MCP command. Expose the tested 12-tool
profile first:

```bash
openclaw mcp add memkeeper \
  --command "$MEMKEEPER_BIN" \
  --arg mcp \
  --env "MEMKEEPER_STORE=$MEMKEEPER_STORE" \
  --env "MEMKEEPER_REQUIRE_SEMANTIC=1" \
  --include "stats,search,get,memory_list,entity_search,graph_neighbors,graph_context,dream_graph,remember,pack,candidate_submit,candidate_list" \
  --timeout 30 \
  --connect-timeout 30
```

Keep `forget`, `entity_upsert`, `relationship_upsert`, and `verify` disabled
until the operator explicitly needs deletion or direct graph/metadata mutation.

## Verify and report

Prove the live stdio connection after registration:

```bash
openclaw mcp doctor memkeeper --probe --json
```

Report the configured store path, enabled tool count, and probe result. Do not
print stored memory contents, API keys, tokens, or other sensitive environment
values.

The MCP connection test does not require an OpenClaw reasoning provider, a
Gateway daemon, or messaging channels. Those are independent, user-selected
choices.

## Handle non-local embedding only on request

Do not change the local mxBai embedding and reranking defaults without explicit
operator direction. An API embedding or reranking provider receives memory text
outside the machine and changes the store's vector backend. Use a separate store
or deliberately re-embed before switching.

For removal, unregister the MCP server with `openclaw mcp unset memkeeper`.
Leave the local store and models in place unless the user explicitly requests
their removal.
