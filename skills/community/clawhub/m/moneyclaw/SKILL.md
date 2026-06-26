---
name: moneyclaw
description: Inspect a MoneyClaw wallet, create bounded payment tasks, and continue user-confirmed payment steps using a prepaid account. Use only when the user clearly asks to use MoneyClaw for their own payments.
metadata:
  openclaw:
    homepage: https://moneyclaw.ai/openclaw
    primaryEnv: MONEYCLAW_API_KEY
    requires:
      env:
        - MONEYCLAW_API_KEY
---

# MoneyClaw

 MoneyClaw helps OpenClaw agents inspect prepaid payment state, create auditable payment tasks, and continue explicitly requested payment steps.

Primary use case: buyer-side payments for OpenClaw agents.

## Authentication

This skill requires one MoneyClaw API key.

```bash
Authorization: Bearer $MONEYCLAW_API_KEY
```

Base URL: `https://moneyclaw.ai/api`

## Trust Model

MoneyClaw is designed for real, user-authorized agent payments.

- use prepaid balances to keep risk bounded
- use payment intents as the main auditable execution surface
- keep account inbox state inspectable for receipts and account messages
- let the user approve the payment step before money moves

## Approval Model

Default to dashboard approval unless the account has explicitly enabled agent auto-approval.

- MoneyClaw accounts expose an account-level `agentAutoApproveEnabled` flag through `GET /api/me`.
- When that flag is off, API-key-created payment tasks wait for dashboard approval before spending.
- When that flag is on, API-key-created payment tasks can be auto-approved within the merchant and amount scope of the task.
- Do not assume agent auto-approval is enabled unless the account state confirms it.

## Safety Boundaries

- Only use MoneyClaw for purchases or payment flows explicitly requested by the user. If the account is not clearly configured for agent auto-approval and the user has not explicitly asked for the next payment step, stop and ask.
- Only use wallet, card, and billing data returned by the user's own MoneyClaw account.
- Respect merchant, issuer, card-network, and verification controls.
- Treat fraud checks, KYC, sanctions, geography rules, merchant restrictions, issuer declines, and other payment controls as hard boundaries.
- Never fabricate billing identity, cardholder data, addresses, names, phone numbers, or verification information.
- If a transaction fails, looks suspicious, or produces conflicting signals, stop and inspect transaction state before retrying.
- Prefer prepaid, bounded-risk flows by default.
- Never invoke this skill automatically from a shopping, billing, or checkout page. Use it only after an explicit user request to use MoneyClaw.

## Before Any High-Risk Step

Before any action that can spend funds, retrieve execution details, or submit a payment step:

1. Confirm the exact merchant domain.
2. Confirm the amount and currency.
3. Confirm the user explicitly asked for this exact action, or that the account is clearly configured for agent auto-approval for this scope.
4. Stop if that confirmation is missing or ambiguous.

## Default Buyer Flow

Use the product in this order:

1. `GET /api/me` for wallet readiness, deposit address, and inbox context. Fresh accounts may also finish mailbox, deposit-address, and provider setup on this first authenticated read.
2. `POST /api/payment-intents` for the exact purchase.
3. If `agentAutoApproveEnabled` is off, wait for dashboard approval. If it is on, the API-key task can move directly toward `approved` and `card_ready`. Approved tasks can auto-prepare or reuse the account's hidden execution card when wallet funding is available.
   On the first hidden-card bootstrap for an account, MoneyClaw may reserve the provider minimum initial deposit onto that shared hidden card even if the current task amount is smaller. Any residual stays on the same hidden card for later tasks.
4. Use `GET /api/payment-intents/:intentId/credentials` only when the task is `card_ready` and the user explicitly asked to continue the current payment step.
5. After a successful one-time checkout, use `POST /api/payment-intents/:intentId/reconcile` to write the settled charge back into MoneyClaw accounting.
6. Inspect payment-task state and wallet transactions before retrying.

## Load References When Needed

- Read `references/payment-safety.md` before entering payment details on an unfamiliar merchant, when a checkout keeps failing, or when retry boundaries matter.

## Core Jobs

### 1. Check account readiness

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/me
```

Important fields:

- `balance`: wallet balance
- `depositAddress`: where to send USDT
- `mailboxAddress`: inbox address for receipts and account messages
- `agentAutoApproveEnabled`: whether API-key-created payment tasks can auto-approve without a dashboard click

When the user asks for readiness, report wallet balance, deposit address, inbox state, and whether a payment task can proceed.

### 2. Create an auditable payment task

```bash
curl -X POST -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "intentType": "one_time_purchase",
    "merchantName": "OpenAI",
    "merchantDomain": "openai.com",
    "expectedAmount": "20.00",
    "fundingCap": "20.00",
    "currency": "USD",
    "metadata": {
      "serviceName": "ChatGPT Plus"
    }
  }' \
  https://moneyclaw.ai/api/payment-intents
```

Use payment intents to hold merchant context, approval state, and audit history.

Rules:

- use the account's `agentAutoApproveEnabled` state as the default control path for API-key-created tasks
- if the account does not have agent auto-approval enabled and the intent is `pending_approval`, stop and ask the user to approve it in the dashboard instead of pretending you can finish approval yourself
- treat the intent as the source of truth for execution state, not the card

### 3. Inspect the payment task state

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/payment-intents/{intentId}
```

Use the payment task as the source of truth for readiness, approval, execution, and completion.

### 4. Read the payment task history

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/payment-intents/{intentId}/history
```

Use the history when the user wants an audit trail or when a payment step gave ambiguous results.

### 5. Continue the approved payment step

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/payment-intents/{intentId}/credentials
```

Rules:

- only call this when the intent is `card_ready`
- only call this after the user explicitly asked to continue that payment step
- do not treat these execution details as a general account-level card surface
- do not expose PAN or CVV longer than needed for the active checkout

## Payment Execution Rules

- The spending model is prepaid. The loaded balance is the hard limit.
- Fresh accounts may need enough wallet balance for the first shared hidden-card bootstrap, not only for the immediate merchant total.
- Before payment, confirm the merchant domain and total amount are correct.
- Use the billing address returned by MoneyClaw. Never invent one.
- If a merchant asks for unexpected out-of-band verification, stop and ask the user instead of assuming the skill should continue automatically.
- Do not retry the same merchant checkout more than twice in one session without user confirmation or clear pre-authorization.
- If the user asks for a risky or suspicious payment, stop and explain why.

Use `references/payment-safety.md` for expanded safety and retry guidance.

## Good Default Prompt Shapes

- `Check my MoneyClaw account and tell me if the wallet, inbox, and payment tasks are ready.`
- `Create a payment task for this purchase and keep the amount bounded to the expected total.`
- `Continue this already approved payment step.`
- `Check whether this payment task completed, still needs dashboard approval, or should be inspected before retrying.`
