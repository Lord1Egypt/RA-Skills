# Booking Workflow

1. **Venue lookup** — Check `venues.jsonl` for a config match. If no match, run `spot.platform.probe` on the provided URL.
2. **Availability check** — Use the platform-appropriate method (see Platform Support below). Each platform's script, selectors, edge cases, and known limitations are documented in `references/platforms/<platform>.md`.
3. **Bot detection** — After page load, run `detect_bot_block()`. If blocked, trigger VPN workflow and retry.
4. **Conflict check (Sands)** — If Sands is present, write a conflict-check request to `{agent_root}/commons/data/ocas-sands/intake/{check_id}.conflict.json`. If Sands reports a conflict, surface it and ask for confirmation. If Sands is absent or unresponsive, proceed.
5. **Slot selection** — Present available dates/times to user. Wait for confirmation.
6. **Booking** — Execute booking flow using `human_click()` and `human_type()` for all interactions. Capture confirmation reference.
7. **Record** — Write BookingRecord to `bookings.jsonl`. Emit Signals to Elephas. Write InsightProposal to Vesper. If Voyage itinerary matches, append Travel Context. If Sands is present, write calendar event request. Sands write failure does NOT cancel the external booking.