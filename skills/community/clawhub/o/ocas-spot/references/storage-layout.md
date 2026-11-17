# Spot — Storage Layout

```
{agent_root}/commons/data/ocas-spot/
  config.json               — defaults (timezone, name, email, phone)
  venues.jsonl              — registered venues with platform configs
  bookings.jsonl            — booking history (past and upcoming)
  watch.jsonl               — watchlist records (active and inactive)
  intents.jsonl             — audit trail of booking intents
  evidence.jsonl            — audit evidence (screenshots, API responses, hashes)
  opentable-session.json    — OpenTable session state (gitignored)
  yelp/
    alias-cache.md          — name+location → Yelp alias/ID
    shortlists.md           — saved discovery sessions
    request-log.md          — redacted endpoint logs

{agent_root}/commons/journals/ocas-spot/
  YYYY-MM-DD/
    {run_id}.json
```

## Record Schemas

Full schema definitions with field types and validation rules: `references/schemas.md`.

**VenueRecord** — `venue_id`, `name`, `platform`, `booking_url`, `services[]`, `added_at`, `last_checked`

**BookingRecord** — `booking_id`, `venue_id`, `venue_name`, `service`, `datetime`, `status`, `confirmation_ref`, `booked_at`, `signal_emitted`

**WatchRecord** — `watch_id`, `venue_id`, `venue_name`, `platform`, `party_size`, `dates[]`, `date_range`, `time_window`, `priority`, `active`, `added_at`, `last_checked`, `last_found`