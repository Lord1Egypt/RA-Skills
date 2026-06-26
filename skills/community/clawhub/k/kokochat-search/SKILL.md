---
name: kokochat-search
version: 0.2.0
description: "Web search via KokoChat's hosted Brave-backed search proxy. No API key required on the user's machine — credentials live on KokoChat's server (deeply.plus). Use this skill when you need quick web search results inside an OpenClaw agent without configuring Tavily / Serper / Brave keys locally."
author: komako-workshop
license: Apache-2.0
tags: [latest, search, web, web-search, kokochat, brave, no-key]
triggers:
  - search the web
  - 搜一下
  - 联网查
  - hosted search
  - kokochat search
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      capabilities:
        - network
      platforms:
        - linux
        - darwin
        - windows
---

# kokochat-search

`kokochat-search` is a thin local OpenClaw exec wrapper around KokoChat's
hosted search API. The user's OpenClaw does **not** store Brave (or any
other search) API credentials; it only runs `bin/search.mjs`, which POSTs
`{ query, count }` to the KokoChat search endpoint (default
`https://deeply.plus/deeply/search`, override via `KOKO_SEARCH_API_BASE`).

Originally written for KokoChat's Deeply mini-app, but the wrapper itself
is generic — any agent that just wants "give me web search with no
per-user key" can install and call it.

## Install

```bash
openclaw skills install kokochat-search --agent <your-agent>
```

After install, add it to the agent's exec allowlist so the agent is allowed
to invoke `bin/search.mjs`. KokoChat's own installer does this
automatically; standalone users can do it via
`openclaw approvals` (see OpenClaw docs).

## Tool command

```bash
~/.openclaw/agents/<your-agent>/workspace/skills/kokochat-search/bin/search.mjs '{"query":"EN keywords","count":5}'
```

(Inside KokoChat's `deeply` agent, the host prompt rewrites this to the
real absolute path automatically.)

Input:

- `query` (string, required): concise English keywords.
- `count` (number, optional): 1-10, default 5.

Output:

```json
{
  "ok": true,
  "provider": "brave",
  "query": "...",
  "requestedCount": 5,
  "count": 5,
  "results": [
    { "title": "...", "url": "https://...", "snippet": "..." }
  ]
}
```

If `ok` is false, be honest in the visible narration and do not invent
URLs. Common failure modes: `search_not_configured` (server has no Brave
key configured), `rate_limited` (hosted endpoint is throttling).

## Optional env

- `KOKO_SEARCH_API_BASE` — override search endpoint, e.g.
  `http://127.0.0.1:8788` when running a local KokoChat Deeply server.
- `KOKO_SEARCH_TOKEN` — bearer token if the hosted endpoint requires one
  (default deployment is unauthenticated with per-IP rate limit).
- Legacy aliases `KOKO_DEEPLY_SEARCH_BASE` / `KOKO_DEEPLY_SEARCH_TOKEN`
  are still honoured.

## Source

<https://github.com/komako-workshop/koko-chat/tree/main/openclaw/skills/kokochat-search>
