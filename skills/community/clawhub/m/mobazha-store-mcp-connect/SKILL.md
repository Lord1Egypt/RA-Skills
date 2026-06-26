---
name: store-mcp-connect
description: Connect an AI agent to a Mobazha store via MCP (Model Context Protocol). Use when the user wants their agent to directly manage store products, orders, and settings.
requires_credentials: true
credential_types:
  - API token (Bearer token generated from the store's admin panel)
  - SSH credentials (optional, only for tunneled connections to remote VPS stores)
---

# Connect AI Agent to Your Store (MCP)

Connect your AI coding agent to your Mobazha store via MCP (Model Context Protocol). Once connected, your agent can directly manage products, orders, messages, and more.

> **This skill requires credentials.** The agent needs an API token from your store to connect. The agent must ask for your explicit consent before initiating any connection to your store. Tokens should be stored in environment variables, never committed to source control.

## What You Get

After connecting, your AI agent has access to 30+ store management tools:

| Category | Tools | What They Do |
|----------|-------|-------------|
| **Products** | `listings_create`, `listings_update`, `listings_delete`, `listings_list_mine`, `listings_import_json` | Full product CRUD + bulk import |
| **Orders** | `orders_get_sales`, `orders_confirm`, `orders_fulfill`, `orders_refund` | Order lifecycle |
| **Chat** | `chat_get_conversations`, `chat_send_message` | Buyer communication |
| **Discounts** | `discounts_create`, `discounts_update`, `discounts_delete` | Promotions |
| **Collections** | `collections_create`, `collections_add_products` | Product organization |
| **Profile** | `profile_get`, `profile_update` | Store identity |
| **Notifications** | `notifications_list`, `notifications_mark_read` | Activity feed |
| **Search** | `search_listings`, `search_profiles` | Marketplace discovery |
| **Finance** | `exchange_rates_get`, `wallet_get_receiving_accounts`, `fiat_get_providers` | Payments and rates |

## Connection Method: SSE (Recommended)

All Mobazha deployments include a built-in MCP SSE endpoint. This is the recommended method because:

- No additional binary to install or maintain
- Tools are always up-to-date with your store version
- Works with Claude Code, Cursor, Codex, and all modern AI agents

### SSE Endpoint

| Deployment | SSE URL |
|------------|---------|
| **SaaS** | `https://app.mobazha.org/platform/v1/mcp/sse` |
| **Standalone (custom domain)** | `https://shop.example.com/platform/v1/mcp/sse` |
| **Standalone (local Docker)** | `http://localhost/platform/v1/mcp/sse` |
| **Native install (local)** | `http://localhost:5102/platform/v1/mcp/sse` |
| **Native install (VPS)** | `http://<vps-ip>:5102/platform/v1/mcp/sse` |

---

## Step 1: Get Your API Token

### SaaS Store

1. Log in to your store at `app.mobazha.org`
2. Go to **Settings > API**
3. Click **Generate Token**
4. Copy the token

### Standalone Store (Docker with domain)

Open your store's admin panel in a browser and generate a token via **Settings > API**, or via curl:

```bash
curl -X POST https://shop.example.com/platform/v1/auth/tokens \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<your-admin-password>"}'
```

### Native Install (local or VPS)

The default gateway port for native installs is **5102**:

```bash
curl -X POST http://localhost:5102/platform/v1/auth/tokens \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<your-admin-password>"}'
```

For a VPS, replace `localhost` with your server's IP or use an SSH tunnel:

```bash
ssh -L 5102:localhost:5102 root@<vps-ip>
# Then use http://localhost:5102 from your local machine
```

---

## Step 2: Configure Your AI Agent

### Claude Code

Add to `~/.claude.json` (or project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "mobazha-store": {
      "type": "sse",
      "url": "https://shop.example.com/platform/v1/mcp/sse",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "mobazha-store": {
      "url": "https://shop.example.com/platform/v1/mcp/sse",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

Or go to **Settings > MCP Servers > Add Server** and enter the SSE URL.

### Codex CLI

```bash
codex mcp add mobazha-store --transport sse \
  --url "https://shop.example.com/platform/v1/mcp/sse" \
  --header "Authorization: Bearer <your-token>"
```

### OpenCode

Add to `opencode.json`:

```json
{
  "mcp": {
    "mobazha-store": {
      "type": "sse",
      "url": "https://shop.example.com/platform/v1/mcp/sse",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

> Replace `https://shop.example.com` with your actual store URL from the table above.

---

## Step 3: Verify the Connection

Ask your AI agent:

> "List my store's products" or "Show my recent orders"

The agent should call `listings_list_mine` or `orders_get_sales` and return results. If it works, the connection is live.

For a guide on what you can do with MCP tools, see the `store-management` skill.

---

## Advanced: stdio Transport

For environments where SSE is not supported by the AI agent, or for air-gapped setups, a `mobazha-mcp` stdio binary is available. It ships with the standalone Docker image and native install.

### When to Use stdio

- Your AI agent doesn't support SSE MCP transport
- Air-gapped or restricted network environment
- Development/debugging of the MCP layer itself

### Using stdio from Standalone Docker

The binary is bundled in the container:

```bash
docker exec -it <container> mobazha-mcp --gateway-url http://localhost:5102 --token <token>
```

### stdio CLI Reference

| Flag | Env Variable | Default | Description |
|------|-------------|---------|-------------|
| `--gateway-url` | `MOBAZHA_GATEWAY_URL` | `http://localhost:5102` | Store gateway URL |
| `--token` | `MOBAZHA_TOKEN` | (required) | Bearer token |
| `--search-url` | `MOBAZHA_SEARCH_URL` | (optional) | Marketplace search API URL |

### stdio Agent Configuration

```json
{
  "mcpServers": {
    "mobazha-store": {
      "command": "mobazha-mcp",
      "args": ["--gateway-url", "http://localhost:5102"],
      "env": {
        "MOBAZHA_TOKEN": "<your-token>"
      }
    }
  }
}
```

---

## Troubleshooting

### "connection refused" or timeout

- Native install: verify the store is running with `curl http://localhost:5102/healthz`
- Standalone Docker: the SSE endpoint is at port 80/443 (not 5102), try `curl http://localhost/healthz`
- For remote stores, check that the domain resolves and HTTPS is configured

### "401 Unauthorized"

- Verify the token: `curl -H "Authorization: Bearer <token>" http://localhost:5102/v1/profiles`
- Token may have expired — generate a new one
- Ensure the token has the required scopes for the tools you want to use

### "tool not found"

- `search_listings` and `search_profiles` require the marketplace search service
- Some tools require specific scopes on the API token (e.g., `listings:write` for `listings_create`)

### Credential Safety

- **Never hardcode tokens** in source code or config files committed to git
- Store the token in environment variables or a secrets manager
- Add MCP config files to `.gitignore` if they contain tokens
- Tokens can be revoked and regenerated at any time from the store admin panel
- The agent must **never log, display, or transmit** tokens to any party other than the target store endpoint
