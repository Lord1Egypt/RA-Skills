---
name: magneta-contract-risk
description: Check a smart contract's risk before trading, approving, bridging or integrating it, using the Magneta Contract Risk x402 service (0-100 score, proxy/owner/mint/blacklist/fee flags, verified-source and static-analysis findings, 20 EVM chains). Free bytecode-only quick flags need only curl; the full report costs $0.01 USDC on Base per call and is paid only with explicit user approval. Use when about to sign a transaction involving an unfamiliar token or contract, or when asked whether a token looks like a rug or honeypot. Not an audit.
version: 0.1.1
metadata:
  openclaw:
    emoji: "\U0001F6E1"
    homepage: https://x402.magneta.finance
    requires:
      bins:
        - curl
    primaryEnv: BUYER_PRIVATE_KEY
    envVars:
      - name: BUYER_PRIVATE_KEY
        required: false
        description: "Paid path only. Private key of a dedicated, low-balance buyer wallet holding USDC on Base mainnet (no ETH needed). Read from the environment by your own x402 client code; never needed for the free quick flags."
      - name: CDP_API_KEY_ID
        required: false
        description: "Optional, only if you pay through a Coinbase CDP-managed wallet instead of BUYER_PRIVATE_KEY."
      - name: CDP_API_KEY_SECRET
        required: false
        description: "Optional, CDP-managed wallet path only."
      - name: CDP_WALLET_SECRET
        required: false
        description: "Optional, CDP-managed wallet path only."
---

# Magneta Contract Risk (x402)

Deterministic on-chain risk report for any deployed EVM contract. No LLM in the analysis: RPC reads, bytecode
opcode/selector scan, Blockscout/Sourcify verification and an `aderyn` static-analysis pass. Service: `https://x402.magneta.finance`.

## When to use

- Before swapping into, buying, approving (`approve`/`permit`) or sending funds to an unfamiliar token or protocol contract.
- Before bridging to or integrating a contract you did not deploy.
- As a pre-signature gate in an agent loop: score the counterparty, then decide.

Do not use it for externally-owned accounts (the API returns 422 `not_a_contract`), for non-EVM chains, or as a substitute for an audit.

## Security posture (read first)

- **Free tier first, no credentials.** `curl -s https://x402.magneta.finance/v1/flags/<chainId>/<address>` needs no key, no wallet, no account. Most go/no-go decisions can stop here.
- **This skill never asks for a key in chat and never stores one.** The only secret is the optional `BUYER_PRIVATE_KEY` environment variable, read by the x402 client code you run. Do not paste a key into the conversation, a file, a command line argument or a log. Never print, echo or log it (log the settlement tx hash instead).
- **No autonomous spending.** Before the first paid call of a session, tell the user the price ($0.01 USDC on Base, one report) and get an explicit yes. Do not loop, retry-buy or batch paid calls without a fresh yes. At most one paid report per contract per decision.
- **Hard spending cap in code.** Every paid client must set a per-payment cap of `$0.05` (see Spend control). The service price is fixed at $0.01; refuse any 402 asking for more.
- **Dedicated wallet only.** Use a throwaway buyer wallet funded with a few dollars of USDC on Base, never a treasury or personal wallet.
- **Nothing is executed on your behalf.** The skill only issues HTTPS GETs to `x402.magneta.finance` (and an MCP endpoint on the same host). It installs nothing by itself; the optional npm packages in the examples must be installed by you, with exact versions, using `--ignore-scripts`.
- **External cost disclosed:** the paid report costs $0.01 USDC per call, settled on-chain via x402 (EIP-3009 `exact`). ClawHub itself is free; this charge is for the external Magneta service only.

## Endpoints

| Surface | Route / tool | Price |
|---|---|---|
| HTTP | `GET /v1/risk/:chainId/:address` | $0.01 USDC, Base mainnet (`eip155:8453`), x402 `exact` |
| HTTP | `GET /v1/flags/:chainId/:address` (bytecode-only preview) | free |
| MCP `https://x402.magneta.finance/mcp` | `contract_risk_summary {chainId:int, address:string}` | $0.01 |
| MCP | `contract_quick_flags`, `supported_chains`, `scoring_rubric` | free |

Chains (20): mainnets 1, 10, 56, 100, 130, 137, 146, 480, 5000, 8453, 42161, 42220, 43114, 59144, 81457, 534352;
testnets 84532, 11155111, 11155420, 421614. The payment is always in USDC on Base mainnet, whichever chain the target contract is on.

## Workflow

0. Confirm the target chain id and address with the user (never guess an address).
1. Free first: call `/v1/flags/:chainId/:address` (or `contract_quick_flags`). If it already shows a blocking flag for your use case, stop; no need to pay.
2. If the decision still depends on source verification, owner state or static analysis, ask the user to approve the $0.01 report, then buy it.
3. Read the report (below), apply your own threshold, and tell the user which flags drove the decision.
4. A report is cached server-side for 10 minutes per chain+address; the payment still happens on each call, so do not re-buy the same pair in a loop.

## Call it

Versions this repo is tested with: `@x402/core|evm|fetch|mcp` **2.28.0**, `viem` **2.57.7**, `@coinbase/cdp-sdk` **1.58.0**,
`@modelcontextprotocol/sdk` 1.32.1. Pin exact versions.

### (a) HTTP with `@x402/fetch` + `@x402/evm`

```ts
import { x402Client, wrapFetchWithPayment, x402HTTPClient } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(process.env.BUYER_PRIVATE_KEY as `0x${string}`); // holds USDC on Base
const client = new x402Client();
client.setSpendControls({ maxAmountPerPayment: "$0.05" });
client.register("eip155:*", new ExactEvmScheme(account));
const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const httpClient = new x402HTTPClient(client);

const res = await fetchWithPayment("https://x402.magneta.finance/v1/risk/8453/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913");
if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
const settle = httpClient.getPaymentSettleResponse((n) => res.headers.get(n)); // PAYMENT-RESPONSE header
const report = await res.json();
console.error("paid tx", settle.transaction, "payer", settle.payer);
```

The same wrapper is packaged as `@magnetafinance/contract-risk` (published on npm: `npm i --ignore-scripts @magnetafinance/contract-risk @x402/core@2.28.0 @x402/evm@2.28.0 @x402/fetch@2.28.0 viem@2.57.7`)` (`createContractRiskClient({ privateKey })` with `risk()`, `quickFlags()`, LangChain and AI SDK adapters).

### (b) MCP with `@x402/mcp`

```ts
import { createx402MCPClient } from "@x402/mcp";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(process.env.BUYER_PRIVATE_KEY as `0x${string}`);
const MAX_ATOMIC = 50_000n; // $0.05 in USDC base units (6 decimals)
const mcp = createx402MCPClient({
  name: "my-agent", version: "0.1.0",
  schemes: [{ network: "eip155:8453", client: new ExactEvmScheme(account) }], // X402_NETWORK=eip155:8453
  autoPayment: true,
  onPaymentRequested: async (ctx) => BigInt(ctx.paymentRequired.accepts[0].amount) <= MAX_ATOMIC, // refuse above the cap
});
await mcp.connect(new StreamableHTTPClientTransport(new URL("https://x402.magneta.finance/mcp")));
try {
  const r = await mcp.callTool("contract_risk_summary", { chainId: 8453, address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" });
  if (r.isError) throw new Error((r.content[0] as { text?: string }).text);
  const report = JSON.parse((r.content[0] as { text: string }).text);
  console.error("paid:", r.paymentMade, r.paymentResponse?.transaction);
} finally { await mcp.close(); }
```

Free tools use the same client (`mcp.callTool("contract_quick_flags", {chainId, address})`, `"supported_chains"`, `"scoring_rubric"`); no payment is requested.

### (c) Coinbase CDP-managed wallet / Agentic Wallet

Documented import only (from `@coinbase/cdp-sdk` 1.58.0); it drops into `wrapFetchWithPayment` in place of the `x402Client` in (a):

```ts
import { CdpX402Client } from "@coinbase/cdp-sdk/x402";
```

It needs `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`, `CDP_WALLET_SECRET`, plus `@x402/core`, `@x402/evm`, `@x402/svm`, `@x402/extensions`
installed. Constructor options (for example which network it targets: omitting them may mean mainnet) and wallet funding are
in the CDP buyer quickstart: https://docs.cdp.coinbase.com/x402/buyer/quickstart . Read it before writing the call; do not guess the API.
The wallet must hold USDC on Base mainnet to pay this service. For a no-code agent wallet, see Coinbase's Agentic Wallet docs.

## Reading the report

Key fields: `score` (0-100, higher = riskier), `level`, `flags[]`, `proxy`, `erc20` (owner, `ownerRenounced`, `paused`), `opcodes`,
`selectors.found`, `blockscout`/`sourcify` (verification), `aderyn` (`ran`, `counts`, `top`), `notes[]`.

Bands: 0-24 `low`, 25-49 `medium`, 50-74 `high`, 75-100 `critical`. Points are additive, capped at 100:

| Flag | Pts | Meaning |
|---|---|---|
| `unverified-source` | 25 | logic contract not verified on Blockscout nor Sourcify |
| `source-verification-unknown` | 0 | providers unreachable; not penalised, treat as unknown |
| `upgradeable-proxy` | 15 | proxy detected; admin can change behaviour |
| `owner-not-renounced` | 10 | `owner()` exists and is not the zero address |
| `mint-function` | 15 | mint selector present (supply can grow) |
| `blacklist-function` | 15 | blacklist / bot-list selector (transfers can be blocked per address) |
| `fee-or-limit-setters` | 10 | fee, tax, max-tx, max-wallet or trading-switch setters |
| `pausable` / `currently-paused` | 5 / 5 | pause selectors / `paused()` is true now |
| `selfdestruct-opcode` | 10 | SELFDESTRUCT in bytecode |
| `aderyn-high-findings:N` | 5 each, max 20 | high-severity static-analysis findings on verified source |

Caveats (from the service's own rubric, also served by `scoring_rubric`):
- Selector presence is a heuristic: the function may exist but be restricted or unused.
- A high score flags centralisation and upgrade power, not a proven exploit; a low score is not an endorsement.
- Reports are cached 10 minutes per chain+address.
- A good score on a contract whose `proxy.implementation` can be swapped is only as good as the proxy admin; check `proxy.admin`.

## Spend control

- Cap every payment at `$0.05` (the call costs $0.01): `setSpendControls({ maxAmountPerPayment: "$0.05" })` or the `onPaymentRequested` check above.
- Use a dedicated buyer wallet with a small USDC balance; never reuse a treasury key. Never print or log the key.
- The service's `payTo` address cannot be the payer (the facilitator rejects `self_send_not_allowed`).
- Budget per task: free preview first, at most one paid report per contract per decision.

## Errors (never charged)

| Status | Meaning |
|---|---|
| 400 | unsupported chain (`supportedChains` listed in body) or malformed address; returned before any payment is requested |
| 422 | `not_a_contract`: no code at that address on that chain |
| 429 | rate limited; back off and retry |
| 502 | upstream data source failed (`analysis_failed`) |
| 504 | analysis timeout (24 s hard deadline) |

x402 settles only successful responses, so every non-2xx above costs nothing. MCP failures come back as `isError: true` and are not settled either.
A `402` that survives the client wrapper usually means: wallet has no USDC on Base, the cap is below $0.01, or the scheme network is not `eip155:8453`/`eip155:*`.
