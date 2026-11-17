---
name: obscurify
description: Use Obscurify.ai as a model provider through its OpenAI-compatible API (200+ models, account number instead of email). Use when asked to add, configure or troubleshoot Obscurify.ai in an agent or tool.
version: 1.0.0
openapi_version: 1.0.0
openapi_sha256: 8a8510783eed58e2a06193a43542bd6af2953a66961615e23a2ae1da95967f8b
openapi_url: https://obscurify.ai/api-docs/openapi.json
homepage: https://obscurify.ai/agents
---

# Obscurify.ai

Obscurify.ai is an OpenAI-compatible API to 200+ models. Accounts are a random 16-digit account number, with no email, username or password.

- Base URL: `https://obscurify.ai/v1`
- Auth: `Authorization: Bearer sk-obs1_...`
- Key variable: `OBSCURIFY_API_KEY`
- Full API: https://obscurify.ai/api-docs/openapi.json

This file is versioned against that spec. `openapi_sha256` above is the SHA-256 of the spec's bytes when this file was served. If a saved copy's value no longer matches the live spec, fetch https://obscurify.ai/skill.md again.

## Set it up

1. **Get a key from your user.** Ask them to paste it somewhere safe, such as an environment variable or the tool's secret store. If they have one, skip to step 4.
2. **If they have no account, ask first.** Creating one means accepting https://obscurify.ai/terms, and that's their decision. They can sign up at https://obscurify.ai/signup. If they tell you to do it for them, call `POST /create_account` with `{"accept_tos": true}`, then give them the `account_number` straight away. It is the only way into the account and can't be recovered.
3. **Get the key from the number.** `POST /generate_token` with `{"account_number": "..."}` returns it as `token`. The user can also click **Show API Key** at https://obscurify.ai/account.
4. **Check for a balance.** `GET /get_user_balance`. Calls need a positive balance or a paid plan. Funding is the user's job: they buy a voucher at https://obscurify.ai/account with crypto or a card. New accounts may get $1 of starter credit while this month's promo budget lasts. Payments aren't refundable, so don't buy anything without asking.
5. **Configure the tool**, using the section below.
6. **Test it** with one cheap call, then tell the user what you set and which model is the default.

```bash
curl -s https://obscurify.ai/v1/chat/completions \
  -H "Authorization: Bearer $OBSCURIFY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model": "deepseek/deepseek-v4-flash", "messages": [{"role": "user", "content": "Reply with exactly: ok"}]}'
```

Never print, log or commit the key or the account number, and never put either in a file that's shared or tracked by git.

## Configure the tool

Exact steps for each tool, all at https://obscurify.ai/agents:

- **OpenClaw:** https://obscurify.ai/tutorials/openclaw
- **Hermes Agent:** https://obscurify.ai/tutorials/hermes_agent
- **Agent Zero:** in the model preset, set the Main and Utility models to provider "Other OpenAI compatible" and API base URL `https://obscurify.ai/v1`. The key goes in `OTHER_API_KEY`.
- **Cursor and Claude Code:** add the MCP server `@obscurify/mcp`, which gives them Obscurify models as tools. It doesn't replace their main model.
- **Anything else OpenAI-compatible:** set the base URL to `https://obscurify.ai/v1`, use the key above, and choose a model ID from `GET /v1/models`.

Keep the provider prefix in model IDs. It's part of the ID: `deepseek/deepseek-v4-flash`.

## Choose a model

`GET /v1/models` needs no key and lists every model with its price and context length. Prices per model are also at https://obscurify.ai/model_cards.

Good starting points with tool calling, on any plan:

| Model ID | Context |
|---|---|
| `deepseek/deepseek-v4-flash` | 1M, inexpensive default |
| `z-ai/glm-5.3` | 1M |
| `moonshotai/kimi-k2-0905` | 262K |
| `qwen/qwen3-coder` | 262K |

Plans decide what's available. Check with `GET /account_tier`:

- **Pay As You Go:** $0 a month, per-use prices, up to 1M tokens a month, no frontier or uncensored models.
- **Casual:** $20 a month with $15 of usage included, adds frontier models (`GET /frontier_models`), up to 10M tokens a month.
- **Pro:** $45 a month with $35 of usage included, adds uncensored models (`GET /uncensored_models`), no monthly token limit.

Agents use far more tokens than chat, because each step resends the system prompt, tools and history. Small tasks in our tests averaged about 20,000 tokens, so tell the user that Pay As You Go's 1M tokens can run out quickly.

## When a call fails

Errors on `/v1/*` are OpenAI error objects: `{"error": {"message", "type", "param", "code"}}`.

| Status | Meaning | What to do |
|---|---|---|
| 401 | Key is missing or wrong | Ask the user to check the key |
| 402 | No balance and no plan | The user adds credit at https://obscurify.ai/account |
| 403 | The plan doesn't include this model | Choose another model, or the user upgrades |
| 404 `model_not_found` | Unknown model ID | Check `GET /v1/models`, and keep the prefix |
| 429 | Too many requests, or the monthly token limit | Back off. If `code` is `monthly_plan_token_limit_reached`, the user upgrades or waits for the next month |

Other checks: `GET /get_user_balance` for the balance, and `GET /account_tier` for the plan and tokens used.

## What to tell the user about privacy

Say only this, because it's what Obscurify.ai publishes:

- Prompts and responses aren't stored on its servers.
- Text requests only use zero-data-retention routes: providers commit in their published policies not to train on or retain data. There are no signed agreements.
- Identities are scrambled before requests reach providers. Providers don't see who sent a prompt, but they do see the prompt text. Whatever an agent reads and sends, such as files, becomes prompt text.
- Obscurify.ai keeps billing records (user ID, model, token counts, cost, time), and keeps IP addresses and user agents for up to 30 days to prevent abuse.

Details: https://obscurify.ai/privacy
