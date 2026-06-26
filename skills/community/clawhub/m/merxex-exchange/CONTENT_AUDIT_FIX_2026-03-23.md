# Website Content Audit — Pricing Accuracy Fix

**Date:** 2026-03-23 08:02 UTC  
**Task:** [Heartbeat Task] Audit merxex.com content — is it current and accurate?  
**Status:** ✅ Audit Complete — Fix Ready for Deployment

---

## Issue Found

The website incorrectly stated **"fees as low as 1%"** in two meta description tags, which is misleading because:

- Our **actual pricing** is a **flat 2%** transaction fee (validated and approved by Nate on 2026-03-19)
- The "1%" figure is only available in **future reputation tiers** (Legendary tier: 10,000+ contracts, 4.95★+ rating)
- This creates false expectations and could damage trust when agents discover the real pricing

## Fix Applied (Local)

Updated `/home/ubuntu/.zeroclaw/workspace/merxex-website/index.html`:

**Line 7 — Meta Description:**
```html
<!-- BEFORE -->
<meta name="description" content="...fees as low as 1%.">

<!-- AFTER -->
<meta name="description" content="...flat 2% transaction fee.">
```

**Line 16 — Extended Description:**
```html
<!-- BEFORE -->
<meta name="description-extended" content="...Fees as low as 1% for elite agents. ...">

<!-- AFTER -->
<meta name="description-extended" content="...Flat 2% transaction fee. ...">
```

## Verification

The FAQ section (line 75) already correctly states:
> "Registration is free. Merxex charges a **flat 2% transaction fee** on all contracts. ... Reputation-based fee tiers (1-2%) are planned for future release."

The hero stats (line 159) also correctly display:
> "2% Flat — Transaction Fee"

The reputation tiers section (lines 639-661) is properly marked "Coming Soon" with the 1%-2% range.

## Deployment Required

**Nate Action Needed:** Deploy the fix to production

```bash
cd /home/ubuntu/.zeroclaw/workspace/merxex-infra
./scripts/deploy-static.sh prod
```

This will:
1. Sync the updated `index.html` to S3
2. Invalidate CloudFront cache for `/*`
3. Make the fix live within 1-2 minutes

**Impact:** SEO meta descriptions will accurately reflect our flat 2% pricing, preventing customer confusion and maintaining trust.

---

## Additional Audit Findings

✅ **Copyright year:** Correct (2026)  
✅ **Pricing in hero/stats:** Accurate (2% Flat)  
✅ **FAQ section:** Accurate (flat 2%, tiers coming soon)  
✅ **Reputation tiers section:** Properly marked "Coming Soon"  
✅ **Payment methods:** Accurate (Stripe live, crypto coming v1.1)  
✅ **Exchange status:** Correctly shows "Operational — Improving Stability" badge  

**Overall:** Website content is current and accurate after this single fix.

---

## Next Steps

1. **Deploy fix** (command above) — 1 minute
2. **Verify deployment** — `curl -s https://merxex.com | grep "flat 2%"`
3. **Mark complete** — Update KG task status

**Priority:** Medium — accuracy fix, no security or revenue impact  
**Effort:** 1 minute deployment  
**Risk:** Low — single file change, well-tested deployment script