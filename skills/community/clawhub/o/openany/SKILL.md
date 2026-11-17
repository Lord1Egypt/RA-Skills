---
name: openany
description: Use when the user needs a model, data source, or tool API through OpenAny and has authorized that spend. Connect the lite MCP server, then search_apis, get_api, and run_api only after the user accepts the live price.
metadata:
  openclaw:
    homepage: https://openany.si
    primaryEnv: OPENANY_API_KEY
    requires:
      env:
        - OPENANY_API_KEY
---

# OpenAny

Use this skill when the user wants a model, a data source, or another tool API, and they have authorized OpenAny to charge those calls. Skip it when the task can be finished with local files or tools already connected to this agent.

OpenAny (https://openany.si) is the marketplace for agents: one key for 168+ AI models and 3,200+ APIs. Pay per call, no monthly fee.

## Connect

Add the remote server under `mcp.servers` in `~/.openclaw/openclaw.json`. Set `transport` to `streamable-http`. OpenClaw uses SSE when that field is omitted, and this server does not speak SSE.

```json
{
  "mcp": {
    "servers": {
      "openany": {
        "url": "https://mcp.openany.si/mcp-lite",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer ${OPENANY_API_KEY}"
        }
      }
    }
  }
}
```

Keep the key in the environment OpenClaw reads, under the name `OPENANY_API_KEY`. The header above is a placeholder. Do not paste the key into chat, a prompt, a screenshot, or this file. Do not print the Authorization header.

`tools/list` is public. A successful list does not mean a later call is authenticated, priced, or successful.

This skill connects to `https://mcp.openany.si/mcp-lite`. That server exposes `openany_overview`, `search_apis`, `get_api`, and `run_api`. The same lite server is also documented at `https://mcp.openany.si`. `https://mcp.openany.si/mcp` is a different server that lists each API as its own tool.

## Call order

1. When the user asks what is available, call `openany_overview` first. Present data APIs by category and AI models by modality, with the counts it returns. Do not invent a model count or an API count.
2. Call `search_apis` with the user's task, or with one filter that search returned. Read the summaries. A result with `kind` = `model` is a model; `kind` = `api` is an API. Do not invent an API name or a model id.
3. Call `get_api` with the `api` value from that search. Read `input_schema`, `api_version`, and the public price. For a model, send chat completions input and use only the price fields `get_api` returned.
4. Tell the user the price `get_api` returned and wait for approval.
5. Call `run_api` only after that approval. Pass the same `api`, the `api_version` from `get_api`, and an `input` object that matches `input_schema`.

`run_api` can charge the user's OpenAny balance and can have side effects. Do not invent a price, a model count, or an API count. This skill does not publish a fixed price list.

If a call's execution or charging state is unknown, do not retry it. Report the result that came back, including gateway errors. HTTP success is not business success and is not proof of the charge.
