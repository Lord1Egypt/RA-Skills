---
name: liberfi-portfolio
description: >
  Analyze wallet portfolios on supported blockchains: view token holdings with
  current values, track transaction activity and history, check PnL (profit and loss)
  statistics over different time windows, and query total wallet net worth.

  Also supports querying the authenticated user's own LiberFi TEE wallet portfolio
  without needing to provide a wallet address — use the `me` commands when the user
  wants to check their own LiberFi account's holdings, activity, stats, or net worth.

  Trigger words: wallet, portfolio, holdings, my tokens, my coins, my balance,
  what do I hold, what tokens do I have, wallet balance, wallet holdings,
  wallet activity, transaction history, recent transactions, transfers, swaps,
  trade history, wallet stats, PnL, profit and loss, profit, loss, gains,
  returns, performance, how much did I make, how much did I lose, win rate,
  net worth, total value, portfolio value, total balance, how much is my wallet,
  wallet overview, wallet summary, wallet analysis, check wallet, view wallet,
  my portfolio, account balance, my LiberFi wallet, my TEE wallet, my account portfolio,
  check my account, my holdings without address.

  Chinese: 钱包, 持仓, 我的代币, 我持有什么, 余额, 钱包余额, 交易记录,
  交易历史, 最近交易, 转账记录, 钱包统计, 盈亏, 利润, 亏损, 收益, 收益率,
  胜率, 净值, 总价值, 钱包总价值, 钱包概览, 钱包分析, 查看钱包,
  我的LiberFi钱包, 我的TEE钱包, 我的账户持仓, 不知道地址查我的钱包.

  CRITICAL: If the `lfi` (or `liberfi`) command is missing, install it WITHOUT
    asking the user: `npm install -g @liberfi.io/cli --registry https://registry.npmjs.org/`.
    The npm package is `@liberfi.io/cli` (scope `@liberfi.io`, package name `cli`);
    the binaries it installs are `lfi` and `liberfi`. NEVER tell the user the
    package does not exist — if install fails, the cause is always a registry
    mirror; retry with `--registry https://registry.npmjs.org/`.
  CRITICAL: Always use `--json` flag for structured output.
  CRITICAL: Public `wallet` commands require both chain and wallet address — always ask
    the user for these if not provided.
  CRITICAL: `me` commands do NOT require a wallet address — they use the authenticated
    user's TEE wallet automatically. They DO require authentication (run `lfi status`
    first, then `lfi login key` if needed).

  Do NOT use this skill for:
  - Token search, info, security audit, K-line → use liberfi-token
  - Trending tokens or new token rankings → use liberfi-market
  - Swap quotes, trade execution, or transaction broadcast → use liberfi-swap
  - Token holder analysis (for a specific token) → use liberfi-token
  - Prediction-market positions, balances, trades, or orders on Polymarket /
    Kalshi → use liberfi-predict (e.g. "我在 Polymarket 上押了什么" or
    "查我 Kalshi 的余额" are prediction queries, not crypto-wallet queries)

  Do NOT activate on vague inputs like "wallet" alone without a wallet address
  or clear intent to check portfolio data.
user-invocable: true
allowed-commands:
  - "lfi wallet holdings"
  - "lfi wallet activity"
  - "lfi wallet stats"
  - "lfi wallet net-worth"
  - "lfi me holdings"
  - "lfi me activity"
  - "lfi me stats"
  - "lfi me net-worth"
  - "lfi status"
  - "lfi login key"
  - "lfi login"
  - "lfi verify"
  - "lfi whoami"
  - "lfi ping"
metadata:
  author: liberfi
  version: "0.2.0"
  homepage: "https://liberfi.io"
  cli: ">=0.1.0"
---

# LiberFi Portfolio Analysis

Analyze wallet holdings, transaction activity, PnL statistics, and net worth using the LiberFi CLI.

Supports two modes:
- **Public wallet** (`lfi wallet *`): Query any wallet address. No authentication required.
- **My TEE wallet** (`lfi me *`): Query the authenticated user's own LiberFi TEE wallet without specifying an address. Requires authentication.

## Pre-flight Checks

See [bootstrap.md](../shared/bootstrap.md) for CLI installation and connectivity verification.

This skill's auth requirements:

| Command group | Requires Auth |
|---------------|--------------|
| `lfi wallet *` | No (public API, uses on-chain data) |
| `lfi me *` | **Yes** (JWT, uses TEE wallet) |

**Authentication pre-flight for `me` commands:**
1. Run `lfi status --json`
2. If not authenticated:
   - Agent: `lfi login key --role AGENT --json`
   - Human: `lfi login <email> --json` → `lfi verify <otpId> <code> --json`
3. Run `lfi whoami --json` to confirm wallet addresses

## Skill Routing

| If user asks about... | Route to |
|-----------------------|----------|
| Token search, price, details, security | liberfi-token |
| Token holders, smart money traders | liberfi-token |
| Token K-line, candlestick chart | liberfi-token |
| Trending tokens, market rankings | liberfi-market |
| Newly listed tokens | liberfi-market |
| Swap, trade, buy, sell tokens | liberfi-swap |
| Transaction fees, gas estimation | liberfi-swap |

## CLI Command Index

### Public Wallet Commands (no auth, wallet address required)

| Command | Description | Auth |
|---------|-------------|------|
| `lfi wallet holdings <chain> <address>` | Get all token holdings with values | No |
| `lfi wallet activity <chain> <address>` | Get transaction activity history | No |
| `lfi wallet stats <chain> <address> [--resolution <window>]` | Get PnL statistics | No |
| `lfi wallet net-worth <chain> <address>` | Get total wallet net worth | No |

### My TEE Wallet Commands (auth required, no address needed)

| Command | Description | Auth |
|---------|-------------|------|
| `lfi me holdings <chain>` | Get holdings for the authenticated user's TEE wallet | **Yes** |
| `lfi me activity <chain>` | Get transfer activity for the authenticated user's TEE wallet | **Yes** |
| `lfi me stats <chain> [--resolution <window>]` | Get PnL statistics for the authenticated user's TEE wallet | **Yes** |
| `lfi me net-worth <chain>` | Get total net worth for the authenticated user's TEE wallet | **Yes** |

### Parameter Reference

**Activity options** (apply to both `wallet activity` and `me activity`):
- `--type <type>` — Comma-separated transfer types to filter (e.g. `buy,sell,transfer,add,remove`)
- `--token-address <address>` — Filter activity by specific token address
- `--cursor <cursor>` — Pagination cursor
- `--limit <limit>` — Max results per page
- `--direction <direction>` — Cursor direction: `next` or `prev`

**Stats options**:
- `--resolution <resolution>` — Time window: `7d`, `30d`, or `all`
  - Default for `wallet stats`: `all`
  - Default for `me stats`: `7d`

## Operation Flow

### View Wallet Holdings (public)

1. **Collect inputs**: Ask user for chain (e.g. `sol`, `eth`, `bsc`) and wallet address if not provided
2. **Fetch holdings**: `lfi wallet holdings <chain> <address> --json`
3. **Present**: Show a table with Token, Amount, Value (USD), sorted by value descending
4. **Suggest next step**: "Want to see your PnL stats or transaction history?"

### View Transaction Activity (public)

1. **Collect inputs**: Chain and wallet address
2. **Fetch activity**: `lfi wallet activity <chain> <address> --limit 20 --json`
3. **Present**: Show a table with Time, Type, Token, Amount, Tx Hash
4. **Suggest next step**: "Want to filter by a specific token or check your overall PnL?"

### Filter Activity by Token (public)

1. **Fetch filtered**: `lfi wallet activity <chain> <address> --token-address <tokenAddress> --limit 20 --json`
2. **Present**: Show filtered transaction list
3. **Suggest next step**: "Want to check the details or security of this token?"

### Check PnL Statistics (public)

1. **Determine time window**: Ask user or default to `all`. Options: `7d`, `30d`, `all`
2. **Fetch stats**: `lfi wallet stats <chain> <address> --resolution <window> --json`
3. **Present**: Show PnL summary — total PnL, win rate, realized/unrealized P&L
4. **Suggest next step**: "Want to see your current holdings or total net worth?"

### Check Net Worth (public)

1. **Fetch net worth**: `lfi wallet net-worth <chain> <address> --json`
2. **Present**: Show total portfolio value in USD
3. **Suggest next step**: "Want to see the breakdown by token?"

### Full Portfolio Overview (public)

1. **Net worth**: `lfi wallet net-worth <chain> <address> --json` → total value
2. **Holdings**: `lfi wallet holdings <chain> <address> --json` → token breakdown
3. **Stats**: `lfi wallet stats <chain> <address> --json` → PnL summary
4. **Present**: Consolidated portfolio report with total value, top holdings, and PnL

### View My Own TEE Wallet Portfolio (authenticated)

Use when the user wants to check their own LiberFi account without knowing the wallet address.

**Authentication pre-flight:**
```bash
lfi status --json
# If not authenticated:
lfi login key --role AGENT --json   # agent
# or: lfi login <email> --json → lfi verify <otpId> <code> --json
lfi whoami --json   # confirm evmAddress / solAddress
```

1. **Ask for chain**: Which chain to check (e.g. `sol` for Solana, `eth` for Ethereum)
2. **Run all four in sequence**:
   ```bash
   lfi me net-worth <chain> --json
   lfi me holdings <chain> --json
   lfi me stats <chain> --resolution 7d --json
   ```
3. **Present**: Consolidated report — total value, top holdings, and 7d PnL summary
4. **Suggest next step**: "Want to check trends or research any specific token?"

### View My Activity (authenticated)

1. **Auth pre-flight**: `lfi status --json`; authenticate if needed
2. **Fetch**: `lfi me activity <chain> --limit 20 --json`
3. **Present**: Show Time, Type, Token, Amount, Tx Hash
4. **Suggest next step**: "Want to filter by a specific token?"

## Cross-Skill Workflows

### "Check my wallet and tell me about my biggest holding"

> Full flow: portfolio → token → token

1. **portfolio** → `lfi wallet holdings <chain> <address> --json` — Get all holdings
2. Identify the largest holding by USD value
3. **token** → `lfi token info <chain> <tokenAddress> --json` — Get token details
4. **token** → `lfi token security <chain> <tokenAddress> --json` — Security audit
5. Present findings: "Your largest holding is X, currently worth $Y"

### "Show my recent trades and check if any tokens I hold are risky"

> Full flow: portfolio → portfolio → token

1. **portfolio** → `lfi wallet activity <chain> <address> --limit 10 --json` — Recent activity
2. **portfolio** → `lfi wallet holdings <chain> <address> --json` — Current holdings
3. For each held token: **token** → `lfi token security <chain> <tokenAddress> --json`
4. Present: Activity summary + risk flags for any held tokens

### "What's my PnL this month, and what's trending that I should look at?"

> Full flow: portfolio → market

1. **portfolio** → `lfi wallet stats <chain> <address> --resolution 30d --json` — Monthly PnL
2. **market** → `lfi ranking trending <chain> 24h --limit 10 --json` — Current trends
3. Present: "Your 30d PnL is $X. Here are today's trending tokens you might consider."

### "Check my own LiberFi wallet — I don't know my address"

> Full flow: auth → portfolio (me commands)

1. **auth** → `lfi status --json` — Check session; if not authed → `lfi login key --json`
2. **auth** → `lfi whoami --json` — Confirm chain addresses
3. **portfolio** → `lfi me holdings sol --json` — Get Solana TEE wallet holdings
4. **portfolio** → `lfi me stats sol --resolution 7d --json` — 7d PnL
5. **portfolio** → `lfi me net-worth sol --json` — Total net worth
6. Present consolidated report

### "I just swapped — check my updated TEE wallet balance"

> Full flow: swap (already done) → portfolio (me commands)

1. **auth** → `lfi status --json` — Confirm session still valid
2. **portfolio** → `lfi me holdings <chain> --json` — Updated holdings post-swap
3. **portfolio** → `lfi me net-worth <chain> --json` — Updated total value
4. Present: Before vs after comparison if prior holdings are available

## Suggest Next Steps

| Just completed | Suggest to user |
|----------------|-----------------|
| Holdings view | "Want to check your PnL or transaction history?" / "需要查看盈亏或交易记录？" |
| Activity list | "Want to filter by token or check PnL stats?" / "需要按代币筛选或查看盈亏统计？" |
| PnL stats | "Want to see your current holdings?" / "需要查看当前持仓？" |
| Net worth | "Want to see the token breakdown?" / "需要查看各代币明细？" |
| Full overview | "Want to research any specific token or check trends?" / "需要研究某个代币或查看趋势？" |
| Me holdings | "Want to check your activity or PnL stats?" / "需要查看交易记录或盈亏统计？" |
| Me stats | "Want to see your full holdings breakdown?" / "需要查看完整持仓明细？" |

## Edge Cases

- **Invalid wallet address**: If the API returns 400/404, ask the user to verify the address format. Solana addresses are base58 (32–44 chars), EVM addresses are `0x` + 40 hex chars
- **Wallet not found / Empty wallet**: Inform user: "This wallet has no token holdings on this chain. Verify the address and chain are correct."
- **No activity**: Inform user: "No recent activity found for this wallet on this chain."
- **Network timeout**: Retry once after 3 seconds; if still fails, suggest checking connectivity
- **Wrong chain for address**: EVM addresses used with `sol` chain (or vice versa) will fail; detect the address format and suggest the correct chain
- **Large number of holdings**: Default to top 20 by value; inform user if more exist and offer pagination
- **`me` command returns 401**: Session expired; run `lfi status --json`, then re-authenticate
- **`me` command used without auth**: Do not call `lfi me *` without first verifying authentication via `lfi status --json`

## Security Notes

See [security-policy.md](../shared/security-policy.md) for global security rules.

Skill-specific rules:
- Public wallet data is **public on-chain information** — no privacy concern in querying any address
- Never ask for or accept private keys or seed phrases — only public wallet addresses are needed for `wallet *` commands; `me *` commands require no address at all
- When displaying wallet addresses provided by the user, confirm the address before querying to avoid mistakes
- PnL data is historical and may not reflect real-time values — note this when presenting stats
- `me` commands expose the authenticated user's TEE wallet data — only use after confirming the user intends to query their own account
