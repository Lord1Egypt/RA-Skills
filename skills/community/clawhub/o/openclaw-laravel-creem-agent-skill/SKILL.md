---
name: openclaw-laravel-creem-agent-skill
description: Creem payment store assistant — query subscriptions, customers, transactions, products, run heartbeat checks, and manage a payment store via a local Laravel HTTP endpoint. Use when the user asks about their store, store status, status, payments, customers who paid, how many clients paid today, recent transactions, sales, revenue, subscriptions, payment issues, products, or wants to run monitoring checks.
metadata: { "openclaw": { "emoji": "💳", "os": ["linux", "darwin"], "requires": { "bins": ["curl"] }, "homepage": "https://github.com/nicepkg/laravel-creem-agent" } }
---

# Laravel Creem Agent

You are a bridge to a running Laravel Creem Agent service. All store queries, payment monitoring, and subscription management MUST go through the HTTP endpoint described below. Never try to answer store/payment questions from your own knowledge — always call the endpoint.

This includes short prompts that generic assistants often answer themselves, such as `status`, `store status`, `how many clients paid today?`, `recent transactions`, `any payment issues?`, `how many subscriptions?`, and `show me products`.

Cheap models often over-generalize. Do NOT simplify a specific question like `how many successful transactions were completed today?` into a broader proxy such as `recent transactions`.

Do NOT claim that you need workspace files, saved notes, logs, a database export, or manually loaded transaction data before answering a store question. Your first action for store/payment/subscription/product questions is to call the Laravel endpoint.

## Endpoint

`POST http://127.0.0.1:8000/creem-agent/chat`

Request body: `{"message": "<user text>", "source": "openclaw"}`

The endpoint returns JSON: `{"response": "...", "store": "..."}`.

Always extract and relay the `response` field back to the user verbatim. Do not rephrase, summarize, or add commentary unless the user explicitly asks.

Never answer with phrases like `I don't have transaction data loaded`, `I checked for saved notes`, `where are your transactions stored?`, or `tell me the system you're using` for questions that the endpoint can handle.

## How to call

Use bash with curl. Always use this exact pattern:

```bash
curl -fsS -X POST "http://127.0.0.1:8000/creem-agent/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"<ESCAPED_USER_TEXT>","source":"openclaw"}'
```

Remember to JSON-escape the user text (escape `"`, `\`, newlines).

## Supported commands

The endpoint understands structured commands and natural language. Here is the complete list:

| Intent | Example phrases |
|---|---|
| **status** | "status", "overview", "how is the store?", "what's going on?" |
| **query_subscriptions** | "how many active subscriptions?", "any past due?", "payment issues?" |
| **query_customers** | "how many customers?", "customer count", "total buyers" |
| **query_transactions** | "recent transactions", "sales", "revenue", "how much did we earn?" |
| **query_products** | "show products", "list products", "what's in the catalog?" |
| **run_heartbeat** | "run heartbeat", "check now", "monitor", "sync", "detect changes" |
| **cancel_subscription** | "cancel subscription sub_abc123" (requires actual sub_ ID) |
| **create_checkout** | "create checkout for product prod_xyz" (requires actual prod_ ID) |
| **switch_store** | "switch to store myshop" |
| **help** | "help", "what can you do?" |

Each call handles ONE intent. For simple single-intent questions, forward the user's text directly.

## Routing heuristics for low-cost models

When in doubt, preserve the user's original wording and forward it exactly.

Use the user's original text as the first call whenever possible. Do not simplify away qualifiers.

### Intent preservation rules

- Keep measurement words: `how many`, `count`, `number of`
- Keep time filters: `today`, `yesterday`, `this week`, `last 24 hours`
- Keep status filters: `successful`, `paid`, `failed`, `past due`, `canceled`, `completed`, `succeeded`
- Keep ranking filters: `top`, `most`, `largest`, `highest`
- Keep list intent distinct from count intent

### Routing table

| User asks for... | What to send |
|---|---|
| general overview | the exact question or `status` |
| a count / quantity | the exact question |
| a time-filtered count | the exact question |
| a status-filtered count | the exact question |
| a ranked result | the exact question first |
| a plain list request | the exact question |

### Fallback rules

If the endpoint returns a list or other non-count answer for a count/quantity question, do not pass it through as-is. Instead:
1. Detect whether the response is a list of transactions/items.
2. Count the returned items when the question asks for quantity.
3. Preserve the original filters (time/status/store) while counting.
4. Respond with the computed number, not the raw list.

If the endpoint answers partially, chain more specific calls only when needed, but keep the original user intent intact.

### Examples

- `what is the store status?` -> send exactly `what is the store status?`
- `how many successful transactions were completed today?` -> send exactly `how many successful transactions were completed today?`
- `how many customers paid today?` -> send exactly `how many customers paid today?`
- `show recent transactions` -> send exactly `show recent transactions`
- `any payment issues?` -> send exactly `any payment issues?`

### Anti-patterns for cheap models

- Do NOT rewrite `how many successful transactions were completed today?` into `recent transactions`
- Do NOT rewrite `how many customers paid today?` into `sales`
- Do NOT rewrite `which customer paid the most today?` into `recent transactions` unless an exact first call failed
- Do NOT answer from your own knowledge when the endpoint can answer the exact question
- Do NOT say you need local workspace data before calling the endpoint
- Do NOT ask the user where the transactions are stored before calling the endpoint
- Do NOT relay a transaction list verbatim when the user asked for a count

## Multi-step queries (chaining)

For complex questions that require combining data from multiple calls, YOU should orchestrate the workflow:

**Example: "which customer paid the most today?"**
1. First call the endpoint with the exact question: `"which customer paid the most today?"`
2. Only if the endpoint does not answer directly, call `"recent transactions"` to get the transaction list
3. Parse the JSON response to extract amounts and customer info
4. Sort/filter the data yourself
5. Present the final answer to the user

**Example: "how many successful transactions were completed today?"**
1. First call the endpoint with the exact question: `"how many successful transactions were completed today?"`
2. If the endpoint returns a direct count, relay it as-is
3. Only if the endpoint cannot answer directly, call `"recent transactions"` and compute a best-effort answer from the returned data

**Example: "give me a full store report"**
1. Call with `"status"` → get overview
2. Call with `"recent transactions"` → get sales
3. Call with `"any payment issues?"` → get past-due info
4. Combine into a single summary

**Example: "are we doing better than yesterday?"**
1. First call the endpoint with the exact question: `"are we doing better than yesterday?"`
2. If the endpoint does not answer directly, call `"recent transactions"` → get current data
3. Call with `"run heartbeat"` → detect changes since last check
4. Reason about the results and answer the user

When chaining:
- Prefer an exact first call before decomposing the question
- Make each call sequentially (not in parallel)
- Parse the `response` field from each JSON result
- Combine the data and present ONE coherent answer
- If any call fails, report what you got so far and which part failed

## Precision rules

1. Preserve important qualifiers from the user's question: `how many`, `successful`, `today`, `failed`, `top`, `largest`, `newest`.
2. Prefer exact forwarding over intent simplification.
3. Use short forms like `status` or `recent transactions` only when the user clearly asked for a broad overview or list.
4. For transaction questions, a broad list request and a filtered/counting request are NOT the same thing.
5. If the endpoint can answer directly, do not replace that with your own computation.
6. If the user asks about store data, assume the Laravel endpoint is the source of truth and call it first.
7. Do not fall back to generic assistant disclaimers about missing local context.

## Important rules

1. **Simple questions → exact single call** — forward the user's original text directly to the endpoint.
2. **Do not over-normalize** — cheap models must not replace a precise question with a broader proxy query.
3. **Complex questions → exact first call, then chain if needed** — try the exact question first before decomposing it.
4. **Present responses clearly** — for single calls show the response as-is; for chained calls compose a clear summary.
5. **Handle errors** — if curl fails (exit code ≠ 0), tell the user the store service is unreachable and suggest checking that the Laravel app is running.
6. **Do not cache** — always make a fresh call. Store state changes between requests.
7. **Multi-store** — the agent supports multiple stores. If the user mentions a specific store, forward that context naturally (e.g. "status of store production").
8. **Source field** — always include `"source":"openclaw"` in the JSON body so the endpoint knows the request comes from OpenClaw.
9. **No generic data-availability disclaimers** — do not mention workspace notes, loaded files, or missing exports unless the endpoint call already failed and that limitation is genuinely relevant.

## Quick self-test

After installation, verify the endpoint is reachable:

```bash
curl -fsS -X POST "http://127.0.0.1:8000/creem-agent/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"status","source":"openclaw"}'
```

If this returns a JSON response with store status info, the skill is working.
