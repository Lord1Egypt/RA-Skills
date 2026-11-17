---
name: live-events-ticketing-research
description: Research public StubHub and SeatGeek event calendars and resale-price snapshots. Use for location, category, performer, or venue ticket-market comparisons; not for purchases, bids, or primary-ticket checkout.
---

# Live-event ticketing research

Research public, read-only secondary-market listings from StubHub and
SeatGeek. Treat every price and availability result as a timestamped snapshot,
not an offer, reservation, or guaranteed inventory.

## Discover and resolve events

- Start with SeatGeek `/seatgeek/search?q=...&limit=1..50` for a named event,
  performer, or venue. Use returned provider IDs only with the matching
  SeatGeek endpoints: `/seatgeek/event?id=...`, `/seatgeek/performer-events`,
  or `/seatgeek/venue-events`. `/seatgeek/categories` supplies taxonomy IDs
  for `/seatgeek/events-by-category`; `/seatgeek/cities` supplies curated
  coordinates for `/seatgeek/events-near`. These page indexes are one-based
  and `per_page` is 1–50.
- For StubHub geographic discovery, pass valid `lat` and `lon` to
  `/stubhub/explore`, optionally with `from`, `to`, price bounds, or category
  filters. Dates accept RFC3339 or a bare `YYYY-MM-DD`; the default window is
  now through 14 days later. `/stubhub/categories` requires the same location
  and is the discovery source for `category_id` in `/stubhub/category-events`.
- Use `/stubhub/trending` and `/stubhub/trending-events` only as currently
  featured discovery feeds. For a performer or venue schedule, carry both the
  real slug and numeric ID from a returned canonical URL into
  `/stubhub/performer-events` or `/stubhub/venue-events`; do not construct or
  mix identifiers. StubHub feed pages are one-based. `include_parking_passes`
  can add parking-only entries, so label them separately from admission.

## Compare responsibly

- Verify matches using performer/event name, venue address or city, local date,
  and start time. Preserve each provider's event ID and canonical URL. Normalize
  a local date/time only when its timezone or offset is supplied; keep TBA/TBD
  or date-only timing unknown rather than assuming UTC.
- SeatGeek `/seatgeek/event` provides a secondary-market aggregate snapshot
  (listing/ticket counts and low/average/median/high prices), not individual
  seat listings. StubHub discovery/schedule results provide starting-price
  signals, not a complete inventory view. Do not infer a section, row, exact
  seat, quantity, accessibility feature, transfer method, or ticket guarantee
  when it is absent.
- These sources are resale marketplaces. Distinguish their listed or aggregate
  secondary prices from primary-market face value and official availability;
  neither establishes what an official seller has in stock. Use a separately
  scoped primary-ticket source when that comparison is needed, and keep source,
  market type, and collection time visible.
- Retain the currency returned by the source. A starting/aggregate price may
  exclude fees, taxes, delivery, or other checkout charges; never call it an
  all-in total or combine it with a fee-inclusive price from another source.

## Report

Return a dated snapshot table with provider, resale status, event/provider ID,
canonical URL, normalized-but-source-faithful venue and local time, price field
meaning, currency, availability/listing signal, and an `observed_at` timestamp
with timezone. Report empty feeds as no results for that query/window, not
proof that the event is sold out or unavailable. This skill performs no
authentication, ticket purchase, bid, hold, checkout, account action, or
availability guarantee.
