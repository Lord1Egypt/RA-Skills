---
name: global-market-analyst
description: "Global asset investment analysis and advisory — VN & US stocks, forex, gold, oil, crypto, ETF, DCA. Combines real-time technical analysis (RSI, MACD, EMA, Bollinger Bands) from TradingView with fundamental analysis (P/E, ROE, Sharpe, CAGR, sector valuation). Use when: (1) user asks about VN or global stock prices, (2) user wants to know which assets to buy, (3) user asks about portfolio management, (4) user wants to calculate monthly DCA accumulation, (5) user asks how much to invest per month, (6) user wants to estimate returns over time, (7) user wants to compare global asset classes, (8) user asks about gold, crypto, S&P 500, ETF, (9) user asks about swing trading, scalping, day trading VN, (10) user asks about forex EUR/USD, USD/JPY, (11) user asks about commodities oil WTI, silver, (12) user asks about US stocks AAPL, NVDA, TSLA, MSFT, (13) user wants to analyze/rebalance an existing portfolio, (14) user wants to scan markets for a new optimal portfolio, (15) user asks about portfolio optimization, Markowitz, asset allocation."
---

# Global Market Analyst

Global asset analysis — VN stocks, US equities, Forex, Commodities, Crypto, ETF — real-time technical + fundamental + valuation + return estimation.

## ⚠️ Most Important Principle

**Historical CAGR ≠ expectation from current price.**
Always ask: *"If buying TODAY at this price, what is the P/E? Is it still cheap?"*

Example: MCH CAGR 73%/year from the 30k bottom → but at current price 161k, P/E ~37x is **expensive**.
Sharpe 2.19 is historical from low price zone — does not apply to buyers today.

---

## Step 0: Understand Requirements & Check Macro

Before analyzing any asset, always check:

### 🇻🇳 Macro Việt Nam
**Current macro context (updated 23/03/2026):**
- **🔴 VN-Index: ~1,604** — down 14% in the month, foreign net selling -27,591 tỷ YTD
- **🟢 FTSE upgrade VN** → effective 21/09/2026 → biggest catalyst
- SBV rate: Holding, following FED
- GDP target 2026: 6.5-7%

### 🇺🇸 Macro Mỹ
- **FED rate: 3.5-3.75%** (held 18/3/2026, hawkish — only 1 cut expected in 2026)
- **PCE inflation: 2.7%** (raised from 2.4%)
- **Unemployment:** ~4.0% (stable)
- **S&P 500:** In correction ~5-8% from ATH, tech leading
- **US 10Y yield:** ~4.2-4.4%

### 🌍 Global Macro
- **🔴 Iran War ongoing** — dầu WTI $95-99, threatening Strait of Hormuz
- **Vàng XAUUSD:** ~$4,362 (corrected -15% from ATH $5,608)
- **DXY (USD Index):** ~103-105
- **BNB:** Risk-off pressure, ecosystem still strong (TVL $6.7B, #3 globally)
- **ECB rate:** ~3.0%, gradually cutting
- **BOJ rate:** ~0.5%, just raised from 0.25%

**Portfolio impact:**
- 🟢 Accumulate: MBB (P/E 6.5x), Vàng, S&P 500 ETF (VOO)
- 🟢 DCA: FPT (P/E 13-14x, unusually cheap but below EMA200)
- ⏳ Hold: BNB (wait for FED cut), TCB, AAPL, MSFT
- 🔴 Avoid: VCB (P/E expensive), BĐS (rates rising), crypto mới, meme coins
- 🟢 New buys: GAS/PVS (benefiting from high oil), Energy ETF (XLE)

See details: `references/macro-update-2026-03.md`, `references/crypto-analysis.md`, `references/gold-analysis.md`.

---

Determine:
- **Asset class**: VN stocks? US stocks? Forex? Gold? Crypto? ETF?
- **Objective**: Find new opportunities? Analyze a specific ticker? Estimate returns? Scan the market?
- **Holding period**: Short-term (< 3 months), medium-term (3-12 months), long-term (> 1 year)
- **Capital**: For portfolio allocation and risk estimation
- **Risk appetite**: Conservative / Balanced / Aggressive

---

## Step 1: Real-time Data (TradingView Scanner)

TradingView scanner works **WITHOUT auth**:

### 🇻🇳 VN Stocks
```bash
# Scan all HOSE for oversold stocks
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 40 --exchange HOSE

# Deep technical analysis for a single VN stock
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/analyze_stock.py FPT HOSE
```

### 🇺🇸 US Stocks
```bash
# Scan NASDAQ oversold (large-cap > $2B)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 40 --exchange NASDAQ

# Scan NYSE
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 35 --exchange NYSE
```

### 🌍 Global Markets (Crypto, Forex, Commodities)
```bash
# Scan US equities (large-cap > $10B)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market us --rsi 40

# Scan crypto
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market crypto --rsi 35

# Scan forex major pairs
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market forex

# Scan commodities (gold, oil, silver)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market commodities

# Scan all markets
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market all --rsi 40
```

**Manually fetch multiple tickers (any market):**
```python
import urllib.request, json

# VN stocks
payload = {
    "symbols": {"tickers": ["HOSE:MBB","HOSE:TCB","HOSE:FPT"]},
    "columns": ["name","close","change","volume","RSI","EMA20","EMA50","EMA200",
                "MACD.macd","MACD.signal","BB.upper","BB.lower",
                "price_52_week_high","price_52_week_low","Stoch.K","Stoch.D"]
}
req = urllib.request.Request(
    "https://scanner.tradingview.com/vietnam/scan",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    method="POST"
)

# US stocks → "https://scanner.tradingview.com/america/scan"
# Crypto → "https://scanner.tradingview.com/crypto/scan"
# Forex → "https://scanner.tradingview.com/forex/scan"
# Commodities → "https://scanner.tradingview.com/cfd/scan"
```

---

## Step 2: Technical Analysis (Applies to ALL asset classes)

Read each indicator in priority order:

### 1. EMA200 — Check FIRST
- `close > EMA200` ✅ → Long-term uptrend intact → **consider buying**
- `close < EMA200` ❌ → Long-term downtrend → **be cautious, buy only with a clear catalyst**

**⚠️ Do NOT buy oversold assets below EMA200** (unless there is a clear catalyst)

### 2. RSI(14)
| RSI | Signal | Action |
|---|---|---|
| < 30 | 🟢🟢 Extreme oversold | Consider strong buy if above EMA200 |
| 30–40 | 🟢 Oversold | DCA if above EMA200 |
| 40–60 | 🟡 Neutral | Hold / wait |
| 60–70 | 🔴 Near overbought | Do not add positions |
| > 70 | 🔴🔴 Overbought | Consider taking profit |

### 3. MACD
- `macd > signal` → 🟢 Bullish momentum
- `macd < signal` → 🔴 Bearish momentum
- MACD just crossed above signal in negative zone → **strong buy signal**

### 4. Bollinger Bands
- `close ≤ BB.lower` → Near lower band → potential bounce
- BB squeezing → strong move coming, wait for breakout

### 5. Stochastic K/D
- K < 20: Oversold | K > 80: Overbought
- K cắt lên D ở vùng < 20 → mua signal

### 6. 52W Position
```
pos52 = (close - low52w) / (high52w - low52w) × 100
```
- < 20%: Near 52W low — good value zone
- > 80%: Near 52W high — high momentum but risky

### 🎯 Buy Zone Score (composite)
```python
score = 0
if rsi < 30: score += 3
elif rsi < 40: score += 2
if close > ema200: score += 2
if pe_discount > 20%: score += 3  # P/E < Fair P/E - 20%
elif pe_discount > 0: score += 2
if pos52 < 20: score += 2
elif pos52 < 40: score += 1
if close <= bb_lower * 1.02: score += 2
if macd > macd_signal: score += 1
# Max: 15 điểm
# ≥ 10: Mua mạnh | 7-9: DCA | 4-6: Theo dõi | < 4: Bỏ qua
```

---

## Step 3: Valuation Analysis — MANDATORY (Stocks & ETF)

**Do NOT recommend BUY without checking valuation.**

### P/E Analysis
```
Upside = (Fair P/E - Current P/E) / Fair P/E × 100%
```

| Upside | Assessment |
|---|---|
| > 25% | 🟢 Very cheap — buy |
| 10–25% | 🟡 Slightly cheap — accumulate |
| 0–10% | 🟡 Fair — OK |
| < 0% | 🔴 Expensive — wait for correction |
| < -15% | 🔴🔴 Very expensive — avoid |

**Fair P/E by VN sector:**
- Ngân hàng: 10–12x | Công nghệ: 20–25x | Thép: 8–12x
- Tiêu dùng: 15–22x | BĐS: 12–18x | Dầu khí: 10–14x

**Fair P/E by US sector:** (Xem chi tiết `references/us-equities.md`)
- Tech (mega): 25–30x | Tech (growth): 30–45x | Healthcare: 16–20x
- Financials (banks): 10–13x | Energy: 10–14x | Consumer Disc.: 22–28x
- **US dùng Forward P/E** nhiều hơn Trailing P/E
- **PEG Ratio** = P/E / EPS Growth Rate → PEG < 1.0 = rẻ tương đối

See details in `references/sector-fundamentals.md` (VN) và `references/us-equities.md` (US)

### Other Fundamental Metrics
- **ROE > 15%**: tốt | **> 20%**: xuất sắc
- **D/E < 1.0**: ít nợ (ngân hàng ngoại lệ)
- **FCF dương**: công ty sinh tiền thực
- **EPS CAGR**: driver chính của giá dài hạn

See full framework in `references/financial-analysis-knowledge.md`

---

## Step 4: Sector & Catalyst Analysis

### 🇻🇳 VN Sectors
Reference `references/sector-fundamentals.md` và `references/sector-update-2026.md`.

**Catalyst VN 2026-2028:**
- Nâng hạng thị trường FTSE/MSCI → vốn ngoại đổ vào
- Lãi suất giảm → P/E hợp lý cao hơn, BĐS phục hồi
- Đầu tư công tăng → thép, vật liệu xây dựng
- GDP 6-7%/năm → ngân hàng, tiêu dùng

### 🇺🇸 US Sectors
Reference `references/us-equities.md`.

**Catalyst US 2026-2028:**
- AI revolution → NVDA, MSFT, GOOG, META, AMZN
- FED rate cuts → growth stocks rally, REITs phục hồi
- Infrastructure spending → industrials, materials
- GLP-1 drugs → LLY, NVO, healthcare sector

Always answer:
1. **Where is the sector in the cycle?** (growth / peak / recession / bottom)
2. **What are the catalysts for the next 1-3 years?**
3. **What are the main risks?**

---

## Step 5: US Equities Analysis

When user asks about US stocks (AAPL, NVDA, TSLA, MSFT, GOOG, META, AMZN, v.v.):

### Workflow:
1. **Scan data:** `scan_global.py --market us` hoặc fetch trực tiếp
2. **Technical:** Áp dụng Step 2 (EMA200, RSI, MACD, BB)
3. **Valuation:** Forward P/E vs sector average, PEG ratio
4. **Earnings:** Check earnings calendar — KHÔNG mua ngay trước earnings
5. **Macro:** FED rate path, US 10Y yield, DXY ảnh hưởng

### Key Metrics for US Stocks:
- **Forward P/E** (quan trọng hơn trailing)
- **PEG Ratio** (< 1.0 = rẻ, 1.0-2.0 = hợp lý, > 2.0 = đắt)
- **FCF Yield** (FCF / Market Cap — > 5% = tốt)
- **Revenue Growth** (YoY — quan trọng cho tech)
- **Gross Margin** (>60% cho software, >40% cho hardware)

### US vs VN Differences:
- US trade pre/after-market → gap risk cao hơn
- Earnings season 4 lần/năm → stock có thể ±20% trong 1 ngày
- Options market rất active → đọc implied volatility
- Buyback programs → hỗ trợ giá (AAPL buyback $100B+/năm)
- US dùng **fractional shares** → mua $10 NVDA được

See details: `references/us-equities.md`

---

## Step 6: Forex Analysis

When user asks about forex (EUR/USD, USD/JPY, GBP/USD, v.v.):

### Workflow:
1. **Scan:** `scan_global.py --market forex`
2. **Macro check:** Interest rate differential giữa 2 đồng tiền
3. **Technical:** EMA, RSI, Fibonacci, pivot points
4. **Session timing:** Asian/European/US session
5. **Risk:** Swap rates, leverage management

### Key Pairs & Factors:
| Cặp | Key Factors |
|-----|--------------|
| EUR/USD | FED vs ECB rates, trade balance EU-US |
| USD/JPY | FED vs BOJ, risk sentiment, carry trade |
| GBP/USD | BOE rate, Brexit effects, UK economy |
| AUD/USD | RBA rate, commodities (iron ore), China demand |
| USD/VND | SBV policy, trade balance VN, FDI flows |

### Session Times (VN time):
- **London-NY overlap (19:30-23:00 VN)** = best time to trade
- **Asian session (06:00-14:00)** = range-bound, phù hợp range trading
- **London open (14:00-17:00)** = breakout Asian range

### Risk Management Forex:
- **2% rule:** Max risk 2% account per trade
- **Leverage max 1:30** cho beginner
- **ATR-based stop loss:** SL = 1.5-2x ATR(14)

See details: `references/forex-guide.md`

---

## Step 7: Commodities Analysis (Gold, Oil, Silver)

When user asks about gold (XAUUSD), oil (WTI/Brent), silver (XAGUSD):

### Workflow:
1. **Scan:** `scan_global.py --market commodities`
2. **Macro:** Real rates (US 10Y - CPI), DXY, geopolitics
3. **Technical:** EMA200, RSI, Fibonacci retracement
4. **Specific factors:** (xem bên dưới)

### 🥇 Gold (XAUUSD):
- **Bullish khi:** Real rates giảm, DXY yếu, risk-off, NHTW mua vàng
- **Bearish khi:** Real rates tăng, DXY mạnh, risk-on
- **Key levels:** Round numbers ($4000, $4500, $5000)
- **Seasonal:** Thường mạnh Q1 và Q4
- See details: `references/gold-analysis.md`

### 🛢️ Oil (WTI / Brent):
- **Bullish khi:** OPEC+ cắt sản lượng, geopolitics (Iran/ME), demand tăng
- **Bearish khi:** Recession fears, OPEC+ tăng sản lượng, US shale tăng
- **Key data:** EIA Weekly Inventory, Baker Hughes Rig Count
- **Correlation:** USD/CAD (inverse), energy stocks (positive)

### 🥈 Silver (XAGUSD):
- **Dual nature:** Industrial metal + precious metal
- **Gold/Silver Ratio:** > 80 = bạc rẻ tương đối, < 60 = bạc đắt
- **Volatile hơn vàng:** Beta ~1.5-2x so với gold

---

## Step 8: Global ETF Analysis

When user asks about ETF (VOO, QQQ, VNM, v.v.):

### Workflow:
1. **Identify need:** Core portfolio? Sector bet? Country exposure?
2. **Compare:** Expense ratio, tracking error, AUM, liquidity
3. **Technical:** Áp dụng EMA200, RSI cho ETF chart
4. **DCA plan:** Phân bổ theo risk profile

### Quick ETF Recommendations:
| Purpose | ETF | Expense | Notes |
|----------|-----|---------|---------|
| Core US | VOO / IVV | 0.03% | S&P 500, portfolio foundation |
| Tech/Growth | QQQ / QQQM | 0.15-0.20% | NASDAQ 100, AI exposure |
| VN Exposure | VNM | 0.66% | VanEck Vietnam ETF |
| Emerging Markets | VWO / IEMG | 0.08-0.09% | Broad EM |
| Bonds | BND / AGG | 0.03% | US total bond |
| Gold | GLD / IAU | 0.25-0.40% | Physical gold ETF |
| All-World | VT | 0.07% | Toàn cầu, lazy portfolio |

### DCA Portfolios:

**Conservative:** VOO 40% + BND 30% + VWO 15% + GLD 15%
**Balanced:** VOO 45% + QQQ 20% + VWO 15% + BND 10% + GLD 10%
**Aggressive:** QQQ 35% + VOO 25% + VWO/VNM 20% + ARKK/SOXX 10% + GLD 10%

See details: `references/global-etf.md`

---

## Step 9: Portfolio Management

When user asks about **portfolio management, rebalancing, asset allocation, or building a new portfolio**:

### Option 1: Analyze Existing Portfolio → Rebalance
```bash
# Analyze & recommend rebalancing for current portfolio
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/portfolio_optimizer.py \
  --portfolio "MBB:30,FPT:25,GOLD:20,BNB:15,CASH:10" \
  --capital 500000000 \
  --risk balanced
```

**Input:**
- `--portfolio` : Current portfolio dạng "MÃ:tỷ_trọng%,..." 
- `--capital` : Total capital (VND)
- `--risk` : `conservative` | `balanced` | `aggressive`

**Output:**
- Portfolio analysis: return, volatility, Sharpe, max drawdown
- Assessment: concentration, diversification, risk fit
- Correlation matrix between assets
- Rebalance recommendation via Markowitz Mean-Variance
- Before/after rebalance comparison
- Bear/Base/Bull return scenarios
- Implementation plan

**Supported asset classes:** VN stocks, US stocks, ETF, crypto (BTC/ETH/BNB/SOL...), gold (GOLD/XAUUSD), forex, bonds (BOND), cash (CASH)

### Option 2: Scan Market → Recommend New Portfolio
```bash
# Scan & recommend new optimal portfolio
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/portfolio_screener.py \
  --capital 500000000 \
  --risk balanced \
  --markets vn,us,crypto,gold \
  --horizon medium
```

**Input:**
- `--capital` : Total capital (VND)
- `--risk` : `conservative` | `balanced` | `aggressive`
- `--markets` : `vn,us,crypto,gold` (chọn thị trường)
- `--horizon` : `short` (< 3 tháng) | `medium` (3-12 tháng) | `long` (> 1 năm)

**Output:**
- Real-time TradingView scan to find top assets by score
- Allocation by risk profile:
  - **Conservative:** 50% bonds/cash, 30% blue chip, 15% gold, 5% crypto
  - **Balanced:** 30% blue chip, 25% growth, 20% gold, 15% ETF, 10% crypto
  - **Aggressive:** 35% growth, 25% crypto, 20% midcap, 15% forex/commodities, 5% commodities
- Specific ticker list + allocation + rationale
- Expected return range (Bear/Base/Bull)
- Suggested DCA schedule by horizon

### Risk Profiles:
| Profile | Max single | Max equity | Max crypto | Min safe assets | Target Vol |
|---------|-----------|-----------|-----------|----------------|-----------|
| Conservative | 25% | 40% | 5% | 35% | 12% |
| Balanced | 30% | 60% | 15% | 20% | 18% |
| Aggressive | 35% | 80% | 25% | 5% | 25% |

---

## Step 10: Return Estimation

```bash
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/estimate_returns.py [TICKER] [--capital X] [--years N]
```

Script calculates from historical data:
- **CAGR** 3Y/5Y (compound annual growth rate)
- **Volatility** hàng năm (annualized volatility)
- **Max Drawdown** (maximum drawdown from peak)
- **Sharpe Ratio** (return/risk)
- **3 scenarios** Bear/Base/Bull × 6M/1Y/3Y/5Y

**⚠️ Always remind user:**
- Historical CAGR is from past ENTRY price, not current price
- If current P/E is already high → realistic estimate is lower than historical CAGR
- Compare with: bank deposit 5.5%/year (VN), US Treasury 4.5%/year, VN-Index ~11%/year, S&P 500 ~12%/year

See full methodology in `references/return-estimation.md`

---

## Step 11: Portfolio Allocation (Global)

When user asks how to allocate capital:

### Sizing by Sharpe
| Sharpe | Max allocation |
|---|---|
| > 1.5 | 35% |
| 1.0–1.5 | 25% |
| 0.5–1.0 | 15% |
| < 0.5 | 10% |

### Sizing by Max Drawdown
| Max DD | Max allocation |
|---|---|
| < 30% | 30% |
| 30–50% | 20% |
| 50–70% | 10% |
| > 70% | 5% |

### Global Portfolio Framework:
| Asset Class | Conservative | Balanced | Aggressive |
|-------------|-------------|----------|------------|
| VN Stocks | 20% | 25% | 30% |
| US Stocks/ETF | 30% | 35% | 35% |
| Bonds/Cash | 25% | 10% | 5% |
| Gold | 15% | 15% | 10% |
| Crypto | 0% | 5% | 10% |
| Forex/Commodities | 0% | 5% | 10% |
| EM ETF | 10% | 5% | 0% |

### DCA Strategy
- Don't go all-in at once
- Split into 3-5 purchases over 4-8 weeks
- Buy more when RSI drops to oversold zone
- **ETF DCA:** Same day each month, don't time the market

---

## Step 12: Output Formats

### 📊 VN Stock Output
```
## 📊 [TICKER] — [Tên công ty]
Price: X,XXX VND | Today: +/-X.XX% | Volume: XM

### Technical
- RSI: XX.X [tín hiệu]
- EMA200: X,XXX [▲ Trên / ▼ Dưới] — [Uptrend / Downtrend]
- MACD: [🟢 Bullish / 🔴 Bearish]
- Bollinger: [vị trí]
- 52W: High X,XXX | Low X,XXX | Vị trí: XX%
- Score: X/15

### Valuation
- P/E hiện tại: XX.Xx (Fair: XX-XXx)
- Upside định giá: +/-XX%
- ROE: XX% | D/E: XX

### Conclusion
[🟢 MUA / 🟡 THEO DÕI / ⏳ CHỜ / 🔴 TRÁNH]
Reason: [1-2 câu]
Ideal buy zone: [X,XXX – X,XXX VND]
```

### 🇺🇸 US Stock Output
```
## 🇺🇸 [TICKER] — [Company Name]
Price: $XXX.XX | Today: +/-X.XX% | Volume: XM | Market Cap: $X.XB

### Technical
- RSI: XX.X [signal]
- EMA200: $XXX [▲ Above / ▼ Below]
- MACD: [🟢 Bullish / 🔴 Bearish]
- 52W: High $XXX | Low $XXX | Position: XX%

### Valuation
- Forward P/E: XX.Xx (Sector avg: XX-XXx)
- PEG Ratio: X.XX
- FCF Yield: X.X%
- Next Earnings: [Date]

### Conclusion
[🟢 MUA / 🟡 THEO DÕI / ⏳ CHỜ / 🔴 TRÁNH]
Reason: [1-2 câu]
Entry zone: $XXX – $XXX
```

### 💱 Forex Output
```
## 💱 [PAIR] — Forex Analysis
Price: X.XXXX | Today: +/-X.XX% | Session: [Asian/European/US]

### Technical
- RSI: XX.X | EMA200: X.XXXX [▲/▼]
- MACD: [🟢/🔴] | Fibonacci: [key level]
- Support: X.XXXX | Resistance: X.XXXX

### Macro
- Rate differential: [FED X.XX% vs ECB/BOJ X.XX%]
- DXY: XXX.X [trend]
- Key data upcoming: [event + date]

### Trade Setup
Direction: [🟢 LONG / 🔴 SHORT / 🟡 NEUTRAL]
Entry: X.XXXX | SL: X.XXXX (-XX pips) | TP: X.XXXX (+XX pips)
R:R: 1:X | Lot size (2% risk, $5K account): X.XX lots
```

### 🏆 Commodity Output
```
## 🏆 [COMMODITY] — Analysis
Price: $X,XXX | Today: +/-X.XX%

### Technical
- RSI: XX.X | EMA200: $X,XXX [▲/▼]
- Key S/R: $X,XXX / $X,XXX

### Drivers
- [Factor 1: impact]
- [Factor 2: impact]

### Conclusion
[🟢 MUA / 🟡 TRUNG LẬP / 🔴 TRÁNH]
Buy zone: $X,XXX – $X,XXX
```

### 📈 ETF Output
```
## 📈 [ETF] — [Name]
Price: $XXX.XX | YTD: +/-X.XX% | Expense: X.XX% | Yield: X.X%

### Technical
- RSI: XX.X | EMA200: $XXX [▲/▼]
- Drawdown từ ATH: -X.X%

### So sánh
- vs S&P 500: [outperform/underperform] XX%
- vs category: [ranking]

### DCA Estimate ($XXX/tháng)
- 5 năm: ~$XX,XXX (gốc $XX,XXX, lãi ~$XX,XXX)
- 10 năm: ~$XX,XXX

### Conclusion
[🟢 DCA / 🟡 CHỜ / 🔴 TRÁNH]
```

---

## Step 13: Swing Trading (VN)

When user asks about **swing trading, scalping, day trading**, or short-term trading (2-10 days):

Full reference: `references/swing-trading-vn.md`

### Quick Workflow

1. **Screening:** Chạy swing screener tìm mã phù hợp
   ```bash
   python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 45 --exchange HOSE
   ```

2. **Technical check (swing-specific):**
   - RSI divergence (bullish/bearish) trên D1
   - MACD crossover position (vùng âm = mua mạnh)
   - Bollinger squeeze → chờ breakout
   - ADX > 25 → trend đủ mạnh để swing

3. **Entry criteria:**
   - R:R tối thiểu 1:2 (KHÔNG trade nếu < 1:2)
   - Volume xác nhận (> 1.5x avg 20 phiên)
   - Stop loss xác định TRƯỚC khi vào lệnh

4. **Position sizing:**
   - 2% rule: Max risk 2% vốn per trade
   - Max 3-5 vị thế swing cùng lúc

### Output Format (Swing)
```
## 🏄 [TICKER] — Swing Analysis
Setup: [RSI Divergence / BB Squeeze / MACD Cross / ...]
Entry: X,XXX VND | Stop Loss: X,XXX (-X%) | Target: X,XXX (+X%)
R:R: 1:X | Position Size: X% vốn (XX CP)
Timeframe: X-X ngày
⚡ Confidence: [Cao/Trung bình/Thấp]
```

---

## References

### VN Market
- `references/sector-fundamentals.md` — Standard P/E, catalyst, risk per VN sector
- `references/sector-update-2026.md` — Sector update Q1/2026
- `references/swing-trading-vn.md` — Swing trading, scalping VN

### US & Global
- `references/us-equities.md` — Top 20 S&P 500, US sector breakdown, P/E benchmarks, ADR/OTC
- `references/forex-guide.md` — Major/cross pairs, factors, sessions, swap rates
- `references/global-etf.md` — VOO/QQQ/SPY comparison, VNM ETF, EM ETFs, Bond ETFs, DCA strategy

### Macro & Asset-specific
- `references/macro-update-2026-03.md` — Macro context 03/2026: FED, VN-Index, Iran War
- `references/crypto-analysis.md` — Crypto/BNB analysis framework
- `references/gold-analysis.md` — Gold XAUUSD analysis framework

### Knowledge Base
- `references/financial-analysis-knowledge.md` — RSI, MACD, P/E, Sharpe, DCA, Global portfolio
- `references/advanced-ta.md` — Fibonacci, Elliott Wave, Volume Profile
- `references/return-estimation.md` — Return estimation methodology

## Scripts

- `scripts/scan_market.py` — Scan VN + US exchanges (HOSE, HNX, NASDAQ, NYSE)
- `scripts/scan_global.py` — Scan global markets (US, crypto, forex, commodities)
- `scripts/analyze_stock.py` — Deep technical analysis for a single ticker
- `scripts/estimate_returns.py` — Estimate returns from historical data
- `scripts/dca_calculator.py` — Calculate monthly DCA accumulation
- `scripts/portfolio_optimizer.py` — Analyze existing portfolio → rebalance recommendation (Markowitz)
- `scripts/portfolio_screener.py` — Scan market → recommend new optimal portfolio

**DCA Calculator:**
```bash
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/dca_calculator.py [monthly_vnd] [years]
# Example: 2 million VND/month, 10 years
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/dca_calculator.py 2000000 10
```

---

*⚠️ Analysis is for reference only, not investment advice. DYOR.*
