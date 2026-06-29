# The Graph x402 gateway — recipe & examples

Everything needed to discover, price, and query The Graph's subgraphs pay-per-query, with no API key.

## Endpoints

| | URL |
|---|---|
| Query a subgraph (mainnet) | `https://gateway.thegraph.com/api/x402/subgraphs/id/<SUBGRAPH_ID>` |
| Query a subgraph (testnet) | `https://testnet.gateway.thegraph.com/api/x402/subgraphs/id/<SUBGRAPH_ID>` |

- **Method:** `POST`, `Content-Type: application/json`, body `{"query":"...","variables":{}}`.
- **Payment:** the first request returns `402` with the challenge in a base64 **`payment-required` response header** (`accepts[]` → `scheme: exact`, `network: eip155:8453`, `asset:` USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, `amount:` atomic USDC, `extra.assetTransferMethod: eip3009`). Sign the EIP-3009 authorization and retry with the `X-PAYMENT` header — any x402 client (`@x402/fetch`, `@graphprotocol/client-x402`) does this for you. Settlement is **gasless** (the facilitator pays gas).
- **Price:** ~**$0.01 USDC** per query.

## 1. Discover a subgraph (free if you have a registry; else a tiny paid query)

Query The Graph **network subgraph** (`DZz4kDTdmzWLWsV373w2bSmoar3umKKH9y82SUKr5qmp`) with its fulltext index, ranked by curation signal:

```graphql
query Search($text: String!, $first: Int!) {
  subgraphMetadataSearch(text: $text, first: $first) {
    displayName
    description
    subgraphs(first: 1, where: { active: true }, orderBy: currentSignalledTokens, orderDirection: desc) {
      id
      currentVersion { subgraphDeployment { ipfsHash queryFeesAmount signalledTokens } }
    }
  }
}
```

`text` uses tsquery syntax — turn `"uniswap v3"` into `"uniswap:* & v3:*"`. The `subgraphs[0].id` is the `<SUBGRAPH_ID>` you query in step 2.

## 2. Query it

```graphql
{
  pools(first: 3, orderBy: volumeUSD, orderDirection: desc) {
    token0 { symbol }
    token1 { symbol }
    volumeUSD
  }
}
```

Example result (Uniswap V3, `5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV`):

```json
{
  "data": {
    "pools": [
      { "token0": { "symbol": "USDC" }, "token1": { "symbol": "WETH" }, "volumeUSD": "1234567890.12" }
    ]
  }
}
```

The paid response includes an `X-PAYMENT-RESPONSE` header (base64) with the settlement receipt: `{ success, transaction (tx hash), network, amount }`.

## Funding

Hold **USDC on Base** — no ETH needed (gasless). **Use a dedicated, low-balance wallet** funded with only the USDC you intend to spend; seeding it is a one-time human step. This skill makes paid **reads** — it does not swap, trade, or auto-top-up the wallet, so keep funding a separate, human-approved action. For server-side spend caps/allowlists, use an [Ampersend](https://ampersend.ai)-managed wallet.
