---
name: Product Lifecycle Planner
description: Map products across introduction, growth, maturity, and decline stages with stage-appropriate marketing, pricing, and inventory strategies.
---

# Product Lifecycle Planner

Classify every product in your catalog into its current lifecycle stage — Introduction, Growth, Maturity, or Decline — and receive tailored marketing, pricing, and inventory strategies calibrated to each stage. This skill transforms raw sales trajectory data into a strategic roadmap that tells you exactly how to treat each product right now and what transitions to prepare for next. It bridges the gap between historical sales numbers and forward-looking product strategy by combining velocity trends, revenue acceleration, margin trajectory, and competitive signals into stage assignments with actionable playbooks.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Data window | 12+ months of monthly sales covering full seasonality | 6-11 months with known gaps documented | Under 6 months or missing peak season |
| Stage classification | 4-stage model (Intro/Growth/Maturity/Decline) with confidence scores | 4-stage model without confidence indicators | Binary "growing vs not" without nuance |
| Transition signals | Leading indicators flagged 30-60 days before stage shift | Stage assignment only, no forward look | Backward-looking classification only |
| Strategy specificity | Channel-specific tactics with budget allocations per stage | General stage-appropriate recommendations | Generic "invest more" or "cut spend" |
| Portfolio view | Cross-catalog stage distribution with balance assessment | Individual product stages without portfolio context | Products analyzed in isolation |
| Financial grounding | Dollar-value projections for each strategic recommendation | Directional impact (high/medium/low) | No financial quantification |

## Solves

- You launched several new products and need to determine which ones have caught traction, which are plateauing, and which should be sunsetted before they become deadweight inventory
- Your marketing team is planning next quarter's budget allocation and needs to know which products deserve awareness spending versus which should get loyalty or clearance campaigns
- You are preparing a quarterly business review and need a visual portfolio lifecycle map showing how your catalog is distributed across stages
- Your purchasing team needs lead-time-adjusted inventory recommendations that account for whether products are accelerating, stable, or winding down
- You merged product lines after an acquisition and need a unified framework to compare lifecycle positions across previously separate catalogs
- You need to identify products approaching decline early enough to execute graceful exit strategies rather than panic liquidation
- Your pricing team wants stage-aware pricing guidance — penetration pricing for Introduction, value capture for Growth, competitive pricing for Maturity, and clearance for Decline

## Workflow

### Step 1 — Collect and validate time-series sales data
Gather monthly or weekly sales data for each product covering at minimum the last six months. Required fields: product name or SKU, time period, units sold, and revenue per period. Optional but valuable: product launch dates, COGS per period, marketing spend per product, and category or product line groupings. Validate completeness by checking for missing periods, zero-revenue months that might indicate stockouts versus true zero demand, and data anomalies.

### Step 2 — Calculate trajectory metrics
For each product compute: month-over-month unit growth rate (last 3 months average), revenue acceleration (is growth rate itself increasing or decreasing), peak revenue identification (highest monthly revenue achieved and how far current revenue is from peak), cumulative revenue curve shape (convex = still accelerating, linear = stable, concave = decelerating), and time since launch if launch dates are available.

### Step 3 — Classify into lifecycle stages
Apply the stage classification framework:
- **Introduction**: Less than 6 months since launch OR revenue below 10% of category average AND positive month-over-month growth. Characterized by low but growing sales, high customer acquisition cost, negative or minimal profit contribution.
- **Growth**: Positive revenue acceleration (growth rate is increasing), revenue between 10-80% of eventual peak, expanding month-over-month. Characterized by rapidly increasing sales, improving margins from scale, growing market share.
- **Maturity**: Revenue within 20% of peak, growth rate near zero or single-digit, stable month-over-month patterns. Characterized by peak or near-peak sales, highest absolute profit, market saturation signals.
- **Decline**: Revenue more than 20% below peak with negative trend sustained 3+ months, decelerating sales velocity. Characterized by falling sales, margin compression from discounting, shrinking market relevance.

Assign a confidence level (High/Medium/Low) based on data sufficiency and pattern clarity.

### Step 4 — Generate stage-specific strategy briefs
For each product, produce a strategy brief containing:
- **Pricing approach**: Penetration (Intro), value capture (Growth), competitive/premium (Maturity), clearance/harvest (Decline)
- **Marketing channel priorities**: Ranked by expected ROI for that stage with budget allocation percentages
- **Inventory posture**: Build stock (Growth), maintain (Maturity), draw down (Decline), test quantities (Intro)
- **Product development**: Line extensions (Growth), refresh/bundle (Maturity), sunset planning (Decline)

### Step 5 — Build the transition watch list
Flag products showing early indicators of an upcoming stage shift: Growth products whose acceleration is decelerating (approaching Maturity), Maturity products with 2+ consecutive months of decline (entering Decline), Introduction products with strong velocity (graduating to Growth). For each, specify the estimated timeline and recommended preemptive actions.

### Step 6 — Compile portfolio lifecycle map
Produce the final portfolio view showing: stage distribution (% of SKUs and % of revenue in each stage), portfolio balance assessment (healthy portfolios have products across all stages), revenue concentration risk (what % of revenue comes from Maturity/Decline products), and pipeline health (are Introduction/Growth products sufficient to replace declining revenue).

### Step 7 — Validate and sanity-check
Cross-check classifications against: seasonal products (a winter product in summer looks like Decline but isn't), promotional spikes (a one-time sale doesn't indicate Growth), supply constraints (stockouts create artificial Decline signals), and new market entries (products new to a channel may show Introduction patterns despite being mature products). Flag any overrides with justification.

## Example 1: DTC Skincare Brand (35 Products)

**Input data**: 18 months of Shopify sales data, 35 active SKUs across 4 product lines (cleansers, serums, moisturizers, SPF).

**Stage classification results**:
- Introduction: 5 products (14%) — launched in last 4 months, generating 3% of revenue
- Growth: 8 products (23%) — generating 31% of revenue, average MoM growth 18%
- Maturity: 15 products (43%) — generating 58% of revenue, stable ±3% MoM
- Decline: 7 products (20%) — generating 8% of revenue, average MoM decline -12%

**Key strategy outputs**:
| Product | Stage | Confidence | Key Action | Timeline |
|---|---|---|---|---|
| Vitamin C Serum 30ml | Growth | High | Increase ad spend 40%, launch 60ml variant | Next 30 days |
| Original Cleanser | Maturity | High | Bundle with new serums, loyalty program focus | Ongoing |
| Retinol Night Cream | Decline | Medium | Clearance at 30% off, discontinue in 90 days | Immediate |
| Peptide Eye Cream | Introduction | Low | Monitor 60 more days before scaling spend | 60-day review |

**Transition watch list**: Hyaluronic Acid Serum showing deceleration — 3 months of declining growth rate despite still-positive sales. Recommend shifting from acquisition to retention marketing within 30 days.

## Example 2: Amazon Electronics Seller (200 Products)

**Input data**: 12 months of Amazon Seller Central data, 200 active ASINs across phone accessories, cables, and audio.

**Stage classification results**:
- Introduction: 22 products (11%) — new listings from last quarter, 2% of revenue
- Growth: 38 products (19%) — generating 28% of revenue
- Maturity: 89 products (45%) — generating 61% of revenue
- Decline: 51 products (25%) — generating 9% of revenue

**Portfolio health assessment**: Revenue is dangerously concentrated in Maturity (61%) with insufficient Growth pipeline (28%) to replace the 9% actively declining. At current trajectory, 15% revenue gap will emerge within 6 months as Decline products exit and Maturity products begin transitioning. Recommendation: accelerate new product launches and invest in Growth product visibility.

**Financial impact**: Implementing stage-appropriate strategies projected to save $23,400/year in misallocated ad spend (currently spending acquisition dollars on Decline products) and generate $41,000 in additional revenue by reallocating budget to Growth products.

## Common Mistakes

1. **Confusing seasonality with lifecycle stage**: A winter product's summer sales dip is not Decline. Always analyze stage using year-over-year comparisons for seasonal products, or explicitly exclude off-season months from the trajectory analysis.

2. **Ignoring data sufficiency**: Products with fewer than 3 months of sales history cannot be reliably classified. Flag them as "Insufficient Data" rather than guessing — a wrong Introduction vs. Growth classification leads to dramatically different (and potentially wasteful) strategy recommendations.

3. **Treating all Decline products the same**: Some products decline slowly over years (harvest opportunity) while others crater in weeks (urgent exit). Always specify the decline velocity and recommended response timeline. A product declining 2% monthly needs a different strategy than one declining 20% monthly.

4. **Classifying at the wrong granularity**: A product variant (e.g., "Blue, Size M") may be in Decline while the parent product is in Growth. Decide upfront whether to classify at the SKU, parent product, or product line level and document the rationale.

5. **Missing the Growth-to-Maturity transition**: This is the most expensive transition to miss. Products entering Maturity need a strategy shift from market expansion to market defense. Continuing to spend on acquisition marketing for a Maturity product wastes budget that should shift to retention and loyalty.

6. **Not accounting for external factors**: A competitor's product launch, a platform algorithm change, or a viral moment can shift lifecycle stages abruptly. Always note external factors that may be driving trajectory changes, as the strategic response differs from organic stage transitions.

7. **Presenting stage assignments without actionable strategies**: Simply labeling a product "Maturity" is useless without specifying what to do about it. Every stage classification must come with at least three specific, actionable recommendations covering pricing, marketing, and inventory.

8. **Failing to build the portfolio view**: Individual product stages are less valuable than the portfolio distribution. A catalog with 80% Maturity products and 5% Growth products is headed for a revenue cliff regardless of how well each individual product is managed.

## Resources

- [Output template](references/output-template.md) — Structured report format for presenting lifecycle analysis results
- [Stage classification framework](references/stage-classification.md) — Detailed rules, thresholds, and edge cases for stage assignment
- [Stage strategy playbooks](references/stage-strategies.md) — Comprehensive marketing, pricing, and inventory tactics per stage
- [Quality checklist](assets/quality-checklist.md) — Pre-delivery validation checklist
