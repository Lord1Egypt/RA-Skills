---
name: Global Tax Guide
description: Navigate tax obligations for multi-country ecommerce including VAT, GST, sales tax thresholds, and marketplace facilitator rules by region.
---

# Global Tax Guide

Navigate tax obligations for multi-country ecommerce including VAT, GST, sales tax thresholds, and marketplace facilitator rules by region. This skill converts your selling situation into a structured compliance map so you know where you're exposed, where you're covered, and what to do next.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Jurisdiction to assess first | Highest revenue market above threshold | Market approaching threshold | Market with negligible volume |
| Threshold status signal | Revenue + transaction count both clear | Revenue clear, count borderline | Only one metric tracked |
| Marketplace facilitator reliance | Platform confirmed MF in writing | Platform docs say MF applies | Assumed MF without confirmation |
| Filing scheme choice | OSS/IOSS for EU multi-country | Individual country VAT registrations | No scheme, selling anyway |
| Product classification approach | Category confirmed with local customs code | Same category used across all regions | Default to standard rate everywhere |
| Professional support trigger | Revenue exceeds $50k in new market | Launching into regulated product category | Any cross-border expansion |
| Compliance review cadence | Quarterly review with advisor | Annual review | Ad hoc when problems appear |

## Solves

1. **Threshold blindness** — Sellers cross economic nexus or VAT thresholds without realizing it, then face retroactive penalties and back-registration costs.
2. **Marketplace facilitator confusion** — Sellers remit tax on sales where the platform already collected it, or skip remittance assuming the platform handled it without confirming.
3. **Product classification errors** — Applying the wrong VAT rate to food supplements, clothing, digital products, or medical goods where reduced or zero rates apply.
4. **EU multi-country fragmentation** — Managing individual VAT registrations in 5+ EU countries instead of using OSS or IOSS where eligible.
5. **UK/EU post-Brexit divergence** — Treating UK and EU VAT rules as identical after 2021 rule changes created separate obligations for each territory.
6. **Digital product tax gaps** — Missing GST/VAT obligations for digital downloads and SaaS sold to consumers in Australia, Singapore, and New Zealand.
7. **Filing frequency miscalculation** — Filing annually when quarterly or monthly is required above certain revenue thresholds, triggering late penalties.

## Workflow

### Step 1 — Map Your Selling Footprint
List every country and US state you actively ship into. For each, record your approximate annual revenue and order count for the past 12 months. Flag any market where you crossed a revenue threshold mid-year, as partial-year threshold breaches create retroactive obligations in some jurisdictions.

### Step 2 — Identify Marketplace Facilitator Coverage
For each selling platform (Amazon, TikTok Shop, Shopee, Lazada, own Shopify), confirm in writing whether the platform acts as a marketplace facilitator for tax collection in each of your active markets. Do not assume — platform policies vary by country and change without announcement. Pull the platform's published MF policy page and document the date you reviewed it.

### Step 3 — Assess Threshold Status Per Jurisdiction
Apply the registration threshold rules for each jurisdiction:
- **EU VAT**: €10,000 annual cross-border threshold across all EU member states triggers OSS obligation; individual country thresholds were removed in 2021 for B2C digital goods
- **UK VAT**: £85,000 annual UK revenue threshold for non-established sellers shipping physical goods into UK
- **US Sales Tax**: Economic nexus thresholds vary by state; most common is $100,000 annual revenue OR 200 transactions — both may apply
- **Australia GST**: AUD $75,000 annual revenue threshold for both physical and digital goods
- **Singapore GST**: SGD $1,000,000 annual global turnover threshold; lower threshold applies to digital services sold to SG consumers
- **New Zealand GST**: NZD $60,000 annual threshold for remote sellers

### Step 4 — Flag Product-Specific Rate Variations
Identify any products in your catalog that may qualify for reduced VAT/GST rates or exemptions. Common flags: food and beverages (UK and EU zero/reduced rates apply to many categories), children's clothing (UK zero-rated), medical devices and supplements (varies widely by jurisdiction), digital educational content (some jurisdictions apply reduced rates), and books (zero-rated in many EU countries and UK).

### Step 5 — Build the Market-by-Market Obligations Map
For each jurisdiction: confirm registration status required (yes/no/MF-covered), identify filing scheme (individual registration, EU OSS, IOSS for imports under €150), note filing frequency, flag any product-specific rate adjustments, and assign a risk level (exposed, near threshold, covered).

### Step 6 — Generate the Remediation Plan
Rank markets by risk: highest revenue market where you're exposed comes first. For each exposed market, define the registration action, estimated timeline to become compliant, and whether a local tax agent or platform-specific service (e.g., Avalara, TaxJar, or a Big 4 advisor) is the right execution path.

### Step 7 — Output the Structured Report
Produce the four-section output: Market Summary Table, Obligations Narrative, Risk Flags, and Recommended Next Steps. Flag all outputs as educational and recommend professional verification before acting on any obligation assessment.

## Examples

### Example 1 — TikTok Shop UK Seller Expanding to EU

**Input:**
- Platforms: TikTok Shop UK, own Shopify store shipping to DE, FR, NL
- Revenue: UK £120,000, Germany €45,000, France €22,000, Netherlands €8,000
- Products: Skincare and cosmetics
- Current compliance: UK VAT registered, no EU registrations

**Output:**
```
MARKET SUMMARY TABLE
Market        | Tax Type | Threshold Status | MF Coverage
UK            | VAT 20%  | Above (registered) | TikTok Shop MF for TTS sales; Shopify requires direct registration
Germany       | VAT 19%  | Above €10k EU threshold | Not covered — direct registration or OSS required
France        | VAT 20%  | Above €10k EU threshold | Not covered — direct registration or OSS required
Netherlands   | VAT 21%  | Below individual NL threshold but above EU OSS threshold | OSS covers if combined EU > €10k

OBLIGATIONS NARRATIVE
You are above the EU cross-border threshold of €10,000 (your combined DE+FR+NL revenue is €75,000). You need to register for EU OSS in one EU member state to cover your EU B2C sales through Shopify. Your UK VAT registration covers Shopify UK sales; TikTok Shop acts as marketplace facilitator for its own platform sales in both UK and EU.

RISK FLAGS
1. HIGH — Shopify EU sales to DE, FR, NL are unregistered and above OSS threshold. Retroactive exposure for past 12 months.
2. MEDIUM — Cosmetics classification: verify whether any products qualify for reduced rates in specific EU markets (unlikely for cosmetics but confirm).

RECOMMENDED NEXT STEPS
1. Register for EU One Stop Shop (OSS) in Ireland or any EU member state within 30 days — this covers all EU B2C Shopify sales with a single quarterly return.
2. Engage an EU VAT specialist to assess retroactive back-filing exposure for the period you were above threshold without OSS registration.
3. Document TikTok Shop MF confirmation from TTS policy page and retain as compliance evidence.
```

### Example 2 — US Marketplace Seller Hitting State Nexus

**Input:**
- Platforms: Amazon US (FBA), own website
- Revenue: California $145,000, Texas $88,000, Florida $62,000, 18 other states $5,000–$15,000 each
- Products: Electronics accessories
- Current compliance: No sales tax registrations; assumed Amazon handles everything

**Output:**
```
MARKET SUMMARY TABLE
State         | Tax Type        | Threshold Status | MF Coverage
California    | Sales Tax 7.25%+| Above ($145k > $100k) | Amazon FBA: YES (MF). Own website: NO
Texas         | Sales Tax 6.25%+| Near ($88k, approaching $100k or 200 txn) | Amazon FBA: YES. Own website: NO
Florida       | Sales Tax 6%+   | Near ($62k) | Amazon FBA: YES. Own website: NO
Other 18 states | Varies       | Most below thresholds | Amazon FBA: YES. Own website: Below most thresholds

OBLIGATIONS NARRATIVE
Amazon FBA collects and remits sales tax in all states where it operates as a marketplace facilitator — this covers your Amazon sales entirely. Your own website sales are your direct responsibility. California: your website sales alone are $X (need to isolate). If your website-only California revenue exceeds $100,000 or 200 transactions, you have economic nexus there independently.

RISK FLAGS
1. HIGH — Own website California sales likely create independent nexus. Register for California Seller's Permit immediately.
2. MEDIUM — Texas approaching threshold on combined revenue basis. Monitor monthly.
3. LOW — Own website sales in 18 smaller states are likely below thresholds but confirm transaction counts for any state approaching 200 transactions.

RECOMMENDED NEXT STEPS
1. Pull website-only revenue by state for past 12 months to separate from Amazon MF-covered sales.
2. Register for California Seller's Permit via CDTFA online portal (2–3 business days).
3. Implement TaxJar or Avalara on your website to automate calculation and track nexus exposure in real time.
4. Set a threshold monitor alert at 80% of revenue or transaction limits for Texas and 5 other large states.
```

## Common Mistakes

1. **Assuming Amazon MF coverage extends to your own website** — Amazon's marketplace facilitator status covers Amazon-facilitated sales only. Your own DTC site always creates its own nexus exposure.

2. **Using the old EU country-level VAT thresholds post-2021** — The EU's distance selling thresholds (€35,000–€100,000 per country) were replaced by a single €10,000 cross-border threshold across all EU member states in July 2021. Many guides still show the old numbers.

3. **Not tracking transaction counts alongside revenue** — Many US states have dual nexus triggers (revenue OR transaction count). A seller with $60,000 in revenue but 250 transactions in a state can still be over the nexus threshold.

4. **Treating digital products the same as physical goods** — In Australia, Singapore, and the EU, digital services have different registration thresholds and sometimes different tax rates compared to physical goods. Applying physical goods rules to digital downloads creates gaps.

5. **Not confirming marketplace facilitator status in writing** — Platform MF policies change and may not apply in all markets or for all seller types. Assuming MF coverage without confirming it creates liability.

6. **Filing VAT returns with the wrong frequency** — Many sellers default to annual filing when their revenue requires quarterly or monthly returns. Late filing penalties apply from the first missed deadline.

7. **Ignoring UK/EU divergence on IOSS** — The Import One Stop Shop (IOSS) covers low-value imports (under €150) into the EU. UK has a separate equivalent called the OSS for UK imports. These are separate registrations with separate filing requirements.

8. **Not classifying products before estimating rates** — Tax rate estimates are meaningless if the product classification hasn't been confirmed. A 20% VAT estimate is wrong if your product qualifies for a 0% or 5% rate in that jurisdiction.

9. **Waiting for marketplace penalties before registering** — Marketplaces increasingly check seller tax compliance and can suspend listings or dithold payouts for sellers without valid VAT/GST numbers in required markets.

10. **Missing post-Brexit UK requirements for EU sellers** — EU sellers shipping physical goods into the UK need UK VAT registration once they exceed the £85,000 threshold, independent of any EU VAT registration they hold.

## Resources

- [output-template.md](references/output-template.md) — Structured output format for tax obligation reports
- [jurisdiction-reference.md](references/jurisdiction-reference.md) — Threshold reference table by country with registration links
- [marketplace-facilitator-guide.md](references/marketplace-facilitator-guide.md) — Platform-by-platform MF coverage reference
- [compliance-checklist.md](assets/compliance-checklist.md) — Quality checklist for reviewing completed tax assessments
