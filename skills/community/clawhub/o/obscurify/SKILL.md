---
name: obscurify
description: Use Obscurify.ai as a model provider through its OpenAI-compatible API (200+ models, an account code instead of email). Use when asked to add, configure or troubleshoot Obscurify.ai in an agent or tool.
version: 1.1.0
openapi_version: 1.0.0
openapi_sha256: df50dde0f512bfd24f6a8b91c736912392f1cec1b6266be2a234177e8a1d2afa
openapi_url: https://obscurify.ai/api-docs/openapi.json
homepage: https://obscurify.ai/agents
---

# Obscurify.ai

Obscurify.ai is an OpenAI-compatible API to 200+ models. An account is a random 20-character account code (four groups of five letters and digits), with no email, username or password. Older accounts have a 16-digit account number instead, which still works.

- Base URL: `https://obscurify.ai/v1`
- Auth: `Authorization: Bearer sk-obs1_...`
- Key variable: `OBSCURIFY_API_KEY`
- Full API: https://obscurify.ai/api-docs/openapi.json

This file is versioned against that spec. `openapi_sha256` above is the SHA-256 of the spec's bytes when this file was served. If a saved copy's value no longer matches the live spec, fetch https://obscurify.ai/skill.md again.

## Set it up

1. **Get a key from your user.** Ask them to paste it somewhere safe, such as an environment variable or the tool's secret store. If they have one, skip to step 4.
2. **If they have no account, ask first.** Creating one means accepting https://obscurify.ai/terms, and that's their decision. They can sign up at https://obscurify.ai/signup. If they tell you to do it for them, run `npx -y @obscurify/cli signup --accept-terms --json` on this machine: it makes the account code here (never on our side), creates the account and prints `account_code` and `api_key`. Give the user the code (four groups of five characters) straight away: it is the only way into the account and can't be recovered. Make one account, not several: each network address can create only a few per hour and per day, and accounts that are never funded or used are deleted after 30 days.
3. **Get the key.** The simplest: the user clicks **Show API Key** at https://obscurify.ai/account and pastes it. Otherwise, with the user's account code on this machine: `echo 'CODE' | npx -y @obscurify/cli api-key` prints it. (The raw calls are in https://obscurify.ai/tutorials/account_keys.) Never send the account code itself: it's refused, and it must stay on the user's devices. An older account's 16-digit number can be sent as `{"account_number": "..."}`.
4. **Check for a balance.** `GET /get_user_balance`. Calls need a positive balance or a paid plan. Funding is the user's job: they add credit at https://obscurify.ai/account with crypto or a card. New accounts may get $1 of starter credit while this month's promo budget lasts. Payments aren't refundable, so don't buy anything without asking.
5. **Configure the tool**, using the section below.
6. **Test it** with one cheap call, then tell the user what you set and which model is the default.

```bash
curl -s https://obscurify.ai/v1/chat/completions \
  -H "Authorization: Bearer $OBSCURIFY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model": "deepseek/deepseek-v4-flash", "messages": [{"role": "user", "content": "Reply with exactly: ok"}]}'
```

Never print, log or commit the key or the account code, and never put either in a file that's shared or tracked by git.

## Configure the tool

Exact steps for each tool, all at https://obscurify.ai/agents:

- **OpenClaw:** https://obscurify.ai/tutorials/openclaw
- **Hermes Agent:** https://obscurify.ai/tutorials/hermes_agent
- **Agent Zero:** in the model preset, set the Main and Utility models to provider "Other OpenAI compatible" and API base URL `https://obscurify.ai/v1`. The key goes in `OTHER_API_KEY`.
- **Claude Code:** set `ANTHROPIC_BASE_URL=https://obscurify.ai`, `ANTHROPIC_AUTH_TOKEN` to the key and `ANTHROPIC_MODEL` (and `ANTHROPIC_DEFAULT_HAIKU_MODEL`) to a model id with tools; Obscurify.ai serves the Anthropic Messages API at `/v1/messages`. Or add the MCP server `@obscurify/mcp` to keep Claude Code's own model and call Obscurify models as tools.
- **Cursor:** add the MCP server `@obscurify/mcp`, which gives it Obscurify models as tools. It doesn't replace its main model.
- **Anything else OpenAI-compatible:** set the base URL to `https://obscurify.ai/v1`, use the key above, and choose a model ID from `GET /v1/models`.

Keep the provider prefix in model IDs. It's part of the ID: `deepseek/deepseek-v4-flash`.

## Choose a model

`GET /v1/models` needs no key and lists every model with its price and context length. Prices per model are also at https://obscurify.ai/models. Cached input is billed at a lower rate on models that support it: `pricing.input_cache_read` is that price, `usage.prompt_tokens_details.cached_tokens` says how much of a request was cached, and `usage.cost` is what it was charged.

Good starting points with tool calling, on any plan:

| Model ID | Context |
|---|---|
| `deepseek/deepseek-v4-flash` | 1M, default |
| `z-ai/glm-5.3` | 1M |
| `moonshotai/kimi-k2-0905` | 262K |
| `qwen/qwen3-coder` | 262K |

Plans decide what's available. Check with `GET /account_tier`:

- **Pay As You Go:** $0 a month, per-use prices, no token limit on paid models, free models up to 1M tokens a month, no frontier or uncensored models.
- **Casual:** $20 a month with $15 of usage included, adds frontier models (`GET /frontier_models`), no token limit on paid models, free models up to 10M tokens a month.
- **Pro:** $45 a month with $35 of usage included, adds uncensored models (`GET /uncensored_models`), no monthly token limit.

Agents use far more tokens than chat, because each step resends the system prompt, tools and history. Small tasks in our tests averaged about 20,000 tokens, so tell the user that the 1M free-model tokens a month on Pay As You Go can run out quickly. `deepseek/deepseek-v4-flash` is currently free up to that limit, then charged at its listed price.

## When a call fails

Errors on `/v1/*` are OpenAI error objects: `{"error": {"message", "type", "param", "code"}}`.

| Status | Meaning | What to do |
|---|---|---|
| 401 | Key is missing or wrong | Ask the user to check the key |
| 402 | No balance and no plan | The user adds credit at https://obscurify.ai/account |
| 403 | The plan doesn't include this model | Choose another model, or the user upgrades |
| 404 `model_not_found` | Unknown model ID | Check `GET /v1/models`, and keep the prefix |
| 429 | Too many requests, or the monthly token limit on free models | Back off. If `code` is `monthly_plan_token_limit_reached`, switch to a paid model, upgrade, or wait for the next month |

Other checks: `GET /get_user_balance` for the balance, and `GET /account_tier` for the plan and tokens used.

## What to tell the user about privacy

Say only this, because it's what Obscurify.ai publishes:

- Prompts and responses aren't stored on its servers.
- Models with the ZDR tag (category "Zero retention" in `/v1/models`) run only on zero-data-retention routes: their providers commit in published policies not to train on or retain data. There are no signed agreements. Other models follow their provider's own policy.
- Identities are scrambled before requests reach providers. Providers don't see who sent a prompt, but they do see the prompt text. Whatever an agent reads and sends, such as files, becomes prompt text.
- Optional secret scrubbing: with the header `X-Obscurify-Scrub-Secrets: 1` (or the setting on the API key), API keys, tokens, private keys and passwords in well-known formats are replaced with placeholders before the prompt reaches the model. Off by default. https://obscurify.ai/tutorials/secret_scrubbing
- Obscurify.ai keeps billing records (user ID, model, token counts, cost, time), and keeps IP addresses and user agents for up to 30 days to prevent abuse.

Details: https://obscurify.ai/privacy

To keep conversations from being linked to the account or to each other, the user can turn on private sessions (unlinkable inference): run the open-source `unlinkable-inference` proxy and point the tool's base URL at it (`http://127.0.0.1:8899/v1`, or `http://127.0.0.1:8899` for Anthropic clients), same key. Setup for Claude Code, Codex, pi and MCP: https://obscurify.ai/tutorials/private_sessions
