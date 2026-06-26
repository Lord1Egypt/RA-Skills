# Crypto & BNB Analysis Framework
> Comprehensive crypto analysis framework — On-chain, Tokenomics, DeFi, Technical

---

## 1. ON-CHAIN ANALYSIS — Blockchain Data Analysis

### 1.1 MVRV — Market Value to Realized Value
**"P/E ratio" của crypto**

**Công thức:** MVRV = Market Cap / Realized Cap
- **Market Cap:** Giá hiện tại × Circulating Supply
- **Realized Cap:** Tổng giá trị mỗi coin tại mức giá lần cuối nó di chuyển on-chain (= tổng cost basis)

| MVRV | Meaning | Hành động |
|------|---------|-----------|
| < 1.0 | 🟢🟢 Most holders at loss → accumulation zone | Strong buy (historically = bottom) |
| 1.0–2.0 | 🟢 Holder lãi vừa phải → healthy | DCA bình thường |
| 2.0–3.5 | 🟡 Overvalued → profit-taking bắt đầu | Cẩn thận, bắt đầu chốt lời |
| > 3.5 | 🔴 Extreme overvalued → bubble territory | Chốt lời mạnh |

**MVRV-Z Score:** Đo mức độ chênh lệch MVRV so với trung bình lịch sử
- Z > 7: Đỉnh chu kỳ (2017, 2021) → BÁN
- Z < 0: Đáy chu kỳ → MUA

**Source data:** Glassnode, CryptoQuant, Santiment

### 1.2 NVT — Network Value to Transactions
**"P/E ratio" dựa trên giao dịch thực tế**

**Công thức:** NVT = Market Cap / Daily Transaction Volume (USD)

| NVT | Meaning |
|-----|---------|
| < 20 | 🟢 Network undervalued so với usage → mua |
| 20–50 | 🟡 Fair value |
| > 65 | 🔴 Speculative premium → giá chạy trước utility |

**NVT Signal (NVTS):** Dùng MA90 của transaction volume → smoother, chính xác hơn

**Ví dụ thực tế:**
- BTC NVT > 100 vào đỉnh 2021 → speculative bubble
- BTC NVT < 20 vào đáy 2022 → undervalued, cơ hội mua

### 1.3 Supply Distribution — Phân bố nguồn cung
- **Whale wallets** (> 1000 BTC hoặc > 10,000 BNB): Theo dõi tích lũy/phân phối
- **Exchange inflow/outflow:** Coin chuyển vào sàn = chuẩn bị bán, ra khỏi sàn = hold
- **Long-term holder supply:** Tỷ lệ coin held > 1 năm tăng = bullish signal

### 1.4 Hash Rate (chỉ cho PoW — Bitcoin)
- Hash rate tăng → miners tin tưởng network → bullish
- Hash rate giảm → miners thoát → bearish
- **Không áp dụng cho BNB** (BNB dùng PoSA, không phải PoW)

---

## 2. BNB — DEEP ANALYSIS

### 2.1 BNB Tokenomics (03/2026)

| Metric | Giá trị |
|--------|---------|
| **Max Supply** | 200,000,000 BNB |
| **Circulating Supply** | ~136,360,000 BNB |
| **Target long-term** | 100,000,000 BNB (giảm dần qua burn) |
| **Staking APY** | 0.95% – 1.25% |
| **Staked Amount** | > 25.7 triệu BNB |
| **Consensus** | Proof of Staked Authority (PoSA) |

### 2.2 Burn Mechanism (Deflationary)

**Dual Burn Strategy:**

1. **Quarterly Auto-Burn** (BEP-95 auto-burn)
   - Mỗi quý burn tự động dựa trên: giá BNB × số block được tạo
   - Q1/2026 (lần thứ 34): **1,371,804 BNB burned** (~$1.27 tỷ)
   - Burn vào "black hole" address, không thể recover

2. **Real-time BEP-95 Burn**
   - Một phần gas fee mỗi block bị burn liên tục
   - ~281,000 BNB đã burn qua cơ chế này
   - Tạo áp lực giảm phát thường trực

**Why it matters:**
```
Supply giảm liên tục (136M → target 100M)
+ Demand tăng (DeFi, trading, gas)
= Áp lực tăng giá dài hạn
```

### 2.3 BNB Chain Ecosystem (2025-2026)

| Metric | 2025 | Trend |
|--------|------|-------|
| **TVL** | ~$6.7 tỷ | +40.5% YoY |
| **Daily transactions** | Tăng 150% YoY | 🚀 |
| **Stablecoin market cap on BNB** | Gấp đôi YoY | 🚀 |
| **RWA on-chain** | ~$2 tỷ (03/2026) | Mới nổi |
| **Vị trí TVL toàn cầu** | #3 (sau ETH, SOL) | Ổn định |

**Tech Roadmap 2026:**
- Target: 20,000 TPS (transactions per second)
- Sub-second finality
- Giảm gas fee thêm
- Focus: High-performance EVM trading chain
- Use cases: AI + RWA + advanced DeFi

### 2.4 Factors Affecting BNB Price

**Bullish Factors:**
- ✅ Deflationary tokenomics (burn liên tục)
- ✅ Ecosystem growth mạnh (TVL, transactions)
- ✅ RWA tokenization trend
- ✅ FED cắt lãi suất → liquidity tăng → crypto tăng
- ✅ Binance exchange vẫn #1 globally
- ✅ Tech upgrades (speed, fees)

**Bearish Factors:**
- ❌ Regulatory risk (Binance đã settle $4.3B với DOJ nhưng vẫn bị theo dõi)
- ❌ Competition từ Ethereum, Solana, Sui
- ❌ FED hawkish → USD mạnh → crypto áp lực
- ❌ Geopolitical risk → risk-off → crypto bán trước
- ❌ Correlation cao với BTC (BTC giảm → BNB giảm)

### 2.5 BNB Price Forecast 2026

| Source | Range | Kịch bản |
|-------|-------|----------|
| CoinCodex / Standard Chartered | $1,300 – $2,100 | Base case |
| Coinpedia / DigitalCoinPrice | Lên tới $3,300 | Bull case |
| Investing Haven / Ambcrypto | < $1,100 | Bear case |
| Consensus moderate | $1,000 – $1,400 | Phổ biến nhất |
| Recovery target (04/2026) | $680 – $720 | Ngắn hạn |

---

## 3. COMPREHENSIVE CRYPTO ANALYSIS FRAMEWORK

### 3.1 Five-Step Process

```
Bước 1: MACRO CHECK
→ FED rate trend? (cắt = bullish, giữ/tăng = bearish)
→ USD Index (DXY)? DXY giảm = crypto tăng
→ Risk sentiment? (VIX, Fear & Greed Crypto)

Bước 2: ON-CHAIN ANALYSIS
→ MVRV ratio (< 1 = mua, > 3.5 = bán)
→ Exchange flow (outflow = bullish)
→ Whale accumulation patterns
→ NVT ratio (usage vs valuation)

Bước 3: TOKENOMICS
→ Supply dynamics (burn rate, emission)
→ Staking ratio (cao = less selling pressure)
→ Vesting schedule (team/VC unlock = selling pressure)

Bước 4: ECOSYSTEM HEALTH
→ TVL trend (tăng = adoption)
→ Daily active addresses
→ Transaction volume
→ Developer activity (GitHub commits)

Bước 5: TECHNICAL ANALYSIS
→ Áp dụng RSI, MACD, EMA, BB như cổ phiếu
→ Thêm: Fibonacci levels, Volume Profile
→ Bitcoin dominance (BTC.D) — nếu tăng = altcoins yếu
→ Funding rate (perpetual futures) — negative = oversold
```

### 3.2 Crypto Fear & Greed Index

**Source:** Alternative.me (0-100)

| Giá trị | State | Hành động |
|---------|-----------|-----------|
| 0-10 | 🟢🟢 Extreme Fear | Mua mạnh (lịch sử = đáy) |
| 10-25 | 🟢 Fear | Tích lũy DCA |
| 25-50 | 🟡 Neutral | Giữ nguyên |
| 50-75 | 🔴 Greed | Cẩn thận, giảm tỷ trọng |
| 75-100 | 🔴🔴 Extreme Greed | Chốt lời, giảm mạnh |

### 3.3 Bitcoin Dominance (BTC.D)

| BTC.D | Meaning cho Altcoins (BNB) |
|-------|---------------------------|
| > 60% & tăng | 🔴 Money flowing to BTC, alts weak → chờ |
| 50-60% | 🟡 Neutral |
| < 50% & giảm | 🟢 Alt season → BNB có thể outperform |
| BTC.D đỉnh + BTC tăng | 🟢 Tiền sắp chảy sang alts |

### 3.4 Funding Rate (Perpetual Futures)

| Funding | Meaning |
|---------|---------|
| > 0.1% | 🔴 Quá nhiều long → overheated |
| 0 – 0.05% | 🟡 Neutral |
| < 0% | 🟢 Nhiều short → potential squeeze up |
| < -0.1% | 🟢🟢 Extreme negative → bottom signal |

---

## 4. DCA CRYPTO — Accumulation Strategy

### 4.1 Allocation Within Crypto Portfolio
```
BTC:  50-60% — Store of value, lowest risk trong crypto
BNB:  20-30% — Ecosystem play, deflationary
ETH:  10-20% — DeFi + smart contracts
Others: 0-10% — High risk, high reward
```

### 4.2 When to Increase/Decrease Crypto DCA?
- **Tăng gấp đôi DCA khi:** Fear & Greed < 20, MVRV < 1, FED signal dovish
- **Giữ nguyên DCA khi:** Market neutral, macro stable
- **Giảm/dừng DCA khi:** Extreme Greed > 80, MVRV > 3, FED tăng lãi suất

### 4.3 Where to Buy in Vietnam
| Platform | BNB? | BTC? | Min | Fee |
|----------|------|------|-----|-----|
| Binance | ✅ | ✅ | $10 | 0.1% |
| OKX | ✅ | ✅ | $10 | 0.08% |
| Bybit | ✅ | ✅ | $1 | 0.1% |
| Gate.io | ✅ | ✅ | $1 | 0.2% |

**Lưu ý:** P2P VND → USDT → Mua BNB (phổ biến nhất cho người Việt)

---

## 5. MONITORING TOOLS

| Tool | Mục đích | Link |
|------|---------|------|
| Glassnode | On-chain metrics (MVRV, NVT) | glassnode.com |
| CryptoQuant | Exchange flows, whale | cryptoquant.com |
| DeFiLlama | TVL, protocol comparison | defillama.com |
| Alternative.me | Fear & Greed Index | alternative.me |
| CoinGecko | Price, market cap | coingecko.com |
| TradingView | Charts, TA | tradingview.com |
| BNBBurn.info | BNB burn tracker | bnbburn.info |

---

## 6. LESSONS LEARNED — Crypto Edition

### ❌ Common Mistakes
1. **FOMO mua đỉnh** khi Fear & Greed > 80 → luôn kiểm tra trước khi mua
2. **Không set stop-loss** → crypto có thể giảm 80%+ trong bear market
3. **All-in 1 coin** → diversify BTC/BNB/ETH
4. **Trade futures không có kinh nghiệm** → leverage 10x+ = cháy tài khoản nhanh
5. **Bỏ qua macro** → FED là driver #1 cho crypto

### ✅ Best Practices
1. **DCA hàng tháng, bất kể giá** → simple & effective
2. **Check MVRV trước khi mua lớn** → < 1 = cơ hội hiếm
3. **Theo dõi BTC trước** → BTC dẫn dắt, alts theo sau
4. **Giữ trên cold wallet** (Ledger, Trezor) nếu hold dài hạn
5. **Không đầu tư tiền cần dùng trong 1-2 năm**

---

*This framework combines with technical analysis in SKILL.md for comprehensive crypto analysis.*
