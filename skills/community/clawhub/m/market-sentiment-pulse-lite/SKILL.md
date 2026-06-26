---
name: Market Sentiment Pulse Lite
slug: market-sentiment-pulse-lite
version: 1.0.0
description: >
  Quick sentiment check for any stock, crypto, or index. Delivers a bullish/bearish/
  neutral score, a 3-5 headline summary, and a basic fear/greed read in minutes.
  Free version — upgrade for deep multi-source aggregation, contrarian signals,
  social volume analysis, and institutional positioning data.
author: OpenClaw Skills
tags: [trading, sentiment, stocks, crypto, news, free]
metadata:
  emoji: 📡
  requires:
    tools: [web_search, web_fetch]
  os: [linux, darwin, win32]
---

# Market Sentiment Pulse Lite

> *"The market is a voting machine in the short run and a weighing machine in the long run."* — Benjamin Graham

**🔍 Want deep multi-source sentiment with contrarian signals?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## What This Skill Does

A fast gut-check on market sentiment for any ticker before you make a move. Get a sentiment score, the headlines driving the narrative, and a read on whether the crowd is fearful or greedy.

**Included in Lite:**
- ✅ Quick sentiment score: Bullish / Bearish / Neutral (with +/- rating)
- ✅ 3-5 headline summary (what's moving the narrative right now)
- ✅ Basic fear/greed read (is the crowd at an extreme?)
- ✅ Analyst consensus direction (upgrades vs. downgrades trend)

**Upgrade to Full for:**
- ❌ Scored composite Pulse (-100 to +100) with weighted sub-dimensions
- ❌ Social volume analysis (Reddit, Twitter/X mention trends vs. baseline)
- ❌ Options flow signals (put/call ratio, unusual activity, IV rank)
- ❌ Contrarian signal detection (when to fade the crowd)
- ❌ Institutional positioning data
- ❌ Historical sentiment comparison (is this extreme by historical standards?)
- ❌ Pre-earnings whisper number check
- ❌ Multi-ticker sentiment comparison tables

---

## Workflow

### Step 1: Identify the Ticker

Parse the asset from user input:
- `$AAPL`, `AAPL`, `Apple` → `AAPL`
- `BTC`, `Bitcoin`, `$BTC` → `BTC`
- `SPY`, `S&P 500`, `the market` → `SPY`

Confirm the ticker before proceeding if ambiguous.

---

### Step 2: Gather Signals

Run these searches:

```
"[TICKER] news today"
"[TICKER] analyst upgrade downgrade this week"
"[TICKER] [company name] earnings guidance outlook"
"[TICKER] sentiment bullish bearish"
```

**Focus on the last 48-72 hours.** Flag anything older.

---

### Step 3: Score the Sentiment

Assess across three dimensions and combine into an overall read:

#### News Tone (most important)

| Score | What You're Seeing |
|-------|-------------------|
| 🔥 Strongly Bullish | Blowout earnings, major positive catalyst, takeover bid, analyst upgrades |
| 📈 Mildly Bullish | Beat estimates, positive guidance, favorable news flow |
| ⚖️ Neutral | In-line results, mixed news, no clear direction |
| 📉 Mildly Bearish | Missed estimates, soft guidance, competitive headwinds |
| ❄️ Strongly Bearish | Major miss, regulatory action, fraud allegations, guidance cut |

#### Crowd Temperature

Read from the headlines and any social signals you find:
- **Euphoric**: Viral excitement, FOMO language, everyone talking about it
- **Optimistic**: Positive but measured, steady buying interest
- **Neutral**: Quiet, no strong directional chatter
- **Nervous**: Cautious, worry in headlines, selling into strength
- **Fearful**: Panic language, capitulation signals, "how low can it go" framing

#### Analyst Activity (directional trend)

- More upgrades than downgrades in last 30 days? → Positive
- Price target raises? → Positive
- Estimate cuts? → Negative
- Downgrades accumulating? → Negative

---

### Step 4: Headline Summary

Pull the **3-5 most important stories** driving current sentiment. For each:
- The key fact or event
- Whether it's bullish 📈, bearish 📉, or mixed ⚖️
- How fresh it is (breaking / last 7 days / established)

---

### Step 5: Fear/Greed Check

Simple but important: **Is the crowd at an extreme?**

- **Extreme Greed signals**: Unanimous bullishness, "can't go wrong" framing, everyone piling in
- **Extreme Fear signals**: "It's over" language, capitulation, people swearing off the stock/asset

**Why this matters**: Extremes are often contrarian signals. The full version scores and tracks these systematically — here, use your judgment based on what the headlines and chatter show.

---

## Output Format

```markdown
# 📡 Sentiment Pulse: $[TICKER] — [Company Name]
**As of:** [Date]
**Data window:** Last 48-72 hours

---

## Overall Sentiment: [BULLISH / BEARISH / NEUTRAL] [📈/📉/⚖️]

[One sentence capturing the dominant narrative right now]

---

## Signal Read

| Dimension | Read | Notes |
|-----------|------|-------|
| 📰 News Tone | [🔥/📈/⚖️/📉/❄️] | [Top headline driver] |
| 🌡️ Crowd Temperature | [Euphoric/Optimistic/Neutral/Nervous/Fearful] | [Brief description] |
| 🏦 Analyst Activity | [Positive/Mixed/Negative] | [Upgrades vs. downgrades trend] |

---

## Key Headlines (Last 48-72h)

1. **[Headline]** — [📈/📉/⚖️]
   [1-2 sentences on why this matters and what it means]

2. **[Headline]** — [📈/📉/⚖️]
   [1-2 sentences]

3. **[Headline]** — [📈/📉/⚖️]
   [1-2 sentences]

[4th and 5th if relevant]

---

## Fear/Greed Check

[1-2 sentences: Is the crowd at a sentiment extreme? Is this a "everyone loves it" or
"everyone hates it" moment? Any contrarian signal worth noting?]

---

## Quick Trading Frame

**If you're bullish:** [What sentiment says — is it a tailwind or are you fighting momentum?]
**If you're bearish:** [Is there fear you can exploit, or is sentiment too strong to fight?]
**Watch for:** [The one catalyst or signal that would change this read]

---
*⚠️ Lite sentiment check — headlines and crowd temperature only.*
*For scored multi-source Pulse, contrarian signals, and options flow:*
*Full version → agentofalpha.com*
```

---

## Where the Lite Version Ends

This gives you a fast, useful read on what's happening in sentiment right now. You'll know if the narrative is positive or negative, what the key stories are, and whether the crowd is at an extreme worth noting.

**What you won't get here:**
- A scored composite Pulse from -100 (Max Fear) to +100 (Max Greed)
- Social volume data — is chatter rising or falling vs. baseline?
- Options market signals — is smart money buying puts or calls?
- Systematic contrarian detection — when exactly is crowd sentiment too extreme to trust?
- Institutional positioning (are funds accumulating or distributing?)
- Historical context — is today's sentiment extreme by 1-year or 5-year standards?
- Side-by-side sentiment comparison across multiple tickers

Sentiment is one of the highest-edge signals available if you can measure it rigorously. The full version does exactly that.

**🔍 Want deep multi-source sentiment with contrarian signals?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## Example Queries

- `"Quick sentiment check on TSLA"`
- `"What's the vibe on Bitcoin right now?"`
- `"Is NVDA sentiment bullish or bearish heading into earnings?"`
- `"Sentiment pulse on the market today"`
- `"Any extreme fear or greed I should know about on META?"`

---

*Sentiment is a short-term signal — hours to days. Always combine with technical and fundamental analysis. Not investment advice.*
