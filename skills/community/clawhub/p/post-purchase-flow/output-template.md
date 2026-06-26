# Post-Purchase Flow — Output Template

Use this template to deliver a complete post-purchase flow design to the client or stakeholder.

---

## 1. Executive Summary

**Brand:** [Brand name]
**Industry/Category:** [e.g., DTC Skincare, Fashion Marketplace, Consumer Electronics]
**Average Order Value:** $[AOV]
**Current Repeat Purchase Rate:** [X%]
**Current WISMO Ticket Share:** [X% of total support volume]
**Current Review Collection Rate:** [X%]

### Goals
- Increase repeat purchase rate from [X%] to [Y%]
- Reduce WISMO support tickets by [X%]
- Improve review collection rate from [X%] to [Y%]
- [Additional goal]

---

## 2. Current State Audit

### Existing Touchpoints

| Touchpoint | Channel | Timing | Open Rate | Click Rate | Notes |
|---|---|---|---|---|---|
| Order confirmation | Email | Immediate | [X%] | [X%] | [Current state notes] |
| Shipping confirmation | Email | On shipment | [X%] | [X%] | |
| Delivery confirmation | Email/SMS | On delivery | [X%] | [X%] | |
| Review request | Email | [Current timing] | [X%] | [X%] | |
| Cross-sell/reorder | Email | [Current timing] | [X%] | [X%] | |

### Identified Gaps
1. [Gap description — e.g., "No proactive delay communication"]
2. [Gap description]
3. [Gap description]

---

## 3. Proposed Post-Purchase Journey Map

### Timeline Overview

```
Day 0: Order placed
  └─ Order confirmation email (immediate)
  └─ Order confirmation SMS (immediate, optional)
Day 1-2: Order ships
  └─ Shipping confirmation email
  └─ Shipping confirmation SMS
Day 2-4: In transit
  └─ Proactive delay alert (if applicable)
Day 3-7: Delivered
  └─ Out for delivery notification (SMS)
  └─ Delivery confirmation email
  └─ Unboxing experience (physical)
Day 10-14: Review window
  └─ Review request email
Day 17-21: Review follow-up
  └─ Review reminder (non-responders only)
Day 30-60: Replenishment window
  └─ Replenishment/cross-sell email
  └─ Replenishment SMS reminder
Day 45-75: Win-back window
  └─ Win-back sequence (non-purchasers)
```

---

## 4. Touchpoint Specifications

### 4.1 Order Confirmation Email

**Timing:** Within 60 seconds of order placement
**Subject line:** [Recommended subject line]
**Preview text:** [Preview text]

**Content blocks:**
1. Warm thank-you header with brand voice
2. Order summary (items, quantities, prices)
3. Shipping method and estimated delivery window
4. "What happens next" timeline graphic
5. Cross-sell recommendations (2-3 complementary products)
6. Support links and FAQ
7. Social media follow CTAs

**Conditional logic:**
- First-time buyer: Include welcome message and brand story
- Repeat buyer: Include loyalty points earned and tier status
- High-value order ($X+): Add personal thank-you note element
- Gift order: Adjust messaging for gift giver vs. recipient

---

### 4.2 Shipping Notification Sequence

**Trigger:** Carrier scan events via shipment tracking integration

| Event | Channel | Subject/Message | Key Content |
|---|---|---|---|
| Label created | Email | "We're packing your order!" | Estimated ship date, preparation details |
| Shipped | Email + SMS | "Your order is on its way!" | Tracking link, estimated delivery, content CTA |
| In transit milestone | SMS (optional) | "Your package is in [city]" | Updated ETA |
| Out for delivery | SMS | "Arriving today!" | Real-time tracking link |
| Delivered | Email | "Your order has arrived!" | Unboxing guide, setup instructions |
| Delayed | Email + SMS | "Shipping update for your order" | New ETA, apology, support contact |

---

### 4.3 Unboxing Experience

**Physical elements:**
- [ ] Branded outer packaging
- [ ] Inner wrapping/tissue paper
- [ ] Insert card with CTA (QR code to [destination])
- [ ] Product-specific care/setup guide
- [ ] Surprise element (sample, sticker, note)
- [ ] Return/exchange information

**Digital companion:**
- QR code destination: [URL — setup guide, social sharing page, loyalty enrollment]
- Social sharing hashtag: #[BrandHashtag]
- Photo contest or UGC campaign details

---

### 4.4 Review Collection Flow

**Timing rules by category:**

| Product Category | Initial Request | Follow-up | Max Touches |
|---|---|---|---|
| Consumables (food, beauty) | Day 7 post-delivery | Day 14 | 2 |
| Apparel & accessories | Day 10 post-delivery | Day 17 | 2 |
| Electronics & gadgets | Day 14 post-delivery | Day 21 | 2 |
| Home & furniture | Day 14 post-delivery | Day 21 | 2 |

**Incentive structure:**
- Text review: [X loyalty points / X% discount]
- Photo review: [X loyalty points / X% discount]
- Video review: [X loyalty points / X% discount]

**Negative review handling:**
- Ratings 1-3 stars → Route to support team before public posting
- Support response SLA: [X hours]
- Resolution follow-up: Invite updated review after resolution

---

### 4.5 Cross-Sell & Replenishment Sequence

**Replenishment timing by category:**

| Product Category | Avg Consumption Cycle | First Reminder | Second Reminder |
|---|---|---|---|
| [Category 1] | [X days] | Day [X-10] | Day [X] |
| [Category 2] | [X days] | Day [X-10] | Day [X] |

**Cross-sell recommendation rules:**
1. Complementary products from same category
2. Frequently bought together items
3. Higher-tier/premium alternatives
4. Seasonal or trending items in related categories

**Incentive ladder:**
- First replenishment: [X% discount or free shipping]
- Subscription conversion: [X% ongoing discount]
- Win-back (60+ days inactive): [X% discount with expiration]

---

## 5. Technical Requirements

### Integrations Needed
- [ ] ESP/Marketing automation: [Platform]
- [ ] SMS provider: [Platform]
- [ ] Shipping/tracking: [Carrier API or aggregator]
- [ ] Review platform: [Platform]
- [ ] Loyalty program: [Platform]
- [ ] Ecommerce platform: [Platform]

### Data Requirements
- Order data (items, value, shipping method)
- Customer data (purchase history, segment, lifetime value)
- Shipping events (carrier webhooks)
- Product metadata (category, consumption cycle, complementary items)
- Engagement data (email opens, clicks, website visits)

---

## 6. Success Metrics & Targets

| Metric | Current | Target | Measurement |
|---|---|---|---|
| Repeat purchase rate (90-day) | [X%] | [Y%] | Cohort analysis |
| Time to second order | [X days] | [Y days] | Median calculation |
| WISMO ticket share | [X%] | [Y%] | Support ticket categorization |
| Review collection rate | [X%] | [Y%] | Reviews / delivered orders |
| Post-purchase email revenue | $[X] | $[Y] | Attribution model |
| NPS / CSAT | [X] | [Y] | Survey at Day 30 |

---

## 7. Implementation Roadmap

| Phase | Timeline | Deliverables |
|---|---|---|
| Phase 1: Foundation | Weeks 1-2 | Order confirmation redesign, shipping notifications setup |
| Phase 2: Engagement | Weeks 3-4 | Review collection flow, unboxing experience design |
| Phase 3: Revenue | Weeks 5-6 | Cross-sell sequences, replenishment automations |
| Phase 4: Optimization | Ongoing | A/B testing, performance analysis, iteration |
