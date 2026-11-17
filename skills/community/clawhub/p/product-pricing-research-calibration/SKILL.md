---
name: product-pricing-research-calibration
description: "Calibrate an enterprise-software or AI product-pricing research article before drafting. Use when a topic links pricing, packaging, governance, product strategy, or commercial model and there is a risk of treating broad platform pricing as direct feature pricing, using media-style vendor camps, or jumping to procurement advice before analyzing product facts."
description_zh: "产品定价研究校准"
description_en: "Product Pricing Research Calibration"
disable: false
agent_created: true
version: "1.0.0"
---

# Product Pricing Research Calibration

Use this workflow for enterprise software, AI platform, security, or governance research that studies how a capability is priced and what that says about product strategy.

## When to use

- A topic asks about pricing, packaging, monetization, commercial model, or product strategy.
- The evidence includes a mix of direct feature prices, broad AI bundles, usage credits, security services, and unpublished SKU prices.
- A draft risks becoming a vendor-news roundup, a vague strategic slogan, or a procurement guide before the commercial reality is understood.

## Not for

- Simple product price comparison where each SKU and scope is already comparable.
- Financial valuation or investment recommendation.
- Sales-pricing design advice for a specific vendor.

## Workflow

### Step 1: [Deterministic] Define the research object

Write one sentence each for:

1. The concrete capability under study.
2. What counts as direct pricing evidence.
3. What counts only as a commercial-attachment signal.
4. What the article explicitly will not answer.

Example distinction:
- Direct pricing evidence: a governance product has a public license and stated scope.
- Commercial-attachment signal: a broader AI bundle contains an agent development console, but has no governance-specific price.

Do not proceed until these two evidence types are separated.

### Step 2: [Deterministic] Build a fact matrix

For every vendor or product, record:

| Vendor | Product boundary | Public price or unit | License/purchaser | Capability evidence | Evidence strength | Permitted claim |
|---|---|---|---|---|---|---|

Use three evidence labels:
- **Direct**: official price plus explicit feature scope.
- **Adjacent**: broader plan or usage model that contains related agent capability.
- **Boundary-only**: product positioning exists but no public price.

A claim may never exceed its evidence label. Adjacent evidence cannot become “the feature is priced this way.” Boundary-only evidence cannot become a price comparison.

### Step 3: [LLM] Extract commercial attachment

For each supported example, answer three concrete questions:

1. **Product attachment**: Which existing product contains the capability?
2. **Responsibility / purchaser**: Who is licensed, owns the budget, or is accountable?
3. **Price unit**: What is counted: user, task, credit, organization, event, service, or something else?

Call this the **commercial attachment**. It is an interpretive clue, not proof of corporate strategy.

### Step 4: [LLM] Test causal strength

Before writing any conclusion, distinguish:

- Confirmed fact: what the vendor actually licenses, meters, includes, or announces.
- Supported inference: what product boundary the combined evidence suggests.
- Unsupported leap: “the vendor wants to win X,” “customers will pay Y,” or “this model will become the market standard.”

Pricing may also be shaped by existing contracts, channel structure, serving cost, sales maturity, and implementation cost. State this boundary if the article infers strategy from a price unit.

### Step 5: [LLM] Design the article around reality

Use this sequence:

1. **Reality**: show the non-comparable commercial forms.
2. **Mechanism**: explain why the forms differ through product attachment, responsibility, and price unit.
3. **Boundary**: explain what cannot yet be inferred and why a universal price may not exist.
4. **Conclusion**: state the narrowest conclusion supported by the evidence.

Do not begin with vendor factions, historical analogies, market-war metaphors, or procurement recommendations.

### Step 6: [Deterministic] Title check

A title must pass both tests:

- **Object test**: a reader can identify the concrete research object on first read.
- **Substance test**: the title states a real phenomenon or research proposition; it does not hide the answer behind “what it reveals,” “what they are really fighting for,” or another empty suspense phrase.

If the evidence cannot support a final conclusion, use a clear research proposition rather than an artificial hook.

### Step 7: [LLM] Draft and self-check

Before review, verify:

- Direct, adjacent, and boundary-only examples are visibly distinguished.
- Broad AI bundle pricing is never labeled as direct governance pricing.
- A security product without public price is discussed as product boundary, not price evidence.
- The draft analyzes current product facts before any implication for buyers or product teams.
- No vendor-news parade, media-war framing, or consulting-style “what you should buy” section appears.

## Hard Rules

1. Never treat a broad AI plan, token package, or organization bundle as direct pricing for a single governance feature unless the vendor explicitly states that scope.
2. Never infer company intent from one price point alone. Use “suggests,” “places,” or “attaches” only when product boundary, license object, and price unit align.
3. Do not construct a theory from acronyms or historical analogies before analyzing current product facts.
4. Do not turn research into procurement advice. Describe the commercial structure and leave decisions to the reader.
5. Title and thesis must state the actual research object. Avoid vague suspense and media-style oppositions.
6. Mark unpublished pricing as unpublished. Do not fill gaps with analyst estimates or unverified reseller claims.

## Failure handling

| Scenario | Action |
|---|---|
| Only broad AI package price is public | Label as adjacent evidence; analyze product attachment only. |
| Feature scope and price cannot be matched | Exclude it from price comparison; retain only as boundary evidence if official product material exists. |
| Thesis depends on an inferred corporate motive | Narrow to an observable product-boundary claim. |
| Article becomes a vendor roundup | Reorganize around price units and product attachment, not companies. |
| Title is abstract or hides the answer | Rewrite it as a concrete research proposition before drafting. |

## Output format

```text
Research object:
Direct pricing evidence:
Adjacent commercial signals:
Explicit exclusions:

Fact matrix:
| Vendor | Evidence label | Product attachment | Responsibility/purchaser | Price unit | Permitted claim |

Supported observation:
Boundary of the observation:
Draft structure: reality → mechanism → boundary → conclusion
Title check: object pass/fail; substance pass/fail
```
