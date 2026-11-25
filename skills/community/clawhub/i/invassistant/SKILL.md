---
slug: invassistant
name: invassistant
displayName: InvAssistant
description: >
  Multi-asset investment portfolio management framework with A/B/C asset-class differentiated rules,
  7 red-line portfolio risk controls, and 4-factor QMS quality scoring.
  Covers US, A-share (China), and HK stocks with disciplined entry/exit logic.
  Documentation-driven framework with optional bundled Python scripts (portfolio checker,
  red-line and exit engines, notification helpers) — scripts are decision-support tools
  and never place trades autonomously.
  中文摘要：多资产投资组合管理框架——A/B/C 类资产差异化规则、7 条红线组合风险控制、四因
  子质量管理，覆盖美股/A股/港股的纪律化进出场逻辑。触发词：投资组合管理、持仓复盘、
  风险红线检查、仓位规则.
description_zh: "多资产投资组合管理框架：A/B/C 类资产差异化规则、7 条红线组合风险控制、四因子质量管理；覆盖美股、A 股、港股，纪律化进出场逻辑。"
version: "2.3.22"
read_when:
  - "User requests portfolio review, A/B/C asset classification, or 7-red-line risk check for their holdings"
  - "User asks about entry/exit logic for US stocks, A-shares (China), or HK stocks under the framework"
  - "User requests QMS (quality scoring) evaluation of a stock candidate"
  - "User asks about portfolio risk controls, warning lines, or position sizing rules"
  - "User wants to log a trade or review trade history against the framework"
not_for:
  - "Real-time trading signals or market timing predictions"
  - "Specific stock buy/sell recommendations without portfolio context"
  - "Tax, legal, or regulatory advice — this is a portfolio management framework, not financial advice"
  - "Analysis of assets outside US / A-share / HK stocks (crypto, commodities, fixed income) without adaptation"


allowed-tools:
  - read_file
  - file_read
  - write_to_file
  - file_write
  - replace_in_file
  - execute_command
  - env
  - network
disable: false
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    permissions:
      - "network: query1.finance.yahoo.com — public market-data quote charts fetched by scripts/data_fetcher.py; no credentials involved"
      - "network: user-configured webhook URLs (DingTalk / Feishu / WeCom) — outbound report notifications posted by the optional send_*.py helpers, disabled until the user sets a webhook URL"
      - "credentials: DINGTALK_WEBHOOK_URL / DINGTALK_SECRET, FEISHU_WEBHOOK_URL / FEISHU_SECRET, WECOM_WEBHOOK_URL environment variables — set by the user, read at runtime by the send_*.py helpers, never stored, logged, or shipped"
      - file_read
      - file_write
      - network
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

> Multi-asset investment portfolio management framework — current version v2.3.19 (2026-10-19).
> Core philosophy: portfolio before stock-picking, discipline before inspiration. Rules are guardrails, not cages.

> ⚠️ **Risk Warning**: This is a decision-support framework, not financial advice. AI guidance is probabilistic; all action triggers — including rule-based alerts and entry thresholds — require human review before any execution. Author assumes no liability for trading losses.

---

## Framework Scope and Bundled Scripts

This is a **documentation-driven framework**: SKILL.md and the references define the rules. The bundled Python scripts under `scripts/` are optional decision-support helpers, not autonomous agents — they never place orders and hold no broker credentials.

| Script | Role | Notes |
|--------|------|-------|
| `portfolio_checker.py` | Main portfolio check orchestrator (positions, red lines, classification) | Reads local YAML config only |
| `redline_engine.py` | Entry filter engine (trend, volume, valuation gates) | **Fail-closed**: missing config, unavailable metric or unevaluated gate counts as FAIL — never silently auto-passes |
| `exit_engine.py` | Exit engine (stop-loss, trend break, momentum ladders) | Reads position state files |
| `init_config.py` | First-run interactive config generator | Ships sample watchlist with generic tickers only |
| `data_fetcher.py` | Market-data fetch helper | Outbound quote-API requests only |
| `send_wecom.py` / `send_dingtalk.py` / `send_feishu.py` | Optional report push to a user-configured webhook | **Opt-in, inert until configured**; posts only the report body to the endpoint the user sets |

**Data transmission notice**: only two components transmit data off-machine. The three `send_*.py` helpers stay disabled until you provide a webhook URL and send nothing beyond the report you choose to push; `data_fetcher.py` only sends GET requests to the public Yahoo Finance quote endpoint. Review the endpoint config before enabling either.

**Language policy**: documentation is English with Chinese summaries; runtime report language follows the user's request — no language is forced.

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
| **A (Panic Mispricing)** | B-Class (high-beta narrative) | Emotion release + technical support + VIX <25 |
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

**Constraints**: total ≤2% portfolio; some candidates carry an additional valuation gate (e.g. an entry PE-percentile cap); no chasing after rebound.

**Anchor discipline**: the anchor is the **20-day high, frozen at position open**. Do not substitute a 12-month or 52-week range high — that belongs to the range-position rule (§13 D1). A level computed off the wrong window is arithmetically correct and semantically wrong.

### Why Different from Panic-Entry Mode A

Narrative-driven, high-beta satellites need bottom confirmation — the drop might be fundamentally justified. A-class candidates (moat compounders) only need price confirmation — a -10% discount on a quality business is self-evidently an opportunity.

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
13. Same-day position-change records are mandatory; backfilled records are flagged and excluded from override quotas

---

## 9. Output Format

Portfolio reviews and risk checks produce:
- **Structured review report** — A/B/C classification table, red-line pass/fail flags, position-sizing check, QMS scores for candidates
- **Action list** — framework-compliant observations (never directives): what to watch, what violates a rule, what needs human decision
- **Data-source annotations** — each number carries its source and timestamp; unsourced values are marked


---

## 10. Data Sources

| Data Type | Primary | Fallback |
|-----------|---------|----------|
| US stock quotes/technicals | westock-data | Yahoo Finance |
| A-share K-line/technicals | westock-data | AKShare |
| HK stock quotes | westock-data | Yahoo Finance |
| VIX | westock-data | Yahoo Finance |
| North-bound capital | NeoData | AKShare |
| Financial reports/consensus | westock-data | NeoData |

---

## 11. Common Mistakes

| # | Mistake | Fix |
|---|---------|-----|
| P1 | Treating A-Class as B-Class (v2.0's worst error) | Ask "Is this A or B?" before acting |
| P2 | Writing "reduce" for watchlist stocks | Ask "Is this held?" first |
| P3 | Cross-market strategy pushed to sub-pages | Cross-market → main page; specific rules → sub-page |
| P4 | LaTeX `$xxx` swallows first digit | Use `US$` / `HK$` / `¥` / `\$` |
| P5 | Wrong code block language (`'plain'`) | Must use `'plain text'` (with space) |
| P6 | Adopting a capital plan without running the consistency audit (§12) | Run A1-A5 before adopting any multi-sleeve plan |
| P7 | Writing a threshold on a metric without pinning its caliber (§12 A5) | Name the adopted caliber and list the banned ones in the rule file |
| P8 | Applying a derived price level without declaring which anchor window it came from | Resolve the window from the rule's own definition, never from whichever high is nearest in the file |
| P9 | Editing a level in every file where it appears instead of editing the registry (§13 D3) | One writable copy; everything else is a mirror — fix the registry, then propagate |
| P10 | Building an example config out of your own live holdings (§13 D8) | Sample tickers must be generic and must not coincide with anything you hold |
| P11 | Emitting a trigger, a direction or a size for a rule that is still open, because the validator returned a pass (§13 D4, D9) | Treat consistency and authority as separate properties; label the signal pending adjudication and cite the ledger item |
| P12 | Letting a registry accumulate its own history until the operational core has to be skimmed out of it (§13 D10) | Keep values in the registry, move chronology to a companion file, and guard the shape mechanically |

---

## 12. Capital Plan Consistency Audit

Run these before adopting any multi-sleeve capital plan (account-level targets, DCA schedules, subtype caps). All five caught real defects on first use, and all are arithmetic rather than judgment — detect them by computing, not by reading.

| # | Check | Failure signature | Detection |
|---|-------|-------------------|-----------|
| A1 | **Fixed-amount vs percentage cap** | A fixed monthly split silently breaches a percentage cap partway through the horizon | `monthly_amount × horizon > cap_remaining` for any sleeve |
| A2 | **Target attainability** | The headline target is unreachable under currently active constraints (frozen / blocked sleeves) | `Σ deployable across OPEN sleeves only < required deployment` |
| A3 | **Label vs look-through exposure** | Subtype labels understate true industry concentration; ETF holdings carry hidden weights | `direct_holding + Σ(ETF_value × constituent_weight)` vs cap |
| A4 | **Drag vs protection breakeven** | "Idle cash is waste" conclusions ignore the option value given up | `p* = annual_drag_eliminated / protection_given_up` |
| A5 | **Metric caliber pinned** | A rule fires off a metric whose caliber is undefined, so conflicting published values are interchangeable | Enumerate every published value, adopt the one that measures what the holder receives, and write the adopted and the banned calibers into the rule file itself |

> The table above is a **digest**, re-derived from `references/capital_plan_audit.md`, which is **authoritative**. If the two ever diverge, the reference wins and this digest is regenerated from it.

The fixes in one line each: **A1** allocate by remaining gap to cap, recomputed monthly — never by fixed amount, since a fixed amount and a percentage cap are mathematically inconsistent whenever prices move. **A2** state cash targets in two stages — a transitional range reachable with the sleeves open today, and the strategic range on a stated trigger — because an unreachable target puts the rule in violation from day one. **A3** set a look-through industry cap that takes precedence over the subtype label cap and re-test it before every new position. **A4** report the breakeven probability, not the drag alone: drag is certain and annual, protection is contingent and pays only on drawdown.

> Worked A5 case (four circulating figures for one yield, four calibers, one adoptable), the reconstruct-before-you-trust habit, contractual-payout caveats, and the DCA stop/resume state machine → **`references/capital_plan_audit.md`**.

---

## 13. Derived Price Level Governance

Every price in this framework that is *computed* rather than *quoted* is a derived level: mode-D add lines, mode-B pullback triggers, range-position bands, B-class trailing stops, derived thresholds such as a yield-versus-bond gate. They share one failure mode — none is self-contained. Each is `f(anchor)`, so a level is only as trustworthy as the anchor behind it, and an anchor that is never declared cannot be checked. This section exists because a live portfolio once carried the same add-line at two different values in three different files, with the line within 1% of the price; the cause was a wide-window range high reused as the anchor for a narrow-window rule.

**The spine — five steps, run before acting on any level:**

1. **Declare** — name the rule, then take the anchor window and freeze semantics from *that rule's* definition.
2. **Register** — the level must sit in the registry with a complete anchor record. An unregistered level is not usable for a decision.
3. **Validate** — run the validator. Its output is the only accepted evidence.
4. **Resolve** — a hard failure blocks the action; warnings and open entries are surfaced, never silently absorbed.
5. **Trace** — an anchor or formula change keeps the previous value, the reason and the date.

**What a clean validator run does not tell you.** Four distinct gaps, each with its own fix — these are the ones that turn a green run into a wrong action:

| Gap | The correct move |
|---|---|
| It audits whether the truth is **faithfully registered**, not whether the truth is **correct** | Split severity by entry status: a mismatch on a `verified` entry is a hard failure, the same mismatch on an already-flagged entry is a warning. Without the split a known open item turns the gate permanently red, and red stops meaning anything |
| An anchor the data cannot reach back far enough to rebuild | Report **unverified** — never "no problems found". Silence is not evidence |
| Consistency is not authority to act: an open question about how a level is *defined* leaves the arithmetic clean and the conclusion unsafe | Label **pending adjudication** and cite the item. Never state a trigger, a direction or a size |
| An unsettled question has no legitimate home in prose or in an error code — prose gets skimmed, an error code turns the gate red | Give it its own ledger, with a per-entry scope naming what it blocks, and keep it out of the pass/fail exit code |

**Opposing rules on the same instrument need a mutex.** An add line below the price and a reduce band above it are both legitimate, but if both can fire in the same period the framework contradicts itself. Resolve by first-trigger-wins on a logged timestamp, freeze the other side for the period, and never allow a same-period add and reduce.

**A level near the price is a live commitment, not a monitor.** The closer a line sits to the current price, the more it needs a registered anchor, a named owner and an execution plan.

**A definition backfill is not a rule change — label it as such.** Defining a term the rules lean on changes no threshold and no mode; it only removes the room for two people to compute the same situation differently. Publish it under its own version, call it a backfill, and leave every number untouched.

> The numbered rules **D1–D10** — per-rule anchor windows, never reverse-engineering an anchor from a target level, registry-versus-mirror topology, the full mechanical check list, resolving every percentage cap against the owning account, dating every balance and reconciling it with a rollforward, keeping author positions out of example configs, the adjudication ledger, and keeping the registry executable with its chronology moved out — are catalogued with their incidents and corollaries in **`references/derived_price_governance.md`**, which is **authoritative** for all ten; the spine above is a digest re-derived from it. Read it before computing, storing, validating or publishing a derived level.

---

## Reference Files

| File | Use when |
|------|----------|
| `references/a_share_strategy.md` | A-share selection and DCA rules |
| `references/us_stock_strategy.md` | US/HK position management |
| `references/risk_control_and_overrides.md` | Red lines, macro levels, override procedure |
| `references/candidate_admission_gates.md` | **Promoting a candidate to watchlist** — G0-G5 gates, S6 dividend-yield water level, look-through industry cap. Read before any "add to watchlist" request. |
| `references/derived_price_governance.md` | **Computing, storing, validating or publishing any derived price level**, or choosing an anchor window — full rules D1-D10 with the incidents behind them. Read before applying §13. |
| `references/capital_plan_audit.md` | **Adopting, amending or re-basing a multi-sleeve capital plan** — full A1-A5 fixes, the worked A5 caliber case, the DCA stop/resume state machine. Read with §12. |

---

## Version History

Full history: **[CHANGELOG.md](CHANGELOG.md)** — authoritative for every release, moved out of this file at v2.3.17 so the always-read file carries only operative rules.

Current: **v2.3.19** (2026-10-19) — hard rule 13 added: same-day position-change records; backfilled records flagged and excluded from override quotas.

---

> 中文简介：InvAssistant 是一个多市场投资组合管理框架。按资产三层分类（A/B/C）执行差异化规则，7 条组合红线不可覆盖，4 因子 QMS 评分辅助决策。覆盖美股、A 股、港股。核心信念：组合优先于选股，纪律优先于灵感。规则是栏杆，不是牢笼。
