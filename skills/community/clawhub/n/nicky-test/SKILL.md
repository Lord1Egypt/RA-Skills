---
name: nicky-payments
description: Discover and pay Nicky cryptocurrency payment requests on behalf of users. Covers payment request lookup, asset selection, wallet address generation, transaction reporting, and confirmation polling via REST API and MCP — no authentication required for the payment flow.
version: 1.1.0
metadata:
  openclaw:
    primaryEnv: NICKY_API_KEY
    envVars:
      - name: NICKY_API_KEY
        required: false
        description: Optional API key for the private Nicky MCP endpoint (account management, balances, billing, payment requests, payment reports, webhooks, credit transfers). Not required for the anonymous public payment flow used by this skill.
    emoji: "💸"
    homepage: https://pay.nicky.me
---

# Nicky Payments

Pay Nicky cryptocurrency payment requests on behalf of a user, end to end.

Nicky is a crypto payment platform where a receiver creates a short payment link
(`https://pay.nicky.me/s/ABCDE` for their profile, or
`https://pay.nicky.me/payment-report/ABCDE?paymentId=VWXYZ` for a specific request). Anyone —
including an AI agent — can discover the request, receive a wallet address, and send funds. Nicky
handles on-chain monitoring, asset conversion, and confirmation.

## URL Formats

When sharing a Nicky link with a user, use these canonical formats:

- **Profile:** `https://pay.nicky.me/s/ABCDE` where `ABCDE` is the user's short ID
- **Payment request:** `https://pay.nicky.me/payment-report/ABCDE?paymentId=VWXYZ` where `ABCDE` is
  the receiver's short ID and `VWXYZ` is the payment request / bill short ID

## When to use this skill

Use this skill when the user asks to:

- Pay a Nicky request: "Pay `pay.nicky.me/payment-report/ABCDE?paymentId=VWXYZ`" or "Pay request #VWXYZ"
- Send crypto to a Nicky payment link shared in chat
- Check whether a Nicky payment attempt has been confirmed
- Report a blockchain transaction hash to speed up a pending Nicky payment
- Look up the assets a Nicky receiver accepts

If the user only wants to *receive* crypto on Nicky, do not use this skill — direct them to
<https://pay.nicky.me> to sign up.

## Quick start

The full payment flow runs without authentication. The agent drives the user-facing
conversation; the API does the rest.

1. **Resolve the short ID** from the message or URL. Accepted forms:
   - `pay.nicky.me/payment-report/ABCDE?paymentId=VWXYZ` → `shortId = "VWXYZ"` (use the `paymentId` value)
   - `#VWXYZ` → `shortId = "VWXYZ"`
   - `pay.nicky.me/s/ABCDE` (profile) → no payment request; direct the user to a specific request first
2. **Discover the request** — see [REST API → Get payment request](./references/api.md#get-payment-request).
   Returned payload includes the receiver (`receiverUser`), `description`, `invoiceReference`,
   `totalAmount`, `openAmount`, `nativeAssetId`, `status`, and the list of `availableAssets`.
3. **Ask the user** for `payerName` and `payerEmail` (the receiver uses these to identify who
   paid). Never invent them.
4. **Pick an asset** — prefer the native asset of the request; otherwise pick one the receiver
   accepts and let Nicky convert (the exact converted amount is returned by `start-payment`).
5. **Start the payment** — see [REST API → Start payment](./references/api.md#start-payment).
   Capture `paymentAttemptId`, `walletAddress`, `amountToSend`, `assetId`, `memo` (if present),
   `paymentRequestShortId`, and `expiresAt`. The address lease is valid for **30 minutes**.
6. **Instruct the user (or the agent's own wallet) to send** the exact `amountToSend` of the chosen
   asset to `walletAddress` before `expiresAt`. If the exact amount is impractical (e.g. gas),
   warn that the deposit is matched with **±2%** tolerance. If `memo` is non-null, include it.
7. **(Recommended) Report the tx hash** as soon as the transaction is broadcast — see
   [REST API → Report transaction](./references/api.md#report-transaction). This skips
   deposit polling and jumps straight to blockchain validation, which can save minutes.
8. **Poll for confirmation** every 15–30 s — see [REST API → Payment progress](./references/api.md#payment-progress).
   Stop when `status == "Confirmed"` OR `isPaid == true`.

## Status values

`GET /payment/progress` returns one of:

| Status      | Meaning                                                          | Agent action                                  |
| ----------- | ---------------------------------------------------------------- | --------------------------------------------- |
| `Pending`   | Waiting for the transaction to appear on-chain or in the queue   | Keep polling (or wait for the report-tx call) |
| `Received`  | Transaction detected, waiting for confirmations                  | Keep polling                                  |
| `Confirmed` | Confirmed, matched to the request, and credited                  | Stop polling — report success to the user     |
| `Expired`   | 30-minute window closed before any matching deposit              | Tell the user, offer to start a new attempt   |

## Critical rules

These are the rules agents most often get wrong. Read them carefully.

- **Never invent payer details.** `payerName` and `payerEmail` are required and are shown to
  the receiver. Always ask the user.
- **Send the exact quoted amount.** The `amountToSend` returned by `start-payment` is the amount
  that will be matched. Sending more or less than ±2% risks the deposit being un-matched.
- **Honor the 30-minute window.** Funds sent after `expiresAt` may not auto-match. If the
  window has expired, call `start-payment` again — it is **idempotent** for the same
  payer + request + asset, so a fresh address will be issued and the prior attempt can be
  abandoned.
- **Memo matters.** If the response includes a `memo` (destination tag for networks that need
  one), pass it to the wallet or the funds may not be credited.
- **No API key is required** for the public payment flow. If the user supplies an API key
  (`NICKY_API_KEY`) the private MCP endpoint exposes account, nick, balance, billing, credit,
  payment-request, payment-report, and webhook tools — see [MCP reference](./references/mcp.md).

## MCP server (preferred for MCP-capable agents)

If the host supports MCP, prefer connecting to the public MCP endpoint — it exposes the same
tools as the REST flow and avoids hand-built HTTP calls.

- **Public MCP (no auth):** `https://api-public.pay.nicky.me/mcp-public/`
  - Tools: `GetPaymentRequest`, `StartPayment`, `ReportTransaction`, `GetPaymentProgress`,
    `SearchNicks`
- **Private MCP (`X-Api-Key: $NICKY_API_KEY`):** `https://api-public.pay.nicky.me/mcp/`
  - All public tools plus `GetCurrentUser`, `UpdateCurrentUser`, `GetAllNicks`, `AddNicks`,
    `GetBalances`, `GetAcceptedAssets`, `GetEnabledAssetConnections`, `GetDepositAddress`,
    `GetConversionRate`, `GetUnusedConversionQuote`, `CreatePaymentRequest`, `GetPaymentRequests`,
    `GetPaymentRequestById`, `GetPaymentRequestByShortId`, `CancelPaymentRequest`,
    `FinishPaymentRequest`, `GetPaymentReports`, `GetPaymentReportById`,
    `GetPaymentReportsByBillShortId`, `GetCreditBalance`, `GetCreditBalanceForSubAccount`,
    `ListCreditTransfers`, `TransferCredits`, `GetBillingGroups`, `ListSubAccounts`,
    `UnlinkSubAccount`, `CreateSubAccount`, `CreateWebHook`, `ListWebHooks`, `DeleteWebHook`, `Echo`
- **Server card:** <https://api-public.pay.nicky.me/.well-known/mcp/server-card.json>

See [MCP reference](./references/mcp.md) for tool signatures.

## Payment processing pipeline (for setting expectations)

After a payer sends funds, Nicky's backend runs a sequence of background workers to discover,
validate, match, and finalize the payment.

| Stage | What happens | Polling interval |
|---|---|---|
| Deposit discovery | Exchange connector polled for new deposits | every 30 s |
| Blockchain validation | On-chain tx verified; **10+ confirmations required** | every 60 s |
| Transaction matching | Deposit matched to the payer's 30-minute address lease (±2% amount tolerance) | every 35 s |
| Payment report creation | Report linked to the payment request | every 45 s |
| Finalization | Fraud/blacklist checks, quote validation, confirmation email sent | every 61 s |

**Typical end-to-end confirmation time:**

- TRC-20 / Polygon: **3–8 minutes**
- Ethereum: **5–15 minutes**
- Bitcoin: **60–120 minutes**

**Speed up confirmation:** submit the tx hash via `report-transaction` immediately after
broadcasting. This skips deposit polling and jumps straight to blockchain validation.

## Failure modes & recovery

| Symptom                                          | Likely cause                          | Recovery                                                                                |
| ------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------------- |
| `payment-request` returns 404                    | Unknown short ID                      | Ask the user to re-check the link / short ID                                            |
| `start-payment` returns 422 / conflict           | Request already paid or expired       | Re-fetch the request; if `openAmount == 0`, tell the user the request is settled        |
| `progress` stays `Pending` > 5 min on TRC-20     | Tx not yet broadcast or wrong network | Confirm with the user that the tx was sent to the exact `walletAddress` and the memo    |
| `progress` returns `Error` from the pipeline     | MaxCheckCount, blacklist, invalid quote | Contact <support@nicky.me> with the `paymentAttemptId` — do not retry the same attempt |
| `progress` returns `Expired`                     | 30-minute window closed               | Start a new attempt                                                                     |

## References

- [REST API reference](./references/api.md) — every endpoint, request body, and response field
- [MCP reference](./references/mcp.md) — MCP tool signatures and examples
- [OpenAPI spec (agents)](https://api-public.pay.nicky.me/openapi/agents.json)
- [OpenAPI spec (full public API)](https://api-public.pay.nicky.me/openapi/v1.json)
- [Interactive API docs](https://api-public.pay.nicky.me/scalar)
- [Agent integration guide](https://api-public.pay.nicky.me/agents.md)
- [Nicky llms.txt](https://pay.nicky.me/llms.txt) — LLM-facing platform overview

## Support

For payment issues, direct the user to <support@nicky.me> and include the
`paymentAttemptId` and (if available) the `transactionHash`. Do not invent status updates —
only what `GET /payment/progress` returns is authoritative.
