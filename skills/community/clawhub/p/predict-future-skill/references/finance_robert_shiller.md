# Robert Shiller — Finance Forecasting

Yale; Nobel 2013 (with Fama and Hansen). Primary sources: Campbell & Shiller
(1988, *Journal of Finance*); *Irrational Exuberance* (2000/2005/2015);
*Irrational Exuberance* Nobel lecture (2013); *Narrative Economics* (2019);
[data.yale.edu/~shiller](http://www.econ.yale.edu/~shiller/data.htm).

**Role in the finance stack:** *What* moves prices — valuation anchor + narrative
contagion.

---

## Speculative bubble (operational definition)

From Shiller's Nobel lecture — a bubble is **not** mass irrationality but a
**social epidemic**:

> News of price increases spurs investor enthusiasm, which spreads by
> psychological contagion from person to person, amplifying stories that justify
> the price increases and drawing in a larger class of investors.

Prices shift when superficially plausible narratives win debates — amplified by
media — not only when fundamentals change.

**Track record:** *Irrational Exuberance* published March 2000 (dot-com peak);
2005 edition warned on housing before 2007–09 crisis.

For **30-day forecasts**: name the **active narrative** (AI supercycle, soft
landing, tariff spiral) and whether it is **emerging or exhausted** (already
front-page → often late, not early).

---

## CAPE (Shiller P/E, PE10)

**Formula:** current price ÷ average **real** (inflation-adjusted) earnings over
the prior 10 years. Smooths business-cycle earnings spikes (e.g. COVID-era
distortions to simple P/E).

**Empirical finding (Campbell & Shiller 1988):**
- Higher CAPE (lower earnings yield) → **lower subsequent long-horizon returns**.
- 10-year return regressions: R² ≈ **0.57** with CAPE vs. ~0.30 for simple
  earnings yield (Shiller, Yale data notes).
- Presented to the Federal Reserve Dec 1996 when CAPE was historically extreme;
  subsequent decade bore out weak real returns.

CAPE yield remains among the stronger **long-horizon** equity predictors in
academic work (Wharton/Shiller slides, 2018; Fed SF EL 2017).

**Limits — state these in every forecast:**
| Limit | Why it matters |
|-------|----------------|
| **Poor short-term timing** | High CAPE can persist years (1990s Japan, late 1990s US) |
| **No fixed "fair" CAPE** | Real rates, inflation, and payout policy shift equilibrium (fair-value CAPE models) |
| **Earnings definition** | GAAP vs. NIPA debates — use **historical comparison within one series** |
| **Linear extrapolation risk** | Regression from "normal" eras may overstate bearishness in structurally shifted regimes |

Use CAPE for **expected return direction over your horizon**, not "crash in 30
days." Pair with `finance_hyman_minsky.md` when valuation is extreme **and**
financing is fragile.

---

## Excess volatility & narrative economics

Shiller (*Market Volatility*, 1989): stock prices move far more than dividend/
earnings fundamentals alone would imply — behavior and stories matter.

**Narrative economics** (*Narrative Economics*, 2019): popular stories spread
like epidemics (contagion rate, recovery rate) and shift consumption, investment,
and prices. Historical analogies (1929, Japan 1990s, Smoot-Hawley) can move
behavior even when the analogy is imperfect — track **which ghost story is
active** in media and policy rhetoric.

---

## How to apply in this skill

Layer on `general_Philip_Tetlock.md` for finance queries.

1. **Narrative** — Dominant story, contagion stage, who is still not positioned.
2. **Valuation** — CAPE or sector multiple vs. own history; implied long-run
   return skew (higher/lower), not crash date.
3. **Bubble check** — Is price rise feeding new stories feeding new buyers?
4. **Cross-check Minsky** — Extreme valuation + fragile credit → widen downside
   scenario probability.

**Search targets:** Shiller online data (CAPE, housing), sector P/E vs. 10-yr
history, news/social narrative volume, Case-Shiller HPI for housing queries.
