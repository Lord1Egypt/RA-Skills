# Return Estimation — Projected Investment Returns

> Quantitative methods for estimating expected returns over time,
> combining historical data and scenario analysis.

---

## Method 1: Historical Return Analysis

### API: VNDirect dChart

Fetch daily price history (daily OHLCV):

```
GET https://dchart-api.vndirect.com.vn/dchart/history
    ?symbol=FPT
    &resolution=D
    &from=1609459200   (Unix timestamp — 2021-01-01)
    &to=1742400000     (Unix timestamp — today)
```

**No authentication required.** Response format:
```json
{
  "t": [1609459200, ...],   // timestamps
  "c": [72500, ...],        // close prices (VND)
  "o": [...], "h": [...], "l": [...], "v": [...]
}
```

### Metrics to Calculate

| Metric | Công thức | Meaning |
|--------|-----------|---------|
| **Return N tháng** | `(close_now / close_Nmonths_ago - 1) × 100` | Actual return |
| **CAGR** | `(close_now / close_Nyears_ago)^(1/N) - 1` | Compound growth/year |
| **Volatility** | `std(daily_returns) × √252` | Annual risk |
| **Max Drawdown** | `min((price - running_max) / running_max)` | Maximum drawdown from peak |
| **Sharpe Ratio** | `(CAGR - rf_rate) / volatility` | Return/risk (rf = 4.5%) |

### Reference Benchmarks
- **Gửi ngân hàng**: 5.5%/năm (12-month term)
- **VN-Index trung bình**: ~10–12%/năm (2010–2024)
- **Inflation VN**: ~3–4%/năm

---

## Method 2: Scenario Analysis (3 Scenarios)

Based on historical volatility × time horizon:

```
Bear (bi quan):    Return = risk-free rate (5.5%) ± 0 (giữ nguyên giá, chỉ dividend)
Base (trung bình): Return = EPS growth rate (consensus) + P/E stable
Bull (lạc quan):   Return = EPS growth + P/E re-rating + catalyst premium
```

### Estimation Formula

```python
bear_annual  = max(rf_rate, cagr_3y - 1.0 * volatility)   # 1 std dev dưới mean
base_annual  = cagr_3y                                      # mean reversion
bull_annual  = cagr_3y + 0.5 * volatility                  # 0.5 std dev trên mean

def project(principal, annual_rate, years):
    return principal * (1 + annual_rate) ** years
```

### Template Output

```
## 📈 Estimate Lợi Nhuận — [TICKER]
Vốn đầu tư: X triệu VND | Giá hiện tại: X,XXX VND

### Lịch sử (thực tế)
Giá 1 năm trước:  X,XXX | Return: +/-XX.X%
Giá 3 năm trước:  X,XXX | CAGR: +/-XX.X%/năm
Giá 5 năm trước:  X,XXX | CAGR: +/-XX.X%/năm
Volatility/năm:   XX.X%
Max Drawdown:     -XX.X%
Sharpe Ratio:     X.XX

### Dự báo theo kịch bản (từ giá hiện tại)
                    6 tháng    1 năm     3 năm     5 năm
Bear  (bi quan):    +X.X%     +XX.X%    +XX.X%    +XX.X%  → VND X.X triệu
Base  (trung bình): +XX.X%    +XX.X%    +XX.X%    +XX.X%  → VND X.X triệu
Bull  (lạc quan):   +XX.X%    +XX.X%    +XX.X%    +XX.X%  → VND X.X triệu

### So sánh với tài sản khác (vốn X triệu, 3 năm)
Gửi ngân hàng 5.5%/năm:        +X.X triệu  (tổng: X.X triệu)
[TICKER] Base case:             +X.X triệu  (tổng: X.X triệu)
VN-Index trung bình 11%/năm:    +X.X triệu  (tổng: X.X triệu)

### Catalyst & Timeline (sự kiện tác động giá)
- [Catalyst 1]: dự kiến tháng X/20XX → +XX% nếu xảy ra
- Nâng hạng thị trường FTSE/MSCI: dự kiến 2026–2027 → inflow ~$X tỷ
- Kết quả kinh doanh Q1: tháng 4/20XX
```

---

## Method 3: Automated Script `estimate_returns.py`

Xem `scripts/estimate_returns.py` để tính tự động với Python.

The script performs:
1. Fetch 5 năm daily data từ VNDirect dChart API
2. Tính CAGR, volatility, max drawdown, Sharpe Ratio
3. Build 3 scenario projections (Bear/Base/Bull)
4. So sánh với benchmark (ngân hàng, VN-Index)
5. Output bảng đầy đủ

**Sử dụng:**
```bash
python3 scripts/estimate_returns.py FPT
python3 scripts/estimate_returns.py VCB --capital 100  # 100 triệu VND
python3 scripts/estimate_returns.py HPG --capital 50 --years 3
```

---

## Important Notes

### Model Limitations
- **Past performance ≠ future results** — đặc biệt với cổ phiếu chu kỳ (thép, BĐS)
- Scenario analysis dựa trên **volatility lịch sử** — volatility tương lai có thể khác
- Không tính **dividend reinvestment** (thêm ~2–5%/năm cho cổ phiếu dividend cao)
- Không tính **thuế** (thuế TNCN 0.1% trên doanh số bán, hiện hành)

### When to Use Which Method
| Scenario | Method |
|-----------|-------------|
| Stock with 3+ years of history | Historical Return + Scenario |
| Newly IPO stock (<2 years) | Use Sector CAGR benchmark only |
| Cyclical stocks (steel, real estate) | Emphasize Max Drawdown, use Bear case |
| Stable blue chips (VNM, GAS) | Base case reliable, Sharpe ratio important |

### Bank Interest Rate Benchmark (updated Q1/2026)
| Term | Rate |
|--------|---------|
| 6 tháng | 4.8–5.2% |
| 12 tháng | 5.3–5.8% |
| 24 tháng | 5.5–6.0% |
| **Use 5.5%/year as baseline** | |

---

*Disclaimer: Return estimates are for reference only. Not investment advice.*
