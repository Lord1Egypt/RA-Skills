---
name: price-compare
description: Compare product prices across major US e-commerce platforms. Triggers when the user asks "what's the best price for X", "compare prices", "where to buy [product] cheapest", "price check", "is [product] cheaper on Amazon or Walmart", or any variation asking for price comparison or shopping recommendations. Targets US shoppers and searches Amazon, Walmart, Target, Best Buy, eBay, Temu, Google Shopping, Costco, and Kroger.
metadata: {"openclaw": {"emoji": "🏷️", "homepage": "https://clawhub.ai/skills/price-compare"}}
---

# Price Compare

Compare prices for any product across major US retailers, with pros/cons, trust scores, and buy recommendations.

> **Pattern: Inversion + Pipeline + Reviewer**
> This skill uses structured questions before searching (Inversion), a multi-step workflow with gates (Pipeline), and a price trust scoring system (Reviewer). Follow the phases in order — do not skip ahead.

---

## Phase 1 — Pre-Search: Gather Requirements (Inversion)

**DO NOT start searching until you have answered the questions below.**

### Required (ask if not clear from the prompt)

- **Product**: What exactly do they want? (brand, model, size/quantity if relevant)
- **Budget**: Is there a max price? (filters results before showing)
- **Context**: Indoor or outdoor use? New or refurbished acceptable? (avoids irrelevant results)

### Ask only if relevant

- **Timeline**: Need it today/this week, or can wait 2-3 weeks?
- **Used/refurb OK?**: If asking about electronics, clarify new vs. refurbished preference
- **Specific retailers?**: Any retailer they want to avoid or prefer?

**If the user gives enough context** (e.g., "best price for Sony WH-1000XM5 under $300"), skip redundant questions and move to Phase 2.

---

## Phase 2 — Execute Search (Pipeline)

### Step 1 — Search All Platforms in Parallel

Try `web_search` first. Run all calls simultaneously:

```
web_search(query="site:amazon.com {product}", count=5)
web_search(query="site:walmart.com {product}", count=5)
web_search(query="site:target.com {product}", count=5)
web_search(query="site:bestbuy.com {product}", count=5)
web_search(query="site:ebay.com {product}", count=5)
web_search(query="site:temu.com {product}", count=5)
web_search(query="site:costco.com {product}", count=5)
web_search(query="{product} price comparison site:google.com/shopping", count=5)
```

### Step 1 Fallback — When web_search fails

If `web_search` returns errors (403/429/503) or empty results, use the browser instead:

```
browser(action="navigate", url="https://www.google.com/search?q={product}+price+site:amazon.com+OR+site:walmart.com+OR+site:target.com&num=10", profile="openclaw")
browser(action="snapshot", profile="openclaw")  // extract prices from results
```

If browser also fails, fall back to a single `web_fetch` on Google Shopping:
```
web_fetch(url="https://www.google.com/shopping?q={product}&hl=en", maxChars=10000)
```

### Step 2 — Fetch Top Results (with Browser Fallback)

For each platform that returned results, attempt `web_fetch`:

**URL patterns:**
- Amazon: `https://www.amazon.com/s?k={product}&s=price-asc-rank`
- Walmart: `https://www.walmart.com/search?q={product}`
- Target: `https://www.target.com/s?searchTerm={product}`
- Best Buy: `https://www.bestbuy.com/site/searchpage.phtml?st={product}`
- eBay: `https://www.ebay.com/sch/i.html?_nkw={product}&_sop=15`
- Temu: `https://www.temu.com/search_result.html?search_key={product}`
- Costco: `https://www.costco.com/search?search={product}`
- Google Shopping: `https://www.google.com/shopping?q={product}&hl=en`

**Browser fallback for JS-rendered pages:**
If `web_fetch` returns a bot-check page or empty content for Amazon/Walmart/Target/Temu:

```
browser(action="navigate", url="<platform URL>", profile="openclaw")
browser(action="act", kind="evaluate", fn="() => { const items = document.querySelectorAll('[data-component-type=\"s-search-result\"]'); return Array.from(items).slice(0,5).map(i => ({ title: i.innerText.substring(0,100), price: i.querySelector('.a-price .a-offscreen, [class*=\"price\"]')?.innerText || 'N/A' })).slice(0,5); }")
```

### Step 3 — Load References

Always load these reference files:
```
read(path="{skill_dir}/references/platforms.md")
read(path="{skill_dir}/references/trust-checklist.md")
```

---

## Phase 3 — Price Trust Scoring (Reviewer)

Apply the trust score from `trust-checklist.md` to every price result. Flag suspicious prices before presenting.

### Trust Score Criteria (Reviewer Pattern)

For each platform result, score:

| Signal | Score | Meaning |
|--------|-------|---------|
| Official store / first-party seller | ✅ +2 | Authentic, full warranty |
| 4.5+ stars, 500+ reviews | ✅ +1 | Popular, likely real |
| Price history shown (Google Shopping) | ✅ +1 | Can verify if it's a good deal |
| "was $X, now $Y" with X > 30% above market | ⚠️ -2 | Fake discount — X was never real |
| No reviews / <10 reviews | ⚠️ -1 | Hard to verify quality |
| Temu unbranded generic | ⚠️ -1 | Quality not assured |
| Used/refurbished | ℹ️ ±0 | Normal risk, acceptable if disclosed |
| eBay seller <95% rating | ⚠️ -2 | High return/defect risk |
| "Only 2 left!" / countdown timers | 🚩 -1 | Dark pattern, ignore |
| Price < 30% of average market | 🚩 -3 | Almost certainly fake/knockoff |

### Trust Score Totals

- **+3 to +5**: 🟢 Reliable — show prominently
- **+1 to +2**: 🟡 Acceptable — show with note
- **0 to -1**: 🟠 Caution — show only if user OK with risk
- **-2 or below**: 🔴 Suspicious — skip or warn explicitly

---

## Phase 4 — Price Anomaly Gate (Pipeline)

Before presenting results, check for anomalies:

**Gate: If any result is >50% below market average**
→ Flag as "⚠️ Suspicious cheap — likely fake/counterfeit. Verify before buying."

**Gate: If Temu price is <30% of branded alternatives**
→ Add warning: "Temu's low price suggests unbranded/knockoff quality. Compare photos with official listing."

**Gate: If price has moved >20% in 30 days** (from Google Shopping)
→ Note: "↗ Price up X% in 30 days — not the best time" OR "↓ Price down X% — good time to buy"

**Gate: If web_search AND browser both failed for a platform**
→ Do NOT fabricate prices. Mark that platform as "❌ Data unavailable — results may be incomplete."

---

## Phase 5 — Output (Generator)

Use this structure every time:

### 📦 [Product Name]

**Quick summary:** [1 sentence: best pick + price range]

**Trust-scored comparison:**

| Platform | Price | Ship | Rating | Trust | Verdict |
|---------|-------|------|--------|-------|---------|
| ... | ... | ... | ... | 🟢/🟡/🟠/🔴 | ... |

**Recommended:**

🥇 **Best overall:** [Platform] — $XX — [1 sentence why]
🥈 **Runner-up:** [Platform] — $XX — [1 sentence why]
♻️ **Best used/refurb:** [Platform] — $XX — [1 sentence why]
💸 **Budget pick:** [Platform] — $XX — [1 sentence why]

**⚠️ Warnings & gotchas:**
- [Any trust score issues, fake discounts, shipping gotchas]

**📈 Price trend:**
- [From Google Shopping: "↓ Good time — down 20% from 90-day average" OR "↗ Rising — up 15% in 30 days"]

**🔗 Direct links:**
- [Amazon](url) · [Walmart](url) · [Target](url) · [Best Buy](url) · [eBay](url) · [Temu](url)

---

## Output Examples

### Example — Basketball
```
### 📦 Wilson NBA Official Game Ball (Size 7)

**Quick summary:** Best authentic option is DICK'S at $219.99 (11% off); cheapest decent ball is Walmart's Wilson Prestige at $15.94 for outdoor use.

| Platform | Price | Ship | Rating | Trust | Verdict |
|---------|-------|------|--------|-------|---------|
| DICK'S | $219.99 | Free | ⭐ 4.7 (129) | 🟢 | 🔥 Best Price + ⭐ Best Value — 11% off, 90-day returns |
| Wilson.com | $219.95 | Free ($50+) | ⭐ 4.5 (64) | 🟢 | ⚡ Fastest — direct from manufacturer |
| Scheels | $219.95 | — | — | 🟡 | Same price, reliable retailer |
| NBA Store | $249.99 | Free ($50+) | ⭐ 4.6 | 🟢 | ❌ Overpriced — avoid |
| eBay | $190.00 | +$7.95 | varies | 🟠 | ♻️ Bulk deal — verify seller rating 98%+ first |

**⚠️ Warnings & gotchas:**
- The official Wilson game ball is **genuine leather — for indoor use only**. New it is slippery; needs 2-3 weeks of break-in.
- eBay at $190 is suspicious for new — verify authenticity before buying.
- Temu had no relevant results (mostly unbranded generic balls under $10 — 🔴 low quality risk).

**📈 Price trend:** → Stable — typically $220, within normal range for 90 days.

**Recommended:**
🥇 **Best overall:** DICK'S Sporting Goods — $219.99 — matches all-time low, free shipping, 90-day returns.
🥈 **Runner-up:** Wilson.com — $219.95 — direct from maker, 30-day returns.
💸 **Budget outdoor:** Walmart — Wilson Prestige Outdoor — $15.94, pickup today.
```

---

## Quick Rules

- **Trust score every result** before showing it. Never present a 🔴 price without a warning.
- **Always show total cost** (price + shipping). A "cheaper" item with $20 shipping may cost more.
- **Parallelize all searches** — never run them sequentially unless using fallback.
- **Flag fake discounts.** "Was $X" where X was never actually sold = -2 trust score.
- **No fabricated prices.** If a platform's data is unavailable, say so.
- **Direct links in every response.** Users need to be able to click and buy.
- **Platforms:** Amazon, Walmart, Target, Best Buy, eBay, Temu, Costco, Google Shopping. Add Kroger for groceries.
