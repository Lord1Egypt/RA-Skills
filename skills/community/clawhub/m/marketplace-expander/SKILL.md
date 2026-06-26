---
name: marketplace-expander
description: Evaluate new marketplace opportunities by comparing platform fees, audience fit, competition density, fulfillment requirements, and expected ROI to build a prioritized expansion roadmap.
---

# Marketplace Expander

Systematically evaluate new marketplace opportunities for ecommerce sellers. This skill walks through platform fee analysis, audience-product fit scoring, competitive landscape assessment, fulfillment feasibility, and ROI modeling to produce a prioritized expansion roadmap with clear go/no-go recommendations.

---

## Quick Reference

Use this table to rapidly classify decisions during marketplace evaluation. Each row represents a critical evaluation dimension.

| Decision Area | Strong | Acceptable | Weak |
|---|---|---|---|
| **Platform Fee Impact** | All-in fees under 20% of revenue; margin remains above 25% after fees | All-in fees 20-30%; margin stays above 15% after fees | All-in fees exceed 30% or margin drops below 15% after fees |
| **Audience-Product Fit** | Platform's core demographic overlaps 70%+ with your buyer persona; category is top-10 on the marketplace | 40-70% demographic overlap; category exists but is not dominant | Under 40% overlap; your category is niche or unsupported on the platform |
| **Competition Density** | Fewer than 50 direct competitors in your subcategory; top sellers have under 5,000 reviews | 50-200 direct competitors; top sellers have 5,000-20,000 reviews | Over 200 direct competitors; entrenched sellers with 20,000+ reviews and brand lock-in |
| **Fulfillment Feasibility** | Existing 3PL or warehouse covers the marketplace region; integration takes under 2 weeks | Need one new fulfillment partner; integration takes 2-6 weeks | Requires building new logistics from scratch; regulatory or customs barriers; 6+ weeks to operationalize |
| **Expected ROI Timeline** | Positive unit economics from month 1; payback on setup costs within 3 months | Break-even by month 3; payback within 6 months | Break-even beyond 6 months; payback exceeds 12 months |
| **Regulatory & Compliance** | No new certifications required; existing product labels and documentation transfer directly | 1-2 new certifications or labeling changes needed; achievable within 30 days | Major regulatory hurdles (e.g., new country product safety standards, restricted categories); 60+ days and significant cost |
| **Brand Control & IP Protection** | Platform offers brand registry, counterfeit reporting, and content control | Partial brand tools available; some risk of unauthorized sellers | No brand protection tools; high risk of counterfeits or listing hijacking |

---

## Solves

This skill addresses the following problems ecommerce operators face when considering marketplace expansion:

1. **Scattered fee intelligence** -- Platform fee structures are complex (referral fees, fulfillment fees, subscription fees, advertising costs, currency conversion) and hard to compare apples-to-apples across marketplaces.
2. **Gut-feel marketplace selection** -- Sellers pick marketplaces based on hype or anecdotes instead of structured data about audience fit and category demand.
3. **Underestimating fulfillment complexity** -- Expanding to a new marketplace often means new warehouses, new 3PLs, customs paperwork, or marketplace-specific fulfillment programs (FBA, Shopee Fulfillment) that are poorly understood upfront.
4. **Ignoring competitive moats** -- Entering a marketplace where incumbents have tens of thousands of reviews and established ad positions leads to expensive, low-ROI launches.
5. **No ROI framework** -- Sellers invest in new marketplaces without modeling the timeline to profitability, leading to cash flow surprises and premature exits.
6. **Compliance blind spots** -- Product labeling, safety certifications, tax registration (VAT/GST), and import requirements vary by marketplace and region; missing these causes listing suspensions or border holds.
7. **Resource overextension** -- Trying to launch on too many marketplaces simultaneously dilutes focus and operational capacity, degrading performance on existing channels.

---

## Workflow

Follow these steps sequentially when evaluating a marketplace expansion opportunity. Each step builds on the outputs of the previous one.

### Step 1: Define Expansion Objectives and Constraints

Before evaluating any marketplace, document the seller's strategic context:

- **Revenue target**: What incremental annual revenue does the seller need from the new marketplace? (e.g., $500K in Year 1)
- **Product catalog scope**: Which SKUs are candidates for expansion? (full catalog vs. hero SKUs only)
- **Geographic appetite**: Which regions or countries are in scope?
- **Budget envelope**: How much can be invested in setup costs (listing creation, inventory, advertising launch budget)?
- **Operational capacity**: How many hours per week can the team allocate to a new channel? Is there headcount to hire?
- **Timeline**: When does the seller need to be live and generating revenue?

Document these in the "Expansion Objectives" section of the output template. These constraints act as filters throughout the evaluation.

### Step 2: Build the Marketplace Long List

Identify all plausible marketplaces based on the seller's product category, geography, and objectives. For each marketplace on the long list, capture:

- Marketplace name and region(s) served
- Estimated GMV and active buyer count
- Primary product categories
- Seller onboarding requirements (business registration, bank account, tax ID)
- Whether the marketplace is open to international sellers or requires a local entity

Typical long list sources:
- Industry reports (eMarketer, Marketplace Pulse, Statista)
- Competitor presence analysis (where are your competitors already selling?)
- Trade association recommendations for your product category

Aim for 5-10 marketplaces on the long list. Immediately eliminate any that require a local entity if the seller has no plans to establish one.

### Step 3: Score Each Marketplace on Five Dimensions

For each marketplace remaining on the long list, score it on a 1-5 scale across five dimensions. Use the Quick Reference table to calibrate scores.

**Dimension A: Platform Fees (Weight: 25%)**
Calculate the all-in cost to sell one unit of your hero product on each marketplace. Include:
- Referral/commission fee (category-specific percentage)
- Fulfillment fee (if using marketplace fulfillment)
- Storage fees (monthly, long-term)
- Payment processing fee
- Subscription/account fee (amortized per unit)
- Advertising cost assumption (use category average ACoS)
- Currency conversion fee (if applicable)

Reference: `references/platform-fee-comparison-guide.md`

**Dimension B: Audience-Product Fit (Weight: 25%)**
Assess how well the marketplace's buyer demographics and shopping behavior match your product:
- Age, income, and geographic distribution of the marketplace's buyers
- Category search volume and trend direction (growing, stable, declining)
- Average order value in your category vs. your price point
- Product format compatibility (e.g., does the marketplace favor bundles, subscriptions, or single units?)

**Dimension C: Competition Density (Weight: 20%)**
Analyze the competitive landscape in your specific subcategory:
- Number of sellers offering similar products
- Review counts and ratings of top 10 sellers
- Price range of competing products
- Brand presence (are major brands dominating, or is it fragmented?)
- Advertising saturation (estimated CPC for your top keywords)

**Dimension D: Fulfillment Feasibility (Weight: 15%)**
Evaluate the logistics requirements:
- Does your current 3PL serve this marketplace's region?
- Does the marketplace offer its own fulfillment service? Is it mandatory or optional?
- Shipping time expectations of buyers on this platform
- Return handling requirements
- Customs and import duties (for cross-border)

Reference: `references/expansion-readiness-framework.md`

**Dimension E: ROI Projection (Weight: 15%)**
Model the financial outcome for the first 12 months:
- Setup costs (listing creation, initial inventory, photography, compliance)
- Monthly fixed costs (subscription, software, incremental headcount)
- Monthly variable costs (fees, fulfillment, advertising)
- Revenue projection (conservative, base, optimistic)
- Months to break-even
- 12-month cumulative profit/loss

### Step 4: Rank and Shortlist

Calculate a weighted score for each marketplace:

```
Weighted Score = (Fee Score x 0.25) + (Fit Score x 0.25) + (Competition Score x 0.20) + (Fulfillment Score x 0.15) + (ROI Score x 0.15)
```

Rank marketplaces by weighted score. Apply a cut-off: marketplaces scoring below 3.0 are eliminated. The top 2-3 marketplaces become the shortlist for deeper analysis.

If only one marketplace scores above 3.0, proceed with that single option but flag the limited alternatives.

### Step 5: Deep-Dive on Shortlisted Marketplaces

For each shortlisted marketplace, conduct a detailed investigation:

- **Fee deep-dive**: Calculate exact fees for your top 10 SKUs, not just the hero product. Account for category-specific fee variations.
- **Demand validation**: Use marketplace-specific tools (Helium 10, Jungle Scout, Shopee Keyword Tool) to pull actual search volumes and sales estimates for your product keywords.
- **Compliance checklist**: Identify every certification, label, and registration required. Get cost and timeline estimates for each.
- **Fulfillment plan**: Select a specific 3PL or fulfillment program. Get rate quotes. Map the end-to-end order flow from purchase to delivery to return.
- **Launch budget**: Build a detailed 90-day launch budget covering inventory, advertising, promotions, and contingency.

### Step 6: Build the Expansion Roadmap

Sequence the shortlisted marketplaces into a phased rollout plan:

- **Phase 1 (Months 1-3)**: Launch on the highest-scoring marketplace. Allocate full team attention. Target: achieve break-even run rate.
- **Phase 2 (Months 4-6)**: If Phase 1 metrics are on track, begin onboarding for the second marketplace while optimizing the first.
- **Phase 3 (Months 7-12)**: Launch marketplace two; begin evaluation of marketplace three if warranted.

For each phase, define:
- Specific milestones and KPIs (revenue, unit sales, ACoS, margin)
- Resource allocation (headcount, budget)
- Go/no-go criteria for advancing to the next phase
- Risk mitigation actions

### Step 7: Validate with the Expansion Readiness Framework

Before finalizing the roadmap, run the seller's current operations through the readiness assessment to confirm they can support the planned expansion without degrading performance on existing channels.

Reference: `references/expansion-readiness-framework.md`

Use the checklist at `assets/marketplace-expander-checklist.md` to verify completeness of the evaluation.

---

## Worked Examples

### Example 1: DTC Skincare Brand Expanding to Amazon EU

**Context**: A US-based DTC skincare brand selling through their own Shopify store ($2.4M annual revenue) and Amazon US ($1.8M). They want to expand internationally to reach $6M total by end of next year. Product line: 12 SKUs of clean beauty serums and moisturizers, price range $28-$65. Team size: 5 people. Expansion budget: $150K.

**Step 1 -- Objectives and Constraints**:
- Revenue target: $1.8M incremental (from $4.2M to $6.0M)
- SKUs for expansion: Top 5 hero SKUs (80% of revenue)
- Geography: Europe and Southeast Asia
- Budget: $150K for setup and first 90 days of operation
- Capacity: Can hire 1 additional person; founders can allocate 15 hrs/week
- Timeline: Live within 4 months

**Step 2 -- Long List**:
| Marketplace | Region | Est. GMV | Open to US Sellers? |
|---|---|---|---|
| Amazon.de (EU unified) | EU (5 countries) | $38B | Yes |
| Amazon.co.uk | UK | $30B | Yes |
| Shopee | Southeast Asia (6 countries) | $18B | Yes (cross-border) |
| Lazada | Southeast Asia (6 countries) | $8B | Yes (cross-border) |
| TikTok Shop UK | UK | $2B | Yes |
| Zalando | EU (25 countries) | $12B | Yes (partner program) |

Eliminated: Zalando (fashion-only, skincare not a core category).

**Step 3 -- Scoring** (1-5 scale):

| Dimension | Amazon EU | Amazon UK | Shopee | Lazada | TikTok Shop UK |
|---|---|---|---|---|---|
| Platform Fees (25%) | 4 | 4 | 3 | 3 | 4 |
| Audience Fit (25%) | 5 | 5 | 2 | 2 | 4 |
| Competition (20%) | 3 | 3 | 4 | 4 | 5 |
| Fulfillment (15%) | 4 | 4 | 2 | 2 | 3 |
| ROI Projection (15%) | 4 | 4 | 2 | 2 | 3 |

Fee analysis detail for Amazon EU (hero product, Vitamin C Serum, retail $45):
- Referral fee: 8% = $3.60
- FBA fee (standard size): $4.20 (Pan-EU)
- Storage: $0.35/month
- Subscription (amortized): $0.15/unit
- Advertising (25% ACoS assumption): $11.25
- VAT impact: Registered in DE, reclaim input VAT
- **All-in fees: $19.55/unit = 43.4% of revenue** -- but $11.25 is advertising, not a platform fee. Platform fees alone: $8.30 = 18.4%. Acceptable.

Audience fit for Amazon EU: Clean beauty is a fast-growing category in Germany and France. Amazon.de Beauty category grew 22% YoY. Income demographics align well with $45 price point. Score: 5.

Competition for Amazon EU: Searched "Vitamin C Serum" on Amazon.de -- 4,000+ results, but top 10 have 2,000-8,000 reviews. The brand's US reviews won't transfer. Will need to build from zero. Score: 3.

**Step 4 -- Weighted Scores**:
- Amazon EU: (4x0.25)+(5x0.25)+(3x0.20)+(4x0.15)+(4x0.15) = 1.0+1.25+0.6+0.6+0.6 = **4.05**
- Amazon UK: (4x0.25)+(5x0.25)+(3x0.20)+(4x0.15)+(4x0.15) = **4.05**
- TikTok Shop UK: (4x0.25)+(4x0.25)+(5x0.20)+(3x0.15)+(3x0.15) = **3.90**
- Shopee: (3x0.25)+(2x0.25)+(4x0.20)+(2x0.15)+(2x0.15) = **2.65** -- eliminated
- Lazada: (3x0.25)+(2x0.25)+(4x0.20)+(2x0.15)+(2x0.15) = **2.65** -- eliminated

Shortlist: Amazon EU, Amazon UK, TikTok Shop UK.

**Step 5 -- Deep Dive Findings**:
- Amazon EU + UK can share FBA inventory via Pan-European FBA, reducing fulfillment complexity. Combined launch cost: ~$85K (inventory $50K, compliance $10K, advertising $20K, listing creation $5K).
- TikTok Shop UK requires video content creation capability. Estimated $30K for initial content + influencer seeding. Lower barrier to entry but requires different skills than the team currently has.
- EU compliance: Need EU Responsible Person, Cosmetic Product Notification Portal (CPNP) registration, multilingual labeling. Timeline: 8-10 weeks. Cost: $8K.

**Step 6 -- Roadmap**:
- Phase 1 (Months 1-4): Launch Amazon UK (simpler compliance -- no multilingual labels). Target: $30K/month revenue by Month 4.
- Phase 2 (Months 4-7): Expand to Amazon EU (DE, FR, IT, ES) using Pan-EU FBA. Target: $80K/month combined EU by Month 7.
- Phase 3 (Months 8-12): Evaluate TikTok Shop UK if video content capability has been built. Target: $25K/month.
- 12-month projection: $1.2M incremental revenue. Below $1.8M target -- flag to stakeholders that the target may require accelerated ad spend or additional marketplaces.

---

### Example 2: Electronics Accessories Seller Evaluating TikTok Shop vs Shopee

**Context**: A Shenzhen-based seller of phone cases and screen protectors currently on Amazon US ($3.2M), Amazon JP ($800K), and their own Shopify store ($400K). Exploring Southeast Asian marketplaces. Product range: 200+ SKUs, price range $8-$25. Team: 12 people including 3 dedicated to marketplaces. Budget: $80K for expansion.

**Step 1 -- Objectives and Constraints**:
- Revenue target: $1M incremental in Year 1
- SKUs: Top 30 SKUs (covers 60% of revenue)
- Geography: Southeast Asia (priority: Thailand, Vietnam, Philippines, Indonesia)
- Budget: $80K
- Capacity: Can dedicate 2 team members full-time; Mandarin and English fluency, basic Thai
- Timeline: Live within 6 weeks (aggressive)

**Step 2 -- Long List**:
| Marketplace | Region | Est. GMV | Notes |
|---|---|---|---|
| Shopee | SEA (6 countries) | $18B | Dominant in SEA, strong cross-border program |
| TikTok Shop | SEA (6 countries) | $16B | Fastest growing; content-driven |
| Lazada | SEA (6 countries) | $8B | Alibaba-backed; strong in electronics |
| Tokopedia | Indonesia | $7B | Merged with TikTok Shop ID |
| Sendo | Vietnam | $0.5B | Small; Vietnam-only |

Eliminated: Sendo (too small), Tokopedia (now merged with TikTok Shop Indonesia).

**Step 3 -- Scoring**:

| Dimension | Shopee | TikTok Shop | Lazada |
|---|---|---|---|
| Platform Fees (25%) | 4 | 5 | 3 |
| Audience Fit (25%) | 5 | 4 | 4 |
| Competition (20%) | 2 | 4 | 3 |
| Fulfillment (15%) | 4 | 3 | 4 |
| ROI Projection (15%) | 3 | 4 | 3 |

Key analysis:

**Shopee fees** (phone case, retail $12):
- Commission: 6.5% = $0.78
- Payment fee: 2.0% = $0.24
- Shopee cross-border service fee: 2.0% = $0.24
- Shipping subsidy program: Shopee often subsidizes shipping in exchange for seller co-pay (~$0.50/order)
- All-in platform fees: ~$1.76/unit = 14.7%. Strong.

**TikTok Shop fees** (phone case, retail $12):
- Commission: 5.0% = $0.60 (introductory rate, rises to 8% after 90 days)
- Payment fee: 1.0% = $0.12
- Shipping: Seller-arranged or TikTok Fulfillment, ~$1.20/order in-region
- Content creation cost (amortized): ~$0.40/unit (video production for 30 SKUs)
- All-in: ~$2.32/unit = 19.3% including content costs. Acceptable.

**Competition analysis**:
- Shopee "phone case" search in Thailand: 500,000+ results. Extremely saturated. Top sellers have 100K+ units sold. Price war environment -- many listings at $2-4 from local sellers. Score: 2.
- TikTok Shop: Significantly fewer established sellers in phone accessories. Content quality matters more than price alone. Viral potential for unique designs. Score: 4.

**Step 4 -- Weighted Scores**:
- Shopee: (4x0.25)+(5x0.25)+(2x0.20)+(4x0.15)+(3x0.15) = 1.0+1.25+0.4+0.6+0.45 = **3.70**
- TikTok Shop: (5x0.25)+(4x0.25)+(4x0.20)+(3x0.15)+(4x0.15) = 1.25+1.0+0.8+0.45+0.6 = **4.10**
- Lazada: (3x0.25)+(4x0.25)+(3x0.20)+(4x0.15)+(3x0.15) = 0.75+1.0+0.6+0.6+0.45 = **3.40**

Shortlist: TikTok Shop (1st), Shopee (2nd), Lazada (3rd -- borderline, keep as backup).

**Step 5 -- Deep Dive**:
- TikTok Shop: Team already has product photography; need to build short-form video capability. Can hire a local content creator in Thailand ($800/month) and Vietnam ($600/month). TikTok's affiliate program can drive sales through influencer partnerships at 10-15% commission. Estimated 90-day launch cost: $25K (inventory $12K, content $8K, ads $5K).
- Shopee: Cross-border seller program (SIP) provides logistics support from China. Lower setup friction but the price competition is brutal. Would need to compete at $6-8 price points (vs $12 target), which compresses margins to under 10%. Viable only with volume strategy.

**Step 6 -- Roadmap**:
- Phase 1 (Weeks 1-6): Launch TikTok Shop in Thailand and Vietnam (largest TAM, team has language capability). Start with top 15 SKUs. Hire 2 local content creators. Target: $40K/month by end of Month 3.
- Phase 2 (Months 3-5): Expand TikTok Shop to Philippines and Indonesia. Add 15 more SKUs. Target: $80K/month by Month 5.
- Phase 3 (Months 6-9): Launch on Shopee with a value-line strategy (select 10 SKUs priced competitively at $6-8). Use Shopee as a volume channel while TikTok Shop remains the margin channel. Target: $40K/month from Shopee.
- 12-month projection: TikTok Shop $960K + Shopee $280K = $1.24M. Exceeds $1M target.

**Key insight from this example**: The highest-GMV marketplace (Shopee) was not the best first move because competition density made profitability difficult. TikTok Shop's lower competition and content-driven discovery model better suited a seller with differentiated products.

---

## Common Mistakes

1. **Chasing GMV instead of category fit**: A marketplace processing $50B in GMV means nothing if your product category represents 0.1% of sales and the platform's algorithms don't surface it. Always check category-level demand, not just total marketplace size.

2. **Ignoring the all-in cost stack**: Sellers compare referral fees (e.g., "Shopee is 6.5% vs Amazon at 15%") without accounting for fulfillment fees, advertising costs, currency conversion, and marketplace-specific surcharges. The cheapest referral fee marketplace is often not the cheapest all-in.

3. **Assuming reviews and ratings transfer**: Launching on a new marketplace means starting with zero reviews, zero ratings, and zero search ranking history. Budget for the "cold start" period: heavy advertising, promotional pricing, and potentially 3-6 months before organic sales become meaningful.

4. **Underestimating content localization**: Translating listings is not localization. Each marketplace has different listing formats, keyword conventions, image requirements, and buyer expectations. A listing that converts at 15% on Amazon US may convert at 2% on Amazon.de if simply translated without cultural adaptation.

5. **Launching too many SKUs on day one**: Start with 5-15 hero SKUs. This reduces inventory risk, concentrates advertising budget, and lets you learn the marketplace's algorithms and buyer behavior before scaling. Many sellers launch 200 SKUs, spread budget thin, and conclude "the marketplace doesn't work."

6. **Neglecting marketplace-specific advertising**: Each platform has its own ad system with different auction mechanics, keyword tools, and optimization levers. Assuming your Amazon PPC expertise transfers directly to Shopee Ads or TikTok Promote leads to wasted spend. Budget for a learning period or hire platform-specific expertise.

7. **Skipping the compliance deep-dive**: Getting listings suspended 2 weeks after launch because you missed a required certification or labeling requirement is expensive and demoralizing. Do the compliance work before ordering inventory, not after.

8. **Not defining exit criteria**: Before launching, define what failure looks like. "If we haven't reached $X revenue at Y% margin by month Z, we will exit this marketplace." Without this, sellers keep pouring money into underperforming channels because of sunk cost bias.

9. **Ignoring working capital requirements**: New marketplaces may have 14-30 day payment cycles. Combined with 30-60 days of inventory lead time, you may need 60-90 days of working capital tied up before seeing any cash return. Model the cash flow impact, not just the P&L.

10. **Treating all marketplaces the same operationally**: Each marketplace has different customer service SLAs, return policies, and seller performance metrics. Amazon requires response within 24 hours; Shopee expects chat responses within minutes during business hours. Staff accordingly or risk account health penalties.

---

## Resources

- [Output Template](references/output-template.md) -- Structured template for documenting marketplace evaluation deliverables
- [Platform Fee Comparison Guide](references/platform-fee-comparison-guide.md) -- Side-by-side fee structure comparison across 7 major marketplaces
- [Expansion Readiness Framework](references/expansion-readiness-framework.md) -- Operational readiness assessment for marketplace expansion
- [Marketplace Expander Checklist](assets/marketplace-expander-checklist.md) -- Quality checklist with 40+ items across 8 categories
