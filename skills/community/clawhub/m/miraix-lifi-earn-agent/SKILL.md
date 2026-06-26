---
name: miraix-lifi-earn-agent
description: Use this skill when the user wants to discover the best USDC vaults with LI.FI Earn, ask an agent to choose a safe vault on Base/Arbitrum/Ethereum, prepare a Composer-compatible deposit, execute the deposit with an Agentic Wallet, and explain which receipt token was received after deposit.
---

# Miraix LI.FI Earn Agent

Use this skill for Miraix AI yield actions powered by `LI.FI Earn` and `Composer` when the user wants an agent to move from intent to deposit.

Relevant product surfaces:

- Earn discovery API: `POST /api/earn/chat`
- Composer quote API: `POST /api/earn/quote`
- Miraix UI: `LI.FI Earn -> USDC Vault Discovery -> Composer Deposit Flow`

## When to use it

- The user says things like:
  - `Put 1 USDC into the safest vault on Base`
  - `Find the best USDC vault on Arbitrum`
  - `Deposit 5 USDC into the best LI.FI Earn vault`
  - `Use Agentic Wallet to deposit into a vault`
- The user wants an agent to recommend a vault and prepare a deposit instead of manually comparing vault cards.
- The user wants to know where deposited funds went and which receipt token they now hold.

## Workflow

1. Extract:
   - amount in `USDC` if provided
   - preferred chain (`Base`, `Arbitrum`, `Ethereum`) if provided
   - risk mode if provided (`safe`, `balanced`, `degen`)
2. Call the Miraix Earn discovery endpoint:

```bash
curl -sS -X POST https://app.miraix.fun/api/earn/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Put 1 USDC into the safest vault on Base"}'
```

3. Base the answer on the returned JSON. The most important fields are:
   - `message`
   - `thoughts`
   - `data.filters`
   - `data.action.mode`
   - `data.action.summary`
   - `data.action.rationale`
   - `data.action.selectedVaultId`
   - `quote.vaults`

4. Treat the first recommended vault as the default execution target unless the user asks to compare options first.

5. If the user wants to execute now, prepare the Composer deposit quote:

```bash
curl -sS -X POST https://app.miraix.fun/api/earn/quote \
  -H 'Content-Type: application/json' \
  -d '{
    "chainId":8453,
    "vaultAddress":"<vault-address>",
    "walletAddress":"<wallet-address>",
    "fromAmount":"1000000",
    "fromTokenAddress":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  }'
```

6. For execution:
   - Prefer an embedded or Agentic Wallet connected in Miraix.
   - Execute approval first if `estimate.approvalAddress` is present and allowance is insufficient.
   - Execute the Composer deposit transaction.

7. After a successful deposit, explain:
   - which vault received the funds
   - which chain the funds were deposited on
   - which receipt token or position token was received
   - that the receipt token remains in the same wallet

## Output guidance

- Keep the answer action-oriented.
- When recommending a vault, include:
  - vault name
  - chain
  - protocol
  - APY
  - why it was selected
- When deposit execution succeeds, use plain language:
  - `Deposited 1 USDC into Spark USDC Vault on Base. Expected receipt: sparkUSDC in the same wallet.`
- Explain receipt tokens in simple language:
  - `sparkUSDC is the vault receipt token that represents the deposited position.`
- If live discovery falls back to seeded vaults, say that clearly instead of pretending the list is live.
- If gas is insufficient, say that the wallet needs more native gas token on the target chain before the deposit can proceed.
