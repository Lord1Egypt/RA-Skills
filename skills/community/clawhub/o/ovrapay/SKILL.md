---
name: ovra-agentic-payments
description: >
  Use this skill when the agent needs to buy something online, pay for a
  service, complete a checkout, manage spending budgets, or track purchases.
  Enables secure payments where the agent never sees card data. Works with
  any website that accepts Visa. EU-native, GDPR by design. Use even if
  the user just says "buy", "order", "purchase", "subscribe", or "pay for".
homepage: https://getovra.com
license: MIT
compatibility: >
  Requires OVRA_API_KEY (get at https://getovra.com/dashboard/keys) and
  MCP server connection to https://api.getovra.com/api/mcp. Network access
  to api.getovra.com required. Sandbox keys (sk_test_*) available for testing.
requires:
  env:
    - OVRA_API_KEY
metadata:
  version: "2.3.0"
  author: "Ovra Labs"
  website: "https://getovra.com"
  docs: "https://docs.getovra.com"
  mcp-endpoint: "https://api.getovra.com/api/mcp"
  data-residency: "EU (Germany)"
  compliance: "GDPR, PSD2"
---

# Ovra Agentic Payments

Secure, EU-native payments for AI agents. The agent never touches card data.

## Prerequisites

1. **Ovra API Key** — sign up at [getovra.com](https://getovra.com) and get a key from [Dashboard > Keys](https://getovra.com/dashboard/keys)
2. **MCP Server Connection** — this skill communicates with Ovra via MCP at `https://api.getovra.com/api/mcp`

Sandbox keys (`sk_test_*`) are free and have no spending limits. Production keys (`sk_live_*`) require account verification.

## Setup

Add the Ovra MCP server to your agent configuration:

```json
{
  "mcpServers": {
    "ovra": {
      "url": "https://api.getovra.com/api/mcp",
      "headers": { "Authorization": "Bearer YOUR_OVRA_API_KEY" }
    }
  }
}
```

Replace `YOUR_OVRA_API_KEY` with your key from [getovra.com/dashboard/keys](https://getovra.com/dashboard/keys).

### What this skill sends externally

All tool calls (`ovra_pay`, `ovra_card`, etc.) are sent to `https://api.getovra.com/api/mcp` via the MCP protocol. Receipt uploads (`ovra_receipt`) transmit base64-encoded PDF or PNG files (max 5MB) to the same endpoint — only upload invoices/receipts from the current transaction, never arbitrary files. No data is sent to any other external service. All data is stored in the EU (Germany) per GDPR.

## Quick Start — One-Step Payment

For most payments, use `ovra_pay` which handles the entire flow:

```
ovra_pay({
  action: "checkout",
  agentId: "ag_xxx",
  purpose: "Notion Team Plan",
  amount: 79,
  merchant: "Notion"
})
```

Returns tokenized card data (DPAN + cryptogram). The real card number is never exposed.

### Handle HTTP 402 Paywalls

When a web API returns HTTP 402 Payment Required:

```
ovra_pay({
  action: "handle_402",
  agentId: "ag_xxx",
  url: "https://api.example.com/data",
  merchant: "Example API",
  amount: 0.05
})
```

## Available Tools (12)

### Payment Flow
| Tool | Actions | Description |
|------|---------|-------------|
| `ovra_pay` | checkout, status, handle_402, discover | **Primary tool.** Complete payment in one step. |
| `ovra_intent` | list, declare, get, cancel, verify | Fine-grained intent management. |
| `ovra_credential` | obtain, grant, issue, redeem, revoke, status | Advanced credential control. |

### Cards & Policy
| Tool | Actions | Description |
|------|---------|-------------|
| `ovra_card` | issue, list, freeze, unfreeze, close, rotate | Virtual Visa card management. |
| `ovra_policy` | get | View spending policy (read-only). |

### Records & Compliance
| Tool | Actions | Description |
|------|---------|-------------|
| `ovra_transaction` | list, get, memo | Payment history and notes. |
| `ovra_receipt` | upload, get | Receipt management. Upload only PDF/PNG invoices from the current transaction. Max 5MB. |
| `ovra_dispute` | list, get, file | File disputes on transactions. |

### Admin
| Tool | Actions | Description |
|------|---------|-------------|
| `ovra_agent` | list, provision, get, update, issue_card, token_list, token_create, token_revoke | Provision and manage agents. |
| `ovra_customer` | get, update, gdpr_export, gdpr_consent, gdpr_delete | Account and GDPR compliance. |
| `ovra_merchant` | resolve, explain, list_mcc, suggest | Merchant intelligence. |
| `ovra_config` | (varies) | System configuration. |

## Step-by-Step Flow (when you need fine control)

For cases where `ovra_pay` is too opaque:

```
1. ovra_policy     → get: check spending rules
2. ovra_intent     → declare: state what to buy
3. ovra_credential → obtain: get DPAN + cryptogram
4. ovra_receipt    → upload: attach proof
5. ovra_intent     → verify: confirm actual vs expected
```

### Step 1: Check policy

```
ovra_policy({ action: "get", agentId: "ag_xxx" })
```

### Step 2: Declare intent

```
ovra_intent({
  action: "declare",
  agentId: "ag_xxx",
  purpose: "Buy wireless keyboard",
  expectedAmount: 49.99,
  expectedMerchant: "amazon.de"
})
```

If status is `pending_approval`: **stop and wait**. Tell the user approval is needed in the dashboard.

### Step 3: Get credentials

```
ovra_credential({ action: "obtain", intentId: "in_xxx" })
```

Returns DPAN + cryptogram. The agent never sees the real card number.

### Step 4: Attach receipt

Only upload the invoice/receipt PDF or PNG from this specific transaction. Never upload unrelated files.

```
ovra_receipt({
  action: "upload",
  intentId: "in_xxx",
  fileBase64: "JVBER...",
  fileName: "invoice.pdf"
})
```

### Step 5: Verify

```
ovra_intent({
  action: "verify",
  intentId: "in_xxx",
  actualAmountEuros: 49.99,
  actualMerchant: "amazon.de"
})
```

## Gotchas

- **Use `ovra_pay` for most payments.** Step-by-step is for edge cases.
- Intents expire (default 24h). If expired, create a new one.
- `pending_approval` means a human must approve. The agent cannot bypass this.
- Card data must never appear in output, logs, or context.
- `ovra_card` close is irreversible.
- `ovra_customer` gdpr_delete permanently erases ALL data per GDPR Art. 17.

## Agent vs Human boundaries

**Agent does autonomously:** checkout via ovra_pay, declare intents, obtain credentials, upload receipts, verify transactions, list transactions, file disputes, check balances, handle 402 paywalls.

**Agent asks human first:** provision/delete agents, fund wallets, change policies, freeze/unfreeze cards, manage API keys, approve high-value intents, GDPR deletion.

## Checking balance and status

```
ovra_agent({ action: "get", agentId: "ag_xxx" })
ovra_policy({ action: "get", agentId: "ag_xxx" })
ovra_transaction({ action: "list", agentId: "ag_xxx", limit: 5 })
ovra_intent({ action: "list", status: "pending_approval" })
```

## Filing a dispute

```
ovra_dispute({
  action: "file",
  transactionId: "tx_xxx",
  reason: "not_received",
  description: "Package not delivered after 14 days"
})
```

Reasons: `unauthorized`, `fraud`, `not_received`, `duplicate`, `incorrect_amount`, `canceled`.

## Merchant intelligence

```
ovra_merchant({ action: "suggest", query: "cloud hosting" })
ovra_merchant({ action: "resolve", query: "hetzner.com" })
```
