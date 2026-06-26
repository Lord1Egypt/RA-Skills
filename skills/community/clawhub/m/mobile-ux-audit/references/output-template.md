# Mobile UX Audit Report — Template

Use this format for audit deliverables. One document per audit, shared with the product and engineering teams.

## Executive summary

- **Store / property**: [name]
- **Date**: [YYYY-MM-DD]
- **Auditor**: [name]
- **Devices tested**: [iPhone XX, Pixel Xx, etc.]
- **Networks tested**: [Wi-Fi, 4G, 3G-throttled]

**Headline metrics (p75, last 28 days):**

- LCP: [Xs] — target ≤2.0s
- INP: [Xms] — target ≤150ms
- CLS: [X] — target ≤0.05
- Mobile conversion rate: [X%] vs. desktop [Y%]
- Mobile cart abandonment: [X%]

**Top-3 fixes**, in priority order:

1. [P0 fix] — estimated impact: [X% lift]
2. [P0 fix] — estimated impact: [X% lift]
3. [P1 fix] — estimated impact: [X% lift]

## Findings by priority

### P0 — blocks or significantly degrades checkout

For each finding, include:

- **Finding**: [one sentence description]
- **Screen / step**: [home / PDP / cart / checkout / payment]
- **Evidence**: [screenshot, metric, session recording ID]
- **Fix**: [concrete implementation]
- **Owner**: [team / role]
- **Estimated impact**: [X% lift, Y ms improvement]

Repeat per P0 finding.

### P1 — measurable conversion or engagement impact

Same structure as P0.

### P2 — polish and hygiene

Same structure as P0 and P1.

## Funnel walkthrough notes

Step-by-step notes from the in-device walk. Helpful for reviewers who didn't do the audit. Optional but valuable for the first audit of a store.

- **Home → category**: [notes]
- **Category → PDP**: [notes]
- **PDP → cart**: [notes]
- **Cart → checkout**: [notes]
- **Checkout → payment**: [notes]
- **Payment → confirmation**: [notes]

## Benchmarks and context

- Industry p75 mobile LCP for the store's category: [X s]
- Competitor mobile CVR estimate: [X%]
- Last audit date and change since: [delta]

## Appendix: raw data

- PageSpeed Insights link
- Search Console Core Web Vitals screenshot
- Session recording replays (list IDs, timestamps)
- Device spec list used

## Next review

Suggested next audit: [YYYY-MM-DD] (quarterly by default; sooner if a major launch lands).
