# Install and Smoke Test

## Install Strategy

Use the official Ollama installer or package flow for the user's operating system instead of ad hoc third-party scripts.
After installation, verify the binary first:

```bash
ollama --version
```

## Minimum Local Smoke Test

Start with the smallest proof that the runtime works:

```bash
ollama list
curl -s http://127.0.0.1:11434/api/tags | jq '.models | length'
```

If no local service is running yet, start it in the foreground for verification:

```bash
ollama serve
```

In another shell, verify generation with an exact model tag:

```bash
ollama pull MODEL:TAG
ollama run MODEL:TAG "Reply with exactly: OK"
```

## Acceptance Checks

A healthy first setup should confirm:
- `ollama --version` returns normally
- the API responds on `127.0.0.1:11434`
- at least one model is pulled successfully
- one local generation completes end to end
- `ollama ps` shows where the model is loaded when performance matters

## Remote or Server Notes

For remote hosts, verify local health before changing bind address, firewall rules, or reverse proxies.
Never expose port `11434` outside localhost until the local smoke test is clean and the user explicitly approves remote access.
