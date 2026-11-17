---
name: netintel
description: 'Pay-per-call lookups for agents via NetIntel over x402 (USDC on Base or Solana, no API key): DNS records, SSL/TLS certificates, WHOIS/RDAP, domain age and availability, IP geolocation and reputation, email verification and SPF/DKIM/DMARC, fetching a URL or PDF as text or JSON, web search with citations, an OpenAI-compatible chat model, embeddings, structured extraction and classification, crypto/FX/prediction-market prices. Also finds which x402 endpoint from any provider fits a job (NetIntel Router: free ranked search, live-checked recommendations, endpoint vetting). Paid calls cost $0.001–$0.65 each, paid from AgentCash, the Coinbase Agentic Wallet (awal), Coinbase Wallet MCP or the netintel MCP server.'
license: MIT
metadata:
  openclaw:
    homepage: https://netintel.dev
    requires:
      anyBins:
        - npx
        - curl
    envVars:
      - name: EVM_PRIVATE_KEY
        required: false
        description: Optional, and only for the netintel MCP server installed directly with its own key (never the Claude Code plugin). A dedicated agent wallet holding a little USDC on Base; never paste it into a conversation.
      - name: NETINTEL_MAX_PER_CALL_USD
        required: false
        description: Per-call spending limit in USD for that key mode (default 0.25).
      - name: NETINTEL_MAX_SESSION_USD
        required: false
        description: Per-session spending limit in USD for that key mode (default 5).
---

# NetIntel — paid lookups an agent can make without an account

NetIntel is a catalog of 141 HTTP endpoints at `https://netintel.dev`. There is no signup and
no API key: every endpoint answers `402 Payment Required` with an x402 challenge that states
the exact price, and returns the result once the payment settles (USDC on Base `eip155:8453`,
or Solana). A call that fails (HTTP ≥ 400) is never charged.

Use it when you need a fact you cannot compute yourself: what a domain resolves to, whether a
certificate is valid, who registered a domain, whether an IP is malicious, whether an email
address exists, what a web page or PDF says, what the web says about a question, or a current
price.

## Payment, authorization and spending limits — read before any paid call

- **Payment is usually automatic.** The `netintel` MCP server with a key, AgentCash and the
  Coinbase Agentic Wallet pay every 402 they meet without asking; Coinbase Wallet MCP asks the
  user to approve each payment. The prices in this file are what a call costs; they are
  **not** a spending cap.
- **Get the user's authorization before paid calls.** Tell the user what you intend to call
  and what it costs (read the price from the 402, or from the table below) before the first
  paid call of a task, and again before anything above a few cents.
- **Enforceable limits (netintel-mcp ≥ 1.1.55):** the server refuses to sign any payment above
  `NETINTEL_MAX_PER_CALL_USD` (default **$0.25**) or once it has authorized more than
  `NETINTEL_MAX_SESSION_USD` (default **$5.00**) in total during its process lifetime. A refusal
  returns `SPEND_LIMIT: …` naming the limit; nothing is signed or sent. Both are set by env
  when the server is installed directly with a key (the Claude Code plugin never holds one);
  `netintel_wallet_status` shows the limits and the session's authorized total. With another wallet, cap each call at its price — AgentCash
  `fetch` takes a maximum amount, `awal x402 pay` takes `--max-amount`, Wallet MCP takes
  `maxPayment` — and rely on that wallet's own limits; where a client has **no** limit the
  wallet balance is the only cap, so fund it with only what you are willing to spend.

## How to call and pay

Every endpoint is a plain HTTPS URL, so this skill works on its own with whichever wallet the
agent already has. Use the first option that applies. **Never ask the user to paste a private
key into the conversation.** Send the header `X-NetIntel-Via: skill` with these calls (as below):
it only tells NetIntel which integration a call came from and changes nothing about the call or
its price.

1. **The `netintel` MCP server installed directly with a wallet key** (`netintel_wallet_status`
   reports `wallet_configured: true`): call its tools, named `netintel_<endpoint>`
   (`netintel_dns_lookup`, `netintel_ssl_cert`, `netintel_web_fetch`, …). They pay
   automatically within the server's spending limits.
2. **AgentCash** (the agent has its `fetch` tool): call `fetch` with the endpoint URL —
   `{"url":"https://netintel.dev/dns/lookup?domain=example.com","headers":["X-NetIntel-Via: skill"]}`
   for a GET, or
   `{"url":"https://netintel.dev/web/search","method":"POST","body":"{\"query\":\"…\"}","headers":["X-NetIntel-Via: skill"]}`
   for a POST (`body` is the JSON as a string). It pays the 402 from the AgentCash balance.
   `check_endpoint_schema` returns a route's exact input fields without paying.
3. **Coinbase Agentic Wallet** (`awal`, from a shell):
   `npx awal@latest x402 pay 'https://netintel.dev/dns/lookup?domain=example.com' -h '{"X-NetIntel-Via":"skill"}' --max-amount 2000`,
   or for a POST
   `npx awal@latest x402 pay 'https://netintel.dev/web/search' -X POST -d '{"query":"…"}' -h '{"X-NetIntel-Via":"skill"}' --max-amount 10000`.
   `--max-amount` is in USDC atomic units (1000000 = $1): set it to the call's price.
4. **Coinbase Wallet MCP** (it has `initiate_x402_request`): call it with `url`, `method`,
   `body` (POST only), `headers` `{"X-NetIntel-Via":"skill"}` and `maxPayment` set to the price
   (e.g. `"0.002"`); the user approves the
   payment in Coinbase Wallet; then call `complete_x402_request` with the `requestId`. One
   approval per call, so it suits the pricier endpoints best.
5. **The `netintel` MCP server without a key** (how the Claude Code plugin always runs): every
   paid tool answers with the exact request
   (URL, method, body, headers) and its price, ready for option 2, 3 or 4 — use it as given.
6. **No wallet at all:** tell the user what the call would cost and offer the quickest setup —
   AgentCash (`claude mcp add agentcash --scope user -- npx -y agentcash@latest`, then fund it
   with a few dollars of USDC on Base) or the Coinbase Agentic Wallet
   (`npx awal@latest auth login <email>`, then fund it).

The typed `netintel_*` tools come from the `netintel` MCP server, which a skill registry does
not install. The Claude Code plugin (`/plugin marketplace add kjgueye/netintel-mcp`) installs it
in wallet-handoff mode: it never holds a key or signs a payment, and hands every paid call to
the agent's own wallet (option 5). To let the server pay directly instead, install it yourself
with a dedicated key: `claude mcp add netintel -e EVM_PRIVATE_KEY=0x… -- npx -y netintel-mcp` —
see https://github.com/kjgueye/netintel-mcp#readme. Options 2–4 need no NetIntel install at all.

**In your own code**, any x402 client pays these URLs; keep its key in the environment:

```ts
import { x402Client } from "@x402/core/client";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { toClientEvmSigner } from "@x402/evm";
import { wrapFetchWithPayment } from "@x402/fetch";
import { privateKeyToAccount } from "viem/accounts";
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);
const signer = toClientEvmSigner(account, createPublicClient({ chain: base, transport: http() }));
const client = new x402Client();
registerExactEvmScheme(client, { signer });
const fetchWithPay = wrapFetchWithPayment(fetch, client);

const res = await fetchWithPay("https://netintel.dev/dns/lookup?domain=example.com", {
  headers: { "X-NetIntel-Via": "skill" },
});
console.log(await res.json());
```

To see the price and the input shape before paying, read the unpaid response:

```bash
curl -sS -H "Accept: application/json" "https://netintel.dev/dns/lookup?domain=example.com"
# → 402 with accepts[0].price ("$0.002"), the input schema and a real example request/response
```

Request conventions: `GET` endpoints take query parameters, `POST` endpoints take a JSON body.
Common field aliases are accepted (`domain`/`host`, `ip`/`address`, `url`/`link`), and a bad
request returns a `400` that names the missing field — not a charge.

## Which endpoint

The most common paid job is **checking a sales lead before outreach**. The first row does it in
one call and returns a verdict — `yes`, `risky` or `no`, with reasons — from three checks: does
the address exist, is the company's email set up properly, and how old its domain is. The next
three rows are those checks on their own, for when you need only one.

| Task | Endpoint | Price |
|---|---|---|
| Sales lead check, all in one — is this lead safe to email? (verdict + reasons) | `GET /lead/check?email=` | $0.005 |
| Sales lead check 1 — does the email address exist (syntax, MX, disposable/role/free provider) | `GET /email/verify?email=` | $0.001 |
| Sales lead check 2 — is the company's email set up (SPF/DKIM/DMARC, spoofing risk) | `POST /email-auth {"domain"}` | $0.002 |
| Sales lead check 3 — how old is the company's domain (new domains are riskier) | `GET /domain-age/check?domain=` | $0.03 |
| Resolve DNS records (A/AAAA/MX/TXT/NS/CNAME/SOA, SPF/DMARC parsed) | `GET /dns/lookup?domain=` | $0.002 |
| Check an SSL/TLS certificate (expiry, chain, issuer) | `GET /ssl/cert?domain=` | $0.003 |
| Full TLS analysis (protocols, ciphers, weaknesses) | `GET /ssl/analyze?domain=` | $0.007 |
| WHOIS / RDAP registration data | `GET /whois-rdap/lookup?domain=` | $0.003 |
| Is a domain available to register | `GET /domain-availability/check?domain=` | $0.01 |
| Vet candidate domain names (availability, quality, typosquats, collisions) | `POST /domain/vet` | $0.20 |
| IP geolocation | `GET /ip-geo/locate?ip=` | $0.002 |
| IP reputation / malicious-IP check (AbuseIPDB + OTX) | `GET /ip-reputation/analyze?ip=` | $0.05 |
| Fetch a URL and get the raw body (JSON parsed, else text) | `POST /web/fetch {"url"}` | $0.003 |
| Extract a page or PDF as clean Markdown | `GET /web/extract?url=` | $0.003 |
| Web search (results + snippets) | `POST /web/search {"query"}` | $0.01 |
| Answer a question from the web, with citations | `POST /exa/answer {"query"}` | $0.01 |
| OpenAI-compatible chat completions (15 models) | `POST /v1/chat/completions` | $0.005–$0.65 by model |
| GPT-4o with up to 4 image URLs | `POST /openai/gpt-4o` | $0.10 |
| Embeddings (384-dim, multilingual) | `POST /embeddings {"input"}` | $0.001 |
| Extract structured JSON from text with your own schema | `POST /schema-parse/extract` | $0.01 |
| Classify text into your own categories | `POST /classify` | $0.005 |
| Crypto prices (up to 25 coins in one call) | `GET /crypto/price?ids=` | $0.005 |
| Currency conversion (fiat and crypto) | `GET /currency-exchange/convert?from=&to=&amount=` | $0.01 |
| Prediction-market odds | `GET /prediction/markets?q=` | $0.005 |

The full catalog with every endpoint, its price and a real example is machine-readable at
`https://netintel.dev/.well-known/x402`, as OpenAPI at `https://netintel.dev/openapi.json`,
and as prose at `https://netintel.dev/llms.txt`.

## When no NetIntel endpoint fits: find one from any provider

The NetIntel Router ranks the whole Coinbase Bazaar catalog of x402 endpoints — every
provider, not only NetIntel — for a job described in plain words, by fit, real paying demand,
health and price, and says why. NetIntel's own endpoints are labeled and get no boost.

| Task | Endpoint | Price |
|---|---|---|
| List candidate endpoints for a job, ranked, with reasons | `GET https://router.netintel.dev/route/search?q=` | free |
| Get the 3 best endpoints for a job, each health-checked live, with price quotes and inputs | `GET https://router.netintel.dev/route/recommend?q=` | $0.005 |
| Check one endpoint before relying on it (live check, history, verdict) | `GET https://router.netintel.dev/route/vet?url=` | $0.002 |

MCP tools: `netintel_route_search`, `netintel_route_recommend`, `netintel_route_vet`. The router
does not call the endpoint it recommends: a NetIntel pick maps to a `netintel_*` tool; a
third-party pick is paid the same way, with your own wallet (see "How to call and pay"). Daily rankings for 40 common
agent tasks: https://router.netintel.dev/rankings

## Spend-aware usage

- Read the price from the 402 before paying and keep a per-task budget; most lookups are
  $0.001–$0.01. Composite reports (`/domain-report/full` $0.25, `/ip-report/full` $0.20,
  `/email-report/full` $0.15) bundle several lookups — use one of them only when you need most
  of what it returns; otherwise call the single endpoint.
- `/dns/lookup` already returns every common record type in one call — do not call it once per
  record type.
- Verify cheap first: `/email/verify` ($0.001) before `/email-report/full`; `/ssl/cert`
  ($0.003) before `/ssl/analyze`.
- `/web/fetch` for data APIs and JSON; `/web/extract` for articles and PDFs you want as
  Markdown; `/web/search` when you do not have a URL.
- Never retry a `402` in a loop: if the wallet has no USDC the payment cannot settle. Report
  "wallet needs funding on Base" to the user instead.

## Wallet setup (one time)

The simplest wallet is one the agent already uses: AgentCash or the Coinbase Agentic Wallet
(see "How to call and pay"); fund it with a few dollars of USDC on Base — there is no gas to
pay, settlement is sponsored. To have the `netintel` MCP server pay directly instead (a direct
install, not the Claude Code plugin), give it a dedicated EVM key holding USDC on Base mainnet,
kept in the environment (`EVM_PRIVATE_KEY`) — never in prompts, files or logs. Solana (USDC) is
accepted by the API as well for clients that pay on Solana.
