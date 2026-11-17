# SevenRooms

**Status:** ✅ Production
**Last tested:** 2026-05-25
**Method:** Public widget API (no auth) for availability; browser automation for booking

---

## Overview

SevenRooms provides a **public widget API** that returns full availability data without authentication. This is the preferred method for availability checks.

For **booking**, there is no customer-facing REST API. Booking is done through browser automation on the customer widget page at `/explore/{venue}/reservations/create/search/`.

**Important:** The authenticated API at `api.sevenrooms.com` is for **merchants/venues only** (OAuth client credentials). It cannot be used for customer bookings.

**Key insight:** The public widget API at `api-yoa/availability/widget/range` returns complete, real-time availability data — time slots, seating types, duration, policies, pacing limits, and credit card requirements. Earlier documentation incorrectly claimed it returned empty arrays.

---

## Public Widget API (No Auth Required)

**Endpoint:** `GET https://www.sevenrooms.com/api-yoa/availability/widget/range`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `venue` | string | Venue slug from the booking URL (e.g. `fiorellanoe` from `sevenrooms.com/explore/fiorellanoe/...`) |
| `time_slot` | string | Preferred time in HH:MM (24h format), e.g. `19:15` |
| `party_size` | int | Number of guests |
| `halo_size_interval` | int | Always `16` |
| `start_date` | string | Start date in YYYY-MM-DD |
| `num_days` | int | Number of days to scan (1-30) |
| `channel` | string | Always `SEVENROOMS_WIDGET` |

**Response structure:**
```json
{
  "status": 200,
  "data": {
    "availability": {
      "2026-06-01": [
        {
          "name": "Dinner Mo-Th",
          "shift_category": "DINNER",
          "is_closed": false,
          "duration_minutes_by_party_size": {"1": 75, "2": 75, "3": 75, "4": 75, "5": 90, "6": 90, "7": 90, "8": 90, "9": 90, "10": 105, "-1": 105},
          "times": [
            {
              "type": "book",
              "time": "5:00 PM",
              "time_iso": "2026-06-01 17:00:00",
              "access_persistent_id": "ahNzfnNl...",
              "public_time_slot_description": "Main Dining Room",
              "duration": 75,
              "is_held": false,
              "pacing_limit": 14,
              "pacing_covers_remaining": 14,
              "require_credit_card": false,
              "cc_party_size_min": 7,
              "default_service_charge": 10.0,
              "default_gratuity": 10.0,
              "cancellation_policy": "We ask that any cancellation...",
              "policy": "Thank you for your reservation..."
            }
          ]
        }
      ]
    }
  }
}
```

**Slot availability:** A slot is available when `type == "book"` AND `access_persistent_id` is not null.

---

## Implementation

**File:** `scripts/sevenrooms.py`

### Availability check (no auth):
```bash
python3 sevenrooms.py check --venue fiorellanoe --date 2026-06-01 --party-size 2
python3 sevenrooms.py check --venue fiorellanoe --date 2026-06-01 --party-size 2 --num-days 7
python3 sevenrooms.py check --venue fiorellanoe --date 2026-06-01 --party-size 2 --start-time 19:00 --end-time 21:00
python3 sevenrooms.py check --venue fiorellanoe --date 2026-06-01 --party-size 2 --seating "Bar"
python3 sevenrooms.py check --venue fiorellanoe --date 2026-06-01 --party-size 2 --json
```

### Book (browser automation via Playwright):
```bash
python3 sevenrooms.py book --venue fiorellanoe --date 2026-07-15 --time "7:00 PM" \
    --party-size 2 --first-name <operator> --last-name <operator-last> \
    --email owner@example.com --phone "+141****1234"

# Headed mode (visible browser) for debugging:
python3 sevenrooms.py book --venue fiorellanoe --date 2026-07-15 --time "7:00 PM" \
    --party-size 2 --first-name <operator> --last-name <operator-last> \
    --email owner@example.com --phone "+141****1234" --headed
```

---

## Tested: 2026-05-25

**Restaurant:** Fiorella (fiorellanoe)
**Result:** ✅ Working

**Sample availability for June 1, 2026 (party of 2):**
- 5:00 PM – 5:45 PM: Main Dining Room (75min duration)
- 6:00 PM – 8:30 PM: Main Dining Room (90min duration)
- 15 slots per day, 45 slots across 3 days

**Time filtering:** ✅ `--start-time 19:00 --end-time 20:30` correctly returns 7 slots (7:00 PM – 8:30 PM)

---

## Key Findings

1. **Public widget API works** — Returns full availability with no auth required
2. **Rich data per slot** — Seating type, duration, cancellation policy, CC requirements, service charges, gratuity, pacing limits
3. **Duration varies by party size** — Check `duration_minutes_by_party_size` in the shift data
4. **CC required for large parties** — `cc_party_size_min` indicates when credit card is required
5. **Shift categories** — LUNCH, DINNER, etc. available in shift data
6. **Closed dates** — `is_closed: true` or empty availability array
7. **No customer booking API** — Must use browser automation for booking; `api.sevenrooms.com` is merchant-only

---

## Booking Flow (Browser Automation)

The customer booking flow on SevenRooms:

1. Navigate to `https://www.sevenrooms.com/explore/{venue}/reservations/create/search/`
2. Widget loads availability from the public widget API
3. Customer selects party size
4. Customer selects date (calendar picker)
5. Customer clicks on a time slot button
6. Customer fills in guest details (first name, last name, email, phone)
7. Customer clicks "Book" / "Reserve" / "Confirm" button
8. Confirmation page shows reservation reference code

The Playwright automation follows these steps. A screenshot is saved for verification.

---

## DOM Structure

**Date picker:**
```html
<button>Date Mar 30</button>
<!-- Opens calendar modal -->
<td>5</td> <!-- Click to select date -->
```

**Time slots:**
```html
<button>7:00 PM Bar Table</button>
<button disabled>8:00 PM Bar Table</button>
```

**Guest detail inputs:**
```html
<input name="first_name" placeholder="First Name">
<input name="last_name" placeholder="Last Name">
<input name="email" type="email" placeholder="Email">
<input name="phone" type="tel" placeholder="Phone">
```

---

## Rejected Methods

| Method | Result |
|--------|--------|
| Direct HTTP without proper params | 400 Bad Request — `time_slot` param is required |
| `api.sevenrooms.com` for customer booking | Merchant-only API, requires venue OAuth credentials |
| Headless without stealth | May trigger Cloudflare; use `--headed` for bot-blocked venues |

---

## References

- Public widget: `https://www.sevenrooms.com/api-yoa/availability/widget/range`
- Booking page: `https://www.sevenrooms.com/explore/{venue}/reservations/create/search/`
- Community reference: https://github.com/jasonpraful/sevenrooms
- MCP server reference (merchant API): https://github.com/csnkarthik/seven-rooms-mcp-v2