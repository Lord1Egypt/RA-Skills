# Meta Ads Campaign Plan — Output Template

## 1. Campaign Overview

| Field | Value |
|---|---|
| Brand / Business Name | [Brand name] |
| Industry / Vertical | [e.g., Fashion DTC, Supplements] |
| Campaign Objective | [Sales / Traffic / Leads] |
| Campaign Duration | [Start] to [End] |
| Total Budget | $[amount] over [duration] |
| Daily Budget | $[amount] |
| Primary Goal | [e.g., Generate $X revenue at Y ROAS] |
| AOV | $[amount] |
| Target ROAS (Blended) | [X.Xx] |
| Breakeven CPA | $[amount] (AOV x Gross Margin %) |
| Attribution Window | [7-day click, 1-day view] |

**Key Assumptions**: List 3-5 assumptions about market, product, or audience informing this plan.

---

## 2. Audience Segments

### BOF — Retargeting

| Segment | Source | Window | Est. Size | Priority |
|---|---|---|---|---|
| Cart Abandoners — Recent | Pixel: AddToCart | 0-7 days | [size] | High |
| Cart Abandoners — Extended | Pixel: AddToCart | 8-14 days | [size] | Medium |
| Checkout Abandoners | Pixel: InitiateCheckout | 0-14 days | [size] | High |
| Product Viewers | Pixel: ViewContent | 0-7 days | [size] | Medium |
| Past Purchasers (cross-sell) | Customer List | 30-180 days | [size] | Medium |

**Exclusions**: Purchasers within [X] days

### MOF — Engagement

| Segment | Source | Window | Est. Size | Priority |
|---|---|---|---|---|
| Website Visitors | Pixel | 0-30 days | [size] | High |
| IG/FB Engagers | Profile interaction | 0-60 days | [size] | Medium |
| Video Viewers (75%+) | Video engagement | 0-30 days | [size] | Medium |
| Email Subscribers | Customer List | Active | [size] | Low |

**Exclusions**: All BOF audiences, purchasers within [X] days

### TOF — Prospecting

| Segment | Source | Spec | Est. Size | Priority |
|---|---|---|---|---|
| LAL — Purchasers 1% | Customer List | 1% US | [size] | High |
| LAL — High-AOV 1% | Filtered list | 1% US | [size] | High |
| LAL — Purchasers 2-3% | Customer List | 2-3% US | [size] | Medium |
| Interest Stack A | [Interests] | Detailed | [size] | Medium |
| Advantage+ Shopping | Algorithmic | Broad | Full market | Medium |
| Broad — No Targeting | None | Open | Full market | Test |

**Exclusions**: All MOF/BOF audiences, purchasers within [X] days

---

## 3. Creative Brief

### By Funnel Stage

**TOF Angles**:
| Angle | Hook/Headline | Format | Placement |
|---|---|---|---|
| Problem/Solution | [text] | [format] | [placement] |
| Social Proof | [text] | [format] | [placement] |
| Lifestyle | [text] | [format] | [placement] |

**MOF Angles**:
| Angle | Hook/Headline | Format | Placement |
|---|---|---|---|
| Product Education | [text] | [format] | [placement] |
| Testimonial | [text] | [format] | [placement] |

**BOF Angles**:
| Angle | Hook/Headline | Format | Placement |
|---|---|---|---|
| Urgency | [text] | [format] | [placement] |
| Cart Reminder | DPA | Carousel | Feed |
| Offer/Incentive | [text] | [format] | [placement] |

### Specs
| Format | Ratio | Resolution | Duration |
|---|---|---|---|
| Feed Image | 1:1 or 4:5 | 1080x1080/1350 | N/A |
| Feed Video | 1:1 or 4:5 | 1080x1080/1350 | 6-15s |
| Stories/Reels | 9:16 | 1080x1920 | 6-15s |
| Carousel | 1:1 | 1080x1080 | N/A |

### Ad Copy Template
**Primary Text**: [Hook line] > [Problem] > [Solution] > [Benefit] > [Social proof] > [CTA]
**Headline**: Max 40 characters | **Description**: Max 30 characters | **CTA Button**: Shop Now / Learn More

---

## 4. Placement Matrix

| Placement | TOF | MOF | BOF | Format |
|---|---|---|---|---|
| Facebook Feed | Yes | Yes | Yes | Image, Video, Carousel |
| Instagram Feed | Yes | Yes | Yes | Image, Video, Carousel |
| Instagram Stories | Yes | Yes | Yes | Vertical Video/Image |
| Instagram Reels | Yes | No | No | Vertical Video |
| Facebook Stories/Reels | Yes | No | No | Vertical Video |
| Marketplace | No | No | Yes | Image, Carousel |

---

## 5. Bidding Strategy

| Campaign Tier | Bid Strategy | Target | Rationale |
|---|---|---|---|
| TOF — Launch | Lowest Cost | No cap | Maximize learning |
| TOF — Scaled | Cost Cap | $[CPA] | Cost control + volume |
| MOF | Lowest Cost | No cap | Maximize engagement |
| BOF — Retargeting | Min ROAS | [X.Xx] | Revenue optimization |
| BOF — Dynamic Ads | Cost Cap | $[CPA] | Volume + cost balance |

**Escalation**: CPA >1.3x target for 3 days = reduce budget 20%. CPA >1.5x for 5 days = pause. Underdelivery (<70% budget) = loosen cap 10-15%.

---

## 6. Budget Allocation

### Monthly: $[total]

| Stage | % | Monthly | Daily |
|---|---|---|---|
| TOF | [X]% | $[amount] | $[amount] |
| MOF | [X]% | $[amount] | $[amount] |
| BOF | [X]% | $[amount] | $[amount] |
| Testing Reserve | [X]% | $[amount] | $[amount] |

### Campaign Breakdown

| Campaign | Funnel | Audience | Monthly $ | Bid Strategy |
|---|---|---|---|---|
| [Campaign 1] | TOF | [audience] | $[amount] | [strategy] |
| [Campaign 2] | TOF | [audience] | $[amount] | [strategy] |
| [Campaign 3] | MOF | [audience] | $[amount] | [strategy] |
| [Campaign 4] | BOF | [audience] | $[amount] | [strategy] |

---

## 7. Testing Plan

| Test | Variable | Control | Variant(s) | Budget | Duration |
|---|---|---|---|---|---|
| Creative hooks | Hook type | [control] | [A, B] | $[amount] | [X days] |
| Format | Static vs Video | [control] | [variant] | $[amount] | [X days] |
| Audience | LAL % | 1% LAL | 2-3%, 4-5% | $[amount] | [X days] |

**Success Criteria**: 50+ conversions/variant, 90% confidence, 3-7 day minimum

---

## 8. KPI Targets

| Metric | TOF | MOF | BOF | Blended |
|---|---|---|---|---|
| ROAS | [X.Xx] | [X.Xx] | [X.Xx] | [X.Xx] |
| CPA | $[amt] | $[amt] | $[amt] | $[amt] |
| CPM | $[amt] | $[amt] | $[amt] | $[amt] |
| CTR | [X.X]% | [X.X]% | [X.X]% | [X.X]% |

**Review**: Daily spend pacing + anomalies, weekly optimization, biweekly creative refresh, monthly strategic review.

### Naming Convention
- **Campaign**: `Brand_Funnel_Objective_Date`
- **Ad Set**: `AudienceType_Detail_Geo`
- **Ad**: `Format_Angle_Version`
