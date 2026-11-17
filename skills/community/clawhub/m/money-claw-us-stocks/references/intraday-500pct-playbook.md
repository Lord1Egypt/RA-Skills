# 500% Extreme-Move Intraday Playbook

This reference governs 5-minute execution after `score_candidates.py` has
classified a security. It is an event-driven momentum/squeeze process, not
risk-free arbitrage. Extreme moves can halt, gap through stops, or become
untradeable without notice.

## Non-negotiable ordering

1. Run the upstream structure and supply gates.
2. Verify the catalyst with primary sources.
3. Classify the live 5-minute phase.
4. Enter only after a retest confirms price, VWAP, turnover, and spread.
5. Reduce risk as the move becomes parabolic; never use technical strength to
   override dilution, a halt, or an upstream status other than `EXECUTE`.

## Catalyst fermentation

Use a timestamped catalyst log. Preserve what was knowable at each decision
time; do not import later headlines into an earlier label.

| Stage | Operational definition | Trading consequence |
|---|---|---|
| `UNVERIFIED` | Social post, screenshot, or secondary headline without a primary source | No new entry |
| `FRESH` | Primary source published within 30 minutes | Monitor spread and initial price discovery |
| `FERMENTING` | 30–120 minutes; price and unique-volume participation continue to expand | Best window for a confirmed first or second retest |
| `CROWDED` | Older than 120 minutes or already vertically repriced | Require tighter retest; prefer managing an existing position |

Primary sources include SEC filings, company investor-relations releases, court
or regulator publications, and named-counterparty releases. Score materiality
separately from credibility:

- Compare annualized economic value with market capitalization and prior-year
  revenue.
- Discount unsigned awards, unnamed counterparties, long implementation
  periods, non-binding memoranda, and company-only promotion.
- Check recent S-1/F-1, resale registration, ATM, warrants, convertibles,
  exchange-compliance notices, and reverse splits before any entry.

## 5-minute state machine

| Phase | Observable pattern | New entry | Existing long |
|---|---|---|---|
| `OPEN_CONFIRMATION` | Above/near VWAP but insufficient MA stack or turnover evidence | Wait | Wait |
| `TREND_EXPANSION` | `last >= VWAP`, `last >= MA5 >= MA10 >= MA20`, turnover expanding | Enter only on confirmed retest | Hold; trail below structure |
| `CONTROLLED_PULLBACK` | Gain >=50%, 8–25% below high, still above VWAP and MA20 | Retest entry permitted | Reduce to core |
| `PARABOLIC_EXTENSION` | Gain >=150% and >=40% above VWAP or >=12% above MA5 | No chase | Scale out 50–80% |
| `BLOW_OFF_DISTRIBUTION` | Gain >=250%, >=10% off high, bar volume >=2x 5-bar average, plus below MA5 or non-positive MACD histogram | No new entry | Exit runner |
| `FAILED_TREND` | Below VWAP or >=30% below high | No entry | Exit |
| `HALTED` | Exchange halt | No orders based on stale quotes | Re-evaluate after resumption |
| `WAIT_DATA` | Missing price, high, VWAP, or prior close | No entry | Manual data repair |

## Retest confirmation

Set `retest_confirmed=true` only when all conditions are observed:

- A completed 5-minute bar holds VWAP or the prior breakout level.
- The next bar trades above the retest bar high.
- Pullback volume contracts versus the impulse bar.
- Bid/ask spread is no more than 2.50%.
- No active halt and `premarket_supply_risk == false`; any confirmed supply risk
  must already have forced the upstream candidate to `EXCLUDE`.

Do not buy the first vertical bar, a halt-resumption market order, or a
breakout whose spread cannot be measured.

## Risk and position management

Default per-trade account risk:

`risk_budget = account_equity × 0.25%`

`shares = floor(risk_budget / (entry_price - stop_price))`

Rules:

- Maximum two entry attempts per symbol.
- Maximum realized plus open session risk: 0.50% of account equity.
- Stop belongs below a verified 5-minute structure level, not at an arbitrary
  percentage.
- Never average down.
- In `PARABOLIC_EXTENSION`, sell 50–80% and trail the remainder.
- In `BLOW_OFF_DISTRIBUTION`, exit the runner; a high-volume late bar below
  MA5 is supply, not a fresh breakout.
- Exit regular-session positions by 15:55 ET unless a separately tested
  overnight strategy explicitly authorizes holding.
- Do not naked-short a low-float squeeze. Borrow recalls, halts, and unbounded
  gap risk make it a different strategy.

## CLI

Run the upstream gate first:

```powershell
python scripts/score_candidates.py candidates.json --format json
```

Then feed live 5-minute snapshots to:

```powershell
python scripts/classify_intraday_phase.py snapshots.json --format markdown
```

Optional snapshot fields:

`symbol`, `timestamp`, `candidate_status`, `position_state`, `prev_close`,
`open_price`, `last_price`, `high_price`, `vwap`, `bid`, `ask`, `ma5`, `ma10`,
`ma20`, `current_bar_volume`, `bar_volume_ma5`, `macd_hist`, `halted`,
`dilution_overhang`, `premarket_supply_risk`, `supply_risk_type`,
`supply_risk_source`, `supply_risk_checked_at`, `turnover_expanding`, `retest_confirmed`,
`official_primary_source`, `catalyst_age_minutes`, `account_equity`,
`entry_price`, `stop_price`.

The phase classifier is a deterministic execution aid. It is not a forecast of
the probability of another 500% move.
