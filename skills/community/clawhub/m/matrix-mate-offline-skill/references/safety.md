# Safety Boundary

This skill is local-first and read-focused.

## What it may do

- Parse ITA Matrix itinerary links with the local Matrix Mate app
- Accept manual JSON plus fare rules fallback input
- Return discrepancy-aware trip output, exports, and future booking intent data
- Use browser automation to search ITA Matrix and capture a resulting itinerary URL

## What it must not do

- Book tickets
- complete payment flows
- bypass CAPTCHA or anti-abuse measures
- claim live fare guarantees
- invent missing fare rules, validation states, or booking outcomes

If Matrix Mate cannot verify a result, the skill should say so plainly and fall back to manual input guidance.
