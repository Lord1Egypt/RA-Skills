# Transaction Endpoints

## Get a transaction

**Operation Identity:**
- Operation ID: `getTransaction`
- `GET /v1/{chainName}/transaction_v2/{txHash}/`
- SDK: `TransactionService.getTransaction()`

**Role:** primary | **Credit Cost:** 0.1 per call | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `txHash` | string | Yes | The transaction hash. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-logs` | boolean | No | - | Omit log events. |
| `with-internal` | boolean | No | - | Whether to include internal transfers/transactions. |
| `with-state` | boolean | No | - | Whether to include all transaction state changes with before and after values. |
| `with-input-data` | boolean | No | - | Whether to include the transaction's input data such as the Method ID. |

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
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |
| `internal_transfers` | array<object> | List of internal transfers/transactions associated with the wallet address. |
| `state_changes` | array<object> | List of state changes with before and after values and balances for involved contract and wallet addresses. |
| `input_data` | object | Object with a transaction's input data such as the Method ID. |


**Credit Cost:** 0.1 per call

**Processing:** Realtime

> **Note:** Base cost is `0.1` credits (e.g. requests that return with status `200` but no items).

Calls with `no-logs` cost `0.05` credits/item.

The following tracing features each cost `0.05` credits where available on [Foundational Chains](https://goldrush.dev/chains):

- `with-internal` - includes internal transfers/transactions.
- `with-state` - includes all transaction state changes with before and after values.
- `with-input-data` - includes the transaction’s input data such as the Method ID.

Currently, tracing features are supported on the following chains:

- `eth-mainnet`

#### Related guides

    Comparing GoldRush's Transactions API to RPC Providers
  

  
    How to Get Transaction History for an Address on Ethereum

---

## Get all transactions in a block by page (v3) 

**Operation Identity:**
- Operation ID: `getTransactionsForBlockByPage`
- `GET /v1/{chainName}/block/{blockHeight}/transactions_v3/page/{page}/`

**Role:** specialized | **Credit Cost:** 0.1 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `blockHeight` | integer | Yes | The requested block height. Also accepts `latest` to get latest block. |
| `page` | integer | Yes | The requested 0-indexed page number. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-logs` | boolean | No | - | Omit log events. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `chain_tip_height` | integer | The latest block height of the blockchain at the time this response was provided. |
| `chain_tip_signed_at` | string | The timestamp of the latest signed block at the time this response was provided. |
| `links` | object |  |
| `items` | array | List of response items. |

### Link Fields

| Field | Type | Description |
|-------|------|-------------|
| `prev` | string | URL link to the next page. |
| `next` | string | URL link to the previous page. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

---

## Get all transactions in a block (v3)

**Operation Identity:**
- Operation ID: `getTransactionsForBlockHash`
- `GET /v1/{chainName}/block_hash/{blockHash}/transactions_v3/`

**Role:** specialized | **Credit Cost:** 0.1 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `blockHash` | string | Yes | The requested block hash. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-logs` | boolean | No | - | Omit log events. |

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
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

#### Related guides

    Introducing Transactions V3 APIs
  

  
    Comparing GoldRush's Transactions API to RPC Providers
  

  
    How to Track Wallets or Transactions with the GoldRush API
  

  
    How to Get the Number of Transactions in a Block 
  

  
    How to Get All Historical Transactions in a Block

---

## Get earliest transactions for address (v3) 

**Operation Identity:**
- Operation ID: `getEarliestTimeBucketTransactionsForAddress`
- `GET /v1/{chainName}/bulk/transactions/{walletAddress}/`

**Role:** specialized | **Credit Cost:** 0.1 per item | **API Type:** REST

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
| `no-logs` | boolean | No | - | Omit log events. |

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
| `complete` | boolean |  |
| `current_bucket` | integer | The current bucket of the response. |
| `links` | object |  |
| `items` | array | List of response items. |

### Link Fields

| Field | Type | Description |
|-------|------|-------------|
| `prev` | string | URL link to the next page. |
| `next` | string | URL link to the previous page. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** Returns the same results as the first timebucket for an address in the **Get recent transactions** endpoint.

Requests that return status 200 and no data cost 0.1 credits.

Enabling `no-logs` reduces request cost to 0.05 per item.

#### Related guides

    Introducing Transactions V3 APIs
  

  
    Comparing GoldRush's Transactions API to RPC Providers
  

  
    How to Get Transaction History for an Address on Ethereum

---

## Get paginated transactions for address (v3)

**Operation Identity:**
- Operation ID: `getTransactionsForAddressV3`
- `GET /v1/{chainName}/address/{walletAddress}/transactions_v3/page/{page}/`

**Role:** primary | **Credit Cost:** 0.1 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `page` | integer | Yes | The requested page, 0-indexed. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-logs` | boolean | No | - | Omit log events. |
| `block-signed-at-asc` | boolean | No | - | Sort the transactions in ascending chronological order. By default, it's set to `false` and returns transactions in descending chronological order. |

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
| `current_page` | integer | The current page of the response. |
| `links` | object |  |
| `items` | array | List of response items. |

### Link Fields

| Field | Type | Description |
|-------|------|-------------|
| `prev` | string | URL link to the next page. |
| `next` | string | URL link to the previous page. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** This endpoint returns paginated transactions, starting with the earliest transactions on page 0. For the most recent transactions, refer to the [Get recent transactions for address (v3)](https://www.covalenthq.com/docs/api/transactions/get-recent-transactions-for-address-v3/) endpoint.

Requests that return status 200 and no data cost 0.1 credits.

Enabling `no-logs` reduces request cost to 0.05 per item.

#### Related guides

    Introducing Transactions V3 APIs
  

  
    Comparing GoldRush's Transactions API to RPC Providers
  

  
    How to Get Transaction History for an Address on Ethereum

---

## Get recent transactions for address (v3)

**Operation Identity:**
- Operation ID: `getRecentTransactionsForAddress`
- `GET /v1/{chainName}/address/{walletAddress}/transactions_v3/`

**Role:** primary | **Credit Cost:** 0.1 per item | **API Type:** REST

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
| `no-logs` | boolean | No | - | Omit log events. |
| `block-signed-at-asc` | boolean | No | - | Sort the transactions in ascending chronological order. By default, it's set to `false` and returns transactions in descending chronological order. |

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
| `current_page` | integer | The current page of the response. |
| `links` | object |  |
| `items` | array | List of response items. |

### Link Fields

| Field | Type | Description |
|-------|------|-------------|
| `prev` | string | URL link to the next page. |
| `next` | string | URL link to the previous page. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** Requests that return status 200 and no data cost 0.1 credits.

Enabling `no-logs` reduces request cost to 0.05 per item.

#### Related guides

    Introducing Transactions V3 APIs
  

  
    Comparing GoldRush's Transactions API to RPC Providers

---

## Get bulk time bucket transactions for address (v3)

**Operation Identity:**
- Operation ID: `getTimeBucketTransactionsForAddress`
- `GET /v1/{chainName}/bulk/transactions/{walletAddress}/{timeBucket}/`
- SDK: `TransactionService.getTimeBucketTransactionsForAddress()`

**Role:** specialized | **Credit Cost:** 0.1 per item | **API Type:** REST

**Chains:** All supported chains

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainName` | string | Yes | The chain name eg: `eth-mainnet`. |
| `walletAddress` | string | Yes | The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically. |
| `timeBucket` | integer | Yes | The 0-indexed 15-minute time bucket. E.g. 27 Feb 2023 05:23 GMT = 1677475383 (Unix time). 1677475383/900=1863861 timeBucket. |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `quote-currency` | string | No | - | The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`. |
| `no-logs` | boolean | No | - | Omit log events. |

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
| `complete` | boolean |  |
| `current_bucket` | integer | The current bucket of the response. |
| `links` | object |  |
| `items` | array | List of response items. |

### Link Fields

| Field | Type | Description |
|-------|------|-------------|
| `prev` | string | URL link to the next page. |
| `next` | string | URL link to the previous page. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. Use it to remove transactions from re-org-ed blocks. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_offset` | integer | The offset is the position of the tx in the block. |
| `successful` | boolean | Indicates whether a transaction failed or succeeded. |
| `from_address` | string | The sender's wallet address. |
| `miner_address` | string | The address of the miner. |
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
| `fees_paid` | string | b;The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. |
| `gas_quote` | number | The gas spent in `quote-currency` denomination. |
| `pretty_gas_quote` | string | A prettier version of the quote for rendering purposes. |
| `gas_quote_rate` | number | The native gas exchange rate for the requested `quote-currency`. |
| `explorers` | array<object> | The explorer links for this transaction. |
| `log_events` | array<object> | The log events. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** Requests that return status 200 and no data cost 0.1 credits.

Enabling `no-logs` reduces request cost to 0.05 per item.

#### Related guides

    Scaling Transactions API with Time Buckets
  

  
    Introducing Transactions V3 APIs
  

  
    Comparing GoldRush's Transactions API to RPC Providers

---

## Get transaction summary for address

**Operation Identity:**
- Operation ID: `getTransactionSummary`
- `GET /v1/{chainName}/address/{walletAddress}/transactions_summary/`
- SDK: `TransactionService.getTransactionSummary()`

**Role:** primary | **Credit Cost:** 1 per call | **API Type:** REST

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
| `with-gas` | boolean | No | - | Include gas summary details. Response times may be impacted for wallets with large number of transactions. |
| `with-transfer-count` | boolean | No | - | Represents the total count of ERC-20 token movement events, including `Transfer`, `Deposit` and `Withdraw`. Response times may be impacted for wallets with large number of transactions. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `address` | string | The requested address. |
| `chain_id` | integer | The requested chain ID eg: `1`. |
| `chain_name` | string | The requested chain name eg: `eth-mainnet`. |
| `items` | array | List of response items. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_count` | integer | The total number of transactions. |
| `transfer_count` | integer | Represents the total count of ERC-20 token movement events, including `Transfer`, `Deposit` and `Withdraw`. |
| `earliest_transaction` | object | The earliest transaction detected. |
| `latest_transaction` | object | The latest transaction detected. |
| `gas_summary` | object | The gas summary for the transactions. |


**Credit Cost:** 1 per call

**Processing:** Batch

> **Note:** - Base cost is `1` credit.
- Using `with-gas` is an additional `1` credit.
- Using `with-transfer-count` is an additional `3` credits.

#### Related guides

    Building Web3 Wallets (Part 7) - Multi-Chain Wallet Activity Summary 
  

  
    Comparing GoldRush's Transactions API to RPC Providers
  

  
    How to Get Transaction History for an Address on Ethereum

---

## Get Bitcoin transactions for non-HD address

**Operation Identity:**
- Operation ID: `getTransactionsForBtcAddress`
- `GET /v1/cq/covalent/app/bitcoin/transactions/`
- SDK: `BitcoinService.getTransactionsForBtcAddress()`

**Role:** primary | **Credit Cost:** 0.1 per item | **API Type:** REST

**Chains:** btc-mainnet

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `address` | string | No | - | The bitcoin address to query. |
| `page-size` | integer | No | 100 | Number of items per page. Omitting this parameter defaults to 100. |
| `page-number` | integer | No | - | 0-indexed page number to begin pagination. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `updated_at` | string | The timestamp when the response was generated. Useful to show data staleness to users. |
| `items` | array | List of response items. |
| `pagination` | object | Pagination metadata. |

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | integer | The requested chain ID eg: `20090103`. |
| `chain_name` | string | The requested chain name eg: `btc-mainnet`. |
| `contract_decimals` | integer | Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. |
| `block_signed_at` | string | The block signed timestamp in UTC. |
| `block_height` | integer | The height of the block. |
| `block_hash` | string | The hash of the block. |
| `tx_hash` | string | The requested transaction hash. |
| `tx_idx` | integer | The position index of the tx in the block. |
| `type` | string | Either 'input' as the sender or 'output' as the receiver of btc. |
| `address` | string | The wallet address. |
| `value` | string | b;The value attached to this tx in satoshi. |
| `quote` | number | The value attached to this tx in USD. |
| `quote_rate` | number | The value token exchange rate in USD. |
| `fees_paid` | string | b;The total transaction fees denoted in satoshi. |
| `gas_quote` | number | The gas spent in USD. |
| `gas_quote_rate` | number | The native gas token exchange rate in USD. |
| `coinbase` | boolean | Indicates if this is a coinbase tx where btc is rewarded to a miner for validating the block. |
| `locktime` | integer | The earliest Unix timestamp or block height at which the tx is valid and can be included. Is `0` if no restriction. |
| `weight` | integer | A measure that reflects impact on the block size limit. Used to determine fees. |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `has_more` | boolean | True if there is another page. |
| `page_number` | integer | The requested page number. |
| `page_size` | integer | The requested number of items on the current page. |
| `total_count` | integer | The total number of items across all pages for this request. |


**Credit Cost:** 0.1 per item

**Processing:** Realtime

> **Note:** Only supports non-HD bitcoin addresses.

---
