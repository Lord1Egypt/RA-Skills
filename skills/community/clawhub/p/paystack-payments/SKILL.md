---
name: paystack-payments
description: Manage Paystack customers, transactions, payment pages, transfers, and payment operations via the Paystack API. Use this skill when users want to verify payments, manage customers, create payment pages, and review transaction data via Paystack.
---

# Paystack Payments

![Paystack Payments](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/paystack.png)

Access Paystack's payment platform via the Paystack API. Manage customers, transactions, payment pages, transfers, products, and payment operations.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=paystack-payments) for hosted connection flows and credentials so you do not need to configure Paystack API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Paystack |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Paystack |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Paystack API   │
│   (User Chat)   │     │   (API Key)  │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Paystack  │                       │
          │                      │  4. Secure Proxy      │
          │                      │  5. API Requests      │
          │                      │                       │
          ▼ ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Paystack │
    │  File    │           │ Auth     │           │ Platform │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Paystack again."

## Quick Start

```bash
# List transactions
clawlink_call_tool --tool "paystack_list_transactions" --params '{"limit": 50}'

# Get transaction details
clawlink_call_tool --tool "paystack_get_transaction" --params '{"id": "TRANSACTION_ID"}'

# Verify a transaction
clawlink_call_tool --tool "paystack_verify_transaction" --params '{"reference": "TXN_REFERENCE"}'
```

## Authentication

All Paystack tool calls are authenticated automatically by ClawLink using the user's Paystack API key.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Paystack API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=paystack and connect Paystack.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `paystack` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration paystack
```

**Response:** Returns the live tool catalog for Paystack.

### Reconnect

If Paystack tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=paystack
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration paystack`

## Security& Permissions

- Access is scoped to customers, transactions, and resources within the connected Paystack account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete customer, cancel transfer) must be confirmed.
- Transfer and payment operations affect real money — confirm recipient and amount carefully.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Paystack is connected.
2. Call `clawlink_list_tools --integration paystack` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `paystack`.
5. If no Paystack tools appear, direct the user to https://claw-link.dev/dashboard?add=paystack.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List transactions → Verify → Show status         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Code Examples

### List transactions

```bash
clawlink_call_tool --tool "paystack_list_transactions" \
  --params '{
    "per_page": 50,
    "status": "success"
  }'
```

### Verify a transaction

```bash
clawlink_call_tool --tool "paystack_verify_transaction" \
  --params '{
    "reference": "TXN_REF_ABC123"
  }'
```

### Create a customer

```bash
clawlink_call_tool --tool "paystack_create_customer" \
  --params '{
    "email": "customer@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "phone": "+2348012345678",
    "metadata": {
      "plan": "premium"
    }
  }'
```

### Create a payment page

```bash
clawlink_call_tool --tool "paystack_create_payment_page" \
  --params '{
    "name": "Product Purchase",
    "description": "One-time purchase for premium plan",
    "amount": 50000,
    "currency": "NGN"
  }'
```

## Notes

- Paystack API has rate limits. Use exponential backoff when encountering 429 errors.
- Transaction references are unique strings — verify before using in verification calls.
- Amounts are in the smallest currency unit (kobo for NGN, cents for USD).
- Currency codes must be uppercase (e.g., `NGN`, `USD`, `KES`).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration paystack`. |
| Missing connection | Paystack is not connected. Direct the user to https://claw-link.dev/dashboard?add=paystack. |
| `not_found` | Transaction, customer, or resource does not exist. Check the ID or reference. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Rate limited | Too many requests. Wait and retry with exponential backoff. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `paystack`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Paystack API Documentation](https://paystack.com/docs/api/)
- [Transaction API](https://paystack.com/docs/api/transaction/)
- [Customer API](https://paystack.com/docs/api/customer/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=paystack-payments
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Paystack](https://clawhub.ai/hith3sh/paystack-payments) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=paystack-payments)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
