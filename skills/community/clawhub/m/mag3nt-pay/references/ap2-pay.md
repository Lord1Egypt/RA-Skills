# AP2 Pay — Google Agentic Payment Protocol v2

AP2 is a **mandate-based** payment protocol designed by Google for agentic commerce. It does NOT use HTTP 402 challenge-response.

## Key Difference

| | x402 / MPP | AP2 |
|---|---|---|
| **Trigger** | HTTP 402 + headers | Merchant checkout flow (no 402) |
| **Model** | Challenge → Pay → Retry | Instruments → Mandate → Receipt |
| **Endpoint** | `POST /api/pay` (universal) | Dedicated `/api/ap2/*` routes |
| **Roles** | Payer + Merchant | Shopping Agent, Credential Provider (Mag3nt), Merchant, MPP, Trusted Surface |

## How AP2 Works

Mag3nt acts as the **Credential Provider (CP)** — it issues payment credentials (SD-JWT mandates) and verifies receipts.

### Flow

1. **List Instruments** — See what payment instruments are available
2. **Merchant Checkout** — The merchant issues a signed Checkout JWT describing the purchase
3. **Issue Mandate** — Agent requests a signed SD-JWT Payment Mandate from Mag3nt
4. **Present to Merchant** — Agent presents the mandate to the merchant's payment processor
5. **Verify Receipt** — Agent submits the Payment Receipt JWT to Mag3nt for verification

## AP2 Endpoints

### List Instruments

```
GET https://mag3nt.com/api/ap2/instruments?card_id=<CARD_ID>&card_token=<CARD_TOKEN>
```

Returns available payment instruments with balance info.

### Issue Payment Mandate

```
POST https://mag3nt.com/api/ap2/mandate
Content-Type: application/json
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_id` | string | yes | Card identifier |
| `card_token` | string | yes | Card secret token |
| `checkout_jwt` | string | yes | Merchant-signed Checkout JWT |
| `amount` | number | yes | Payment amount in USDC |
| `currency` | string | yes | Currency (e.g. `USDC`) |
| `payee.name` | string | yes | Merchant name |
| `payee.website` | string | yes | Merchant website URL |
| `open_mandate` | string | no | Open mandate JWT (for autonomous flow) |

Response includes `mandate` (signed SD-JWT), `mandate_id`, and `expires_at`. Present the mandate to the merchant's payment processor.

### Verify Payment Receipt

```
POST https://mag3nt.com/api/ap2/receipt
Content-Type: application/json
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_id` | string | yes | Card identifier |
| `card_token` | string | yes | Card secret token |
| `payment_receipt` | string | yes | MPP-signed receipt JWT |
| `mandate_id` | string | yes | The mandate ID from the issue step |

### JWKS (Public Key)

```
GET https://mag3nt.com/api/ap2/.well-known/jwks.json
```

Returns the ES256 public key used to verify mandate signatures.

## Autonomous (Human-Not-Present) Flow

AP2 supports pre-authorized spending via **Open Mandates**:

1. Human authorizes an open mandate with a max spending cap and allowed payees
2. Agent derives closed mandates from the open mandate for individual purchases
3. Each closed mandate is chained to the open mandate via `sd_hash`
4. The open mandate's constraints (max amount, allowed payees, expiry) are enforced

### Open Mandate Endpoint

```
POST https://mag3nt.com/api/ap2/open-mandate
Content-Type: application/json
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_id` | string | yes | Card identifier |
| `card_token` | string | yes | Card secret token |
| `max_amount` | number | yes | Maximum total spend allowed |
| `currency` | string | yes | Currency (e.g. `USDC`) |
| `agent_key` | object | yes | Agent's public JWK for mandate derivation |
| `ttl_minutes` | number | yes | How long the open mandate is valid |

To derive a closed mandate from an open mandate, call `POST /api/ap2/mandate` with the `open_mandate` field set to the open mandate JWT.

## Notes

- AP2 uses **SD-JWT VCs** (Selective Disclosure JWT Verifiable Credentials) for mandates
- Mandates are signed with ES256 (P-256) by Mag3nt as the Credential Provider
- The autonomous flow enforces human-set spending limits — the agent cannot exceed the open mandate's `max_amount`
- Receipt verification checks the MPP's signature against their published JWKS
