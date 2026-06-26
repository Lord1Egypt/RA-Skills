# Troubleshooting — Ollama Memory Setup

## 1. `memory_search` still says disabled

Check provider status:

```bash
openclaw memory status --deep
openclaw config get agents.defaults.memorySearch
```

Expected config:

```json
{
  "enabled": true,
  "provider": "ollama",
  "model": "nomic-embed-text",
  "remote": { "baseUrl": "http://localhost:11434" }
}
```

Then restart and reindex:

```bash
openclaw gateway restart
openclaw memory index --force
```

Also start a fresh chat/session if the current session cached old state.

## 2. Ollama is not reachable

```bash
curl -s http://localhost:11434/api/tags
```

macOS:

```bash
brew services restart ollama
```

Linux:

```bash
systemctl --user restart ollama 2>/dev/null || sudo systemctl restart ollama 2>/dev/null || ollama serve
```

If Ollama was installed as a desktop app, open it once and retry.

## 3. Model missing

```bash
ollama list
ollama pull nomic-embed-text
```

If `nomic-embed-text` fails, update Ollama and retry.

## 4. OpenClaw config command fails

First validate the CLI and config path:

```bash
openclaw config file
openclaw config validate
openclaw config set --help
```

If your installed CLI is older than your config file, update OpenClaw before writing config. Do not hand-edit config unless you have a backup.

## 5. Search works but results are bad

Reindex:

```bash
openclaw memory index --force
```

Then query with a specific concept that exists in memory. Bad query:

```text
test
```

Good query:

```text
Caresys DB auth Railway credentials issue
```

If results are still poor, check that the indexed files actually contain the information.

## 6. Search is slow

First query can be slow because Ollama loads the model. Subsequent queries should be faster.

If every query is slow:

- keep Ollama running as a service
- close heavy local chat models
- use `nomic-embed-text` instead of a large embedding model
- run `openclaw memory status --deep` to inspect provider latency

## 7. Security warning: exposed Ollama

Do not expose Ollama publicly.

Bad:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Acceptable only behind a trusted private VPN/firewall. For local memory search, prefer:

```text
http://localhost:11434
```


## 8. Quality test says noisy

Run the test with topics you know exist in your memory files:

```bash
bash scripts/check-ollama-memory.sh --quality-test \
  --query="exact project or decision name" \
  --query="specific bug you solved"
```

If generic queries are noisy but specific queries work, the system is healthy. Semantic search is not magic; it still needs meaningful queries and indexed source files.


## 9. Script refuses my base URL

The helper intentionally accepts only localhost, loopback, `.local`, or private LAN Ollama URLs. This prevents accidental use of a public Ollama endpoint.

Preferred:

```text
http://localhost:11434
```

If you need a remote host, put it behind a trusted VPN/private network and review the script before changing the allowlist.


## 10. Sensitive quality-test queries

The script deletes its temp result files on exit, but query strings and excerpts can still appear in terminal output, shell scrollback, CI logs, or agent transcripts. For sensitive memories, use abstract queries or skip `--quality-test` on shared machines.
