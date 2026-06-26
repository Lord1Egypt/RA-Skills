---
name: invassistant
description: >
  Multi-asset investment portfolio management framework with A/B/C asset-class differentiated rules,
  7 red-line portfolio risk controls, and 4-factor QMS quality scoring.
  Covers US, A-share (China), and HK stocks with disciplined entry/exit logic.
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - execute_command
disable: false
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    tags:
      - investment
      - trading
      - portfolio
      - stock
      - finance
      - us-stock
      - a-share
      - hk-stock
      - risk-control
---

# InvAssistant

> Multi-asset investment portfolio management framework — current version v2.1.2 (2026-06-06).
> Core philosophy: portfolio before stock-picking, discipline before inspiration. Rules are guardrails, not cages.

---

## 1. Asset Classification (Three Tiers)

This is the foundation of v2.1+. Different assets use different exit logic.

| Tier | Definition | Rules | When To Sell |
|------|-----------|-------|-------------|
| **A-Class (Platform Core)** | Long-moat, cash-flow-stable platform companies | HOLD, no trailing stop; DCA entries | Only 3 reasons: ① fundamental deterioration (2+ quarters) ② narrative change ③ portfolio limit breach |
| **B-Class (High-Beta Cyclical)** | High-beta, narrative-driven growth | Trailing stop + position management | QMS < 40 triggers review |
| **C-Class (Low-Volatility Income)** | Broad-market/dividend ETFs, utilities | DCA + rebalancing | No active timing |

Key insight: A-class price drawdowns ≠ sell signals. Using trailing stops on A-class washes out long-term compounders.

---

## 2. Portfolio Risk Controls: 7 Red Lines (Non-Overridable)

| # | Rule | Threshold | Action |
|---|------|-----------|--------|
| 1 | Single position concentration | >25% | Reduce to ≤20% within 3 months |
| 2 | Single sector concentration | >35% | Reduce to ≤30% within 3 months |
| 3 | AI single-narrative | >50% | Reduce to ≤40% within 6 months |
| 4 | Portfolio drawdown (mild) | >-12% | Halve satellite positions |
| 5 | Portfolio drawdown (severe) | >-15% | Total position ≤60% |
| 6 | VIX systemic risk | ≥40 | Reduce total to ≤50% |
| 7 | Pre-Trade Log compliance | <100% | Log immediately |

---

## 3. US Stock Strategy

### Entry Modes

| Mode | Applies To | Logic |
|------|-----------|-------|
| **A (Panic Mispricing)** | B-Class (TSLA/NVDA extreme) | Emotion release + technical support + VIX <25 |
| **B (Trend Confirmation)** | B-Class | Price > MA50 + breakout + fundamentals + valuation |
| **C (Rebalancing)** | Portfolio-level | Triggered by Red Lines 1-3 only |
| **D (A-Class Candidate Zone Entry)** | Candidate pool (non-tech diversification targets) | Callback-based, no observation delay |

### Mode D: A-Class Candidate Zone Entry (v2.1.1)

Applied to new A-class candidates before they join the core portfolio. Designed to solve the "observation delay misses entry window" problem.

**Principle**: No observation delay. A -10% pullback from 20D high on an A-class candidate is itself a complete entry signal — the underlying moat business doesn't change with share price.

| Zone | Trigger | Allocation | Execution |
|------|---------|------------|-----------|
| First tranche | -10% from 20D high | 50% of target | Execute immediately |
| Add | -15% (or >3% further drop after first) | 30% | Execute on trigger |
| Final | -20% (or 5+ days sideways without new low) | 20% | Within zone |

**Constraints**: total ≤2% portfolio; MCO requires PE percentile <60%; no chasing after rebound.

### Why Different from TSLA Mode A

TSLA (B-Class satellite) needs bottom confirmation — the drop might be fundamentally justified. A-class candidates (moat compounders) only need price confirmation — a -10% discount on a quality business is self-evidently an opportunity.

---

## 4. A-Share Strategy (3-Condition Engine)

All three conditions must pass for entry:

| Condition | Standard |
|-----------|----------|
| ① Engine score ≥80 + 3 consecutive days on list | Core selection pool |
| ② Current price ≤ dynamic target (with floor) | `max(static×0.85, min(static, MA20×0.95))` |
| ③ MA20 flat or turning up | MA20 delta ≥ -0.05 |

**Flex window**: 2/3 conditions met + 3rd deviation ≤10% → half-position trial.
**Time stop**: 6 months max in selection pool without entry → forced review.

---

## 5. HK Stock Strategy

| Source | Framework |
|--------|-----------|
| Actively bought | Follow A/B/C classification rules |
| Company allocation/incentive | Warning line + reduction framework (not hard stop) |

**Warning line** (not hard stop): Triggers 48h review upon breach.
**Time limit**: 18 months post-vesting with remaining position → unconditional full exit.

---

## 6. QMS Scoring (4-Factor)

```
QMS = 0.35 × Earnings Trend
    + 0.25 × Sector Relative Strength
    + 0.25 × EPS Revision
    + 0.15 × Price Structure
```

| Score | Meaning | Action |
|-------|---------|--------|
| ≥70 | High quality + good timing | Hold / observe entry |
| 50-70 | Healthy, not at entry point | HOLD |
| <50 | Quality or timing issues | No new positions |
| <40 | Review exit queue | Evaluate reduction (B-Class only) |

**Boundary**: QMS is entry reference for A-Class, NOT an exit trigger. Only B-Class uses QMS <40 as reduction signal.

---

## 7. Monthly KPIs

| KPI | Threshold | Type |
|-----|-----------|------|
| Monthly turnover rate | ≤15% | Red line |
| Pre-Trade Log compliance | =100% | Red line |
| A-Class sold on price volatility | =0 | Red line |
| Panic-period reduction (VIX≥30) | =0 | Red line |
| System execution rate | ≥80% | KPI |

---

## 8. Hard Rules Summary

1. Asset classification determines action semantics: A-Class no trailing stop, B-Class uses trailing stop
2. Held vs. watchlist semantics must not be mixed
3. A-share 3-condition is a filter: all pass → entry (flex window = 2/3 + deviation + half-size)
4. US B-Class dual-mode: Mode A (3 red lines all pass) / Mode B (4 conditions all pass)
5. Unfilled ≠ holding: portfolio data must reflect actual positions
6. Never fabricate data: all indicators must come from live data sources
7. A-Class only sells on 3 fundamental reasons (never price)
8. 7 Red Lines triggered = must follow, no override
9. Allocation/incentive positions do not use standard stops
10. Every override must be logged
11. Max 2 overrides per ticker per quarter; 3rd is void
12. Daily self-check: 5 questions, all "no" = no trade today

---

## 9. Data Sources

| Data Type | Primary | Fallback |
|-----------|---------|----------|
| US stock quotes/technicals | westock-data | Yahoo Finance |
| A-share K-line/technicals | westock-data | AKShare |
| HK stock quotes | westock-data | Yahoo Finance |
| VIX | westock-data | Yahoo Finance |
| North-bound capital | NeoData | AKShare |
| Financial reports/consensus | westock-data | NeoData |

---

## 10. Common Mistakes

| # | Mistake | Fix |
|---|---------|-----|
| P1 | Treating A-Class as B-Class (v2.0's worst error) | Ask "Is this A or B?" before acting |
| P2 | Writing "reduce" for watchlist stocks | Ask "Is this held?" first |
| P3 | Cross-market strategy pushed to sub-pages | Cross-market → main page; specific rules → sub-page |
| P4 | LaTeX `$xxx` swallows first digit | Use `US$` / `HK$` / `¥` / `\$` |
| P5 | Wrong code block language (`'plain'`) | Must use `'plain text'` (with space) |

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| v2.1.2 | 2026-06-06 | Audit cleanup: bilingual README, remove legacy files |
| v2.1.1 | 2026-06-04 | Mode D: A-class candidate zone entry (no observation delay) |
| v2.1 | 2026-05-18 | A/B/C asset classification; 7 red lines; 4-factor QMS; trailing stop removed from A-class |
| v2.0 | 2026-05-18 | Full rebuild: decision pyramid, 5-factor QMS, 10 red lines (replaced) |
| v1.5 | 2026 Q1-Q2 | 3-condition engine, dual-mode entry, trailing stops |

---

> 中文简介：InvAssistant 是一个多市场投资组合管理框架。按资产三层分类（A/B/C）执行差异化规则，7 条组合红线不可覆盖，4 因子 QMS 评分辅助决策。覆盖美股、A 股、港股。核心信念：组合优先于选股，纪律优先于灵感。规则是栏杆，不是牢笼。
