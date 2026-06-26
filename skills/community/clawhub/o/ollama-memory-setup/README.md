# 🧠 Ollama Memory Setup

**Local semantic memory for OpenClaw in ~5 minutes — no API key, no cloud embeddings, no `node-llama-cpp` pain.**

OpenClaw memory is much stronger when it can search by meaning instead of exact keywords. This skill sets up Ollama as the local embedding backend, usually with `nomic-embed-text`, and includes checks for setup quality.

## Use This When

- `memory_search` is disabled or returns no semantic results
- OpenClaw complains about `node-llama-cpp` or local embeddings
- You want private local embeddings instead of hosted APIs
- You need to diagnose whether memory search is connected, indexed, and useful

## What It Does

- Checks whether Ollama is installed and reachable
- Pulls the embedding model if missing
- Configures `agents.defaults.memorySearch.*` for OpenClaw
- Rebuilds/validates the memory index
- Runs optional quality tests against real memory topics
- Keeps defaults private: `localhost` only unless you intentionally override

## Quick Start

```bash
bash scripts/check-ollama-memory.sh --install --apply-config
openclaw gateway restart
openclaw memory index --force
openclaw memory status --deep
bash scripts/check-ollama-memory.sh --quality-test --query="known memory topic"
```

Expected result:

```text
provider: ollama
model: nomic-embed-text
semantic search: enabled
memory_search(...) returns relevant hits
```

## Side Effects Are Explicit

Default mode is diagnostic only. These flags change things:

| Flag | Side effect |
|---|---|
| `--install` | May install/start Ollama and pull the embedding model |
| `--apply-config` | Writes OpenClaw memory config |
| `--quality-test` | Runs read-only memory searches and prints sample result lines |

Avoid sensitive query terms if terminal logs are captured.

## Manual Config

```json
{
  "agents.defaults.memorySearch.enabled": true,
  "agents.defaults.memorySearch.provider": "ollama",
  "agents.defaults.memorySearch.model": "nomic-embed-text",
  "agents.defaults.memorySearch.remote.baseUrl": "http://localhost:11434"
}
```

## Security Notes

- Keep Ollama on `localhost` or a trusted private network
- Do not expose port `11434` publicly
- Do not paste API keys or private memory snippets into bug reports
- Review custom `--model` and `--base-url` values before letting an agent apply them

## Quality Test

Connectivity is not enough. Prove retrieval quality:

```bash
bash scripts/check-ollama-memory.sh --quality-test \
  --query="project decision" \
  --query="bug fix learning" \
  --query="open todo"
```

The script classifies searches as `OK`, `noisy`, or `broken`.

---

*by brasco05 · local/private semantic memory for OpenClaw*
