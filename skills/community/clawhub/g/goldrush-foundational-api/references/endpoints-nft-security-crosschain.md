# NFT, Security & Cross-Chain Endpoints

## Check ownership in NFT collection for specific token

**Operation Identity:**
- Operation ID: `checkOwnershipInNftForSpecificTokenId`
- `GET /v1/{chainName}/address/{walletAddress}/collection/{collectionContract}/token/{tokenId}/`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, base-mainnet, bsc-mainnet, gnosis-mainnet, optimism-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `collectionContract` | string | Yes | The requested collection address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `tokenId` | string | Yes | The requested token ID. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `address` | string | The requested address. |
| `collection` | string | The requested collection. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. Supported on all Foundational Chains. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `token_id` | string | b;The token's id. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `last_transfered_at` | string |  |
| `balance` | string | b;Nft balance. |
| `balance_24h` | string |  |
| `type` | string |  |
| `nft_data` | object |  |


**Credit Cost:** 1 per call

**Processing:** Batch

#### Related guides

    How to Create an NFT Allowlist (AKA Whitelist)

---

## Check ownership in NFT collection

**Operation Identity:**
- Operation ID: `checkOwnershipInNft`
- `GET /v1/{chainName}/address/{walletAddress}/collection/{collectionContract}/`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, base-mainnet, optimism-mainnet, bsc-mainnet, gnosis-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `collectionContract` | string | Yes | The requested collection address. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `traits-filter` | string | No | - | Filters NFTs based on a specific trait. If this filter is used, the API will return all NFTs with the specified trait. Must be used with "values-filter", is case-sensitive, and requires proper URL encoding. |
| `values-filter` | string | No | - | Filters NFTs based on a specific trait value. If this filter is used, the API will return all NFTs with the specified trait value. Must be used with "traits-filter", is case-sensitive, and requires proper URL encoding. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `address` | string | The requested address. |
| `collection` | string | The requested collection. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. Supported on all Foundational Chains. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `token_id` | string | b;The token's id. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `last_transfered_at` | string |  |
| `balance` | string | b;Nft balance. |
| `balance_24h` | string |  |
| `type` | string |  |
| `nft_data` | object |  |


**Credit Cost:** 1 per call

**Processing:** Batch

#### Related guides

    How to Create an NFT Allowlist (AKA Whitelist)

---

## Get NFTs for address

**Operation Identity:**
- Operation ID: `getNftsForAddress`
- `GET /v1/{chainName}/address/{walletAddress}/balances_nft/`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, bsc-mainnet, arbitrum-mainnet, optimism-mainnet, base-mainnet, mantle-mainnet, linea-mainnet, zksync-mainnet, gnosis-mainnet (+2 more)

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `no-spam` | boolean | No | - | If `true`, the suspected spam tokens are removed. Supported on all Foundational Chains. |
| `no-nft-asset-metadata` | boolean | No | - | If `true`, the response shape is limited to a list of collections and token ids, omitting metadata and asset information. Helpful for faster response times and wallets holding a large number of NFTs. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. Supported on all Foundational Chains. |
| `last_transfered_at` | string | The timestamp when the token was transferred. |
| `block_height` | integer | The height of the block. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `balance_24h` | string | b;The 24h asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `type` | string |  |
| `floor_price_quote` | number | The current floor price converted to fiat in `quote-currency`. The floor price is determined by the last minimum sale price within the last 30 days across all the supported markets where the collection is sold on. |
| `pretty_floor_price_quote` | string | A prettier version of the floor price quote for rendering purposes. |
| `floor_price_native_quote` | number | The current floor price in native currency. The floor price is determined by the last minimum sale price within the last 30 days across all the supported markets where the collection is sold on. |
| `nft_data` | array<object> |  |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get token approvals for address

**Operation Identity:**
- Operation ID: `getApprovals`
- `GET /v1/{chainName}/approvals/{walletAddress}/`
- SDK: `SecurityService.getApprovals()`

**Role:** primary | **Credit Cost:** 2 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `token_address` | string | The address for the token that has approvals. |
| `token_address_label` | string | The name for the token that has approvals. |
| `ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `logo_url` | string | The contract logo URL. |
| `quote_rate` | number | The exchange rate for the requested quote currency. |
| `balance` | string | b;Wallet balance of the token. |
| `balance_quote` | number | Value of the wallet balance of the token. |
| `pretty_balance_quote` | string | A prettier version of the quote for rendering purposes. |
| `value_at_risk` | string | Total amount at risk across all spenders. |
| `value_at_risk_quote` | number | Value of total amount at risk across all spenders. |
| `pretty_value_at_risk_quote` | string | A prettier version of the quote for rendering purposes. |
| `spenders` | array<object> | Contracts with non-zero approvals for this token. |


**Credit Cost:** 2 per call

**Processing:** Realtime

---

## Get activity across all chains for address

**Operation Identity:**
- Operation ID: `getAddressActivity`
- `GET /v1/address/{walletAddress}/activity/`
- SDK: `AllChainsService.getAddressActivity()`

**Role:** primary | **Credit Cost:** 0.5 per call | **API Type:** REST


### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | string | Yes | The requested wallet address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `testnets` | boolean | No | - | Set to true to include testnets with activity in the response. By default, it's set to `false` and only returns mainnet activity. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `address` | string | The requested address. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `extends` | object |  |
| `first_seen_at` | string | The timestamp when the address was first seen on the chain. |
| `last_seen_at` | string | The timestamp when the address was last seen on the chain. |


**Credit Cost:** 0.5 per call

**Processing:** Realtime

---

## Get multichain balances

**Operation Identity:**
- Operation ID: `getTokenBalances`
- `GET /v1/allchains/address/{walletAddress}/balances/`
- SDK: `AllChainsService.getMultiChainBalances()`

**Role:** specialized | **Credit Cost:** 2.5 per call | **API Type:** REST

**Use Cases:** wallets, accounting-tax-reporting, portfolio-tracking

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | string | Yes | The requested address. Domain names (e.g. `demo.eth`) NOT supported. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | string | No | all | Comma separated list of chain names or IDs to retrieve token balances from. Defaults to all foundational chains. |
| `limit` | integer | No | max | Number of token balances to return per page, up to the default max of 100 items. |
| `before` | string | No | - | Pagination cursor pointing to fetch token balances before a certain point. |
| `cutoff-timestamp` | integer | No | - | UNIX timestamp to retrieve the balance snapshot from the nearest block before the specified cutoff time. |
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, `GBP`, `BTC` and `ETH`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | Timestamp for when the data was last updated. |
| `cursor_before` | string | Pagination cursor pointing to the previous page. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `items` | array | List of token balances returned by the API. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `contract_display_name` | string | A display-friendly name for the contract. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_urls` | object | The contract logo URLs. |
| `last_transferred_at` | string | The timestamp when the token was transferred. |
| `is_native_token` | boolean | Indicates if a token is the chain's native gas token, eg: ETH on Ethereum. |
| `type` | string | One of `cryptocurrency`, `stablecoin`, `nft` or `dust`. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `balance_24h` | string | b;The 24h asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `quote_rate` | number | The exchange rate for the requested quote currency. |
| `quote_rate_24h` | number | The 24h exchange rate for the requested quote currency. |
| `quote` | number | The current balance converted to fiat in `quote-currency`. |
| `quote_24h` | number | The 24h balance converted to fiat in `quote-currency`. |
| `pretty_quote` | string | A prettier version of the quote for rendering purposes. |
| `pretty_quote_24h` | string | A prettier version of the 24h quote for rendering purposes. |
| `chain_id` | integer | The chain ID that this balance is on. eg: `1`. |
| `chain_name` | string | The chain name that this balance is on. eg: `eth-mainnet`. |
| `chain_display_name` | string | A display-friendly name for the chain. |


**Credit Cost:** 2.5 per call

**Processing:** Realtime

> **Note:** Base cost is `2.5` credits (including requests that return with status `200` but no items) for the first page.

Subsequent pages cost `1` credit.

All EVM chains are supported. When no chains are specified, the [Foundational Chains](https://goldrush.dev/chains) are passed as default.

Domain names (e.g. `demo.eth`) are not supported.

The UNIX `cutoff-timestamp` retrieves the token balance snapshot from the nearest block before the specified timestamp.

Balances presented in descending order of the fiat quote value for most major tokens. Minor tokens may be presented in descending order of their `last_transferred_at` timestamp.

---

## Get multichain & multiaddress transactions

**Operation Identity:**
- Operation ID: `getTransactions`
- `GET /v1/allchains/transactions/`
- SDK: `AllChainsService.getMultiChainMultiAddressTransactions()`

**Role:** specialized | **Credit Cost:** 0.25 per item | **API Type:** REST

**Use Cases:** wallets, portfolio-tracking, audit-compliance-forensics, accounting-tax-reporting

**Chains:** All supported chains

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | string | No | all | Comma separated list of chain names or IDs to retrieve transactions from. Defaults to all foundational chains. |
| `addresses` | string | No | - | Comma separated list of addresses for which transactions are fetched. |
| `limit` | integer | No | max | Number of transactions to return per page, up to the default max of 100 items. |
| `before` | string | No | - | Pagination cursor pointing to fetch transactions before a certain point. |
| `after` | string | No | - | Pagination cursor pointing to fetch transactions after a certain point. |
| `with-logs` | boolean | No | - | Whether to include raw logs in the response. |
| `with-decoded-logs` | boolean | No | - | Whether to include decoded logs in the response. |
| `with-internal` | boolean | No | - | Whether to include internal transfers/transactions. |
| `with-state` | boolean | No | - | Whether to include all transaction state changes with before and after values. |
| `with-input-data` | boolean | No | - | Whether to include the transaction's input data such as the Method ID. |
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, `GBP`, `BTC` and `ETH`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | Timestamp for when the data was last updated. |
| `cursor_before` | string | Pagination cursor pointing to the previous page. |
| `cursor_after` | string | Pagination cursor pointing to the next page. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `items` | array | List of transactions returned by the API. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_height` | integer | The height of the block. |
| `block_signed_at` | string | The signed block timestamp in UTC. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from blocks that are reorged. |
| `tx_hash` | string | The transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `miner_address` | string | The address of the miner who mined the block. |
| `from_address` | string |  |
| `from_address_label` | string | The label of `from` address. |
| `to_address` | string | The recipient's wallet address. |
| `to_address_label` | string | The label of `to` address. |
| `value` | string | b;The value of the transaction in wei. |
| `value_quote` | number | The value attached in `quote-currency` to this tx. |
| `pretty_value_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_offered` | integer | The gas offered for the transaction. |
| `gas_spent` | integer | The gas actually spent by the transaction. |
| `gas_price` | integer | The gas price at the time of this tx in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_metadata` | object | The requested chain native gas token metadata. |
| `successful` | boolean | Indicated whether the transaction was successful or failed. |
| `chain_id` | string | The chain ID of the blockchain where the transaction occurred. |
| `chain_name` | string | The chain name of the blockchain where the transaction occurred. |
| `explorers` | array<object> | The block explorer links for this transaction. |
| `log_events` | array<object> | Event logs generated by the transaction. |
| `internal_transfers` | array<object> | List of internal transfers/transactions associated with the wallet address. |
| `state_changes` | array<object> | List of state changes with before and after values and balances for involved contract and wallet addresses. |
| `input_data` | object | Object with a transaction's input data such as the Method ID. |


**Credit Cost:** 0.25 per item

**Processing:** Realtime

> **Note:** Base cost is `0.1` credits (e.g. requests that return with status `200` but no items).

Calls without logs cost `0.1` credits/item.

Calls `with-logs` costs `0.2` credits/item.

Calls `with-decoded-logs` costs `0.25` credits/item.

The following tracing features each cost `0.05` per transaction that they are available for:

- `with-internal` - includes internal transfers/transactions.
- `with-state` - includes all transaction state changes with before and after values.
- `with-input-data` - includes the transaction's input data such as the Method ID.

Currently, tracing features are supported on the following chains:

- `eth-mainnet`

This Multichain & Multiaddress Transactions API is supported across all EVM chains. When no chains are specified, the [Foundational Chains](https://goldrush.dev/chains) are passed as default.

Domain names (e.g. `demo.eth`) are not supported.

---
