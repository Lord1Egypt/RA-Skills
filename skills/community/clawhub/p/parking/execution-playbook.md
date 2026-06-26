# Execution Playbook - Parking Radar

Pick the smallest workflow that fits the task.

## 1. Find Parking Nearby Now

1. Lock city, neighborhood, or destination.
2. Ask whether the user needs a guaranteed booking or only the fastest likely option.
3. Start with maps plus the strongest local provider from `provider-registry.md`.
4. Return 2 to 4 options with price model, walking distance, opening status, and whether the result is reservation, payment, or discovery only.

## 2. Pre-Book for Airport, Station, or Event

1. Get arrival and exit window, vehicle type, and budget.
2. Prefer reservation-first providers over payment-first city apps.
3. Verify shuttle, walking time, cancellation policy, height limit, and in-and-out privileges.
4. Label each option as official operator, marketplace, or host inventory.

## 3. Repeated Parking in a Home City

1. Ask whether the user wants local memory.
2. Save recurring venues, trusted operators, and no-go patterns only after approval.
3. Keep favorites separate from unverified findings.
4. Promote repeated discoveries into `cities.md` or `favorites.md`.

## 4. Research a New Country or City

1. Identify whether the market is reservation-first, payment-first, or operator-native.
2. Start from `provider-registry.md`, then confirm with official operator or app pages.
3. Record only what is reusable: dominant providers, public data sources, and booking limitations.
4. If nothing credible appears, fall back to maps plus official venue parking information.

## 5. API or Product Research

1. Separate public APIs, partner APIs, and no-public-API cases.
2. Use `api-notes.md` for evidence, not guesswork.
3. Distinguish facility discovery, pricing, booking, and occupancy APIs because providers rarely expose all four.
4. Stop before claiming live booking automation if access appears partnership-only.

## Output Pattern

Prefer this response shape:
- best option for the stated goal
- fallback options
- what is verified
- what is not verified yet
- one next action

## Availability Language

Use these exact meanings:
- `Guaranteed reservation`: provider confirms a booking path and inventory for the requested window
- `Reservable now`: a live booking flow exists, but full booking success still depends on checkout
- `Payment app only`: the app helps pay after the user finds a bay
- `Discovery only`: useful for location and facility details, not for committing a space
