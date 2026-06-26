# Post-Purchase Email Timing Guide

Comprehensive timing recommendations for every post-purchase touchpoint, organized by product category and channel.

---

## Core Timing Principles

### The Post-Purchase Attention Curve

Customer attention follows a predictable curve after purchase:

- **Peak attention (Day 0-1):** Order confirmation window. Customers actively check email and tracking. Open rates 60-80%.
- **High attention (Day 1-5):** Shipping and delivery window. Customers monitoring package progress. Open rates 50-70%.
- **Moderate attention (Day 5-14):** Product experience window. Customers using the product and forming opinions. Open rates 25-40%.
- **Declining attention (Day 14-30):** Review and cross-sell window. Engagement drops unless content is highly relevant. Open rates 15-25%.
- **Low attention (Day 30+):** Replenishment and win-back window. Requires strong hooks or incentives. Open rates 10-18%.

### Channel Selection by Urgency

| Urgency Level | Primary Channel | Secondary Channel | Use Case |
|---|---|---|---|
| Immediate | SMS | Push notification | Delivery alerts, time-sensitive offers |
| Same day | Email | SMS | Shipping updates, order status changes |
| Within 48 hours | Email | — | Review requests, content recommendations |
| Flexible | Email | — | Cross-sell, educational content, loyalty updates |

---

## Timing by Product Category

### Consumables (Food, Supplements, Beauty, Personal Care)

**Consumption cycle:** 30-90 days depending on product size and usage frequency.

| Touchpoint | Timing | Channel | Notes |
|---|---|---|---|
| Order confirmation | Immediate | Email + SMS | Include usage instructions or recipe ideas |
| Shipping confirmation | On shipment | Email | Storage or handling instructions if perishable |
| Delivery confirmation | On delivery | Email + SMS | First-use guide, dosage reminder setup |
| Check-in / tips | Day 5 post-delivery | Email | "How to get the most from your [product]" |
| Review request | Day 7-10 post-delivery | Email | Enough time to experience results |
| Review follow-up | Day 14-17 post-delivery | Email | Non-responders only, add incentive |
| Replenishment reminder | 10 days before estimated depletion | Email + SMS | One-click reorder, subscription offer |
| Urgent reorder | Estimated depletion day | SMS | "Running low? Reorder now for [delivery estimate]" |
| Win-back | Day 75+ (no reorder) | Email | Stronger incentive, "we miss you" messaging |

### Apparel & Accessories

**Consumption cycle:** Seasonal/trend-driven, 60-120 days between purchases.

| Touchpoint | Timing | Channel | Notes |
|---|---|---|---|
| Order confirmation | Immediate | Email | Size guide reminder, styling suggestions |
| Shipping confirmation | On shipment | Email | Care instructions preview |
| Delivery confirmation | On delivery | Email | Styling guide, outfit inspiration |
| Fit check-in | Day 3 post-delivery | Email | "How does it fit?" — Easy return/exchange CTA |
| Review request | Day 10-14 post-delivery | Email | Fit-specific questions, photo incentive |
| Review follow-up | Day 17-21 | Email | Non-responders, emphasize helping other shoppers |
| "Complete the look" | Day 14-21 | Email | Complementary pieces, accessories |
| New arrivals / seasonal | 45-60 days | Email | Category-relevant new products |
| Sale / clearance alert | Opportunistic | Email + SMS | Items in browsed/purchased categories |

### Electronics & Gadgets

**Consumption cycle:** 12-36 months, accessory purchases more frequent.

| Touchpoint | Timing | Channel | Notes |
|---|---|---|---|
| Order confirmation | Immediate | Email | Compatibility checklist, what's in the box |
| Shipping confirmation | On shipment | Email | Setup preparation steps |
| Delivery confirmation | On delivery | Email | Quick-start guide link, video tutorial |
| Setup support | Day 1 post-delivery | Email | "Need help setting up? Here's how" |
| Tips & features | Day 7 post-delivery | Email | "5 features you might not know about" |
| Review request | Day 14-21 post-delivery | Email | Technical detail prompts, comparison angles |
| Review follow-up | Day 21-28 | Email | Non-responders only |
| Accessories cross-sell | Day 14-30 | Email | Compatible accessories, protection plans |
| Software/firmware update | Ongoing | Email | Keep engagement with product updates |
| Upgrade cycle | 12-24 months | Email | Trade-in offers, new model announcements |

### Home & Furniture

**Consumption cycle:** Varies widely, 3-12 months between purchases.

| Touchpoint | Timing | Channel | Notes |
|---|---|---|---|
| Order confirmation | Immediate | Email | Delivery scheduling info, room prep tips |
| Shipping confirmation | On shipment | Email | Assembly requirements, tools needed |
| Delivery/installation | On delivery | Email + SMS | Assembly guide, professional installation offer |
| Settling-in check | Day 7 post-delivery | Email | Care instructions, "how does it look?" |
| Review request | Day 14-21 post-delivery | Email | Room photo incentive, style rating |
| Review follow-up | Day 21-28 | Email | Non-responders only |
| "Complete the room" | Day 21-30 | Email | Complementary furniture, decor pieces |
| Seasonal refresh | Quarterly | Email | Seasonal collections, styling inspiration |
| Care / maintenance | Every 6 months | Email | Product-specific maintenance tips |

---

## Send Time Optimization

### Best Send Times by Channel

**Email:**
- Transactional (confirmation, shipping): Send immediately — timing is event-driven
- Marketing (reviews, cross-sell): Tuesday-Thursday, 10am-2pm local time
- Promotional (sales, discounts): Tuesday or Thursday, 10am local time
- Weekend sends: Lower open rates but potentially higher conversion for leisure shoppers

**SMS:**
- Delivery alerts: Send immediately — these are time-sensitive
- Marketing SMS: Tuesday-Friday, 10am-7pm local time
- Never send SMS before 9am or after 9pm local time
- Limit to 4-6 SMS per month to avoid opt-outs

### Frequency Caps

| Time Window | Maximum Emails | Maximum SMS | Notes |
|---|---|---|---|
| Per day | 2 | 1 | Transactional emails exempt from cap |
| Per week | 4 | 2 | Include newsletters in count |
| Per month | 12 | 6 | Adjust based on engagement tier |

---

## Suppression Rules

### Always Suppress When:
- Customer has an open support ticket (suppress marketing, allow transactional)
- Return or exchange is in progress (suppress review requests and cross-sell)
- Customer has unsubscribed from marketing (allow transactional only)
- Order was cancelled or refunded (suppress entire post-purchase flow)
- Customer made a new purchase (restart journey from new order confirmation)
- Customer left a negative review (route to support, suppress cross-sell for 30 days)

### Engagement-Based Adjustments:
- **Highly engaged** (opens 80%+ of emails): Standard timing, full sequence
- **Moderately engaged** (opens 30-80%): Standard timing, skip optional touchpoints
- **Low engagement** (opens <30%): Extend timing by 50%, reduce to essential touchpoints only
- **Unengaged** (no opens in 60 days): Sunset sequence before re-permission campaign
