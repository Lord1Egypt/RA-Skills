# Gift Cards — Decay Law, Bankruptcy, and Resale Economics

## 1. The scale of the problem
- CEB TowerGroup / NRF-family estimates: Americans buy $130–190 billion in gift cards per year; roughly 1–3% ($2–4 B/yr) goes unredeemed, and the cumulative pile of dormant money is estimated at $15–23 billion.
- Average household holds $150–200 in cards; a meaningful share is for stores the holder never visits.
- Gift cards are the #1 requested holiday gift in the US every year — the inflow is structural, so the leakage is too.

## 2. US federal floor: CARD Act 2009 (Credit CARD Act, gift-card provisions)
| Rule | Detail |
|---|---|
| Validity floor | Funds usable ≥ **5 years** from issuance or last reload/activity |
| Inactivity fees | Prohibited in the first **12 months** of inactivity; after that ≤1/month, must be disclosed on the card |
| Fee disclosure | Terms must be printed on the card/packaging |
| Preempted state law | States may be *more* generous (e.g., no fees at all in several states; some ban expiry entirely) |
What the floor does NOT do: keep the retailer solvent, protect resale value, or stop **state escheat/unclaimed-property** intake after the state's dormancy period (commonly 3–5 years of no activity). Claim back at the state's unclaimed-property site (missingmoney.com aggregates most).

## 3. Bankruptcy mechanics for cardholders
- In Chapter 11, accepting gift cards post-piling requires court permission; chains commonly announce a "we still accept gift cards" window of days to a few weeks, then stop.
- In Chapter 7 / liquidation, cards are effectively dead; you can file a proof of claim with the bankruptcy court, priority: unsecured. Recovery historically $0–25¢/$1, often $0.
- Historical pattern (casual dining and home-goods chains, 2016–2024): headlines about missed vendor payments or "exploring strategic alternatives" precede filings by weeks — that's your sell/spend window.
- Practical doctrine: **distress news = spend week.** Essentials first; if you truly can't use it, buy a resale-durable item (tools, small electronics) and sell it privately.

## 4. Resale economics
- Exchanges buy at 60–92% of face: big-box home improvement/electronics/warehouse clubs top; restaurants mid (60–80%); fashion/niche low.
- Exchanges sell at 5–15% discount — the spread is the business. For a seller, comparing two exchanges on the same brand routinely finds a 10–15 point difference.
- Physical-card kiosks (grocery/coin-star family) pay less (~50–70%) but are instant.
- Raise/CardCash-style marketplaces: verify payout terms (check vs ACH), buyer-protection, and the brand's transfer policy before listing.
- Rule of thumb: if resale ≥ 70% and you won't use the card within 3 months, selling is usually the better expected value than "someday" spending — because of bankruptcy tail-risk alone.

## 5. Escheat (unclaimed property) — the invisible one
- After the state's dormancy period (typically 3–5 years), the retailer hands balances to the state as unclaimed property. The money isn't gone — you reclaim it from the state — but you must know to look.
- Any card activity (purchase or balance check at the register in some states) restarts clocks; buying a $1 item is the cheapest insurance.
- Check: your state treasurer's unclaimed-property database + missingmoney.com (NAAG-backed aggregator). Old addresses and maiden names are where money hides.

## 6. Security and fraud (condensed)
- Balance checks: only by typing the retailer's URL yourself. Fake "check your balance" sites harvest card+PIN pairs in bulk and drain them within minutes.
- Refund/OTA/AI-voice scams increasingly demand payment in gift cards: **no legitimate business or agency asks for gift cards.** Treat that request as the scam signature itself.
- Registry hygiene: store last-4 + balance, keep full numbers in the retailer's app (which is also the recovery path if the plastic is lost).

## 7. Outside the US (brief)
- EU: several member states mandate minimum validity (often 2+ years after purchase); expiry terms must be clear, else unenforceable.
- UK: gift cards can expire only if clearly communicated at purchase; typical 12–24-month terms from major chains.
- Canada: expiry bans federally (2008 gift-card rules) for most retail cards; fees tightly restricted.
The skill's registry math is jurisdiction-neutral; verdicts cite US rules by default — swap in local floors when advising non-US users.

## 8. Sources & caveats
- CARD Act 2009 gift-card provisions (15 U.S.C. §1693l-2); state unclaimed-property acts; CFPB gift-card guidance; bankruptcy claims process (US Courts proof-of-claim).
- Dollar figures are industry estimates that vary by year and methodology — used for magnitude, not precision.
- Resale percentages drift with market conditions; the script takes `--offer-pct` as live input rather than hardcoding a stale spread.
