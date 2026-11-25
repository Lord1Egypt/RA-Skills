---
name: hotel-rate-watcher
description: Watch Google Hotels rates and get alerted only when a nightly price drops or hits a target. Use when the user wants hotel price tracking, rate-drop alerts for a destination and dates, or a one-off hotel search with structured rates. Runs the magnova/hotel-price-watch Actor through the Apify plugin for OpenClaw; hotel records cost $0.002 and drop alerts $0.02 on the user's own Apify account.
version: 1.0.0
homepage: https://apify.com/magnova/hotel-price-watch
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# Hotel Rate Watcher

Hotel rates move daily, and nobody wants to re-check the
same stay by hand. This skill registers rate watches on
destinations and dates the user cares about and, on each
check, reports only what changed: properties whose nightly
rate fell, and the first moment a stay's lowest rate reaches
the user's target price. It can also run a plain one-off
search.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not scrape Google Hotels
yourself and do not substitute another source.

**Cost, stated plainly:** the Actor charges $0.002 per
hotel record and $0.02 per price-drop alert, no start fee.
A watch's first check delivers the current properties as
baseline records (about $0.04 for 20 results); later checks
charge nothing unless a rate actually drops. A daily watch
on one stay typically costs a few cents a month. The Actor
reads public Google Hotels data only — no login, no
booking.

## Setup (first run only)

Ask the user for: the destination (a city, area or
landmark, e.g. "New York" or "Dubai Marina"), check-in and
check-out dates, and optionally a target price per night.
Rates are priced at Google's standard occupancy (2 guests,
1 room). Store the watch input so later checks reuse it
exactly — a watch is identified by destination, dates and
currency, so changing any of them starts a new baseline.

## Workflow

**Register or check a watch** — call the Actor
`magnova/hotel-price-watch` with:

```json
{
  "searches": [{"destination": "New York", "checkInDate": "2027-06-15", "checkOutDate": "2027-06-17"}],
  "mode": "watch",
  "targetPricePerNight": 150,
  "maxResultsPerSearch": 20
}
```

**One-off search** — same input with `"mode": "search"`.

Reading the results:

- `BASELINE` records appear only on a watch's first check.
  Summarize the cheapest few and the lowest nightly rate,
  and tell the user the watch is set.
- `PRICE_DROP` records carry `previousPricePerNight`,
  `dropAmount` and `dropPercent` — report the property,
  the new nightly rate and the drop, with the record's
  `googleHotelsUrl`.
- `TARGET_HIT` means the stay's lowest nightly rate
  reached the target — lead with it.
- A check that returns only a `SUMMARY` record means
  nothing changed: say so in one line, or stay silent if
  the user asked for alerts only.
- `ERROR` records name the search that could not be
  checked; mention it and retry on the next scheduled
  check.

## Scheduling

Offer to run the watch check on a daily cadence (the user's
own scheduler or cron). Rates for far-out dates move
slowly; daily is plenty, twice daily for check-ins inside
a month.
