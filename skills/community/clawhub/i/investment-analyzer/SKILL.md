---
name: investment-analyzer
description: "Investment analysis for properties and ETFs. BUY/PASS/INVESTIGATE verdicts backed by data. Scans Centris for listings, advises DCA allocation. Triggers: analyze property, ETF, scan Centris, 定投, DCA, 投资房, compare real estate vs ETF."
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["gemini"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY"}}
---

# Investment Analyzer Skill

Give data-driven investment conclusions. Always end with ✅ BUY / ⚠️ INVESTIGATE / ❌ PASS.

## Resource Locations
- **Personal profile**: [references/profile.md](references/profile.md) — income, tax rate, LOC
- **Current portfolio**: [references/portfolio.md](references/portfolio.md) — existing ETF + properties
- **Decision criteria**: [references/criteria.md](references/criteria.md) — thresholds and methodology
- **Scripts**: `scripts/`

## Standard Workflows

### 1. Analyze a Rental Property
- **Trigger**: User shares a listing (address, price, estimated rent) or asks "should I buy X property"
- **Process**:
  1. Collect: purchase price, estimated monthly rent, property taxes, address.
  2. Run `scripts/analyze_property.py` with the inputs.
  3. Calculate: mortgage payment (20% down, current rate), cash flow, CoC, Cap Rate, GRM.
  4. Factor in Quebec welcome tax, maintenance reserve, vacancy, insurance.
  5. Compare result against thresholds in `references/criteria.md`.
  6. Present full breakdown + **conclusion**.

### 2. Analyze an ETF
- **Trigger**: User asks "is XEQT worth buying", "analyze VFV", or names a ticker
- **Process**:
  1. Run `scripts/analyze_etf.py <TICKER>` to fetch MER, returns, top holdings.
  2. Calculate overlap with current TEC.TO holdings.
  3. Compare historical return vs thresholds in `references/criteria.md`.
  4. Assess whether it improves portfolio diversification.
  5. Present full breakdown + **conclusion**.

### 3. ETF vs Real Estate — Where to Put the Money
- **Trigger**: "should I invest in ETF or property", "where should I put $X", "compare ETF vs real estate"
- **Process**:
  1. Clarify available capital (if not stated).
  2. Run `scripts/compare_allocation.py` with the capital amount.
  3. Model both scenarios over the investment horizon using same capital base.
  4. Apply after-tax adjustments (marginal rate ~46%, capital gains 50% inclusion).
  5. State leverage effect explicitly.
  6. Present side-by-side comparison + **conclusion**.

### 4. Daily Property Scan
- **Trigger**: "scan for properties", "帮我找投资房", "daily scan", "Centris scan"
- **Process**:
  1. Run `scripts/scan_properties.py --city sherbrooke --min-price 280000 --max-price 550000`.
  2. Surface only ✅ BUY or ⚠️ INVESTIGATE listings with address, price, units, cash flow, cap rate, CoC, URL.
  3. If Centris scraping fails, paste listing details manually and use `analyze_property.py`.

### 5. DCA Advisor — How Much to Invest Each Paycheck
- **Trigger**: "how much should I invest", "定投比例", "工资投多少", "DCA advice"
- **Process**:
  1. Run `scripts/dca_advisor.py` with current emergency fund, TFSA/RRSP room, LOC balance.
  2. Priority: Emergency fund → TFSA (HXQ) → RRSP (HXQ) → LOC paydown → Down payment reserve → HXQ taxable.
  3. Report exact dollar split per bucket and any flags.

## Output Format
Each analysis must include: Key Metrics table, 2-3 sentence summary, and final verdict ✅ BUY / ⚠️ INVESTIGATE / ❌ PASS with one-line reason.

