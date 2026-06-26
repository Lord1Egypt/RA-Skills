# Background Knowledge: SkillPay Billing & Weather Event Trading

**This document explains the design philosophy, meteorological principles, and engineering trade-offs in sniper.py**

---

## Table of Contents

1. [Why 2 PM? — Meteorological Principles](#1)
2. [What Are We Trading? — Weather Event Markets](#2)
3. [System Execution Flow](#3)
4. [Time Window Technical Considerations](#4)
5. [Balance & Billing: The Art of Separation](#5)
6. [Exception Handling Philosophy](#6)
7. [Production Recommendations](#7)

---

<a name="1"></a>
## 1. Why 2 PM? — Meteorological Principles

### 1.1 The Physics of Diurnal Heating

Solar radiation reaching Earth's surface doesn't instantly convert to air temperature. The process follows:

```
Solar Radiation → Surface Absorption → Heat Convection/Conduction → Air Temperature Rise
```

**Key delays**:
- **Thermal inertia**: Surface (soil, water) needs time to warm up
- **Heat accumulation**: Energy builds up in lower atmosphere
- **Radiative balance**: Surface net heating continues while incoming > outgoing radiation

### 1.2 Typical Daily Temperature Curve

```
Temperature
  ↑
  |               /\
  |              /  \
  |    ________/    \________
  |   /                       \
  |  /                         \
  | /                           \
  +------------------------------→ Time
    00:00   06:00   12:00   18:00
```

- **Minimum**: Around sunrise (05:00-07:00, seasonal/location dependent)
- **Rising phase**: Fast warming morning (08:00-13:00)
- **Maximum**: **13:00-15:00 (1-3 PM)** ← Your strategy's sweet spot
- **Falling phase**: Slow cooling afternoon through night

### 1.3 Why Peak Temperature at 2 PM (Not Noon)?

**Common misconception**: "Sun is highest at noon, so it should be hottest"

**Actual physics**:

```
Time    Solar Elevation   Incoming Radiation   Surface Temp   Air Temp
06:00   Low               Weak                Cold           Cold
12:00   Highest           Strongest           Warm           Warming
14:00   High              Strong              Highest        **Peak**
15:00   Medium            Medium              Peak           Cooling
```

**Key factors**:
1. **Net energy accumulation**: Surface continues absorbing net heat from sunrise to noon (incoming > outgoing)
2. **Thermal lag**: Air temperature lags surface temperature by 1-2 hours
3. **Heat capacity**: Air and surface specific heat capacity needs time to transfer warmth

> 📊 **Data reference**: In most regions of China, daily maximum temperature occurs between 14:00-15:00 with >75% probability. In extreme cases, it can delay until 16:00.

### 1.4 Seasonal & Geographic Corrections

- **Summer**: Longer lag (up to 3 hours), peak may occur at 16:00
- **Winter**: Shorter lag, peak may occur at 13:00-14:00
- **Coastal vs Inland**: Coastal areas moderated by ocean, peak temperature may occur earlier
- **Altitude**: High altitude regions have strong UV but thin air, warming/cooling is faster

**Your strategy assumption**: Across 50 major cities (CITY_SLUGS), daily max temperature consistently occurs between 14:00-15:00.

---

<a name="2"></a>
## 2. What Are We Trading? — Weather Event Markets

### 2.1 Polymarket Weather Events

Polymarket is a decentralized prediction market platform. The contract type you trade:

```
Question: "Will the high temperature in Tokyo on March 26, 2026 exceed 75°F?"

Yes token: Pays $1 if temperature exceeds 75°F, $0 otherwise
No token:  Pays $1 if temperature does NOT exceed 75°F, $0 otherwise
```

**Key parameters**:
- `token_id`: Unique identifier for YES token (what you buy)
- `no_token_id`: Unique identifier for NO token (used for sell-side calculations)
- `best_ask`: Lowest ask price for YES token (e.g., $0.53 means 53% market probability)
- `market_id`: Unique market identifier

### 2.2 Your Trading Logic

**Core assumption**: Temperature forecast uncertainty remains in the morning but becomes certain by afternoon.

**Your strategy**:
1. **Scan window**: 10:00-14:00 (monitoring period)
2. **Trigger condition**: City's "today" or "tomorrow" date, YES token price below threshold (e.g., <0.6)
3. **Entry**: Buy YES token with fixed amount (`TRADE_AMOUNT_USD=1.0`)
4. **Expectation**: Price rises as temperature becomes certain → buy low → sell high (or hold to settlement)

**Risks**:
- Token value goes to $0 if temperature doesn't meet threshold
- Polymarket liquidity risk
- Network/API failures

---

<a name="3"></a>
## 3. System Execution Flow

### 3.1 Main Loop: `scan_cycle()`

```
┌─────────────────────────────────────────────────────┐
│ scan_cycle(api_client)                              │
├─────────────────────────────────────────────────────┤
│ 1. Balance Pre-check (SKILLPAY)                     │
│    if balance < MIN_CHARGE_AMOUNT: return           │
│                                                     │
│ 2. Market Scanning (scan_and_find_trades)           │
│    - Iterate 50 cities × 2 days = 100 combinations │
│    - Fetch orderbook, temperature forecast, gamma  │
│    - Determine: tradeable? (price < max(0.6,gamma))│
│                                                     │
│ 3. Monitor Window Filtering                         │
│    is_in_monitor_window(city, date)                 │
│    - Today: 10:00-14:00 (after official forecast)  │
│    - Tomorrow: All day (market already open)       │
│                                                     │
│ 4. Order Loop (for cand in window_candidates)      │
│    - Check existing position (1 per city/day)      │
│    - 【Real-time balance check】prevent depletion  │
│    - execute_buy_order(...)                         │
│    - Success → save position, record trade         │
│    - Fail → skip, continue next                    │
│                                                     │
│ 5. Fallback Phase (10:00-10:04)                     │
│    - Execute fallback for unpositioned cities      │
│    - Pick highest probability candidate           │
│    - Same pre-order balance check                  │
│                                                     │
│ 6. State Persistence                               │
└─────────────────────────────────────────────────────┘
```

### 3.2 Order Function: `execute_buy_order()`

```
execute_buy_order(token_id, price, max_price, dry_run, ...)

├── dry_run=True → print only, no API calls
├── price > max_price → slippage protection exit
├── Initialize ClobClient (L2 credentials)
│
├── Retry loop (MAX_RETRIES)
│   ├── client.create_order() → sign
│   ├── client.post_order() → on-chain
│   │   SUCCESS → return order_id
│   │   FAIL → catch exception, retry/exit
│
├── Billing call (after order success)
│   └── try:
│         billing_charge(user_id)  # deduct 0.01 USDT
│         if ok: print success
│         else: print warning + payment_url
│       except Exception as e:
│         print warning (ignore)
│
└── Return order_result dict
```

**Core constraint**:
- Billing happens **after** `post_order` → guarantees "charge only on successful order"
- Billing exceptions are caught → prevents order rollback (already on-chain)

### 3.3 Pre-check vs Real-time Check

| Stage | Location | Purpose | Frequency |
|-------|----------|---------|-----------|
| **Pre-scan check** | scan_cycle start | Fast-fail obvious insufficiency | 1x/scan |
| **Pre-order check** | window_candidates loop | Prevent mid-run depletion | Before every order |
| **Fallback check** | fallback loop | Same as above | Before every fallback |

**Design principle**:
- Pre-check is "fast-fail" to avoid wasting API calls
- Real-time check is "hard constraint" ensuring sufficient balance per order
- Combination: performance + correctness

---

<a name="4"></a>
## 4. Time Window Technical Considerations

### 4.1 Monitor Window

```python
def is_in_monitor_window(city: str, date_obj: date) -> bool:
    now = datetime.now(timezone.utc) + timedelta(hours=8)  # UTC+8
    date_str = date_obj.strftime("%Y-%m-%d")

    # Today: only after forecast release
    if date_str == today:
        window = WINDOW_TIMES[city]["today"]
        start = datetime.strptime(f"{today} {window['start']}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{today} {window['end']}", "%Y-%m-%d %H:%M")
        return start <= now <= end
    # Tomorrow: all day
    else:
        return True
```

**Window time definition** (inferred, based on weather forecast release schedules):

| City | Today Window | Reason |
|------|--------------|--------|
| Tokyo, Seoul, Singapore | 10:00-14:00 | JMA releases daily forecast at 08:00, market needs reaction time |
| London, Paris, Frankfurt | 09:00-15:00 | European meteorological services update at 09:00 |
| New York, Chicago, LA | 08:00-14:00 | NWS morning release |
| Sydney, Melbourne | 23:00-03:00 (next day) | Timezone shifted |

**Your current config**: `WINDOW_TIMES` not visible in code, but presumably different per city based on local forecast agency schedules.

### 4.2 Fallback Window: Why 10:00-10:04?

```
Fallback trigger conditions:
  - is_fallback_time(city, today_str) returns True
  - AND city has no position today

Time logic (sniper.py:is_fallback_time):
  Current time within 10:00-10:04 (inclusive) → execute fallback
```

**Design intent**:
1. **Last chance**: 10:00 provides 4 hours until 14:00 peak temp, market liquidity is healthy
2. **Avoid duplication**: Each city can fallback only once per day (`fallback_executed` set)
3. **Stability**: 4-minute window ensures all cities get checked reliably
4. **Avoid open congestion**: 9:30-10:00 may have heavy order flow, 10:00+ market stabilizes

**Why not later?**
- By 14:00 temperature is essentially certain, trading value diminishes
- Need time for position to potentially profit before settlement (though holding to settlement also works)

---

<a name="5"></a>
## 5. Balance & Billing: The Art of Separation

### 5.1 Design Constraints

- **Order placement ≠ Billing success**
- Orders are settled on-chain irreversibly
- Billing API may fail (network issues, insufficient balance, SkillPay server errors)

### 5.2 The Original Problem

**Scenario**:
```
User balance = 0.01 USDT
5 cities triggered in same scan cycle
Pre-check: balance >= 0.01 → PASS
Loop:
  1st order: success + billing success → balance = 0
  2nd order: order success, billing fail (insufficient balance) → only warning logged
  3rd-5th: same billing fail
Result: User pays gas 5 times, but only 1 billing counted
Risk: User loses 5x transaction costs, SkillPay only receives 0.01
```

### 5.3 Solution: Real-time Balance Check Before Every Order

**Fixed flow**:

```
Pre-check: balance = 0.01 → PASS

for cand in window_candidates:
    # Pre-order check
    balance = billing_get_balance(user_id)
    if balance < 0.01:
        break  # exit loop, stop trying
    execute_buy_order():
        order success
        billing_charge(user_id)  # may fail but order already on-chain
```

**Effect**:
- After 1st order: balance = 0 → Before 2nd order: check finds < 0.01 → break
- Prevents meaningless orders and gas waste
- Protects user from depletion during multi-city bursts

### 5.4 Why Not Rollback Inside `execute_buy_order`?

```python
# Bad approach: try to rollback after billing fail (impossible)
order_result = await execute_buy_order(...)  # already on-chain
bill = billing_charge(user_id)
if not bill['ok']:
    cancel_order(order_result['order_id'])  # ❌ order already filled, cannot cancel
```

**Why cancellation impossible**:
- `OrderType.GTC` (Good Till Cancel) requires explicit cancel request
- Filled orders cannot be canceled, only wait for settlement
- Rollback on blockchain is non-atomic operation, requires complex additional logic

**Correct approach**: Prevent, not remediate

---

<a name="6"></a>
## 6. Exception Handling Philosophy

### 6.1 Tiered Handling

| Exception Type | Source | Handling | Impact |
|----------------|--------|----------|--------|
| Pre-check insufficient balance | SkillPay API | `return` skip entire scan | No trades executed |
| Order price exceeds limit | Local check | `return None` | Skip this city, continue |
| Polymarket API error | `ClobClient` | Retry (up to `MAX_RETRIES`) | Temporary failure, may succeed |
| Billing fail after order | SkillPay API | print warning + payment_url | **Order still succeeds** |
| Billing network timeout | `requests` timeout | try-except, print warning | **Order still succeeds** |
| Balance query exception | SkillPay API | try-except, print warning, continue | Continue (risk: may have insufficient balance) |

### 6.2 Core Principle

**"Order success is hard, billing failure is soft"**

```python
try:
    order = post_order()  # critical path
    billing_charge()      # non-critical path
except BillingError:
    log_warning()         # continue, don't throw
```

**Philosophy**:
- User's trading intent is paramount
- Billing failure is an operational issue, shouldn't penalize user
- Log warnings and show payment link, let user handle later

### 6.3 Fallback Exception Handling

Fallback loop also has balance check; on exception it breaks:

```python
if not self.dry_run and SKILLPAY_USER_ID:
    try:
        balance = billing_get_balance(SKILLPAY_USER_ID)
        if balance < MIN_CHARGE_AMOUNT:
            print("[ERROR] Insufficient balance, stopping fallback orders")
            break
    except Exception as e:
        print(f"[WARN] Balance check failed ({e}), continuing...")
        # Not breaking, still try orders (since we can't know balance)
```

**Why "fail open" here?**
- Balance API occasionally times out, shouldn't miss all fallback opportunities
- Costs already incurred (pre-check passed), worth attempting

---

<a name="7"></a>
## 7. Production Recommendations

### 7.1 Key Metrics to Monitor

| Metric | Location | Normal Range | Alert Threshold |
|--------|----------|--------------|-----------------|
| `scan_cycle` duration | logs | < 60 seconds | > 120 seconds |
| Billing success rate | billing_charge return `ok=True` | > 99% | < 95% |
| Insufficient balance stops | "[ERROR] 余额不足" log | 0/day | any > 0 |
| Fallback execution count | "[FALLBACK]" log | ≤ number of cities | abnormally high (strategy broken?) |
| `billing_get_balance` error rate | "[WARN] 余额检查失败" | < 1% | > 5% |

### 7.2 SkillPay Recharge Strategy

**Current configuration**:
- Per-order billing: `0.01 USDT` (fixed)
- Minimum recharge amount: `8 USDT` (from `payment_link` call)

**Recommendations**:
1. **Initial top-up**: At least `0.01 × max concurrent orders × 2`, e.g., max 5 orders → `0.1 USDT`, suggest `0.5 USDT` to avoid frequent top-ups
2. **Alerting**: Send email/Telegram when balance < `0.05 USDT`
3. **Auto-topup** (optional): Monitor `payment_url` output, auto-open browser for manual top-up

### 7.3 Log Analysis Examples

```bash
# Count billing failures
grep "Billing failed" sniper.log | wc -l

# Check balance depletion stops
grep "余额不足" sniper.log

# Count fallback effectiveness
grep "FALLBACK" sniper.log | grep -v "Skipping" | wc -l
```

### 7.4 Deployment Best Practices

**Environment variables** (`.env`):
```bash
SKILLPAY_USER_ID=your_wallet_address
SKILL_BILLING_API_KEY=sk_live_xxxxx
SKILL_ID=e56f2a83-819c-4e43-a457-5442ebba0098
POLY_API_KEY=...
PRIVATE_KEY=0x...
PROXY_WALLET=0x...
TRADE_AMOUNT_USD=1.0
```

**Running**:
```bash
# Production (recommend screen/tmux)
python sniper.py --dry-run=False

# Testing
python sniper.py --dry-run=True
```

**Version control**:
- Keep `state.json` (positions, trade history)
- Backup periodically to S3/cloud storage
- Exclude `.env` and `state.json` from git commits

---

## Appendix: Glossary

| Term | Explanation |
|------|-------------|
| **Daily Max Temp** | Peak temperature of the day, typically 14:00-15:00 |
| **YES token** | Event occurrence warrant, price = market probability |
| **best_ask** | Lowest ask price (price buyer must accept) |
| **slippage tolerance** | `SLIPPAGE_TOLERANCE`, e.g., 5% → max_price = best_ask × 1.05 |
| **dry_run** | Simulation mode, no orders/billing, for testing |
| **fallback** | Force order at 10:00-10:04 for unpositioned cities, ensure every city has a position |
| **MIN_CHARGE_AMOUNT** | Minimum pre-check balance (0.01 USDT), guarantees at least one billing can occur |
| **MAX_RETRIES** | Order retry count (default 3) |
| **L2 credentials** | Polymarket secondary auth (API key + secret + passphrase) |

---

## Conclusion

The system's design philosophy:

1. **Meteorology-driven**: Leverages "daily max at 2 PM" certainty, scanning intensively in 10:00-14:00 window
2. **Defensive programming**: Pre-order balance checks prevent mid-run depletion
3. **Order-first**: Order success is hard requirement, billing failure is soft warning
4. **Time-sensitive**: Strict time windows, fallback as last 4-minute opportunity
5. **Observable**: Every critical step is logged for post-mortem analysis

Understanding these background concepts helps you:
- Adjust parameters (e.g., window times) for seasonal/city variations
- Diagnose issues (billing failures, order slippage, balance anomalies)
- Optimize strategy (increase/decrease concurrent orders, refine fallback logic)

Happy trading! 🎯
