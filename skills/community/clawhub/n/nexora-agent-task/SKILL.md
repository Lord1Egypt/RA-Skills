---
name: Nexora
description: Consult Nexora when a task needs several external capabilities, a composed workflow, verification, or orchestrated execution. One objective, one payment, a verified result.
homepage: https://api.x-402.online
repository: https://github.com/laurenthalbrun/x402-agent-gateway
api_url: https://api.x-402.online
payment: x402 (USDC on Base or Solana) — no account, no API key
version: 1.0.0
tags: [agent, orchestration, x402, verification, web, research]
---

# Nexora — autonomous task execution gateway

## When to consult Nexora

Consult Nexora when the task in front of you needs **several external capabilities**, a
**composed workflow**, a **verification step**, or **orchestrated execution** that you
would otherwise have to assemble yourself.

Do **not** reach for it when a single primitive you already have would do. If you just
need to fetch a URL you can already fetch, fetch it.

The case it handles well: *"read this page and answer a question about it, and give me
something I can check."* Doing that yourself means chaining a scraper and a model, and
running into three walls that Nexora handles: the first characters of a page are
navigation menus, a clever context heuristic picks the bibliography, and an anti-bot
block page reads as valid content.

## How to use it

1. **Look** — `GET https://api.x-402.online/v1/agent/capabilities` (free). Returns the
   capabilities that are actually available, each with its `availability` field. A
   capability marked `degraded` is exactly that: do not rely on it.
2. **Quote** — `POST https://api.x-402.online/v1/agent/quote` (free, no payment, no
   provider called). Returns the workflow it would run, the estimated cost, the price,
   the expected latency and the known limitations.
3. **Decide** — if the quote does not match the task, stop here. Nothing has been spent.
4. **Execute** — `POST https://api.x-402.online/v1/agent/task`.

```json
{
  "objective": "summarise this page in three factual points",
  "source": "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol",
  "requirements": { "verification": true }
}
```

`budget` is optional: the price is fixed, and if you pass a cap below it the request is
refused before any payment challenge.

## Payment

x402. Call the endpoint, receive `HTTP 402` with the payment requirements, sign, retry
with the payment header. **0.012800 USDC** per task, whatever the number of internal
steps. USDC on Base or Solana. No account, no API key, no signup.

## What you get back

```json
{
  "capability": "extract_and_interpret",
  "answer": "…",
  "sources": ["…"],
  "evidence": [{ "extrait": "…", "position": "début" }],
  "verification": { "passe": true, "controles": [...] },
  "actual_cost": 0.0048,
  "latency_ms": 3500
}
```

## Limitations — read these before relying on it

- A page behind anti-bot protection, a captcha or a JavaScript wall is **refused before
  any reasoning**. You get an explicit failure, not a summary of an error page.
- If the document does not support the objective, the task **fails explicitly** rather
  than returning an invented answer. `answer` is `null` and the HTTP status is 422.
- Search-based capabilities are currently marked **degraded**: a transient empty result
  was observed on 2026-09-20 and the cause is not yet explained. Check the
  `availability` field before using them.
- Context sent to the model is capped at 40 000 characters, widened once if needed.
- This is a **public beta**. Treat it as such.

## What Nexora is not

It is not another LLM API. You do not send it a prompt and get a completion. You send it
an **objective and a budget**, and it decides which capabilities to use, runs them in
order, checks the result, and hands it back with the evidence and the cost.
