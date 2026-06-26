# Universal Pay — Pay Any 402-Protected API

The universal payment endpoint `POST /api/pay` handles 402-based protocols (x402 and MPP) in a single call. The engine probes the target URL, detects the protocol, settles on-chain, and returns settlement evidence.

## When to Use

Use this for **any** external API that returns HTTP 402 with x402 or MPP headers. The engine detects the protocol — you don't need to. For AP2 (mandate-based, not 402), see `references/ap2-pay.md`.

## Endpoint

```
POST https://mag3nt.com/api/pay
Authorization: Bearer <MAG3NT_API_KEY>
Content-Type: application/json
```

## Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_id` | string | yes | Card identifier (`mag3nt_...`, legacy `sx_...`) |
| `card_token` | string | yes | Card secret token (`tok_...`) |
| `url` | string | yes | The 402-protected URL the agent originally called |
| `method` | string | no | HTTP method the agent used (default: `POST`) |
| `body` | object | no | Request body the agent originally sent |
| `headers` | object | no | Additional headers for the probe request |

Pass the same URL, method, and body that triggered the 402. The engine will probe the URL, extract the payment challenge, settle on-chain, and return evidence.

## Response

The engine returns **settlement evidence**. It does NOT fulfill the purchase for you — every merchant may implement fulfillment differently.

| Field | Description |
|-------|-------------|
| `success` | `true` if settlement completed |
| `transaction_id` | Mag3nt transaction ID for audit |
| `amount_debited` | Total charged to the card (merchant + fee) |
| `merchant_amount` | Amount sent to the merchant |
| `platform_fee` | Mag3nt platform fee |
| `token` | Settlement asset (e.g. USDC) |
| `network` | CAIP-2 network where settlement happened |
| `protocol` | Detected protocol (x402, tempo, etc.) |
| `settlement.status` | On-chain status |
| `settlement.tx_hash` | On-chain transaction hash — proof of payment |
| `credential.header_name` | HTTP header name for fulfillment |
| `credential.header_value` | HTTP header value — settlement proof |
| `credential.protocol` | Protocol the credential was built for |
| `credential.expires` | When the credential expires |


## Fulfillment

After payment, you must claim what you paid for. The pay engine does NOT do this for you — every merchant may implement fulfillment differently.

The `credential` object in the pay response contains settlement evidence formatted for the detected protocol. Read the merchant's original 402 challenge to understand how they expect payment proof. The credential is your starting point — adapt it to what the merchant specified.

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Invalid request (missing fields) |
| 403 | Insufficient balance or card inactive |
| 410 | Endpoint removed or resource gone |
| 422 | No payable option offered by merchant |

## Notes

- The engine probes, detects protocol, settles on-chain, and returns settlement evidence
- Fulfillment is the agent's responsibility — read the merchant's challenge to understand their expected format
- `protocol` tells you what was detected (x402, tempo, etc.)
- Settlement happens on the network the merchant's challenge specified
- AP2 uses a separate mandate-based flow — see `references/ap2-pay.md`
