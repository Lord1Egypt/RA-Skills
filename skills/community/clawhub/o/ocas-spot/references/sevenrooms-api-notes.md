# SevenRooms API Research Notes

## Architecture: No Customer Booking API

SevenRooms has **no customer-facing REST API for booking**. The authenticated API at `api.sevenrooms.com` is for **merchants/venues only** (OAuth client credentials). As a customer, you cannot obtain these credentials.

Spot's SevenRooms integration uses two separate paths:

| Operation | Method | Auth |
|-----------|--------|------|
| **Availability** | Public widget API | None |
| **Booking** | Browser automation (Playwright) | N/A |

---

## Public Widget API (No Auth)

```
GET https://www.sevenrooms.com/api-yoa/availability/widget/range
  ?venue={slug}
  &time_slot={HH:MM}        # 24h format, e.g. 19:15
  &party_size={N}
  &halo_size_interval=16    # always 16
  &start_date={YYYY-MM-DD}
  &num_days={N}             # 1-30
  &channel=SEVENROOMS_WIDGET
```

**Key response fields per slot:**

| Field | Description |
|-------|-------------|
| `type` | `"book"` = bookable (filter on this) |
| `access_persistent_id` | non-null = available, null = unavailable |
| `time` | e.g. `"5:00 PM"` |
| `time_iso` | e.g. `"2026-06-01 17:00:00"` |
| `public_time_slot_description` | e.g. `"Main Dining Room"`, `"Bar Table"`, `"Patio"` |
| `duration` | Slot duration in minutes |
| `cancellation_policy` | Human-readable policy text |
| `require_credit_card` | Boolean |
| `cc_party_size_min` | Party size threshold for CC requirement |
| `default_service_charge` | Percentage (e.g. 10.0) |
| `default_gratuity` | Percentage (e.g. 10.0) |
| `pacing_limit` / `pacing_covers_remaining` | Pacing controls |

**Shift-level data:**

| Field | Description |
|-------|-------------|
| `shift_category` | `"DINNER"`, `"LUNCH"`, etc. |
| `duration_minutes_by_party_size` | Maps party size → duration |
| `is_closed` | Boolean |

---

## Venue ID Resolution

The public widget API uses the **venue slug** from the booking URL:
- URL: `https://www.sevenrooms.com/explore/fiorellanoe/reservations/create/search/`
- Slug: `fiorellanoe`

---

## Discovery: Widget API Works (Contradicts Prior Docs)

The pre-v2.6.0 `sevenrooms.md` stated:
> "Widget API returns empty arrays — Don't rely on `api-yoa/availability/widget/range`"

This was **wrong**. The public widget API returns full, rich availability data with no authentication required. Always test the widget API directly before assuming it doesn't work.

---

## Community References

- https://github.com/jasonpraful/sevenrooms — Working widget API client (Python)
- https://github.com/csnkarthik/seven-rooms-mcp-v2 — MCP server using merchant API (not usable for customer booking)
- https://github.com/omarshahine/restaurant-cli — Multi-platform CLI (no SevenRooms provider yet)
- https://github.com/ZenningAI/booking-sdk-ios — iOS SDK (merchant-facing)

---

## Testing

Tested against `fiorellanoe` (Fiorella restaurant):

| Date | Party Size | Slots | Notes |
|------|-----------|-------|-------|
| 2026-05-25 | 2 | 15/day | 75min (≤4 guests), 90min (5+ guests) |
| 2026-05-25 | 4 | 44/3 days | Time filtering confirmed |
| 2026-05-25 | 2 | 7 slots | `--start-time 19:00 --end-time 20:30` filter confirmed |

Rich metadata confirmed: seating types, duration, policies, charges, gratuity.