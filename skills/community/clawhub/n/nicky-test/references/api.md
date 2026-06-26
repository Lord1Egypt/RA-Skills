# REST API reference

Base URL: `https://api-public.pay.nicky.me`

All endpoints below are **anonymous** — no API key, no Authorization header. The agent should
not send any auth header on these calls.

The canonical machine-readable schema is at
`https://api-public.pay.nicky.me/openapi/agents.json`.

## URL Formats

When you need to share a link with the user, use these canonical formats:

- **Profile:** `https://pay.nicky.me/s/ABCDE` (short ID)
- **Profile by email:** `https://pay.nicky.me/e/EMAIL`
- **Profile by domain:** `https://pay.nicky.me/d/DOMAIN`
- **Payment request:** `https://pay.nicky.me/payment-report/ABCDE?paymentId=VWXYZ` (receiver short ID
  + payment request / bill short ID)

## Get payment request

```
GET /api/agents/payment-request?shortId={shortId}
```

| Query param | Type   | Notes                                          |
| ----------- | ------ | ---------------------------------------------- |
| `shortId`   | string | 6-character short ID, or a `nick` (username)   |

Example:

```bash
curl 'https://api-public.pay.nicky.me/api/agents/payment-request?shortId=ABCDEF'
```

Response:

```json
{
  "shortId": "VWXYZ",
  "description": "Invoice for consulting work",
  "invoiceReference": "INV-2026-0042",
  "totalAmount": 50.0,
  "openAmount": 50.0,
  "nativeAssetId": "USDT_TRC20",
  "status": "PaymentPending",
  "receiverUser": {
    "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "email": "alice@example.com",
    "name": "Alice Example",
    "publicName": "alice",
    "websiteUrl": "https://alice.example.com",
    "bio": "Freelance illustrator",
    "country": "NL",
    "hasProfilePicture": true
  },
  "availableAssets": [
    {
      "id": "USDT_TRC20",
      "assetName": "USDT (Tron, TRC-20)",
      "isFiat": false,
      "decimalPrecisionUI": 2
    },
    {
      "id": "ETH.USDT",
      "assetName": "USDT (Ethereum, ERC-20)",
      "isFiat": false,
      "decimalPrecisionUI": 6
    }
  ]
}
```

Notes:

- `openAmount` may be less than `totalAmount` for partially-paid requests.
- `availableAssets[i]` is the list of every asset the receiver accepts. The native asset is the one
  whose `id` matches `nativeAssetId`. The exact amount to send for the native asset is `openAmount`
  in `nativeAssetId`; for every other asset, call `start-payment` to receive the exact converted
  `amountToSend`.
- `status == "PaymentPending"` means the request is open and can be paid. Other values: `Finished`,
  `Canceled`.
- `receiverUser` may be a partial profile — fields like `email` can be `null` if the user is
  anonymous.

## Start payment

```
POST /api/agents/payment/start
Content-Type: application/json
```

Body:

```json
{
  "paymentRequestShortId": "ABCDEF",
  "assetId": "USDT_TRC20",
  "payerName": "John Doe",
  "payerEmail": "john@example.com"
}
```

| Field                    | Required | Notes                                                                       |
| ------------------------ | -------- | --------------------------------------------------------------------------- |
| `paymentRequestShortId`  | yes      | The `shortId` from `get-payment-request`                                    |
| `assetId`                | yes      | One of the IDs from `availableAssets[].id`                                  |
| `payerName`              | yes      | Receiver-visible identifier                                                 |
| `payerEmail`             | yes      | Receiver-visible contact                                                    |

Response:

```json
{
  "paymentAttemptId": "X7K2P1",
  "walletAddress": "TX...abc",
  "memo": null,
  "amountToSend": 50.0,
  "assetId": "USDT_TRC20",
  "assetName": "USDT (Tron, TRC-20)",
  "paymentRequestShortId": "ABCDEF",
  "expiresAt": "2026-06-08T13:55:00Z",
  "createdAt": "2026-06-08T13:25:00Z",
  "status": "Pending"
}
```

Notes:

- `memo` is non-null for networks that require a destination tag (XRP, Stellar, etc.). Pass it to
  the wallet when sending the funds.
- `amountToSend` is the exact amount to send. If you chose a non-native asset, the figure is
  already converted at a live rate and is the value that will be matched.
- Idempotency: calling `start-payment` again with the same `paymentRequestShortId`, `assetId`, and
  `payerEmail` returns the *same* `paymentAttemptId` and `walletAddress`. Safe to call if the
  user lost the previous attempt.

## Report transaction

```
POST /api/agents/payment/report-transaction
Content-Type: application/json
```

Body:

```json
{
  "paymentAttemptId": "X7K2P1",
  "transactionHash": "0xabc123..."
}
```

| Field             | Required | Notes                                                                            |
| ----------------- | -------- | -------------------------------------------------------------------------------- |
| `paymentAttemptId`| yes      | Returned by `start-payment`                                                      |
| `transactionHash` | yes      | The full on-chain tx hash. Nicky validates it on-chain and starts confirmation.  |

This call is **strongly recommended** as soon as the user (or the agent's wallet) broadcasts
the transaction. It short-circuits Nicky's deposit-discovery polling and jumps the pipeline
to blockchain validation. The response is the updated `AgentPaymentProgressResponse` (see
below).

## Payment progress

```
GET /api/agents/payment/progress?paymentAttemptId={id}
```

Response:

```json
{
  "paymentAttemptId": "X7K2P1",
  "walletAddress": "TX...abc",
  "expectedAmount": 50.0,
  "assetId": "USDT_TRC20",
  "assetName": "USDT (Tron, TRC-20)",
  "status": "Received",
  "isPaid": false,
  "createdAt": "2026-06-08T13:25:00Z",
  "expiresAt": "2026-06-08T13:55:00Z",
  "finishedAt": null,
  "paymentRequest": {
    "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "createdDate": "2026-06-08T13:00:00Z",
    "blockchainAssetId": "USDT_TRC20",
    "amountNative": 50.0,
    "requester": null,
    "creator": { "...": "..." },
    "status": "PaymentPending",
    "successUrl": null,
    "cancelUrl": null,
    "openAmountNative": 0.0,
    "bill": { "...": "..." }
  },
  "transactions": [
    {
      "transactionHash": "0xabc123...",
      "assetId": "USDT_TRC20",
      "receiverAddress": "TX...abc",
      "createdDate": "2026-06-08T13:30:00Z",
      "blockchainStatus": "TxFound",
      "paymentReportStatus": "WaitingForBlockchainCheck"
    }
  ],
  "suggestedTransactionHash": "0xabc123..."
}
```

| Field                     | Meaning                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------- |
| `status`                  | `Pending` / `Received` / `Confirmed` / `Expired`                                       |
| `isPaid`                  | True once the request is fully settled                                                |
| `finishedAt`              | Set once the payment is `Confirmed`                                                   |
| `expectedAmount`          | The amount the agent should send (matches `amountToSend` from `start-payment`)         |
| `transactions`            | Blockchain transactions found for this attempt                                         |
| `transactions[].blockchainStatus`     | `Pending` / `TxFound` / `Finished` / `Error`                              |
| `transactions[].paymentReportStatus`  | `WaitingForBlockchainCheck` / `Finished` / `Error`                       |
| `suggestedTransactionHash`           | The hash reported by the agent (if any)                                  |

**Poll cadence:** every 15–30 seconds is appropriate. Avoid polling faster than 10 s — the
pipeline itself runs on 30–60 s intervals and faster polling does not produce fresher data.

## Error responses

The API returns standard HTTP status codes:

| Status | Meaning                                                                |
| ------ | ---------------------------------------------------------------------- |
| 200/201 | Success                                                               |
| 400    | Malformed request (e.g. unknown `assetId` for the request)             |
| 404    | Unknown `shortId` or `paymentAttemptId`                                |
| 422    | Conflict — request already paid, expired, or payer info inconsistent   |
| 429    | Rate limited (per-IP / per-token)                                      |
| 5xx    | Server error — back off and retry with jitter                          |

The agent should treat any 5xx as transient and retry the call once after 2–3 s before
surfacing the error to the user.
