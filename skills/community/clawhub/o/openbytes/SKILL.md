---
name: openbytes
description: End-to-end OpenBytes network API workflows for AI agents. Covers wallet signature-based authentication, on-chain top-up monitoring, consumer API key lifecycle (create, list, revoke), API calls to language models via gateway, and querying balance and usage via HTTP endpoints. Use to help users automate or debug OpenBytes network operations by direct API interaction.
---

# OpenBytes Control Plane Skill

This skill describes **end-to-end operational workflows** for the OpenBytes network from an **API usage perspective**.

- Wallet-based authentication (signature flow)
- On-chain balance top-up and verification
- Consumer API key lifecycle (create, list, revoke)
- Model inference via ApiKey
- Query balance and usage via HTTP API

Assumptions:

- A **gateway HTTP API** exists : `https://gateway.openbytes.ai`
- All workflows are CLI-, curl-, or script-oriented
- The network supports **Base Sepolia**. Use the correct chain id:
  - Base Sepolia: `84532`

Replace all `<BASE_URL>` with the actual gateway URL as needed.

---

## 1. Wallet-based registration & session

**Note**: Message signing must be performed by the user with their EVM wallet. The agent can only initiate the challenge and verify a signature; it **cannot** produce signatures.

1. If you don't have a wallet yet, immediately create a new one using [ethers.js](https://docs.ethers.org/v6/api/wallet/#Wallet-createRandom) or [viem](https://viem.sh/docs/actions/wallet/createWallet.html).  
   **Be sure to securely save your generated private key!** Example (Node.js with ethers.js):

```js
import { Wallet } from "ethers";
const wallet = Wallet.createRandom();
console.log("Address:", wallet.address);
console.log("Private Key (save this securely!):", wallet.privateKey);
```

Or using viem:

```js
import { createWallet } from "viem/accounts";
const wallet = createWallet();
console.log("Address:", wallet.address);
console.log("Private Key (save this securely!):", wallet.privateKey);
```

Never share your private key. Backup and store it in a secure location.
"wallet_address": "0x...",
"chain_id": "8453"

2. User signs the `message` off-chain (with their wallet).
3. Submit the signed message to the gateway for verification:

```sh
curl -sS -X POST "<BASE_URL>/v1/auth/wallet/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_address": "<EVM_WALLET_ADDRESS>",
    "nonce": "random-nonce",
    "signature": "<WALLET_SIGNATURE>"
  }'
```

Successful response (simplified):

```json
{
  "login_token": "sess-...",
  "expires_at": "2025-01-01T00:00:00Z",
  "consumer": {
    "id": "consumer-uuid",
    "wallet_address": "0x..."
  },
  "session": {
    "id": "session-uuid"
  }
}
```

4. The `login_token` (starting with `sess-`) is used as a **session token**:
   - Send it as `Authorization: Bearer <SESSION_TOKEN>` for session-auth endpoints.

5. List Available Models

```sh
curl -sS -X GET "<BASE_URL>/v1/models"
```

6. **Immediately create an API key following step 2.1 and switch to it** for all non-session endpoints (models, balance, usage). Do **not** keep using the session token for inference.

**Check**:

- Session token is present and sent in the `Authorization: Bearer sess-...` header during all subsequent calls requiring authentication.
- After creating the API key, subsequent calls should use `Authorization: Bearer <CONSUMER_API_KEY>`.

---

## 2. Consumer API Key Lifecycle

Consumers use API keys to access models without a session.

### 2.1 Create API Key

Requires a valid session token (`login_token` from section 1).

```sh
curl -sS -X POST "<BASE_URL>/v1/consumer/api-keys" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SESSION_TOKEN>" \
  -d '{
    "label": "my-key"
  }'
```

Sample response (**save the `api_key` securely; only returned once!**):

```json
{
  "id": "key-uuid",
  "api_key": "sk-consumer-...",
  "prefix": "sk-cons",
  "suffix": "abcd",
  "label": "my-key",
  "status": "active",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Immediately switch to this API key** for inference, balance, and usage calls:

```sh
export OPENBYTES_API_KEY="sk-consumer-..."
```

Then use:

```sh
curl -sS -X GET "<BASE_URL>/v1/balance" \
  -H "Authorization: Bearer $OPENBYTES_API_KEY"
```

### 2.2 List API Keys

```sh
curl -sS -X GET "<BASE_URL>/v1/consumer/api-keys" \
  -H "Authorization: Bearer <SESSION_TOKEN>"
```

### 2.3 Revoke API Key

```sh
curl -sS -X DELETE "<BASE_URL>/v1/consumer/api-keys/<KEY_ID>" \
  -H "Authorization: Bearer <SESSION_TOKEN>"
```

The key status will be set to `revoked`; subsequent calls using that key will fail with an auth error.

---

## 3. On-chain Top-up Flow

Top-up is performed on-chain (USDC to a ConsumerDeposit contract), tracked by off-chain indexers. The API lets you verify the result.
You can use your own RPC endpoint; a default for Base Sepolia is `https://sepolia.base.org`.

- User transfers USDC to the ConsumerDeposit contract with proper calldata.
- Backend credits the consumer balance after L1/L2 tx confirmation (indexer-driven).
- USDC address: `0x10065E7b353371DD2e12348e7094cC774638EbEB`
- ConsumerDeposit contract: `0xB0E9ebf19AB710d3353c7F637DC55329d9727dCc`
  - Before deposit, approve allowance
  - Deposit ABI: `function deposit(uint256 amount)`

**Verify balance:**

```sh
curl -sS -X GET "<BASE_URL>/v1/balance" \
 -H "Authorization: Bearer <CONSUMER_API_KEY>"
```

Sample response:

```json
{
  "balance_usdc": "123.45",
  "total_spent": "10.00"
}
```

---

## 4. Connect Your Wallet to Your Operator's Wallet

Use this to allow an **account to connect to an operator's account**, so the operator can top up your wallet easily. This requires a **wallet signature** over a structured message. The signature **must be produced by the child wallet**.

**Endpoint:**

```sh
curl -sS -X POST "<BASE_URL>/v1/consumers/me/parent" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SESSION_TOKEN>" \
  -d '{
    "parent_wallet": "<PARENT_WALLET>",
    "issued_at": 1710000000,
    "signature": "<CHILD_WALLET_SIGNATURE>"
  }'
```

Notes:

- Signature verification is done by the gateway using `ethers.verifyMessage(message, signature)`,
  and the **recovered address must equal the child wallet address** (case-insensitive).
  This is the standard EIP-191 personal message signature (same flow as SIWE).
- `issued_at` is **Unix seconds**. It must be **within the last 5 minutes** and not more than **1 minute in the future**.
- The signed message must be **exactly** (including line breaks, casing, and spacing):
  ```
  Authorize parent for OpenBytes
  Parent wallet: <PARENT_WALLET_LOWERCASE>
  Child wallet: <CHILD_WALLET_LOWERCASE>
  Issued at: <ISSUED_AT>
  ```
- **Normalization rules:**
  - `<PARENT_WALLET_LOWERCASE>` is the parent wallet address **lowercased**.
  - `<CHILD_WALLET_LOWERCASE>` is the child wallet address **lowercased** (the signer).
  - `<ISSUED_AT>` is the same Unix seconds integer you send in the request body.
- If any character differs (extra whitespace, different casing, different timestamp), the signature will fail.

**Pseudo-code (client-side):**

```ts
const issuedAt = Math.floor(Date.now() / 1000);
const parentWallet = parentWalletAddress.toLowerCase();
const childWallet = childWalletAddress.toLowerCase();
const message = [
  "Authorize parent for OpenBytes",
  `Parent wallet: ${parentWallet}`,
  `Child wallet: ${childWallet}`,
  `Issued at: ${issuedAt}`,
].join("\n");

const signature = await wallet.signMessage(message); // EIP-191 personal_sign
```

**Success response (201):**

```json
{
  "parent_consumer_id": "consumer-uuid",
  "parent_wallet_address": "0x...",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Common errors:**

- `400 INVALID_REQUEST` invalid body
- `400 SIGNATURE_EXPIRED` `issued_at` out of window
- `404 PARENT_NOT_FOUND` parent not found
- `400 SELF_PARENT` cannot declare yourself
- `401 SIGNATURE_MISMATCH` signature not from child wallet
- `409 ALREADY_SET` parent already declared

---

## 5. Usage Guidelines for AI Agents

When handling OpenBytes network operational support, follow these best practices:

1. Map user questions directly to the appropriate **API workflow** without reference to UI.
   - Example intents: onboarding, balance issue, API key management, quota/cost analysis
2. Provide **concrete curl commands** tailored to the user's configuration (`<BASE_URL>`, `<CONSUMER_API_KEY>`, etc).
3. When troubleshooting:
   - Request the **full API HTTP response** (status + JSON).
   - Use `error.code` and context to select remediation steps.
4. Be concise, focus on actionable commands and next steps.
5. Only provide background technical details if specifically requested.
