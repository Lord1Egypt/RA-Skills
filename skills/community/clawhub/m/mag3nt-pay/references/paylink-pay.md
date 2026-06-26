# Pay Link Settlement — Pay-per-Access via Pay Links

Use when the server returns HTTP 402 with a `paylink` object in the response body. Pay Links are the universal payment interface — agents pay with just `card_id` + `card_token`, **no API key required**.

## Detection

```typescript
if (response.status === 402) {
  const body = await response.json();
  if (body.paylink?.code) {
    // This is a Pay Link challenge
    const { code, url, amount, memo } = body.paylink;
  }
}
```

## Settle the Pay Link

The agent settles the Pay Link by calling `POST /api/pay/{code}/settle` on the Mag3nt API. **No API key is required** — the card token is sufficient.

```typescript
const settleResponse = await fetch(
  `https://mag3nt.com/api/pay/${body.paylink.code}/settle`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      protocol: "x402",
      payer_card_id: process.env.MAG3NT_CARD_ID,
      payer_card_token: process.env.MAG3NT_CARD_TOKEN,
    }),
  }
);

const settlement = await settleResponse.json();

if (settlement.success) {
  console.log("Payment settled:", settlement.transaction_id);
}
```

## Request Body

Two settlement methods are supported:

**Card settlement (agent-to-agent):**

| Field | Type | Description |
|-------|------|-------------|
| `protocol` | string | Settlement protocol (e.g. `"x402"`) |
| `payer_card_id` | string | Agent's card ID (`mag3nt_...`, legacy `sx_...`) |
| `payer_card_token` | string | Agent's card token (`tok_...`) |

**On-chain settlement (wallet-to-wallet):**

| Field | Type | Description |
|-------|------|-------------|
| `tx_hash` | string | On-chain transaction hash |
| `from_address` | string | Sender wallet address |
| `amount` | number | Amount sent |

## Response

```json
{
  "success": true,
  "transaction_id": "txn_abc123"
}
```

## Retry the Original Request

After settlement, retry the original request with the paylink code:

```typescript
const retryResponse = await fetch(originalUrl, {
  method: originalMethod,
  headers: {
    "Content-Type": "application/json",
    "X-Mag3nt-Paylink": body.paylink.code,
  },
  body: originalBody,
});
```

## Full Example

```typescript
// 1. Call the screening API
const res = await fetch("https://screening.example.com/api/screen", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "John Doe" }),
});

// 2. Detect the 402 with Pay Link
if (res.status === 402) {
  const { paylink } = await res.json();

  // 3. Settle with card credentials (no API key needed)
  const settle = await fetch(
    `https://mag3nt.com/api/pay/${paylink.code}/settle`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        protocol: "x402",
        payer_card_id: process.env.MAG3NT_CARD_ID,
        payer_card_token: process.env.MAG3NT_CARD_TOKEN,
      }),
    }
  );

  const { success, transaction_id } = await settle.json();
  console.log("Paid:", success, transaction_id);

  // 4. Retry with the paylink code
  const result = await fetch("https://screening.example.com/api/screen", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Mag3nt-Paylink": paylink.code,
    },
    body: JSON.stringify({ name: "John Doe" }),
  });

  const screening = await result.json();
  console.log("Screening result:", screening);
}
```

## Key Points

- **No API key required** — card credentials are sufficient to settle a Pay Link
- **Idempotent** — settling an already-settled Pay Link returns `410 Gone`. Handle gracefully.
- **Retry header** — use `X-Mag3nt-Paylink` header when retrying the original request
