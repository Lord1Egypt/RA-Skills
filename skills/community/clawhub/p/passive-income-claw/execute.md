# Execution Flow

Execution is a standalone entry point, fully decoupled from the scan flow.

## Triggers

1. **User command**: "buy #1" / "execute" / "subscribe 500 USDT to BNB flexible"
2. **Auto mode**: when `confirmation_mode: auto` in user-profile.md, execution runs immediately after scan

## Step 0: Daily Reset

```bash
node {baseDir}/bin/profile.ts reset-daily
```

Resets `today_executed_amount` if the date has changed. Safe to call multiple times per day.

## Step 1: Parse Intent

Extract from user message:
- Operation type: subscribe / redeem
- Target product: name or number (matched against last push or snapshot)
- Amount: user specifies in USDT equivalent

If target product cannot be determined, show the most recent pushed candidates for the user to choose.

**If amount is not specified**, suggest one instead of asking:
1. Read `single_amount_limit` from profile
2. Query available balance: `node {baseDir}/bin/earn-api.ts balance`
3. Suggest: min(single_amount_limit, available_balance for that asset), rounded down
4. Example: "I'll subscribe 500 USDT (your single op limit). OK?"

### Amount Conversion

When the product asset is not USDT, convert before calling the API:

Use the **Binance Spot skill** to get the current price for the trading pair (e.g. BNBUSDT), then calculate the asset amount: `amount_in_asset = usdt_amount / price`.

Use the USDT amount for authorization checks. Use the converted asset amount for the API call.
Show both in confirmation: "500 USDT ≈ 0.83 BNB at current price"

## Step 2: Authorization Check

```bash
node {baseDir}/bin/auth-check.ts --amount 500 --asset BNB --op subscribe
```

Returns JSON:
- `{"pass": true, ...}` → proceed
- `{"pass": false, "check": N, "reason": "..."}` → stop, show the reason to user, do not execute

**On any failure: stop, show the reason, do not execute.**

## Step 3: Confirmation (when confirmation_mode = confirm-first)

Show operation summary and wait:

```
Ready to execute:
- Operation: [Subscribe / Redeem] [Product Name]
- Amount: [amount] USDT (≈ [converted] [asset])
- Expected APY: [X.X%] (actual returns may vary)
- Risk note: [product risk description]

Confirm? (reply "yes" or "cancel")
```

If user replies "cancel" — abort, do not log.

## Step 4: Execute Operation

Read `productId` / `projectId` from snapshot:
```bash
node {baseDir}/bin/snapshot.ts read
# Parse the JSON output to find the target product by name in the "products" array
```

### 4a. Direct Earn (subscribe / redeem)

Amount is in asset quantity after conversion:

```bash
# Subscribe flexible
node {baseDir}/bin/earn-api.ts subscribe-flexible --productId BNB001 --amount 0.83

# Redeem flexible
node {baseDir}/bin/earn-api.ts redeem-flexible --productId BNB001 --amount 0.83

# Subscribe locked
node {baseDir}/bin/earn-api.ts subscribe-locked --projectId USDT30D --amount 500

# Redeem locked (query position first)
node {baseDir}/bin/earn-api.ts positions --type locked --asset USDT  # get positionId
node {baseDir}/bin/earn-api.ts redeem-locked --positionId 12345
```

### 4b. Borrow-to-Earn (margin-borrow)

When the user doesn't hold the required asset but wants to borrow against collateral. See `{baseDir}/path-analysis.md` for the full analysis flow.

**Pre-execution safety checks** (must pass even if scan already checked — conditions may have changed):
```bash
# Re-check margin level
node {baseDir}/bin/margin-api.ts account  # marginLevel must be > 2.0 after borrow

# Re-check net yield is still positive
node {baseDir}/bin/margin-api.ts interest-rate --assets USDT
# Annualize: hourly_rate * 24 * 365. Earn APY - borrow APY must be > 0
```

If margin level would drop below 2.0 or net yield is no longer positive → abort and notify user.

**Dual auth check** — both borrow and subscribe must be authorized:
```bash
node {baseDir}/bin/auth-check.ts --amount 500 --asset USDT --op margin-borrow
node {baseDir}/bin/auth-check.ts --amount 500 --asset USDT --op subscribe
```

Execute as a two-step chain — both must succeed:

```bash
# Step 1: Borrow
node {baseDir}/bin/margin-api.ts borrow --asset USDT --amount 500

# Step 2: Subscribe to earn
node {baseDir}/bin/earn-api.ts subscribe-flexible --productId USDT001 --amount 500
```

**Rollback**: If borrow succeeds but earn subscribe fails, immediately repay. Query live liability to include any accrued interest:
```bash
# Get actual amount owed (principal + interest)
node {baseDir}/bin/margin-api.ts account
# From the JSON output, find the asset entry where asset == "USDT" and read borrowed + interest
# Repay full amount
node {baseDir}/bin/margin-api.ts repay --asset USDT --amount <borrowed + interest>
```

If rollback repay also fails → **notify user immediately** with the outstanding debt details. Do not silently swallow the error.

For repayment (when earn matures or user exits):
```bash
# 1. Redeem from earn
node {baseDir}/bin/earn-api.ts redeem-flexible --productId USDT001 --amount 500

# 2. Query live liability (NOT a hardcoded amount — interest accrues over time)
node {baseDir}/bin/margin-api.ts account
# From the JSON output, find the asset entry where asset == "USDT" and read borrowed + interest

# 3. Repay actual owed amount
node {baseDir}/bin/margin-api.ts repay --asset USDT --amount <borrowed + interest>
```

## Step 5: Handle Result

Parse the JSON response. On success, proceed to Step 6. On error, interpret the error code per `binance-earn/SKILL.md` error table, notify user, do not auto-retry.

**Success notification format:**
```
✅ Executed successfully
Operation: [Subscribe / Redeem] [Product Name]
Amount: [amount] USDT (≈ [converted] [asset])
Time: [timestamp]
Today's total executed: [cumulative] USDT
```

## Step 6: Log Result

```bash
node {baseDir}/bin/log.ts append \
  --op subscribe \
  --product "BNB Flexible Earn" \
  --amount 500 \
  --asset USDT \
  --result success
```

This does three things:
- Appends to `~/passive-income-claw/execution-log.md`
- Updates `today_executed_amount` in `user-profile.md` (only on success)
- Updates `last_execution_time` in `user-profile.md`

For failed operations, pass the error as `--result`:
```bash
node {baseDir}/bin/log.ts append --op subscribe --product "..." --amount 500 --asset USDT --result "Quota full (-6014)"
```

**In auto mode, the Step 5 success notification is always sent and cannot be disabled.**
