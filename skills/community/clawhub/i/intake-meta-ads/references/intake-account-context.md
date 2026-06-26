# Intake Breathing — META Account Context

## Account Identity

| Field | Value |
|---|---|
| Brand | Intake Breathing |
| Product | Nasal dilator / nasal strips (magnetic technology) |
| Positioning | "Life Changing Breathing" |
| Archetype | Hero (peer brands: Nike, Adidas, Eightsleep, BMW) |
| Ad Account ID | `act_2335535636459862` |
| Developer App | "Intake Ads Reporting" |
| Business Email | maxwellcwaggoner@gmail.com |
| Account Manager | Max Waggoner — maxwaggoner@growthset.ai (GrowthSet) |
| Spend Level | ~$1M+/month |

---

## Brand Reference

- **Primary colors:** Black #000000, White #FFFFFF
- **Accent colors:** Electric Green #00FEA9, Slate Blue #63B7BA
- **Font:** Inter (Google Fonts)
- **Key personas:**
  - Sporty Steve (athlete)
  - Helpful Heather (fitness instructor)
  - Peak Performer Paul (entrepreneur)

---

## Historical CPA Benchmarks

| Period | CPA | Notes |
|---|---|---|
| Jan–Feb 15, 2026 | ~$67 | Pre-inflection baseline — the target to return to |
| Feb 16–Mar 2026 | ~$88–96 | Post-inflection, new (worse) normal |
| Last 4 weeks (as of Apr 7, 2026) | ~$87–96 blended purchase CPA | Still elevated |
| Account average (Apr 2026) | ~$112.93 | Includes lead actions; pure purchase CPA ~$87–96 |

**The Feb 16, 2026 inflection point is the key event in this account.** CPA jumped cleanly from ~$67 to ~$88+ that week and has never recovered. Root cause: an offer structure change by the Intake team on or around Feb 16. All platforms and demographics declined simultaneously — ruling out platform, creative, or targeting causes.

---

## Campaign Structure & Naming Conventions

Campaign prefixes:
- **RG** = Revenue Generation (prospecting)
- **LSG** = Lower Sales Generation (retargeting / MOFU)

Campaign types seen in account:
- **ASC** = Advantage+ Shopping Campaign (automated)
- **Manual** = Manual targeting campaigns
- **Gender Split** = Campaigns split by gender targeting
- **EVG** = Evergreen

---

## Campaign Efficiency (Last 30 Days — as of April 7, 2026)

| Campaign | Spend | Purchases | CPA | Notes |
|---|---|---|---|---|
| Sale Test – CGH | $33K | 926 | **$35.64** | OUTLIER — investigate offer structure |
| RG Prospecting ASC Creative Testing | $147K | 1,866 | $78.76 | Most efficient at scale |
| RG Prospecting Manual (Mouth Tape) | $16K | 209 | $77.63 | Small budget, efficient |
| RG Prospecting EVG Manual Sales | $404K | 4,745 | $85.16 | Largest budget, not best CPA |
| RG Gender Split ASC | $188K | 2,121 | $88.54 | — |
| LSG Prospecting Manual Gender Split | $174K | 1,906 | $91.27 | — |
| LSG Retargeting MOFU | $85K | 931 | $91.31 | — |
| LSG Wellness ASC+ | $62K | 660 | $94.49 | — |

**Key insight:** RG Prospecting EVG Manual Sales has $404K (31% of total spend) but delivers $85.16 CPA. ASC Creative Testing delivers $78.76 on $147K. Budget should shift toward ASC.

---

## Top Ads by Purchases (Last 30 Days — as of April 7, 2026)

| Ad | Purchases | CPA | CTR | Notes |
|---|---|---|---|---|
| Internal UGC \| Level Up Breathing — @maknificient | 1,851 | $78.91 | 1.63% | Volume leader |
| UGC \| @drew.tts — March Level Up Video V1 | 1,252 | $75.40 | 2.25% | Strong CTR + CPA |
| Sleep-Snoring UGC — @lauren_sah_girlmama | 847 | $73.65 | 2.33% | Best CTR among top 3 |
| New Sales Ad | 594 | **$35.16** | 1.14% | Outlier CPA — tied to Sale Test CGH campaign |
| UGC \| @colombanese — Couple Application Explainer | 423 | $96.43 | 3.00% | Highest CTR, highest CPA — clicker profile mismatch |

---

## Creative Fatigue Status

**Frequency data (top 5 ads by purchases, 13-week window):** All showing 1.06–1.25.

Creative fatigue threshold is 3.0. **Creative fatigue is ruled out as a CPA driver.** Do not recommend creative refreshes based on frequency — the content is fresh.

---

## Platform Breakdown (Last 90 Days)

All platforms declined ~equally after Feb 16:
- Facebook: +3.6% CPA increase
- Instagram: +6.1% CPA increase
- Audience Network: +4.7% CPA increase

Simultaneous multi-platform decline confirms the cause is on-site (offer/landing page) not platform-side.

---

## Demographic Breakdown

Older audiences (45+) were hit hardest by the Feb 16 inflection. Consistent with price sensitivity — if the offer change made the product more expensive or reduced perceived value, older demographics react more strongly.

---

## Purchase Volume Trends (8-Week Comparison)

| Metric | Last 4 Weeks | Prior 4 Weeks | Change |
|---|---|---|---|
| Spend | $916,309 | $1,290,448 | -29% |
| Purchases | 10,573 | 15,598 | -32% |
| CPA | ~$87–96 | ~$83 | +~15% |
| CTR | 1.38% | 1.59% | -13% |
| CPM | $18.05 | $17.61 | +2.5% |

---

## Known Issues

### 1. Revenue Tracking Broken (CRITICAL)
`purchase_roas` and `website_purchase_roas` return zero across all campaigns. The META Pixel is likely not passing the `value` parameter on Purchase events. ROAS is invisible. Budget decisions are currently based on purchase count only. This must be fixed before value-based optimization (ROAS bidding, Value Optimization) can be used.

### 2. Budget Concentration in Manual Campaign
31% of total spend ($404K) is in a manual EVG campaign at $85 CPA while ASC delivers $79 CPA. This spread represents ~$25K–$30K/month in recoverable efficiency.

### 3. Sale Test – CGH Not Understood
The $35 CPA campaign ran Mar 11–25 and then stopped. The offer structure that drove this performance has not been analyzed or modeled for permanent use. This is the highest-value investigation in the account.

---

## META Rep Analysis (April 2026)

The META rep attributed the CPA dip to CTR/purchase rate negative correlation (-0.78) and internal auction competition.

**Our assessment:**
- Internal auction competition: valid point, worth testing campaign consolidation
- CTR/purchase correlation claim: weak. CTR is falling alongside purchases, not rising. The "clicker vs buyer algorithm shift" narrative doesn't hold when both metrics decline together.
- **The rep missed the Feb 16 inflection point entirely** — which is the actual root cause. Weight rep recommendations accordingly.
