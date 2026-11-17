# Habilis SaaS & MCP Gateway Architecture Pattern

## Overview
**Habilis** is an autonomous SaaS and MCP Gateway built inside Orca IDE (`/home/orca/orca/habilis`) running as `habilis.service` on port `3080` (publicly routed via `https://xvix.com.br`). It acts as a secure reverse-proxy and AI intelligence layer between client AI agents (Hermes, Claude Desktop, Cursor, n8n) and external advertising APIs (Meta Ads Graph API v21.0+, OpenAI Ads API).

---

## 1. Core Architectural Pillars

### A. Real-Time Workspace Synchronization with Orca
- **Shared Filesystem**: The project workspace lives at `/home/orca/orca/habilis`, owned by `orca:orca`.
- **Dual Runtime**: Orca IDE / Server (`orca-serve.service` at `wss://orca.xvix.com.br:6768`) and system services share the same files in real time. Changes in terminal or Orca are instantly synchronized.
- **Service Supervision**: Managed via systemd service `habilis.service` (`systemctl status|restart habilis`).

### B. Security Hardening & Zero-Leak Admin Protection
1. **Hidden Admin Console**: The `/admin` link is **strictly omitted from the public Navbar/Header** to prevent malicious bot scanning and unauthorized discovery. Access is direct via URL (`https://xvix.com.br/admin`).
2. **Admin Authentication**: Protected by administrative password (`Ramel@2026`).
3. **Thin-Skill Isolation**: Client AI agents receive only lightweight endpoints and Bearer tokens (`hab_live_...`). Proprietary prompts, CPA heuristics, and safe-margin rendering (1080x1080) execute server-side.
4. **BYOK (Bring Your Own Keys) Vault**: Client ad account secrets (Meta Access Tokens, Pixel IDs, OpenAI API Keys) are encrypted in the local vault and never exposed in chat transcripts.

### C. Default Language Standard (EN First)
- **Default Locale**: Interface and pages (`/`, `/dashboard`, `/admin`, and `<html lang="en">`) default to **English (`EN`)**.
- **Bilingual Toggle**: Built-in PT/EN switcher available in the Navbar.

---

## 2. Dynamic Thin-Skill Exporter Matrix

When an admin or client generates a skill, Habilis automatically generates pre-configured client bundles:

| Target Client | File / Format | Integration Mechanism |
| :--- | :--- | :--- |
| **Hermes Agent** | `SKILL.md` | Skill markdown with pre-injected Bearer curl calls and tool schemas. |
| **Claude Desktop** | `claude_desktop_config.json` | `mcpServers` definition with remote MCP endpoint. |
| **Cursor IDE** | `.cursor/mcp.json` | MCP HTTP/SSE remote connection definition with headers. |
| **n8n Automation** | `HTTP Request Node` | Pre-configured JSON payload with `Authorization: Bearer <TOKEN>`. |

---

## 3. Production Deployment & Stripe Integration

### A. Environment Configuration (`/home/orca/orca/habilis/.env.local`)
```env
# Stripe Production Keys
STRIPE_SECRET_KEY=sk_live_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# App URL & Server Base
NEXT_PUBLIC_APP_URL=https://xvix.com.br
SERVER_BASE_URL=https://xvix.com.br
ADMIN_PASSWORD=Ramel@2026
```

### B. Webhooks & Endpoints
- **Universal MCP Gateway**: `https://xvix.com.br/api/mcp` (JSON-RPC 2.0 / SSE)
- **Stripe Checkout**: `https://xvix.com.br/api/checkout`
- **Stripe Webhook Listener**: `https://xvix.com.br/api/webhooks/stripe` (Events: `checkout.session.completed`, `invoice.payment_succeeded`, `customer.subscription.deleted`)
- **Skill Generator API**: `https://xvix.com.br/api/skills/generate?serviceId=<id>&token=<token>&format=hermes`

### C. Build & Restart Procedure
```bash
cd /home/orca/orca/habilis
npm run build
chown -R orca:orca /home/orca/orca/habilis
systemctl restart habilis
```
