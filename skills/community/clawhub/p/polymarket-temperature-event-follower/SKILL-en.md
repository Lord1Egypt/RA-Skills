# SkillPay Weather Sniper / Weather Event Trading Bot

**Automated trading bot for Polymarket's weather event markets**

---

## 📋 Table of Contents

1. [Project Overview](#1)
2. [Quick Start (5 min)](#2)
3. [Preparation](#3)
4. [API Key Tutorial](#4)
5. [Configuration Details (.env)](#5)
6. [Code Parameters Reference](#6)
7. [Launch Guide](#7)
8. [Security Best Practices](#8)
9. [Troubleshooting](#9)
10. [FAQ](#10)

---

<a name="1"></a>
## 1. Project Overview / 项目概述

### 1.1 What is this? / 这是什么？

This is an automated trading bot for trading **weather event** contracts on the **Polymarket** prediction market platform.

**Core Features**:
- ✅ Real-time scanning of weather markets across 33 global cities
- ✅ Automatic buying of "today's high temperature exceeds threshold" contracts during the forecast certainty window (10:00-14:00)
- ✅ Integrated SkillPay per-call billing (0.01 USDT deducted per successful order)
- ✅ Exception tolerance: network retries, balance checks, slippage protection
- ✅ Complete logging and state persistence

### 1.2 Who is this for? / 适合谁用？

- Traders interested in weather prediction markets
- Developers wanting to automate trading strategies
- Beginners learning Polymarket API and prediction markets

### 1.3 Core Strategy / 核心策略

```
Assumption: Daily maximum temperature typically occurs between 14:00-15:00 (meteorological principle)
Logic:
  1. After 10:00, official temperature forecasts have been released, market uncertainty reduced
  2. When YES token price is below 0.35, consider market underestimating "high temp" probability
  3. Buy with fixed amount (default $1.0), wait for price to rise as temperature becomes certain
  4. Can either sell after price increase, or hold to settlement (auto-settles at $1.0 or $0.0)
```

---

<a name="2"></a>
## 2. Quick Start (5 min) / 快速开始（5分钟）

### 2.1 Prerequisites / 前置条件

- ✅ Python 3.9+ (recommended 3.10-3.12)
- ✅ Registered [Polymarket](https://polymarket.com) account
- ✅ Basic command line skills

### 2.2 One-Command Setup / 一键启动脚本

```bash
# 1. Clone/enter project directory (you're already here)
cd C:\Users\19154\Desktop\skill

# 2. Install dependencies (takes ~2 minutes)
pip install -r requirements.txt

# 3. Copy environment template
copy .env.example .env
# Then edit .env file and fill in your keys (see Section 4)

# 4. Test run (simulation mode, no real money)
python sniper.py --dry-run --once

# 5. If you see scan output, installation successful!
# 6. Real trading (caution!)
python sniper.py --live --once
```

---

<a name="3"></a>
## 3. Preparation / 准备工作

### 3.1 Environment Check / 环境检查

```bash
# Check Python version (needs 3.9+)
python --version
# Expected: Python 3.10.x or 3.11.x or 3.12.x

# Check pip
pip --version
```

### 3.2 Virtual Environment (Optional but Recommended) / 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Dependencies List / 依赖列表

Create `requirements.txt` file (if not exists):

```
python-dotenv>=1.0.0
requests>=2.31.0
aiohttp>=3.9.0
pytz>=2024.1
eth-account>=0.11.0
py-clob-client>=0.2.0  # Polymarket official client (live trading required)
```

Install:
```bash
pip install -r requirements.txt
```

---

<a name="4"></a>
## 4. API Key Tutorial / API 密钥获取教程

### 4.1 Polymarket Credentials / Polymarket 凭证

#### Step 1: Export Wallet (EOA and Proxy)

1. Visit [Polymarket Settings](https://polymarket.com/settings)
2. Connect your MetaMask wallet to Polymarket homepage
3. You need the following information:

| Field | Description | Where to get |
|-------|-------------|--------------|
| `PRIVATE_KEY` | Your EOA wallet private key (**SECRET!**) | MetaMask Export Private Key (NOT seed phrase) |
| `PROXY_WALLET` | Polymarket proxy wallet address | Settings page "Wallet Address" |
| `POLY_API_KEY` | L2 API Key | Get after running command (see below) |
| `POLY_API_SECRET` | L2 API Secret | Get after running command |
| `POLY_API_PASSPHRASE` | L2 password | Get after running command |

#### Step 2: Generate Private Key (MetaMask)

1. Open MetaMask extension
2. Select account → More → "Account details"
3. Click "Export Private Key"
4. Enter password to confirm
5. Copy the 64-character hex string starting with `0x`

⚠️ **Security Warning**:
- Private key = full control! Anyone with it can transfer all assets
- Never upload private key to GitHub, cloud storage
- Recommended: use a **separate wallet** for trading only, don't store large amounts

#### Step 3: Determine `SIGNER_TYPE`

- If `PRIVATE_KEY` belongs to regular EOA wallet → `SIGNER_TYPE = "2"`
- If using Gnosis Safe multisig → `SIGNER_TYPE = "2"` (recommended)

Most users choose `"0"` or `"2"`.

**Important**: Some users with email-registered Polymarket accounts may use `SIGNER_TYPE=1`. Check your account type in Polymarket Settings.

---

#### Step 4: Get L2 Credentials

Run this command in the project directory:

```bash
python sniper.py --live --once
```

The code will automatically derive L2 API credentials from your PRIVATE_KEY and display them:

```
[AUTH] L2 Credentials derived successfully:
  POLY_API_KEY=pk_live_xxxxxxxxxxxx
  POLY_API_SECRET=sk_live_xxxxxxxxxxxx
  POLY_API_PASSPHRASE=your_passphrase_here
```

Copy these three values into your `.env` file.

---

### 4.2 SkillPay / SkillPay 计费

**Note**:
- This is a per-call billing service, deducting **0.01 USDT** for each successful order
- If balance is insufficient, order will fail (system shows recharge link)
- Minimum recharge amount: **8 USDT** (800 calls worth)

**Setup**:

1. Log in to [SkillPay Dashboard](https://skillpay.me/dashboard)
2. Go to "Integration" or "API" page
3. Copy your `API Key` (starts with `sk_`)
4. Copy `SKILL_ID` (usually fixed: `e56f2a83-819c-4e43-a457-5442ebba0098`)
5. Add these to `.env`

**Recharge**:
- Minimum 8 USDT per recharge
- Your `SKILLPAY_USER_ID` should be the wallet address you've verified with SkillPay
- Monitor balance via dashboard or bot logs

---

### 4.3 userId / User ID

`SKILLPAY_USER_ID`: This is your wallet address (the one that holds funds on SkillPay).

Usually it's the same as `PROXY_WALLET`. Example:
```
SKILLPAY_USER_ID=0x1234567890123456789012345678901234567890
```

---

<a name="5"></a>
## 5. Configuration Details / 配置文件详解

All configuration is managed via **environment variables** (`.env` file).

### 5.1 Create `.env` File

Create `.env` in project root:

```ini
# ============================================
# Required: Polymarket Authentication
# ============================================
PRIVATE_KEY=0xsk_your_private_key_here_64_hex_chars
PROXY_WALLET=0x1234567890123456789012345678901234567890
POLY_API_KEY=pk_live_xxxxxxxxxxxxxxxxxxxx
POLY_API_SECRET=sk_live_xxxxxxxxxxxxxxxxxxxx
POLY_API_PASSPHRASE=your_passphrase_here
SIGNER_TYPE=1  # 1=email account, 2=MetaMask registered account

# ============================================
# Trading Parameters (recommended defaults)
# ============================================
TRADE_AMOUNT_USD=1.0          # Order size in USD
MIN_ORDERBOOK_SIZE=1.0        # Minimum orderbook depth (liquidity filter)
SLIPPAGE_TOLERANCE=0.15       # Slippage tolerance (15%)
ENTRY_THRESHOLD=0.35          # Entry threshold (buy only if YES token < 0.35)
MAX_COST_PER_TRADE=1.2        # Max cost per trade (skip if exceeded)

# ============================================
# Time Windows (Local Time, UTC+8)
# ============================================
MONITOR_START_HOUR=9          # Monitoring start (hour, decimal)
MONITOR_END_HOUR=9.9167       # Monitoring end (9:55 = 9 + 55/60 = 9.9167)
FALLBACK_START_HOUR=10        # Fallback start time
FALLBACK_WINDOW_MINUTES=5     # Fallback window length (minutes)

# ============================================
# Execution Intervals (seconds)
# ============================================
CHECK_INTERVAL=300            # Scan interval (300 sec = 5 minutes)
REPORT_INTERVAL=240           # Report interval (240 sec = 4 minutes)

# ============================================
# Caching & Retry
# ============================================
CACHE_TTL=3600                # General cache TTL (1 hour)
GAMMA_CACHE_TTL=300           # Gamma API cache (5 minutes)
CLOB_CACHE_TTL=30             # CLOB orderbook cache (30 seconds)
MAX_CONCURRENT_REQUESTS=50    # Max concurrent requests
REQUEST_DELAY=0.05            # Min delay between requests (seconds)
MAX_RETRIES=3                 # Max retry count for network failures
RETRY_DELAY=1.0               # Retry delay (seconds)

# ============================================
# File Paths
# ============================================
STATE_FILE=state.json         # State file (positions, trade history)
CACHE_DIR=cache               # Cache directory
```

---

### 5.2 Parameter Reference / 参数详细说明

#### 5.2.1 Authentication / 认证参数

| Parameter | Type | Required | Description | Example | Recommended |
|-----------|------|----------|-------------|---------|-------------|
| `PRIVATE_KEY` | string | ✅ | EOA wallet private key (hexadecimal, `0x` prefix) | `0xabc123...` | Use **dedicated wallet**, not main wallet |
| `PROXY_WALLET` | string | ✅ | Polymarket proxy wallet address | `0x1234...` | Should match PRIVATE_KEY holder |
| `POLY_API_KEY` | string | ✅ | L2 API Key (`pk_` or `sk_` prefix) | `pk_live_xxx` | Create from Settings → API Keys |
| `POLY_API_SECRET` | string | ✅ | L2 API Secret | `sk_live_xxx` | Same as above |
| `POLY_API_PASSPHRASE` | string | ✅ | Password set when creating API key | `myPass123` | Remember it, won't show again |
| `SIGNER_TYPE` | int | ✅ | Signer type: `1`=email, `2`=MetaMask/Gnosis Safe | `0` or `2` | Regular wallet: `2` (or `1` for email accounts) |

#### 5.2.2 Trading Parameters / 交易参数

| Parameter | Type | Default | Description | Recommended | Risk Note |
|-----------|------|---------|-------------|-------------|-----------|
| `TRADE_AMOUNT_USD` | float | `1.0` | Target order size in USD. System auto-calculates shares | `0.5` - `5.0` | Higher = higher potential gain/loss |
| `MIN_ORDERBOOK_SIZE` | float | `1.0` | Minimum orderbook depth (needs at least $1.0 liquidity) | `1.0` | Too low = severe slippage |
| `SLIPPAGE_TOLERANCE` | float | `0.15` (15%) | Max acceptable slippage. Skip if best_ask > expected × (1 + slippage) | `0.05` - `0.20` | Conservative: 5%, Aggressive: 20% |
| `ENTRY_THRESHOLD` | float | `0.35` | Entry threshold. Buy only if YES token price < this | `0.30` - `0.50` | Too low = miss opportunities; too high = overpay |
| `MAX_COST_PER_TRADE` | float | `1.2` | Max cost per trade in USD. Skip if actual cost > this | `1.5` - `2.0` | Prevents extreme slippage losses |

**Formula Example**:
```
Assume TRADE_AMOUNT_USD = 1.0, best_ask = 0.5
Target shares = 1.0 / 0.5 = 2.0 shares
Actual cost = 0.5 × 2.0 = $1.0 OK

Assume best_ask = 0.6, but max_price = 0.6 × 1.15 = 0.69
If 0.6 < 0.69 → can buy
If 0.7 > 0.69 → skip (excessive slippage)
```

#### 5.2.3 Time Windows / 时间窗口

| Parameter | Type | Default | Description | Calculation |
|-----------|------|---------|-------------|-------------|
| `MONITOR_START_HOUR` | float | `9` | Monitoring start time (hour) | `9` = 09:00 |
| `MONITOR_END_HOUR` | float | `9.9167` | Monitoring end time | `9 + 55/60 = 9.9167` = 09:55 |
| `FALLBACK_START_HOUR` | float | `10` | Fallback start time | `10` = 10:00 |
| `FALLBACK_WINDOW_MINUTES` | int | `5` | Fallback window length | 10:00-10:04 |

**Time Logic**:
- 09:00-09:55: Normal scan window (today's markets)
- 10:00-10:04: Fallback forced-buy window (for unpositioned cities)
- 09:55-10:00: Gap period, no scanning

**Why these settings**:
- Meteorological agencies typically release daily forecasts at 08:00-09:00
- After 09:00 market has digested information, uncertainty reduced
- 10:00 is last buy opportunity, 4 hours before 14:00 peak temperature
- Fallback window is short to avoid duplicate orders

#### 5.2.4 Execution Frequency / 执行频率

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `CHECK_INTERVAL` | int | `300` | Scan cycle (seconds), checks market every 5 minutes |
| `REPORT_INTERVAL` | int | `240` | Status report cycle (seconds), prints positions/PnL every 4 minutes |

**Recommendations**:
- Testing: `CHECK_INTERVAL=60` (every minute) to see effects quickly
- Production: `CHECK_INTERVAL=300` (5 minutes) to avoid API rate limits

#### 5.2.5 Caching & Retry / 缓存与重试

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `CACHE_TTL` | int | `3600` | General cache TTL (seconds), 1 hour |
| `GAMMA_CACHE_TTL` | int | `300` | Gamma Events API cache (5 minutes) |
| `CLOB_CACHE_TTL` | int | `30` | CLOB orderbook cache (30 seconds) |
| `MAX_CONCURRENT_REQUESTS` | int | `50` | Max concurrent requests (async) |
| `REQUEST_DELAY` | float | `0.05` | Min delay between requests (seconds), prevents rate limiting |
| `MAX_RETRIES` | int | `3` | Max retry count for network failures |
| `RETRY_DELAY` | float | `1.0` | Retry delay (seconds), exponential backoff |

#### 5.2.6 File Paths / 文件路径

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `STATE_FILE` | string | `state.json` | State file (positions, trade history, statistics) |
| `CACHE_DIR` | string | `cache` | Cache directory (stores API responses, auto-created) |

---

<a name="6"></a>
## 6. Code Parameters Reference (sniper.py Constants)

Besides `.env` configuration, some **hard-coded constants** in code need understanding:

### 6.1 Weather-related Constants

```python
# City list (33 cities)
CITY_SLUGS = [
    "taipei", "seoul", "shanghai", "shenzhen", "wuhan", "beijing", "chongqing",
    "tokyo", "singapore", "hong-kong", "tel-aviv", "lucknow",
    "london", "warsaw", "paris", "milan", "madrid", "munich", "ankara",
    "atlanta", "nyc", "toronto", "miami", "chicago", "dallas", "seattle",
    "wellington", "buenos-aires", "sao-paulo",
    "denver", "houston", "austin", "san-francisco",
]

# Timezone mapping (auto-converts local time to UTC)
TIMEZONES = {
    "nyc": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "london": "Europe/London",
    # ... 33 timezone definitions total
}
```

**To modify cities**: Edit `CITY_SLUGS` list directly.

### 6.2 API Endpoints (usually no changes needed)

```python
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"
BILLING_URL = "https://skillpay.me/api/v1/billing"
```

---

<a name="7"></a>
## 7. Launch Guide / 启动指南

### 7.1 CLI Arguments / 命令行参数

```bash
python sniper.py [OPTIONS]

Options:
  --dry-run          Scan only, no real orders (default mode)
  --once             Run one scan cycle then exit (for debugging)
  --status           Show current positions and statistics
  --live             Enable real trading (requires all API credentials configured)
```

### 7.2 Launch Sequence / 启动流程

#### Scenario 1: First-time Test (Highly Recommended)

```bash
# 1. Ensure .env is configured
# 2. Run simulation mode (no money, no orders)
python sniper.py --dry-run --once

# Expected output:
# [AUTH] Loaded credentials...
# [SCAN] Starting scan...
# [SCAN] Tradeable in monitor window: X
# [BUY] Triggered: ... (if trigger conditions met)
# [DRY] Would buy 1 share @ $0.45 (max: $0.52)
# [OK] State saved, exiting.
```

**Verification checklist**:
- ✅ No errors
- ✅ See `[SCAN]` logs
- ✅ If market conditions met, see `[BUY] Triggered` and `[DRY] Would buy...`
- ✅ Final `[OK] State saved, exiting.`

#### Scenario 2: Check Current Status

```bash
python sniper.py --status
```

Sample output:
```
Positions:
  - tokyo_2026-03-26: entry_price=0.45, shares=2.22, PnL=$0.12
  - london_2026-03-26: entry_price=0.52, shares=1.92, PnL=-$0.08

Stats:
  Total trades: 5
  Total PnL: $0.45
  Billing cost: 0.05 USDT
```

#### Scenario 3: Production Run
Before that, don't forget to deposit funds into the Polymarket web interface. Simply click the "Deposit" button to proceed.
```bash
# Method A: Foreground (for testing)
python sniper.py --live --once

# Method B: Background daemon (recommended)
# Windows (using start)
start /B python sniper.py --live

# macOS/Linux (using screen/tmux)
screen -S weather_sniper
python sniper.py --live
# Press Ctrl+A, D to detach
```

**Monitor logs**:
```bash
# Real-time view
tail -f sniper.log  # if configured
# Or add FileHandler in code
```

---

<a name="8"></a>
## 8. Security Best Practices / 安全建议

### 8.1 Private Key Management / 私钥管理

| Approach | Rating | Description |
|---------|--------|-------------|
| Hardware wallet (Ledger/Trezor) + proxy | ⭐⭐⭐⭐⭐ | Most secure, but complex setup |
| Separate EOA wallet, small amount (<$100) | ⭐⭐⭐⭐ | Good security/convenience balance |
| Main wallet directly | ⭐⭐ | High risk, not recommended |

### 8.2 Environment Variable Security

```bash
# ✅ Correct: Add .env to .gitignore
echo ".env" >> .gitignore

# ❌ Wrong: Never hardcode in code
PRIVATE_KEY="0x..."  # Don't do this!

# ✅ Correct: Read from environment
private_key = os.getenv('PRIVATE_KEY')
```

### 8.3 SkillPay Balance Monitoring

- Don't recharge too much at once (start with 0.5-1.0 USDT)
- Set up Telegram/Email alerts (when balance < 0.05 USDT)
- Backup `state.json` periodically

---

<a name="9"></a>
## 9. Troubleshooting / 故障排查

### 9.1 Common Errors / 常见错误

#### Error 1: `py-clob-client not available`

**Cause**: Dependencies not installed

**Fix**:
```bash
pip install py-clob-client
```

---

#### Error 2: `Invalid private key` or `Insufficient balance`

**Cause**:
- Private key format incorrect (missing `0x` prefix)
- Wallet balance insufficient (Polygon needs gas)

**Fix**:
1. Verify `PRIVATE_KEY` is 64 hex chars with `0x` prefix
2. Transfer at least $5-10 worth USDC/ETH to wallet (Polygon chain)
3. Confirm network is Polygon Mainnet

---

#### Error 3: `market not found` (404)

**Cause**:
- `token_id` market not yet open
- City/date combination doesn't exist

**Fix**:
```bash
# Manual API test
curl "https://gamma-api.polymarket.com/markets?limit=10"
# Verify returned data contains your target city and date
```

---

#### Error 4: `Billing failed (balance: 0.0000)`

**Cause**: SkillPay balance depleted

**Fix**:
1. Recharge via SkillPay Dashboard (minimum 8 USDT)
2. Or wait for next scan cycle (already skips when depleted)

---

#### Error 5: `rate limit` or `429`

**Cause**: API calls too frequent

**Fix**:
- Increase `CHECK_INTERVAL` (e.g., to `600` seconds)
- Decrease `MAX_CONCURRENT_REQUESTS`
- Ensure `REQUEST_DELAY` >= `0.1`

---

### 9.2 Adjust Logging Level

For more verbose logs, add to code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # or INFO, WARNING
```

---

### 9.3 Reset State

Delete `state.json` and `cache/` directory:

```bash
del state.json
rmdir /S /Q cache
python sniper.py --dry-run --once
```

---

<a name="10"></a>
## 10. FAQ / 常见问题

### Q1: What's the difference between dry-run and live mode?

A: `--dry-run` calls `execute_buy_order` but:
- Doesn't initialize real `ClobClient`
- Doesn't send HTTP requests to Polymarket
- Doesn't call `billing_charge`
Only prints "would buy" logs to validate logic.

---

### Q2: Is the billing really only 0.01 USDT per order?

A: Yes. Billing amount is hardcoded as `0.01` in `billing_charge()`. This is SkillPay's rate. You can see each deduction in SkillPay Dashboard.

---

### Q3: If billing fails, does the order get canceled?

A: No. Design principle is "order first":
- Once order is on-chain, it remains valid even if billing fails
- Billing failure only logs warning and shows recharge link
- This is **correct behavior** because on-chain orders cannot be canceled

---

### Q4: Why isn't my `state.json` position info updating?

A: `state.json` saves after each successful order. If not updating:
- Check file permissions (writable?)
- Check for crashes (view error logs)
- Manual restart auto-loads state

---

### Q5: Can I run multiple instances simultaneously?

A: **Not recommended**. Multiple instances compete for `state.json`, causing data corruption. To scale:
- Modify code for multiprocessing (`multiprocessing`)
- Or use shared database (SQLite/PostgreSQL)

---

### Q6: How to adjust trading cities or time windows?

A: Edit `CITY_SLUGS` list (sniper.py:93-100), or modify time parameters like `MONITOR_START_HOUR`.

---

### Q7: How is profit calculated?

A: System doesn't auto-sell; positions hold until settlement:
- If YES token settles at $1.0 → profit = shares × ($1.0 - entry_price)
- If NO token settles at $1.0 → YES token becomes $0 → loss = - shares × entry_price
Actual P&L = unrealized position value + realized P&L (if manually closed)

---

### Q8: Is there an unsubscribe/cancel mechanism?

A: No automatic cancellation. Positions remain in `state.json` until manually deleted or settlement completes.

---

### Q9: How to set up Telegram notifications?

A: Not in current scope. Recommend external script monitoring `sniper.log`, matching keywords (e.g., `Billing failed`, `余额不足`) then sending alerts.

---

### Q10: What does `MIN_CHARGE_AMOUNT` do?

A: Pre-check threshold. If `billing_get_balance` returns < 0.01, scan exits early to avoid wasting API calls. This is **protection mechanism**, not billing amount.

---

## 📞 Support / 支持

- Tele: @zerofinnley

---

**Wishing you successful trading! Remember: risk management first, profits second.** 🎯
