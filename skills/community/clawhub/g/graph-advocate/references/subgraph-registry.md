# Subgraph Registry Reference

14,733 classified subgraphs with query hints across 20+ chains.

## How to use
1. Search by protocol/chain keyword → get subgraph ID + query hint
2. Use subgraph ID to query via gateway: `POST https://gateway.thegraph.com/api/[KEY]/subgraphs/id/[ID]`
3. Free API key: https://thegraph.com/studio/ (100K queries/month)

## Common Subgraph Entity Names
| Protocol | Entity | Sort Field | Example Fields |
|----------|--------|------------|---------------|
| Uniswap V2 | pairs | reserveUSD | token0 { symbol }, token1 { symbol }, reserveUSD, volumeUSD |
| Uniswap V3 | pools | totalValueLockedUSD | token0 { symbol }, token1 { symbol }, totalValueLockedUSD, feeTier |
| Aave V2/V3 | markets | totalDepositBalanceUSD | name, inputToken { symbol }, totalDepositBalanceUSD, totalBorrowBalanceUSD |
| Compound | markets | totalDepositBalanceUSD | name, inputToken { symbol }, totalDepositBalanceUSD |
| ENS | registrations | registrationDate | domain { name }, registrant { id }, registrationDate |
| Curve | pools | totalValueLockedUSD | name, totalValueLockedUSD |

## Top Subgraphs by Query Volume
| Name | Network | ID (first 20 chars) | 30d Queries |
|------|---------|---------------------|-------------|
| Uniswap V4 Base | base | Qmbsc6XQWbiv4DfLVf... | 440M |
| Uniswap V3 | mainnet | 5zvR82QoaXYFyDEKLZ... | 22M |
| Uniswap V2 | mainnet | A3Np3RQbaBA6oKJgiw... | 51M |
| ENS | mainnet | (search registry) | 38M |
| Aerodrome | base | (search registry) | 47M |

## npm Package
`npx subgraph-registry-mcp` — MCP server with search, schema, and execute tools.
