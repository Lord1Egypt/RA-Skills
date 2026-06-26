# First-Time Setup

Goal: scan account, set authorization defaults, done in 1 round.

## Step 1: Validate API Key

```bash
node {baseDir}/bin/earn-api.ts account
```

- Succeeds → key valid, earn permission OK
- Fails -2008 → tell user to check API key config
- Permission error → tell user which permissions are missing

Optional margin check:
```bash
node {baseDir}/bin/margin-api.ts account
```
- Succeeds → borrow-to-earn available
- Fails → skip borrow-to-earn, no problem

## Step 2: Scan Account

```bash
node {baseDir}/bin/earn-api.ts balance
node {baseDir}/bin/earn-api.ts positions --type flexible
node {baseDir}/bin/earn-api.ts positions --type locked
```

Use **Binance Spot skill** to get current prices for USDT valuation of each asset. Filter out dust (< 1 USDT).

## Step 3: Set Defaults (don't ask questions, calculate)

Derive from account scan:
- `main_holdings`: all non-dust assets from balance
- `single_amount_limit`: round down to nearest 100 of (total_value × 10%), minimum 100 USDT
- `daily_amount_limit`: round down to nearest 100 of (total_value × 20%), minimum 200 USDT
- `asset_whitelist`: same as main_holdings
- `allowed_operations`: `[subscribe, redeem]` (add `margin-borrow` if margin check passed)
- `confirmation_mode`: `confirm-first`

## Step 4: Present & Confirm (one screen)

```
I've scanned your Binance account:

📊 Holdings:
- BNB: 12.5 (~8,250 USDT)
- USDT: 3,200
- BTC: 0.02 (~1,960 USDT)
Total: ~13,410 USDT

📊 Existing Earn:
- BNB Flexible: 5.0 BNB (APY 0.05%)

🔧 Authorization defaults:
- Execute mode: confirm each time
- Single op limit: 1,300 USDT
- Daily limit: 2,600 USDT
- Assets: BNB, USDT, BTC
- Operations: subscribe, redeem, margin-borrow

Want to change anything? Or say "ok" to start.
```

## Step 5: Save & First Scan

```bash
mkdir -p ~/passive-income-claw
cp {baseDir}/memory-template.md ~/passive-income-claw/user-profile.md
node {baseDir}/bin/profile.ts set main_holdings "BNB, USDT, BTC"
node {baseDir}/bin/profile.ts set execution_enabled "true"
node {baseDir}/bin/profile.ts set confirmation_mode "confirm-first"
node {baseDir}/bin/profile.ts set single_amount_limit "1300 USDT"
node {baseDir}/bin/profile.ts set daily_amount_limit "2600 USDT"
node {baseDir}/bin/profile.ts set allowed_operations "[subscribe, redeem, margin-borrow]"
node {baseDir}/bin/profile.ts set asset_whitelist "[BNB, USDT, BTC]"
```

Then immediately run a full scan per `{baseDir}/scan.md` — this will show the first batch of strategies.

Auto-register cron:
```bash
openclaw cron add \
  --name "passive-income-scan" \
  --cron "0 1,5,9,13,17,21 * * *" \
  --message "Run passive income scan" \
  --session isolated
```

```
Done! Scanning every 4 hours. You'll get a push when there's a new opportunity.
```

## API Key Permissions

| Permission | Required |
|------------|---------|
| Read (balance / holdings / history) | ✅ Yes |
| Spot trading | ❌ Not needed |
| Earn operations | ✅ Yes |
| Margin | ✅ If borrow-to-earn wanted |
| Futures | ❌ Do not enable |
| Withdrawal | ❌ Never |
| IP whitelist | ✅ Bind to OpenClaw's running IP |
