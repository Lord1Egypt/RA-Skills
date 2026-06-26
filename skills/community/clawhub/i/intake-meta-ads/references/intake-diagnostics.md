# Intake Breathing — Diagnostic Playbooks

This file contains structured diagnostic frameworks for the most common issues in the Intake META account.

---

## Diagnostic 1: CPA Spike Investigation

When CPA rises significantly, run through these in order:

### Step 1 — Identify the Inflection Date
Pull daily campaign data (`--time-increment 1`, last 90 days). Look for the exact date CPA broke upward. A sudden break (1–3 day change) = external cause. A gradual increase over weeks = creative fatigue or audience saturation.

**Intake history:** The Feb 16, 2026 break was sudden (1-day shift). This points to an external cause rather than platform drift. Offer/landing page changes occurred in this timeframe and are the leading hypothesis, but root cause is not yet confirmed.

### Step 2 — Platform Check
Break by `publisher_platform`. If Facebook, Instagram, and Audience Network all move together → the cause is on-site (offer, landing page, checkout). If one platform moves while others stay flat → platform-specific issue (placement change, algorithm update, targeting issue).

### Step 3 — Creative/Frequency Check
Pull frequency data for top 10 ads by purchases. If any ad is above 2.5 frequency AND CTR has declined more than 20% from its peak → creative fatigue is a contributing factor. Below 2.5 = rule out creative fatigue.

**Intake status (Apr 2026):** Frequency 1.06–1.25 on top ads. Creative fatigue ruled out as a cause of the Feb 16 inflection.

### Step 4 — Demographic Check
Break by age + gender. If all demographics decline equally → external cause. If specific demographics (e.g., 45+) decline disproportionately → price sensitivity signal, check if offer change increased effective price for that segment.

### Step 5 — Offer/Landing Page Check
This requires information outside META data. Ask Max:
- Did checkout flow change around the inflection date?
- Did any discount, bundle, or subscription offer change?
- Did the landing page or pricing page change?
- Did shipping costs or return policy change?

**Intake history:** Offer/landing page changes occurred around Feb 16, 2026 and are the leading hypothesis for the CPA inflection. Root cause not yet confirmed — on-site conversion rate data (Shopify, GA4) is needed to validate. Competing hypotheses to rule out include: auction/competitive pressure, iOS signal loss changes, and audience saturation at scale.

---

## Diagnostic 2: ROAS / Purchase Value Missing

**Symptom:** `purchase_roas` and `website_purchase_roas` return 0 or null across all campaigns.

**Cause:** The META Pixel Purchase event is firing but not passing the `value` parameter. This means META knows purchases happened but not their dollar value.

### Verification Steps

1. Pull ROAS data:
```bash
python scripts/meta_campaign_insights.py \
  -t TOKEN \
  -a act_2335535636459862 \
  --date-preset last_7d \
  --level campaign \
  --fields campaign_name,spend,actions,action_values,purchase_roas,website_purchase_roas \
  -o /home/user/workspace/roas_check.csv
```

2. Check if `action_values:offsite_conversion.fb_pixel_purchase` is 0 while `actions:offsite_conversion.fb_pixel_purchase` is > 0. If so, confirmed: purchases are tracked but values are not.

### Fix Instructions (for Max to pass to dev team)

The Pixel's Purchase event call needs to include the `value` and `currency` parameters:

```javascript
// Correct implementation
fbq('track', 'Purchase', {
  value: 89.99,        // order total in USD
  currency: 'USD',
  content_ids: ['SKU123'],
  content_type: 'product'
});
```

Also verify via Conversions API (CAPI) that the server-side Purchase event is sending `value`. Check in META Events Manager → Data Sources → Intake Pixel → Test Events.

**Impact of fixing this:**
- Enables ROAS-based campaign optimization
- Unlocks Value Optimization bid strategy (optimize for high-value purchasers, not just purchase volume)
- Makes META's algorithm smarter about which audiences convert at higher AOV
- Enables accurate ROAS reporting for budget decisions

---

## Diagnostic 3: Campaign Budget Reallocation

**Use when:** CPA varies significantly across campaigns and budget is concentrated in a lower-efficiency campaign.

### Current Opportunity (as of Apr 2026)

| Campaign | Spend | CPA | Delta vs. Best |
|---|---|---|---|
| RG Prospecting EVG Manual Sales | $404K | $85.16 | +8% above ASC |
| RG Prospecting ASC Creative Testing | $147K | $78.76 | ← benchmark |

Moving $100K from Manual EVG to ASC at the current CPA differential saves approximately:
- Manual at $85.16 = 1,174 purchases per $100K
- ASC at $78.76 = 1,270 purchases per $100K
- **Net gain: ~96 additional purchases/month for the same $100K spend**

### Reallocation Protocol

1. Do NOT cut the Manual campaign abruptly — triggers a learning phase reset
2. Reduce Manual budget by ≤20% every 2–3 days
3. Increase ASC budget by equivalent amount, same cadence
4. Monitor for 7 days before next adjustment
5. Watch for ASC CPA to rise as it scales — if it exceeds $85 at new volume, pause reallocation

---

## Diagnostic 4: Sale Test – CGH Investigation

**Priority: HIGH.** This campaign ran Mar 11–25 at $35.64 CPA — 60% below account average. Understanding it is the highest-value investigation in the account.

### Data to Pull

```bash
# Pull campaign-level data with date range covering Mar 11–25
python scripts/meta_campaign_insights.py \
  -t TOKEN \
  -a act_2335535636459862 \
  --since 2026-03-01 \
  --until 2026-03-31 \
  --level adset \
  -o /home/user/workspace/sale_test_march.csv

# Pull ad-level for same period
python scripts/meta_campaign_insights.py \
  -t TOKEN \
  -a act_2335535636459862 \
  --since 2026-03-01 \
  --until 2026-03-31 \
  --level ad \
  -o /home/user/workspace/sale_test_ads_march.csv
```

Filter results to "Sale Test – CGH" campaign.

### Questions to Answer

1. What offer/discount was running during Mar 11–25?
2. What landing page or URL was the campaign pointing to?
3. Was this a sale price, a bundle, a subscription offer, or a promotional discount?
4. What ad creative ran in this campaign?
5. Why did it stop running on Mar 25?
6. Is the offer replicable permanently, or was it a one-time promotion?

**Target outcome:** Model a permanent offer structure based on whatever drove the $35 CPA. Even getting to $60 CPA permanently would transform the account economics.

---

## Diagnostic 5: Creative Performance Scoring

When evaluating ads, use this scoring rubric:

| Signal | Good | Concerning |
|---|---|---|
| CPA | < $80 | > $95 |
| CTR | > 1.5% | < 1.0% |
| Frequency (13-week) | < 2.5 | > 3.0 |
| Purchase volume | > 500/month | < 100/month |

**CTR ≠ CPA quality.** The @colombanese ad has 3.00% CTR but $96.43 CPA — high click rate with poor purchase conversion. This pattern suggests the creative attracts curiosity clicks (not buyer intent). Weight purchase CPA over CTR when ranking creative.

**Top creative benchmarks (Apr 2026):**
- Best CPA: New Sales Ad — $35.16 (tied to Sale Test CGH)
- Best CTR: @colombanese — 3.00% (but highest CPA in top 5)
- Best volume + efficiency balance: @drew.tts — 1,252 purchases at $75.40 CPA, 2.25% CTR

---

## Diagnostic 6: Learning Phase Check

If CPA is volatile or elevated on a specific campaign, check if it's in learning phase.

Signs of learning phase:
- Campaign or ad set recently launched (< 7 days)
- Budget changed >20% recently
- New ad added or removed from ad set
- CPA is highly variable day-to-day (>30% swings)

**Fix:** Do not make further changes. Wait 7 days and re-evaluate. If still in learning after 7 days with < 50 conversions/week, consider broadening targeting or increasing budget.

At Intake's spend level ($1M+/month), most campaigns should be well past learning phase. If a campaign shows "Learning Limited" status, it's likely fragmented — consolidation is the fix.
