# Gate Reference — Detailed Criteria & Thresholds

## Gate 1: Contract Safety

**Source:** GoPlus Security API + Chain RPC
**Behavior:** Instant kill on any critical finding

| Check | Threshold | Source Field | Action |
|-------|-----------|-------------|--------|
| Honeypot | `is_honeypot == "1"` | GoPlus | INSTANT FAIL |
| Mintable | `is_mintable == "1"` | GoPlus | FAIL |
| Ownership takeback | `can_take_back_ownership == "1"` | GoPlus | FAIL |
| Blacklist | `is_blacklisted == "1"` | GoPlus | FAIL |
| Slippage modifiable | `slippage_modifiable == "1"` | GoPlus | FAIL |
| Transfer pausable | `transfer_pausable == "1"` | GoPlus | FAIL |
| Sell tax > 5% | `sell_tax > 0.05` | GoPlus | FAIL |
| Tax asymmetry | `sell_tax > buy_tax + 0.03` | GoPlus | FAIL |
| Closed-source proxy | `is_proxy == "1" && is_open_source != "1"` | GoPlus | FAIL |

## Gate 2: Liquidity Structure

**Source:** DexScreener + GoPlus LP data
**Behavior:** Sequential checks, fail on first breach

| Check | Threshold | Action |
|-------|-----------|--------|
| No pairs found | `len(pairs) == 0` | FAIL |
| Total liquidity | `< $10,000` | FAIL |
| LP/market cap ratio | `< 5%` | FAIL |
| No LP locked | `locked_count == 0` | FAIL |
| 24h volume | `< $1,000` | FAIL |

## Gate 3: Wallet Behavior

**Source:** GoPlus holder data + DexScreener transactions
**Behavior:** Evaluate holder health and trading patterns

| Check | Threshold | Action |
|-------|-----------|--------|
| Holder count | `< 50` | FAIL |
| No 24h transactions | `buys + sells == 0` | FAIL |
| Sell pressure | `sells / total > 70%` | FAIL |
| Low activity | `total txns < 20` | FAIL |
| Hourly dump | `1h sells / total > 80% (when txns > 10)` | FAIL |

## Gate 4: Social Momentum (Agent-Driven)

**Source:** Agent browsing X/Twitter, Farcaster
**Behavior:** Agent investigates and assesses

| Signal | Assessment | Action |
|--------|-----------|--------|
| Bot activity | `> 60%` bot-like posts | FAIL |
| No discussion | Zero genuine posts found | FAIL |
| Shill-only | All posts are paid promotion | FAIL |
| Organic growth | Genuine community discussion | PASS |
| Influencer quality | Known, reputable voices | BONUS |

## Gate 5: Narrative Alignment (Agent-Driven)

**Source:** Agent web search and research
**Behavior:** Agent evaluates narrative fit

| Signal | Assessment | Action |
|--------|-----------|--------|
| Dead narrative | Narrative has peaked and declining | FAIL |
| No narrative | Token doesn't fit any current meta | FAIL |
| Latecomer | >20 competitors already established | FAIL |
| Growing narrative | Narrative gaining momentum | PASS |
| Early mover | First/second in emerging narrative | BONUS |

## Gate 6: Market Timing

**Source:** CoinGecko global + DefiLlama TVL/stablecoins
**Behavior:** Assess macro conditions

| Check | Threshold | Action |
|-------|-----------|--------|
| Market freefall | `24h change < -8%` | FAIL |
| Chain TVL decline (7d) | `> -15%` | FAIL |
| Chain TVL decline (30d) | `> -30%` | FAIL |
| BTC dominance | `> 65%` | WARNING |
| Multiple warnings | `>= 2 warnings` | WARN status |

## Gate 7: Cross-Validation

**Source:** DexScreener vs GeckoTerminal comparison
**Behavior:** Verify data consistency across sources

| Check | Threshold | Action |
|-------|-----------|--------|
| Both sources fail | Cannot fetch from either | FAIL |
| Price divergence | `> 10%` between sources | FAIL |
| Volume divergence | `> 50%` between sources | FAIL |
| One source unavailable | Single source only | WARN |
| Moderate price gap | `5-10%` divergence | WARNING logged |
