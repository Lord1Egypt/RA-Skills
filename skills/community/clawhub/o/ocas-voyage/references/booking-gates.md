# Booking Gates

Checklist that must pass before Voyage presents any option as "ready to book."

## Required before any booking recommendation

- [ ] Price re-checked (not just search result — verified on booking page)
- [ ] All mandatory fees surfaced (resort fees, taxes, cleaning)
- [ ] Cancellation terms stated clearly (deadline, refund amount)
- [ ] Inventory confirmed as available (not just "last checked")
- [ ] User has explicitly approved spending money

## Marriott Strider bookings

- [ ] `marriott.search_hotels` result is current (run within last 15 minutes)
- [ ] Bonvoy points redemption value explained if award night
- [ ] Elite upgrade availability confirmed separately if requested
- [ ] `voyage.book` never called without explicit user "yes, book this"

## Expedia / web-mode bookings

- [ ] Candidate page opened and verified (not just search result)
- [ ] Package contents listed (what's included, what's not)
- [ ] Deeplink or booking URL is fresh (not cached from a prior session)

## Never do this

- Present a search result price as the final total
- Auto-book without explicit approval
- Treat a held rate as permanent — it expires
- Combine Expedia and Marriott pricing in the same total without labeling sources
