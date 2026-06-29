---
name: "ecommerce-conversion"
description: "Diagnostic sub-skill for analyzing e-commerce purchase behavior, cart abandonment patterns, pricing perception, and checkout friction. Uses Human Behavior OS modules to diagnose WHY shoppers do or don't complete purchases. Outputs behavioral diagnosis ONLY — never provides conversion optimization tactics, pricing strategies, or sales interventions."
---

# E-Commerce Purchase Behavior Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules from the parent Human Behavior OS skill. It adds e-commerce-specific lenses for **understanding** shopper behavior patterns.

**Scope**: Diagnose WHY purchase behavior occurs or doesn't occur. Do NOT provide optimization playbooks.

---

## Diagnostic Framework

### The Purchase Journey (Analytical Lens)

```
Awareness → Consideration → Comparison → Decision → Purchase → Post-Purchase
```

Use each stage to locate WHERE in the journey behavior breaks down.

| Stage | Diagnostic Focus | Key Question |
|-------|-----------------|--------------|
| Awareness | How did shoppers discover the product? | Source effectiveness |
| Consideration | What need is driving interest? | Need layer identification |
| Comparison | How do they evaluate against alternatives? | Decision factor mapping |
| Decision | What prevents/enables the purchase decision? | Friction vs. driver analysis |
| Purchase | What happens at transaction completion? | Final-barrier diagnosis |
| Post-Purchase | What determines return/referral? | Satisfaction vs. expectation gap |

---

## Module-Specific Diagnostic Applications

### Purchase Need Diagnosis (Module 1)

**E-Commerce Need Layer Reference:**

| Need Layer | Shopper Behavior Signal | Product Category Example |
|-----------|------------------------|------------------------|
| L1 Survival | Emergency/essential buying | Medicine, repairs, staples |
| L2 Efficiency | Deal-seeking, comparison shopping | Tools, bundles, subscriptions |
| L3 Emotion | Impulse, gift, mood-driven | Fashion, entertainment, gifts |
| L4 Identity | Status/luxury purchasing | Premium brands, niche items |
| L5 Growth | Investment/self-improvement buying | Courses, equipment, books |

#### Need Diagnosis Output

```markdown
## Purchase Need Diagnosis
- **Active Need Layer(s)**: [From observed shopper behavior]
- **Purchase Trigger Event**: [What precipitated the shopping session]
- **Need-Urgency Level**: X/10 — [Evidence]
- **Need-Product Fit**: [Does the product actually serve this need?]
```

### Checkout Friction Diagnosis (Module 4)

**Friction Point Taxonomy for E-Commerce:**

| Friction Type | Where It Occurs | Behavioral Signal |
|--------------|-----------------|-------------------|
| Price friction | Product page / cart | Abandonment after price reveal |
| Trust friction | Payment page | Drop-off at payment method selection |
| Effort friction | Checkout form | Abandonment mid-form (long forms) |
| Option friction | Product selection | Cart abandonment with many variants |
| Delivery friction | Shipping info stage | Exit when shipping cost/time shown |
| Security friction | Payment stage | Exit at credit card entry |

#### Cart Abandonment Root Cause Framework

```markdown
## Cart Abandonment Diagnosis
- **Abandonment Rate**: X%
- **Drop-off Stage**: [Identify the specific step with highest exit]
- **Friction Classification**: [From taxonomy above]
- **Root Cause Hypothesis**: [Shoppers abandoned because...]
- **Supporting Evidence**: [Available data points]
- **Confidence Level**: [High/Medium/Low — based on data availability]
```

### Pricing Perception Diagnosis (Module 4)

**Price Value Gap Analysis:**

Use this framework to **assess** how shoppers perceive price relative to value — NOT to design pricing strategies.

| Perception Pattern | Shopper Behavior Signal | Diagnostic Interpretation |
|-------------------|------------------------|-------------------------|
| Price exceeds perceived value | High cart abandonment, price complaints | Value communication failure |
| Price aligns with value | Steady conversion, low price objections | Good value perception |
| Price below expected value | Very high conversion, possible margin loss | Underpricing signal |
| Price confusion | Questions about what's included | Clarity/communication issue |

#### Pricing Perception Diagnosis

```markdown
## Pricing Perception Analysis
- **Price Point**: $X
- **Perceived Value Estimate**: $Y (from shopper behavior signals)
- **Value Gap**: [Positive = good deal perception; Negative = overpriced perception]
- **Competitor Reference**: [How does this compare to alternatives in shopper's mind?]
- **Diagnosis**: [Shoppers perceive this product as underpriced/fair/overpriced because...]
```

### Trust Breakdown Diagnosis (Module 3)

**E-Commerce Trust Failure Points:**

| Failure Point | Shopper Signal | Common Cause |
|--------------|---------------|-------------|
| Pre-purchase trust | Low click-through, high bounce | No social proof, unfamiliar brand |
| Product-page trust | Short dwell time, no scroll | Poor images, sparse description |
| Cart trust | Add-to-cart but no checkout | Hidden costs feared, return anxiety |
| Payment trust | Exit at payment method | Security concerns, unfamiliar processor |
| Post-purchase trust | Returns, negative reviews | Product didn't match expectations |

#### Trust Diagnosis

```markdown
## E-Commerce Trust Diagnosis
- **Trust-Breakdown Stage**: [Where confidence was lost]
- **Failure Type**: [From table above]
- **Shopper Concern Identified**: [What specifically worried them]
- **Diagnosis**: [Trust broke down because...]
```

### Post-Purchase Behavior Diagnosis (Modules 5, 6, 7)

**Post-Purchase Outcome Spectrum:**

| Outcome | Behavior Signal | Diagnostic Implication |
|---------|----------------|----------------------|
| Satisfaction | Repeat purchase, positive review | Expectation met or exceeded |
| Neutral | No further action | Expectation met but no delight |
| Disappointment | Return, complaint, no repeat | Expectation gap (product < promise) |
| Advocacy | Referral, share, public praise | Expectation exceeded significantly |
| Regret | Return, negative review | Significant expectation gap |

#### Post-Purchase Diagnosis

```markdown
## Post-Purchase Behavior Diagnosis
- **Outcome Classification**: [From observed post-purchase data]
- **Expectation Alignment**: [Did product meet pre-purchase expectations?]
- **Gap Source**: [If gap exists: marketing promise vs. product reality vs. delivery experience]
- **Diagnostic Hypothesis**: [Post-purchase behavior indicates...]
```

---

## Complete Output: E-Commerce Behavior Diagnosis Report

```markdown
# E-Commerce Behavior Diagnosis Report

## Summary
[One-paragraph diagnosis of the core behavioral issue]

## Findings by Module
1. **Needs**: [What need drives/isn't driving purchase intent]
2. **Trust**: [Where trust exists/breaks down in the funnel]
3. **Decision Barriers**: [Primary frictions preventing purchase]
4. **Emotions**: [Pre-purchase emotional state and its effect]
5. **Post-Purchase**: [Satisfaction/return/referral pattern]

## Primary Root Cause Hypothesis
[Single most likely explanation for the observed behavior pattern]

## Suggested Investigation Paths
- Path A: [Data point or A/B test to validate hypothesis]
- Path B: [Alternative hypothesis to investigate]

## Key Metrics to Observe
[Metrics that will confirm or refute this diagnosis over time]
```
