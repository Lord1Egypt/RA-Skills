# Balance Endpoints

## Get Bitcoin balance for non-HD address

**Operation Identity:**
- Operation ID: `getBitcoinBalanceForWalletAddress`
- `GET /v1/btc-mainnet/address/{walletAddress}/balances_v2/`
- SDK: `BitcoinService.getBitcoinNonHdWalletBalances()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** btc-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | string | Yes | The requested bitcoin non-HD address. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `contract_display_name` | string | A display-friendly name for the contract. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `logo_urls` | object | The contract logo URLs. |
| `last_transferred_at` | string | The timestamp when the token was transferred. |
| `block_height` | integer | The height of the block. |
| `native_token` | boolean | Indicates if a token is the chain's native gas token, eg: ETH on Ethereum. |
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
| `protocol_metadata` | object | The protocol metadata. |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get Bitcoin balances for HD address

**Operation Identity:**
- Operation ID: `getBitcoinHdWalletBalances`
- `GET /v1/btc-mainnet/address/{walletAddress}/hd_wallets/`
- SDK: `BitcoinService.getBitcoinHdWalletBalances()`

**Role:** specialized | **Credit Cost:** 0.1 per item | **API Type:** REST

**Use Cases:** wallets, accounting-tax-reporting, portfolio-tracking

**Chains:** btc-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | string | Yes | The extended public key (xPub/yPub/zPub) of the HD wallet. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert the balance to. Supports `USD`, `CAD`, `EUR`, etc. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The extended public key (xPub/yPub/zPub) or HD wallet address. |
| `chain_id` | integer | The requested chain ID eg: `20090103`. |
| `chain_name` | string | The requested chain name eg: `btc-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of HD wallet balance items, each containing derived addresses and balances. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `child_address` | string | The specific Bitcoin address derived from the HD wallet. |
| `address_path` | string | Derivation path used to derive the specific Bitcoin address, e.g., `M/0H/0/0`. |
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The name of the token, e.g., `Bitcoin`. |
| `contract_ticker_symbol` | string | The ticker symbol for the token, e.g., `BTC`. |
| `contract_address` | string | Address placeholder for native tokens like BTC. |
| `contract_display_name` | string | A display-friendly name for the token, e.g., `Bitcoin`. |
| `supports_erc` | array<string> | Typically null for Bitcoin, but left for compatibility. |
| `logo_url` | string | The contract logo URL. |
| `logo_urls` | object | The contract logo URLs. |
| `last_transferred_at` | string | The timestamp when the token was last transferred. |
| `native_token` | boolean | Indicates if a token is the chain's native gas token, eg: BTC on Bitcoin. |
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
| `protocol_metadata` | object | The protocol metadata. |
| `nft_data` | string | NA for bitcoin. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** Requests that return status 200 and no data cost 0.1 credits.

---

## Get ERC20 token transfers for address

**Operation Identity:**
- Operation ID: `getErc20TransfersForWalletAddress`
- `GET /v1/{chainName}/address/{walletAddress}/transfers_v2/`
- SDK: `BalanceService.getErc20TransfersForWalletAddress()`

**Role:** primary | **Credit Cost:** 0.05 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `contract-address` | string | Yes | - | The requested contract address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `starting-block` | integer | No | 0 | The block height to start from, defaults to `0`. |
| `ending-block` | integer | No | current | The block height to end at, defaults to current block height. |
| `page-size` | integer | No | 100 | Number of items per page. Omitting this parameter defaults to 100. |
| `page-number` | integer | No | - | 0-indexed page number to begin pagination. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
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
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Whether or not transaction is successful. |
| `miner_address` | string | The address of the miner. |
| `from_address` | string | The sender's wallet address. |
| `from_address_label` | string | The label of `from` address. |
| `to_address` | string | The receiver's wallet address. |
| `to_address_label` | string | The label of `to` address. |
| `value` | string | b;The value attached to this tx. |
| `value_quote` | number | The value attached in `quote-currency` to this tx. |
| `pretty_value_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_metadata` | object | The requested chain native gas token metadata. |
| `gas_offered` | integer |  |
| `gas_spent` | integer | The gas spent for this tx. |
| `gas_price` | integer | The gas price at the time of this tx. |
| `fees_paid` | string | b;The transaction's gas_price * gas_spent, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `transfers` | array<object> |  |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 0.05 per item

**Processing:** Realtime

---

## Get historical Bitcoin balance for non-HD address

**Operation Identity:**
- Operation ID: `getHistoricalBitcoinBalanceForWalletAddress`
- `GET /v1/btc-mainnet/address/{walletAddress}/historical_balances/`
- SDK: `BitcoinService.getBitcoinNonHdWalletBalances()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Use Cases:** accounting-tax-reporting, audit-compliance-forensics, portfolio-tracking

**Chains:** btc-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | string | Yes | Only Bitcoin non-HD addresses are supported. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `block-height` | integer | No | the | Ending block to define a block range. Omitting this parameter defaults to the latest block height. |
| `date` | string | No | the | Ending date to define a block range (YYYY-MM-DD). Omitting this parameter defaults to the current date. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `block_height` | integer | The height of the block. |
| `last_transferred_block_height` | integer | The block height when the token was last transferred. |
| `contract_display_name` | string |  |
| `last_transferred_at` | string | The timestamp when the token was transferred. |
| `native_token` | boolean | Indicates if a token is the chain's native gas token, eg: ETH on Ethereum. |
| `type` | string | One of `cryptocurrency`, `stablecoin`, `nft` or `dust`. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `quote_rate` | number | The exchange rate for the requested quote currency. |
| `quote` | number | The current balance converted to fiat in `quote-currency`. |
| `pretty_quote` | string | A prettier version of the quote for rendering purposes. |
| `protocol_metadata` | object | The protocol metadata. |
| `nft_data` | array<object> | NFT-specific data. |


**Credit Cost:** 1 per call

**Processing:** Realtime

---

## Get historical portfolio value over time

**Operation Identity:**
- Operation ID: `getHistoricalPortfolioForWalletAddress`
- `GET /v1/{chainName}/address/{walletAddress}/portfolio_v2/`
- SDK: `BalanceService.getHistoricalPortfolioForWalletAddress()`

**Role:** primary | **Credit Cost:** 2 per item | **API Type:** REST

**Use Cases:** portfolio-tracking, accounting-tax-reporting

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `days` | integer | No | 30 | The number of days to return data for. Defaults to 30 days. |

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
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `logo_url` | string | The contract logo URL. |
| `holdings` | array<object> |  |


**Credit Cost:** 2 per 30 days

**Processing:** Realtime

---

## Get historical token balances for address

**Operation Identity:**
- Operation ID: `getHistoricalTokenBalancesForWalletAddress`
- `GET /v1/{chainName}/address/{walletAddress}/historical_balances/`
- SDK: `BalanceService.getHistoricalTokenBalancesForWalletAddress()`

**Role:** specialized | **Credit Cost:** 1 per call | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, bsc-mainnet, base-mainnet, optimism-mainnet, gnosis-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-spam` | boolean | No | - | If `true`, the suspected spam tokens are removed. Supported on all Foundational Chains. |
| `block-height` | integer | No | the | Ending block to define a block range. Omitting this parameter defaults to the latest block height. |
| `date` | string | No | the | Ending date to define a block range (YYYY-MM-DD). Omitting this parameter defaults to the current date. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `block_height` | integer | The height of the block. |
| `last_transferred_block_height` | integer | The block height when the token was last transferred. |
| `contract_display_name` | string |  |
| `last_transferred_at` | string | The timestamp when the token was transferred. |
| `native_token` | boolean | Indicates if a token is the chain's native gas token, eg: ETH on Ethereum. |
| `type` | string | One of `cryptocurrency`, `stablecoin`, `nft` or `dust`. |
| `is_spam` | boolean | Denotes whether the token is suspected spam. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `quote_rate` | number | The exchange rate for the requested quote currency. |
| `quote` | number | The current balance converted to fiat in `quote-currency`. |
| `pretty_quote` | string | A prettier version of the quote for rendering purposes. |
| `protocol_metadata` | object | The protocol metadata. |
| `nft_data` | array<object> | NFT-specific data. |


**Credit Cost:** 1 per call

**Processing:** Realtime

> **Note:** Supported on all [Foundational Chains](https://goldrush.dev/chains/).

---

## Get native token balance for address

**Operation Identity:**
- Operation ID: `getNativeTokenBalance`
- `GET /v1/{chainName}/address/{walletAddress}/balances_native/`
- SDK: `BalanceService.getNativeTokenBalance()`

**Role:** primary | **Credit Cost:** 0.5 per call | **API Type:** REST

**Use Cases:** wallets, accounting-tax-reporting, portfolio-tracking

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `block-height` | integer | No | the | Ending block to define a block range. Omitting this parameter defaults to the latest block height. |

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
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `block_height` | integer | The height of the block. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `quote_rate` | number | The exchange rate for the requested quote currency. |
| `quote` | number | The current balance converted to fiat in `quote-currency`. |
| `pretty_quote` | string | A prettier version of the quote for rendering purposes. |


**Credit Cost:** 0.5 per call

**Processing:** Realtime

> **Note:** Not supported on non-EVM chains such as Bitcoin and Solana.

---

## Get token balances for address

**Operation Identity:**
- Operation ID: `getTokenBalancesForWalletAddress`
- `GET /v1/{chainName}/address/{walletAddress}/balances_v2/`
- SDK: `BalanceService.getTokenBalancesForWalletAddress()`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

**Use Cases:** wallets, portfolio-tracking, accounting-tax-reporting

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-spam` | boolean | No | - | If `true`, the suspected spam tokens are removed. Supported on all Foundational Chains. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | The requested address. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `quote_currency` | string | The requested quote currency eg: `USD`. |
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `contract_display_name` | string | A display-friendly name for the contract. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `logo_urls` | object | The contract logo URLs. |
| `last_transferred_at` | string | The timestamp when the token was transferred. |
| `block_height` | integer | The height of the block. |
| `native_token` | boolean | Indicates if a token is the chain's native gas token, eg: ETH on Ethereum. |
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
| `protocol_metadata` | object | The protocol metadata. |


**Credit Cost:** 1 per call

**Processing:** Realtime

#### Related guides

    Understanding Web3 Wallets with GoldRush
  

  
    How to Get Bitcoin Balances and Transactions
  

  
    Comparing GoldRush’s Token Balances API to RPC Providers

---

## Get token holders as of any block height (v2)

**Operation Identity:**
- Operation ID: `getTokenHoldersV2ForTokenAddress`
- `GET /v1/{chainName}/tokens/{tokenAddress}/token_holders_v2/`
- SDK: `BalanceService.getTokenHoldersV2ForTokenAddress()`

**Role:** specialized | **Credit Cost:** 0.02 per item | **API Type:** REST

**Chains:** eth-mainnet, matic-mainnet, bsc-mainnet, base-mainnet, optimism-mainnet, gnosis-mainnet

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `tokenAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `no-snapshot` | boolean | No | false | Defaults to `false`. Set to `true` to bypass last snapshot and get the latest token holders list. |
| `block-height` | integer | No | the | Ending block to define a block range. Omitting this parameter defaults to the latest block height. |
| `date` | string | No | the | Ending date to define a block range (YYYY-MM-DD). Omitting this parameter defaults to the current date. |
| `page-size` | integer | No | 100 | Number of items per page. Note: Currently, only values of `100` and `1000` are supported. Omitting this parameter defaults to 100. |
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
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `contract_name` | string | The string returned by the `name()` method. |
| `contract_ticker_symbol` | string | The ticker symbol for this contract. This field is set by a developer and non-unique across a network. |
| `contract_address` | string | Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. |
| `supports_erc` | array<string> | A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. |
| `logo_url` | string | The contract logo URL. |
| `address` | string | The requested address. |
| `balance` | string | b;The asset balance. Use `contract_decimals` to scale this balance for display purposes. |
| `total_supply` | string | b;Total supply of this token. |
| `block_height` | integer | The height of the block. |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 0.02 per item

**Processing:** Realtime

> **Note:** When no `block-height` is specified, the default is to use the latest token holder snapshot which updates every 30 mins.

To fetch the current token holders list without using the snapshot, set `no-snapshot=true`.

Page size is either `100` (default) or `1000`.

Supported only on [Foundational Chains](https://goldrush.dev/chains/).

---

# Enhanced Bitcoin Support

GoldRush offers production-grade Bitcoin data for wallets, tax tools, explorers, and analytics. We operate dedicated Bitcoin node infrastructure and index the chain from the genesis block to ensure complete, accurate balance and transaction history.

### Key Concepts
- **Hierarchical Deterministic (HD) Wallet** refers to a wallet that generates all of its keys and addresses from a single source (e.g. a seed phrase). These keys and addresses can be organized into a tree (hierarchial) and are always generated the same way (deterministic). 
- **Extended public keys** (e.g., `xpub...`, `ypub...`, `zpub...`) are HD address-level public keys used to derive many child receive addresses.
- **Non-HD addresses or child addresses** follow different standards:
    - **BIP44 Legacy, P2PKH**: addresses typically start with `1`, derived path `m/44'/0'/...`
    - **BIP49 Nested SegWit, P2SH-P2WPKH**: addresses typically start with `3`, derived path `m/49'/0'/...`
    - **BIP84 Native SegWit, P2WPKH/bech32**: addresses typically start with `bc1`, derived path `m/84'/0'/...`
    - **BIP86 Taproot, P2TR**: addresses typically start with `bc1p`, derived path `m/86'/0'/...`

For an excellent resource to understand HD wallets and derivation paths, see: [Learn Me A Bitcoin - HD Wallets](https://learnmeabitcoin.com/technical/keys/hd-wallets/)

### Capabilities

- **Full-chain ingestion**: Dedicated node and indexers ingest all Bitcoin transactions from genesis for complete historical coverage.
- **Extensive HD wallet derivation scans (gap limit 20)**: We continue to derive child addresses until encountering 20 consecutive child addresses with zero balance and no transaction history.
- **Support multiple child address formats**: Includes BIP44 Legacy, BIP49 Nested SegWit, BIP84 Native SegWit.
- **Spot and historical balances for non-HD/child addresses**: Includes current and historical **fiat price** conversions.
- **Spot balances for derived child addresses from HD wallet addresses (xpub/ypub/zpub)**: Includes spot balances, fiat prices and 24hr deltas.
- **Historical transactions for non-HD addresses**: Retrieve time-ordered transactions for a Bitcoin address for statements, tax, and activity feed workflows.

### API endpoints

- [Get Bitcoin balances for HD address](https://goldrush.dev/docs/api-reference/foundational-api/balances/get-bitcoin-balances-for-hd-address)
- [Get Bitcoin balance for non-HD address](https://goldrush.dev/docs/api-reference/foundational-api/balances/get-bitcoin-balance-for-address)
- [Get historical Bitcoin balance for non-HD address](https://goldrush.dev/docs/api-reference/foundational-api/balances/get-historical-bitcoin-balance-for-address)
- [Get transactions for Bitcoin non-HD address](https://goldrush.dev/docs/api-reference/foundational-api/transactions/get-transactions-for-bitcoin-address)
