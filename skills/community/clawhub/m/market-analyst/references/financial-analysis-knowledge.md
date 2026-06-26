# Financial Analysis Knowledge Base
> Self-study & compilation — continuously updated during usage

---

## 1. TECHNICAL ANALYSIS

### 1.1 Momentum Indicators

#### RSI — Relative Strength Index
**Công thức:** RSI = 100 - (100 / (1 + RS)) | RS = Avg Gain / Avg Loss (14 kỳ)

| Vùng | Ý nghĩa | Hành động |
|---|---|---|
| < 30 | Oversold cực mạnh | Xem xét mua, tìm điểm đảo chiều |
| 30–40 | Oversold | Bắt đầu theo dõi, DCA |
| 40–60 | Neutral | Giữ nguyên |
| 60–70 | Overbought nhẹ | Cân nhắc chốt lời một phần |
| > 70 | Overbought mạnh | Không thêm vị thế mới |

**Lesson learned:** RSI oversold KHÔNG đảm bảo giá sẽ tăng ngay — có thể oversold và tiếp tục giảm (bearish momentum). Cần kết hợp EMA200.

**RSI Divergence (quan trọng):**
- **Bullish divergence:** Giá tạo đáy mới thấp hơn, RSI tạo đáy cao hơn → tín hiệu đảo chiều tăng mạnh
- **Bearish divergence:** Giá tạo đỉnh mới cao hơn, RSI tạo đỉnh thấp hơn → tín hiệu đảo chiều giảm

#### MACD — Moving Average Convergence Divergence
**Công thức:** MACD = EMA(12) - EMA(26) | Signal = EMA(9) của MACD

| Tín hiệu | Ý nghĩa |
|---|---|
| MACD > Signal | Bullish momentum |
| MACD < Signal | Bearish momentum |
| MACD cắt lên Signal | Mua (Golden Cross MACD) |
| MACD cắt xuống Signal | Bán (Death Cross MACD) |
| MACD dương & tăng | Uptrend mạnh |
| MACD âm & giảm | Downtrend mạnh |

#### Stochastic Oscillator
**Công thức:** %K = (Close - Lowest Low) / (Highest High - Lowest Low) × 100

| Vùng | Ý nghĩa |
|---|---|
| < 20 | Oversold |
| > 80 | Overbought |
| %K cắt lên %D ở vùng < 20 | Mua mạnh |
| %K cắt xuống %D ở vùng > 80 | Bán mạnh |

---

### 1.2 Trend Indicators

#### EMA — Exponential Moving Average
**EMA nhanh hơn SMA** (ưu tiên giá gần đây hơn)

| EMA | Ý nghĩa | Dùng cho |
|---|---|---|
| EMA20 | Trend ngắn hạn (1 tháng) | Trader |
| EMA50 | Trend trung hạn (2-3 tháng) | Swing trader |
| EMA200 | Trend dài hạn (1 năm) | Investor |

**Golden rule:**
- Giá > EMA200: Long-term uptrend còn nguyên → **BUY bias**
- Giá < EMA200: Long-term downtrend → **cẩn thận**
- EMA20 cắt lên EMA50 = Golden Cross → tín hiệu tích cực
- EMA20 cắt xuống EMA50 = Death Cross → tín hiệu tiêu cực

**Lesson learned from practice:**
- FPT: RSI 31 (oversold) nhưng giá -21% dưới EMA200 → KHÔNG mua dù RSI oversold
- BAF: RSI 33 + Trên EMA200 → Combo tốt, hội đủ điều kiện mua
- Luôn kiểm tra EMA200 TRƯỚC khi quyết định mua cổ phiếu oversold

#### Bollinger Bands
**Công thức:** Middle = SMA(20) | Upper = SMA(20) + 2σ | Lower = SMA(20) - 2σ

| Tín hiệu | Ý nghĩa |
|---|---|
| Giá chạm BB Lower | Tiềm năng bounce ngắn hạn |
| Giá chạm BB Upper | Tiềm năng điều chỉnh |
| Bands co lại (squeeze) | Sắp có biến động mạnh |
| Bands mở rộng | Trend đang mạnh |

---

### 1.3 Volume Analysis
- **Volume tăng + giá tăng** = Uptrend khỏe mạnh (xác nhận xu hướng)
- **Volume tăng + giá giảm** = Bán mạnh, tránh bắt đáy
- **Volume giảm + giá tăng** = Uptrend yếu, không bền
- **Volume thấp bất thường** = Thiếu thanh khoản, khó thoát lệnh

---

## 2. FUNDAMENTAL ANALYSIS

### 2.1 Valuation Metrics

#### P/E — Price to Earnings Ratio
**Công thức:** P/E = Giá cổ phiếu / EPS (Thu nhập trên mỗi cổ phiếu)

**How to read:**
- P/E = 10x: Nhà đầu tư trả 10đ để mua 1đ lợi nhuận
- P/E thấp = rẻ (tương đối) | P/E cao = đắt hoặc kỳ vọng tăng trưởng cao

**P/E theo ngành VN:**
| Ngành | P/E hợp lý | Ghi chú |
|---|---|---|
| Ngân hàng | 8–12x | Rẻ so với khu vực |
| Công nghệ (FPT) | 18–25x | Premium cho tăng trưởng |
| Thép | 6–12x | Cyclical |
| Tiêu dùng | 15–22x | Ổn định |
| BĐS | 10–20x | Biến động theo chu kỳ |

**⚠️ Low P/E Trap:**
- P/E thấp vì earnings bất thường cao (sắp giảm) → "Value trap"
- Ví dụ: Thép P/E = 5x khi giá thép đỉnh → earnings sẽ giảm → P/E thực cao hơn

**⚠️ Historical CAGR Trap:**
- MCH CAGR 73.6%/năm từ đáy 2023 → không có nghĩa sẽ tiếp tục từ giá cao hiện tại
- Luôn hỏi: "Nếu mua HÔM NAY, P/E là bao nhiêu?"

#### P/B — Price to Book Value
**Công thức:** P/B = Giá cổ phiếu / Giá trị sổ sách mỗi cổ phiếu

- P/B < 1: Giá thấp hơn tài sản ròng (có thể rẻ hoặc có vấn đề)
- P/B 1–2x: Hợp lý cho ngân hàng
- P/B > 3x: Đắt, cần tăng trưởng cao để justify

#### PEG — Price/Earnings to Growth
**Công thức:** PEG = P/E / EPS Growth Rate

- PEG < 1: Rẻ tương đối (P/E thấp hơn tốc độ tăng trưởng)
- PEG = 1: Fair value
- PEG > 2: Đắt

**Ví dụ:** FPT P/E 22x, EPS growth 20%/năm → PEG = 22/20 = 1.1 → Fair

#### EV/EBITDA
**Công thức:** EV/EBITDA = Enterprise Value / EBITDA

- Tốt hơn P/E vì không bị ảnh hưởng bởi cấu trúc nợ và thuế
- Thép, BĐS thường dùng chỉ số này
- EV/EBITDA < 8x = rẻ (cyclical) | < 15x = hợp lý (growth)

---

### 2.2 Profitability Metrics

#### ROE — Return on Equity
**Công thức:** ROE = Net Income / Shareholders' Equity × 100%

| Mức | Đánh giá |
|---|---|
| < 10% | Kém |
| 10–15% | Trung bình |
| 15–20% | Tốt |
| > 20% | Xuất sắc |

**Ngân hàng VN tốt:** VCB ROE ~22%, MBB ROE ~22%, TCB ROE ~18%

**Chú ý:** ROE cao có thể do đòn bẩy cao (vay nhiều) → kiểm tra D/E ratio

#### ROA — Return on Assets
**Công thức:** ROA = Net Income / Total Assets × 100%
- Ngân hàng: ROA > 1.5% = tốt
- Sản xuất: ROA > 5% = tốt

#### EBITDA Margin
**Công thức:** EBITDA / Revenue × 100%
- Thước đo sinh lời hoạt động thuần túy
- Loại bỏ ảnh hưởng của thuế, lãi vay, khấu hao
- > 20% = tốt | > 30% = xuất sắc

#### Gross Margin (Biên lợi nhuận gộp)
**Công thức:** (Revenue - COGS) / Revenue × 100%
- Phản ánh lợi thế cạnh tranh của sản phẩm
- MCH: ~45% (cao → thương hiệu mạnh)
- Thép: ~15% (thấp → commodity)

---

### 2.3 Financial Health

#### Debt/Equity (D/E)
**Công thức:** D/E = Total Debt / Shareholders' Equity
- D/E < 1: Ít nợ, an toàn
- D/E 1–2x: Bình thường
- D/E > 3x: Nhiều nợ, rủi ro (trừ ngân hàng vì bản chất kinh doanh)

#### Interest Coverage Ratio
**Công thức:** ICR = EBIT / Interest Expense
- ICR > 3x: Tốt (lợi nhuận gấp 3 lần lãi vay)
- ICR < 1.5x: Nguy hiểm

#### Current Ratio (Thanh khoản ngắn hạn)
**Công thức:** Current Assets / Current Liabilities
- > 2x: Tốt | 1–2x: Chấp nhận | < 1x: Rủi ro

#### Free Cash Flow (FCF)
**FCF = Operating Cash Flow - CapEx**
- FCF dương = công ty sinh tiền thực
- FCF âm kéo dài = cẩn thận (đang đốt tiền)
- FCF Yield = FCF / Market Cap → > 5% = hấp dẫn

---

### 2.4 Growth Metrics

#### Revenue Growth (Tăng trưởng doanh thu)
- > 20%/năm: Tốt (growth stock)
- 10–20%: Khá
- < 10%: Chậm (defensive/mature)

#### EPS CAGR — Compound Annual Growth Rate of EPS
**Công thức:** (EPS_n / EPS_0)^(1/n) - 1

- Đây là driver chính của giá cổ phiếu dài hạn
- P/E × EPS = Giá cổ phiếu
- Nếu EPS tăng 20%/năm và P/E giữ nguyên → giá tăng 20%/năm

---

## 3. RISK METRICS

### 3.1 Volatility
**Công thức:** Standard deviation của daily returns × √252 (annualized)

| Mức | Classification |
|---|---|
| < 15%/năm | Thấp (ngân hàng lớn, tiện ích) |
| 15–25% | Trung bình |
| 25–40% | Cao (hầu hết cổ phiếu VN) |
| > 40% | Rất cao (penny stocks) |

### 3.2 Sharpe Ratio
**Công thức:** (Return - Risk-free rate) / Volatility
- Risk-free rate VN: ~5.5% (lãi suất ngân hàng)

| Sharpe | Đánh giá |
|---|---|
| < 0 | Tệ (thua gửi ngân hàng) |
| 0–0.5 | Kém |
| 0.5–1.0 | Chấp nhận được |
| 1.0–2.0 | Tốt |
| > 2.0 | Xuất sắc |

**Lesson learned:** Sharpe của MCH là 2.19 từ đáy 2023 — nhưng Sharpe tính BACKWARD từ giá thấp. Người mua ở 161,000 VND hiện tại có Sharpe kỳ vọng thấp hơn nhiều.

### 3.3 Max Drawdown
**Công thức:** (Trough - Peak) / Peak × 100%

| Mức drawdown | Ý nghĩa |
|---|---|
| -10 đến -20% | Bình thường (correction) |
| -20 đến -40% | Bear market |
| -40 đến -60% | Khủng hoảng nghiêm trọng |
| > -60% | Nguy hiểm (HPG -72%, TCB -64%) |

**Quy tắc:** Max Drawdown càng lớn → cần tâm lý càng vững → phân bổ vốn ít hơn

### 3.4 Beta
**Công thức:** Covariance(Stock, Market) / Variance(Market)

| Beta | Ý nghĩa |
|---|---|
| < 0.5 | Ít biến động hơn thị trường |
| 0.5–1.0 | Ít biến động hơn thị trường |
| = 1.0 | Biến động bằng thị trường |
| > 1.5 | Biến động mạnh hơn thị trường (high risk/reward) |

---

## 4. COMPREHENSIVE ANALYSIS FRAMEWORK

### 4.1 Five-Step Process

```
Bước 1: SCREENING
→ Scan RSI < 40, Volume > 500K, Exchange HOSE/HNX
→ Loại bỏ mã dưới EMA200 (trừ khi có catalyst đặc biệt)

Bước 2: VALUATION CHECK
→ P/E hiện tại vs P/E lịch sử vs ngành
→ PEG < 1.5 là hợp lý
→ KHÔNG mua khi P/E > 40x (trừ high-growth với EPS CAGR > 30%)

Bước 3: FUNDAMENTAL QUALITY
→ ROE > 15%
→ D/E hợp lý (theo ngành)
→ FCF dương
→ Revenue/EPS growth trend

Bước 4: CATALYST
→ Điều gì sẽ làm giá tăng trong 1-3 năm tới?
→ Nâng hạng thị trường, expansion, chu kỳ ngành, lãi suất...

Bước 5: SIZING
→ Sharpe > 1.0 → 25-35% danh mục
→ Sharpe 0.5-1.0 → 15-25%
→ Sharpe < 0.5 → < 15%
→ Max Drawdown > 60% → < 10%
```

### 4.2 Scoring System (Applied in Skill)

| Tiêu chí | Điểm | Điều kiện |
|---|---|---|
| RSI < 30 | +3 | Oversold cực mạnh |
| RSI 30-40 | +2 | Oversold |
| Trên EMA200 | +2 | Long-term uptrend intact |
| P/E < Fair P/E | +3 | Định giá hấp dẫn (>20% discount) |
| P/E gần Fair | +2 | Hợp lý (0-20% discount) |
| Dưới BB Lower | +2 | Tiềm năng bounce |
| 52W position < 30% | +2 | Gần đáy 52 tuần |
| MACD bullish | +1 | Momentum cải thiện |
| **Tổng tối đa** | **17** | |

**Recommendations:**
- Score 10+: Mua mạnh
- Score 7-9: Mua tích lũy (DCA)
- Score 4-6: Theo dõi
- Score < 4: Không quan tâm

---

## 5. CENTRAL BANKS & MACRO

### Interest Rate Impact on Stocks
- **Lãi suất giảm** → Chi phí vốn giảm → Doanh nghiệp lợi nhuận tăng → CK tăng
- **Lãi suất tăng** → DCF valuation giảm → P/E hợp lý thấp hơn → CK giảm
- **Quy tắc ngón tay cái:** Lãi suất tăng 1% → P/E hợp lý giảm ~1-2x

### Macro Indicators to Monitor for VN
| Chỉ số | Tốt cho CK | Xấu cho CK |
|---|---|---|
| GDP growth | > 6% | < 5% |
| Lạm phát (CPI) | 2-4% | > 6% |
| Tín dụng tăng trưởng | 14-16% | < 10% hoặc > 20% |
| Tỷ giá VND/USD | Ổn định | Mất giá mạnh > 5% |
| FDI | Tăng | Giảm |
| Xuất khẩu | Tăng | Giảm |

---

## 6. LESSONS LEARNED (From Practical Analysis)

### ❌ Mistakes to Avoid
1. **Mua chỉ vì RSI oversold** — cần kết hợp EMA200 và định giá
2. **Dùng CAGR lịch sử để dự báo tương lai** — MCH CAGR 73%/năm từ đáy không apply cho người mua ở đỉnh
3. **Bỏ qua valuation** — Sharpe cao là lịch sử, không phải tương lai
4. **Overweight 1 mã** — dù MCH/MBB tốt, không nên >40% danh mục
5. **Không có stop loss** — luôn biết mức nào sẽ cut loss

### ✅ Best Practices
1. **Kết hợp ít nhất 3 tín hiệu** trước khi quyết định
2. **Luôn hỏi "Tại sao rẻ?"** — có lý do chính đáng hay là "value trap"
3. **DCA theo thời gian** — không all-in một lúc
4. **Review định kỳ** — thị trường thay đổi, thesis có thể sai
5. **So sánh với benchmark** — beat VN-Index mới gọi là tốt

---

*This document is continuously updated during practical analysis. Each new lesson learned → recorded here.*

---

## 7. DCA — DOLLAR COST AVERAGING

### 7.1 Why Is DCA More Effective Than Lump Sum?

**Lump Sum** (bỏ vào một lần):
- Rủi ro mua đúng đỉnh → lỗ ngay từ đầu
- Cần vốn lớn ban đầu
- Tâm lý khó: sợ mua sai thời điểm

**DCA** (tích lũy hàng tháng):
- Mua cả khi giá cao lẫn khi giá thấp → giá trung bình tối ưu
- Không cần vốn lớn ban đầu
- Tâm lý dễ: cứ mua đều đặn, không cần đoán thị trường
- **Compounding effect bùng nổ từ năm 8-10 trở đi**

### 7.2 DCA Calculation Formula

```python
def dca_simulate(monthly_invest, annual_return, years):
    monthly_return = (1 + annual_return) ** (1/12) - 1
    total = 0
    for month in range(years * 12):
        total = (total + monthly_invest) * (1 + monthly_return)
    invested = monthly_invest * 12 * years
    return total, invested
```

### 7.3 Practical Benchmarks (1 triệu VND/tháng)

| Thời gian | Đã bỏ vào | NH 5.5% | S&P 500 18% | VN tốt 30% | Mix 22% |
|---|---|---|---|---|---|
| 1 năm | 12tr | 12.4tr | 13.1tr | 13.9tr | 14.2tr |
| 3 năm | 36tr | 39.1tr | 46.9tr | 55.3tr | 59.1tr |
| 5 năm | 60tr | 69tr | 94tr | 125tr | 141tr |
| 10 năm | 120tr | 159tr | 309tr | 591tr | 384tr |
| 15 năm | 180tr | 277tr | 801tr | 2,321tr | 1,274tr |
| 20 năm | 240tr | 431tr | 1,927tr | 8,742tr | 2,996tr |

**Insight quan trọng:** Compound bùng nổ từ năm 10. Người bắt đầu sớm 5 năm = lợi thế khổng lồ.

### 7.4 DCA Rules

1. **Mua ngày cố định hàng tháng** (VD: ngày 1 hoặc ngày lương) — không cần chọn thời điểm
2. **Không dừng lại khi thị trường giảm** — đây là cơ hội mua rẻ hơn
3. **Tăng gấp đôi khi thị trường giảm > 20%** — "sale" lớn nhất trong năm
4. **Không tăng khi thị trường tăng mạnh** — tránh FOMO
5. **Tái đầu tư cổ tức** — không rút ra, để compound

### 7.5 DCA Allocation by Monthly Capital

**Recommended global DCA portfolio:**
```
S&P 500 ETF (VOO/IVV):    40% — Core, ổn định, dễ mua
Cổ phiếu VN (MBB/TCB):   30% — Upside VN, nâng hạng thị trường
Vàng (SJC/DOJI):          20% — Hedge, bảo toàn vốn
Bitcoin:                   10% — High risk, long-term hold
```

**Where to buy in Vietnam:**
| Tài sản | Nơi mua | Tối thiểu |
|---|---|---|
| Vàng nhẫn | SJC/DOJI/PNJ | ~100k |
| Cổ phiếu VN | VNDirect/SSI/MBS App | ~100k (lô lẻ) |
| S&P 500 ETF | Exness, Interactive Brokers | $1 |
| Bitcoin | Binance, OKX | $10 |

### 7.6 Estimate by Accumulation Level (10 năm, mix 22%/năm)

| Tháng/tháng | Bỏ vào 10Y | Kết quả | Lãi ròng |
|---|---|---|---|
| 500k | 60tr | 192tr | +132tr |
| 1tr | 120tr | 384tr | +264tr |
| 2tr | 240tr | 767tr | +527tr |
| 3tr | 360tr | 1.15 tỷ | +791tr |
| 5tr | 600tr | 1.92 tỷ | +1.32 tỷ |

### 7.7 Lesson: Starting Early Matters More Than Amount

**Kịch bản A:** Bắt đầu 25 tuổi, 1tr/tháng, 30 năm → **~5.2 tỷ** (mix 22%)
**Kịch bản B:** Bắt đầu 35 tuổi, 3tr/tháng, 20 năm → **~3 tỷ** (mix 22%)

→ Dù B bỏ vào gấp 3 lần/tháng nhưng bắt đầu muộn 10 năm vẫn thua A.
**"The best time to start was yesterday. The second best time is now."**

---

## 8. GLOBAL INVESTMENT PORTFOLIO

### 8.1 Global Assets Ranked by Sharpe (3 năm, Q1 2026)

| Tài sản | CAGR | Sharpe | Max DD | Notes |
|---|---|---|---|---|
| Vàng (XAU/USD) | +33.8% | **1.52** 🏆 | -14% | Best risk-adjusted globally |
| MBB (VN Bank) | +41.3% | **1.16** ⭐ | -51% | VN best pick |
| Nikkei 225 | +28.0% | 0.97 | -26% | Japan breakout khỏi deflation |
| Nasdaq 100 | +23.9% | 0.93 | -24% | US tech stable |
| S&P 500 | +18.9% | 0.91 | -19% | Safest core holding |
| TCB (VN Bank) | +34.3% | 0.88 | -64% | High DD risk |
| BAF (VN Agri) | +36.0% | 0.84 | -54% | Cyclical |
| Bitcoin | +35.3% | 0.65 | -49% | High risk/reward |
| VCB (VN Bank) | +7.5% | 0.08 | -35% | Underperform — tránh |

### 8.2 Optimal Global Portfolio for VN Investors

**Conservative (ưu tiên an toàn):**
```
Vàng:         35% — Sharpe tốt nhất, hedge lạm phát
S&P 500 ETF:  30% — Core ổn định
Nikkei 225:   15% — Asia diversification
MBB (VN):     10% — VN upside
Bitcoin:      10% — Small crypto bet
```

**Balanced (cân bằng):**
```
Vàng:         25%
S&P 500 ETF:  20%
MBB (VN):     20%
Nasdaq 100:   15%
TCB/BAF (VN): 10%
Bitcoin:      10%
```

**Aggressive (tối đa hóa return):**
```
MBB + TCB (VN): 35%
Nasdaq 100:     25%
Vàng:           20%
Bitcoin:        15%
S&P 500:         5%
```

### 8.3 Diversification Principles

- **Không bỏ > 35% vào 1 tài sản** dù Sharpe có tốt đến đâu
- **Kết hợp tài sản ít tương quan** (vàng thường ngược chiều cổ phiếu)
- **Rebalance 6 tháng/lần** — cắt bớt tài sản tăng mạnh, mua thêm tài sản giảm
- **Core + Satellite:** 60-70% tài sản ổn định (vàng, S&P 500) + 30-40% high growth


---

## 9. MACRO FACTORS — FED, INTEREST RATES, INVESTOR SENTIMENT

### 9.1 FED & FOMC

**FOMC họp 8 lần/năm** — quyết định lãi suất Fed Funds Rate (FFR).
Lịch 2026: Jan, **Mar 17-18**, Apr 28-29, Jun 16-17, Jul, Sep, Oct, Dec

**FED Statement mới nhất — 18/03/2026:**
- ✅ **GIỮ NGUYÊN lãi suất 3.5% – 3.75%**
- Kinh tế vẫn tăng trưởng ổn định
- Lạm phát vẫn "somewhat elevated" — chưa đủ điều kiện cắt giảm
- Rủi ro Trung Đông tạo bất ổn
- 1 thành viên (Miran) muốn cắt -0.25% nhưng bị phủ quyết
- **Tín hiệu:** FED không vội cắt lãi suất → neutral/hawkish

**Tại sao thị trường giảm hôm nay (19/3)?**
FED giữ nguyên nhưng thị trường kỳ vọng tín hiệu cắt giảm sớm hơn → thất vọng → bán tháo.

### 9.2 Interest Rate Impact on Each Asset

| Lãi suất | Cổ phiếu | Vàng | Crypto | Trái phiếu | VND |
|---|---|---|---|---|---|
| **Tăng** | 📉 Giảm (P/E compression) | 📉 Giảm | 📉 Giảm mạnh | 📉 Giảm | 📈 Mạnh lên |
| **Giữ** | 🔄 Neutral | 🔄 Neutral | 🔄 Neutral | 🔄 Neutral | 🔄 Neutral |
| **Giảm** | 📈 Tăng | 📈 Tăng | 📈 Tăng mạnh | 📈 Tăng | 📉 Yếu đi |

**FFR hiện tại: 3.5-3.75%**
Market kỳ vọng cắt lần đầu: Q3/Q4 2026
→ Nếu FED cắt lãi suất → P/E hợp lý cao hơn → CK tăng

### 9.3 Fear & Greed Index — Market Sentiment

**Nguồn:** CNN Fear & Greed Index (0-100)
- 0-25: **Extreme Fear** 🔴 → thường là đáy, cơ hội mua
- 25-45: **Fear** 🟡
- 45-55: **Neutral** ⬜
- 55-75: **Greed** 🟢
- 75-100: **Extreme Greed** 🔴 → thường là đỉnh, cẩn thận

**Lesson:** Warren Buffett: *"Be fearful when others are greedy, and greedy when others are fearful"*

**VIX — Volatility Index (Fear gauge của S&P 500)**
- VIX < 15: Thị trường bình tĩnh, tự tin
- VIX 15-25: Lo ngại trung bình
- VIX > 30: Sợ hãi → thường là cơ hội mua
- VIX > 40: Khủng hoảng → mua mạnh nếu có tiền

### 9.4 Key Macro Events to Monitor

| Sự kiện | Tần suất | Tác động |
|---|---|---|
| FOMC Meeting | 8 lần/năm | ⭐⭐⭐⭐⭐ Lớn nhất |
| CPI (Lạm phát Mỹ) | Hàng tháng | ⭐⭐⭐⭐ |
| Non-Farm Payrolls (Việc làm Mỹ) | Thứ 6 đầu tháng | ⭐⭐⭐⭐ |
| GDP Mỹ | Hàng quý | ⭐⭐⭐ |
| Kết quả kinh doanh (Earnings Season) | Hàng quý | ⭐⭐⭐ |
| NHNN VN họp | 2 lần/năm | ⭐⭐⭐ (cho VN stocks) |
| Địa chính trị (Trung Đông, Đài Loan) | Bất định | ⭐⭐⭐ |

### 9.5 Vietnam Interest Rates

**NHNN Việt Nam:**
- Lãi suất điều hành hiện tại: ~4.5%
- Lãi suất huy động ngân hàng: 4.5-5.5%/năm
- Xu hướng: Giảm nhẹ theo FED để hỗ trợ tăng trưởng

**Tác động lãi suất VN giảm:**
- ✅ Ngân hàng: NIM cải thiện, chi phí vốn thấp hơn → lợi nhuận tăng → MBB, TCB, VCB hưởng lợi
- ✅ BĐS: Người mua vay dễ hơn → VHM, DXG tăng
- ✅ Cổ phiếu nói chung: Định giá P/E hợp lý cao hơn

### 9.6 Investor Sentiment Analysis

**Chỉ số cần theo dõi:**
1. **VIX** (fear gauge Mỹ) — ảnh hưởng gián tiếp VN
2. **Margin debt** — nhà đầu tư dùng đòn bẩy nhiều = thị trường quá nóng
3. **Put/Call ratio** — > 1.2 = nhiều người mua put (hedge/bear) → cơ hội mua
4. **Short interest** — cổ phiếu bị short nhiều, nếu tin tốt → short squeeze
5. **Insider buying** — ban lãnh đạo tự mua cổ phiếu công ty = tín hiệu mạnh

**Cho VN thêm:**
- **Khối ngoại mua ròng/bán ròng** (HOSE daily data)
- **Margin call pressure** khi thị trường giảm mạnh
- **Thanh khoản thị trường** — khối lượng giao dịch giảm = ít nhà đầu tư tham gia

### 9.7 Direct Impact on Eddie's Portfolio

**FED giữ 3.5-3.75% (hôm nay):**
- S&P 500, Nasdaq giảm → tác động tâm lý lan sang VN, crypto
- BNB giảm tiếp vì crypto nhạy cảm với lãi suất cao
- FPT giảm một phần do sentiment toàn cầu

**Nếu FED cắt lãi suất (dự kiến Q3/Q4 2026):**
- BNB có thể bật mạnh (crypto lên khi USD yếu)
- MBB/TCB hưởng lợi (ngân hàng VN)
- S&P 500 tăng → portfolio mix cải thiện

**→ Chiến lược: Tích lũy MBB + S&P 500 ETF hiện tại, chờ FED cắt lãi suất = catalyst chính**


---

## 10. PORTFOLIO REBALANCING

### 10.1 When to Rebalance?

- **Tỷ trọng lệch > 10%** so với mục tiêu (VD: FPT từ 30% → 38%)
- **Macro thay đổi** (FED cắt/tăng lãi suất, suy thoái, chiến tranh)
- **Fundamental thay đổi** (P/E đột ngột đắt, Sharpe giảm mạnh)
- **Định kỳ** mỗi 6 tháng — dù thị trường bình thường

### 10.2 Rebalancing Principles

1. **Cắt tài sản đã tăng mạnh** → overweight → bán bớt về target %
2. **Mua thêm tài sản đang rẻ** → underweight → tăng về target %
3. **Không bán lỗ để rebalance** nếu fundamental vẫn tốt — chỉ dùng tiền mới
4. **Dùng DCA hàng tháng để rebalance dần** thay vì all-in một lúc

### 10.3 Macro-Based Decision Framework

```
FED HAWKISH (giữ/tăng lãi suất):
→ Tích lũy: Vàng, S&P 500 ETF (pre-cut positioning)
→ Tránh: Crypto, growth stocks (nhạy lãi suất cao)
→ Ngân hàng VN: neutral (tín dụng khó tăng)

FED DOVISH (cắt lãi suất):
→ Tích lũy: Crypto (BTC/BNB), S&P 500, Ngân hàng VN
→ Vàng: có thể chốt lời một phần (USD yếu nhưng có thể điều chỉnh)
→ MBB/TCB: mua mạnh (NIM cải thiện, tín dụng tăng)

GEOPOLITICAL RISK CAO:
→ Tăng Vàng, giảm risk assets
→ Crypto thường giảm trong giai đoạn đầu bất ổn

INFLATION TĂNG:
→ Vàng, BĐS, hàng hóa (commodity stocks: HPG, GAS)
→ Giảm trái phiếu, cash
```

### 10.4 Lesson from Eddie's Portfolio (19/03/2026)

**Vấn đề phát hiện:**
- FPT 38% → overweight, dưới EMA200, downtrend
- VCB P/E đắt hơn fair value, Sharpe 0.09
- BNB -51% vì FED hawkish, crypto nhạy lãi suất
- Thiếu diversification quốc tế (100% VN + Crypto)

**Điều chỉnh đúng:**
- Cắt VCB (đắt, Sharpe tệ) → Mua MBB (rẻ, Sharpe tốt) + Vàng (hedge)
- Thêm S&P 500 ETF (trước khi FED cắt = pre-cut positioning)
- Giữ BNB (không bán lỗ -51%, chờ FED cắt = catalyst recovery)
- Giảm FPT dần khi giá phục hồi (không bán lúc RSI oversold)

**Catalyst chờ đợi: FED cắt lãi suất Q3/Q4 2026**
→ Sẽ kích hoạt: BNB +50-100%, S&P 500 +15-20%, MBB +20-30%

### 10.5 Target Portfolio After Rebalance

| Tài sản | % Mục tiêu | Lý do |
|---|---|---|
| MBB | 28% | P/E 7x, FED cut = ngân hàng hưởng lợi |
| S&P 500 ETF | 14% | Pre-cut positioning, diversification |
| Vàng | 12% | Hedge hawkish FED, geopolitical risk |
| FPT | 21% | Giảm concentration, giữ dài hạn |
| BNB | 15% | Hold, chờ FED cut |
| VCB | 5% | Giảm mạnh (đắt, Sharpe tệ) |
| Tiết kiệm | 6% | Emergency fund |


---

## 11. GEOPOLITICAL RISK

### 11.1 Hottest Event 19/03/2026 — Iran War

**Actual situation (AP News):**
- Israel tấn công Iran: phá hủy kho dầu, nhà máy lọc dầu tại Tehran
- Mỹ có 7 quân nhân thiệt mạng trong chiến tranh Iran
- Iran đe dọa tấn công mục tiêu Mỹ thêm
- Mojtaba Khamenei (con trai) vừa được bổ nhiệm Lãnh tụ Tối cao mới
- Dầu WTI: **$95.77/thùng** (đang ở mức cao, dao động $94-99 hôm nay)

**FED đã nhắc đến trong statement 18/3:** *"The implications of developments in the Middle East for the U.S. economy are uncertain"*

### 11.2 Iran War Impact on Assets

| Tài sản | Tác động | Lý do |
|---|---|---|
| **Dầu WTI/Brent** | 📈 Tăng mạnh | Iran = 3.5M thùng/ngày, Eo Hormuz rủi ro |
| **Vàng** | 📈 Tăng | Safe haven, USD không chắc |
| **S&P 500** | 📉 Giảm | Chi phí năng lượng tăng → lạm phát → FED hawkish hơn |
| **Crypto** | 📉 Giảm | Risk-off sentiment |
| **GAS (PV Gas VN)** | 📈 Tiềm năng | Giá dầu cao → doanh thu tăng |
| **PLX (Petrolimex)** | 🔄 Neutral | Giá bán xăng điều chỉnh theo nhà nước |
| **HPG (Hòa Phát)** | 📉 Áp lực | Chi phí năng lượng sản xuất tăng |
| **Hàng không (HVN)** | 📉 Giảm | Nhiên liệu bay chiếm 30-40% chi phí |

**Dầu $95-100+: Tác động chuỗi:**
```
Dầu tăng → Lạm phát tăng → FED giữ lãi suất cao hơn lâu hơn
→ S&P 500 giảm → Tâm lý nhà đầu tư sợ → Crypto giảm → BNB giảm
→ Nhưng: Vàng tăng, cổ phiếu dầu khí tăng
```

### 11.3 Geopolitical Hotspots to Monitor 2026

| Khu vực | Sự kiện | Tài sản ảnh hưởng |
|---|---|---|
| **🔴 Trung Đông** | Israel-Iran war đang diễn ra | Dầu ↑, Vàng ↑, CK Mỹ ↓ |
| **🔴 Đài Loan** | Căng thẳng Mỹ-Trung | Chip, tech ↓, Vàng ↑ |
| **🟡 Ukraine-Nga** | Chiến tranh kéo dài | Khí đốt EU ↑, Lúa mì ↑ |
| **🟡 Biển Đông** | Căng thẳng Việt Nam-TQ | VN-Index ↓ khi leo thang |
| **🟢 Mỹ bầu cử 2026** | Midterm elections | Policy uncertainty |

### 11.4 Geopolitical Risk Analysis Framework

**Risk Level → Portfolio Action:**

```
🔴 HIGH RISK (chiến tranh lớn, sanctions mới):
→ Tăng Vàng lên 20-25%
→ Giảm Crypto về 5-8%
→ Mua thêm dầu khí (GAS, PLX nếu ở VN)
→ Giảm hàng không, tiêu dùng

🟡 MEDIUM RISK (căng thẳng leo thang nhưng chưa chiến tranh):
→ Giữ nguyên danh mục
→ Tăng tỷ lệ cash/tiết kiệm lên 15%
→ Tránh mở vị thế mới lớn

🟢 LOW RISK (đàm phán, hòa giải):
→ Giảm Vàng → tái phân bổ vào CK
→ Mua thêm Crypto (risk-on)
→ Tăng S&P 500
```

### 11.5 Specific Impact on Eddie's Portfolio

**Với Iran War đang diễn ra:**

| Tài sản Eddie | Tác động | Hành động |
|---|---|---|
| FPT | ⬇️ Nhẹ (sentiment) | Giữ nguyên |
| MBB | ↔️ Neutral | Tiếp tục tích lũy |
| VCB | ↔️ Neutral | Vẫn nên giảm (P/E đắt) |
| BNB | ⬇️ Risk-off pressure | Giữ, không thêm |
| **Vàng** *(chưa có)* | ⬆️ Strong buy | **Ưu tiên mua Vàng trước** |
| **S&P 500** *(chưa có)* | ⬇️ Ngắn hạn | DCA bình thường, không panic |

**Điều chỉnh kế hoạch tháng 3:**
```
Thay vì: MBB 10tr + Vàng 10tr
Nên:     Vàng 13tr + MBB 7tr
→ Ưu tiên Vàng cao hơn vì Iran War = geopolitical hedge cần thiết
```

### 11.6 Geopolitical News Sources

Fetch tự động từ:
- **AP News Iran:** `https://apnews.com/hub/iran`
- **AP News World:** `https://apnews.com/world-news`
- **Dầu WTI real-time:** `https://stooq.com/q/l/?s=cl.f`
- **Vàng real-time:** `https://stooq.com/q/l/?s=xauusd`

**Oil alert thresholds:**
- WTI > $100: Cảnh báo lạm phát, FED sẽ hawkish hơn → giảm CK
- WTI > $120: Khủng hoảng năng lượng → tăng Vàng mạnh
- WTI < $70: Rủi ro giảm, có thể giảm Vàng

