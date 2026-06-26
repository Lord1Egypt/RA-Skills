# Scan Flow

Default behavior: scan ALL feasible strategies, calculate real numbers, sort by net yield, present everything. Don't filter by subjective preferences — show data, let user decide.

## Triggers

- Cron job (recommended: every 4 hours)
- User asks "what's available" / "scan" / "recommend"
- First scan after setup

## Flow

### 0. Daily Reset

```bash
node {baseDir}/bin/profile.ts reset-daily
```

### 1. Gather Data (parallel)

```bash
# Holdings
node {baseDir}/bin/earn-api.ts balance

# All earn products
node {baseDir}/bin/earn-api.ts list-flexible --size 50
node {baseDir}/bin/earn-api.ts list-locked --size 50

# Existing earn positions
node {baseDir}/bin/earn-api.ts positions --type flexible
node {baseDir}/bin/earn-api.ts positions --type locked

# Margin rates (if margin-borrow in allowed_operations)
node {baseDir}/bin/margin-api.ts interest-rate --assets USDT,BTC,ETH,BNB
node {baseDir}/bin/margin-api.ts account
```

Use **Binance Spot skill** for current prices (USDT valuation).

### 2. Generate ALL Candidate Strategies

For each earn product, evaluate every feasible path:

**Path A — Direct Earn**: user holds the required asset
- Feasibility: `balance[asset] > product.minPurchaseAmount`
- Net yield: product APY (no cost)
- Lock period: flexible (0) or fixed (N days)
- Risk: low (earn product risk only)

**Path B — Borrow-to-Earn**: user doesn't hold the asset but can borrow it
- Feasibility: `margin-borrow` in allowed_operations AND asset is borrowable AND `maxBorrowable > minPurchaseAmount`
- Earn APY: product APY
- Borrow cost: `hourlyInterestRate × 24 × 365` (annualized)
- Net yield: Earn APY − Borrow APY
- Collateral: user's current holdings
- Margin level impact: estimate post-borrow margin level
- Risk: medium-high (liquidation, variable borrow rate)

**Skip if**:
- Product is sold out (`isSoldOut: true` or `canPurchase: false`)
- Net yield for borrow path is negative

### 3. Score & Sort

For each candidate, compute a composite score:

```
score = net_yield
        - (lock_days > 0 ? 0.5 : 0)          // liquidity penalty
        - (path == "borrow" ? 1.0 : 0)        // complexity/risk penalty
        - (margin_level_after < 3.0 ? 2.0 : 0) // leverage risk penalty
```

Sort by score descending. Group into tiers:

| Tier | Criteria |
|------|----------|
| **Recommended** | score > 0, direct earn or borrow with net yield > 2% |
| **Possible** | score > 0 but low net yield or long lock |
| **Not worth it** | net yield < 1% or negative after costs |
| **Too risky** | margin level would drop below 2.0 |

### 4. Snapshot Comparison

```bash
echo '<candidates JSON>' | node {baseDir}/bin/snapshot.ts diff --threshold 0.5
```

- `has_changes: false` → no push, update scan time, end
- `has_changes: true` → continue

**push_frequency handling**:
- `every-4h` → push on every change (default)
- `daily` → at most once per day
- `important-only` → only new products or yield delta > 2x threshold

### 5. Generate Output

Present ALL tiers, not just "recommended". User sees the full picture.

```
📊 Passive Income Scan — [timestamp]
Holdings: BNB 12.5 (~8,250), USDT 3,200, BTC 0.02 (~1,960)

✅ Recommended:
1. USDT Flexible Earn — 4.2% APY, direct, withdraw anytime
2. BNB Flexible Earn — 3.8% APY, direct, withdraw anytime
3. USDT Locked 30d — 8.2% APY, direct, locked 30 days

💡 Possible (borrow-to-earn):
4. [borrow] USDT Locked 90d — earn 9.5% − borrow 3.2% = net 6.3%, locked 90d
   Collateral: BNB, margin level after: 4.1 (healthy)

⚠️ Not worth it:
5. BTC Locked 120d — 1.2% APY, long lock, low yield
6. [borrow] ETH Flexible — earn 2.1% − borrow 2.8% = net -0.7%

To execute: "buy #1" or "buy #1, 500 USDT"
```

### 6. Update Snapshot

```bash
echo '<all candidates JSON>' | node {baseDir}/bin/snapshot.ts update
node {baseDir}/bin/profile.ts set last_scan_time "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 7. Auto-Execute Check

```bash
node {baseDir}/bin/profile.ts get confirmation_mode
```

- `confirm-first` → flow ends, wait for user
- `auto` → execute only **Recommended** tier items:
  1. Run `auth-check.ts` for each
  2. Use **Binance Spot skill** for price conversion if needed
  3. Execute via `earn-api.ts` (or `margin-api.ts` + `earn-api.ts` for borrow path)
  4. Log via `log.ts`
  5. Send result notification
  6. If any fails, notify and continue to next

**Auto mode never executes "Possible", "Not worth it", or "Too risky" items.**
