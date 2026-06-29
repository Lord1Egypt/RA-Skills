# Current Meta Setup Notes

Meta UI and product names change often. Treat these as durable setup intentions, then verify the current Ads Manager labels before giving click-by-click instructions.

## Campaign And Conversion Location

Meta supports multiple lead-generation routes:

- Instant forms inside Facebook/Instagram.
- Website forms or application pages.
- Click-to-message flows on Messenger, Instagram Direct, or WhatsApp.
- Call-focused lead ads for businesses that can handle live calls.

For high-ticket-ish service funnels, a website/application funnel often provides better education and qualification than low-friction instant forms. Instant forms can still be useful for volume, testing, or lower-consideration offers, especially if CRM feedback is strong.

Meta has promoted mixed lead strategies that combine instant forms and website forms. Recommend testing this only when the business can separate lead sources, measure quality, and follow up quickly.

## Advantage+ And Automation

Current Meta guidance pushes Advantage+ audience, placements, budget, and creative automation, especially for leads campaigns. Do not give blanket advice to disable all automation.

Use controls only for real business constraints:

- Geography served.
- Language.
- Legal or compliance restrictions.
- Offer-specific exclusions.
- Budget/capacity constraints.

Let creative, copy, and conversion feedback do more targeting work than narrow interest stacks. Interest targeting is increasingly a suggestion, not a complete control system.

## Signal Quality

Meta optimizes toward the events it can see. If it only sees cheap form submissions, it may find more cheap form submitters.

For quality lead generation:

- Track the lead event.
- Track booking/scheduled-call events.
- Track showed-call, qualified-lead, opportunity, sale, and customer value when practical.
- Feed qualified downstream outcomes back through CRM integrations or Conversions API.
- Do not send success events for disqualified leads.

Use the Meta Pixel with Conversions API where practical. Meta describes Conversions API as a direct connection from server, website platform, app, CRM, or offline sources to Meta's optimization and measurement systems. It can be used alongside the Pixel for better connection reliability and later-stage optimization.

## Pixel And CAPI Hygiene

When Pixel and Conversions API send the same event, deduplication must be handled correctly, usually through shared event IDs and consistent event names. Broken deduplication can inflate results and mislead optimization.

Minimum hygiene:

- Events fire on the right pages/actions only.
- Test events before launch.
- Use UTMs on ads.
- Compare platform results with CRM and bank/payment data.
- Exclude test/staging traffic.
- Verify event match quality where available.
- Preserve privacy, consent, and platform terms.

## Campaign Review

Review useful columns, not every available metric:

- Spend
- CPM
- Link CTR, not all-click CTR
- CPC
- Cost per lead
- Cost per booking/schedule
- Frequency
- Conversion rate by stage
- Quality/show/close metrics from CRM

Optimization habit:

- Use a consistent date range, often last 7-30 days depending on volume.
- Sort by spend to find where budget is actually going.
- Look for outliers with enough spend.
- Cut or revise poor performers; keep winners running; create new ads from winning ideas.

## Scaling

Scale only when:

- CPA is profitable after fulfillment and sales costs.
- Sales team can handle more calls.
- Calendar availability supports booking rate.
- Show rate and close rate remain acceptable.
- Cash flow can absorb the learning period.

Expect ROAS to decline as budget reaches colder audiences. Judge scale by net profit and capacity, not by preserving the prettiest ROAS.
