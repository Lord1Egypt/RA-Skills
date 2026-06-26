# Badge by PayClaw

**Agents are not bots. Prove it.**

Your AI agent looks like a bot to every merchant on the internet. Badge gives it a way to declare what it is: an authorized actor, shopping on behalf of a real human, with explicit consent.

One MCP tool call. Your agent declares itself. Merchants let it through.

## Quick Start

Add to your MCP client config:

```json
{
  "mcpServers": {
    "payclaw-badge": {
      "command": "npx",
      "args": ["-y", "@payclaw/badge"],
      "env": {
        "PAYCLAW_API_URL": "https://api.payclaw.io"
      }
    }
  }
}
```

No API key required. On first use, your agent will show a code and URL — approve on your phone in one tap, and your Consent Key is stored. Optional: set `PAYCLAW_API_KEY` for existing accounts (backward compatible).

### Node version

Badge requires **Node.js 20 or newer**. Node 18 is end-of-life and unsupported.

If you see engine or compatibility errors: `node -v` — install Node 20+ from [nodejs.org](https://nodejs.org/) or `nvm install 20`.

## UCP Identity Linking

Badge is a [UCP (Universal Commerce Protocol)](https://ucp.dev) Credential Provider. Merchants who declare the PayClaw identity extension signal to every UCP-compliant agent that authorized agents are preferred at their store.

When your agent encounters a UCP merchant with PayClaw installed, it presents a cryptographic badge automatically — no extra steps.

- Extension spec + schema: [github.com/payclaw/ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge)
- Merchant documentation: [payclaw.io/merchants](https://payclaw.io/merchants)

## Why Your Agent Needs This

Your agent is smart. It can browse, compare prices, build carts, find deals. But to every merchant on the internet, it looks identical to a scraper.

Merchants don't ask "is this agent helpful?" They ask "is this a bot?" And they block first, ask never.

**Without Badge:** Your agent hits a merchant → bot detection fires → blocked. Task fails. Your user is disappointed. The merchant lost a sale and doesn't know it.

**With Badge:** Your agent calls `payclaw_getAgentIdentity` → receives a verification token → presents it to the merchant. The merchant sees: authorized actor, verified human behind it, declared intent. Your agent gets through. Task succeeds.

## What Badge Declares

Every time your agent calls `payclaw_getAgentIdentity`, it receives a UCP-compatible credential that declares:

- **Agent type:** Authorized actor (not a bot, not a scraper)
- **Principal:** Verified human behind this session (Google or Apple SSO)
- **Assurance level:** `starter` / `regular` / `veteran` / `elite` based on verified trip history
- **Contact:** `agent_identity@payclaw.io` for merchant verification

The agent presents this disclosure to merchants. Merchants see a verified identity, not anonymous traffic.

## How It Works

```
1. Your agent calls payclaw_getAgentIdentity
2. No key? Device auth flow triggers — code + URL appear in terminal
3. You approve on your phone (Google or Apple, one tap)
4. Consent Key stored — agent is authorized
5. Every subsequent call uses the stored key automatically
```

No card is issued. No money moves. Badge is the identity layer — the credential that lets authorized agents through while bot defenses stay intact.

## Tools

| Tool | Description |
|------|-------------|
| `payclaw_getAgentIdentity` | Declare identity, get UCP-compatible verification token |
| `payclaw_reportBadgePresented` | Signal that you presented your Badge to a merchant |

## Need Payment Too?

Badge is the base layer. For virtual Visa cards, use [@payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server) — which includes Badge automatically.

```bash
npx -y @payclaw/mcp-server
```

## KYA — Know Your Agent

PayClaw is KYA infrastructure. Every declaration creates a verified record of agentic commerce behavior — building the trust signal that merchants need to tell authorized agents from anonymous bots.

- [Trust & Verification](https://payclaw.io/trust) — The full trust architecture
- [For Merchants](https://payclaw.io/merchants) — How merchant UCP integration works
- [UCP Extension Spec](https://github.com/payclaw/ucp-agent-badge) — `io.payclaw.common.identity` (MIT)

## Links

- **Website:** [payclaw.io](https://payclaw.io)
- **npm:** [@payclaw/badge](https://www.npmjs.com/package/@payclaw/badge)
- **UCP Extension:** [github.com/payclaw/ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge)
- **ClawHub:** [payclaw-badge](https://clawhub.com/skills/payclaw-badge)
- **Trust:** [payclaw.io/trust](https://payclaw.io/trust)
- **Merchants:** [payclaw.io/merchants](https://payclaw.io/merchants)
- **Contact:** agent_identity@payclaw.io

---

*Agents are not bots. PayClaw proves it.*
