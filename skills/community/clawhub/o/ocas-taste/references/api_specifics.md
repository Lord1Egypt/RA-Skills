# API Specifics

## Gmail API

- Query syntax: space = AND, OR must be uppercase, date filters use `after:` not `since:`.
- The `from:` operator matches partial domains: `from:@opentable.com` matches all OpenTable emails.
- Rate limit: 250 quota units per user per second. A `messages().list()` costs 5 units, `messages().get()` costs 1 unit.
- Pagination: always check `nextPageToken` — a single query can return hundreds of results.

## Google Calendar API

- `calendarList().list()` returns all calendars the user has access to, including shared ones.
- `events().list()` requires `singleEvents=true` to expand recurring events into individual instances.
- Time format: RFC 3339 (`2024-01-15T00:00:00-08:00`). Always include timezone offset.
- The `accessRole` field determines write access: `owner` and `writer` can create events; `reader` and `freeBusyReader` cannot.

## Google Places API (via Styx)

- Text search endpoint: `places:searchText` — best for natural language queries like "Italian restaurant in Mission District".
- Nearby search: `places:searchNearby` — best when you have coordinates.
- Rate limit: 100 requests/second on the free tier.
- Response includes `displayName`, `formattedAddress`, `priceLevel`, `rating`, and `types` — map these to taste attributes per `references/enrichment.md`.