# LetAgentPay Skill for OpenClaw

Spending guardrails for your OpenClaw agent. Set budgets, restrict categories, enforce per-request limits, and require human approval for large purchases — all through a deterministic policy engine, not prompt-based rules.

## What it does

Every time your agent wants to spend money, the request goes through 9 policy checks:

1. Agent status (active/paused)
2. Velocity (requests per minute / hour — runaway-loop guard)
3. Category (allowed/blocked)
4. Per-request limit
5. Schedule (time-of-day, day-of-week)
6. Daily spending limit
7. Weekly spending limit
8. Monthly spending limit
9. Total budget

If all checks pass and auto-approve criteria are met, the purchase proceeds instantly. Otherwise, you get a notification in your chat to approve or reject.

## Quick Start

### 1. Get a token

Sign up at [letagentpay.com](https://letagentpay.com) and create an agent to get your `agt_xxx` token.

Or self-host: see [self-hosting docs](https://github.com/LetAgentPay/letagentpay).

### 2. Set environment variable

```bash
export LETAGENTPAY_TOKEN=agt_xxx
```

### 3. Add MCP server to OpenClaw config

Edit `~/.openclaw/config.json`:

```json
{
  "mcpServers": {
    "letagentpay": {
      "command": "npx",
      "args": ["-y", "letagentpay-mcp"],
      "env": {
        "LETAGENTPAY_TOKEN": "${LETAGENTPAY_TOKEN}"
      }
    }
  }
}
```

### 4. Install the skill

```bash
cp -r . ~/.openclaw/workspace/skills/letagentpay
```

### 5. Try it

Tell your agent: "Buy me a Notion subscription for $10/month"

The agent will:
1. Call `request_purchase` with amount, category, and description
2. If auto-approved: confirm the purchase was made
3. If pending: notify you to approve via your chat channel

## Self-Hosted

Replace the MCP server config with your instance URL:

```json
{
  "mcpServers": {
    "letagentpay": {
      "command": "npx",
      "args": ["-y", "letagentpay-mcp"],
      "env": {
        "LETAGENTPAY_TOKEN": "${LETAGENTPAY_TOKEN}",
        "LETAGENTPAY_API_URL": "http://your-server:8000/api/v1"
      }
    }
  }
}
```

## Security Model

Policy enforcement happens **on the LetAgentPay server**, not on the agent's machine. The agent token (`agt_`) only grants access to submit purchase requests and check status — it cannot modify policies or approve its own requests.

This is a **cooperative enforcement** model: it protects against budget overruns, category violations, and scheduling mistakes. It does not sandbox a malicious agent with direct access to payment APIs.

> **Important:** Don't store payment API keys (Stripe, PayPal, etc.) in environment variables accessible to OpenClaw. LetAgentPay should be the only channel for agent spending. Use `pending` + manual approval for high-value purchases.

## Also works with

The same MCP server works with any MCP-compatible client:

- **Claude Desktop** / **Claude Code**
- **Cursor**
- **Any MCP client**

See [MCP server docs](https://github.com/LetAgentPay/letagentpay-mcp).

## SDKs

If you're building your own agent integration:

- **Python**: `pip install letagentpay` ([GitHub](https://github.com/LetAgentPay/letagentpay-python))
- **TypeScript**: `npm install letagentpay` ([GitHub](https://github.com/LetAgentPay/letagentpay-js))

## Links

- [LetAgentPay](https://letagentpay.com) — Dashboard & playground
- [GitHub](https://github.com/LetAgentPay/letagentpay) — Main repo (open source)
- [Agent API Reference](https://letagentpay.com/developers)

## License

MIT
