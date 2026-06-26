# GiftDrop Skill

Send and claim crypto red packets on Solana via the GiftDrop API. Humans and AI Agents are equal participants — wallets don't care who holds the private key.

## Prerequisites

- A Solana wallet keypair (for signing transactions and API key registration)
- An API key from GiftDrop (register via wallet signature)

## API Base URL

```
https://giftdrop.fun/api/v1
```

## Authentication

All requests require an `X-API-Key` header:
```
X-API-Key: gd_<your_key>
```

Key format: `gd_` + 32 hex chars (35 chars total).

### Register an API Key

Sign a message with your Solana wallet to get an API key. The message must:
- Contain "GiftDrop API Key"
- Contain an ISO timestamp within 5 minutes of current time
- Each signature can only be used once

```bash
MESSAGE="GiftDrop API Key request at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

curl -X POST https://giftdrop.fun/api/v1/keys \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "<WALLET_ADDRESS>",
    "signature": "<BASE64_ED25519_SIGNATURE_OF_MESSAGE>",
    "message": "'"$MESSAGE"'"
  }'
# Response: { "success": true, "apiKey": "gd_..." }
# Save this key! It won't be shown again.
```

Max 3 keys per wallet. Max 10 registration attempts per IP per hour.

## Commands

### Create a Gift Drop

1. Send SOL/SPL tokens to host wallet: `3sZVJLG64tGyAzfNNau3nks7i44oVR6fAmoAjF5A5b7N`
   - For SPL tokens, also send 0.003 SOL × totalClaims as gas reserve
2. Register the gift drop:

```bash
curl -X POST https://giftdrop.fun/api/v1/gift \
  -H "X-API-Key: gd_..." \
  -H "Content-Type: application/json" \
  -d '{
    "fundingTx": "<SOLANA_TX_SIGNATURE>",
    "totalAmount": 1.0,
    "totalClaims": 10,
    "tokenSymbol": "SOL",
    "tokenMint": "So11111111111111111111111111111111111111112",
    "decimals": 9,
    "title": "Happy Birthday!",
    "luckyBonusPercent": 30,
    "expiryDays": 7
  }'
# Response: { "success": true, "id": "gift_...", "url": "https://giftdrop.fun/g/gift_..." }
```

Each funding transaction can only be used once.

**Parameters:**
| Field | Required | Type | Description |
|-------|----------|------|-------------|
| fundingTx | ✅ | string | Solana tx signature (base58, 64-128 chars) |
| totalAmount | ✅ | number | Total token amount (positive finite) |
| totalClaims | ✅ | integer | Number of claims (3-100) |
| tokenSymbol | ✅ | string | Token symbol, max 10 chars |
| tokenMint | ✅ | string | SPL token mint address (base58) |
| decimals | | integer | Token decimals, 0-18 (default: 9) |
| title | | string | Optional title, max 40 chars |
| password | | string | Password protection, 4-20 chars |
| passwordHint | | string | Hint for password, max 50 chars |
| luckyBonusPercent | | integer | Lucky bonus: 0, 30, 50, 70, or 100 (default: 30) |
| expiryDays | | integer | Expiry: 1, 3, 7, or 30 (default: 7) |

### Claim a Gift Drop

```bash
curl -X POST https://giftdrop.fun/api/v1/gift/<GIFT_ID>/claim \
  -H "X-API-Key: gd_..." \
  -H "Content-Type: application/json" \
  -d '{"password": "optional_if_protected"}'
# Response: { "success": true, "amount": 0.15, "isLucky": false, "signature": "..." }
```

Uses the wallet associated with your API key as the claimant.

### Check Gift Drop Status

```bash
curl https://giftdrop.fun/api/v1/gift/<GIFT_ID> \
  -H "X-API-Key: gd_..."
# Response: { "success": true, "gift": { "totalAmount": 1.0, "claimed": 3, "remaining": 7, ... } }
```

### List My Gift Drops

```bash
curl https://giftdrop.fun/api/v1/gifts \
  -H "X-API-Key: gd_..."
# Response: { "success": true, "gifts": [...] }
```

## Rate Limits

| Action | Limit |
|--------|-------|
| Key registration | 10/hr per IP, 3 keys per wallet |
| Gift creation | 5/hr per wallet |
| Claims | 10/min per wallet |
| General API | 60/min per key |

## Fees

- 1% platform fee (deducted from total amount)
- SPL tokens: 0.003 SOL × totalClaims as gas reserve

## Token Limits

| Token | Max per drop |
|-------|-------------|
| SOL | 10 |
| USDC | 1,000 |
| USDT | 1,000 |
| Others | No limit |

## Error Codes

| Status | Meaning |
|--------|---------|
| 400 | Validation error |
| 401 | Invalid or missing API key |
| 404 | Gift drop not found |
| 409 | Duplicate (tx already used, gift already exists) |
| 410 | Expired or sold out |
| 429 | Rate limit exceeded |
| 503 | Service unavailable |

## Example: Full Agent Workflow (Python)

```python
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.system_program import transfer, TransferParams
from solders.hash import Hash
import requests, json, base64, time, struct

API = "https://giftdrop.fun/api/v1"
HOST = Pubkey.from_string("3sZVJLG64tGyAzfNNau3nks7i44oVR6fAmoAjF5A5b7N")
SOL_MINT = "So11111111111111111111111111111111111111112"
RPC = "https://api.mainnet-beta.solana.com"

# Load your keypair
kp = Keypair()  # or Keypair.from_base58_string("your_private_key")

# Step 1: Register API Key
msg = f"GiftDrop API Key request at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"
sig = kp.sign_message(msg.encode())
r = requests.post(f"{API}/keys", json={
    "wallet": str(kp.pubkey()),
    "signature": base64.b64encode(bytes(sig)).decode(),
    "message": msg,
})
api_key = r.json()["apiKey"]
headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

# Step 2: Send SOL to host wallet
bh_resp = requests.post(RPC, json={"jsonrpc":"2.0","id":1,"method":"getLatestBlockhash","params":[{"commitment":"finalized"}]})
blockhash = Hash.from_string(bh_resp.json()["result"]["value"]["blockhash"])
ix = transfer(TransferParams(from_pubkey=kp.pubkey(), to_pubkey=HOST, lamports=500_000_000))  # 0.5 SOL
msg = MessageV0.try_compile(kp.pubkey(), [ix], [], blockhash)
tx = VersionedTransaction(msg, [kp])
tx_resp = requests.post(RPC, json={"jsonrpc":"2.0","id":1,"method":"sendTransaction","params":[base64.b64encode(bytes(tx)).decode(),{"encoding":"base64"}]})
funding_tx = tx_resp.json()["result"]
time.sleep(15)  # wait for confirmation

# Step 3: Create gift drop
r = requests.post(f"{API}/gift", headers=headers, json={
    "fundingTx": funding_tx,
    "totalAmount": 0.5,
    "totalClaims": 10,
    "tokenSymbol": "SOL",
    "tokenMint": SOL_MINT,
    "title": "Agent Gift 🤖",
})
gift = r.json()
print(f"Gift URL: {gift['url']}")

# Step 4: Check status
r = requests.get(f"{API}/gift/{gift['id']}", headers=headers)
print(r.json())

# Step 5: Claim (with a different wallet/key)
r = requests.post(f"{API}/gift/{gift['id']}/claim", headers=headers)
print(r.json())
```
