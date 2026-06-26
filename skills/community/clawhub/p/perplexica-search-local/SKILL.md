---
name: perplexica-search
description: AI-powered search using your local Perplexica instance. Runs deep research (quality mode) with web search and LLM reasoning; returns answers with cited sources in OpenClaw while keeping search/RAG state in Perplexica. Use when the user asks to "search with Perplexica", "ask Perplexica", "deep search", "research with sources", or wants AI search with citations. Local-only; no data exfiltration.
version: 1.0.3
homepage: https://github.com/eplt/perplexica-search
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - python3
    install: []
    files:
      - "scripts/*"

---

# Perplexica Search Skill

AI-powered search using your **local** Perplexica instance. This skill calls Perplexica's search API for deep research (quality mode), returns the answer and cited sources in OpenClaw, and leaves search/RAG state in Perplexica. **Local-only**: only `localhost`, `127.0.0.1`, `::1`, or `host.docker.internal` (Docker) are allowed; remote URLs are rejected. HTTP redirects are not followed, so the client cannot be sent to a non-local host.

## When to Use

Use this skill when the user wants to:

- Search the web with AI-powered reasoning
- Get answers with cited sources
- Perform deep research on a topic (use `--mode quality`)
- Search academic papers or discussions
- Use a local, privacy-focused search engine
- Get structured search results with metadata

## Prerequisites

- **python3** (required to run the script)
- Perplexica running locally (default: `http://localhost:3000`)
- At least one chat model provider configured in Perplexica
- At least one embedding model configured

## Usage

Run the script by **path**; do not rely on `cd` to the skill directory. The script finds its config from its own location. Use the skill directory your environment provides (e.g. `{baseDir}` or the path where this skill is installed).

```bash
# Basic search (replace <SKILL_DIR> with the actual skill path, e.g. ~/.openclaw/skills/perplexica-search or {baseDir})
python3 <SKILL_DIR>/scripts/perplexica_search.py "What is quantum computing?"

# Specify optimization mode
python3 <SKILL_DIR>/scripts/perplexica_search.py "Latest AI developments" --mode quality

# Search specific sources
python3 <SKILL_DIR>/scripts/perplexica_search.py "Machine learning papers" --sources academic

# Different local port or Docker host (allowed: localhost, 127.0.0.1, ::1, host.docker.internal)
python3 <SKILL_DIR>/scripts/perplexica_search.py "Climate change research" --url http://127.0.0.1:3000
python3 <SKILL_DIR>/scripts/perplexica_search.py "Query" --url http://host.docker.internal:3000

# JSON output for programmatic use
python3 <SKILL_DIR>/scripts/perplexica_search.py "Python best practices" --json

# Deep research (allow slow chunks, e.g. 5 min between chunks)
python3 <SKILL_DIR>/scripts/perplexica_search.py "Comprehensive review of X" --mode quality --timeout 300

# With conversation history
python3 <SKILL_DIR>/scripts/perplexica_search.py "Explain more" --history '[["human", "What is Python?"], ["assistant", "Python is a programming language..."]]'

# Custom system instructions
python3 <SKILL_DIR>/scripts/perplexica_search.py "Explain Rust" --instructions "Focus on memory safety and performance"

# Minimal output (answer + sources only), e.g. for OpenClaw/agents
python3 <SKILL_DIR>/scripts/perplexica_search.py "Your query" --quiet
```

**If the agent has a skill base path variable** (e.g. `{baseDir}`), use it: `python3 {baseDir}/scripts/perplexica_search.py "query"`. Do not `cd` into the skill directory first; run the script by full path so it works regardless of current working directory and install location.

**Minimal output in OpenClaw:** To avoid extra decorative headers when the runner adds its own messages (e.g. "Exec running/finished", "An async command you ran earlier has completed..."), use `--quiet` or `-q`. That prints only the answer and a compact sources list. The "System: Exec...", "Handle the result internally", and timestamp lines are from OpenClaw, not this skill; they cannot be disabled from the skill.

### CLI Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `query` | | *(required)* | The search query |
| `--url` | `-u` | `http://localhost:3000` | Local Perplexica base URL only (localhost, 127.0.0.1, ::1, or host.docker.internal) |
| `--mode` | `-m` | `balanced` | Optimization mode: `speed`, `balanced`, `quality` |
| `--sources` | `-s` | `web` | Search sources: `web`, `academic`, `discussions` (comma-separated) |
| `--chat-model` | | `auto` | Chat model key (e.g., `gpt-4o-mini`, `llama3.1:latest`) |
| `--embedding-model` | | `auto` | Embedding model key (e.g., `text-embedding-3-large`) |
| `--instructions` | `-i` | `None` | Custom system instructions |
| `--history` | | `None` | Conversation history as JSON array |
| `--json` | `-j` | `off` | Output raw JSON instead of formatted summary |
| `--quiet` | `-q` | `off` | Minimal output: answer and sources only (no decorative headers). Use from OpenClaw/agents to reduce clutter. |
| `--timeout` | | `180` | Seconds to wait between stream chunks (increase if the LLM is slow) |

## How It Works

1. **Validate URL**: Ensures the Perplexica base URL is local only (localhost, 127.0.0.1, ::1, or host.docker.internal); exits with error if not. **Redirects are rejected** so the client never follows a redirect to a remote host.
2. **Fetch Providers**: Calls `/api/providers` to get available chat and embedding models
3. **Auto-Select Models**: If not specified, selects the first available chat and embedding models
4. **Execute Search**: POSTs to `/api/search` with **streaming** (same as the Perplexica web UI), so chunks arrive as they’re generated and long-running quality/deep research does not time out
5. **Format Results**: Displays answer with sources and citations in OpenClaw; search/RAG state remains in Perplexica

## Library / past chats in the Perplexica web UI

Searches run **via this skill (API)** are **not** saved to Perplexica’s “library of past chats and sources.” The Perplexica API uses in-memory sessions only and does not write to the same database the web UI uses for the library. So you will **not** see those API searches in the web UI’s history. To have a search appear in the library, run it in the Perplexica web UI. The skill still returns the full answer and sources in OpenClaw.

## Output Structure

### Human-Readable Summary

```
🔍 Query: What is Perplexica?
⚡ Mode: balanced | Sources: web

📄 Answer:
Perplexica is an AI-powered search engine that...

📚 Sources:
[1] Title - https://example.com/page1
[2] Title - https://example.com/page2
```

### JSON Output

```json
{
  "query": "What is Perplexica?",
  "mode": "balanced",
  "sources": ["web"],
  "answer": "Perplexica is...",
  "sources_used": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "content": "Snippet..."
    }
  ],
  "model_used": "gpt-4o-mini",
  "took_ms": 1234
}
```

## Configuration

Optional: create a `config.json` in the skill directory. **`perplexica_url` must be a local URL only** (localhost, 127.0.0.1, ::1, or host.docker.internal); remote URLs are rejected.

```json
{
  "perplexica_url": "http://localhost:3000",
  "default_chat_model": "llama3.1:latest",
  "default_embedding_model": "nomic-embed-text",
  "default_mode": "balanced",
  "default_sources": ["web"]
}
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/providers` | GET | List available model providers |
| `/api/search` | POST | Execute search query |

## Error Handling

- **Connection Error**: Perplexica instance unreachable — check URL and that it's running. If the agent runs in Docker, try `--url http://host.docker.internal:3000` or `--url http://127.0.0.1:3000`.
- **No Providers**: No chat models configured — configure at least one provider in Perplexica settings
- **Invalid Model**: Specified model not found — use `--json` to see available models
- **Timeout**: The skill uses streaming (like the web UI); `--timeout` is the max seconds to wait between chunks (default 180). If the LLM is slow, use e.g. `--timeout 300`.

## Troubleshooting: "failed 2m" or step failing after curl

- **Do not `cd` into the skill directory.** Some runners run `cd ~/.openclaw/skills/perplexica-search` and then the script; if the skill is installed elsewhere (e.g. by ClawHub under a different path), `cd` can fail or the path may be wrong. **Invoke the script by full path** instead: `python3 /path/to/perplexica-search/scripts/perplexica_search.py "query"` (use whatever path or variable your environment gives for the skill directory, e.g. `{baseDir}/scripts/perplexica_search.py`).
- **Runner timeout:** If the runner has a 2-minute (or other) limit for a single step, a long search can be killed. Use `--mode speed` for faster results, or increase the runner’s tool/step timeout if possible.
- **Check where the skill is installed:** Run `ls ~/.openclaw/skills/` or your ClawHub/OpenClaw skills path; then use that directory in the script path.

## Examples

### Quick Fact Check
```bash
python3 scripts/perplexica_search.py "Who won the 2024 Nobel Prize in Physics?"
```

### Research with Academic Sources
```bash
python3 scripts/perplexica_search.py "Transformer architecture improvements 2024" --sources academic --mode quality
```

### Technical Documentation Search
```bash
python3 scripts/perplexica_search.py "Python async await best practices" --instructions "Focus on Python 3.10+ examples"
```

## Publishing to ClawHub

To publish this skill to ClawHub:

```bash
cd ~/.openclaw/skills/perplexica-search
clawhub publish . --slug perplexica-search --name "Perplexica Search" --version 1.0.0 --changelog "Initial release"
```

## Security & Privacy

- **Local only**: The script accepts only local Perplexica URLs (localhost, 127.0.0.1, ::1, or host.docker.internal for Docker). Remote URLs are rejected. **HTTP redirects are not followed**. **Resolved IPs are validated**: the hostname is resolved and every address must be loopback (127.x, ::1) or private (RFC 1918); if DNS or /etc/hosts points a allowed hostname to a public IP, the script exits with an error. The script uses a request-scoped URL opener (no global `install_opener`), so it is safe to run as a subprocess and does not affect other code if imported.
- **No API keys in skill**: Uses Perplexica's configured providers; API keys are configured in Perplexica, not in this skill.

## Limitations

- Requires Perplexica to be running locally
- Search quality depends on configured models and SearXNG setup
- Streaming mode requires additional client-side handling

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `http://localhost:3000/api/providers` | None | Fetch available model providers |
| `http://localhost:3000/api/search` | Query, model selections, sources | Execute AI-powered search |

All requests go to your local Perplexica instance. Perplexica itself may make external requests to search engines (SearXNG, Tavily, Exa) and LLM providers based on your configuration.

## Implementation notes

- **Run as subprocess**: Invoke the script with `python3 path/to/perplexica_search.py` (not by importing it). The script uses a request-scoped URL opener only; it does not call `install_opener`, so it does not modify global urllib state.
- **Resolved IP check**: Before connecting, the script resolves the hostname and ensures every address is loopback (127.x, ::1) or private (RFC 1918). If DNS or /etc/hosts maps an allowed hostname to a public IP, the script exits with an error. Verify that localhost and your Perplexica host resolve to local or private IPs.
- **Sandboxing**: For higher assurance, run the skill in a network-restricted or sandboxed environment so that only localhost (or your Perplexica host) is reachable.

## Trust Statement

By installing this skill, you trust that: (1) the skill will make HTTP requests only to a local Perplexica instance (URLs are validated to localhost, 127.0.0.1, ::1, or host.docker.internal); (2) resolved IPs are checked (loopback or private only) to mitigate DNS/hosts tampering; (3) HTTP redirects are rejected; (4) the script does not install a global urllib opener (intended to be run as a subprocess: `python3 path/to/perplexica_search.py`). Only install if you are running Perplexica locally. For higher assurance, run in a sandboxed or network-restricted environment.
