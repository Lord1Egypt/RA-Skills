# Workflows & Decision Trees

## Quick Decision Tree

**Select the right endpoint based on what the user wants to do:**

### Balance & Portfolio Queries
- Check wallet balance → `getTokenBalancesForWalletAddress` (primary, 1 per call)
- Get historical balance at block → `getHistoricalTokenBalancesForWalletAddress` (specialized, 1 per call)
- Get portfolio value over time → `getHistoricalPortfolioForWalletAddress` (primary, 2 per item)
- Get native token only → `getNativeTokenBalance` (primary, 0.5 per call)

### Transaction Queries
- Get recent transactions → `getRecentTransactionsForAddress` (primary, 0.1 per item)
- Get paginated history → `getTransactionsForAddressV3` (primary, 0.1 per item)
- Get single transaction details → `getTransaction` (primary, 0.1 per call)
- Get ERC20 transfers → `getErc20TransfersForWalletAddress` (primary, 0.05 per item)
- Get transaction summary → `getTransactionSummary` (primary, 1 per call)

### Security & Approvals
- Check token approvals → `getApprovals` (primary, 2 per call)
- Check NFT approvals → `getNftApprovals` (primary, 1 per call)

### NFT & Token Queries
- Get NFT holdings → `getNftsForAddress` (primary, 1 per call)
- Get token holders → `getTokenHoldersV2ForTokenAddress` (specialized, 0.02 per item)

### Multi-chain Queries
- Check which chains address is active on → `getAddressActivity` (primary, 0.5 per call)
- Get balances across chains → `getMultiChainBalances` (specialized, 2.5 per call)
- Get transactions across chains → `getMultiChainMultiAddressTransactions` (specialized, 0.25 per item)

### Token & Price Queries
- Get token price history → `getTokenPrices` (primary, 1 per call)
- Get DEX pool prices → `getPoolSpotPrices` (specialized, Foundational only)

### Block & Event Queries
- Get block details → `getBlock` (specialized, 1 per call)
- Get block heights by date → `getBlockHeights` (specialized, 1 per call)
- Get contract event logs → `getLogEventsByAddress` (specialized, 0.01 per item)
- Get logs by topic hash → `getLogEventsByTopicHash` (specialized, 0.01 per item)

---

## Common Multi-Endpoint Workflows

### Portfolio Valuation & Analysis
```
1. getTokenBalancesForWalletAddress → Get current token holdings with spot prices
2. getHistoricalPortfolioForWalletAddress → Get historical portfolio value over time
3. getTransactionsForAddressV3 → Get full transaction history for cost basis
```
**Use case:** Portfolio trackers, tax calculators, wealth management dashboards

### Transaction Deep Dive
```
1. getRecentTransactionsForAddress → Get latest transactions
2. getTransaction(txHash) → Get detailed decoded data for specific transaction
3. getLogEventsByAddress → Get contract event logs for context
```
**Use case:** Transaction explorers, audit trails, forensic analysis

### Security Audit
```
1. getApprovals → Check ERC20 token approvals
2. getNftApprovals → Check NFT approvals
3. getRecentTransactionsForAddress → Review recent approval transactions
```
**Use case:** Security dashboards, wallet protection tools

### Multi-Chain Portfolio
```
1. getAddressActivity → Discover which chains the address is active on
2. getMultiChainBalances → Get balances across all active chains
3. getMultiChainMultiAddressTransactions → Get transaction history across chains
```
**Use case:** Cross-chain wallets, multi-chain portfolio trackers

### NFT Collection Analysis
```
1. getNftsForAddress → Get NFT holdings for an address
2. checkOwnershipInNft → Verify NFT ownership for token gating
3. getRecentTransactionsForAddress → Get recent NFT transaction history
```
**Use case:** NFT galleries, token-gated access, collection tracking

---

## Common Errors & Troubleshooting

This section covers common errors for frequently used endpoints.

### Get token balances for address

**1. 400 Bad Request - Invalid address**
- Solution: Ensure address starts with 0x and is 40 hex characters
- Example: Valid: `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`

**2. 404 Not Found - Chain not found**
- Solution: Use exact chain name (case-sensitive): `eth-mainnet` not "ethereum"
- Example: Correct: `eth-mainnet` | Wrong: `ethereum`

**3. Response contains spam tokens**
- Solution: Filter by `is_spam: false` or use minimum quote threshold
- Example: Filter: `items.filter(t => !t.is_spam && parseFloat(t.quote) > 0.01)`

### Get paginated transactions for address (v3)

**1. 400 Bad Request - Invalid pagination**
- Solution: Page numbers are 0-indexed. First page is 0, not 1.
- Example: First: `page-number=0` | Second: `page-number=1`

**2. Incomplete transaction history**
- Solution: Check `pagination.has_more` field. Continue until `has_more: false`.
- Example: Loop: `while (response.data.pagination.has_more)`

### Get a transaction

**1. 404 Not Found - Transaction not found**
- Solution: Verify tx hash format (0x + 64 hex chars) and wait for confirmation
- Example: Valid: `0x1234...` (66 chars total)

**2. Tracing costs extra credits**
- Solution: Each trace flag adds 0.05 credits. Only on Foundational chains.
- Example: Base: 0.1 | With traces: 0.25 credits

### Wallet Activity Stream

**1. WebSocket connection failed**
- Solution: Verify URL (wss://gr-staging-v2.streaming.covalenthq.com/graphql) and auth header
- Example: Header: `Authorization: Bearer YOUR_API_KEY`

**2. Subscription not receiving data**
- Solution: Use enum format: `ETH_MAINNET` not `eth-mainnet`. Check chain supports Streaming.
- Example: GraphQL: `ETH_MAINNET` | REST: `eth-mainnet`

### General Tips
- Always check `response.error` field before accessing `response.data`
- Chain names are case-sensitive: use exact values from Chain Capabilities Matrix
- Token balances are strings: use BigInt or decimal libraries for math
- Pagination is 0-indexed: first page is 0, not 1
- Check Chain Capabilities Matrix for feature availability
