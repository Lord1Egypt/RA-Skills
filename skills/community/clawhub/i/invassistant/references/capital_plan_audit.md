# Capital Plan Consistency Audit — full procedure A1–A5

> Companion to `SKILL.md` §12. That section carries the five checks with their failure signatures and detection
> formulas; this file carries the full fixes, the worked A5 caliber case, and the two follow-on habits A5
> surfaced.
>
> **Load this before adopting, amending or re-basing any multi-sleeve capital plan** (account-level targets,
> DCA schedules, subtype caps).

## 12. Capital Plan Consistency Audit

Run these checks before adopting any multi-sleeve capital plan (account-level targets, DCA schedules, subtype caps). All of them caught real defects on first use; all are arithmetic, not judgment — detect them by computing, not by reading.

| # | Check | Failure signature | Detection |
|---|-------|-------------------|-----------|
| A1 | **Fixed-amount vs percentage cap** | A fixed monthly split silently breaches a percentage cap partway through the horizon | `monthly_amount × horizon > cap_remaining` for any sleeve |
| A2 | **Target attainability** | The headline target is unreachable under currently active constraints (frozen / blocked sleeves) | `Σ deployable across OPEN sleeves only < required deployment` |
| A3 | **Label vs look-through exposure** | Subtype labels understate true industry concentration; ETF holdings carry hidden weights | `direct_holding + Σ(ETF_value × constituent_weight)` vs cap |
| A4 | **Drag vs protection breakeven** | "Idle cash is waste" conclusions ignore the option value given up | `p* = annual_drag_eliminated / protection_given_up` |
| A5 | **Metric caliber pinned** | A rule fires off a metric whose caliber is undefined, so conflicting published values are interchangeable | See A5 below |

**A1 fix**: allocate by remaining gap to cap, recomputed monthly — never by fixed amount. A fixed amount and a percentage cap are mathematically inconsistent whenever prices move.

**A2 fix**: state cash targets as two stages — a transitional range that is actually reachable with the sleeves open today, and the strategic range that becomes reachable on a stated trigger. Writing an unreachable target puts the rule in violation from day one.

**A3 fix**: set a look-through industry cap that takes precedence over the subtype label cap. Re-test before every new position, since adding a direct holding and growing an ETF sleeve compound.

**A4 fix**: report the breakeven probability, not the drag alone. Drag is certain and annual; protection is contingent and only pays on drawdown. A drag of 0.1% p.a. is not worth buying with concentration risk.

### A5 — Pin the caliber of every threshold metric

If a rule says "yield < X triggers Y" without defining how yield is measured, the rule is undefined, not implemented. Published values for the same instrument routinely differ by 2x. Worked example on a dividend ETF — four circulating figures, four different calibers:

| Figure | Caliber | Verdict |
|---|---|---|
| 2.44% | Year-to-date distributions ÷ price. **Not annualised**; at mid-year only half of the year's four payments are counted, so it understates at every mid-year point | Ban |
| 4.34% | Trailing four actual distributions ÷ current price | **Adopt** |
| 4.88% | Index yield, rolling, pre-tax, before fund fees | Ban |
| 4.93% | Index yield, index-provider periodic-review basis — updated once a year, denominator is a lagged average market cap | Ban |

**A5 procedure**: enumerate every published value with its caliber; adopt the one that measures what the holder actually receives; write the adopted caliber and the banned calibers into the rule file itself. Then apply A5 to the *other* side of the comparison too — a yield-vs-bond threshold also needs the bond yield pinned (curve yield vs on-the-run yield vs third-party quote differ by 5-15bp), and stale reference rates silently inflate the buffer.

Two follow-on habits that A5 surfaced:

- **Reconstruct suspicious figures before trusting or discarding them.** Back-solving `dividends ÷ yield` gave an implied price of 1.4344 against an actual NAV of 1.4522, which identified the caliber definitively. A number you cannot reconstruct is a number you have not checked.
- **Check whether the payout is contractually guaranteed.** Distributions may be conditional (e.g. fund contract requiring excess return over the benchmark before any distribution). A conditional payout makes the yield a binary variable — it can go to zero — which no continuous threshold handles. Track it as a separate monitoring item.

**Related — DCA stop/resume**: model DCA as a state machine (ACTIVE / PAUSED / STOPPED / FROZEN / BLOCKED) with explicit downgrade and upgrade conditions. **Downgrades may be automatic; upgrades must require human confirmation.** An auto-resume buys back right after a rebound, which is a systematic momentum-chasing switch. Also separate "plan completed" (position count reached — resume needs a new plan) from "risk halt" (cap breached — resume when the ratio falls back); treating both as one frozen state loses the distinction.

Give a thin threshold buffer a false-trigger guard (require two consecutive confirmations) plus a fast path for genuine deterioration (a single large move suspends immediately). Pausing inflows is cheap; breaking DCA continuity is not, since continuity is the point of DCA.

---
