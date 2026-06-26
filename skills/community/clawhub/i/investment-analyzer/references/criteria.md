# Investment Decision Criteria

## Decision Output Format
Every analysis must end with one of:
- **✅ BUY / ADD** — meets all thresholds, proceed
- **⚠️ INVESTIGATE** — passes some thresholds, needs more data or has significant risks
- **❌ PASS** — does not meet minimum criteria

---

## Real Estate Thresholds

| Metric | Minimum to Consider | Target |
|--------|-------------------|--------|
| Monthly cash flow (after all expenses) | > $0 (break-even minimum) | > $300/unit/month |
| Cash-on-Cash Return (CoC) | > 5% | > 8% |
| Cap Rate | > 4.5% | > 6% |
| Gross Rent Multiplier (GRM) | < 20 | < 15 |

### Assumptions for Property Analysis
- **Down payment**: 20% of purchase price (investment property minimum in Canada)
- **Vacancy rate**: 5%
- **Property management**: 0% (self-managed) — adjust if using a manager
- **Maintenance reserve**: 1% of property value per year
- **Insurance estimate**: $150/month per property (adjust per actual)
- **Mortgage stress test rate**: qualifying rate or contract rate + 2% (whichever higher)
- **Appreciation assumption**: 3.5% per year (conservative Quebec average)
- **LOC rate for expense coverage**: 4.95%

### Quebec-Specific Notes
- Welcome tax (taxe de bienvenue): ~1.5% of purchase price (factor into acquisition cost)
- School taxes + municipal taxes: get actuals from listing
- Quebec rental law: strict tenant protections — factor in lower eviction flexibility

---

## ETF Thresholds

| Metric | Threshold |
|--------|-----------|
| MER | < 0.35% preferred, reject if > 0.75% |
| Overlap with TEC.TO | Flag if > 40% overlap in top holdings |
| Historical 10-yr annualized return | Benchmark against 10% (S&P 500 long-term avg) |
| Diversification improvement | Must reduce sector concentration vs current 100% tech |

---

## ETF vs Real Estate Comparison Methodology

When comparing a lump sum or recurring investment between ETF and property:

1. **Same capital base**: Use actual down payment as the equity deployed for both sides
2. **Property total return** = (Annual cash flow + Annual appreciation) / Down payment
3. **ETF total return** = Historical annualized return of the ETF (after MER)
4. **After-tax adjustment**: Apply ~46% marginal rate to rental income; apply 50% inclusion rate on capital gains for both
5. **Leverage premium**: Property uses mortgage leverage — state this explicitly in the conclusion
6. **Break-even horizon**: Calculate how many years until property out-performs ETF (or vice versa)

### Conclusion rule
- If property after-tax CoC + appreciation > ETF after-tax return → **Real estate wins**
- If property cash flow is negative and ETF return > 7% → **ETF wins**
- If close (within 1.5%) → **INVESTIGATE** (consider liquidity, risk tolerance, time commitment)

---

## Property Scanner Configuration

### Target Markets (priority order)
1. **Sherbrooke** — primary target, best cash flow in Quebec
2. **Québec City / Lévis** — already have network, secondary target
3. **Gatineau** — federal workers, stable demand, watch list

### Target Property Types
- Triplex (3 units) — preferred
- Quadruplex (4 units) — ideal if price allows
- Duplex — only if exceptional deal

### Price Range
- Minimum: $280,000
- Maximum: $550,000

### Market Rent Estimates (Sherbrooke, 2025)
| Unit type | Est. monthly rent |
|-----------|-----------------|
| Studio / 3½ | $750 |
| 1 bed / 4½ | $900 |
| 2 bed / 5½ | $1,100 |
| 3 bed / 6½ | $1,300 |

**Default rent estimates by property type:**
- Duplex (2 units): $1,800/month total
- Triplex (3 units): $2,700/month total
- Quadruplex (4 units): $3,400/month total

### Property Tax Estimate (Sherbrooke)
- Approximately **1.1% of purchase price per year**
- Example: $420,000 property → ~$4,620/year

---

## DCA Configuration

### Income
- Bi-weekly take-home: $1,940 CAD
- Annual investable: $50,440

### Priority Order for Each Paycheck
1. **Emergency fund** — target 3 months expenses (~$9,000). If not built, fund this first.
2. **TFSA** — $7,000/year limit (2025). Max this before taxable accounts ($269/bi-weekly).
3. **RRSP** — 18% of earned income (~$16,200/yr room estimate). Use if in high bracket ($623/bi-weekly).
4. **HXQ DCA** — remaining capital after above priorities.
5. **Down payment reserve** — if Sherbrooke triplex is the next target, build toward $90,000.

### Key Unknowns (update these fields)
- **Emergency fund current balance**: TBD
- **TFSA current balance / contribution room remaining**: TBD
- **RRSP current balance / contribution room remaining**: TBD
- **General LOC current outstanding balance**: TBD
- **Student LOC outstanding balance**: $30,000 (interest-only phase, expires in 1–2 years) — used for rental operating expenses, NOT for down payment

