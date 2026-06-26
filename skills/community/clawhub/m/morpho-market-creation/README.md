# Morpho Market Deploy

Helper skill for deploying Morpho markets backed by API3 oracle feeds.

## Requirements

- `pnpm`
- `ts-node`
- `WALLET_MNEMONIC` in `.env` (see `example.env`)
- completed `oracle-params.json` and `market-params.json`

## Scripts

- `get-dapis.ts` and `get-chains.ts` to validate feeds and networks
- `read-data-feed.ts` to verify API3 reader proxies
- `get-oracle-contract-link.ts` to open the factory contract write page
- `deploy-oracle.ts` to deploy the oracle contract from `oracle-params.json`
- `create-market.ts` to create the Morpho market from `market-params.json`

