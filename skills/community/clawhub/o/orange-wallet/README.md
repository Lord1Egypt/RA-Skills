# orange

> [!WARNING]
> Alpha software. This project was largely vibe-coded and likely contains flaws. Do not use it for large sums of money.

A Lightning wallet for AI agents, built on the [Orange SDK](https://github.com/lightningdevkit/orange-sdk). Run the daemon to keep your wallet online and receive real-time payment notifications via webhooks or by polling the event queue.

Orange SDK uses graduated custody — funds start in a trusted Spark backend for instant, low-cost transactions, then automatically move to self-custodial Lightning channels as the balance grows.

## Getting Started

### 1. Install

Requires [Rust](https://rustup.rs/) and `protoc` (Protocol Buffers compiler):

```sh
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install protoc (Ubuntu/Debian — see SKILL.md for other platforms)
sudo apt install -y protobuf-compiler
```

```sh
git clone https://github.com/benthecarman/orange-skill.git
cd orange-skill
cargo install --path .
```

### 2. Configure

```sh
cp config.toml.example config.toml
```

The defaults in `config.toml.example` are configured for Bitcoin mainnet. A wallet seed is generated automatically on first run and saved to `{storage_path}/seed`.

```toml
network = "bitcoin"
storage_path = "~/.orange"

[chain_source]
type = "esplora"
url = "https://blockstream.info/api"

[lsp]
address = "69.59.18.144:9735"
node_id = "021deaa26ce6bb7cc63bd30e83a2bba1c0368269fa3bb9b616a24f40d941ac7d32"
```

### 3. Start the daemon

```sh
# With webhooks — events are POSTed to your endpoints automatically
orange daemon \
  --webhook "https://your-app.example.com/payments|your-secret-token" \
  --webhook "https://chat.example.com/notify"

# Or without webhooks — poll events manually with get-event/event-handled
orange daemon
```

### 4. Receive a payment

In a separate terminal:

```sh
# Generate an invoice
orange receive --amount 50000

# Or set up a reusable lightning address
orange register-lightning-address "alice"
```

Share the invoice or lightning address with the sender. When the payment arrives, your webhook will receive a `payment_received` event, or you can poll it with `orange get-event`.

### 5. Send a payment

```sh
orange send "lnbc500u1p..."
orange balance
```

## Setting Up Your Webhook Endpoint

The daemon POSTs a JSON body to each `--webhook` URL whenever a wallet event occurs. Your endpoint should accept `POST` requests with `Content-Type: application/json` and return any 2xx status code. Non-2xx responses and connection errors are logged to stderr but don't block the daemon.

Each webhook can include an optional Bearer token for authentication: `--webhook "url|token"`. Multiple `--webhook` flags fan out events to different services in parallel, each with its own auth.

When no webhooks are configured, events accumulate in the SDK's persistent queue. Poll them with `get-event` and acknowledge with `event-handled`.

See [SKILL.md](SKILL.md) for full command documentation with example JSON output.

## Commands

| Command | Description |
|---|---|
| `daemon` | Run the wallet daemon with optional webhook notifications |
| `get-event` | Get the next pending event from the queue |
| `event-handled` | Acknowledge the current event, advancing the queue |
| `balance` | Get wallet balance |
| `receive` | Generate single-use BIP21 receive URI |
| `receive-offer` | Get reusable BOLT12 offer |
| `send <payment>` | Send a payment |
| `parse <payment>` | Parse a payment string |
| `transactions` | List transaction history |
| `channels` | List lightning channels |
| `info` | Get wallet/node information |
| `estimate-fee <payment>` | Estimate fee for a payment |
| `lightning-address` | Get the wallet's lightning address |
| `register-lightning-address <name>` | Register a lightning address |

## License

[MIT](LICENSE)
