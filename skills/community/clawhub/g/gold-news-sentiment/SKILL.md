---
name: gold-news-sentiment
description: Use this skill when users want to pull recent global gold-related news, assess short-term or medium-term market sentiment for gold, connect macro drivers like Fed policy, US yields, USD, inflation, geopolitics, and ETF flows to gold, and produce a structured conclusion such as 看涨, 看跌, or 观望 with confidence and risks.
---

# gold-news-sentiment

Use this skill to turn recent gold-related news into a structured market sentiment read.

The default job is not to produce a trading call from vibes. The default job is to:

- gather recent gold-relevant news
- reuse a fresh cached snapshot when available
- separate signal from repeated headlines and noise
- connect the news to macro drivers that usually matter for gold
- output a disciplined conclusion with uncertainty and risk notes

## When To Use

Use this skill when the user wants to:

- get a current gold market sentiment snapshot
- understand whether recent news is net bullish or bearish for gold
- classify the environment as `看涨`, `看跌`, or `观望`
- summarize the main drivers behind gold price moves
- run a recurring workflow that tracks gold-related sentiment over time

## Core Rules

1. Treat the output as analysis support, not investment advice.
2. Prefer high-credibility and recent sources over volume.
3. Do not let repeated headlines count as multiple independent signals.
4. Separate `news sentiment` from `price trend`. They often diverge.
5. Always state uncertainty, key assumptions, and what could invalidate the conclusion.

## Workflow

### 1. Check for a fresh cached snapshot

Before doing a fresh pull, check whether these files already exist:

- `data/latest_sentiment.md`
- `data/latest_digest.md`
- `data/latest_news.json`

If `data/latest_sentiment.md` is fresh enough for the user's need, use it first so the user gets an immediate answer. Default freshness window:

- interactive use: 6 hours
- slower-moving medium-term questions: up to 24 hours if the user accepts it

If the cache is stale, missing, or the user explicitly asks for a refresh, continue with a fresh pull.

For the recurring workflow, read [references/automation-template.md](references/automation-template.md).

### 2. Pull recent news

Run the bundled script from the skill directory:

```bash
python3 scripts/fetch_news.py --hours 48 --limit 40
```

Use `--query` when the user wants a narrower theme such as:

- central bank buying
- Fed rate cuts
- geopolitics
- ETF flows
- inflation

The script outputs normalized JSON with:

- title
- source
- published time
- link
- query bucket
- provider
- detected tags

For source coverage and caveats, read [references/source-list.md](references/source-list.md).

For cached fast-path updates, prefer:

```bash
python3 scripts/update_snapshot.py --hours 48 --limit 50
```

This refreshes:

- `data/latest_news.json`
- `data/latest_digest.md`

The automation can then write:

- `data/latest_sentiment.md`

### 3. Remove weak signals

Before analysis:

- deduplicate near-identical headlines
- down-weight aggregator rewrites
- discard clearly stale items if newer reports supersede them
- flag articles that mention gold only in passing

If the fetch step returns zero usable items or includes request failures, do not fabricate a sentiment conclusion. Report that retrieval failed or that the evidence is insufficient, then stop or ask for a narrower rerun.

If more detail is needed, read [references/scoring-rules.md](references/scoring-rules.md).

### 4. Classify each item

Classify each article into one of:

- `bullish_for_gold`
- `bearish_for_gold`
- `mixed_or_unclear`
- `background_only`

Then note the driver category:

- Fed / rates
- US real yields
- USD
- inflation
- labor / growth slowdown
- geopolitics / risk-off
- central bank demand
- ETF / investor flows
- physical demand / supply

Do not force a directional label when the causal chain is weak.

### 5. Aggregate into a market read

Build the conclusion in this order:

1. short-term news balance
2. macro driver alignment or conflict
3. whether price-sensitive drivers are pointing the same way
4. remaining uncertainty

Default horizon:

- `短线`: next few sessions to two weeks
- `中线`: next one to three months

If the user does not specify a horizon, provide both.

### 6. Produce the final output

Use this structure unless the user asks for another format:

```markdown
结论：观望

情绪方向：
- 短线：偏多
- 中线：中性

置信度：中

核心驱动：
- <driver 1>
- <driver 2>
- <driver 3>

主要新闻：
1. <headline summary + why it matters>
2. <headline summary + why it matters>
3. <headline summary + why it matters>

为什么不是明确看涨/看跌：
- <reason>

风险提示：
- <risk 1>
- <risk 2>
```

## Output Discipline

- A `看涨` conclusion requires multiple aligned bullish drivers, not one dramatic headline.
- A `看跌` conclusion requires multiple aligned bearish drivers, not just temporary USD strength.
- Use `观望` when the main drivers conflict or the incoming news is too noisy.
- Prefer `偏多` or `偏空` in the explanation even when the final top-line conclusion is `观望`.

## Validation Checks

Before answering, verify:

- at least one high-credibility source is represented
- the timeframe is explicit
- bullish and bearish evidence were both considered
- the conclusion matches the balance of evidence
- the fetch result was non-empty and did not fail silently

## Automation Guidance

For recurring runs, the automation prompt should ask for:

- one fresh gold sentiment update
- explicit `看涨 / 看跌 / 观望` conclusion
- supporting drivers and risks
- links to the most relevant recent items

When `data/latest_sentiment.md` exists and is fresh, answer from it first unless the user asks for a real-time refresh.

Avoid claiming certainty. If the signal is mixed, say so.
