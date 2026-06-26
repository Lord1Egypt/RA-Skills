# VN Stock Swing Trading & Scalping

> Reference guide for swing trading analysis in the Vietnamese market.
> Updated: 2026-03-23

---

## 1. Swing Trading VN (Hold 2–10 Days)

### 1.1 Entry/Exit Signals

#### RSI Divergence

RSI divergence is the strongest signal for swing trading, especially on D1 chart.

**Bullish Divergence:**
- Giá tạo đáy thấp hơn (lower low), nhưng RSI tạo đáy cao hơn (higher low)
- → Lực bán suy yếu, giá sắp đảo chiều tăng
- **Ví dụ:** MBB giảm từ 22k xuống 18k (lower low), RSI từ 28 lên 35 (higher low) → buy signal

**Bearish Divergence:**
- Giá tạo đỉnh cao hơn (higher high), nhưng RSI tạo đỉnh thấp hơn (lower high)
- → Lực mua suy yếu, giá sắp đảo chiều giảm
- **Ví dụ:** FPT tăng từ 130k lên 145k (higher high), RSI từ 72 xuống 65 (lower high) → sell signal

**Hidden Divergence (confirms trend):**
- Bullish hidden: Giá higher low + RSI lower low → uptrend tiếp tục
- Bearish hidden: Giá lower high + RSI higher high → downtrend tiếp tục

**Entry rules:**
1. Xác nhận divergence trên D1 chart
2. Chờ RSI break lại vùng 30 (bullish) hoặc 70 (bearish)
3. Kết hợp candlestick confirmation (hammer, engulfing)
4. Entry khi nến xác nhận đóng cửa

**Exit rules:**
- Take profit tại swing high/low trước đó
- Hoặc R:R tối thiểu 1:2
- Stop loss dưới swing low gần nhất (bullish) hoặc trên swing high (bearish)

#### MACD Crossover

**Bullish crossover (tín hiệu mua):**
- MACD line cắt lên trên Signal line
- **Mạnh nhất** khi xảy ra ở vùng âm (dưới zero line) → momentum đang chuyển từ bearish sang bullish
- **Ví dụ:** TCB MACD(-0.8) cắt lên Signal(-1.2) ở vùng âm → buy, target +8-12%

**Bearish crossover (tín hiệu bán):**
- MACD line cắt xuống dưới Signal line
- Mạnh nhất khi xảy ra ở vùng dương → chốt lời

**MACD Histogram:**
- Histogram từ âm sang dương → momentum tăng dần
- Histogram giảm dần từ đỉnh → momentum suy yếu, chuẩn bị exit

**Settings for VN swing:** MACD(12,26,9) trên D1 chart — settings mặc định, hoạt động tốt với chu kỳ 2-10 ngày.

#### Bollinger Squeeze Breakout

**Identifying Squeeze:**
- Bollinger Bands co lại hẹp bất thường (Bandwidth < 10% so với 6 tháng)
- Thị trường đang tích lũy, sắp bùng nổ

**Entry:**
1. Chờ nến đóng cửa NGOÀI upper band (long) hoặc dưới lower band (short)
2. Volume xác nhận: volume breakout > 1.5x trung bình 20 phiên
3. MACD hoặc RSI confirm hướng breakout

**Exit:**
- Trailing stop theo middle band (SMA20)
- Hoặc khi giá chạm lại middle band từ phía ngoài

**Ví dụ:** HPG BB co hẹp 2 tuần, giá breakout trên upper band + volume 15M (bình thường 8M) → long, target +10%, stop loss tại middle band.

### 1.2 Volume Confirmation Patterns

| Pattern | Description | Signal |
|---------|--------|-----------|
| Volume surge + breakout | Volume > 2x avg khi phá resistance | 🟢 Mua mạnh |
| Volume giảm dần khi pullback | Giá giảm nhẹ + volume thấp | 🟢 Healthy pullback, chờ mua |
| Volume tăng + giá giảm | Bán tháo có volume lớn | 🔴 Tránh/Short |
| Volume thấp + giá tăng | Tăng giả, thiếu lực mua | 🟡 Cẩn thận, có thể bull trap |
| Climax volume | Volume cực lớn (>3x) tại đỉnh/đáy | 🟡 Đảo chiều sắp xảy ra |

**Volume rules for VN:**
- Mã VN30: Volume xác nhận khi > 1.5x avg 20 phiên
- Midcap: Volume xác nhận khi > 2x avg 20 phiên
- **Không trade mã có volume < 500K/ngày** — rủi ro thanh khoản cao

### 1.3 Support/Resistance — How to Identify

**Methods for identification:**

1. **Swing highs/lows:** Các đỉnh/đáy rõ ràng trên chart D1
2. **Round numbers:** Các mức giá tròn (10k, 20k, 50k, 100k) — tâm lý thị trường VN rất mạnh ở mức tròn
3. **EMA động:** EMA20 (ngắn hạn), EMA50 (trung hạn), EMA200 (dài hạn)
4. **Volume Profile:** Vùng giá có volume giao dịch lớn nhất → support/resistance mạnh
5. **Gap zones:** Vùng gap chưa lấp → act as S/R

**Rules:**
- S/R được test nhiều lần → càng mạnh
- Khi S bị phá → trở thành R (và ngược lại)
- S/R kết hợp với Fibonacci retracement (38.2%, 50%, 61.8%) → confluence zone = vùng mua/bán tốt nhất

**Real-world example:**
- VNM: Support mạnh tại 65k (EMA200 + round number + swing low 3 lần) → mỗi lần chạm 65k bounce lên 5-8%
- HPG: Resistance 28k (đỉnh cũ + Fib 61.8%) → cần volume lớn để phá

### 1.4 Gap Analysis

**Gap Up (khoảng trống tăng):**
- **Breakaway gap:** Gap kèm volume lớn, phá resistance → trend mới bắt đầu → MUA
- **Continuation gap:** Gap giữa trend, volume trung bình → trend tiếp tục → HOLD
- **Exhaustion gap:** Gap tại cuối trend, volume cực lớn rồi giảm → sắp đảo chiều → CHỐT LỜI

**Gap Down (khoảng trống giảm):**
- Tương tự nhưng ngược lại
- **Gap fill strategy:** ~70% gap được lấp trong 5 phiên → nếu gap down nhỏ (< 2%) + volume thấp → mua đón gap fill

**VN-specific:**
- Biên độ giá HOSE: ±7%/ngày → gap tối đa 7%
- HNX: ±10% → gap có thể lớn hơn
- UPCoM: ±15%
- Gap sau nghỉ lễ dài thường mạnh (tích lũy tin tức)

### 1.5 Important Candlestick Patterns

#### Bullish Reversal Patterns
| Pattern | Description | Reliability |
|---------|--------|------------|
| **Hammer** | Thân nhỏ, bóng dưới dài ≥ 2x thân, xuất hiện ở đáy | ⭐⭐⭐ |
| **Bullish Engulfing** | Nến xanh bao trùm hoàn toàn nến đỏ trước | ⭐⭐⭐⭐ |
| **Morning Star** | 3 nến: đỏ dài + doji/spinning top + xanh dài | ⭐⭐⭐⭐⭐ |
| **Piercing Line** | Nến xanh mở dưới low trước, đóng > 50% thân nến đỏ | ⭐⭐⭐ |
| **Dragonfly Doji** | Doji với bóng dưới rất dài, ở đáy downtrend | ⭐⭐⭐ |

#### Bearish Reversal Patterns
| Pattern | Description | Reliability |
|---------|--------|------------|
| **Shooting Star** | Thân nhỏ, bóng trên dài ≥ 2x thân, ở đỉnh | ⭐⭐⭐ |
| **Bearish Engulfing** | Nến đỏ bao trùm hoàn toàn nến xanh trước | ⭐⭐⭐⭐ |
| **Evening Star** | 3 nến: xanh dài + doji/spinning top + đỏ dài | ⭐⭐⭐⭐⭐ |
| **Dark Cloud Cover** | Nến đỏ mở trên high trước, đóng < 50% thân nến xanh | ⭐⭐⭐ |
| **Gravestone Doji** | Doji với bóng trên rất dài, ở đỉnh uptrend | ⭐⭐⭐ |

**Usage rules:**
- Candlestick pattern CHỈ có ý nghĩa khi ở vùng S/R quan trọng
- Phải có volume xác nhận (volume nến signal > avg)
- Kết hợp với RSI/MACD để tăng xác suất
- **Ví dụ:** MBB tạo Morning Star tại support 18k + RSI < 30 + volume tăng → xác suất tăng > 75%

### 1.6 Risk Management for Swing Trading

**Stop Loss:**
- Mã VN30 (blue chip): stop loss 3-5%
- Midcap: stop loss 5-7%
- **Không bao giờ trade mà không có stop loss**

**Position Sizing (2% Rule):**
```
Số lượng CP = (Vốn × 2%) / (Giá entry - Giá stop loss)
```
**Ví dụ:** Vốn 100tr, mua MBB 20k, stop loss 19k (5%):
```
Số lượng = (100,000,000 × 2%) / (20,000 - 19,000) = 2,000 CP
Giá trị vị thế = 2,000 × 20,000 = 40,000,000 (40% vốn)
```

**Additional rules:**
- Tối đa 3-5 vị thế swing cùng lúc
- Không quá 30% vốn vào 1 ngành
- Trailing stop: dời stop loss lên khi giá tăng (theo EMA20 hoặc swing low mới)

---

## 2. Scalping / Day Trading VN (Intraday)

### 2.1 Phiên ATO/ATC Strategies

**HOSE trading hours:**
| Phiên | Thời gian | Match type |
|-------|-----------|-----------|
| ATO | 09:00 – 09:15 | Opening periodic matching |
| Liên tục sáng | 09:15 – 11:30 | Continuous matching |
| Nghỉ trưa | 11:30 – 13:00 | - |
| Liên tục chiều | 13:00 – 14:30 | Continuous matching |
| ATC | 14:30 – 14:45 | Closing periodic matching |

**ATO Strategy:**
1. **Gap & Go:** Nếu mã gap up > 2% tại ATO với volume lớn → mua ngay sau ATO (09:15-09:20), target +3-5% trong phiên
2. **Fade the gap:** Nếu gap up > 4% nhưng volume yếu → có thể là bull trap → chờ pullback mua hoặc tránh
3. **ATO accumulation:** Đặt lệnh ATO mua khi overnight có tin tốt (KQKD, cổ tức, nâng hạng)

**ATC Strategy:**
1. **ATC momentum:** Mua trước ATC (14:20-14:25) nếu mã đang tăng mạnh cả ngày + volume dồn → closing price thường cao nhất
2. **ATC dump:** Bán ATC nếu mã tăng mạnh nhưng volume yếu → ngày mai có thể gap down
3. **Smart money tracking:** Quan sát dư mua/bán ATC — nếu dư mua đột biến → tín hiệu tích cực cho ngày mai

### 2.2 T+2.5 Settlement Rule VN

**How it works:**
- Mua CP ngày T → chứng khoán về tài khoản trưa ngày T+2
- Có thể bán CHIỀU ngày T+2 (từ 13:00)
- → Gọi là T+2.5

**Strategies leveraging T+2.5:**
1. **Buy Friday afternoon, sell Tuesday afternoon:** Mua chiều thứ 6, bán chiều thứ 3
2. **News trading:** Mua khi có tin tốt, bán T+2.5 khi giá đã phản ánh
3. **Swing ngắn:** Mua chiều nay nếu setup đẹp → bán sáng kia (T+2.5) khi giá gap up

**Important notes:**
- Nếu mua **sáng T** → vẫn phải chờ **chiều T+2** mới bán được
- Tính từ ngày giao dịch, không tính T6-CN
- Một số CTCK cho phép bán trước T+2 nếu có ký quỹ (margin) — kiểm tra với broker

### 2.3 Order Flow Analysis

**VN order flow analysis:**
- **Bước giá HOSE:** 10đ (< 10k), 50đ (10k-50k), 100đ (> 50k)
- **3 giá tốt nhất:** Quan sát top 3 bid/ask
- **Dư mua > dư bán:** Áp lực tăng giá
- **Big lot (lô lớn > 10,000 CP):** Signal tổ chức/cá mập đang giao dịch

**How to read order flow:**
1. **Iceberg orders:** Lô lớn chia nhỏ, liên tục xuất hiện ở 1 mức giá → accumulation
2. **Spoofing:** Đặt lệnh lớn rồi hủy → tạo tín hiệu giả (cẩn thận)
3. **Market depth:** Nếu ask side mỏng + bid dày → giá dễ tăng
4. **Tick-by-tick:** Quan sát mỗi lệnh khớp — nhiều lệnh mua chủ động (hit ask) → bullish

### 2.4 Intraday Breakout Trading

**Setup:**
1. Xác định range sáng (09:15-10:30): High và Low của phiên sáng
2. Chờ breakout khỏi range:
   - Phá trên High + volume tăng → Long
   - Phá dưới Low + volume tăng → Tránh/Short (khó short VN)
3. Target: 1-2% từ breakout point
4. Stop loss: Quay lại trong range → cắt ngay

**Opening Range Breakout (ORB):**
- Range 30 phút đầu (09:15-09:45)
- Phá trên range + RSI > 50 → Long
- Target: ATR/2 từ entry

**Ví dụ:** HPG range sáng 26.5k-27k. Lúc 13:30 phá 27k + volume spike → mua 27.05k, target 27.5k (+1.7%), stop loss 26.8k (-0.9%). R:R = 1:1.9.

### 2.5 VWAP Strategy

**VWAP (Volume Weighted Average Price)** = Giá trung bình có trọng số volume trong ngày.

**How to use:**
- Giá > VWAP → Bullish bias intraday → tìm cơ hội mua
- Giá < VWAP → Bearish bias intraday → tránh mua, hoặc bán
- Giá bounce từ VWAP → Entry point tốt

**VWAP Pullback Strategy:**
1. Mã đang uptrend intraday (giá > VWAP)
2. Giá pullback về chạm VWAP
3. Volume giảm khi pullback
4. Nến bullish xuất hiện tại VWAP → MUA
5. Stop loss: dưới VWAP 0.5%

**Lưu ý VN:** Không phải tất cả platform VN đều hiển thị VWAP. Có thể tự tính:
```python
# Tính VWAP đơn giản
vwap = sum(price_i * volume_i) / sum(volume_i)
```

---

## 3. Special Indicators for Swing Trading

### 3.1 Williams %R

**Formula:** %R = (Highest High - Close) / (Highest High - Lowest Low) × (-100)

**Phạm vi:** 0 đến -100
| Vùng | Signal |
|------|-----------|
| 0 đến -20 | Overbought → chuẩn bị bán |
| -80 đến -100 | Oversold → chuẩn bị mua |
| -50 | Neutral |

**Usage for VN swing:**
- Williams %R phản ứng NHANH hơn RSI → tốt cho scalping và swing ngắn
- Mua khi %R vượt lên trên -80 (từ oversold)
- Bán khi %R rơi xuống dưới -20 (từ overbought)
- **Kết hợp:** Williams %R oversold + RSI < 35 + giá tại support → tín hiệu mua rất mạnh

**Ví dụ:** TCB Williams %R = -85, RSI = 32, giá tại support 24k → mua, target 26k (+8.3%)

### 3.2 CCI (Commodity Channel Index)

**Phạm vi:** Không giới hạn, thường dao động -200 đến +200

| Vùng | Signal |
|------|-----------|
| > +100 | Overbought / Strong uptrend |
| +100 đến -100 | Neutral range |
| < -100 | Oversold / Strong downtrend |
| > +200 | Cực overbought → đảo chiều |
| < -200 | Cực oversold → đảo chiều |

**CCI Swing Strategy:**
1. **Zero-line crossover:** CCI cắt lên 0 → bullish, cắt xuống 0 → bearish
2. **Breakout +100/-100:** CCI phá trên +100 → trend mạnh bắt đầu → mua theo trend
3. **Divergence:** Giá higher high + CCI lower high → sắp giảm

**Settings:** CCI(14) cho swing, CCI(7) cho scalping

### 3.3 Money Flow Index (MFI)

MFI = "RSI có volume" — kết hợp giá VÀ volume để đo áp lực mua/bán.

| Vùng | Signal |
|------|-----------|
| > 80 | Overbought (có volume xác nhận) |
| < 20 | Oversold (có volume xác nhận) |

**Advantages over RSI:**
- MFI tích hợp volume → ít false signal hơn RSI đơn thuần
- Rất hữu ích cho thị trường VN nơi volume là yếu tố quan trọng

**Strategy:**
- MFI < 20 + Price tại support + Volume spike → **Strong buy**
- MFI > 80 + Price tại resistance + Volume giảm → **Sell signal**
- MFI divergence tin cậy hơn RSI divergence vì có volume backing

### 3.4 ADX (Average Directional Index) — Trend Strength

ADX measures trend **strength**, NOT direction. Kết hợp +DI/-DI để xác định hướng.

| ADX | Meaning | Strategy |
|-----|---------|------------|
| 0-20 | Không có trend / sideway | → Range trading, Bollinger Bands |
| 20-25 | Trend đang hình thành | → Chuẩn bị entry |
| 25-50 | Trend mạnh | → Swing theo trend |
| 50-75 | Trend rất mạnh | → Hold, trailing stop |
| > 75 | Cực mạnh (hiếm) | → Cẩn thận đảo chiều |

**How to use:**
1. ADX > 25 + (+DI > -DI) → **Uptrend mạnh → MUA**
2. ADX > 25 + (-DI > +DI) → **Downtrend mạnh → TRÁNH**
3. ADX < 20 → Sideway → dùng RSI/Bollinger thay vì MACD
4. +DI cắt lên -DI + ADX đang tăng → **Signal mua tốt nhất**

**Ví dụ:** FPT ADX = 35 (trend mạnh), +DI = 28 > -DI = 12 → uptrend mạnh, swing long.

### 3.5 Ichimoku Cloud for Swing

**5 thành phần:**
1. **Tenkan-Sen (Conversion):** (High9 + Low9) / 2 — momentum ngắn hạn
2. **Kijun-Sen (Base):** (High26 + Low26) / 2 — momentum trung hạn
3. **Senkou Span A:** (Tenkan + Kijun) / 2, plot 26 kỳ tương lai
4. **Senkou Span B:** (High52 + Low52) / 2, plot 26 kỳ tương lai
5. **Chikou Span:** Close hiện tại, plot 26 kỳ quá khứ

**Kumo (Mây):** Vùng giữa Span A và Span B

**Signal swing:**
| Signal | Description | Hành động |
|--------|--------|-----------|
| Price > Cloud | Uptrend | Tìm mua |
| Price < Cloud | Downtrend | Tránh mua |
| Price trong Cloud | Sideway/Consolidation | Chờ |
| Tenkan cắt lên Kijun (TK Cross) | Bullish signal | Mua nếu trên Cloud |
| Tenkan cắt xuống Kijun | Bearish signal | Bán |
| Cloud xanh (Span A > B) | Bullish bias | Confidence cao hơn |
| Cloud đỏ (Span A < B) | Bearish bias | Cẩn thận |
| Cloud mỏng | Volatility thấp | Dễ phá qua |
| Cloud dày | S/R mạnh | Khó phá |

**Ichimoku for VN:** Dùng settings chuẩn (9,26,52) trên D1 chart. Rất hiệu quả với VN30 bluechip vì đủ thanh khoản.

**Ví dụ:** VCB giá 85k, trên Cloud (bullish), Tenkan vừa cắt lên Kijun, Cloud xanh + dày → strong uptrend, swing long target 92k.

### 3.6 Pivot Points (Daily/Weekly)

**Công thức Standard Pivot:**
```
PP = (High + Low + Close) / 3
R1 = (2 × PP) - Low
S1 = (2 × PP) - High
R2 = PP + (High - Low)
S2 = PP - (High - Low)
R3 = High + 2 × (PP - Low)
S3 = Low - 2 × (High - PP)
```

**How to use:**
- **Daily pivots:** Cho day trading/scalping
- **Weekly pivots:** Cho swing trading 2-10 ngày

**Strategy:**
1. **Bounce:** Giá chạm S1/S2 + nến đảo chiều → mua, target PP hoặc R1
2. **Breakout:** Giá phá R1 + volume → mua, target R2
3. **Range:** Giá dao động giữa S1 và R1 → mua S1, bán R1

**Đặc biệt cho VN:** Pivot points rất hiệu quả khi kết hợp với biên độ giá giới hạn (±7% HOSE).

---

## 4. Swing Trading Capital Management

### 4.1 Kelly Criterion

**Formula:**
```
Kelly % = W - [(1 - W) / R]
```
Trong đó:
- W = Tỷ lệ thắng (win rate)
- R = Tỷ lệ lãi/lỗ trung bình (avg win / avg loss)

**Ví dụ:**
- Win rate: 55% → W = 0.55
- Avg win: 8%, Avg loss: 4% → R = 2.0
```
Kelly % = 0.55 - [(1 - 0.55) / 2.0] = 0.55 - 0.225 = 0.325 = 32.5%
```
→ Đặt tối đa 32.5% vốn cho mỗi trade.

**⚠️ Fractional Kelly (RECOMMENDED):**
- Full Kelly quá rủi ro cho thực tế → dùng **Half Kelly (50%)** hoặc **Quarter Kelly (25%)**
- Ví dụ trên: Half Kelly = 16.25%, Quarter Kelly = 8.1% per trade
- **Recommendation for VN:** Quarter Kelly đến Half Kelly, tối đa 15-20% per trade

**Code tính Kelly:**
```python
def kelly_criterion(win_rate, avg_win, avg_loss):
    """Calculate Kelly % for position sizing"""
    R = avg_win / avg_loss
    kelly = win_rate - ((1 - win_rate) / R)
    half_kelly = kelly / 2
    quarter_kelly = kelly / 4
    return {
        'full_kelly': round(kelly * 100, 1),
        'half_kelly': round(half_kelly * 100, 1),
        'quarter_kelly': round(quarter_kelly * 100, 1),
        'recommended': round(half_kelly * 100, 1)  # Half Kelly recommended
    }

# Ví dụ: Win rate 55%, avg win 8%, avg loss 4%
result = kelly_criterion(0.55, 8, 4)
print(f"Full Kelly: {result['full_kelly']}%")
print(f"Half Kelly (recommended): {result['half_kelly']}%")
# Output: Full Kelly: 32.5%, Half Kelly: 16.3%
```

### 4.2 Risk/Reward Ratio

**Hard rule: minimum R:R 1:2**

| R:R | Đánh giá | Breakeven Win Rate |
|-----|----------|-------------------|
| 1:1 | Tối thiểu | 50% |
| 1:2 | Tốt (khuyến nghị) | 33% |
| 1:3 | Rất tốt | 25% |
| 1:4+ | Xuất sắc (hiếm) | 20% |

**Cách tính:**
```
Risk = Entry price - Stop loss
Reward = Target price - Entry price
R:R = Reward / Risk
```

**Ví dụ:** Mua HPG 27k, stop loss 26k (-3.7%), target 29k (+7.4%)
```
Risk = 1,000 VND
Reward = 2,000 VND
R:R = 2,000 / 1,000 = 1:2 ✅
```

**Rules:** Nếu R:R < 1:2 → KHÔNG TRADE, dù setup đẹp đến mấy.

### 4.3 Max Drawdown Rules

**Drawdown limits:**
| Level | Drawdown | Hành động |
|-------|----------|-----------|
| 🟡 Warning | -5% tổng vốn | Giảm position size 50% |
| 🔴 Stop | -10% tổng vốn | Dừng trade 1 tuần, review |
| ⛔ Circuit breaker | -15% tổng vốn | Dừng trade 1 tháng, xem lại toàn bộ hệ thống |

**Daily loss limit:**
- Thua > 2% trong ngày → dừng trade ngày hôm đó
- Thua 3 trades liên tiếp → nghỉ ít nhất 1 ngày

**Tracking drawdown:**
```python
def check_drawdown(portfolio_value, peak_value):
    """Check drawdown level and raise alerts"""
    drawdown = (peak_value - portfolio_value) / peak_value * 100
    if drawdown >= 15:
        return f"⛔ CIRCUIT BREAKER: -{drawdown:.1f}% — DỪNG TRADE 1 THÁNG"
    elif drawdown >= 10:
        return f"🔴 STOP: -{drawdown:.1f}% — Dừng trade 1 tuần"
    elif drawdown >= 5:
        return f"🟡 WARNING: -{drawdown:.1f}% — Giảm size 50%"
    else:
        return f"✅ OK: -{drawdown:.1f}%"
```

### 4.4 Pyramiding vs Averaging Down

**Pyramiding (CORRECT):**
- Thêm vị thế khi trade ĐANG LỜI → "winners ride"
- Mỗi lần thêm nhỏ hơn lần trước (ví dụ: 100 → 60 → 40 CP)
- Dời stop loss lên breakeven cho phần gốc

**Ví dụ Pyramiding:**
```
Lần 1: Mua MBB 20.0k × 2,000 CP (40tr)
Giá lên 21.0k (+5%) → Lần 2: Mua thêm 1,200 CP (25.2tr)
Giá lên 22.0k (+10%) → Lần 3: Mua thêm 800 CP (17.6tr)
Stop loss dời lên 20.5k (breakeven cho lần 1)
Target: 23.5k → Tổng lời: ~13.5tr
```

**Averaging Down (DANGEROUS):**
- Thêm vị thế khi trade ĐANG LỖ → "catching falling knife"
- **CHỈ chấp nhận** khi:
  1. Cổ phiếu cơ bản tốt (ROE > 15%, FCF dương)
  2. Giá giảm do thị trường chung, không phải tin xấu riêng
  3. Đã plan trước vùng mua DCA (không phải panic buy)
  4. Max 3 lần average down
  5. Vẫn tuân thủ max drawdown rules

**Golden rule:**
> "Pyramiding khi đúng, cắt lỗ khi sai. KHÔNG BAO GIỜ averaging down với mã lướt sóng."

Averaging down chỉ dành cho **đầu tư dài hạn DCA** với cổ phiếu fundamentals tốt (MBB, FPT, VNM...), KHÔNG dùng cho swing/scalping.

---

## 5. VN Swing Trading Screening Criteria

### 5.1 Hard Criteria

| Tiêu chí | Threshold | Reason |
|----------|--------|-------|
| Volume trung bình 20 phiên | > 1,000,000 CP/ngày | Ensures liquidity, easy entry/exit |
| ATR(14) / Giá | > 3% | Amplitude large enough for profit |
| Beta | > 1.2 | More volatile than market |
| Rổ | VN30, VNMID, VN100 | Good liquidity, less manipulation |
| Free-float | > 30% | Enough float for trading |

### 5.2 Soft Criteria (preferred)

| Tiêu chí | Description |
|----------|-------|
| Sector momentum | Ngành đang có dòng tiền chảy vào |
| Near support | Giá gần vùng support quan trọng |
| RSI 30-45 | Đang oversold nhẹ, sắp bounce |
| MACD sắp crossover | Momentum đang chuyển hướng |
| Có catalyst | KQKD sắp công bố, tin ngành tốt |

### 5.3 Popular VN Swing Trading Tickers

**VN30 — Blue chip thanh khoản cao:**
- **Ngân hàng:** MBB, TCB, VPB, STB, CTG, BID, ACB
- **Thép:** HPG, HSG
- **BĐS:** VHM, VIC, NVL
- **Công nghệ:** FPT
- **Dầu khí:** GAS, PLX, PVD, PVS
- **Khác:** MWG, VNM, MSN, VRE

**Midcap — Biến động mạnh:**
- **BĐS:** KDH, DXG, NLG, HDG
- **Chứng khoán:** SSI, VCI, HCM, VND
- **Xây dựng:** CTD, HBC
- **Tiêu dùng:** PNJ, MWG

### 5.4 Swing Screening Script

```python
#!/usr/bin/env python3
"""
Swing Trading Screener for VN market
Scan TradingView for swing trading candidates
"""
import urllib.request, json

def scan_swing_candidates():
    """Scan VN stocks suitable for swing trading"""
    payload = {
        "filter": [
            {"left": "volume", "operation": "greater", "right": 1000000},
            {"left": "RSI", "operation": "in_range", "right": [25, 45]},
            {"left": "average_volume_10d_calc", "operation": "greater", "right": 500000},
        ],
        "symbols": {"query": {"types": ["stock"]}, "tickers": []},
        "columns": [
            "name", "close", "change", "volume",
            "RSI", "MACD.macd", "MACD.signal",
            "EMA20", "EMA50", "EMA200",
            "BB.upper", "BB.lower",
            "ADX", "ADX+DI", "ADX-DI",
            "Stoch.K", "W.R",
            "ATR", "price_52_week_high", "price_52_week_low",
            "average_volume_10d_calc"
        ],
        "sort": {"sortBy": "volume", "sortOrder": "desc"},
        "range": [0, 50],
        "options": {"lang": "vi"}
    }

    req = urllib.request.Request(
        "https://scanner.tradingview.com/vietnam/scan",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    results = []
    for item in data.get("data", []):
        d = item["d"]
        ticker = item["s"].split(":")[-1]
        close = d[1]
        atr = d[17]

        if close and atr and close > 0:
            atr_pct = (atr / close) * 100
            if atr_pct >= 3.0:  # Biên độ ATR > 3%
                results.append({
                    "ticker": ticker,
                    "close": close,
                    "change": d[2],
                    "volume": d[3],
                    "rsi": d[4],
                    "macd": d[5],
                    "macd_signal": d[6],
                    "ema20": d[7],
                    "ema200": d[9],
                    "adx": d[12],
                    "williams_r": d[16],
                    "atr_pct": round(atr_pct, 1),
                })

    # Sort by RSI (most oversold first)
    results.sort(key=lambda x: x["rsi"] if x["rsi"] else 100)
    return results

if __name__ == "__main__":
    candidates = scan_swing_candidates()
    print(f"\n🏄 SWING TRADING CANDIDATES ({len(candidates)} mã):\n")
    for c in candidates[:20]:
        macd_signal = "🟢" if (c["macd"] and c["macd_signal"] and c["macd"] > c["macd_signal"]) else "🔴"
        ema_status = "▲" if (c["close"] and c["ema200"] and c["close"] > c["ema200"]) else "▼"
        print(f"  {c['ticker']:6s} | {c['close']:>10,.0f} | RSI {c['rsi']:5.1f} | "
              f"MACD {macd_signal} | EMA200 {ema_status} | "
              f"ADX {c['adx']:5.1f} | W%R {c['williams_r']:6.1f} | "
              f"ATR {c['atr_pct']}% | Vol {c['volume']/1e6:.1f}M")
```

---

## 6. Summary — Swing Trading Checklist

### ✅ Checklist Before Entering a Trade

1. **Trend:** EMA200 → uptrend hay downtrend?
2. **Momentum:** RSI, MACD, ADX → momentum có ủng hộ?
3. **Volume:** Volume xác nhận tín hiệu?
4. **S/R:** Giá đang ở vùng support hay resistance?
5. **Pattern:** Candlestick pattern đảo chiều?
6. **R:R:** Tối thiểu 1:2?
7. **Position size:** Theo Kelly hoặc 2% rule?
8. **Stop loss:** Đã xác định chính xác?
9. **Catalyst:** Có tin tức hỗ trợ?
10. **Max exposure:** Tổng vị thế < 80% vốn?

### 📊 Strongest Signal Combos

| Combo | Description | Win probability |
|-------|--------|----------------|
| RSI divergence + Hammer tại support + Volume spike | Đảo chiều từ đáy | ~70-75% |
| Bollinger squeeze breakout + MACD crossover + ADX > 25 | Breakout trend mới | ~65-70% |
| Ichimoku TK cross + Price trên Cloud + Volume tăng | Swing theo trend | ~65-70% |
| MFI < 20 + Williams %R < -80 + Price tại S1 pivot | Oversold cực mạnh | ~70% |

### ⚠️ Common Mistakes

1. **FOMO:** Đuổi giá khi đã tăng mạnh → mua đỉnh
2. **Không cắt lỗ:** "Chờ nó về" → từ swing thành "ôm hàng"
3. **Over-trading:** Trade quá nhiều, phí ăn hết lời
4. **Averaging down mã lướt sóng:** Sai lầm chết người
5. **Không có kế hoạch:** Entry/exit/stop loss phải có TRƯỚC khi đặt lệnh
6. **Ignore volume:** Signal không có volume = tín hiệu yếu
7. **Trade mã thanh khoản thấp:** Vào dễ, ra khó

---

*⚠️ Educational reference material, not investment advice. Always DYOR and manage risk.*
