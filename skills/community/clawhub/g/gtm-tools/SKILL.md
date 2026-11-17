---
name: gtm-tools
description: Set up and call the gtm-tools API from any agent — get an API key (including fully autonomous self-registration), connect the browser-session pool, then use all 63 LinkedIn, Reddit, email-finding, buying-signal, and geocoding tools over Bash + curl. Use this skill whenever the user wants to install / set up / connect / onboard gtm-tools, asks how to get a gtm-tools API key, hits a 401 / 402 / "Unauthorized" / "Insufficient tokens" from api.gtm-tools.sh, asks what tools or what token costs are available, asks to check their token balance or top up, asks which LinkedIn or Reddit accounts are connected, asks to install the browser extension, or names any gtm-tools tool (get_linkedin_company_url, get_email, detect_signal, list_linkedin_company_employees, get_reddit_post, …) without a workflow skill already loaded. This is the base capability skill — for full drafting workflows use outbound-sales, linkedin-copywriter, or reddit-community-manager instead.
---

# GTM Tools

Give the agent the whole GTM data surface — LinkedIn, Reddit, verified emails, buying signals, geocoding — behind one bearer token. This skill covers setup and the call contract. The three workflow skills in the same bundle (`outbound-sales`, `linkedin-copywriter`, `reddit-community-manager`) build on top of it.

## The one thing that trips everyone up

Two hosts, and they are not interchangeable:

| Host | What it is |
|---|---|
| `api.gtm-tools.sh` | The API. MCP, REST, OAuth, everything you call. |
| `gtm-tools.sh` | The docs site. **POSTing here returns 405.** |

If a call returns `405`, fix the host before debugging anything else.

## Setup

### 1. Get an API key

Three paths, pick by context.

**A human is present** — send a verification code, then redeem it:

```bash
curl -s -X POST "https://api.gtm-tools.sh/api/v0/get_api_key" \
  -H "Content-Type: application/json" \
  -d '{"email":"you@yourcompany.com"}'

curl -s -X POST "https://api.gtm-tools.sh/api/v0/get_api_key" \
  -H "Content-Type: application/json" \
  -d '{"email":"you@yourcompany.com","code":"123456"}'
# → { "api_key": "sk_..." }
```

**No human is present** — register autonomously via the [auth.md](https://api.gtm-tools.sh/auth.md) protocol. One call, no signup form, own isolated workspace, 100 free tokens:

```bash
curl -s -X POST "https://api.gtm-tools.sh/agent/identity" \
  -H "Content-Type: application/json" \
  -d '{"type":"anonymous"}'
# → { "access_token":"sk_...", "token_type":"bearer", "expires_in":31536000, ... }
```

To bind the key to a known user's workspace instead, send `{"type":"identity_assertion","assertion_type":"verified_email","assertion":"user@example.com"}`, then submit the emailed code to `/agent/identity/claim` and poll `/oauth/token` with `grant_type=urn:workos:agent-auth:grant-type:claim`.

**The CLI is installed** — browser sign-in, key stored in `~/.gtm-tools/config.json`:

```bash
gtm-tools admin login
```

Revoke any key with `curl -X POST https://api.gtm-tools.sh/oauth/revoke -d 'token=sk_...'`, or `revoke_api_key` / `gtm-tools admin keys revoke <id>`. Note that `admin login` revokes the workspace's previous `CLI (…)`-named keys, so don't hard-code one into CI.

### 2. Export it

```bash
export GTM_TOOLS_API_KEY="sk_..."
```

### 3. Connect sessions (only for session-backed tools)

LinkedIn and Reddit writes, plus a few reads, run through a real logged-in browser session pooled by the extension. Check before assuming:

```bash
curl -s -X POST "https://api.gtm-tools.sh/api/v0/list_connected_linkedin_accounts" \
  -H "Authorization: Bearer $GTM_TOOLS_API_KEY" -H "Content-Type: application/json" -d '{}' | jq .
```

Empty list means the user must install the extension and press Connect:

```bash
curl -fsSL https://api.gtm-tools.sh/extension/install.sh | bash
```

Each `ready` row carries a `linkedin_username` / `reddit_username` — pass it as `senderUsername` to write tools. Both tools cost 0, so checking is always free.

## How to call any tool

Every tool is the same shape. Tool name in the path, JSON body, bearer header:

```bash
curl -s -X POST "https://api.gtm-tools.sh/api/v0/TOOL_NAME" \
  -H "Authorization: Bearer $GTM_TOOLS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{...arguments...}' | jq .
```

The same tools are also exposed over MCP at `https://api.gtm-tools.sh/mcp` (Streamable HTTP) and through the `gtm-tools` CLI. Full catalog with token costs and arguments: [`references/tools.md`](./references/tools.md). Never hardcode costs — `get_token_balance` returns the live table.

## Metering: what actually costs tokens

$1 = 100 tokens. New workspaces start with 100 free. The cost is **debited before the tool runs**, and there is no automatic refund, which is the only rule you need to predict a bill:

| Outcome | Charged? |
|---|---|
| `400` bad arguments, `401` bad key, `404` unknown tool | No — rejected before metering |
| `402` insufficient tokens | No — that is the gate declining |
| Session-required error (no pooled session) | No — gated ahead of metering |
| `200` with `status: "not_found"` | Yes — the tool ran, there was nothing to find |
| `429` with `status: "try_again_later"` | Yes — and every retry charges again |
| `5xx` upstream failure | Yes |

So: check `list_connected_*_accounts` and `get_token_balance` (both free) before fanning out, filter cheaply before hydrating expensively, and honor `retry_after_seconds` instead of retrying tightly.

Top up with `buy_tokens` (`{"amount_usd":25}`) or enable `set_auto_reload` once and stop thinking about it.

## Error contract

Branch on the HTTP status, never on message text:

| Status | Meaning | Do this |
|---|---|---|
| `400` | Argument failed schema validation | Read the field list in the message, fix, retry |
| `401` | Missing / invalid / revoked key | Re-key. The response carries `WWW-Authenticate` with the discovery URL for self-registration |
| `402` | Insufficient tokens | `buy_tokens` or `set_auto_reload` |
| `404` | Unknown tool name | Check spelling against `references/tools.md` |
| `405` | You POSTed to `gtm-tools.sh` | Use `api.gtm-tools.sh` |
| `429` | Rate limit, or `status: "try_again_later"` | Sleep `retry_after_seconds`, then one retry |
| `5xx` | Upstream provider failed | Exponential backoff |

A `200` carrying `status: "not_found"` is a real answer: the tool did the work and there is nothing to return. Do not retry it.

## Cost-aware sequencing

The expensive tools are expensive for a reason (they fan out upstream). Order the work so they run on the smallest possible set:

- `detect_signal` (0 + 5 per firing detector) qualifies accounts before any LinkedIn spend.
- `get_linkedin_company_url` (2) then `list_linkedin_company_employees` (30) — always pass `title_filters`, since the cost is identical whether you return everyone or the four people you want.
- `search_linkedin_company_employees` (5) is the cheap SERP-only alternative when name + headline + URL is enough.
- `get_email` (5) runs per candidate, so filter the employee list first.
- `list_linkedin_company_employees_posts` (80) is the most expensive tool in the catalog. Use it deliberately.
- Cache what doesn't move: company IDs, profile URLs, and verified emails are stable for weeks.

## Related skills

Once setup works, hand the actual workflow to the specialist skill in this bundle:

| Skill | Use it for |
|---|---|
| `outbound-sales` | Signal → persona → verified email → cold email + LinkedIn DM drafts |
| `linkedin-copywriter` | Posts, comments, invitations, DMs in the user's voice, AI tells scrubbed |
| `reddit-community-manager` | Thread discovery, poster qualification, disclosed value-first replies |

Docs for agents: [`https://gtm-tools.sh/llms.txt`](https://gtm-tools.sh/llms.txt) is the page index, and appending `.md` to any docs URL returns clean markdown.
