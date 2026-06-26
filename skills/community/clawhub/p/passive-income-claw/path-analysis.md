# Asset Mismatch — Borrow-to-Earn Path

Trigger: user wants to participate in an earn opportunity but doesn't hold the required asset. Instead of selling current holdings, the system can borrow the target asset using current holdings as collateral.

## Step 1: Identify Opportunity

Determine:
- **Target earn product**: name, required asset, APY
- **User's current holdings**: from profile + `node {baseDir}/bin/earn-api.ts balance`
- **Gap**: which asset is needed

## Step 2: Check Feasibility

```bash
# Is the target asset borrowable?
node {baseDir}/bin/margin-api.ts asset-info --asset USDT

# What's the current borrow interest rate?
node {baseDir}/bin/margin-api.ts interest-rate --assets USDT

# How much can user borrow?
node {baseDir}/bin/margin-api.ts max-borrowable --asset USDT

# Current margin account health
node {baseDir}/bin/margin-api.ts account
```

If `borrowable: false` or `maxBorrowable: 0` → tell user this path is not available, end.

## Step 3: Calculate Net Yield

```
Earn APY:        8.2%
Borrow rate:     hourly rate × 24 × 365 = annualized borrow APY
Net yield:       Earn APY - Borrow APY

Example:
  Earn APY:      8.2%
  Borrow APY:    3.1% (hourly 0.000354%)
  Net yield:     5.1%
```

If net yield < 2% → tell user "spread too thin to justify borrowing risk", end. (Threshold: 2% minimum net yield for any borrow-to-earn recommendation.)

## Step 4: Assess Risk

From `margin-api.ts account`, check:
- **Current margin level**: higher is safer (>2.0 is comfortable, <1.5 is risky, <1.1 triggers liquidation)
- **Collateral value**: total collateral in USDT
- **Impact**: how much would this borrow reduce the margin level?

Present to user:

```
Borrow-to-Earn Analysis:

  Earn product:    USDT Locked 30d — 8.2% APY
  Borrow amount:   500 USDT
  Borrow rate:     3.1% APY (current hourly rate, may fluctuate)
  Net yield:       ~5.1% APY on 500 USDT ≈ 25.5 USDT/year

  Collateral:      Your BNB holdings
  Current margin level: 5.2 (healthy)
  After borrow:    ~4.1 (still healthy, liquidation at 1.1)

  Risks:
  - Borrow rate is variable — if it rises above earn rate, you lose money
  - If BNB price drops significantly, margin level falls → liquidation risk
  - Earn product is locked for 30 days — you can't repay early without redeeming

  Confirm? (reply "yes" or "cancel")
```

## Step 5: Execute (on user confirmation)

Authorization checks — both operations must be authorized:
```bash
node {baseDir}/bin/auth-check.ts --amount 500 --asset USDT --op margin-borrow
node {baseDir}/bin/auth-check.ts --amount 500 --asset USDT --op subscribe
```

Then execute the chain:

```bash
# 1. Borrow the target asset
node {baseDir}/bin/margin-api.ts borrow --asset USDT --amount 500

# 2. Subscribe to earn product with borrowed asset
node {baseDir}/bin/earn-api.ts subscribe-flexible --productId USDT001 --amount 500
# (or subscribe-locked for fixed products)
```

Both operations must succeed. If borrow succeeds but earn subscribe fails:
1. Query actual liability: `node {baseDir}/bin/margin-api.ts account` (find the USDT entry in the `assets` array)
2. Repay full amount (principal + any accrued interest): `node {baseDir}/bin/margin-api.ts repay --asset USDT --amount <borrowed + interest>`
3. If repay also fails → notify user immediately with outstanding debt details
4. Log the failed attempt

## Step 6: Log Result

```bash
node {baseDir}/bin/log.ts append \
  --op "margin-borrow+subscribe" \
  --product "USDT Locked 30d (borrowed)" \
  --amount 500 \
  --asset USDT \
  --result success
```

## Repayment Flow

When the user wants to exit the position or the earn product matures:

```bash
# 1. Redeem from earn
node {baseDir}/bin/earn-api.ts redeem-flexible --productId USDT001 --amount 500

# 2. Query live liability (interest accrues over time — never use a hardcoded amount)
node {baseDir}/bin/margin-api.ts account
# From JSON output, find the USDT entry in "assets" array → read "borrowed" and "interest" fields

# 3. Repay actual owed amount
node {baseDir}/bin/margin-api.ts repay --asset USDT --amount <borrowed + interest>

# 4. Log
node {baseDir}/bin/log.ts append --op "redeem+repay" --product "USDT Locked 30d" --amount <repaid> --asset USDT --result success
```

## Auto-Mode Behavior

When `confirmation_mode: auto` and `margin-borrow` is in `allowed_operations`:
- Scan detects opportunity where earn APY > borrow rate by at least 2%
- Net yield is positive
- Margin level after borrow stays above 2.0
- Amount stays within authorization limits
→ Execute automatically, send result notification

Conservative safety: **never auto-borrow if margin level would drop below 2.0 after the operation.**

## When NOT to Recommend

- User's `risk_preference` is `conservative` → do not suggest borrowing
- Net yield < 2% → spread too thin to justify risk
- Margin level would drop below 2.0 → too risky
- Borrow rate is volatile (changed >50% in past 7 days) → warn and suggest monitoring
