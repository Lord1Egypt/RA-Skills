# Scoring Rubric

Use explainable ranking rather than opaque numeric scoring. The final output should make it clear why each event is recommended.

## Ranking Factors

Prioritize events using these factors:

- Fit with `skills/event-scanner/assets/taste-profile.md`.
- Strength of source evidence and event details.
- Practicality for the requested location, or the configured default location when none is requested.
- Novelty or surprise potential.
- Timing and likely energy required.
- Price and ticket friction when known.
- Calendar practicality when availability context is provided.
- Social, cultural, or personal interest signals.
- Confidence that the event is real and accurately described.

## Date Window Biases

Adjust practicality scoring based on how soon the requested window is:

- For requests covering the next 14 days, give a stronger preference to events that are short, easy to attend, and cheaper or free. One-evening, few-hour, drop-in, and low-commitment events should usually outrank multi-day, expensive, or high-planning events unless the fit is exceptional.
- For requests further in the future, allow longer, more expensive, higher-commitment, travel-adjacent, festival, retreat, workshop, and multi-day events to rank more highly when the fit is strong.
- When an event is high-fit but high-commitment in a near-term window, keep it eligible but explain the time, cost, registration, or preparation caveat clearly.

## Recommendation Labels

Use these labels in shortlists:

- Strong pick: highly aligned and practical.
- Worth considering: interesting, with manageable caveats.
- Maybe: promising but missing details or has clear friction.
- Skip for now: low fit, low confidence, or too much friction.

## Calendar Practicality

When calendar context is available, use it as a practicality signal:

- Open: event timing is practical; no calendar caveat needed unless other friction exists.
- Tight: keep the event eligible, but mention the squeeze or buffer issue.
- Conflict: lower the recommendation unless the event is exceptional; explain the conflict without storing private calendar details.

## Required Explanation

For each shortlisted event, include:

- Why it fits.
- What the caveat is.
- What to do next.
- Source link.
- Confidence level: high, medium, or low.

## Preference Learning

Do not suggest preference updates during normal scans. Check for taste-profile updates only after `steps/step-5-add-to-calendar.md` is followed. Send suggestions in chat only, and apply them only after approval.
