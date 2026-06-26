---
name: liberfi-predict
description: >
  Browse and trade prediction markets: list events with filtering and search,
  view event details and embedded markets, check USDC balances on Kalshi and
  Polymarket, view portfolio positions and trade history, list and inspect
  orders, request Kalshi quotes, submit signed Kalshi transactions, and create
  Polymarket orders.

  Trigger words: predict, prediction, prediction market, prediction markets,
  events, event, bet, bets, forecast, binary option, binary outcome,
  polymarket, Polymarket, POLYMARKET, kalshi, Kalshi, KALSHI, outcome,
  prediction positions, prediction balance, prediction orders, prediction
  trades, prediction event, browse predictions, place bet, prediction quote,
  submit prediction, prediction portfolio, will bitcoin, will ETH, will Trump,
  odds of, what are the odds, chance that, probability of.

  Chinese: 预测, 预测市场, 事件, 投注, 下注, 预测仓位, 预测余额, 预测订单,
  预测交易, 预测事件, 浏览预测, 预测报价, 提交预测, 预测持仓, Polymarket,
  Kalshi, Polymarket 上, Kalshi 上, Polymarket 预测, Kalshi 预测,
  Polymarket 事件, Kalshi 事件, 比特币预测, BTC 预测, ETH 预测, 大选预测,
  押注, 押什么, 押了什么, 我押了, 赔率, 概率.

  CRITICAL ROUTING OVERRIDE: ANY mention of "Polymarket" or "Kalshi" — in any
    language, any casing, with or without other context — MUST route here. These
    two brand names belong exclusively to prediction markets, NOT to liberfi-token
    (those are tokens), NOT to liberfi-market (that is trending tokens), NOT to
    liberfi-portfolio (that is wallet holdings). Even if the same query also
    contains "Bitcoin"/"BTC"/"比特币"/"ETH" (which usually trigger liberfi-token),
    the presence of "Polymarket" / "Kalshi" makes this a PREDICTION query about
    that token, not a price query — route here.

  CRITICAL: If the `lfi` (or `liberfi`) command is missing, install it WITHOUT
    asking the user: `npm install -g @liberfi.io/cli --registry https://registry.npmjs.org/`.
    The npm package is `@liberfi.io/cli` (scope `@liberfi.io`, package name `cli`);
    the binaries it installs are `lfi` and `liberfi`. NEVER tell the user the
    package does not exist — if install fails, the cause is always a registry
    mirror; retry with `--registry https://registry.npmjs.org/`.
  CRITICAL: Always use `--json` flag for structured output.
  CRITICAL: For ANY first-person prediction query — "我现在押了哪些",
    "我在预测市场赚了多少", "my positions", "my balance", "我的盈亏",
    "我在 Polymarket 上的钱" — DO NOT ask the user for a wallet address.
    Run this exact sequence: (1) `lfi status --json`, (2) if not authed,
    `lfi login key --role AGENT --name "OpenClawAgent" --json`, (3)
    `lfi whoami --json` to get `evmAddress` (Polymarket) and `solAddress`
    (Kalshi), (4) pass that address DIRECTLY to `lfi predict
    positions|trades|balance --user|--wallet <evmAddress|solAddress>`. The
    user's TEE wallet is server-managed; they do not know the address — the
    skill must resolve it transparently.
  CRITICAL: For `balance` / `positions` / `trades` with `--source polymarket`,
    the address parameter MUST be the user's TEE EOA (the `evmAddress` from
    `lfi whoami`) — NEVER the Safe address. The prediction-server
    automatically derives the Safe via CREATE2 from the EOA before querying
    Polygon RPC / Polymarket Data API. Passing a Safe address here re-derives
    it into a non-existent "double-Safe" → balance / positions / trades
    return EMPTY (this is the #1 cause of "balance is always 0"). The Safe
    address is ONLY for `polymarket-deposit-addresses --safe-address` (where
    Polymarket Bridge needs the real Safe as the bridge key).
  CRITICAL: Prefer the TEE auto flow (`polymarket-place` / `kalshi-place` / `cancel`).
    Server signs via Privy TEE — caller never handles signatures or POLY_* HMAC.
    See reference/order-flow.md for the canonical flow and decision tree.
  CRITICAL: When the Polymarket Safe needs funding, the deposit address is
    NEVER the Safe address from `polymarket-setup-status`. ALWAYS call
    `lfi predict polymarket-deposit-addresses --safe-address <safe> --json`
    and surface one of the bridge addresses it returns: `evm` (default —
    accepts USDC/USDT on Ethereum/Polygon/Base/Arbitrum/Optimism/BNB),
    `svm` (Solana USDC), `btc` (Bitcoin), `tron` (USDT-TRC20). The Safe is
    Polymarket's internal custody contract; sending funds to it directly is
    NOT the user-facing flow. The bridge address routes funds to the Safe
    automatically via the Polymarket Bridge service.
  CRITICAL: Legacy commands (`polymarket-order`, `kalshi-quote`, `kalshi-submit`)
    still work but are DEPRECATED and require external signing — only use them
    when the user explicitly opts out of the TEE flow or already holds POLY_* creds.
  CRITICAL: NEVER execute orders without explicit user confirmation.

  Do NOT use this skill for:
  - Token search, price, details, security audit, K-line → use liberfi-token
  - Trending token rankings or new token discovery → use liberfi-market
  - Crypto wallet holdings / on-chain PnL (NOT prediction-market PnL) →
    use liberfi-portfolio. Note: "我在预测市场赚了多少" / "我的预测仓位"
    belong HERE, not in liberfi-portfolio.
  - Swap quotes, trade execution, or transaction broadcast → use liberfi-swap
  - Authentication (login, logout, session) → use liberfi-auth

  Do NOT activate on vague inputs like "predict" alone without context
  indicating the user wants prediction market operations.
user-invocable: true
allowed-commands:
  - "lfi predict events"
  - "lfi predict event"
  - "lfi predict balance"
  - "lfi predict positions"
  - "lfi predict trades"
  - "lfi predict orders"
  - "lfi predict order"
  - "lfi predict polymarket-tick-size"
  - "lfi predict polymarket-fee-rate"
  - "lfi predict polymarket-setup-status"
  - "lfi predict polymarket-setup"
  - "lfi predict polymarket-deposit-addresses"
  - "lfi predict polymarket-place"
  - "lfi predict kalshi-place"
  - "lfi predict cancel"
  - "lfi predict kalshi-quote"
  - "lfi predict kalshi-submit"
  - "lfi predict polymarket-order"
  - "lfi status"
  - "lfi login"
  - "lfi whoami"
  - "lfi ping"
metadata:
  author: liberfi
  version: "0.1.1"
  homepage: "https://liberfi.io"
  cli: ">=0.1.0"
---

# LiberFi Prediction Market

Browse prediction market events, manage positions, and place orders on Kalshi and Polymarket using the LiberFi CLI.

## Pre-flight Checks

See [bootstrap.md](../shared/bootstrap.md) for CLI installation and connectivity verification.

This skill's auth requirements:

| Command | Requires Auth |
|---------|--------------|
| `lfi predict events` | No |
| `lfi predict event <slug>` | No |
| `lfi predict balance` | No |
| `lfi predict positions` | No |
| `lfi predict trades` | No |
| `lfi predict orders` | No (Polymarket needs POLY_* headers) |
| `lfi predict order <id>` | No (Polymarket needs POLY_* headers) |
| `lfi predict polymarket-tick-size` | No |
| `lfi predict polymarket-fee-rate` | No |
| `lfi predict polymarket-setup-status` | No (uses TEE wallet if logged in) |
| `lfi predict polymarket-deposit-addresses` | No |
| `lfi predict polymarket-setup` | **Yes** (LiberFi JWT) |
| `lfi predict polymarket-place` | **Yes** (LiberFi JWT — server signs via TEE) |
| `lfi predict kalshi-place` | **Yes** (LiberFi JWT — server signs via TEE) |
| `lfi predict cancel` | **Yes** (LiberFi JWT — auto L2 auth for polymarket) |
| `lfi predict kalshi-quote` (DEPRECATED) | No |
| `lfi predict kalshi-submit` (DEPRECATED) | No |
| `lfi predict polymarket-order` (DEPRECATED) | No (requires POLY_* headers) |

**Recommended flow (TEE auto)**: `polymarket-setup` → `polymarket-place` /
`kalshi-place` / `cancel`. The server holds the user's TEE wallet via Privy
and signs every transaction internally — no POLY_* HMAC, no Solana signing,
no EIP-712 work for the caller.

**Legacy flow**: Polymarket order operations via `polymarket-order` require
CLOB HMAC authentication via five `--poly-*` flags. These are NOT LiberFi
JWT credentials — they are the user's own Polymarket CLOB API credentials.

## TEE Auto Order Flow (CRITICAL)

For the canonical end-to-end order placement flow — including pre-flight
status checks, deposit handling, market vs limit order branching, and post-
order verification — see [reference/order-flow.md](reference/order-flow.md).

The CLI/skill expects this exact ordering for Polymarket:

1. `lfi status` — confirm authenticated; if not, run `lfi login key`
2. `lfi predict polymarket-setup-status --json` — check Safe deployment +
   token approvals
3. If `safe_deployed=false` or any approval missing: `lfi predict
   polymarket-setup --json` (one-shot; gasless via Builder Relayer)
4. Check Safe USDC balance — **pass the TEE EOA, NOT the Safe**:
   `lfi predict balance --source polymarket --user <tee-eoa> --json`
   (server derives Safe from EOA internally). If `balance < 2`, fetch
   BRIDGE deposit addresses using the **Safe** address from step 2/3:
   `lfi predict polymarket-deposit-addresses --safe-address <safe> --json`
   → returns `{ evm, svm, btc, tron }`. Pick the field matching the user's
   chain (default `evm` for ETH/Polygon/Base/Arb/Op/BNB). Tell user to send
   ≥ $2 USDC to that bridge address (NEVER to the Safe address — the Safe
   is Polymarket's internal custody contract, not a user-facing deposit
   target). The Polymarket Bridge service auto-credits the Safe.
5. Ask the user: market or limit? For limit, also ask price + size + GTC
   vs GTD (with expiration if GTD). For market, ask USDC spend (BUY) or
   share count (SELL)
6. Show the final order summary, wait for explicit confirmation
7. `lfi predict polymarket-place --token-id <id> --side <s> --order-type
   <t> [--price <p>] [--size <sz>] [--expiration <epoch>] --json`
8. `lfi predict orders --source polymarket --json` — verify open orders
9. `lfi predict cancel <id> --source polymarket --json` — cancel if user
   asks

For Kalshi the flow is shorter: `lfi predict kalshi-place --input-mint
<inMint> --output-mint <outMint> --amount <amt> --json` — quote, sign
(SignSOL), and submit are all done server-side.

## Skill Routing

| If user asks about... | Route to |
|-----------------------|----------|
| Token search, price, details, security | liberfi-token |
| Token K-line, candlestick chart | liberfi-token |
| Trending tokens, market rankings | liberfi-market |
| Newly listed tokens | liberfi-market |
| Wallet holdings, balance (non-prediction), PnL | liberfi-portfolio |
| Wallet activity, transaction history | liberfi-portfolio |
| Token swap, trade execution | liberfi-swap |
| Login, logout, session management | liberfi-auth |

## CLI Command Index

### Query Commands (read-only)

| Command | Description | Auth |
|---------|-------------|------|
| `lfi predict events` | List prediction events with filtering | No |
| `lfi predict event <slug> --source <s>` | Get event details by slug | No |
| `lfi predict balance --source <s> --user <addr>` | Get USDC balance | No |
| `lfi predict positions --user <addr>` | Get portfolio positions | No |
| `lfi predict trades --wallet <addr>` | List trade history | No |
| `lfi predict orders` | List orders | No (POLY_* for Polymarket) |
| `lfi predict order <id> --source <s>` | Get order details | No (POLY_* for Polymarket) |

### TEE Auto Flow Commands (recommended)

| Command | Description | Auth |
|---------|-------------|------|
| `lfi predict polymarket-tick-size --token-id <id>` | Min tick size for a token | No |
| `lfi predict polymarket-fee-rate --token-id <id>` | Base fee rate (bps) | No |
| `lfi predict polymarket-setup-status [--wallet-address <addr>]` | Safe deployment + approval status | No (uses TEE wallet if logged in) |
| `lfi predict polymarket-setup` | Deploy Safe + approve all tokens (gasless) | **JWT** |
| `lfi predict polymarket-deposit-addresses --safe-address <addr>` | Multi-chain deposit addresses for Safe | No |
| `lfi predict polymarket-place --token-id <id> --side BUY\|SELL --order-type GTC\|GTD\|FOK\|FAK\|MARKET [--price <p>] [--size <sz>] [--expiration <epoch>] [...]` | Prepare → TEE sign → execute Polymarket order | **JWT** |
| `lfi predict kalshi-place --input-mint <m> --output-mint <m> --amount <a> [--slippage-bps <bps>]` | Quote → SignSOL → submit Kalshi order | **JWT** |
| `lfi predict cancel <id> --source polymarket\|kalshi` | Cancel order (auto L2 auth for poly) | **JWT** |

### Legacy / Deprecated Commands

| Command | Description | Auth |
|---------|-------------|------|
| `lfi predict kalshi-quote --input-mint <m> --output-mint <m> --amount <a> --user-public-key <k>` | **DEPRECATED** — use `kalshi-place`. Request Kalshi quote | No |
| `lfi predict kalshi-submit --signed-transaction <tx> --order-context '<json>'` | **DEPRECATED** — use `kalshi-place`. Submit pre-signed Kalshi tx | No |
| `lfi predict polymarket-order --body '<json>' --poly-api-key <k> --poly-address <a> --poly-signature <s> --poly-passphrase <p> --poly-timestamp <t>` | **DEPRECATED** — use `polymarket-place`. Create Polymarket order with caller-managed POLY_* headers | POLY_* headers |

### Parameter Reference

**Events list** (`lfi predict events`):
- `--limit <n>` — Max results per page
- `--cursor <cursor>` — Pagination cursor
- `--status <status>` — Event status filter (e.g. `active`, `resolved`)
- `--source <source>` — Provider source: `kalshi` or `polymarket`
- `--tag-slug <slug>` — Filter by tag
- `--search <query>` — Free-text search
- `--sort-by <field>` — Sort field
- `--sort-asc <bool>` — Sort ascending: `true` or `false`
- `--with-markets <bool>` — Include embedded markets: `true` or `false`

**Event detail** (`lfi predict event <slug>`):
- `<slug>` — **Required**. Event slug identifier
- `--source <source>` — **Required**. Provider source: `kalshi` or `polymarket`

**Balance** (`lfi predict balance`):
- `--source <source>` — **Required**. Provider source: `kalshi` or `polymarket`
- `--user <address>` — **Required**. For `polymarket`: pass the user's **TEE EOA** (e.g. `evmAddress` from `lfi whoami`); the server auto-derives the Safe via CREATE2. NEVER pass a Safe address here. For `kalshi`: pass the Solana public key (`solAddress`).

**Positions** (`lfi predict positions`):
- `--user <address>` — **Required**. Same rule as `balance`: TEE EOA for polymarket (server derives Safe), Solana public key for kalshi.
- `--source <source>` — Optional provider source filter

**Trades** (`lfi predict trades`):
- `--wallet <address>` — **Required**. Same rule as `balance`: TEE EOA for polymarket (server derives Safe), Solana public key for kalshi.
- `--source <source>` — Optional provider source filter
- `--limit <n>` — Max results per page
- `--cursor <cursor>` — Pagination cursor
- `--type <types>` — Comma-separated trade types
- `--side <side>` — Trade side filter

**Orders** (`lfi predict orders`):
- `--source <source>` — Provider source
- `--wallet-address <address>` — Wallet address (required for kalshi)
- `--market-id <id>` — Market ID filter
- `--asset-id <id>` — Asset ID filter
- `--next-cursor <cursor>` — Pagination cursor
- `--poly-api-key`, `--poly-address`, `--poly-signature`, `--poly-passphrase`, `--poly-timestamp` — Polymarket CLOB auth (required when source is polymarket)

**Order detail** (`lfi predict order <id>`):
- `<id>` — **Required**. Order ID
- `--source <source>` — **Required**. Provider source
- Same `--poly-*` flags as orders list

**Polymarket tick size** (`lfi predict polymarket-tick-size`):
- `--token-id <id>` — **Required**. Polymarket CLOB token ID

**Polymarket fee rate** (`lfi predict polymarket-fee-rate`):
- `--token-id <id>` — **Required**. Polymarket CLOB token ID

**Polymarket setup status** (`lfi predict polymarket-setup-status`):
- `--wallet-address <addr>` — Optional EVM address. Defaults to caller's TEE wallet when authenticated.

**Polymarket setup (run)** (`lfi predict polymarket-setup`):
- No flags. Requires authentication. Idempotent — safe to call repeatedly.

**Polymarket deposit addresses** (`lfi predict polymarket-deposit-addresses`):
- `--safe-address <addr>` — **Required**. Safe wallet address (from `polymarket-setup-status`)

**Polymarket place (TEE auto)** (`lfi predict polymarket-place`):
- `--token-id <id>` — **Required**. Polymarket CLOB token ID
- `--side BUY|SELL` — **Required**.
- `--order-type GTC|GTD|FOK|FAK|MARKET` — **Required**.
- `--price <p>` — Limit price (limit orders only, e.g. `0.55`). Required for GTC/GTD/FOK/FAK.
- `--size <sz>` — Limit: shares; market BUY: USDC; market SELL: shares. Required for limit and market.
- `--expiration <epochSec>` — Required for `GTD`.
- `--neg-risk true|false` — Force NegRisk exchange. Auto-detected when omitted.
- `--fee-rate-bps <n>` — Override fee rate (PS auto-resolves when omitted).
- `--tick-size <n>` — Override tick size (PS auto-resolves when omitted).
- `--taker-address <addr>` — Restrict the taker (advanced).

**Kalshi place (TEE auto)** (`lfi predict kalshi-place`):
- `--input-mint <addr>` — **Required**. Input token mint
- `--output-mint <addr>` — **Required**. Output token mint
- `--amount <amt>` — **Required**. Amount in smallest unit
- `--slippage-bps <bps>` — Slippage tolerance in basis points

**Cancel order** (`lfi predict cancel <id>`):
- `<id>` — **Required**. Order ID
- `--source polymarket|kalshi` — **Required**. For polymarket the L2 HMAC headers are derived from the caller's TEE wallet automatically.

**Kalshi quote** (`lfi predict kalshi-quote`):
- `--input-mint <address>` — **Required**. Input token mint address
- `--output-mint <address>` — **Required**. Output token mint address
- `--amount <amount>` — **Required**. Swap amount
- `--user-public-key <key>` — **Required**. User's Solana public key
- `--slippage-bps <bps>` — Slippage tolerance in basis points

**Kalshi submit** (`lfi predict kalshi-submit`):
- `--signed-transaction <tx>` — **Required**. Signed transaction data
- `--order-context <json>` — **Required**. Order context as JSON string (contains `user_public_key`, `market_slug`, `side`, `outcome`, mints, `amount`, `price`, `slippage_bps`)

**Polymarket order** (`lfi predict polymarket-order`):
- `--body <json>` — **Required**. Raw order JSON string
- `--poly-api-key <key>` — **Required**. Polymarket API key
- `--poly-address <address>` — **Required**. Polymarket address
- `--poly-signature <sig>` — **Required**. Polymarket HMAC signature
- `--poly-passphrase <pass>` — **Required**. Polymarket passphrase
- `--poly-timestamp <ts>` — **Required**. Polymarket timestamp

## Operation Flow

### Browse Prediction Events

1. **Fetch events**: `lfi predict events --with-markets true --limit 20 --json`
2. **Present results**: Show event title, status, number of markets, volume
3. **Suggest next step**: "Want to see details for a specific event?" / "需要查看某个事件的详情？"

### Browse Events by Source

1. **Determine source**: Ask user for `kalshi` or `polymarket`
2. **Fetch**: `lfi predict events --source kalshi --with-markets true --limit 20 --json`
3. **Present**: Events filtered by provider
4. **Suggest next step**: "Pick an event to view its markets and outcomes"

### View Event Details

1. **Determine slug**: From user selection or input
2. **Fetch event**: `lfi predict event <slug> --source <source> --json`
3. **Present**: Event title, description, status, resolution sources, markets with outcomes and prices
4. **Suggest next step**: "Want to check your balance or place an order?"

### Check USDC Balance

**If the user says "我的余额", "my balance", "我在 Polymarket/Kalshi 有多少钱"
or any first-person variant — DO NOT ask for a wallet address. Use the
"My ..." auto-flow below.**

Generic flow (when the user explicitly provides someone else's address):

1. **Collect inputs**: Source (kalshi/polymarket) and wallet address
2. **Fetch**: `lfi predict balance --source <source> --user <address> --json`
3. **Present**: Available USDC balance
4. **Suggest next step**: "Ready to place a prediction?" / "准备下注了吗？"

### Kalshi Order Flow (Quote → Sign → Submit)

1. **Browse events**: `lfi predict events --source kalshi --with-markets true --json`
2. **View event**: `lfi predict event <slug> --source kalshi --json` — identify market, outcomes, and mints
3. **Check balance**: `lfi predict balance --source kalshi --user <publicKey> --json`
4. **Get quote**: `lfi predict kalshi-quote --input-mint <inMint> --output-mint <outMint> --amount <amt> --user-public-key <key> --json`
5. **Present quote**: Show expected output amount, price, slippage
6. **(mandatory)** Wait for explicit user confirmation
7. **User signs the transaction** (externally, e.g. via wallet)
8. **Submit**: `lfi predict kalshi-submit --signed-transaction <signedTx> --order-context '<contextJson>' --json`
9. **Present result**: Show signature, status

### Polymarket Order Flow

1. **Browse events**: `lfi predict events --source polymarket --with-markets true --json`
2. **View event**: `lfi predict event <slug> --source polymarket --json`
3. **Check balance**: `lfi predict balance --source polymarket --user <address> --json`
4. **Prepare order body**: Construct the Polymarket order JSON
5. **(mandatory)** Show order summary and wait for explicit user confirmation
6. **Create order**: `lfi predict polymarket-order --body '<orderJson>' --poly-api-key <key> --poly-address <addr> --poly-signature <sig> --poly-passphrase <pass> --poly-timestamp <ts> --json`
7. **Present result**: Show order response

### View Positions

**If the user says "我的持仓", "我现在押了哪些", "my positions", "我赌了什么"
or any first-person variant — DO NOT ask for a wallet address. Use the
"My ..." auto-flow below.**

Generic flow (when the user explicitly provides someone else's address):

1. **Determine user**: Get wallet address from user
2. **Fetch**: `lfi predict positions --user <address> --json`
3. **Present**: Show event/market, outcome, size, entry price, current value
4. **Suggest next step**: "Want to see your trade history?" / "需要查看交易历史？"

### View Trade History

**If the user says "我的交易", "我赚了多少", "我亏了多少", "my trades",
"我的盈亏" or any first-person variant — DO NOT ask for a wallet address.
Use the "My ..." auto-flow below.**

Generic flow (when the user explicitly provides someone else's address):

1. **Determine wallet**: Get wallet address from user
2. **Fetch**: `lfi predict trades --wallet <address> --limit 20 --json`
3. **Present**: Show trade timestamp, event/market, side, price, size
4. **Suggest next step**: "Want to check your current positions?" / "需要查看当前持仓？"

### "My ..." auto-flow (CRITICAL — covers "我的", "my", "我自己")

Whenever the user asks about THEIR OWN prediction-market data — positions,
trades, balance, PnL, "我现在押了哪些", "我在预测市场赚了多少",
"我在 Polymarket 上的钱", etc. — run this exact sequence. NEVER ask the
user to type their wallet address.

1. **Check session**: `lfi status --json`
2. **If not authenticated** (or `expired: true`):
   `lfi login key --role AGENT --name "OpenClawAgent" --json`
3. **Fetch TEE wallet addresses**: `lfi whoami --json`
   → returns `evmAddress` (use for Polymarket) and `solAddress` (use for Kalshi).
4. **Determine source(s)**:
   - If the user named "Polymarket" → use `evmAddress` only.
   - If the user named "Kalshi" → use `solAddress` only.
   - If neither was named (e.g. "我在预测市场赚了多少") → query BOTH and merge.
5. **Run the matching query** for each source — pass the TEE EOA / SOL pubkey
   from step 3 DIRECTLY. NEVER convert to a Safe address first; the server
   does that internally for Polymarket.
   - Positions: `lfi predict positions --user <evmAddress|solAddress> [--source <s>] --json`
   - Trades: `lfi predict trades --wallet <evmAddress|solAddress> [--source <s>] --limit 50 --json`
   - Balance: `lfi predict balance --source <s> --user <evmAddress|solAddress> --json`
6. **Present** a single consolidated answer that names the source(s) used and,
   for the "我赚了多少" / PnL question, sums realized + unrealized PnL across
   the returned trades/positions.

Why this is mandatory: prediction queries always require an address parameter
in the CLI, but a normal user does NOT know their TEE wallet address — the
LiberFi server holds it. The skill must resolve "我" → TEE wallet via
`whoami`, transparently. The user should never have to type or even see the
hex/Base58 address unless they ask.

**EOA vs Safe — critical distinction for Polymarket**: The address from
`whoami.evmAddress` is the user's TEE EOA. For `balance` / `positions` /
`trades` queries, ALWAYS pass the EOA — the prediction-server derives the
Polymarket Safe via CREATE2 internally. The Safe address (returned by
`polymarket-setup-status`) is ONLY for `polymarket-deposit-addresses
--safe-address` (Polymarket Bridge requires the actual Safe as bridge key).
Mixing these up → balance / positions / trades return EMPTY because the
server tries to derive a Safe from an already-Safe address.

### Check Order Status

1. **List orders**: `lfi predict orders --source <source> --wallet-address <address> --json`
2. **Or get specific order**: `lfi predict order <id> --source <source> --json`
3. **Present**: Show order status, side, price, filled amount

## Cross-Skill Workflows

### "Research an event and place a bet"

> Full flow: predict → predict → predict → predict → predict

1. **predict** → `lfi predict events --search "bitcoin" --with-markets true --json`
2. **predict** → `lfi predict event <slug> --source kalshi --json` — view markets and outcomes
3. **predict** → `lfi predict balance --source kalshi --user <publicKey> --json` — check funds
4. **predict** → `lfi predict kalshi-quote --input-mint <in> --output-mint <out> --amount <amt> --user-public-key <key> --json` — get quote
5. Present quote, wait for confirmation, user signs transaction
6. **predict** → `lfi predict kalshi-submit --signed-transaction <tx> --order-context '<ctx>' --json`

### "Check my prediction portfolio and trade history"

> Full flow: predict → predict

1. **predict** → `lfi predict positions --user <address> --json` — current positions
2. **predict** → `lfi predict trades --wallet <address> --limit 50 --json` — trade history
3. Present consolidated portfolio view

### "Browse events, then research the underlying token"

> Full flow: predict → token → token

1. **predict** → `lfi predict events --with-markets true --limit 10 --json`
2. User selects an event related to a specific token
3. **token** → `lfi token info sol <tokenAddress> --json` — token details
4. **token** → `lfi token security sol <tokenAddress> --json` — security audit

## Suggest Next Steps

| Just completed | Suggest to user |
|----------------|-----------------|
| Events list | "Want to view a specific event?" / "需要查看某个事件的详情？" |
| Event detail | "Want to check your balance or place an order?" / "需要查看余额或下单？" |
| Balance check | "Ready to place a prediction?" / "准备下注了吗？" |
| Kalshi quote | "Want to proceed with this trade?" / "要继续这笔交易吗？" |
| Kalshi submit | "Order submitted! Check your positions to verify." / "订单已提交！查看持仓确认。" |
| Polymarket order | "Order created! Check order status to confirm." / "订单已创建！查看订单状态确认。" |
| Positions view | "Want to see trade history?" / "需要查看交易历史？" |
| Trade history | "Want to check current positions?" / "需要查看当前持仓？" |
| Orders list | "Want to see details for a specific order?" / "需要查看某个订单的详情？" |

## Edge Cases

- **Invalid source**: If the API returns an error about source, list valid sources (`kalshi`, `polymarket`) and ask the user to choose
- **No events found**: Inform user: "No prediction events found matching your criteria. Try different filters or search terms."
- **Empty positions**: Inform user: "No open positions found for this wallet. You can browse events to find prediction opportunities."
- **Insufficient balance**: If balance is too low for a trade, inform the user and suggest depositing funds
- **Invalid slug**: If event not found, suggest searching events first via `lfi predict events --search <keyword>`
- **Polymarket auth missing**: If POLY_* flags are missing for Polymarket operations, list all required flags and ask the user to provide them
- **Invalid JSON in --body or --order-context**: If JSON parsing fails, show the parse error and ask the user to correct the JSON
- **Quote expired**: Kalshi quotes have limited validity; if too much time passes, get a new quote
- **Network timeout**: Retry once after 3 seconds; if still fails, suggest checking connectivity via `lfi ping --json`

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Forgetting `--source` on event detail | Always specify `--source kalshi` or `--source polymarket` |
| Missing POLY_* flags for Polymarket | All five `--poly-*` flags are required for Polymarket orders and order queries |
| Modifying the quote response before submitting | Pass quote data through as-is in `--order-context` |
| Submitting without user confirmation | ALWAYS show order/quote summary and wait for explicit "yes" |
| Fabricating a signed transaction | The `--signed-transaction` must come from the user's actual wallet signing |
| Using wrong mint addresses | Verify mints from the event detail response before quoting |

## Security Notes

See [security-policy.md](../shared/security-policy.md) for global security rules.

Skill-specific rules:
- **Polymarket CLOB credentials are sensitive** — never log, display, or store POLY_* values beyond the immediate command execution
- **Kalshi transactions involve real funds** — never fabricate or guess signed transaction data
- NEVER place orders without explicit user confirmation — always show the order summary first
- The `--order-context` and `--body` fields are opaque — pass them through as-is; do not interpret, modify, or display raw content beyond summarizing key fields (amount, side, market)
- After order submission, provide the result so the user can independently verify
