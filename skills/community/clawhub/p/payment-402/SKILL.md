---
name: payment-402
description: Access protected APIs and digital resources via the x402 "Payment Required" protocol on Base L2. This skill automates cryptographic handshakes and USDC micro-payments to unlock restricted content. Built for "Pay-per-Resource" agentic billing.
license: MIT
compatibility: Requires Bun (v1.0+).
required_env_vars:
  - CLIENT_PRIVATE_KEY
required_binaries:
  - bun
primary_credential: CLIENT_PRIVATE_KEY
install: bun install
---

# 💳 PayNode 402 Protocol Skill (Base & Bun)

Use this skill to automate **Resource-based Billing**. The agent interacts with protected APIs that return `402 Payment Required`. Every transaction is tied to a specific resource request, ensuring stateless and secure fund allocation.

## 🚀 Pre-execution Readiness

Before any request, verify the environment and balances:

1.  **Initialize Dependencies**: Run `bun install` once within this directory.
2.  **Verify Environment**: Ensure a `.env` file is created in the root directory. The agent **MUST** verify the existence and exact format of this variable before proceeding:
    ```env
    # [REQUIRED] PayNode Burner Wallet Private Key
    # Format: 66-character hex string MUST start with '0x'
    CLIENT_PRIVATE_KEY=0xYourBurnerWalletPrivateKeyHere...
    ```
3.  **Check Balances**: Run `bun run check-wallet --json --network <NETWORK>`.
4.  **Validate Readiness**: Ensure `checks.can_pay` is `true`.

### Expected `check-wallet` Output:

```json
{
  "status": "success",
  "address": "0x...",
  "eth": 0.01,
  "usdc": 100.0,
  "checks": {
    "gas_ready": true, // Has > 0.001 ETH for gas
    "tokens_ready": true, // Has USDC for payments
    "can_pay": true // Ready for x402 flow
  }
}
```

## 🛠️ x402 Execution Workflow

Follow this sequence to unlock protected resources.

### Step 1: Identify Resource
Determine the URL of the protected API you need to access.

### Step 2: Request & Handle Challenge
Run `bun run request "<URL>" --json --network <NETWORK>`.

- **Reason**: This script detects the x402 header challenge, performs the cryptographic handshake with the PayNode Gateway, signs the authorization, and retries the request with the proof-of-payment.

### Step 3: Capture Resource
Upon success, capture the JSON response. The `txHash` will be included in the logs if a payment occurred.

---

## 🛡️ Security Rules & Agent Safety

> [!IMPORTANT]
> **ADHERE TO THESE RULES TO PROTECT FUNDS.**

### 💸 Burner Wallet Policy (Minimal Exposure)
The `CLIENT_PRIVATE_KEY` **MUST** belong to a dedicated "burner" wallet acting as petty cash. **NEVER** hold excessive funds. Maintain balances strictly sufficient for immediate tasks (e.g., < 10 USDC). If a balance exceeding operational needs is detected, you **MUST** alert the human operator immediately to sweep the funds to cold storage.

### 🤖 Autonomous Usage & Human Consent
If you are operating autonomously, be aware that this skill can **sign and broadcast blockchain transactions** without manual confirmation.
- **Threshold Limit**: For any single transaction exceeding `2.0 USDC`, you **MUST** request explicit human approval before execution.
- **Merchant Verification**: Before initial payment to a new domain, perform a `read_url_content` check on the merchant's reputation (if possible) or alert the user.

### 🕵️ Zero-Trust Pre-Flight Validation (Resource Consistency)
Prevent "Confused Deputy" attacks. Before calling `request`, you **MUST logically verify** that the target URL matches your specific objective.
- Ask: _Is this resource exactly what I need? Is the cost reasonable for this resource?_
- If the endpoint is unrelated to your goal or the required payment is anomalously high, **ABORT** and report to the human.
- **Sandbox-First**: Whenever testnet is available, prioritize testing against sandbox endpoints (Sepolia/Base-Sepolia) before using real funds.

---

## ⚠️ Gotchas & Troubleshooting

- **Handshake Failures**: If `request` fails with a 402 exit code, the gateway may be down or the merchant's contract is invalid.
- **Private Key Format**: The `CLIENT_PRIVATE_KEY` **MUST** start with `0x`.
- **Gas vs. Tokens**: You can have $1M USDC but if `gas_ready` is `false` (low ETH), the transaction **WILL** fail.
- **Exit Codes**:
  - `2`: Invalid arguments.
  - `3`: Auth Failure (Check `.env` key format).
  - `4`: Network/RPC Failure.
  - `402`: Challenge detected but automated resolution failed.

---

## 🧪 Sandbox & Testing

Always test against sandbox endpoints first.

- **Mint Test Tokens**: `bun run mint-test-tokens --json`
- **Test Merchant (Doodle Wall)**: `https://paynode.dev/api/pom?network=testnet` (**Note**: Use `&network=mainnet` for mainnet Doodle Wall)
- **Reference**: See [Testing Guide](references/TESTING.md) for more details.

---

## 🔗 References

- **Official Docs**: [PayNode Documentation](https://github.com/PayNodeLabs/paynode-docs)
- **SDKs**: [Node.js SDK](@paynodelabs/sdk-js)
- **Hub**: [PayNode Hub](https://github.com/PayNodeLabs/paynode-web)
- **Testing**: [Detailed Testing & Examples](references/TESTING.md)
