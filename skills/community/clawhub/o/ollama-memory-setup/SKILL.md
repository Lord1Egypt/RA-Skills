---
name: ollama-memory-setup
description: Set up, diagnose, repair, and quality-test private local OpenClaw semantic memory search using Ollama embeddings. Use when memory_search is disabled, node-llama-cpp/local embedding errors appear, the user wants no API-key embeddings, or memory search quality/connectivity needs verification with nomic-embed-text or similar Ollama embedding models.
---

# Ollama Memory Setup

Use this skill to make OpenClaw `memory_search` work locally with Ollama embeddings instead of fragile native `node-llama-cpp` builds or paid hosted embedding APIs.

## What success looks like

A correct setup has all of this:

- Ollama installed and reachable at `http://localhost:11434`
- an embedding model pulled, usually `nomic-embed-text`
- OpenClaw config explicitly sets `agents.defaults.memorySearch.provider` to `ollama`
- memory index rebuilt after config changes
- optional `--quality-test` passes against known memory topics
- `memory_search("...")` or `openclaw memory search "..."` returns results with provider `ollama`


## Side effects and consent

Default script mode is read-only/diagnostic. Side effects require explicit flags:

- `--install`: may install Ollama, start services, and pull a model.
- `--apply-config`: writes OpenClaw `agents.defaults.memorySearch.*` config.
- `--quality-test`: read-only search validation; temp files are deleted on exit, but query text/output may still appear in terminal logs.

Before recommending `--install` or `--apply-config`, tell the user what will change. Do not run those flags silently. Prefer default localhost settings; review/patch the script before letting an agent provide arbitrary `--model` or `--base-url` values.

## Fast path

Prefer the bundled diagnostic script first:

```bash
bash scripts/check-ollama-memory.sh
```

To install/pull the model and print/apply OpenClaw config commands:

```bash
# Diagnostic only first
bash scripts/check-ollama-memory.sh

# Then, with explicit user approval for side effects
bash scripts/check-ollama-memory.sh --install --apply-config
openclaw gateway restart
openclaw memory index --force
openclaw memory status --deep
bash scripts/check-ollama-memory.sh --quality-test --query="known memory topic"
```

If running inside an agent with first-class config tools available, use those for config changes instead of hand-editing JSON.

## Workflow

### 1. Preflight before changing anything

Check:

```bash
command -v ollama
curl -s http://localhost:11434/api/tags
ollama list | grep -E 'nomic-embed-text|qwen.*embedding'
openclaw memory status --deep
```

If Ollama is reachable and the model exists, skip installation and go to config validation.

### 2. Install or start Ollama

macOS:

```bash
brew install ollama
brew services start ollama
```

Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

Do not expose Ollama directly to the public internet. Keep it on localhost, VPN, or private LAN.

### 3. Pull an embedding model

Default:

```bash
ollama pull nomic-embed-text
```

Use `nomic-embed-text` for the lowest-friction setup. Use another embedding model only if OpenClaw/Ollama supports it and the user has a reason.

### 4. Configure OpenClaw memory search

Set this under `agents.defaults.memorySearch`:

```json
{
  "enabled": true,
  "provider": "ollama",
  "model": "nomic-embed-text",
  "remote": {
    "baseUrl": "http://localhost:11434"
  }
}
```

CLI batch form:

```bash
openclaw config set --batch-json '[
  {"path":"agents.defaults.memorySearch.enabled","value":true},
  {"path":"agents.defaults.memorySearch.provider","value":"ollama"},
  {"path":"agents.defaults.memorySearch.model","value":"nomic-embed-text"},
  {"path":"agents.defaults.memorySearch.remote.baseUrl","value":"http://localhost:11434"}
]' --strict-json
```

Then restart the gateway:

```bash
openclaw gateway restart
```

### 5. Reindex and validate

```bash
openclaw memory index --force
openclaw memory status --deep
openclaw memory search "project decision" --max-results 5
```

In-agent validation:

```text
memory_search("a known topic from MEMORY.md")
```

Expected: provider is `ollama`, search is not disabled, and results are semantically relevant. For stronger proof, run:

```bash
bash scripts/check-ollama-memory.sh --quality-test \
  --query="known project decision" \
  --query="known bug fix" \
  --query="known todo"
```

## When to read troubleshooting

Read `references/troubleshooting.md` when:

- `memory_search` still says disabled
- Ollama is installed but not reachable
- the model is pulled but OpenClaw still uses another provider
- indexing is slow or returns no useful results
- config commands fail or the installed OpenClaw CLI is older than the config file

## Safety rules

- Never paste secrets into `openclaw.json` for this setup. Ollama local embeddings do not need real API keys.
- Do not bind Ollama to `0.0.0.0` unless the user understands the network/security risk.
- Do not delete existing memory files to “fix” search. Reindex instead.
- Do not promise semantic quality until a real `memory_search`/`openclaw memory search` validation passes.
