# Utility Endpoints

## Get a block

**Operation Identity:**
- Operation ID: `getBlock`
- `GET /v1/{chainName}/block_v2/{blockHeight}/`
- SDK: `BaseService.getBlock()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `blockHeight` | string | Yes | The block height or `latest` for the latest block available. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_hash` | string | The hash of the block. |
| `signed_at` | string | The block signed timestamp in UTC. |
| `height` | integer | The block height. |
| `block_parent_hash` | string | The parent block hash. |
| `extra_data` | string | Extra data written to the block. |
| `miner_address` | string | The address of the miner. |
| `mining_cost` | integer | The associated mining cost. |
| `gas_used` | integer | The associated gas used. |
| `gas_limit` | integer | The associated gas limit. |
| `transactions_link` | string | The link to the related tx by block endpoint. |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get all chain statuses

**Operation Identity:**
- Operation ID: `getAllChainStatus`
- `GET /v1/chains/status/`
- SDK: `BaseService.getAllChainStatus()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** All supported chains

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The chain name eg: `eth-mainnet`. |
| `chain_id` | string | The requested chain ID eg: `1`. |
| `is_testnet` | boolean | True if the chain is a testnet. |
| `logo_url` | string | A svg logo url for the chain. |
| `black_logo_url` | string | A black png logo url for the chain. |
| `white_logo_url` | string | A white png logo url for the chain. |
| `is_appchain` | boolean | True if the chain is an AppChain. |
| `synced_block_height` | integer | The height of the lastest block available. |
| `synced_blocked_signed_at` | string | The signed timestamp of lastest block available. |
| `has_data` | boolean | True if the chain has data and ready for querying. |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get all chains

**Operation Identity:**
- Operation ID: `getAllChains`
- `GET /v1/chains/`
- SDK: `BaseService.getAllChains()`

**Role:** specialized | **Credit Cost:** 0.01 per call | **API Type:** REST

**Chains:** All supported chains

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The chain name eg: `eth-mainnet`. |
| `chain_id` | string | The requested chain ID eg: `1`. |
| `is_testnet` | boolean | True if the chain is a testnet. |
| `db_schema_name` | string | Schema name to use for direct SQL. |
| `label` | string | The chains label eg: `Ethereum Mainnet`. |
| `category_label` | string | The category label eg: `Ethereum`. |
| `logo_url` | string | A svg logo url for the chain. |
| `black_logo_url` | string | A black png logo url for the chain. |
| `white_logo_url` | string | A white png logo url for the chain. |
| `color_theme` | object | The color theme for the chain. |
| `is_appchain` | boolean | True if the chain is an AppChain. |
| `appchain_of` | object | The ChainItem the appchain is a part of. |


**Credit Cost:** 0.01 per call

**Processing:** Realtime

---

## Get block heights

**Operation Identity:**
- Operation ID: `getBlockHeights`
- `GET /v1/{chainName}/block_v2/{startDate}/{endDate}/`
- SDK: `BaseService.getBlockHeights()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `startDate` | string | Yes | The start date in YYYY-MM-DD format. |
| `endDate` | string | Yes | The end date in YYYY-MM-DD format or `latest` for the latest block available. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page-size` | integer | No | 100 | Number of items per page. Omitting this parameter defaults to 100. |
| `page-number` | integer | No | - | 0-indexed page number to begin pagination. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |
| `pagination` | object | Pagination metadata. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_hash` | string | The hash of the block. |
| `signed_at` | string | The block signed timestamp in UTC. |
| `height` | integer | The block height. |
| `block_parent_hash` | string | The parent block hash. |
| `extra_data` | string | Extra data written to the block. |
| `miner_address` | string | The address of the miner. |
| `mining_cost` | integer | The associated mining cost. |
| `gas_used` | integer | The associated gas used. |
| `gas_limit` | integer | The associated gas limit. |
| `transactions_link` | string | The link to the related tx by block endpoint. |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get gas prices

**Operation Identity:**
- Operation ID: `getGasPrices`
- `GET /v1/{chainName}/event/{eventType}/gas_prices/`
- SDK: `BaseService.getGasPrices()`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `eventType` | string | Yes | The desired event type to retrieve gas prices for. Supports `erc20` transfer events, `uniswapv3` swap events and `nativetokens` transfers. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `event_type` | string | The requested event type. |
| `gas_quote_rate` | number | The exchange rate for the requested quote currency. |
| `base_fee` | string | b;The lowest gas fee for the latest block height. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `gas_price` | string | The average gas price, in WEI, for the time interval. |
| `gas_spent` | string | The average gas spent for the time interval. |
| `gas_quote` | number | The average gas spent in `quote-currency` denomination for the time interval. |
| `other_fees` | object | Other fees, when applicable. For example: OP chain L1 fees. |
| `total_gas_quote` | number | The sum of the L1 and L2 gas spent, in quote-currency, for the specified time interval. |
| `pretty_total_gas_quote` | string | A prettier version of the total average gas spent, in quote-currency, for the specified time interval, for rendering purposes. |
| `interval` | string | The specified time interval. |


**Credit Cost:** 1 per call

**Processing:** Batch

> **Note:** Currently support these event types: `erc20` token transfers, `nativetokens` transfer, and `uniswapv3` swap events.

#### Related guides

    How to Fetch Onchain Gas Prices and Estimate Gas Costs

---

## Get historical token prices

**Operation Identity:**
- Operation ID: `getTokenPrices`
- `GET /v1/pricing/historical_by_addresses_v2/{chainName}/{quoteCurrency}/{contractAddress}/`
- SDK: `PricingService.getTokenPrices()`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `quoteCurrency` | string | Yes | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `contractAddress` | string | Yes | Contract address for the token. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. Supports multiple contract addresses separated by commas. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `from` | string | No | - | The start day of the historical price range (YYYY-MM-DD). |
| `to` | string | No | - | The end day of the historical price range (YYYY-MM-DD). |
| `prices-at-asc` | boolean | No | - | Sort the prices in chronological ascending order. By default, it's set to `false` and returns prices in chronological descending order. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `update_at` | string |  |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `logo_urls` | object | The contract logo URLs. |
| `prices` | array | List of response items. |
| `items` | array | List of response items. |

### Logo Url Fields

| Field | Type | Description |
|-------|------|-------------|
| `token_logo_url` | string | The token logo URL. |
| `protocol_logo_url` | string | The protocol logo URL. |
| `chain_logo_url` | string | The chain logo URL. |

### Price Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_metadata` | object |  |
| `date` | string | The date of the price capture. |
| `price` | number | The price in the requested `quote-currency`. |
| `pretty_price` | string | A prettier version of the price for rendering purposes. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|


**Credit Cost:** 1 per call

**Processing:** Batch

> **Note:** Supports a comma separated list of token contract addresses.

If no date range is provided, the spot price (with a 5 minute refresh) is provided.

---

## Get log events by contract address

**Operation Identity:**
- Operation ID: `getLogEventsByAddress`
- `GET /v1/{chainName}/events/address/{contractAddress}/`
- SDK: `BaseService.getLogEventsByAddress()`

**Role:** specialized | **Credit Cost:** 0.01 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `contractAddress` | string | Yes | The requested contract address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `starting-block` | integer | No | - | The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `ending-block` | string | No | - | The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `page-size` | integer | No | 100 | Number of items per page. Omitting this parameter defaults to 100. |
| `page-number` | integer | No | - | 0-indexed page number to begin pagination. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |
| `pagination` | object | Pagination metadata. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `log_offset` | integer | The offset is the position of the log entry within an event log. |
| `tx_hash` | string | The requested transaction hash. |
| `raw_log_topics` | array<string> | The log topics in raw data. |
| `sender_contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `sender_name` | string | The name of the sender. |
| `sender_contract_ticker_symbol` | string |  |
| `sender_address` | string | The address of the sender. |
| `sender_address_label` | string | The label of the sender address. |
| `sender_logo_url` | string | The contract logo URL. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `sender_factory_address` | string | The address of the deployed UniswapV2 like factory contract for this DEX. |
| `raw_log_data` | string | The log events in raw. |
| `decoded` | object | The decoded item. |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 0.01 per item

**Processing:** Realtime

---

## Get log events by topic hash(es)

**Operation Identity:**
- Operation ID: `getLogEventsByTopicHash`
- `GET /v1/{chainName}/events/topics/{topicHash}/`
- SDK: `BaseService.getLogEventsByTopicHash()`

**Role:** specialized | **Credit Cost:** 0.01 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `topicHash` | string | Yes | The endpoint will return event logs that contain this topic hash. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `starting-block` | integer | No | - | The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `ending-block` | string | No | - | The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `secondary-topics` | string | No | - | Additional topic hash(es) to filter on - padded & unpadded address fields are supported. Separate multiple topics with a comma. |
| `page-size` | integer | No | 100 | Number of items per page. Omitting this parameter defaults to 100. |
| `page-number` | integer | No | - | 0-indexed page number to begin pagination. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `items` | array | List of response items. |
| `pagination` | object | Pagination metadata. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `log_offset` | integer | The offset is the position of the log entry within an event log. |
| `tx_hash` | string | The requested transaction hash. |
| `raw_log_topics` | array<string> | The log topics in raw data. |
| `sender_contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `sender_name` | string | The name of the sender. |
| `sender_contract_ticker_symbol` | string |  |
| `sender_address` | string | The address of the sender. |
| `sender_address_label` | string | The label of the sender address. |
| `sender_logo_url` | string | The contract logo URL. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `sender_factory_address` | string | The address of the deployed UniswapV2 like factory contract for this DEX. |
| `raw_log_data` | string | The log events in raw. |
| `decoded` | object | The decoded item. |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 0.01 per item

**Processing:** Realtime

---

## Get logs

**Operation Identity:**
- Operation ID: `getLogs`
- `GET /v1/{chainName}/events/`
- SDK: `BaseService.getLogs()`

**Role:** primary | **Credit Cost:** 0.01 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `starting-block` | integer | No | - | The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `ending-block` | string | No | - | The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`. |
| `address` | string | No | - | The address of the log events sender contract. |
| `topics` | string | No | - | The topic hash(es) to retrieve logs with. |
| `block-hash` | string | No | - | The block hash to retrieve logs for. |
| `skip-decode` | boolean | No | - | Omit decoded log events. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `log_offset` | integer | The offset is the position of the log entry within an event log. |
| `tx_hash` | string | The requested transaction hash. |
| `raw_log_topics` | array<string> | The log topics in raw data. |
| `sender_contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `sender_name` | string | The name of the sender. |
| `sender_contract_ticker_symbol` | string | The ticker symbol for the sender. This field is set by a developer and non-unique across a network. |
| `sender_address` | string | The address of the sender. |
| `sender_address_label` | string | The label of the sender address. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `sender_logo_url` | string | The contract logo URL. |
| `sender_factory_address` | string | The address of the deployed UniswapV2 like factory contract for this DEX. |
| `raw_log_data` | string | The log events in raw. |
| `decoded` | object | The decoded item. |


**Credit Cost:** 0.01 per item

**Processing:** Realtime

> **Note:** Limits:

- For a block range of 2,000 blocks or less, the response will include all logs within the range.
- For a block range greater than 2,000 blocks:- The response will include up to 10,000 logs.
- If the number of logs exceeds 10,000, no logs will be included in the response. Instead, the response will contain a suggested range within the `info` object, including a link and message.

---

## Get pool spot prices

**Operation Identity:**
- Operation ID: `getPoolSpotPrices`
- `GET /v1/pricing/spot_prices/{chainName}/pools/{contractAddress}/`
- SDK: `PricingService.getPoolSpotPrices()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, base-mainnet, optimism-mainnet, bsc-mainnet, gnosis-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `contractAddress` | string | Yes | The pool contract address. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. |
| `pool_address` | string | The deployed pool contract address. |
| `token_0_address` | string | The deployed contract address of `token_0` in the token pair making up the pool. |
| `token_0_name` | string | The deployed contract name of `token_0` in the token pair making up the pool. |
| `token_0_ticker` | string | The deployed contract symbol of `token_0` in the token pair making up the pool. |
| `token_0_price` | string | Price of `token_0` in units of `token_1`. |
| `token_0_price_24h` | string | Price of `token_0` in units of `token_1` as of 24 hours ago. |
| `token_0_price_quote` | string | Price of `token_0` in the selected quote currency (defaults to USD). |
| `token_0_price_24h_quote` | string | Price of `token_0` in the selected quote currency (defaults to USD) as of 24 hours ago. |
| `token_1_address` | string | The deployed contract address of `token_1` in the token pair making up the pool. |
| `token_1_name` | string | The deployed contract name of `token_1` in the token pair making up the pool. |
| `token_1_ticker` | string | The deployed contract symbol of `token_1` in the token pair making up the pool. |
| `token_1_price` | string | Price of `token_1` in units of `token_0`. |
| `token_1_price_24h` | string | Price of `token_1` in units of `token_0` as of 24 hours ago. |
| `token_1_price_quote` | string | Price of `token_1` in the selected quote currency (defaults to USD). |
| `token_1_price_24h_quote` | string | Price of `token_1` in the selected quote currency (defaults to USD) as of 24 hours ago. |
| `quote_currency` | string | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, `GBP`, `BTC` and `ETH`. |


**Credit Cost:** 1 per call

**Processing:** Batch

> **Note:** Supports pools on Uniswap V2, V3 and their forks on all [Foundational Chains](https://goldrush.dev/chains/).

---

## Get resolved address for registered address

**Operation Identity:**
- Operation ID: `getResolvedAddress`
- `GET /v1/{chainName}/address/{walletAddress}/resolve_address/`
- SDK: `BaseService.getResolvedAddress()`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, axie-mainnet, base-mainnet, matic-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `name` | string |  |


**Credit Cost:** 1 per call

**Processing:** Realtime

#### Related guides

    How to Resolve a Wallet Address Given an ENS Domain

---

# Enhanced Spam Lists

The GoldRush Enhanced Spam Lists are a public good designed to restore trust and transparency in the Web3 ecosystem by helping developers, explorers, wallets, and indexers protect their users from scam tokens and malicious contracts. 

The Enhanced Spam Lists can be accessed as an [npm package](https://www.npmjs.com/package/@covalenthq/goldrush-enhanced-spam-lists).

This package requires Node.js v18 or above.

### Step 1. Install the Package

You can install the package using npm, yarn or pnpm:

```shell npm
npm install @covalenthq/goldrush-enhanced-spam-lists
```

```shell yarn
yarn add @covalenthq/goldrush-enhanced-spam-lists
```

```shell pnpm
pnpm add @covalenthq/goldrush-enhanced-spam-lists
```

### Step 2. Use Cases

    
        ```javascript
        import {
            Networks,
            isERC20Spam,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        // With default options
        const isSpam = await isERC20Spam("0xTokenAddress", Networks.ETHEREUM_MAINNET);
        console.log(isSpam);
        ```
    
    
        ```javascript
        import {
            Confidence,
            Networks,
            isERC20Spam,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        const isPotentialSpam = await isERC20Spam(
            "0xTokenAddress",
            Networks.POLYGON_MAINNET,
            Confidence.MAYBE
        );
        console.log(isPotentialSpam);
        ```
    
    
        ```javascript
        import {
                Networks,
                isNFTSpam,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        const isNftSpam = await isNFTSpam("0xNftAddress", Networks.BSC_MAINNET);
        console.log(isNftSpam);
        ```
    
    
        ```javascript
        import {
            Networks,
            Confidence,
            isERC20Spam,
            clearCache,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        // With caching enabled (default)
        const withCache = await isERC20Spam(
            "0xTokenAddress",
            Networks.ETHEREUM_MAINNET,
            Confidence.YES,
            true // Enable caching (default)
        );

        // Without caching (always fetches fresh data)
        const withoutCache = await isERC20Spam(
            "0xTokenAddress",
            Networks.ETHEREUM_MAINNET,
            Confidence.YES,
            false // Disable caching
        );

        // Clear memory and disk cache if needed
        clearCache();
        ```
    
    
        ```javascript
        import {
            getERC20List,
            getNFTList,
            Confidence,
            Networks,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        // Get ERC20 spam list with default caching
        const ethSpamTokens = await getERC20List(Networks.ETHEREUM_MAINNET, Confidence.YES);

        // Get NFT spam list with caching disabled
        const bscSpamNfts = await getNFTList(Networks.BSC_MAINNET, false);
        ```
    
    
        ```javascript
        import {
            getERC20List,
            getSpamScore,
            Networks,
            Confidence,
        } from "@covalenthq/goldrush-enhanced-spam-lists";

        const ethSpamTokens = await getERC20List(
        Networks.ETHEREUM_MAINNET,
        Confidence.YES
        );
        const score = getSpamScore(ethSpamTokens[0]);
        console.log(score); // Returns the spam score as a string
        ```
