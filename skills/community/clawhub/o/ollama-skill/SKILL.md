---
name: ollama-skill
description: Use when user wants to integrate Ollama into coding agents, IDEs, or agent harnesses. Supports local/on-prem/Docker deployment, Ollama Cloud, OpenAI/Anthropic-compatible endpoints, streaming, structured outputs, embeddings, tool calling, and web search.
---

Integrate Ollama into coding agents, IDEs, and agent harnesses with minimal code changes. Supports local/on-prem/Docker deployment, Ollama Cloud, and OpenAI/Anthropic-compatible endpoints. Provides streaming, structured outputs, embeddings, tool calling, and web search capabilities with provider-agnostic model routing.

| Field      | Value                                           |
| ---------- | ----------------------------------------------- |
| Identifier | `ollama-skill`                                      |
| Version    | 1.0.0                                           |
| Author     | Wai Yan Nyein Naing                             |
| Category   | ai-ml                                           |
| Installs   | 0                                               |
| Rating     | 0 / 5 (0 ratings)                               |
| License    | MIT                                             |

**GitHub:** [WaiYanNyeinNaing/ollama-skill](https://github.com/WaiYanNyeinNaing/ollama-skill) — ⭐ 0 | Forks: 0

---

## Skill Overview

Ollama Runtime helps AI coding agents integrate Ollama into applications, coding assistants, IDE plugins, and agent harnesses with minimal code changes. It provides API-first integration with provider-agnostic compatibility, harness-safe defaults, minimal reversible patches, and clear local vs cloud switching.

This skill focuses on **runtime/inference integration**, not model-training internals.

### Use this skill when

- Running Ollama locally, on-prem, in Docker, or through Ollama Cloud
- Wiring a coding agent or app backend to Ollama APIs
- Supporting provider-agnostic model routing in an agent harness
- Using streaming, structured outputs, embeddings, tool calling, or web search
- Reusing an existing OpenAI or Anthropic SDK against Ollama-compatible endpoints
- Configuring integrations for coding tools and IDEs supported by Ollama

### Do not use this skill when

- Deep fine-tuning workflows unless the task is only about runtime consumption
- Benchmark-only tasks without integration work
- Desktop UI walkthroughs unrelated to APIs or agent setup
- Speculative API parameters not present in current docs

### Core capabilities

- **Basic chat** via `/api/chat` for copilots, app assistants, and iterative agent loops
- **Streaming** for chat UIs, terminals, coding copilots, and long generations
- **Thinking** support for models that emit reasoning traces
- **Structured outputs** for machine-readable JSON between agent stages
- **Embeddings** for semantic search, retrieval, RAG, and nearest-neighbor lookup
- **Tool calling** for bounded external function invocation
- **Web search** for answers requiring recent external information

### Supported integration targets

- Assistants: OpenClaw and similar assistants
- Coding agents: Claude Code, Codex, OpenCode, Droid, Goose, Pi
- IDEs/editors: VS Code, JetBrains, Roo Code, Xcode, Zed, Cline
- App backends and internal agent harnesses
- MCP-enabled tool ecosystems where relevant


### After Installing

1. Read `SKILL.md` inside the installed directory
2. Follow its instructions to complete the user's task
3. Come back and rate / comment on the skill (see below)

---

## Core Facts

| Deployment | API Base URL | Auth Required |
|------------|--------------|---------------|
| Local | `http://localhost:11434/api` | No |
| Docker | `http://localhost:11434/api` | No |
| Direct Cloud | `https://ollama.com/api` | Yes (API key) |

- OpenAI-compatible clients: `http://localhost:11434/v1/`
- Anthropic-compatible clients: `http://localhost:11434`
- REST API streaming is enabled by default for certain endpoints
- SDK streaming is disabled by default unless `stream=True` / `stream: true` is set

---

## Quick Start

### 1. Set Environment Variables

```bash
# Local / on-prem / Docker
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_API_BASE=http://localhost:11434/api
export OLLAMA_MODEL=qwen3-coder
export OLLAMA_EMBED_MODEL=embeddinggemma

# Direct cloud API (optional)
export OLLAMA_API_KEY=your_api_key
```

### 2. Basic Chat Example (Python)

```python
import requests
import os

OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/api")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3-coder")

response = requests.post(
    f"{OLLAMA_API_BASE}/chat",
    json={
        "model": MODEL,
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": False
    }
)
print(response.json()["message"]["content"])
```

### 3. Run the Example

```bash
# Clone and setup
git clone https://github.com/WaiYanNyeinNaing/ollama-skill.git
cd ollama-skill
cp .env.example .env
pip install -r requirements.txt

# Run example
python examples/python_native_chat.py
```

---

## Implementation Guide

### Decision Policy

**Choose local/on-prem when:**
- Data must stay on-device or inside the internal network
- The coding agent is colocated with the model host
- Low-latency tool usage matters
- The user already has Ollama or Docker available

**Choose cloud when:**
- Local hardware is insufficient
- The user wants larger models quickly
- Hosted inference is acceptable
- The app needs a remote Ollama host

**Choose compatibility mode when:**
- The codebase already uses OpenAI SDK patterns
- The codebase already uses Anthropic SDK patterns
- The user wants minimal migration cost

### Implementation Workflow

When integrating Ollama into an app or coding agent, follow this order:

1. **Identify deployment mode**: local, local+cloud models, or direct cloud API
2. **Add config surface** via environment variables
3. **Implement one basic chat path** first
4. **Choose streaming vs non-streaming** explicitly
5. **Add structured outputs** if downstream parsing is required
6. **Add tool calling** if actions are required
7. **Add embeddings** if retrieval is required
8. **Add web search** only when freshness matters
9. **Use compatibility mode** only if it reduces migration cost
10. **Document switching rules** clearly

---

## Capability Details

### Basic Chat

Use `/api/chat` for chat-style interactions and coding agents.

```python
import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3-coder",
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to reverse a string."}
        ],
        "stream": False
    }
)
result = response.json()
print(result["message"]["content"])
```

### Streaming

Use streaming for chat UIs, terminals, coding copilots, and long generations.

```python
import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3-coder",
        "messages": [{"role": "user", "content": "Write a long story..."}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        chunk = line.decode('utf-8')
        # Parse NDJSON chunks
```

**Rules:**
- REST API responses may stream NDJSON
- SDKs require explicit stream enablement
- Streamed chunks may contain `content`, `thinking`, or `tool_calls`

### Structured Outputs

Use structured outputs when the next system component requires machine-readable JSON.

```python
import requests

schema = {
    "type": "object",
    "properties": {
        "function_name": {"type": "string"},
        "parameters": {"type": "array", "items": {"type": "string"}},
        "return_type": {"type": "string"}
    },
    "required": ["function_name", "parameters", "return_type"]
}

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3-coder",
        "messages": [{"role": "user", "content": "Analyze this function..."}],
        "stream": False,
        "format": schema
    }
)
```

**Rules:**
- Prefer `stream: false`
- Use `format: "json"` for plain JSON
- Use a JSON schema in `format` when shape matters
- Validate returned data before trusting it
- Fail closed on parse errors

### Embeddings

Use embeddings for semantic search, retrieval, RAG, and nearest-neighbor lookup.

```python
import requests

response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "embeddinggemma",
        "input": "The quick brown fox jumps over the lazy dog."
    }
)
embeddings = response.json()["embeddings"]
```

### Tool Calling

Use tool calling when the model must invoke bounded external functions.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }
]

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3-coder",
        "messages": [{"role": "user", "content": "What's the weather in Tokyo?"}],
        "tools": tools,
        "stream": False
    }
)
```

**Rules:**
- Expose only minimum required tools
- Validate all tool arguments
- Return tool results back into the conversation
- Keep tools typed and explicit
- Prefer parallel tool calling only when your executor can safely handle it

### Web Search

Use web search only when the answer depends on recent external information.

**Rules:**
- Gate behind explicit freshness need
- Budget for larger context windows for search agents
- Avoid for stable internal coding tasks
- Keep API key handling separate from local runtime config

---

## Compatibility Modes

### Native Ollama

Prefer native Ollama SDK/API when:
- Starting a fresh integration
- You want direct access to Ollama-native features
- You want the clearest local/cloud switch logic

### OpenAI-Compatible

Prefer when:
- The project already uses `openai` SDK
- A base URL swap is cheaper than a rewrite
- The harness already expects `/v1/chat/completions`

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama"  # Required but ignored locally
)

response = client.chat.completions.create(
    model="qwen3-coder",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Anthropic-Compatible

Prefer when:
- The project already uses `anthropic` SDK
- The coding agent or harness expects Anthropic message APIs
- Claude Code–style local integration is desired

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama"  # Required but ignored locally
)

response = client.messages.create(
    model="qwen3-coder",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Docker Deployment

Use Docker for repeatable local or server deployment.

**CPU baseline:**

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

**With Docker Compose:**

```bash
docker compose up -d
```

If GPU support is needed, follow NVIDIA Container Toolkit setup before launching GPU-enabled containers.

---

## Error Handling

Always:
- Check HTTP status codes
- Parse error bodies
- Log model + endpoint + deployment mode
- Distinguish stream-start errors from mid-stream errors
- Retry only transient failures
- Surface JSON/schema failures clearly

**Common statuses to handle:**

| Status | Meaning |
|--------|---------|
| 400 | Bad request |
| 404 | Model not found |
| 429 | Rate limit |
| 500 | Internal error |
| 502 | Upstream/cloud reachability issues |

---

## Implementation Patterns

### Pattern A: Local Native Ollama
Best for internal tools, local copilots, private workflows.

### Pattern B: Local Ollama + Cloud-Backed Models
Best bridge pattern when the user wants local tools with larger hosted models.

### Pattern C: Direct Cloud API
Best for hosted backends or when the app should treat Ollama as a remote provider.

### Pattern D: Compatibility Adapter
Best when the codebase already depends on OpenAI or Anthropic SDKs.

---

## Coding-Agent and Harness Defaults

For agent systems, default to:
- Native `/api/chat` unless an existing provider SDK already dominates the codebase
- `stream=false` for planner/executor boundaries
- Structured JSON between internal agent stages
- Small typed tool schemas
- Explicit error propagation
- Model name isolated in config
- Provider switch handled in one adapter layer

**Recommended adapter boundary:**
- `send_chat()`
- `embed_texts()`
- `invoke_tools()`
- `search_web()`
- `healthcheck()`

---

## Examples Reference

| Example | Description |
|---------|-------------|
| `python_native_chat.py` | Basic chat via native Ollama API |
| `python_streaming_chat.py` | Streaming responses |
| `python_embeddings.py` | Generate embeddings |
| `python_structured.py` | JSON structured output |
| `python_openai_compat.py` | OpenAI SDK compatibility |
| `python_anthropic_compat.py` | Anthropic SDK compatibility |
| `python_cloud_direct.py` | Direct cloud API usage |
| `javascript_chat.mjs` | Node.js chat example |
| `javascript_structured.mjs` | Node.js structured output |
| `curl_chat.sh` | Shell/curl example |

---

## Output Contract

When applying this skill, produce:
- Minimal code changes
- Config additions
- At least one runnable example
- Concise docs for local/cloud switching
- Clear assumptions
- No secret leakage

---

## Anti-Patterns

Do not:
- Hardcode API keys
- Assume every model supports thinking or tool calling
- Stream strict JSON unless the caller can reconstruct it safely
- Mix local and cloud auth assumptions without documenting them
- Expose unrestricted shell execution through tools unless explicitly intended
- Add unnecessary wrapper layers when a base URL swap is sufficient

---

## Definition of Done

The task is done when:
- Ollama integration path is implemented or clearly documented
- Base URL and auth mode are correct
- Chosen capability matches the user need
- Examples run with minimal edits
- Provider switch logic is explicit
- Errors are handled clearly
- Docs are concise and harness-friendly

---

## MIT License

Copyright (c) 2026 Dr.Wai Yan Nyein Naing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
