---
name: market-brief
description: "Produce a decision-useful market brief on any token, sector, or macro question. Format is consistent and structured — drivers, scenarios, uncertainty, practical read. Triggers: 'market brief on X', 'analyze Y', 'what's the call on Z', 'price target for', 'swing trade thesis', 'how should I think about'. Skip for simple price lookups or factual questions."
metadata:
  emoji: "📊"
  pattern_key: "market-brief"
  first_authored: "2026-07-04"
---

# Market Brief

Consistent, decision-useful market analysis for crypto, equities, FX, or macro topics. Avoids shallow takes; emphasizes drivers, scenarios, uncertainty, and practical reads.

## When to use

- ✅ Token / asset price analysis (swing trade or position sizing)
- ✅ Sector thesis (DeFi, L1s, RWA, fintech, etc.)
- ✅ Macro / rate / liquidity calls
- ✅ Project / protocol due diligence with a market angle
- ❌ Simple factual price lookup — just answer it
- ❌ Pure research without a market view — use `researcher` instead

## Required output shape

Every brief follows this exact structure. Don't skip sections.

1. **TL;DR** (1–3 lines)
   - The actual call / position / view in plain language
   - Conviction: high | medium | low
   - Time horizon: days / weeks / months

2. **Current state** (≤5 lines)
   - Price / level
   - Recent action (last 1–4 weeks)
   - Key on-chain or fundamental signals
   - Cite sources inline (URL or source name)

3. **Drivers** (bullets)
   - What's actually moving the asset
   - Catalysts with rough timing
   - Distinguish confirmed vs rumored

4. **Scenarios** (table or structured bullets)

   | Scenario | Drivers | Target $ | Probability |
   |---|---|---|---|
   | Bull | ... | ... | ... |
   | Base | ... | ... | ... |
   | Bear | ... | ... | ... |

5. **Key uncertainty** (≤3 bullets)
   - What would invalidate the call
   - What info would change the view
   - Tail risks not in the base case

6. **Practical read** (1–3 lines)
   - What Daniel should actually do with this
   - Position sizing suggestion if relevant
   - Entry/exit triggers

## Rules

- **Distinguish verified vs inferred** — separate what you confirmed from what you're guessing
- **No "could maybe possibly" hedging** — state the call, then qualify
- **Cite sources** for load-bearing claims (URL or named source)
- **Use real numbers** — specific price targets beat vague ranges
- **Always include time horizon** — different horizons change the call
- **Admit when you don't have enough info** — say so explicitly
- **Don't manufacture confidence** — if uncertainty is high, mark conviction low

## Length

- Default: 250–400 words
- Deep-dive mode (when asked): 600–1000 words
- Always start with TL;DR — never bury the call

## After the brief

If asked, follow up with:
- On-chain data check
- Funding rates / open interest
- Recent news flow
- Comparable asset analysis

---

<!-- Real-world refinements get appended below -->