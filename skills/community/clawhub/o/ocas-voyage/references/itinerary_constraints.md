# Itinerary Constraints

## Feasibility Rules

All itinerary days must pass these logistics feasibility checks:

1. **Travel time between locations** — Account for realistic transit time between activities. Do not schedule activities in different cities on the same day unless flight/train timing allows.

2. **Operating hours** — Never present uncertain operating hours as confirmed. If hours are unknown, flag as "verify before going."

3. **Dietary constraints** — All food recommendations must respect the traveler's dietary requirements (vegetarian, vegan, kosher, halal, allergies).

4. **Pace matching** — Respect the user's pace preference:
   - Relaxed: 2-3 activities per day with long breaks
   - Moderate: 3-4 activities with reasonable transit
   - Intense: 5+ activities, optimized routing

5. **Budget awareness** — Surface cost implications throughout. Never present a listing price as booking-final. Always include taxes + mandatory fees.

6. **Booking gate** — Never present an option as "ready to book" without:
   - Price re-check complete
   - Cancellation terms stated
   - Explicit user approval

7. **Availability honesty** — Never present uncertain availability as confirmed fact. Flag all unverified availability.

## Constraint Violation Handling

- If a recommendation violates a stated constraint, do not present it as a primary option
- If no options satisfy all constraints, surface the trade-off explicitly
- Never silently drop constraints to produce more results
