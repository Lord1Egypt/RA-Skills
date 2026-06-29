# Diagnostics

## Funnel Math

Track the whole chain:

`spend -> impressions -> CPM -> link CTR -> clicks -> CPC -> opt-ins -> CPL -> bookings -> cost per booking -> shows -> cost per show -> sales -> CPA -> revenue -> gross profit -> net profit`

Core formulas:

- Impressions = ad spend / CPM * 1000
- Clicks = impressions * link CTR
- CPC = ad spend / clicks
- Leads = clicks * opt-in rate
- CPL = ad spend / leads
- Bookings = leads * booking rate
- Cost per booking = ad spend / bookings
- Shows = bookings * show rate
- Cost per show = ad spend / shows
- Sales = shows * close rate
- CPA = ad spend / sales
- ROAS = revenue / ad spend
- Net profit = revenue - ad spend - delivery costs - sales costs - overhead allocation

## Bottleneck Read

Low link CTR:

- The audience does not care about the message, the hook is too weak, the promise is unclear, or the creative fails in placement.
- First checks: first line, first 2 seconds, offer framing, who-it-is-for, one clear problem/emotion, proof cue, and CTA.
- Usually fix messaging before targeting.

High link CTR but poor opt-in:

- Traffic is curious but not committed, the ad set the wrong expectation, or the page fails to meet the ad's promise.
- Add specificity, disqualifying language, price/commitment cues where appropriate, and tighter message match.

Low opt-in:

- Page headline is usually the first suspect.
- Check above-the-fold outcome, proof, VSSL relevance, form friction, FAQs, testimonials, page speed, mobile layout, and whether the ad promised the same thing the page delivers.

Low booking rate:

- The booking step does not feel like the natural next action after the application.
- Fix the booking-page subheadline/CTA, explain what happens on the call, show available times, reduce scheduling friction, and make qualification feel beneficial to the lead.

Low show rate:

- The lead loses motivation after booking or was never committed.
- Improve confirmation-page copy, SMS/email/WhatsApp reminders, calendar invites, expectation setting, pre-call value, and lead-quality filters.
- Add reminders close to the call. The method strongly values a final reminder around 15 minutes before the call when practical.

Low close rate:

- First inspect sales process: discovery quality, whether the rep is consulting too early, tie-down questions, price framing, objection handling, and CRM hygiene.
- Only blame lead quality after reviewing call recordings/notes and confirming the sales process was followed.
- If objections repeat, chase them upstream into nurture, page proof, FAQs, or ad messaging.

## Decision States

Build:

- Funnel not live, no tracking, or too little data.
- Goal: launch a credible version quickly and start learning.

Hold:

- Sample size is too small, the sales cycle has not played out, or results are within acceptable range.
- Do not change everything at once.

Problem solve:

- A clear stage is below range or an outlier ad/ad set has enough spend and poor results.
- Change one major lever at a time where possible.

Let it run:

- CPA, net profit, sales capacity, and cash flow work.
- Increase budget gradually enough to keep fulfillment and sales quality stable.

## Sample Size Guardrails

- Prefer 7-30 day windows depending on budget, volume, and sales cycle.
- For cold campaigns, judge creative after enough spend to give Meta a fair chance; exact thresholds depend on CPA and budget.
- Avoid overreacting to one good or bad day.
- Compare the actual cash cycle, not only in-platform attribution.

## Upstream Questions

Ask these when diagnosing:

- What did the ad promise, and what did the next page actually deliver?
- What type of person would this hook attract or repel?
- Which objections keep appearing on calls?
- Which application answers predict no-shows, poor fit, refunds, or complaints?
- Are rejected/unqualified leads being counted as success events?
- Is the calendar slot being protected for people likely to show?
- Which metric improved at the cost of a downstream metric?
