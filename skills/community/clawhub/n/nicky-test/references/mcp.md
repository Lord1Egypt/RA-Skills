# MCP reference

Nicky exposes a Model Context Protocol (MCP) server. Prefer the MCP endpoint when the host
agent runtime supports MCP — it removes the need to hand-build HTTP calls.

## Endpoints

| Endpoint                                                 | Auth                          | Use case                                    |
| -------------------------------------------------------- | ----------------------------- | ------------------------------------------- |
| `https://api-public.pay.nicky.me/mcp-public/`            | none                          | Public payment flow (this skill's main use) |
| `https://api-public.pay.nicky.me/mcp/`                   | `X-Api-Key: $NICKY_API_KEY`    | Account, billing, webhooks, balances, etc.  |

Discovery:

- Server card (JSON): <https://api-public.pay.nicky.me/.well-known/mcp/server-card.json>
- Agent integration guide: <https://api-public.pay.nicky.me/agents.md>
- OpenAPI spec (agents): <https://api-public.pay.nicky.me/openapi/agents.json>

## Public tools

The public MCP exposes the same five tools listed below. Their semantics match the REST
endpoints 1:1 — see [api.md](./api.md) for the field-level details.

### `GetPaymentRequest`

| Parameter | Type   | Required | Notes                                |
| --------- | ------ | -------- | ------------------------------------ |
| `shortId` | string | yes      | 6-character short ID or nick         |

Returns the same payload as `GET /api/agents/payment-request`.

### `StartPayment`

| Parameter              | Type   | Required | Notes                                              |
| ---------------------- | ------ | -------- | -------------------------------------------------- |
| `paymentRequestShortId`| string | yes      |                                                    |
| `assetId`              | string | yes      | One of the accepted assets from `GetPaymentRequest`|
| `payerName`            | string | yes      | Always ask the user                                |
| `payerEmail`           | string | yes      | Always ask the user                                |

Returns `{ paymentAttemptId, walletAddress, memo, amountToSend, assetId, assetName,
paymentRequestShortId, expiresAt, createdAt, status }`.

### `ReportTransaction`

| Parameter         | Type   | Required | Notes                                          |
| ----------------- | ------ | -------- | ---------------------------------------------- |
| `paymentAttemptId`| string | yes      | From `StartPayment`                            |
| `transactionHash` | string | yes      | Full on-chain tx hash                          |

Strongly recommended immediately after broadcasting the tx. Returns the updated payment
progress (same shape as `GetPaymentProgress`).

### `GetPaymentProgress`

| Parameter         | Type   | Required | Notes                                          |
| ----------------- | ------ | -------- | ---------------------------------------------- |
| `paymentAttemptId`| string | yes      | From `StartPayment`                            |

Returns `{ paymentAttemptId, walletAddress, expectedAmount, assetId, assetName, status,
isPaid, createdAt, expiresAt, finishedAt, paymentRequest, transactions,
suggestedTransactionHash }`. Poll every 15–30 s until `status == "Confirmed"` or
`isPaid == true`.

### `SearchNicks`

| Parameter | Type   | Required | Notes                                          |
| --------- | ------ | -------- | ---------------------------------------------- |
| `query`   | string | yes      | Nick, email, or domain to search for           |

Returns a list of matching users with their nicks, public names, and contact details.

## Private tools (require `NICKY_API_KEY`)

The private MCP adds account-level tools. This skill does not exercise them, but the agent
should be aware they exist if the user has a Nicky account and an API key:

- **Account & profile:** `GetCurrentUser`, `UpdateCurrentUser`
- **Nicks:** `GetAllNicks`, `AddNicks`
- **Balances & accepted assets:** `GetBalances`, `GetAcceptedAssets`, `GetEnabledAssetConnections`
- **Wallet:** `GetDepositAddress`
- **Conversion rates:** `GetConversionRate`, `GetUnusedConversionQuote`
- **Payment requests:** `CreatePaymentRequest`, `GetPaymentRequests`, `GetPaymentRequestById`,
  `GetPaymentRequestByShortId`, `CancelPaymentRequest`, `FinishPaymentRequest`
- **Payment reports:** `GetPaymentReports`, `GetPaymentReportById`, `GetPaymentReportsByBillShortId`
- **Billing / subaccounts:** `GetBillingGroups`, `ListSubAccounts`, `UnlinkSubAccount`,
  `CreateSubAccount`
- **Credits:** `GetCreditBalance`, `GetCreditBalanceForSubAccount`, `ListCreditTransfers`,
  `TransferCredits`
- **Webhooks:** `CreateWebHook`, `ListWebHooks`, `DeleteWebHook`
- **Utility:** `Echo` (connectivity test)
- All five public tools above

If the user wants to use these, set `NICKY_API_KEY` and connect to the private MCP endpoint.

## Example MCP session

A typical agent-driven session against the public MCP:

```
1. GetPaymentRequest({ shortId: "VWXYZ" })
   → discovers receiver, native asset, accepted assets
2. Ask the user for payerName + payerEmail
3. StartPayment({
     paymentRequestShortId: "VWXYZ",
     assetId: "USDT_TRC20",
     payerName: "John Doe",
     payerEmail: "john@example.com"
   })
   → { paymentAttemptId: "X7K2P1", walletAddress: "TX...", amountToSend: 50, expiresAt: "..." }
4. User (or agent wallet) sends 50 USDT to TX... before expiresAt (and any memo, if returned)
5. ReportTransaction({ paymentAttemptId: "X7K2P1", transactionHash: "0x..." })
6. Loop every 15–30 s:
     GetPaymentProgress({ paymentAttemptId: "X7K2P1" })
   Stop when status === "Confirmed" || isPaid === true
```
