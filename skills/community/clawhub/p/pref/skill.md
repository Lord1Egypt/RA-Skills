---
name: pref-mcp-onboarding
version: 1.0.0
homepage: https://pref.trade
description: "Quantitative research and data tools for AI agents — 670+ capabilities, 250 daily tool calls included, no credit card, no signup, no commitment. Self-register for a pref_agent API key at https://pref.trade/v1/agents/register"
metadata:
  mcp:
    endpoint: https://pref.trade/mcp
    auth: bearer
    key_format: pref_agent_*
    registration: https://pref.trade/v1/agents/register
    quota_tiers:
      anonymous: 100/day
      agent_key: 250/day
      account: 500/day
---

# PREF MCP Onboarding

Goal:

1. create or reuse an agent-owned `pref_agent_*` key
2. save it safely
3. install `https://pref.trade/mcp`
4. verify the MCP is using that key, not anonymous quota

Once installed, the MCP is self-documenting — call any tool to discover its schema. Start with `search_capabilities` to explore 670+ data sources, then use `browse_capabilities` to find what you need.

## Default Endpoint

```text
https://pref.trade/mcp
```

Do not use `/mcp-gateway` for normal client setup.

Do not open `https://pref.trade/sign-up` for agent onboarding. Browser sign-up
uses human verification and is only for humans. Agents should use
`POST https://pref.trade/v1/agents/register`.

## Fast Onboarding

### 1. Register if no key exists

```bash
curl -s -X POST "https://pref.trade/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Research Agent","description":"Agent using PREF MCP"}' | jq
```

The response includes:
- `api_key`: Your `pref_agent_*` key (shown once — save it now)
- `claim_url`: Share this with a human to link the agent to a Preference account and double the daily quota from 250 to 500 calls. Optional but recommended.

### Key Storage

⚠️ **Save the key to a file immediately — do not echo it into terminal history, logs, or prompts.**

```bash
mkdir -p ~/.config/preference
echo '{"api_key":"pref_agent_xxx"}' > ~/.config/preference/credentials.json
chmod 600 ~/.config/preference/credentials.json
```

Or use an environment variable:

```bash
export PREFERENCE_API_KEY='pref_agent_xxx'
```

Reference the key from your MCP client config (see below) — never inline the real key in YAML/JSON that gets shared.

### 2. Verify the key via MCP

**Important:** `/v1/auth/whoami` does **not** accept `pref_agent_*` keys.
Verify your key by calling `preference_account_status` inside MCP instead:

```bash
curl -s -X POST "https://pref.trade/mcp" \
  -H "Authorization: Bearer ${PREFERENCE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"preference_account_status","arguments":{}}}'
```

Do **not** proceed until this returns your agent identity (not `"anonymous"`).

### 3. Install the MCP

Use a remote HTTP / Streamable HTTP MCP server config equivalent to:

```yaml
mcp_servers:
  pref:
    url: "https://pref.trade/mcp"
    headers:
      Authorization: "Bearer ${PREFERENCE_API_KEY}"
```

For Claude Code:

```bash
claude mcp add --transport http pref \
  "https://pref.trade/mcp" \
  --header "Authorization: Bearer ${PREFERENCE_API_KEY}"

claude mcp list
```

For Codex:

```bash
export PREFERENCE_API_KEY='pref_agent_xxx'
codex mcp add pref --url https://pref.trade/mcp --bearer-token-env-var PREFERENCE_API_KEY
```

### 4. Verify inside MCP

Call `preference_account_status` first.

Expected result:

- identity is the registered agent, not anonymous
- quota tier reflects agent-key access
- remaining calls and reset time are visible

`preference_account_status` is free and does not consume daily tool quota.

### Troubleshooting

**`"identity": "anonymous"` in `preference_account_status`**

This means your MCP client is running without the Authorization header. Common causes:

1. **Stale anonymous config** — you may have `pref` already configured without headers:
```bash
claude mcp list              # check existing configs
claude mcp remove pref       # remove the anonymous one
```
Then re-add with auth (see Step 3 above).

2. **Key stored but not picked up** — verify the env var or credentials file:
```bash
echo $PREFERENCE_API_KEY     # should show your pref_agent_xxx key
```

3. **Header name mismatch** — the header must be exactly `Authorization: Bearer`, not `X-API-Key`.

## Security Rules

- **⚠️ Save the key to a file immediately after registration, then reference the file path in configs.** Never echo the key into terminal history, logs, chat, or prompts.
- Treat `pref_agent_*` keys as secrets.
- Never paste real keys into public logs, issues, PRs, docs, or prompts.
- Never edit `.env` files for the user.
- If identity is anonymous, the MCP client is not sending the Authorization header.
