---
name: connect-my-tool
description: Write the exact config to point a coding agent, IDE, SDK or framework at Kyma API. Covers Cursor, Cline, Claude Code, Codex CLI, Continue, Roo Code, Aider, OpenClaw, LangChain, the Vercel AI SDK and the raw OpenAI SDK. Use when the user names one of these tools and asks to connect it, add Kyma as a provider, point it at Kyma, or set a base URL and key.
---

# Connect my tool to Kyma API

Kyma is an OpenAI-compatible endpoint (plus an Anthropic-compatible one) in front of open and
frontier models, and a hosted MCP server. Most tools below take a base URL and a key; a few also
speak MCP directly, which needs no key in the config at all.

## Get a key

- No account yet: `https://kymaapi.com/signup?src=skill:connect-my-tool` (starts with free credit).
- Already have one: `https://kymaapi.com/keys?src=skill:connect-my-tool`. Keys start with `kyma-`.

## Steps

1. Identify the tool from the table below. If it is not listed, it almost certainly still works:
   see the [any-OpenAI-client guide](https://docs.kymaapi.com/guides/any-openai-client): base URL
   `https://api.kymaapi.com/v1`, key `kyma-your-api-key`.
2. Write the exact field names and values from that row into the file, env var or settings screen
   the tool reads. Do not rename a field or guess a flag that is not shown here.
3. Recommend a model: if the tool has an agent profile in the table, call
   `https://api.kymaapi.com/v1/models/recommend?agent=<agent>`. If it does not, call
   `https://api.kymaapi.com/v1/models/recommend?usecase=coding` (swap `coding` for another value
   from the response's `available_usecases` if the user's job is not coding). Never pass an
   `agent` value that is not in the table; the endpoint will just fall through to a generic answer.
4. Paste the returned `recommended.model` id (or one of its `alternatives`) into the config.

## OpenAI-compatible tools

| Tool | Where | Fields | Agent profile |
|---|---|---|---|
| **Cursor** | Settings (`Cmd/Ctrl+,`) → search "OpenAI" | API Key `kyma-your-api-key`, API Base URL `https://api.kymaapi.com/v1`, add a custom model id | `cursor` |
| **Cline** | Settings gear → provider "OpenAI Compatible" | Base URL `https://api.kymaapi.com/v1`, API Key `kyma-your-api-key`, Model ID `<model id>`. CLI: `cline auth -p openai -k kyma-your-api-key -m <model> -b https://api.kymaapi.com/v1` | `cline` |
| **Roo Code** | Settings → provider "OpenAI Compatible" | Base URL `https://api.kymaapi.com/v1`, API Key `kyma-your-api-key`, Model ID `<model id>` | `roo-code` |
| **Aider** | Shell env, then run | `export OPENAI_API_KEY="kyma-your-api-key"` and `export OPENAI_API_BASE="https://api.kymaapi.com/v1"`, then `aider --model openai/<model id>` | `aider` |
| **Continue** | `config.yaml` | `provider: openai`, `model: <model id>`, `apiBase: https://api.kymaapi.com/v1`, `apiKey: kyma-your-api-key`, `roles: [chat, edit, apply]` (or `[autocomplete]`) | none, use `usecase=coding` |
| **OpenClaw** | `~/.openclaw/openclaw.json` | Under `models.providers.kyma`: `"baseUrl": "https://api.kymaapi.com/v1"`, `"apiKey": "kyma-your-api-key"`, `"api": "openai-completions"`, a `models` array of `{id, name}`; set `agents.defaults.model.primary` to `"kyma/<model id>"` | `openclaw` |
| **LangChain (Python)** | `ChatOpenAI(...)` | `base_url="https://api.kymaapi.com/v1"`, `api_key="kyma-your-api-key"`, `model="<model id>"` | none, use `usecase=coding` |
| **LangChain (JS)** | `new ChatOpenAI({...})` | `configuration: { baseURL: "https://api.kymaapi.com/v1" }`, `apiKey: "kyma-your-api-key"`, `model: "<model id>"` | none, use `usecase=coding` |
| **Vercel AI SDK** | `npm install @kyma-api/ai-sdk ai` | `import { createKyma } from "@kyma-api/ai-sdk"; const kyma = createKyma({ apiKey: "kyma-your-api-key" })`, or set `KYMA_API_KEY` and import the default `kyma` export; pick a model with `kyma("<model id>")` | none, use `usecase=coding` |
| **OpenAI SDK (Python)** | `OpenAI(...)` | `base_url="https://api.kymaapi.com/v1"`, `api_key="kyma-your-api-key"` | none, use `usecase=coding` |
| **OpenAI SDK (JS)** | `new OpenAI({...})` | `baseURL: "https://api.kymaapi.com/v1"`, `apiKey: "kyma-your-api-key"` | none, use `usecase=coding` |

Any tool reading plain env vars (most CLIs and scripts) takes `OPENAI_API_KEY="kyma-your-api-key"`
and `OPENAI_BASE_URL="https://api.kymaapi.com/v1"`.

## MCP-native tools

These speak MCP directly: no key goes in the config, sign-in happens through OAuth on first use.

- **Claude Code**: `claude mcp add --transport http kyma https://mcp.kymaapi.com/mcp`, then `/mcp` to sign in.
- **Cursor**: one-click at `https://mcp.kymaapi.com/mcp`, or add to `.cursor/mcp.json`: `{ "mcpServers": { "kyma": { "url": "https://mcp.kymaapi.com/mcp" } } }`.
- **Codex CLI**: in `~/.codex/config.toml`: `[mcp_servers.kyma]` then `url = "https://mcp.kymaapi.com/mcp"`; then run `codex mcp login kyma`.
- **Cline**: MCP Servers → Configure MCP Servers: `{ "mcpServers": { "kyma": { "url": "https://mcp.kymaapi.com/mcp", "type": "streamableHttp" } } }`, or `cline mcp add kyma https://mcp.kymaapi.com/mcp --transport streamableHttp --yes`.

MCP gives read tools (catalog, pricing, uptime, spend) plus one chat tool guarded by a spend cap
the user sets on first connect (default $10 / 30 days). For a tool in this section, offer MCP as
the option, and fall back to its OpenAI-compatible config above only if the user does not want to
sign in through OAuth.

## Claude Code needs the bare host

Claude Code reads an Anthropic-shaped API, not the OpenAI-compatible one, and
`ANTHROPIC_BASE_URL` takes the host **without** `/v1` (Claude Code appends the path itself):

```bash
export ANTHROPIC_BASE_URL="https://api.kymaapi.com"
export ANTHROPIC_AUTH_TOKEN="kyma-your-api-key"
```

`https://api.kymaapi.com/v1` here makes every request 404. This is the one tool in this whole
skill whose base URL does not match the OpenAI-compatible one. Recommend a model for it with
`https://api.kymaapi.com/v1/models/recommend?agent=claude-code`.

## Do not

- Do not invent a config field, CLI flag, or file path not shown above or in
  [docs.kymaapi.com/guides](https://docs.kymaapi.com/guides). If the user's tool is not listed and
  is not plain OpenAI-compatible, say so and point at the docs site instead of guessing.
- Do not pass an `agent=` value to `/v1/models/recommend` that is not in the table above.
- Do not name or speculate about which inference backend serves a model.
- Do not hardcode a price or uptime number in your answer; call `/v1/models` or
  `/v1/models/recommend` and quote what comes back.
