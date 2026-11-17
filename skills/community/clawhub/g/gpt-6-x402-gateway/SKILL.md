# GPT-6 x402 Gateway

> Cheapest GPT-6 calls on x402. No API key, no account — pay per call in USDC on Base.

## When to use this

- An agent needs **GPT-6 chat completions** but has no provider key, or wants to pay as it goes.
- An agent needs a **specialized GPT-6 task endpoint** (code audit, deep research, translation, prompt-injection firewall) without building prompts from scratch.
- Any agent with an x402-compatible wallet (OpenClaw, `@x402/fetch`, Coinbase `awal`) can pay inline.

## How it's paid (x402 v2 — no key, no signup)

`POST` to an endpoint. First call returns **HTTP 402** with payment requirements (USDC on Base, `eip155:8453`); your wallet pays and retries automatically, returning the result.

```bash
# Without payment: expect 402
curl -X POST https://gpt.558686.xyz/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-6","messages":[{"role":"user","content":"hello"}]}'
# → 402 Payment Required

# With payment (any x402 v2 client handles this automatically)
# npx awal x402 pay https://gpt.558686.xyz/v1/chat/completions -X POST -d '{...}'
```

OpenAI-compatible: point any OpenAI SDK at `https://gpt.558686.xyz/v1` and wrap fetch with `@x402/fetch` (`wrapFetchWithPayment`). Auth is via x402 payment, not an API key.

## Endpoints & live prices (probed 2026-10-10, USDC on Base)

| Endpoint | What it does | Price/call |
|---|---|---|
| `POST /v1/chat/completions` | OpenAI-standard chat completions (GPT-6) | $0.05 |
| `POST /v1/chat` | Chat Pro (GPT-6) | $0.05 |
| `POST /v1/trial` | Low-cost trial calls (GPT-6) | $0.01 |
| `POST /v1/translate/pro` | Translation Pro | $0.30 |
| `POST /v1/doc/summary` | Document Summary Pro | — see 402 |
| `POST /v1/extract/schema` | Structured Schema Extractor | — see 402 |
| `POST /v1/data/insights` | Data Insights Analyst | — see 402 |
| `POST /v1/content/seo` | SEO Content Writer | — see 402 |
| `POST /v1/audit/code` | Code Security & Quality Audit | $1.50 |
| `POST /v1/audit/contract` | Smart Contract & Web3 Security Auditor | — see 402 |
| `POST /v1/research` | Deep Research Report (GPT-6) | $2.00 |
| `POST /v1/guard/prompt` | Agent Prompt Injection Firewall | — see 402 |
| `POST /v1/guard/tx` | Agent Transaction Guard & Calldata Decoder | — see 402 |
| `GET /v1/x402-ping` | Health/canary probe (returns status, model list, MCP address) | $0.002 |

Prices are per call, fixed, no subscription. The 402 response is the source of truth — always read `accepts[0].amount` (6-decimal USDC).

## Why this gateway

- **GPT-6 only, single-model focus** — one model done cheap, not a thin multi-model wrapper.
- **Task endpoints, not just raw chat** — audit, research, guard and extract endpoints encode the prompting work so the calling agent doesn't have to.
- **Machine-discoverable** — `/llms.txt` and `/openapi.json` are public; `/.well-known/x402` manifest exposed; Bazaar discovery extension declared.

## Links

- Service: https://gpt.558686.xyz
- Docs for agents: https://gpt.558686.xyz/llms.txt
- OpenAPI: https://gpt.558686.xyz/openapi.json
- Source/issues: https://github.com/wangletiand/gpt-x402-gateway
