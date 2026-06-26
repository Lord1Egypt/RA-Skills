---
name: ripley-pocket
description: "API client skill for Ripley Pocket — the M2M micro-payment gateway for AI agents. Use this skill whenever you need to: send or receive payments between AI agents, check an agent's XMR balance, withdraw Monero to an external address, swap XMR cross-chain to BTC/ETH/USDT/LTC, deposit BTC/ETH/USDT/LTC and auto-convert to XMR balance, register a new agent account, or view transaction history. Triggers on any mention of Ripley Pocket, agent payments, XMR/Monero payments, micro-payments between agents, POST /pay, X-API-KEY, deposit swap, fund account with BTC/ETH, or the XMR402 payment protocol. Also use when the user wants to integrate an AI agent with a payment system, fund an agent wallet with non-XMR crypto, or asks about paying for API calls with crypto."
requiredEnv:
  - API_KEY
primaryEnv: API_KEY
defaultEnv:
  RIPLEY_URL: "https://pocket.ripley.run"
---

# Ripley Pocket — Agent Payment API

Ripley Pocket gives AI agents custodial XMR wallets on the edge. One REST API, four capabilities: instant agent-to-agent transfers (zero fees), external Monero withdrawals, cross-chain swaps to BTC/ETH/USDT/LTC, and **deposit via any supported crypto** (auto-converts to XMR balance).

## Configuration

Before making any calls, you need two things:

| Variable | Description | Example |
|----------|-------------|---------|
| `RIPLEY_URL` | Base URL of the gateway | `https://pocket.ripley.run` or `http://localhost:8787` |
| `API_KEY` | Agent's API key (issued at registration or by admin) | `rp-live-abc123xyz` |

All agent endpoints authenticate via the `X-API-KEY` header. Alternatively, use `Authorization: Bearer <key>`.

## Quick Reference

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| `POST` | `/register` | None | Self-register a new agent |
| `GET` | `/balance` | API key | Check XMR balance |
| `GET` | `/history` | API key | Transaction history |
| `POST` | `/pay` | API key | Send payment (3 modes) |
| `GET` | `/swaps` | API key | List cross-chain swaps |
| `POST` | `/deposit/swap` | API key | Deposit via BTC/ETH/USDT/LTC → auto XMR |
| `GET` | `/deposit/swaps` | API key | List deposit swap history |
| `POST` | `/xmr402/pay` | API key | Pay an XMR402 challenge (returns txid + proof) |
| `POST` | `/xmr402/proof` | API key | Recover TX proof if initial generation failed |

## 1. Register a New Agent

No authentication required. Returns an API key and deposit address. The account is inactive until a minimum deposit of 0.01 XMR arrives.

```bash
curl -X POST $RIPLEY_URL/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent"}'
```

Response:
```json
{
  "agent_id": "agent-a1b2c3d4",
  "api_key": "rp-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "deposit_address": "4AdUndXHHZ...",
  "status": "pending_deposit",
  "min_deposit": 0.01,
  "message": "Send at least 0.01 XMR to your deposit address to activate."
}
```

Save the `api_key` — it is shown only once. The account activates automatically when XMR arrives at the `deposit_address`.

Rate limit: 3 registrations per IP per hour.

## 2. Check Balance

```bash
curl $RIPLEY_URL/balance -H "X-API-KEY: $API_KEY"
```

Response:
```json
{"balance": 2.5, "agent_id": "agent-a1b2c3d4"}
```

Always check balance before making a payment to confirm sufficient funds.

## 3. Make a Payment — `POST /pay`

This single endpoint handles three scenarios based on `destination` and `currency`:

### 3a. Internal Transfer (agent-to-agent)

Instant, zero fees. Use when paying another AI agent.

```bash
curl -X POST $RIPLEY_URL/pay \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "agent-other-id",
    "amount": 0.1,
    "memo": "Payment for data analysis"
  }'
```

Response:
```json
{
  "status": "paid",
  "amount_deducted": 0.1,
  "remaining_balance": 2.4,
  "message": "Internal transfer complete. 0 network fees."
}
```

The `destination` is the recipient's `agent_id`. If you don't know it, the other agent needs to share it with you.

### 3b. External XMR Withdrawal

Send XMR to any Monero address. The address must start with `4` (main) or `8` (subaddress). Fee: 0.001 XMR.

```bash
curl -X POST $RIPLEY_URL/pay \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "4AdUndXHHZ6cfufTMvppY6JwXNouMBzSkbLYfpAV5Usx...",
    "amount": 1.0
  }'
```

Response:
```json
{
  "status": "processing",
  "amount_deducted": 1.001,
  "fee": 0.001,
  "remaining_balance": 1.499,
  "message": "Withdrawal queued. Will be broadcasted to Monero network shortly."
}
```

The balance is deducted immediately (amount + fee). The actual broadcast is async.

### 3c. Cross-Chain Swap

Pay in BTC, ETH, USDT, LTC, or other supported currencies. Set `currency` to the target coin.

```bash
curl -X POST $RIPLEY_URL/pay \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "amount": 0.001,
    "currency": "btc",
    "network": "Mainnet"
  }'
```

Response:
```json
{
  "status": "swap_processing",
  "message": "Deducted 0.158432 XMR. Delivering 0.001 BTC to destination.",
  "trade_id": "abc123",
  "xmr_deducted": 0.158432,
  "eta_minutes": 10,
  "tracking_url": "https://api.kyc.rip/v2/exchange/status/abc123"
}
```

The `amount` is the amount of the **target currency** you want to deliver — not XMR. The system calculates the XMR cost automatically (exchange rate + 0.5% gateway fee). If there aren't enough funds, you get a 402 with the `required_xmr` field.

Supported networks: `ethereum`/`erc20`, `trc20`/`tron`, `bsc`/`bep20`, `solana`, `polygon`, `arbitrum`, `base`, `lightning`, `ton`, and more. Network names are case-insensitive and aliased automatically.

## 4. Deposit via Swap — `POST /deposit/swap`

**This is the easiest way to fund an agent account if you don't have XMR.** Send BTC, ETH, USDT, LTC, or any supported currency — it's automatically converted to XMR and credited to your balance.

```bash
curl -X POST $RIPLEY_URL/deposit/swap \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "currency": "btc",
    "amount": 0.001,
    "network": "Mainnet"
  }'
```

Response:
```json
{
  "status": "awaiting_deposit",
  "message": "Send exactly 0.001 BTC to the address below. ~0.156700 XMR will be credited to your balance.",
  "trade_id": "xyz789",
  "deposit_address": "bc1q...",
  "send_amount": 0.001,
  "send_currency": "BTC",
  "xmr_expected": 0.1567,
  "eta_minutes": 15,
  "tracking_url": "https://api.kyc.rip/v2/exchange/status/xyz789"
}
```

**Flow:**
1. Call `POST /deposit/swap` with how much BTC/ETH you want to send
2. Send that exact amount to the `deposit_address` returned
3. The swap provider converts it to XMR
4. XMR is automatically credited to your Ripley Pocket balance
5. Poll `GET /deposit/swaps` or `GET /balance` to confirm arrival

The `amount` is how much of the **source currency** you're sending (not XMR). A 0.5% gateway fee is deducted from the XMR received.

### View Deposit Swap History

```bash
curl $RIPLEY_URL/deposit/swaps -H "X-API-KEY: $API_KEY"
```

Returns all deposit swaps with status: `awaiting_deposit` → `processing` → `completed`.

## 5. View Transaction History

```bash
curl "$RIPLEY_URL/history?limit=20&offset=0" \
  -H "X-API-KEY: $API_KEY"
```

Response:
```json
{
  "transactions": [
    {
      "id": 1,
      "type": "deposit",
      "amount": 2.5,
      "fee": 0,
      "status": "success",
      "memo": "XMR deposit",
      "created_at": "2026-03-17 12:00:00"
    }
  ],
  "agent_id": "agent-a1b2c3d4"
}
```

Transaction types: `deposit`, `internal_send`, `internal_recv`, `withdraw`, `swap_debit`.

## 6. View Swap Trades

```bash
curl $RIPLEY_URL/swaps -H "X-API-KEY: $API_KEY"
```

Returns all cross-chain swap trades with their current status.

## Fees

| Operation | Fee |
|-----------|-----|
| Internal transfer | **0** |
| XMR withdrawal | **0.001 XMR** (fixed) |
| XMR402 payment | **0.001 XMR** (fixed, same as withdrawal) |
| Cross-chain swap (out) | **0.5%** gateway fee + exchange spread |
| Deposit swap (in) | **0.5%** gateway fee (deducted from XMR received) |

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 206 | Payment sent, proof generation failed | Use `POST /xmr402/proof` to recover the proof |
| 400 | Bad request (missing/invalid fields) | Fix request body |
| 401 | Missing API key | Add `X-API-KEY` header |
| 402 | Insufficient funds | Check balance, reduce amount |
| 403 | Invalid key or inactive account | Verify key, or use `/deposit/swap` to fund and auto-activate |
| 429 | Rate limited | Wait and retry (max 20 mutations/min, 60 reads/min) |
| 503 | Swap/proof service unavailable | Retry after a delay |

On a 402 for swaps, the response includes `required_xmr` — the exact XMR amount needed.
On a 206 for XMR402, the `txid` from the response is needed for proof recovery — save it.

## XMR402 Protocol Integration

[XMR402](https://xmr402.org) is the stateless payment protocol for the machine economy. When a service returns `HTTP 402 Payment Required`, it includes a cryptographic challenge. Ripley Pocket acts as the **Gateway** — it handles the XMR transfer and TX proof generation so your agent doesn't need its own Monero wallet.

### How XMR402 works

1. Agent hits a protected endpoint → gets `HTTP 402` with:
   ```
   WWW-Authenticate: XMR402 address="4AdUnd...", amount="100000000", message="hmac_nonce...", timestamp="1710000000"
   ```
   - `address` — Monero subaddress to pay (piconero amount in `amount`)
   - `message` — HMAC nonce binding this payment to the specific request payload (intent binding)

2. Agent pays via Ripley Pocket → `POST /xmr402/pay`

3. Agent retries the original request with:
   ```
   Authorization: XMR402 txid="abc123...", proof="InProofV1..."
   ```

### `POST /xmr402/pay`

Synchronous endpoint — broadcasts the XMR transfer and returns the TX proof in one shot (~1-2 seconds).

```bash
curl -X POST $RIPLEY_URL/xmr402/pay \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "4AdUndXHHZ6cfufTMvppY6JwXNouMBzSkbLYfpAV5Usx...",
    "amount": 0.0001,
    "message": "hmac_nonce_from_www_authenticate_header"
  }'
```

Response:
```json
{
  "status": "paid",
  "txid": "7c1e2a3b4d...",
  "proof": "InProofV1TFh...",
  "amount_paid": 0.0001,
  "fee": 0.001,
  "authorization": "XMR402 txid=\"7c1e2a3b4d...\", proof=\"InProofV1TFh...\""
}
```

The `authorization` field is the exact header value to use when retrying the 402'd request. Copy it directly into the `Authorization` header.

**If proof generation fails** (status `206`, `"status": "paid_no_proof"`), the payment was sent on-chain but the cryptographic proof couldn't be generated immediately (usually because the TX is still propagating). Use the recovery endpoint:

### `POST /xmr402/proof` — Recover TX Proof

```bash
curl -X POST $RIPLEY_URL/xmr402/proof \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "txid": "a567e82af696...",
    "address": "8AdUndXHHZ6...",
    "message": "hmac_nonce_from_original_request"
  }'
```

Response:
```json
{
  "status": "proof_recovered",
  "txid": "a567e82af696...",
  "proof": "InProofV2...",
  "authorization": "XMR402 txid=\"a567e82af696...\", proof=\"InProofV2...\""
}
```

Use the same `txid`, `address`, and `message` from the original `/xmr402/pay` request. If the TX is still propagating, wait a few minutes and retry. The endpoint retries automatically up to 3 times with backoff.

**Key differences from `POST /pay`:**
- **Synchronous** — blocks until TX is broadcast and proof is generated (not queued)
- **Returns TX proof** — the cryptographic evidence the server needs to verify payment
- **Intent-bound** — the `message` (HMAC nonce) binds this payment to the specific request, preventing replay attacks
- **Recoverable** — if proof fails, use `/xmr402/proof` to retry without paying again

## Code Examples

### Python (httpx)

```python
import httpx

RIPLEY_URL = "https://pocket.ripley.run"
headers = {"X-API-KEY": "rp-live-your-key-here", "Content-Type": "application/json"}

# Check balance
bal = httpx.get(f"{RIPLEY_URL}/balance", headers=headers).json()
print(f"Balance: {bal['balance']} XMR")

# Pay another agent
resp = httpx.post(f"{RIPLEY_URL}/pay", headers=headers, json={
    "destination": "agent-other",
    "amount": 0.05,
    "memo": "Payment for API call"
}).json()

# Cross-chain: deliver BTC
resp = httpx.post(f"{RIPLEY_URL}/pay", headers=headers, json={
    "destination": "bc1q...",
    "amount": 0.001,
    "currency": "btc"
}).json()
print(f"Track: {resp.get('tracking_url')}")

# Fund account with BTC (deposit swap)
resp = httpx.post(f"{RIPLEY_URL}/deposit/swap", headers=headers, json={
    "currency": "btc",
    "amount": 0.001
}).json()
print(f"Send {resp['send_amount']} {resp['send_currency']} to {resp['deposit_address']}")
print(f"Expected: ~{resp['xmr_expected']} XMR")
```

### TypeScript (fetch)

```typescript
const RIPLEY_URL = "https://pocket.ripley.run";
const headers = { "X-API-KEY": "rp-live-your-key-here", "Content-Type": "application/json" };

// Check balance
const bal = await fetch(`${RIPLEY_URL}/balance`, { headers }).then(r => r.json());

// Internal transfer
const payment = await fetch(`${RIPLEY_URL}/pay`, {
  method: "POST",
  headers,
  body: JSON.stringify({ destination: "agent-other", amount: 0.05 }),
}).then(r => r.json());

// Fund account with ETH
const deposit = await fetch(`${RIPLEY_URL}/deposit/swap`, {
  method: "POST",
  headers,
  body: JSON.stringify({ currency: "eth", amount: 0.01 }),
}).then(r => r.json());
// → Send deposit.send_amount ETH to deposit.deposit_address
```

### Handling XMR402 automatically

```python
import re

def parse_xmr402_challenge(www_auth: str) -> dict:
    """Parse WWW-Authenticate: XMR402 address="...", amount="...", message="...", timestamp="..." """
    return dict(re.findall(r'(\w+)="([^"]*)"', www_auth))

def call_with_xmr402(url: str, method: str = "GET", headers: dict = {}, **kwargs) -> httpx.Response:
    """Hit a URL; if it returns 402 with XMR402 challenge, pay via Ripley Pocket and retry."""
    resp = httpx.request(method, url, headers=headers, **kwargs)

    if resp.status_code != 402:
        return resp

    www_auth = resp.headers.get("WWW-Authenticate", "")
    if not www_auth.startswith("XMR402"):
        return resp  # Not an XMR402 challenge

    # Parse the challenge
    challenge = parse_xmr402_challenge(www_auth)
    address = challenge["address"]
    amount = int(challenge["amount"]) / 1e12  # piconeros → XMR
    message = challenge["message"]

    # Pay via Ripley Pocket (synchronous — returns txid + proof)
    pay_resp = httpx.post(f"{RIPLEY_URL}/xmr402/pay", headers=PAY_HEADERS, json={
        "address": address,
        "amount": amount,
        "message": message,
    }).json()

    if pay_resp.get("status") == "paid_no_proof":
        # Payment sent but proof failed — recover it
        import time
        time.sleep(5)  # Wait for TX propagation
        proof_resp = httpx.post(f"{RIPLEY_URL}/xmr402/proof", headers=PAY_HEADERS, json={
            "txid": pay_resp["txid"],
            "address": address,
            "message": message,
        }).json()
        if proof_resp.get("status") != "proof_recovered":
            raise Exception(f"Proof recovery failed: {proof_resp}")
        pay_resp = proof_resp  # Use recovered proof

    elif pay_resp.get("status") != "paid":
        raise Exception(f"XMR402 payment failed: {pay_resp}")

    # Retry with the cryptographic proof
    retry_headers = {**headers, "Authorization": pay_resp["authorization"]}
    return httpx.request(method, url, headers=retry_headers, **kwargs)
```
