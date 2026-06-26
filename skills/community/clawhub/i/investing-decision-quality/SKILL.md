---
name: investing-decision-quality
description: Apply a research-grade decision pipeline to every investment idea — news-aware bull/bear synthesis, calibrated probability estimation, decision-process audit (separating process from outcome), Kelly-based position sizing, market-microstructure-aware execution, and concentration discipline. Grounded in seven canonical books (Thorp, Poundstone, Tetlock, Silver, Duke, Harris, Munger) loaded as `references/`. Use whenever the user asks to size a position, decide whether to buy/sell, evaluate a past trade, or stress-test conviction.
metadata:
  openclaw:
    emoji: "🎯"
---

# Investing Decision Quality

This skill imposes a disciplined five-stage pipeline between a research finding and any trade execution. Each stage is grounded in published methodology — when applied, every conclusion must cite the relevant author and book by name. The full books are in `references/` and are loaded on demand.

## When to use

Use this skill whenever the user:

- Asks to size a position ("how much should I buy?")
- Decides to buy or sell ("should I take this trade?")
- Reviews a past trade ("did I make the right call?")
- Tests conviction ("am I sure about this thesis?")
- Builds a research-to-trade checklist for a watchlist

Do **not** use this skill for:

- Pure data lookups (use data MCPs)
- Building DCF / multiples valuation (use `aswath-damodaran-investing`, `fp-dcf`, `stock-valuation`)
- Probability estimation alone without action (use the `superforecaster` agent)

The pipeline assumes the user already has a probability or valuation view to translate into action.

## The Pipeline

Run the stages in strict order. Each stage produces an explicit output that feeds the next. Skip none — if a stage cannot be completed (e.g. no base rate available), surface the gap rather than silently proceeding.

```
Decision Quality Pipeline:
- [ ] Stage 0: News-aware Bull/Bear synthesis
- [ ] Stage 1: Calibrated probability estimation
- [ ] Stage 2: Decision-process audit (separate process from outcome)
- [ ] Stage 3: Position sizing (Kelly with fractional discount)
- [ ] Stage 4: Execution (microstructure-aware)
- [ ] Stage 5: Concentration & opportunity-cost check
- [ ] Final: Research → trade checklist
```

---

## Stage 0 — News-aware Bull/Bear Synthesis

**Why this stage exists:** Probability estimation (Stage 1) depends on the *information set* you start from. If you skip recent material news and idiosyncratic events, your base rate dominates and you systematically miss catalysts that have already happened. This stage forces a deep-news scan and a structured bull/bear synthesis *before* any probability is assigned.

This pre-stage is adapted from multi-agent equity research frameworks where a News Analyst + Bull Researcher + Bear Researcher debate before the Research Manager synthesises. We collapse it into one structured pass.

### 0.1 — News scan (mandatory)

Pull material news for the ticker covering the **trailing 14 days**, from at least three of the following sources:

- **SEC EDGAR**: 8-K filings, 10-Q amendments, insider Form 4 — surface anything not yet "priced in"
- **Finnhub / Yahoo Finance**: company-specific headlines, analyst rating changes, price target revisions
- **Macro news**: Fed / ECB statements, sector-wide regulatory actions, geopolitical events affecting the company's supply chain or end markets
- **Earnings call transcripts** (most recent quarter): management language shifts, guidance changes

For each material item, capture:

```
- date · source · one-sentence headline
- impact direction: bull / bear / ambiguous
- magnitude: small / medium / large (operating impact on next 4 quarters)
- already priced in? (yes / partial / no)
```

If **no material news in 14 days**, state that explicitly — it is itself a signal (quiet period, possibly pre-event).

### 0.2 — Bull case (200–400 words)

Write the **strongest** bull case as if you were paid to be long. Include:

- The 2–3 most powerful positive drivers (with numbers, not vibes)
- Why the *current* price under-reflects them
- What would have to be true in 12–24 months for the bull case to play out
- The single most recent piece of news that supports this case

Do not hedge. Do not say "but". A bull case with hedging is a confused case.

### 0.3 — Bear case (200–400 words)

Write the **strongest** bear case as if you were paid to be short. Include:

- The 2–3 most powerful negative drivers (with numbers)
- Why current price over-reflects optimism
- What would have to be true in 12–24 months for the bear case to play out
- The single most recent piece of news that supports this case

Same rule — no hedging, no "but".

### 0.4 — Synthesis (Research Manager voice)

After both cases are on the page, write a 100–150 word synthesis answering:

- Which case rests on more *recent, verifiable* evidence vs. extrapolation?
- Which case rests on facts the market hasn't fully digested?
- Where do the two cases actually agree? (often: long-run direction; disagreement is on path / timing / multiple)
- What probability does the synthesis suggest for the binary outcome that anchors Stage 1's probability estimate?

This synthesis feeds directly into Stage 1 as the **inside view** that gets reconciled with the outside view base rate.

### Stage 0 output

```
News scan: [N items, dates, sources]
Material catalysts not priced in: [list]

Bull case:
- Driver 1: [...]
- Driver 2: [...]
- Driver 3: [...]
- Key recent evidence: [...]

Bear case:
- Driver 1: [...]
- Driver 2: [...]
- Driver 3: [...]
- Key recent evidence: [...]

Synthesis:
- Stronger case: [bull / bear / coin-flip]
- Reason: [...]
- Probability suggested for Stage 1: [X]% with rough range
```

### Anti-patterns specific to Stage 0

- **Skipping news scan when "you already know the story"** — markets price in what most people know; alpha lives in what hasn't been digested yet
- **Writing a weak bear case "just to be balanced"** — a steel-manned bear case must be argued by someone genuinely trying to win
- **Treating absence of news as confirmation** — silence is data, but it is not evidence

---

## Stage 1 — Calibrated Probability Estimation

**Sources:** Tetlock & Gardner, *Superforecasting* (2015). Silver, *The Signal and the Noise* (2012).

### Principle: Outside view first

> "Always start from the outside view: find the reference class and its base rate, *then* update with case-specific evidence."
> — Tetlock, *Superforecasting*, ch. 5

**How to apply:**

1. Identify the reference class. ("What is the base rate of US large-cap stocks rising 30%+ in 12 months?")
2. Find the historical frequency from data (web search, FRED, Alpha Vantage history). State the number and source.
3. **Only then** layer in case-specific factors (the inside view) and adjust via Bayesian updating.

If the user jumps to "I think NVDA will go up 30% because…", interrupt and ask for the base rate first.

### Principle: Give ranges, never point estimates

> "Probabilistic thinkers express forecasts as distributions, not single numbers. Point estimates are wrong 100% of the time."
> — Tetlock, *Superforecasting*, ch. 6 (echoed by Damodaran's "every valuation is a range")

**How to apply:**

- Output every probability with an 80% confidence interval: `P = 35% [CI 25–48%]`.
- If the user demands a point number, push back: "The most likely value is X, but the range that matters for sizing is X-low to X-high."

### Principle: Brier score discipline

> "Calibration is a learnable skill. Track your forecasts. Target Brier scores below 0.15 for high-quality forecasters."
> — Tetlock, *Superforecasting*, ch. 4

**How to apply:**

- Log every probability statement with date, ticker, horizon, and outcome.
- Compute Brier = Σ(forecast − outcome)² / N at the end of each quarter.
- If Brier > 0.20, you are systematically overconfident or noisy. Widen confidence intervals.

### Principle: Signal vs noise

> "The volume of data has exploded. The signal-to-noise ratio has not. Most patterns you 'see' in market data are noise."
> — Silver, *The Signal and the Noise*, ch. 1

**How to apply:**

- Before incorporating any "pattern" or "indicator", ask: what is the prior probability that this is signal vs noise? In financial time series, default to noise.
- Demand out-of-sample evidence or a causal mechanism. Without one, treat the pattern as noise.

### Stage 1 output

```
Reference class: [...]
Base rate: [X]% (source: [...])
Case-specific evidence: [list]
Bayesian-updated probability: [Y]% with 80% CI [low–high]
```

---

## Stage 2 — Decision-Process Audit

**Source:** Annie Duke, *Thinking in Bets* (2018).

### Principle: Resulting is an anti-pattern

> "Resulting is the tendency to judge the quality of a decision by the quality of its outcome. It is the single most common mistake in poker and in investing."
> — Duke, *Thinking in Bets*, ch. 1

**How to apply:**

- When reviewing any trade (yours or one ClawdBot proposed), ask **"was the process sound?"** before asking "did it make money?".
- A bad process that got lucky is still a bad process — do not reinforce it.
- A good process that lost money is still a good process — do not abandon it.

### Principle: Think in bets, not certainties

> "Every decision is a bet on a probability distribution of futures. Saying 'I'm sure' is almost always wrong."
> — Duke, *Thinking in Bets*, ch. 2

**How to apply:**

- Force every conviction statement into bet form: "I'd bet $X at Y:1 odds." If the user wouldn't take the bet they're proposing, the conviction is fake.
- Ask "what would change my mind?" and write down the answer **before** opening the position. This is the kill criterion.

### Principle: Truth-seeking pod

> "Surround yourself with people who reward truth-seeking, accuracy, and open-mindedness, not those who reward you for being right."
> — Duke, *Thinking in Bets*, ch. 4

**How to apply:**

- Use ClawdBot as the truth-seeking pod. Explicitly ask: "Steel-man the bear case. What am I missing?"
- Do not paper over conflicting evidence. Flag it.

### Stage 2 output

```
Process audit:
- Probability source: [base rate / model / vibes?]
- Belief calibration: [explicit % with CI? or implicit "I think so"?]
- Pre-mortem done: [yes/no — if no, do it now]
- Kill criterion stated: [explicit trigger that would invalidate the thesis]
- Bear case steel-manned: [yes/no]
```

If any answer is "no", do not proceed to sizing.

---

## Stage 3 — Position Sizing (Kelly)

**Sources:** Thorp, *Beat the Market* (1967). Poundstone, *Fortune's Formula* (2005).

### Principle: The Kelly formula

> "The fraction of bankroll to commit to a bet is f* = (bp − q) / b, where b is the net odds, p is the probability of winning, q = 1 − p."
> — Thorp, *Beat the Market*, ch. 4 (Kelly criterion derivation)

For a stock position framed as "buy at $P0, target $P1 with probability p, stop at $P2":

```
b = (P1 − P0) / (P0 − P2)
p = your calibrated probability from Stage 1
q = 1 − p
f* = (b × p − q) / b
```

### Principle: Fractional Kelly, never full Kelly

> "Full Kelly maximises geometric growth in theory but is too aggressive for real investors. Half-Kelly captures ~75% of the growth at ~50% of the variance. Quarter-Kelly is right for most retail investors."
> — Poundstone, *Fortune's Formula*, ch. 14

**How to apply:**

- Default to **quarter-Kelly** (f*/4) for any single position.
- Half-Kelly only if (a) the edge is large and well-tested, and (b) the loss would not bankrupt or force exit.
- Never exceed full Kelly. Never.

### Principle: Survival before growth

> "2× Kelly produces zero long-run growth. 3× Kelly produces certain bankruptcy. The asymmetry of compounding means survival dominates returns."
> — Poundstone, *Fortune's Formula*, ch. 14 (paraphrasing Thorp)

**How to apply:**

- Stress-test sizing against a 20% drawdown across all current positions. If a coincident drawdown would force exits, reduce sizing.
- Apply additional haircut for correlated bets: a single "factor bet" disguised as 5 tech positions is one Kelly bet, not five.

### Stage 3 output

```
Kelly inputs: p = [...]%, b = [...], q = [...]%
Full Kelly f*: [...]% of portfolio
Recommended fractional Kelly (×1/4): [...]% of portfolio
Correlation haircut: [...]% (if held alongside correlated positions)
Final position size: $[...] (€-equivalent)
```

If full Kelly is negative — the bet has no edge — **do not size, return to research**.

---

## Stage 4 — Execution

**Source:** Larry Harris, *Trading and Exchanges* (2003).

### Principle: Pay attention to the spread

> "Every market order pays the full bid-ask spread plus market impact. Over a year of trading, the spread is the largest controllable cost for retail investors."
> — Harris, *Trading and Exchanges*, ch. 13

**How to apply:**

- For any order > 0.5% of average daily volume, prefer limit orders. State the limit price explicitly.
- Quote the current bid-ask spread and the order's % of ADV before recommending execution method.

### Principle: Avoid limit orders before scheduled news (adverse selection)

> "Standing limit orders are picked off by informed traders when news breaks. The order looks 'filled at a good price' but you are systematically on the wrong side of new information."
> — Harris, *Trading and Exchanges*, ch. 11

**How to apply:**

- Pull all limit orders before earnings, FOMC, CPI, or major company-specific events.
- If the user wants to participate in a news event, use a market order **after** the news prints and the spread has re-tightened (typically 5–15 minutes), not a pre-positioned limit.

### Principle: Time-of-day matters

> "Spreads are widest at the open and tightest in the last hour. Volatility is highest at the open and the close."
> — Harris, *Trading and Exchanges*, ch. 14

**How to apply:**

- For non-urgent orders, prefer the window 10:30–15:30 ET (4:30 PM CET–9:30 PM CET).
- Avoid the opening 15 minutes unless executing a news-driven trade.

### Stage 4 output

```
Order type: [limit / market]
Limit price (if applicable): $[...]
Time window: [...]
Pre-event check: [no scheduled events in next 24h / event at [...]]
Estimated all-in cost: spread $[...] + commission $[...] = $[...] (X bps of position)
```

---

## Stage 5 — Concentration & Opportunity Cost

**Source:** Charlie Munger, *Poor Charlie's Almanack* (2005) and public talks.

### Principle: Bet heavily when the odds are favourable

> "It's not given to human beings to have such talent that they can just know everything about everything all the time. But it is given to human beings who work hard at it — who look and sift the world for a mispriced bet — that they can occasionally find one. The wise ones bet heavily when the world offers them that opportunity. They bet big when they have the odds. And the rest of the time, they don't. It's just that simple."
> — Munger, *Poor Charlie's Almanack*, talk on "The Art of Stock Picking"

**How to apply:**

- The default action on any single research idea should be **do nothing**.
- Only when Stages 1–4 produce a clear positive Kelly edge with sound process and clean execution path should a position be opened.
- Aim for fewer than 10 active positions. If considering position #11, force a swap — which existing position has the weakest edge?

### Principle: Concentration through patience

> "You're paying less attention to Berkshire than most other people pay to their investments, and yet your results are better. We bought See's Candies and held it for 50 years. Most investment activity is its own enemy."
> — Munger, *Poor Charlie's Almanack* (paraphrased from multiple talks)

**How to apply:**

- A position's default holding period is "indefinite". Sell only if the original thesis is broken (hit a kill criterion) or a clearly superior opportunity exists.
- Trading frequency is inversely correlated with after-cost returns for retail investors (cf. Stage 4 spread costs).

### Principle: Inversion

> "Invert, always invert. Tell me where I'm going to die — that is, so I don't go there."
> — Munger, *Poor Charlie's Almanack* (Jacobi quoted)

**How to apply:**

- Before opening any position, write the failure obituary: "This position lost 50%. Why?"
- The most likely cause is the position's largest risk. Quantify it. If you cannot, do not size up.

### Stage 5 output

```
Current portfolio concentration: [X positions, top 3 = Y%]
This proposed position would be: [new #N / replacing existing #M]
Best alternative use of this capital: [next-best position by Kelly edge]
Failure obituary (1 paragraph): [...]
Decision: [PROCEED / PASS / SWAP for position M]
```

---

## Final — Research → Trade Checklist

Before any order is placed, every box must be ticked. If any box fails, return to that stage.

```
Research-to-Trade Gate:

Stage 0 — News & Synthesis
- [ ] 14-day news scan run, at least 3 sources covered
- [ ] Material catalysts that are not yet priced in listed
- [ ] Bull case written (200–400 words, no hedging)
- [ ] Bear case written (200–400 words, no hedging)
- [ ] Synthesis identifies stronger case and probability anchor

Stage 1 — Probability
- [ ] Reference class identified, base rate sourced
- [ ] Final probability stated as range with 80% CI
- [ ] No "feels likely" hand-waving
- [ ] Stage 0 synthesis used as inside view, reconciled with base rate

Stage 2 — Process
- [ ] Pre-mortem done
- [ ] Kill criterion written in advance
- [ ] Bear case steel-manned

Stage 3 — Sizing
- [ ] Kelly fraction computed from explicit p, b
- [ ] Size capped at quarter-Kelly (default) or half-Kelly (high-conviction only)
- [ ] Correlation haircut applied if other positions overlap
- [ ] Net edge > 0 (negative Kelly → abort)

Stage 4 — Execution
- [ ] No scheduled news in next 24h that would create adverse selection
- [ ] Spread + commission < 25 bps of position (or accept and note)
- [ ] Limit price set (or market order justified)

Stage 5 — Concentration
- [ ] Total active positions ≤ 10
- [ ] This is the best available use of this capital today
- [ ] Failure obituary written
```

If the user pushes to "just buy it" without the boxes ticked, refuse and surface which boxes are unchecked.

---

## Anti-patterns to flag immediately

Whenever the user or any other skill produces output matching these patterns, name the anti-pattern and the source:

| Anti-pattern | Source |
|---|---|
| Skipping the 14-day news scan because "I already know the story" | Stage 0 (this skill) |
| Writing a weak bear case for the sake of balance | Stage 0 (this skill) |
| Judging a decision by its outcome alone ("the trade worked, so it was right") | Duke, *Thinking in Bets* ch. 1 (Resulting) |
| Single-number forecasts ("AAPL will hit $250") | Tetlock, *Superforecasting* ch. 6 |
| Skipping the base rate | Tetlock, *Superforecasting* ch. 5 (Outside View) |
| Sizing above quarter-Kelly without explicit justification | Poundstone, *Fortune's Formula* ch. 14 |
| Limit order standing through a scheduled news event | Harris, *Trading and Exchanges* ch. 11 |
| Adding an 11th position without swapping one out | Munger, *Poor Charlie's Almanack* (concentration) |
| Treating a pattern in price data as signal without out-of-sample evidence | Silver, *Signal and the Noise* ch. 1 |
| Confidence stated without a kill criterion | Duke, *Thinking in Bets* ch. 2 |

---

## References

Full text of each book is in `references/`. Load only what you need; the files are large.

- `references/01-thorp-beat-the-market.md` — Thorp & Kassouf (1967). Kelly criterion derivation, warrant arbitrage.
- `references/02-poundstone-fortunes-formula.md` — Poundstone (2005). History and mathematics of Kelly, why fractional Kelly is sane.
- `references/03-tetlock-superforecasting.md` — Tetlock & Gardner (2015). Outside view, Brier scoring, growth mindset.
- `references/04-silver-signal-and-the-noise.md` — Silver (2012). Signal/noise discrimination, probabilistic thinking in messy domains.
- `references/05-duke-thinking-in-bets.md` — Duke (2018). Resulting, truth-seeking pods, separating process from outcome.
- `references/06-harris-trading-and-exchanges.md` — Harris (2003). Market microstructure, spread cost, adverse selection.
- `references/07-munger-poor-charlies-almanack.md` — Munger (2005). Concentration, inversion, multidisciplinary mental models.

When citing a principle in output, format as: `(Author, *Book*, ch./§ if known)`.
