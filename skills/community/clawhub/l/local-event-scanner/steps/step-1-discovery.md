# Step 1: Discovery

Discover candidate events from user-provided or public sources.

## Inputs

- Source priorities from `skills/event-scanner/assets/sources.md`.
- Geography and availability guidance from `skills/event-scanner/references/availability-rules.md`.
- Any date window or topic requested by the user.

## Procedure

1. Add `event-scanner-discovery` to the current run note's `Skills used` list before discovery work starts.
2. Resolve the scan location from the user request and `skills/event-scanner/assets/sources.md`; if the user did not specify a location, use the configured default location.
3. Check primary sources for the requested location first when they exist.
4. If the requested location has no primary sources, or is not a configured standard location, use public exploration for that location and record that source coverage is exploratory.
5. Use public pages and source links wherever possible.
6. Preserve evidence for every candidate event.
7. Prefer concise candidate notes over exhaustive scraping.
8. Use non-primary sources only as supplemental evidence or one-off discovery; do not propose or log new primary sources during normal scans.
9. Prefer public event information.
10. Update the current run note's `Context` with the resolved location and sources checked.
11. Replace the run note's `Candidate Events` placeholder with concise candidate notes or a short discovery summary.

## Candidate Event Shape

```md
## Event Title

- Date/time:
- Venue/location:
- Source:
- Price/ticket info:
- Short description:
- Why it may be relevant:
- Missing details:
- Confidence:
```

## Output

Return candidate events with source links and confidence, usually a minimum of 8 events unless the request is very niche. Do not produce the final ranked shortlist unless also running step-4-shortlist-review.

When starting this step, explicitly say: "[Step 1: Discovery]"
