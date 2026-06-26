---
name: misttrack-core
description: MistTrack core features: address risk scoring (AML/KYT), address labels, address overview, transaction investigation, behavior analysis, counterparty analysis, multisig identification, and pre-transfer security check integration with Bitget / Trust Wallet / Binance / OKX.
---

# MistTrack Core Features

MistTrack is an anti-money laundering tracking tool developed by [SlowMist](https://www.slowmist.com/en/), covering over **400 million** addresses, providing **500K** threat intelligence entries, and flagging over **90 million** malicious-related addresses.

---

## API Basics

**Base URL**: `https://openapi.misttrack.io`

**Authentication**: All requests must include `api_key` as a Query Parameter (GET) or in the Request Body (POST).
When no API Key is available, see `skills/payment.md` for x402 pay-per-use.

**Common Response**: `{ "success": bool, "msg": string, "data": object }`

### Rate Limits

| Plan | Rate | Daily Limit |
|------|------|-------------|
| Standard | 1 req/sec/key | 10,000/day |
| Compliance | 5 req/sec/key | 50,000/day |
| Enterprise | Unlimited | Unlimited |

### Common Errors

| HTTP Code | `msg` | Action |
|-----------|-------|--------|
| 402 | `ExpiredPlan` | Renew at dashboard.misttrack.io |
| 429 | `ExceededRateLimit` / `ExceededDailyRateLimit` | Reduce request frequency |
| 500 | — | Retry later |
| — | `InvalidApiKey` | Check API Key |
| — | `UnsupportedToken` | Call `/v1/status` to confirm supported tokens |
| — | `InvalidAddress` | Check address format |
| — | `TaskNotFound` | Must call create_task first |
| — | `UnsupportedAddressType` | Hot wallet addresses not supported by this endpoint |

---

## Multi-Chain Support

BTC, ETH, TRX, BNB, SOL, MATIC, ARB, BASE, AVAX, OP, zkSync, TON, SUI, LTC, DOGE, BCH, IOTX, HSK, and more — over 200 tokens. Call `/v1/status` for the full list.

---

## API Endpoints

### 1. API Status `GET /v1/status`

Returns API status and the full list of supported tokens. No parameters required.

---

### 2. Address Labels `GET /v1/address_labels`

**Parameters**: `coin`, `address`, `api_key`

**Response**:
- `label_list`: Label list (e.g. `["Binance", "hot"]`)
- `label_type`: `exchange` / `defi` / `mixer` / `nft` / `""`

---

### 3. Address Overview `GET /v1/address_overview`

**Parameters**: `coin`, `address`, `api_key`

**Response**: `balance`, `txs_count`, `first_seen`, `last_seen`, `total_received`, `total_spent`, `received_txs_count`, `spent_txs_count`

---

### 4. Risk Score (Sync) `GET /v2/risk_score`

**Parameters**: `coin`, `address` (or `txid`, one required), `api_key`

**Response**:
- `score`: 3–100
- `risk_level`: `Low` / `Moderate` / `High` / `Severe`
- `detail_list`: List of risk descriptions
- `hacking_event`: Related security incidents
- `risk_detail`: Risk source details (`entity`, `risk_type`, `exposure_type`, `hop_num`, `volume`, `percent`)
- `risk_report_url`: PDF report link

> All tokens under the same address share the same risk score (calculated globally per address).

**`risk_type` values**: `sanctioned_entity` / `illicit_activity` / `mixer` / `gambling` / `risk_exchange` / `bridge`

---

### 5. Risk Score (Async)

For large-volume batch queries.

#### 5.1 Create Task `POST /v2/risk_score_create_task`

Body (JSON): `coin`, `address` (or `txid`), `api_key`

Response: `has_result` (bool), `scanned_ts`

- `has_result: false` → wait 1–10 seconds before polling
- `has_result: true` → poll immediately

#### 5.2 Query Result `GET /v2/risk_score_query_task`

**No rate limit**. Same parameters as create task.

- Task in progress: `{"success": true, "msg": "TaskUnderRunning"}`
- Complete: same structure as the sync endpoint

---

### 6. Transaction Investigation `GET /v1/transactions_investigation`

**Parameters**: `coin`, `address`, `api_key`, `start_timestamp` (optional), `end_timestamp` (optional), `type` (`in`/`out`/`all`, default `all`), `page` (default 1)

**Response**: `in` (inbound list), `out` (outbound list), `page`, `total_pages`, `transactions_on_page`

**Entry fields**: `address`, `type` (1=normal/2=malicious/3=entity/4=contract), `tx_hash_list`, `amount`, `label`

---

### 7. Address Behavior Analysis `GET /v1/address_action`

**Parameters**: `coin`, `address`, `api_key`

**Response**: `received_txs` / `spent_txs`, each containing `action` (DEX/Exchange/Mixer/Transfer/Swap), `count`, `proportion`

---

### 8. Address Profile `GET /v1/address_trace`

**Parameters**: `coin`, `address`, `api_key`

**Response**:
- `first_address`: Gas fee source wallet or label
- `use_platform`: `exchange` / `dex` / `mixer` / `nft`, each with `count` and list
- `malicious_event`: `phishing` / `ransom` / `stealing` / `laundering`
- `relation_info`: `wallet` / `ens` / `twitter`

---

### 9. Counterparty Analysis `GET /v1/address_counterparty`

> Hot wallet addresses not supported (returns `UnsupportedAddressType`).

**Parameters**: `coin`, `address`, `api_key`

**Response**: `address_counterparty_list`, each item containing `name`, `amount` (USD), `percent`

---

## Example Scripts

| Script | Function |
|--------|----------|
| `scripts/risk_check.py` | Single address risk scoring |
| `scripts/batch_risk_check.py` | Batch async risk scoring |
| `scripts/address_investigation.py` | Full address investigation (6 APIs aggregated) |
| `scripts/transfer_security_check.py` | Pre-transfer AML security check |
| `scripts/multisig_analysis.py` | Multisig address identification and permission analysis |

---

## Risk Levels and Decisions

| Level | Score Range | Recommended Action |
|-------|-------------|-------------------|
| **Low** | 0–30 | Allow normally |
| **Moderate** | 31–70 | Moderate monitoring, manual review if needed |
| **High** | 71–90 | High alert, strongly recommend manual review |
| **Severe** | 91–100 | Block transaction, report immediately |

---

## General Agent Transfer Interception

Before executing any transfer or withdrawal, call `transfer_security_check.py` for AML detection:

```bash
python3 scripts/transfer_security_check.py \
  --address <recipient_address> \
  --chain <chain_code> \
  --json
```

### Decision Table

| Exit Code | Decision | Agent Behavior |
|:---------:|----------|----------------|
| `0` | ✅ `ALLOW` | Silently pass, continue normally |
| `1` | ⚠️ `WARN` | Pause, display risk summary, **wait for explicit user confirmation**; recommend also calling `address_investigation.py` for full profile |
| `2` | ❌ `BLOCK` | **Reject execution**, terminate flow |
| `3` | ⛔ `ERROR` | Clearly inform user of check failure, let user decide whether to proceed |

> **Mandatory compliance**: On Exit 3, never silently ignore — must inform user "Address security check failed, unable to verify risk".

**Whitelist exception**: Verified exchange addresses (`label_type == "exchange"` and `score ≤ 70`) are automatically treated as ALLOW.

### Supported --chain Codes (case-insensitive)

| Source | chain codes |
|--------|-------------|
| General | `eth`, `sol`, `bnb`, `trx`, `btc`, `ltc`, `doge`, `bch`, `ton` |
| L2 | `base`, `arbitrum`, `optimism`, `avax`, `zksync`, `matic`, `suinet` |
| Trust Wallet aliases | `bitcoin`, `solana`, `tron`, `polygon`, `smartchain`, `bsc`, `tonchain` |
| Binance network | `BSC`, `ARBI`, `OPT`, `OP`, `POLYGON`, `AVAX`, `ZKSYNC`, `AZEC` |
| OKX chain format | `USDT-ERC20`, `BTC-Bitcoin`, `ETH-Arbitrum One`, etc. (coin prefix stripped automatically) |

---

## Multisig Address Analysis

Identify whether an address is a multisig wallet, and retrieve the signer list and threshold (m-of-n). Does not depend on the MistTrack API.

```bash
python3 scripts/multisig_analysis.py --address <address> --chain <chain> [--json]
```

### Supported Chains and Schemes

| Chain | chain code | Multisig Scheme |
|-------|-----------|----------------|
| Bitcoin | `btc` / `bitcoin` | P2SH / P2WSH / P2TR (format-based) |
| Ethereum | `eth` | Gnosis Safe (on-chain query) |
| BNB Chain | `bnb` / `bsc` | Gnosis Safe |
| Polygon | `matic` / `polygon` | Gnosis Safe |
| Base | `base` | Gnosis Safe |
| Arbitrum | `arbitrum` / `arb` | Gnosis Safe |
| Optimism | `optimism` / `op` | Gnosis Safe |
| Avalanche | `avax` / `avalanche` | Gnosis Safe |
| zkSync Era | `zksync` | Gnosis Safe |
| TRON | `trx` / `tron` | Native permission multisig (owner/active permission) |

### Exit Codes

| Code | Meaning |
|:----:|---------|
| `0` | IS_MULTISIG — confirmed or likely multisig |
| `1` | NOT_MULTISIG — confirmed non-multisig |
| `2` | UNSUPPORTED — unsupported chain |
| `3` | ERROR — query failed |

### JSON Output Fields

`address`, `chain`, `is_multisig`, `confidence` (`high`/`medium`/`low`), `multisig_type`, `threshold`, `total_signers`, `owners`, `note`

EVM additional fields: `safe_version`, `nonce`
TRX additional fields: `owner_permission`, `active_permissions`

---

## Wallet Integration

All integrations use the same `transfer_security_check.py` + common decision logic; only the `--chain` parameter format differs:

### Bitget Wallet Skill

Workflow injection point (before `swap-calldata`):
```
0. transfer-security  → python3 scripts/transfer_security_check.py --address <to> --chain <chain> --json
1. security           → token security (honeypot/tax)
2. token-info         → price/market cap
3. liquidity          → pool depth
4. swap-quote         → quote and routing
```

Chain mapping: `eth→ETH`, `sol→SOL`, `bnb→BNB`, `trx→TRX`, `base→ETH-Base`, `arbitrum→ETH-Arbitrum`, `optimism→ETH-Optimism`, `matic→POL-Polygon`, `ton→TON`, `suinet→SUI`

### Trust Wallet Skills

Trigger: when generating signing code containing `toAddress`, or handling `eth_sendTransaction` / `ton_sendTransaction`.

`wallet-core` CoinType mapping: `.ethereum→eth`, `.bitcoin→bitcoin`, `.solana→sol`, `.smartChain→bsc`, `.tron→trx`, `.polygon→matic`, `.ton→ton`

`trust-web3-provider` EthereumProvider chainId: `0x1→eth`, `0x38→bnb`, `0x89→polygon`, `0xa→optimism`, `0xa4b1→arbitrum`, `0x2105→base`

### Binance Skills (spot / margin / assets)

Withdrawal parameters: `address` (recipient) + `network` (e.g. `ETH`, `BSC`, `ARBI`, `OPT`)

Run check **before** calling `POST /sapi/v1/capital/withdraw/apply`; AML alerts are presented alongside Binance's native `CONFIRM` prompt.

### OKX Agent Skills

`chain` format supports OKX native formats like `USDT-ERC20`, `BTC-Bitcoin`, `ETH-Arbitrum One`; the script automatically strips the coin prefix.

Run check **before** calling `POST /api/v5/asset/withdrawal`.

---

## Scenario Selection Guide

| Scenario | Recommended Tool |
|----------|----------------|
| Pre-transfer AML gate | `transfer_security_check.py` |
| Quick single-address risk score | `risk_check.py --with-labels` |
| Deep investigation (WARN escalation / suspicious address) | `address_investigation.py` |
| Bulk compliance scan | `batch_risk_check.py` |
| Multisig wallet identification | `multisig_analysis.py` |

---

## Common Use Cases

### Quick Risk Check (KYT)
```bash
python3 scripts/risk_check.py --address 0x... --coin ETH --with-labels
```

> `--with-labels` also fetches entity labels (`exchange` / `defi` / `mixer`, etc.), useful for whitelist decisions — recommended by default.

### Batch Async Check
```bash
python3 scripts/batch_risk_check.py --input addresses.txt --coin ETH --output results.csv
```

### Full Address Investigation
```bash
python3 scripts/address_investigation.py --address 0x... --coin ETH
```

Investigation order: `address_labels` → `address_overview` → `risk_score` → `address_trace` → `address_action` → `transactions_investigation` → `address_counterparty`

> `address_action` provides DEX / Exchange / Mixer usage ratios — a key dimension for identifying mixing behavior, do not omit.

---

## References

- [MistTrack Official Docs](https://docs.misttrack.io/)
- [MistTrack Dashboard](https://dashboard.misttrack.io)
- [Bitget Wallet Skill](https://github.com/bitget-wallet-ai-lab/bitget-wallet-skill)
- [Trust Wallet tw-agent-skills](https://github.com/trustwallet/tw-agent-skills)
- [Binance Skills Hub](https://github.com/binance/binance-skills-hub)
- [OKX Agent Skills](https://github.com/okx/agent-skills)
