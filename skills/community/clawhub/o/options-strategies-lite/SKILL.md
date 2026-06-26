---
name: Options Strategies Lite
slug: options-strategies-lite
version: 1.0.0
description: >
  Options strategy selector and plain-English guide to 5 core strategies. Tell me
  your market outlook and I'll point you to the right strategy. Covers covered calls,
  cash-secured puts, vertical spreads, iron condors, and LEAPS. Free version — upgrade
  for Greeks management, IV rank guidance, position sizing, and full adjustment playbooks.
author: OpenClaw Skills
tags: [options, trading, derivatives, income, spreads, free]
metadata:
  emoji: 🎯
  requires:
    tools: [web_search]
  os: [linux, darwin, win32]
---

# Options Strategies Lite

> *"Options are about probabilities, not predictions."*

**⚙️ Want Greeks management, IV rank guidance, and full adjustment playbooks?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## What This Skill Does

Helps you pick the right options strategy for your market outlook and explains exactly how each of the 5 most widely-used strategies works — in plain English, with P/L breakdowns.

**Included in Lite:**
- ✅ Strategy selector: Tell me bullish / bearish / neutral → get the right strategy
- ✅ Plain-English breakdown of 5 core strategies
- ✅ Max profit, max loss, and breakeven for each
- ✅ Honest "best for" and "avoid when" guidance

**Upgrade to Full for:**
- ❌ Greeks management (Delta, Theta, Vega — how to hedge and size)
- ❌ IV Rank guidance (when to buy vs. sell premium based on volatility environment)
- ❌ Position sizing rules (how much capital to risk per trade)
- ❌ DTE optimization (optimal days to expiration for each strategy)
- ❌ Real-world adjustment playbooks (what to do when a trade goes against you)
- ❌ Advanced strategies (butterflies, calendars, diagonals, jade lizards, BWBs)
- ❌ Exit criteria and take-profit rules

---

## Strategy Selector

Tell me your outlook and I'll point you to the right strategy:

### Bullish Outlook

| Your Situation | Strategy |
|---------------|---------|
| Strongly bullish, want leverage, defined risk | **Long Call** |
| Moderately bullish, want to reduce cost | **Bull Call Spread (Debit)** |
| Moderately bullish, prefer to collect premium | **Bull Put Spread (Credit)** |
| Happy to own the stock at a lower price | **Cash-Secured Put** |
| Already own the stock, neutral to slightly up | **Covered Call** |
| Want stock-like exposure with less capital | **LEAPS Call** |

### Bearish Outlook

| Your Situation | Strategy |
|---------------|---------|
| Strongly bearish, want leverage, defined risk | **Long Put** |
| Moderately bearish, reduce cost | **Bear Put Spread (Debit)** |
| Moderately bearish, collect premium | **Bear Call Spread (Credit)** |
| Own stock, want downside protection | **Protective Put** |

### Neutral / Range-Bound Outlook

| Your Situation | Strategy |
|---------------|---------|
| Stock going nowhere, want to profit from it | **Iron Condor** |
| Already own the stock, don't expect big moves | **Covered Call** |
| Expect low volatility, tight range | **Iron Butterfly** (full version) |

### Unknown Direction (Volatility Play)

| Your Situation | Strategy |
|---------------|---------|
| Big move expected, don't know which way | **Long Straddle** |
| Same but want cheaper entry | **Long Strangle** |

---

## The 5 Core Strategies — Plain English

---

### 1. Covered Call

**What it is:** You own 100 shares and sell someone the right to buy them from you at a higher price. They pay you premium upfront.

**The deal:** You cap your upside at the strike price, but collect income whether the stock goes up, stays flat, or drops a little.

**Example (stock at $100):**
- Sell 1 call at $110 strike, collect $2.50 premium
- Your income: $250 (received now, regardless of what happens)
- Max profit: $1,000 (stock appreciation from $100 to $110) + $250 premium = $1,250
- Max loss: You still own the stock — loss is whatever the stock falls minus the $250 cushion

| Metric | Value |
|--------|-------|
| Max Profit | (Strike - stock cost) + premium |
| Max Loss | Stock drops to zero (minus premium received) |
| Breakeven | Your purchase price minus premium |
| Upside | Capped at strike |

**Best for:** Income generation on stocks you already own. Neutral to mildly bullish outlook.
**Avoid when:** You think the stock is about to rip higher — you'll miss the gains.

---

### 2. Cash-Secured Put

**What it is:** You sell someone the right to sell their shares TO you at a specific price. You collect premium upfront and hold cash in reserve equal to the potential purchase price.

**The deal:** Either you keep the premium (stock stays above strike), or you end up buying the stock at the strike — at a discount to where it was when you sold the put.

**Example (stock at $100):**
- Sell 1 put at $95 strike, collect $3.00 premium
- Your income: $300 (received now)
- If stock stays above $95: keep the $300, trade done
- If stock drops to $90 at expiry: you buy 100 shares at $95 (your effective cost = $92 after premium)

| Metric | Value |
|--------|-------|
| Max Profit | Premium received |
| Max Loss | (Strike - premium) × 100 if stock goes to zero |
| Breakeven | Strike minus premium |
| Assignment | You buy the stock at the strike if it closes below |

**Best for:** Getting paid to potentially buy a stock you want to own anyway at a lower price.
**Avoid when:** You don't actually want to own the stock. Assignment is real — be prepared for it.

---

### 3. Vertical Spread (Bull Call Spread / Bear Put Spread)

**What it is:** You buy one option and sell another at a different strike (same expiry). The sold option reduces your cost but caps your max profit.

**Bull Call Spread Example (stock at $100, bullish):**
- Buy $100 call + Sell $110 call, same expiry
- Net cost: $3.50 (debit)
- Max profit: $10 wide spread minus $3.50 cost = **$6.50** per share ($650 per contract)
- Max loss: $3.50 per share ($350 per contract) — you can never lose more than what you paid

| Metric | Bull Call Spread | Bear Put Spread |
|--------|-----------------|-----------------|
| Cost | Debit (you pay) | Debit (you pay) |
| Max Profit | Spread width minus debit | Spread width minus debit |
| Max Loss | Debit paid | Debit paid |
| Breakeven | Lower strike + debit | Higher strike minus debit |

**Best for:** Directional trades when you want defined risk but don't want to pay full option premium.
**Advantage over long calls/puts:** Much cheaper. IV crush hurts less. Breakeven is lower.
**Trade-off:** You cap your gains. If the stock goes to $150, you still only profit to $110.

---

### 4. Iron Condor

**What it is:** You sell an OTM call spread AND an OTM put spread on the same stock, same expiry. You collect premium from both sides and profit if the stock stays in a range.

**Example (stock at $100):**
- Sell $115 call / Buy $120 call (bear call spread) = collect $1.00
- Sell $85 put / Buy $80 put (bull put spread) = collect $1.50
- Total credit: $2.50

- You profit if stock stays between $85 and $115 at expiry
- Max profit: $250 per contract (keep all premium)
- Max loss: $250 per side ($500 max on the losing spread, minus $250 credit = $250 net max loss)

| Metric | Value |
|--------|-------|
| Max Profit | Total credit received |
| Max Loss | Spread width minus total credit (per side) |
| Profit zone | Between your two short strikes |
| Breakevens | Short put strike minus credit AND short call strike plus credit |

**Best for:** Range-bound stocks during low-volatility or stable periods.
**Avoid when:** Big news or earnings are coming up. Binary events can blow past your wings.
**Key insight:** You don't need to predict direction — you just need the stock to stay in a range. That's why this is popular with income traders.

---

### 5. LEAPS (Long-Term Equity Anticipation Securities)

**What it is:** A call or put option with an expiration date 12-24 months away. Because of the long duration, these move almost like owning the stock — but at a fraction of the cost.

**Example (stock at $100, very bullish):**
- Buy 1 LEAPS call, $90 strike, 18 months out, for $18.00
- Cost: $1,800 (vs. $10,000 to buy 100 shares)
- If stock goes to $140 in 18 months:
  - Stock gain: $4,000 (40%)
  - LEAPS gain: ~$3,200+ (option moves from $18 to ~$50) = **~175%** return on the premium

| Metric | Value |
|--------|-------|
| Max Profit | Effectively unlimited (stock moves a lot in your favor) |
| Max Loss | Premium paid (you can lose 100% if you're wrong) |
| Breakeven | Strike + premium paid |
| Leverage | ~5-7× leverage vs. owning stock outright |

**Best for:** Strong multi-month conviction plays. Capital-efficient alternative to buying 100 shares.
**Avoid when:** You need the stock to move quickly — LEAPS give you time, but you're paying for it.
**Key risk:** If the stock doesn't move much, time decay still erodes value — just slowly.

---

## Quick Vocabulary

| Term | Plain English |
|------|--------------|
| Call option | Right to BUY shares at the strike price |
| Put option | Right to SELL shares at the strike price |
| Strike price | The locked-in price in the contract |
| Premium | What you pay (or collect) for the option |
| Expiration | When the option contract ends |
| In-the-money (ITM) | Option has intrinsic value right now |
| Out-of-the-money (OTM) | Option would not be profitable if expired today |
| Assignment | Being forced to buy/sell stock because your option was exercised |
| DTE | Days to expiration |

---

## Where the Lite Version Ends

You now know how to pick a strategy and what the basic mechanics are for the 5 most important strategies in options trading.

**What you won't get here:**
- **Greeks**: How to read Delta (directional exposure), Theta (time decay per day), Vega (sensitivity to volatility changes) — essential for managing positions
- **IV Rank guidance**: The single most important factor in whether to buy or sell premium. High IV = sell premium. Low IV = buy premium. The full version scores this for you.
- **Position sizing**: How much capital to risk per trade (and why most people risk too much on undefined-risk strategies)
- **DTE optimization**: Each strategy has an optimal entry and exit window — entering too early or too late kills returns
- **Adjustment playbooks**: What to actually do when an iron condor gets tested, or a covered call goes deep ITM
- **Advanced strategies**: Calendars, diagonals, butterflies, the jade lizard, broken wing butterfly

Options edge lives in the details. The full version covers all of it.

**⚙️ Want Greeks management, IV rank guidance, and full adjustment playbooks?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## Example Queries

- `"I'm bullish on AAPL — what's the best options strategy?"`
- `"Explain how a covered call works in plain English"`
- `"What's an iron condor and when should I use it?"`
- `"I want to own MSFT at a lower price — what should I do?"`
- `"What's the difference between a covered call and a cash-secured put?"`
- `"I think TSLA is going to move big but I don't know which way"`

---

*Options trading involves significant risk and is not suitable for all investors. This is educational content only — not investment advice. Always understand the full risk of a strategy before trading.*
