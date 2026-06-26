---
name: paradex-vault-intelligence
description: >
  Vault discovery, comparison, and analytics for Paradex vaults. Ranks vaults by
  risk-adjusted returns, analyzes operator track records, monitors TVL changes,
  and recommends vaults based on user risk profile — all by orchestrating the
  Paradex MCP vault tools (vaults, vault_summary, vault_positions, vault_balance,
  vault_account_summary, vault_transfers).
  Use this skill whenever the user asks about Paradex vaults, wants to find the best
  vaults, compare vault performance, understand vault risks, check a vault's positions
  or strategy, or asks "where should I deposit", "which vaults are performing well",
  "show me vault analytics", "vault ROI", "vault drawdown", or anything related to
  Paradex vault investing and passive income. Also trigger for "yield", "earn", or
  "passive" in a Paradex context.
---

# Paradex Vault Intelligence

Turns raw vault data from Paradex MCP into investment-grade vault analytics.
Helps users discover, compare, and monitor vaults for passive income strategies.

## Available MCP Tools (data sources)

| Tool | What it gives you | Key params |
|---|---|---|
| `paradex_vaults` | Vault config, owner, status, kind | vault_address, jmespath_filter |
| `paradex_vault_summary` | Performance metrics (ROI, PnL, drawdown, volume, TVL) | vault_address, jmespath_filter |
| `paradex_vault_positions` | Current open positions | vault_address |
| `paradex_vault_balance` | Available/locked/total balance | vault_address |
| `paradex_vault_account_summary` | Account health, margin, exposure | vault_address |
| `paradex_vault_transfers` | Deposit/withdrawal history | vault_address |

## Capabilities

### 1. Vault Discovery & Screening

Use `paradex_vault_summary` with JMESPath to screen the full vault universe:

**By performance:**
```
# Top 5 by total ROI
"sort_by([*], &to_number(total_roi))[-5:]"

# Profitable in last 7 days
"[?to_number(roi_7d) > `0`]"

# Best 30-day performers
"sort_by([*], &to_number(roi_30d))[-10:]"
```

**By risk:**
```
# Lowest max drawdown (safer vaults)
"sort_by([*], &to_number(max_drawdown))[:5]"

# Low recent drawdown + positive returns
"[?to_number(max_drawdown_30d) < `0.05` && to_number(roi_30d) > `0`]"
```

**By size/activity:**
```
# Largest by TVL
"reverse(sort_by([*], &to_number(tvl)))"

# Most active by 24h volume
"reverse(sort_by([*], &to_number(volume_24h)))"

# Most depositors (social proof)
"reverse(sort_by([*], &num_depositors))"
```

### 2. Vault Deep Dive

For a specific vault, gather comprehensive data:

1. **`paradex_vaults`** — get config: owner, kind, status, creation details
2. **`paradex_vault_summary`** — performance: ROI (24h/7d/30d/total), PnL, drawdowns, volume, TVL, token price
3. **`paradex_vault_positions`** — current holdings: which markets, sizes, unrealized PnL
4. **`paradex_vault_account_summary`** — account health: margin usage, leverage, exposure
5. **`paradex_vault_balance`** — cash position: available vs. locked
6. **`paradex_vault_transfers`** — fund flows: deposit/withdrawal patterns

### 3. Vault Comparison

When comparing 2+ vaults, build a comparison matrix:

| Metric | Vault A | Vault B | Better |
|---|---|---|---|
| Total ROI | X% | Y% | ✓ higher |
| 30d ROI | X% | Y% | ✓ higher |
| Max Drawdown | X% | Y% | ✓ lower |
| Sharpe-like ratio | ROI/DD | ROI/DD | ✓ higher |
| TVL | $X | $Y | context-dependent |
| # Depositors | N | M | ✓ higher (social proof) |
| 24h Volume | $X | $Y | ✓ higher (activity) |
| Position count | N | M | context-dependent |

**Risk-adjusted ranking:**
Compute a simple Sharpe-like ratio: `total_roi / max_drawdown` (higher = better risk-adjusted returns).
For vaults with zero drawdown, use total_roi alone but flag as "insufficient drawdown history."

### 4. Vault Risk Assessment

For each vault, assess and report:

- **Drawdown risk**: max_drawdown vs. max_drawdown_30d — is drawdown getting worse?
- **Concentration risk**: from positions — how many markets, what % of exposure is in largest position?
- **Leverage risk**: from account_summary — current leverage vs. available margin
- **Liquidity risk**: from TVL + transfers — is TVL stable, growing, or declining?
- **Operator activity**: from volume — is the vault actively trading or dormant?

**Risk score (1-5):**
- 1 (Low): Low drawdown, diversified positions, moderate leverage, stable/growing TVL
- 3 (Medium): Some drawdown history, concentrated in 2-3 markets, moderate leverage
- 5 (High): Large drawdowns, single-market concentration, high leverage, declining TVL

### 5. Vault Monitoring & Alerts

When asked to monitor a vault, check for:

- ROI dropping below a threshold
- Drawdown exceeding user-defined limit
- TVL declining (depositor exodus)
- Position concentration changing significantly
- New large positions opened (strategy shift)

### 6. Vault Recommendation Engine

When a user asks "which vault should I deposit in?", gather their preferences:

**Risk tolerance:**
- Conservative: prioritize low drawdown, stable returns, high TVL, many depositors
- Moderate: balance ROI and drawdown, accept some concentration
- Aggressive: prioritize highest ROI, accept higher drawdown and concentration

**Time horizon:**
- Short-term: weight roi_24h and roi_7d more heavily
- Medium-term: weight roi_30d and last_month_return
- Long-term: weight total_roi and max_drawdown

Then screen, score, and present top 3-5 vaults with reasoning.

## Output Format

### Vault Screening Results
```
## Paradex Vault Screening — [criteria]

Found N vaults matching criteria. Top picks:

### 1. [Vault Name/Address]
- ROI: 24h X% | 7d X% | 30d X% | Total X%
- Risk: Max DD X% | 30d DD X%
- Size: TVL $X | Depositors: N
- Activity: 24h Vol $X
- Risk Score: X/5

[1-sentence take on this vault]
```

### Vault Deep Dive
```
## Vault Analysis — [address]

### Performance
[ROI table across timeframes]

### Current Positions
[Position breakdown with market, size, unrealized PnL]

### Account Health
[Margin usage, leverage, available capacity]

### Risk Assessment
[Risk score with reasoning]

### Fund Flows
[Recent deposit/withdrawal trends]
```

## Important Caveats

- Past vault performance does not guarantee future results — state this clearly
- Vault token price can decline — depositors can lose money
- Withdrawal lockup periods apply — mention the vault's specific lockup
- This is analysis and screening, not investment advice
- Vault operator strategies are private — positions give clues but not full picture
- Small TVL vaults may have inflated ROI percentages from small base effects

See [scoring.md](references/scoring.md) for detailed risk scoring methodology and JMESPath query cookbook.
