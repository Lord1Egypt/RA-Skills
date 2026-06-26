# orange — Lightning Wallet for AI Agents

> [!WARNING]
> Alpha software. This project was largely vibe-coded and likely contains flaws. Do not use it for large sums of money.

`orange` is a CLI for the Orange SDK, a graduated-custody Lightning wallet. It gives any AI agent its own Lightning wallet through simple shell commands that output JSON.

Graduated custody means funds start in a trusted Spark backend for instant, low-cost transactions, then automatically move to self-custodial Lightning channels as the balance grows.

## Setup

### Prerequisites

**Rust** — Install via [rustup](https://rustup.rs/):

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**protoc** (Protocol Buffers compiler) — Required by the Spark SDK dependency:

```sh
# Ubuntu/Debian
sudo apt install -y protobuf-compiler

# macOS
brew install protobuf

# Arch
sudo pacman -S protobuf
```

### Install

```sh
git clone https://github.com/benthecarman/orange-skill.git
cd orange-skill
cargo install --path .
```

### Configure

```sh
cp config.toml.example config.toml
```

Edit `config.toml`. You need:
- A **storage path** — where wallet data (SQLite DB, seed, logs) will be stored
- A **chain source** — Esplora, Electrum, or Bitcoin Core RPC
- An **LSP** — Lightning Service Provider for channel management

A wallet seed is generated automatically on first run and saved to `{storage_path}/seed`. Back up this file — it's the only way to recover your wallet.

The defaults in `config.toml.example` are configured for Bitcoin mainnet:

```toml
network = "bitcoin"
storage_path = "~/.orange"

[chain_source]
type = "esplora"
url = "https://blockstream.info/api"

[lsp]
address = "69.59.18.144:9735"
node_id = "021deaa26ce6bb7cc63bd30e83a2bba1c0368269fa3bb9b616a24f40d941ac7d32"

[spark]
sync_interval_secs = 60
prefer_spark_over_lightning = false
# lnurl_domain = "breez.tips"
```

Pass the config path with `--config` (defaults to `config.toml` in the current directory):

```
orange --config /path/to/config.toml <command>
```

### Start the daemon and receive your first payment

```sh
# 1. Start the daemon (with or without webhooks)
orange daemon --webhook https://your-app.example.com/payments

# 2. In another terminal, generate an invoice
orange receive --amount 1000
# Share the returned invoice or full_uri with the sender

# 3. When the payment arrives, your webhook receives a payment_received event
#    Or poll it manually:
orange get-event        # see the event
orange event-handled    # acknowledge it

# 4. Check your balance
orange balance
```

## Running the Daemon

The daemon is the primary way to run orange. It keeps the wallet online and connected to the Lightning network.

```
orange daemon [--webhook <url> ...]
```

### With webhooks (push model)

When webhooks are configured, the daemon POSTs each event as JSON to every webhook URL in parallel and automatically marks events as handled.

```sh
orange daemon \
  --webhook "https://your-app.example.com/payments|your-secret-token" \
  --webhook "https://chat.example.com/notify"
```

Each `--webhook` value is a URL, optionally followed by `|token`. When a token is provided, it's sent as `Authorization: Bearer <token>` in the POST header so your endpoint can verify requests are authentic. Each webhook can have its own token (or none).

Your webhook endpoint should:

- Accept `POST` requests with `Content-Type: application/json`
- Verify the `Authorization: Bearer <token>` header if a token is configured
- Return any 2xx status code to acknowledge receipt
- Respond quickly — the daemon fires webhooks in parallel and won't block on slow responses, but non-2xx status codes and connection errors are logged to stderr
- Transient failures (connection errors and 5xx responses) are retried up to 3 times with exponential backoff (1s, 2s, 4s). Client errors (4xx) are not retried. If all retries are exhausted, the event is still marked as handled and will not be re-delivered

For a complete example of building a webstore that accepts Lightning payments using webhooks and LNURL-pay, see [docs/agent-payment-flows.md](docs/agent-payment-flows.md).

### Without webhooks (pull model)

When no webhooks are configured, the daemon keeps the wallet online but does not auto-acknowledge events. Events queue up in the SDK's persistent event queue and are consumed via `get-event` and `event-handled` from a separate terminal.

```sh
# Terminal 1: keep wallet online
orange daemon

# Terminal 2: pull events
orange get-event        # returns next pending event or null
orange event-handled    # ack it, advancing the queue
```

### Event Types

Every event includes a `type` and `timestamp` field. Example payload:

```json
{
  "type": "payment_received",
  "timestamp": 1700000000,
  "payment_id": "SC-abcd1234...",
  "payment_hash": "...",
  "amount_msat": 50000000,
  "amount_sats": 50000,
  "custom_records_count": 0,
  "lsp_fee_msats": null
}
```

| Type | Description | Key Fields |
|---|---|---|
| `payment_successful` | Outgoing payment completed | `payment_id`, `payment_hash`, `payment_preimage`, `fee_paid_msat` |
| `payment_failed` | Outgoing payment failed | `payment_id`, `payment_hash`, `reason` |
| `payment_received` | Incoming Lightning payment | `payment_id`, `payment_hash`, `amount_msat`, `amount_sats`, `lsp_fee_msats` |
| `onchain_payment_received` | Incoming on-chain payment | `payment_id`, `txid`, `amount_sat`, `status` |
| `channel_opened` | Channel is ready | `channel_id`, `counterparty_node_id`, `funding_txo` |
| `channel_closed` | Channel was closed | `channel_id`, `counterparty_node_id`, `reason` |
| `rebalance_initiated` | Trusted-to-Lightning rebalance started | `trigger_payment_id`, `amount_msat` |
| `rebalance_successful` | Rebalance completed | `trigger_payment_id`, `amount_msat`, `fee_msat` |
| `splice_pending` | Splice initiated, waiting to confirm | `channel_id`, `counterparty_node_id`, `new_funding_txo` |

## Event Commands

### get-event

Get the next pending event from the wallet's event queue. Returns the event without acknowledging it — call `event-handled` after processing.

```
orange get-event
```

Returns the event JSON if one is pending:

```json
{
  "type": "payment_received",
  "timestamp": 1700000000,
  "payment_id": "SC-abcd1234...",
  ...
}
```

Returns `null` if the queue is empty:

```json
{
  "event": null
}
```

### event-handled

Mark the current event as handled, removing it from the queue and advancing to the next event.

```
orange event-handled
```

```json
{
  "ok": true
}
```

Call this after you have fully processed the event returned by `get-event`. Do not call this if `get-event` returned `null`.

## One-Shot Commands

These commands perform a single action and exit. They can be run while the daemon is active to interact with the wallet (send payments, check balance, generate invoices, etc.).

### balance

Get wallet balance in satoshis.

```
orange balance
```

```json
{
  "trusted_sats": 50000,
  "lightning_sats": 100000,
  "pending_sats": 0,
  "available_sats": 150000
}
```

- `trusted_sats` — balance held in Spark trusted backend
- `lightning_sats` — balance in Lightning channels (self-custodial)
- `pending_sats` — in-flight or unconfirmed balance
- `available_sats` — total spendable (trusted + lightning)

### receive

Generate a single-use BIP21 URI with a BOLT11 invoice for receiving payment.

```
orange receive [--amount <sats>]
```

```json
{
  "invoice": "lnbc500u1p...",
  "address": "bc1q...",
  "amount_sats": 50000,
  "full_uri": "bitcoin:bc1q...?lightning=lnbc500u1p...",
  "from_trusted": false
}
```

- `--amount` — optional amount in satoshis
- `address` — may be `null` if no on-chain address is available
- `from_trusted` — whether this will be received into Spark trusted balance

### receive-offer

Get a reusable BOLT12 offer for receiving payments. Can be shared and paid multiple times.

```
orange receive-offer
```

```json
{
  "offer": "lno1q..."
}
```

### send

Send a payment to a lightning invoice, on-chain address, or BOLT12 offer.

```
orange send <payment> [--amount <sats>]
```

- `payment` — BOLT11 invoice, BOLT12 offer, on-chain address, or BIP21 URI
- `--amount` — required for on-chain addresses and amountless offers

```json
{
  "payment_id": "abcd1234...",
  "amount_sats": 1000,
  "status": "initiated"
}
```

### parse

Parse a payment string and return its details.

```
orange parse <payment>
```

```json
{
  "parsed": "PaymentInstructions { ... }"
}
```

### transactions

List transaction history.

```
orange transactions
```

```json
{
  "count": 2,
  "transactions": [
    {
      "id": "txid123...",
      "status": "Completed",
      "outbound": false,
      "amount_sats": 50000,
      "fee_sats": 100,
      "payment_type": "Lightning",
      "timestamp": 1700000000
    }
  ]
}
```

### channels

List lightning channels.

```
orange channels
```

```json
{
  "count": 1,
  "channels": [
    {
      "channel_id": "ch123...",
      "counterparty_node_id": "02abc...",
      "funding_txo": "txid:0",
      "is_channel_ready": true,
      "is_usable": true,
      "inbound_capacity_sats": 500000,
      "outbound_capacity_sats": 100000,
      "channel_value_sats": 600000
    }
  ]
}
```

### info

Get wallet and node information.

```
orange info
```

```json
{
  "node_id": "02def...",
  "lsp_connected": true,
  "tunables": {
    "trusted_balance_limit_sats": 100000,
    "rebalance_min_sats": 10000,
    "onchain_receive_threshold_sats": 50000,
    "enable_amountless_receive_on_chain": false
  }
}
```

### estimate-fee

Estimate the fee for a payment.

```
orange estimate-fee <payment>
```

```json
{
  "estimated_fee_sats": 150
}
```

### lightning-address

Get the wallet's lightning address, if one has been registered.

```
orange lightning-address
```

```json
{
  "lightning_address": "alice@breez.tips"
}
```

Returns `null` if no lightning address is registered.

### register-lightning-address

Register a lightning address for this wallet. The address will be `<name>@<lnurl_domain>` (default domain: `breez.tips`).

```
orange register-lightning-address <name>
```

```json
{
  "registered": true,
  "lightning_address": "alice@breez.tips"
}
```

Once registered, anyone can pay you using the lightning address. The domain is configured via `lnurl_domain` in the `[spark]` config section.

## Error Format

All errors are returned as JSON to stdout with a non-zero exit code:

```json
{
  "error": "Failed to get balance: ..."
}
```
