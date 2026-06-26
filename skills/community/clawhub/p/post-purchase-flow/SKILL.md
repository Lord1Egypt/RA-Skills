---
name: Post-Purchase Flow
description: Design the complete post-purchase customer experience from order confirmation through delivery and beyond, including transactional emails, shipping updates, unboxing moments, review solicitation, and repeat-purchase nudges.
---

# Post-Purchase Flow

The period between checkout and the next purchase is where most ecommerce brands either build lasting loyalty or silently lose customers. This skill designs the complete post-purchase experience architecture — every touchpoint from the order confirmation screen through delivery, unboxing, review solicitation, and the first cross-sell or replenishment nudge. Instead of treating transactional emails as an afterthought and review requests as a standalone automation, this skill weaves them into a cohesive journey that reinforces brand trust, reduces "where is my order" support tickets, creates shareable unboxing moments, and strategically times the next purchase prompt based on product consumption cycles and customer engagement signals.

---

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Confirmation email timing | Sent within 60 seconds of order | Sent within 5 minutes | Delayed beyond 10 minutes or batched |
| Shipping update frequency | Key milestones (shipped, out for delivery, delivered) plus proactive delay alerts | Shipped and delivered only | Single "your order has shipped" with no tracking context |
| Review request timing | 7-14 days post-delivery based on product category | Fixed 5-day delay for all products | Same day as delivery or 30+ days later |
| Unboxing experience design | Branded insert card with QR code linking to setup guide and social sharing prompt | Generic packing slip with return instructions only | No insert material at all |
| Cross-sell/replenishment timing | Based on product consumption cycle data and customer engagement signals | Fixed 30-day delay for all products | Immediate post-purchase or no follow-up at all |
| WISMO reduction strategy | Proactive shipping updates with estimated delivery windows and delay notifications | Basic tracking link in shipment email | No tracking information provided |

---

## Solves

- **High WISMO ticket volume**: Proactively communicates shipping status to reduce "where is my order" support inquiries by 40-60%
- **Low review collection rates**: Strategically times and incentivizes review requests to increase collection rates from under 2% to 8-15%
- **Poor repeat purchase rates**: Designs data-driven replenishment and cross-sell sequences that increase second-order rates by 20-35%
- **Weak brand recall post-checkout**: Creates memorable unboxing experiences with branded touchpoints that drive social sharing and word-of-mouth
- **Fragmented post-purchase communications**: Unifies transactional emails, SMS, and in-package touchpoints into a coherent customer journey
- **High return rates from unclear expectations**: Sets proper expectations through confirmation details and proactive shipping communication

---

## Workflow

### Step 1: Audit Current Post-Purchase Touchpoints

Map every existing communication a customer receives after placing an order. Document the sender, channel (email, SMS, push), timing, content, and conversion metrics for each touchpoint.

**Key actions:**
- Export all post-purchase automations from your ESP (Klaviyo, Omnisend, Mailchimp, Attentive)
- Review transactional email templates (order confirmation, shipping confirmation, delivery confirmation)
- Document any in-package materials (insert cards, samples, return labels)
- Pull metrics: open rates, click rates, review submission rates, repeat purchase rates, WISMO ticket volume
- Identify gaps where customers receive no communication for extended periods

**Output:** Complete touchpoint map with timing, channel, content summary, and performance metrics.

### Step 2: Design the Order Confirmation Experience

The order confirmation is the highest-opened email in ecommerce (typically 60-80% open rate). Design it to do more than confirm — it should build anticipation, set expectations, and begin the relationship.

**Key actions:**
- Include clear order details (items, quantities, prices, shipping method, estimated delivery)
- Add a "what happens next" timeline showing upcoming touchpoints
- Include a warm brand message that reinforces the purchase decision (reduce buyer's remorse)
- Add relevant cross-sell recommendations (complementary products, not competing ones)
- Provide direct links to order tracking, FAQ, and support
- Consider SMS confirmation for high-value orders

**Output:** Order confirmation email template with all required elements and conditional logic for order types.

### Step 3: Build the Shipping Communication Sequence

Design proactive shipping updates that keep the customer informed at every meaningful milestone. The goal is to eliminate the need for customers to contact support about order status.

**Key actions:**
- Configure notifications for: order processed, label created, shipped/picked up, in transit milestones, out for delivery, delivered
- Design proactive delay notifications that alert customers before they notice
- Include estimated delivery windows that update dynamically
- Create separate flows for domestic vs. international shipping
- Add carrier-specific tracking deep links (not just tracking numbers)
- Design a "delivery confirmed" email that transitions into the post-delivery experience

**Output:** Complete shipping notification sequence with templates for each milestone and delay scenarios.

### Step 4: Engineer the Unboxing Experience

Design the physical and digital unboxing experience that creates a memorable brand moment and drives social sharing.

**Key actions:**
- Design branded insert cards with clear CTAs (QR codes to setup guides, social sharing prompts, referral codes)
- Plan surprise-and-delight elements (samples, handwritten notes for high-value orders, stickers)
- Create a social sharing incentive (hashtag campaign, photo contest, user gallery)
- Design product setup or first-use guides for complex products
- Include return/exchange information in a non-prominent but accessible location
- Plan seasonal or campaign-specific insert variations

**Output:** Insert card designs, unboxing flow documentation, and digital companion content specifications.

### Step 5: Optimize Review Collection Strategy

Design a multi-channel review solicitation strategy that maximizes collection rates while maintaining authenticity and compliance.

**Key actions:**
- Determine optimal timing by product category (consumables: 7-10 days, apparel: 10-14 days, electronics: 14-21 days)
- Design the initial review request with low-friction submission (star rating first, then optional text)
- Create a follow-up sequence for non-responders (max 2 additional touches)
- Add photo/video review incentives (loyalty points, discount on next order)
- Implement review syndication to key platforms (Google, product pages, social)
- Design responses for negative reviews that route to support before public posting
- Ensure compliance with FTC guidelines and platform-specific review policies

**Output:** Review collection flow with timing rules, templates, incentive structure, and negative review handling process.

### Step 6: Design Cross-Sell and Replenishment Sequences

Create data-driven sequences that prompt repeat purchases at the optimal time based on product type, consumption patterns, and customer behavior signals.

**Key actions:**
- Categorize products by replenishment cycle (consumables: 30-90 days, durables: seasonal, fashion: trend-based)
- Build replenishment reminders with easy reorder functionality (one-click reorder, subscription conversion)
- Design cross-sell recommendations based on purchase history, browsing behavior, and category affinity
- Create "complete the set" campaigns for products that have complementary items
- Set up win-back triggers for customers who don't engage with replenishment emails
- A/B test timing, incentive levels, and product recommendation algorithms

**Output:** Replenishment and cross-sell automation flows with product category rules, timing logic, and recommendation criteria.

### Step 7: Measure, Iterate, and Optimize

Establish KPIs, implement tracking, and create a continuous optimization cadence for the entire post-purchase journey.

**Key actions:**
- Define primary KPIs: repeat purchase rate, time to second order, review collection rate, WISMO ticket reduction, NPS/CSAT
- Set up cohort tracking to measure journey effectiveness over time
- Create A/B testing calendar for subject lines, timing, incentives, and content
- Build dashboards that connect post-purchase engagement to lifetime value
- Establish monthly review cadence for performance analysis and optimization
- Document learnings and update playbook quarterly

**Output:** KPI dashboard, testing roadmap, and quarterly review template.

---

## Example 1: DTC Skincare Brand — Complete Post-Purchase Flow

**Context:** A DTC skincare brand selling $45 average order value products with a 60-day replenishment cycle. Current repeat purchase rate is 18%, WISMO tickets account for 35% of support volume, and review collection rate is 1.8%.

**Order Confirmation (Immediate):**
- Subject: "Your skin is going to love this ✨ Order #12847 confirmed"
- Content: Order details, expected delivery window (3-5 business days), "what happens next" timeline, skincare routine guide CTA
- SMS: "Thanks for your order! We'll text you when it ships. Track anytime: [link]"

**Shipping Sequence:**
- Shipped (Day 1-2): "Your order is on its way! 📦" — Tracking link, estimated delivery, "how to prep your skin" content
- Out for delivery (Day 3-5): "Arriving today! Here's your evening routine plan" — Last-mile tracking, product usage tips
- Delivered (Day 3-5): "Your order has arrived! 🎉" — Unboxing guide link, Instagram sharing prompt with branded hashtag

**Unboxing Experience:**
- Branded box with tissue paper in brand colors
- Insert card: "Your Glow-Up Starts Now" — QR code to personalized skincare routine based on products ordered
- Sample sachet of a complementary product (cross-sell seed)
- Sticker sheet for water bottles/laptops (brand awareness)

**Review Request (Day 12 post-delivery):**
- Subject: "How's your skin feeling? We'd love to hear!"
- Content: One-click star rating, photo upload incentive (100 loyalty points), link to full review form
- Follow-up (Day 19): "Quick reminder — your review helps others find their perfect routine"

**Replenishment (Day 50):**
- Subject: "Running low? Your reorder is one tap away"
- Content: One-click reorder button, 10% loyalty discount, subscription option (save 15% + never run out)
- SMS (Day 55): "Your [product] might be running low! Reorder with free shipping: [link]"

**Results target:** Repeat purchase rate 28% (+10pp), WISMO tickets reduced to 15% of volume, review collection rate 9%.

---

## Example 2: Home Goods Marketplace — Multi-Seller Post-Purchase Flow

**Context:** A curated home goods marketplace with 200+ sellers, average order value $120, mixed product categories (candles, ceramics, textiles). Challenge: maintaining brand consistency while supporting seller-specific messaging.

**Order Confirmation (Immediate):**
- Subject: "Order confirmed! Your [seller name] pieces are being prepared"
- Content: Order summary with seller details, split-shipment notice if multi-seller order, estimated delivery per seller
- Marketplace brand message + individual seller "about" snippet

**Shipping (Per Seller Shipment):**
- Shipment 1 shipped: "Your [seller] items are on their way!" — Seller story, care instructions preview
- Shipment 2 shipped: "[Second seller] just shipped your order" — Complete order tracking dashboard link
- All delivered: "Everything has arrived! Your home refresh is complete 🏡"

**Unboxing (Seller-Specific + Marketplace):**
- Marketplace-branded outer packaging with sustainability messaging
- Seller-specific inner wrapping with artisan story card
- Marketplace insert: "Share your styled space" campaign with #MarketplaceAtHome hashtag
- Product care guide specific to materials (ceramics, candles, textiles)

**Review Request (Day 10 post-delivery, per seller):**
- Subject: "How are you enjoying your [product] from [seller]?"
- Content: Seller-specific review (helps the artisan), marketplace review (helps other shoppers)
- Photo incentive: Feature in "Styled by Our Community" gallery

**Cross-Sell (Day 21):**
- Subject: "Complete your space — curated picks based on your style"
- Content: Recommendations from same seller + complementary sellers, "shop the look" editorial content
- Seasonal collection preview if applicable

**Results target:** Cross-seller repeat purchase rate 22%, review collection 11%, seller satisfaction score improvement.

---

## Common Mistakes

1. **Sending review requests too early** — Asking for reviews on delivery day before customers have used the product leads to shallow reviews and low response rates. Wait 7-21 days depending on product category.

2. **Treating transactional emails as afterthoughts** — Order confirmation and shipping emails have the highest engagement rates of any ecommerce email. Using plain-text templates without branding or strategic content wastes the best engagement opportunity.

3. **No proactive delay communication** — When shipments are delayed, waiting for customers to contact support creates frustration and distrust. Always notify customers of delays before they discover them.

4. **One-size-fits-all timing for all products** — A consumable supplement has a completely different replenishment cycle than a durable home good. Using the same timing for replenishment emails across all categories leads to irrelevant messaging.

5. **Overwhelming customers with too many emails** — Sending 8 emails in 5 days (confirmation, shipped, out for delivery, delivered, review request, cross-sell, referral, newsletter) creates fatigue. Space touchpoints and consolidate where possible.

6. **Ignoring SMS as a post-purchase channel** — Shipping updates and delivery confirmations have significantly higher engagement via SMS than email. Use SMS for time-sensitive updates and email for content-rich touchpoints.

7. **No negative review interception** — Sending dissatisfied customers directly to public review platforms without offering a private resolution path damages brand reputation. Route low ratings to support first.

8. **Forgetting about the physical unboxing** — Investing heavily in digital touchpoints while shipping products in plain brown boxes with no insert materials misses the most emotional moment in the customer journey.

9. **Static cross-sell recommendations** — Recommending the same bestsellers to every customer regardless of purchase history and browsing behavior feels impersonal and reduces conversion rates.

10. **Not measuring post-purchase journey holistically** — Tracking individual email metrics without connecting them to repeat purchase rates, lifetime value, and support ticket volume prevents meaningful optimization.

---

## Resources

- [Output Template](references/output-template.md) — Structured template for delivering post-purchase flow documentation
- [Email Timing Guide](references/email-timing-guide.md) — Comprehensive timing recommendations by product category and channel
- [Unboxing Design Guide](references/unboxing-design-guide.md) — Physical and digital unboxing experience design patterns
- [Quality Checklist](assets/quality-checklist.md) — 45-item checklist for post-purchase flow completeness
