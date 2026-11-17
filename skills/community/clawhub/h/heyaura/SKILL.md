---
name: heyaura
description: Fetch and summarize a current multichain EVM wallet portfolio through heyAura's paid x402 API, including token balances, USD values, networks, and DeFi positions. Use when a user asks to inspect a wallet address or ENS name, list its crypto holdings, calculate its portfolio value, show balances by chain, or explicitly use the heyAura portfolio API or x402 portfolio endpoint. Do not use for portfolio strategies, trade execution, swaps, transfers, or generic market-price research.
metadata:
  openclaw:
    requires:
      bins: [node, npm]
    primaryEnv: HEYAURA_EVM_PRIVATE_KEY
    envVars:
      - name: HEYAURA_EVM_PRIVATE_KEY
        required: false
        description: EVM payer private key, required only for paid requests; unpaid inspection works without it.
---

# heyAura

Fetch and summarize one wallet's portfolio through heyAura's x402 balances endpoint. Inspect the live payment terms and use the authorization rules below before signing.

## Prerequisites

- Require Node.js 20 or newer.
- Install runtime dependencies once with `npm install --omit=dev --ignore-scripts --prefix {baseDir}` if `{baseDir}/node_modules` is absent.
- Read [references/portfolio-api.md](references/portfolio-api.md) before handling the first request in a session.
- Use `HEYAURA_EVM_PRIVATE_KEY` only from the environment of the process running the skill. Never request that the user paste a private key into chat, place it in a command argument, commit it to a file, or print it.

## Update check

Once per session, before first use, read the installed version from `{baseDir}/package.json` and make an HTTP GET request to `https://clawhub.ai/api/v1/skills/heyaura?ownerHandle=heyaura` with a five-second timeout. This public check needs no credentials or ClawHub CLI.

Compare the installed version with `latestVersion.version` only when `owner.handle` is `heyaura`. If a newer stable version exists, mention the installed and available versions alongside the requested result and offer to update through the original installation method. Continue using the installed version unless the user requests an update.

If the check fails or the metadata is missing or invalid, continue the task without claiming the skill is up to date. Do not repeat the check in the same session.

## Fetch workflow

1. Obtain the portfolio address. Never substitute the payer address for the queried address; they may differ.
2. Inspect the live x402 challenge without signing or paying:

   ```bash
   node {baseDir}/scripts/portfolio.mjs inspect --address "<wallet-or-ens>"
   ```

3. If inspection returns `resultFile`, read that saved response and summarize it; no payment is needed.
4. If it returns payment options, check the configured payer:

   ```bash
   node {baseDir}/scripts/portfolio.mjs status
   ```

   It returns `payerConfigured` and the public `payerAddress`. If the payer is missing or invalid, ask the user to configure `HEYAURA_EVM_PRIVATE_KEY` in the agent runtime's environment and stop.
5. Use an existing explicit authorization when it covers this heyAura request, the payer, selected network, asset, payee, and amount within the remaining spending limit. Respect any request or wallet scope and track cumulative spend; count uncertain payments against the budget until resolved. Do not ask again for a request already covered. A configured payer alone is not spending authorization.

   Otherwise, present the query address, payer address, and live payment terms and ask for authorization. If the authorization does not cover which offered network to use, ask the user to choose one.
6. Once authorized, copy the selected live challenge fields exactly into the guarded payment command:

   ```bash
   node {baseDir}/scripts/portfolio.mjs pay \
     --address "<wallet-or-ens>" \
     --network "<network>" \
     --asset "<asset-address>" \
     --amount "<atomic-amount>" \
     --pay-to "<payee-address>" \
     --confirm-payment YES
   ```

   The `pay` command fetches a fresh challenge and pays in one invocation. It rejects any change to the selected network, asset, amount, or payee. `--confirm-payment YES` may be used for either a specifically approved payment or a request covered by an existing explicit spending authorization.

   When the live challenge advertises `payment-identifier`, the command generates one identifier for the logical request and adds it before the x402 library creates the signed payload. It records the identifier and whether it was applied. The command does not retry automatically.

7. When portfolio data is returned, `inspect` and `pay` save the complete response in a temporary JSON file. Standard output contains `status`, `resultFile`, and `resultBytes`; payment results also include receipt details inside the file. Process `resultFile` locally. If a view is too large, query smaller portions of that same file rather than printing the entire response or fetching it again.
8. Summarize the data from `resultFile`:
   - total USD value;
   - totals by network;
   - material token holdings, including units and USD value;
   - DeFi positions grouped by provider and type;
   - cached status and API version when present.

Keep low-value dust concise unless the user asks for every asset. Treat negative borrow positions according to the API payload instead of silently converting them to positive holdings.

## Payment safety

- Use only the balances endpoint documented in [references/portfolio-api.md](references/portfolio-api.md).
- Never loosen the script's exact-match guards or redirect it to another host.
- Allow at most one retry for an unpaid inspection after a transient network error.
- Do not create a fresh payment automatically after a timeout, connection loss, or ambiguous settlement.
- If an ambiguous paid call reports `paymentIdentifierApplied: true`, preserve its `paymentIdentifier`. A later user-authorized retry may pass that same identifier with `--payment-identifier` only for the same address and the exact same confirmed payment terms. Let the x402 library create a fresh signed payload; never replay a previous payment header.
- Do not assume a payment identifier remains valid. Its cache lifetime is controlled by the server and is not advertised by the current challenge; a retry after expiry can settle another payment.
- Never reuse a payment identifier for a different address, route, method, network, asset, amount, or payee.
- If payment succeeds but portfolio retrieval fails, report the payment settlement details and the API failure separately.

## Errors

- `400`: report the API message and ask for a valid EVM address or ENS name.
- `402`: inspect and present the live payment requirement; do not call it an authentication error.
- `409`: report that the payment identifier conflicts with a different request fingerprint and stop.
- `429`: report the rate limit and wait for user direction; do not repay automatically.
- `500`: report the upstream error and stop.
- No exact challenge match during `pay`: stop, inspect again, and check the new terms against the authorization before proceeding.
