<!--
Glossary of financial terms used by the InvestorClaw analyzers. Carried
forward from v2.6 essentially unchanged — the underlying mathematics
is identical in v4.x.
-->

# Financial Terminology Guide

**InvestorClaw Educational Reference** — Plain English explanations of financial metrics used in portfolio analysis.

---

## Performance Metrics

### Sharpe Ratio
**What it is:** Risk-adjusted return metric that tells you how much excess return you're earning per unit of risk taken.

**Formula:** (Annual Return - Risk-Free Rate) / Annual Volatility

**Interpretation:**
- **> 2.0** = Excellent (professional-quality risk-adjusted returns)
- **> 1.5** = Very Good
- **> 1.0** = Good (solid risk-adjusted returns)
- **> 0.5** = Modest
- **< 0** = Poor (underperformed risk-free rate)

**Plain English:** A Sharpe of 1.5 means for every 1% of volatility you accept, you're earning 1.5% of excess return. Higher is better.

---

### Volatility (Annual & Daily)
**What it is:** Measure of how much your investment's price swings up and down.

**What it means:**
- **Low volatility (5-10%)** = Stable, predictable value (bonds, utilities)
- **Medium volatility (15-25%)** = Typical for diversified stock portfolios
- **High volatility (30%+)** = Large swings, often tech or growth stocks
- **Extreme volatility (50%+)** = Penny stocks, speculative positions

**Plain English:** 18% annual volatility means in a typical year, your returns fall within ±18% of average about 68% of the time.

---

### Beta
**What it is:** Measures how your investment moves compared to the overall market (S&P 500).

**What it means:**
- **Beta = 1.0** = Moves exactly with the market (if S&P drops 10%, you drop ~10%)
- **Beta > 1.0** = More volatile than market (amplified swings)
- **Beta < 1.0** = Less volatile than market (smoother rides)
- **Beta ≤ 0** = Moves opposite the market (rare; some bonds/gold)

**Plain English:** A stock with beta 1.3 is 30% more volatile than the market. When the S&P 500 drops 10%, this stock typically drops ~13%.

---

### Value at Risk (VaR)
**What it is:** The worst-case loss you might experience under normal market conditions (95% confidence level).

**What it means:** 95 times out of 100 years, your losses won't exceed this amount.

**Example:** VaR of -$50K on a $2M portfolio means in the worst 5% of years, you'd lose up to $50K (2.5% of portfolio).

**Plain English:** Think of it as the downside scenario to plan for. It answers: "What's the most I could reasonably lose?"

---

### Conditional Value at Risk (CVaR / Expected Shortfall)
**What it is:** Average loss on the 5% worst days (goes beyond worst single day).

**What it means:** When things go really wrong, how bad does it get on average?

**Plain English:** If VaR is "worst case," CVaR is "average of worst cases." VaR ≤ CVaR always.

---

### Max Drawdown
**What it is:** The largest peak-to-bottom loss experienced during the analysis period.

**Historical context:**
- **2008 Financial Crisis:** S&P 500 -57%
- **2020 COVID Crash:** S&P 500 -34%
- **2022 Bear Market:** S&P 500 -19%

**Plain English:** Shows you what happened in past bad times. Helps you mentally prepare for future crashes.

---

### Herfindahl-Hirschman Index (HHI)
**What it is:** Concentration measure on a 0-to-1 scale. Measures how much portfolio risk is concentrated in few positions.

**Range:**
- **0.01-0.05** = Well-diversified (40+ holdings)
- **0.05-0.15** = Moderate concentration (20-40 holdings)
- **0.15-0.30** = Concentrated (5-20 holdings)
- **0.30+** = Highly concentrated (few large positions)

**Formula:** HHI = sum of (weight%)². Example: 50% in one stock = 0.25 HHI.

**Plain English:** Lower HHI = better diversification. An HHI of 0.08 means your portfolio is well-spread across many holdings.

---

## Bond Metrics

### Yield to Maturity (YTM)
**What it is:** Total annual return you'll earn if you hold the bond until it matures.

**What it includes:**
- Annual coupon payments
- Price change from current price to face value at maturity
- Reinvestment of coupon payments

**Plain English:** The "all-in" return you can lock in right now if you hold to maturity. This is what bond investors compare to find good deals.

---

### Duration
**What it is:** Sensitivity of bond price to interest rate changes. Measured in years.

**What it means:**
- **Duration = 5 years** = If interest rates rise 1%, bond price falls ~5%
- **Short duration (1-3 years)** = Less sensitive to rate changes
- **Medium duration (5-7 years)** = Typical for many bonds
- **Long duration (10+ years)** = Very sensitive; large price swings with rate moves

**Plain English:** Duration tells you how much a bond's price will change if interest rates move. Higher duration = bigger risk/reward.

---

### Modified Duration
**What it is:** Adjusted duration that directly shows price change per 1% interest rate move.

**What it means:**
- **Modified duration = 4.5** = If rates rise 1%, bond price drops 4.5%
- **Modified duration = 7.2** = If rates rise 1%, bond price drops 7.2%

**Plain English:** The practical version of duration. Shows the actual percentage price move for each 1% rate change.

---

### Convexity
**What it is:** Fine-tuning to duration; accounts for the curve in the bond price/yield relationship.

**What it means:** Duration is a straight-line approximation; convexity is the curve.

**Plain English:** For large interest rate moves, convexity becomes important. Most investors can ignore it for bonds held long-term.

---

### Coupon Rate
**What it is:** Annual interest payment as a percentage of face value.

**Example:** A $1,000 bond with 4% coupon pays $40 per year ($10 quarterly).

**Plain English:** The guaranteed income you get each year. Different from yield (which includes price moves).

---

## Portfolio Metrics

### Allocation
**What it is:** How your portfolio is divided among asset types: stocks, bonds, cash.

**Common allocations:**
- **Age 30 (growth):** 80% stocks, 15% bonds, 5% cash
- **Age 50 (balanced):** 60% stocks, 35% bonds, 5% cash
- **Age 65+ (conservative):** 40% stocks, 50% bonds, 10% cash

**Plain English:** Your "recipe" for risk and return. More stocks = more risk, more return potential. More bonds = more stability.

---

### Concentration Risk
**What it is:** Risk from having too much money in too few positions.

**Guideline:** Prudent investors keep any single stock under 5% of portfolio.

**Plain English:** If one stock crashes 50%, how much damage to your portfolio? Concentration measures this.

---

### Dividend Yield
**What it is:** Annual dividends as a percentage of current stock price.

**Example:** A $100 stock paying $4/year in dividends has 4% yield.

**Context:**
- **0-2%** = Growth stocks (tech, growth)
- **2-4%** = Balanced stocks (blue chips)
- **4-6%** = Income stocks (utilities, REITs)
- **6%+** = High yield (risky; verify sustainability)

**Plain English:** Your cash income from owning the stock. Higher yield = more income, but check if it's sustainable.

---

### Correlation
**What it is:** How two investments move together. Range: -1 to +1.

**What it means:**
- **+1.0** = Perfectly correlated (move together exactly)
- **+0.5** = Partially correlated (tend to move same direction)
- **0.0** = No correlation (move independently)
- **-0.5** = Partially inverse (tend to move opposite)
- **-1.0** = Perfectly inverse (always move opposite)

**Plain English:** Low correlation = good diversification. Gold and stocks often have negative correlation (when stocks drop, gold often rises).

---

### Spread (Credit Spread, Yield Spread)
**What it is:** Difference in yield between two bonds.

**Example:** If a corporate bond yields 5% and a Treasury yields 2%, the spread is 3%.

**What it means:** The extra return you get for taking on extra risk (corporate default risk).

**Plain English:** Wider spreads = more compensation for risk. Tight spreads = market thinks risk is low.

---

## Risk Classifications (from diversification analysis)

- **Well-Diversified:** 40+ holdings, HHI < 0.05
- **Adequately Diversified:** 20-40 holdings, HHI 0.05-0.15
- **Concentrated:** 10-20 holdings, HHI 0.15-0.30
- **Highly Concentrated:** < 10 holdings, HHI > 0.30

---

## Interest Rate & Bond Concepts

### Risk-Free Rate
**What it is:** Return on U.S. Treasury securities (safest investments).

**Used for:** Baseline in Sharpe ratio; benchmark for comparing other investments.

**Current:** InvestorClaw uses 3-month T-Bill yield (updated daily).

---

### Duration Risk
**What it is:** Risk that changing interest rates will significantly impact bond portfolio value.

**High duration risk:** Long-duration bonds; rates rising = significant losses.

**Low duration risk:** Short-duration bonds or bond funds; insulated from rate changes.

---

## Questions to Ask Your Advisor

- What's my portfolio's allocation target, and why?
- What volatility should I expect in a normal year?
- How much can I expect to lose in a bad year (worst-case)?
- Is my bond duration aligned with when I need the money?
- Are my dividend yields sustainable, or at risk of being cut?

---

**Last Updated:** April 2026  
**Source:** InvestorClaw v1.0.1 Financial Education System
