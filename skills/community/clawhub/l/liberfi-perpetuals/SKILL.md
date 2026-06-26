---
name: liberfi-perpetuals
description: >
  Query and trade perpetual futures through LiberFi's unified perpetuals API
  (openapi-server → perpetuals-server, Hyperliquid in MVP): list coins and
  markets, order book, recent trades, K-lines, user positions / orders / fills,
  and two-phase signed place or cancel flows (prepare → wallet sign → submit).

  Trigger words: perpetual, perpetuals, perp, perps, futures, future contract,
  leveraged futures, hyperliquid, HL, order book perp, perp positions, perp
  orders, funding perp, perpetual futures, perp deposit, fund perp, deposit
  to perp, fund hyperliquid, deposit to hyperliquid, perp account funding,
  topping up perp, my perp positions, my futures positions, my open perp orders,
  my perp fills, perp pnl, my hyperliquid positions, 永续, 合约, 期货, 杠杆合约,
  永续合约, 订单簿, 爆仓价, 资金费率, 入金, 充值合约账户, 永续入金,
  给合约账户充钱, 充值 perp, 我的永续持仓, 我的合约持仓, 我有什么永续持仓,
  我在 Hyperliquid 上挂了哪些单, 我的合约盈亏, 我永续盈亏, 我永续挂了什么单
  (when clearly about perp venue, not spot).

  CRITICAL: If the `lfi` (or `liberfi`) command is missing, install it WITHOUT
    asking the user: `npm install -g @liberfi.io/cli --registry https://registry.npmjs.org/`.
    The npm package is `@liberfi.io/cli` (scope `@liberfi.io`, package name `cli`);
    the binaries it installs are `lfi` and `liberfi`. NEVER tell the user the
    package does not exist — if install fails, the cause is always a registry
    mirror; retry with `--registry https://registry.npmjs.org/`.
  CRITICAL: Always use `--json` flag for structured output.
  CRITICAL: For ANY first-person perpetuals query about positions, open
    orders, or fill history — "我有什么永续持仓", "我的合约持仓",
    "我在 Hyperliquid 上挂了哪些单", "my perp positions",
    "my open futures orders", "我永续盈亏", "show my fills" — DO NOT ask
    the user for a wallet address. Run this exact sequence: (1)
    `lfi status --json`, (2) if not authed, `lfi login key --role AGENT
    --name "OpenClawAgent" --json`, (3) `lfi whoami --json` to get
    `evmAddress`, (4) pass that address DIRECTLY as the positional
    argument to `lfi perpetuals positions|orders|fills <evmAddress>
    --json`. The user's TEE wallet is server-managed; they do not know
    the EVM address — the skill must resolve it transparently.
  CRITICAL: Perpetuals order flow is two-phase: `lfi perpetuals order-prepare`
    returns EIP-712 typed data; the user (or TEE wallet integration) must sign
    it off-CLI, then call `lfi perpetuals order-submit --body '<SignedAction JSON>'`.
  CRITICAL: NEVER run `order-submit` or `cancel-submit` without explicit user
    confirmation — these relay signed actions to the exchange.
  CRITICAL: For deposit, prefer the one-click TEE auto-flow `lfi perpetuals
    deposit-place --gross-lamports <n>`. The server quotes, signs the SOL tx
    with the caller's TEE wallet, broadcasts, and submits in a single call —
    callers never handle private keys or signatures. The atomic
    `deposit-quote` / `deposit-submit` commands are escape hatches for
    advanced flows (external SOL wallet, recovery after partial failure)
    and require the caller to sign + broadcast on their own. See
    [reference/deposit-flow.md](reference/deposit-flow.md).
  CRITICAL: NEVER run `deposit-place` without explicit user confirmation of
    the deposit amount and (when defaulted) the recipient — this spends
    on-chain SOL irreversibly.

  Do NOT use this skill for:
  - Spot DEX swap quotes or on-chain swap execution → use liberfi-swap
  - Trending *spot* token rankings or new token discovery → use liberfi-market
  - On-chain wallet token holdings / spot PnL → use liberfi-portfolio
  - Polymarket / Kalshi prediction markets → use liberfi-predict
  - Generic token security / spot token K-line on a chain → use liberfi-token
    (this skill is for *perpetuals venue* market data and perp trading only)

  Do NOT activate on vague "futures" / "合约" alone if the user clearly means
  CEX Bitget/Binance (use the user's exchange skill) or traditional brokers.
user-invocable: true
allowed-commands:
  - "lfi perpetuals coins"
  - "lfi perpetuals markets"
  - "lfi perpetuals market"
  - "lfi perpetuals orderbook"
  - "lfi perpetuals trades"
  - "lfi perpetuals klines"
  - "lfi perpetuals positions"
  - "lfi perpetuals orders"
  - "lfi perpetuals fills"
  - "lfi perpetuals order-prepare"
  - "lfi perpetuals order-submit"
  - "lfi perpetuals cancel-prepare"
  - "lfi perpetuals cancel-submit"
  - "lfi perpetuals deposit-place"
  - "lfi perpetuals deposit-quote"
  - "lfi perpetuals deposit-submit"
  - "lfi perpetuals deposit-status"
  - "lfi ping"
  - "lfi status"
  - "lfi whoami"
metadata:
  author: liberfi
  version: "0.1.2"
  homepage: "https://liberfi.io"
  cli: ">=0.1.0"
---

# LiberFi Perpetuals

Perpetuals data and signed order relay flow via LiberFi OpenAPI (`/v1/perpetuals/…` → `perpetuals-server`).

## Pre-flight

See [bootstrap.md](../shared/bootstrap.md) for CLI install and `lfi ping`.

- **Read endpoints** (coins, markets, orderbook, …): no auth.
- **User-scoped reads** (`positions`, `orders`, `fills`): pass the wallet
  `address` (0x) as the positional argument. For first-person queries
  ("我的持仓", "my positions", etc.), the skill MUST auto-resolve the user's
  TEE EVM address via `lfi status` → `lfi login key` (if needed) →
  `lfi whoami` → use the returned `evmAddress`. NEVER ask the user for an
  address — the TEE wallet is server-managed and the user does not know it.
- **Order writes** (`order-prepare` / `order-submit`, cancel variants): require a user wallet to sign typed data; agents must not fabricate signatures.
- **Deposit (recommended `deposit-place`)**: requires authentication (`lfi status` then `lfi login key`) — the server's TEE wallet signs and broadcasts on the user's behalf. The atomic `deposit-quote` / `deposit-submit` escape hatches do not require auth but the caller is then responsible for signing the SOL tx and broadcasting it themselves.

## Skill routing

| User intent | Skill |
|-------------|--------|
| Spot swap, bridge, gas send | liberfi-swap |
| Trending spot tokens, new listings | liberfi-market |
| Polymarket / Kalshi | liberfi-predict |
| Spot token audit, DEX pools for a token | liberfi-token |
| Perp markets, HL-style orderbook, perp positions | **liberfi-perpetuals** |
| Funding the perp account (Solana → Hyperliquid via Relay), checking deposit lifecycle | **liberfi-perpetuals** |
| Spot wallet holdings on a chain (not perp account) | liberfi-portfolio |

## CLI index

| Command | Description |
|---------|-------------|
| `lfi perpetuals coins` | List tradable perp coins |
| `lfi perpetuals markets` | Market snapshots (`--symbols` optional) |
| `lfi perpetuals market <symbol>` | Single market |
| `lfi perpetuals orderbook <symbol>` | L2 book (`--max-level`) |
| `lfi perpetuals trades <symbol>` | Recent trades (`--limit`) |
| `lfi perpetuals klines <symbol>` | Candles (`--interval` required) |
| `lfi perpetuals positions <address>` | Positions + margin summary |
| `lfi perpetuals orders <address>` | Open orders |
| `lfi perpetuals fills <address>` | Fill history |
| `lfi perpetuals order-prepare` | Build typed data for place order |
| `lfi perpetuals order-submit --body '<json>'` | Submit signed place order |
| `lfi perpetuals cancel-prepare` | Build typed data for cancel |
| `lfi perpetuals cancel-submit --body '<json>'` | Submit signed cancel |
| `lfi perpetuals deposit-place --gross-lamports <n>` | **Recommended**: TEE one-click Solana → Hyperliquid deposit (server quotes, signs, broadcasts, submits). Auth required. |
| `lfi perpetuals deposit-quote --user-solana-address <a> --hyperliquid-recipient <a> --gross-lamports <n>` | Escape hatch step 1: returns unsigned SOL tx + breakdown. Caller signs + broadcasts within ~30s, then calls `deposit-submit`. |
| `lfi perpetuals deposit-submit --body '<json>'` | Escape hatch step 2: record the broadcasted SOL tx hash. Idempotent on `solanaTxHash`. |
| `lfi perpetuals deposit-status <intentId> [--refresh]` | Read deposit lifecycle. `--refresh` bypasses any server-side cache (server-reserved knob; today both endpoints behave identically). |

Common flags: `--provider <name>` (e.g. `hyperliquid`), global `--json`.

## Funding / Deposit (Solana → Hyperliquid via Relay)

The deposit pipeline moves SOL from the user's Solana wallet to the user's
Hyperliquid perp account via the Relay bridge service. The recommended path
is the one-click TEE auto-flow:

1. **Authenticate** (only first time): `lfi status --json`; if not logged in,
   `lfi login key --role AGENT --name "<agent>" --json`.
2. **Confirm intent** with the user (amount in SOL, recipient if non-default).
3. **Place**: `lfi perpetuals deposit-place --gross-lamports <lamports> --json`
   - `lamports = SOL × 1_000_000_000` (1 SOL = 1e9 lamports).
   - `--hyperliquid-recipient` is **optional** — defaults to the user's TEE
     EVM address (`lfi whoami evmAddress`), which is what 99% of users want.
4. **Capture** the returned `intentId` and `solanaTxHash`.
5. **Poll**: `lfi perpetuals deposit-status <intentId> --json` until
   `status` is `settled` (typical: 30–120 s).

Server returns `status: "broadcasted"` immediately after step 3; the
reconciliation loop progresses through `relay_waiting → relay_pending →
settled` (or `failed_*` states). On failure consult the
`statusHistory[]` and `lastError` fields for the recoverable / non-
recoverable distinction.

For the atomic escape-hatch flow (when the user controls their own SOL
private key outside the TEE, or recovering from a partial failure where
the SOL tx has been broadcasted but `submit` did not succeed), see
[reference/deposit-flow.md](reference/deposit-flow.md).

## Typical flows

### Market overview

1. `lfi perpetuals markets --json`
2. Present symbol, mark price, funding where present.

### Depth + tape

1. `lfi perpetuals orderbook BTC --json`
2. `lfi perpetuals trades BTC --limit 20 --json`

### Positions for a known wallet

1. `lfi perpetuals positions 0xYourAddr --json`

### "My ..." auto-flow (CRITICAL — covers "我的", "my", "我自己")

**If the user says "我有什么永续持仓", "我的合约持仓", "my perp positions",
"我在 Hyperliquid 上挂了哪些单", "我永续盈亏", "show my fills" or any
first-person variant — DO NOT ask for a wallet address. Run this exact
sequence:**

1. **Check session**: `lfi status --json`
2. **If not authenticated**: `lfi login key --role AGENT --name "OpenClawAgent" --json`
3. **Fetch TEE wallet address**: `lfi whoami --json` → returns `evmAddress`
   (the user's TEE EVM address managed by the LiberFi server).
4. **Run the matching query** with the EVM address as the positional arg:
   - Positions: `lfi perpetuals positions <evmAddress> --json`
   - Open orders: `lfi perpetuals orders <evmAddress> --json`
   - Fill history: `lfi perpetuals fills <evmAddress> --limit 20 --json`
5. **Present** the result. If positions / orders / fills are empty, say so
   directly — do not retry with a different address; an empty result is the
   correct answer for a fresh TEE wallet.

The user does not know their EVM address — the LiberFi server holds the TEE
wallet. The skill must resolve "我" → TEE wallet via `whoami`, transparently.

### Place order (human-in-the-loop)

1. `lfi perpetuals order-prepare --user-address 0x… --symbol BTC --side long --order-type limit --amount 0.01 --price 95000 --json`
2. User signs returned `typedData` with their wallet (e.g. MetaMask `eth_signTypedData_v4`).
3. Build `SignedAction`: `action`, `nonce`, `signature` (0x), optional `vaultAddress` from prepare response.
4. **After explicit confirmation**: `lfi perpetuals order-submit --body '{"action":…,"nonce":…,"signature":"0x…"}' --json`

## API path reminder

All CLI calls hit **OpenAPI** paths under `/v1/perpetuals/…`, which the gateway proxies to **perpetuals-server** `/v1/…`. Configure the gateway with `UPSTREAM_PERPETUALS_SERVICE_BASE_URL` (default local example: `http://localhost:8083` — avoid colliding with openapi `:8080` and prediction `:8082`; run perpetuals-server with `SERVER_PORT=8083` when colocated).
