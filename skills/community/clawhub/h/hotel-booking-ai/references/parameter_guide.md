# B2B Booking Skill - Parameter Reference

## Region IDs (HTS Regions)

**China:**
- `569` - Beijing
- `2862` - Shanghai
- `765` - Zhengzhou
- `794` - Chongqing
- `3045` - Shenzhen
- `1328` - Hangzhou
- `3489` - Wuhan

**Asia:**
- `174` - Singapore
- `575` - Bangkok
- `2446` - Osaka
- `3263` - Tokyo
- `20994` - Bali

**Europe:**
- `1918` - London
- `2481` - Paris
- `2736` - Roma
- `514` - Berlin

*Note: Region IDs are HTS-specific identifiers. Use `/static/v2/region/fuzzy?keyword=xxx` API to search for more regions.*

---

## Date Format Rules

All date parameters must use ISO 8601 format: **YYYY-MM-DD**

Examples:
- ✅ `2026-03-25` (March 25, 2026)
- ✅ `2026-12-31` (December 31, 2026)
- ❌ `03/25/2026` (incorrect format)
- ❌ `2026-3-25` (missing leading zero on month)
- ❌ `25-03-2026` (day-first format)

Minimum lead time varies by property but typically:
- Search: Can query current date or future
- Booking: Recommend 24-48 hours in advance

---

## Currency Codes

Standard ISO 4217 currency codes:
- `CNY` - Chinese Yuan (default for China region)
- `USD` - US Dollar
- `EUR` - Euro
- `GBP` - British Pound
- `JPY` - Japanese Yen

*The system normalizes all quotes to the configured default currency.*

---

## Hotel Pricing Tiers

Typical room type hierarchy by price:
1. **Standard Room** - Base price, typically no view
2. **Deluxe Room** - Enhanced amenities, partial view
3. **Suite** - Large space, premium amenities
4. **Executive Suite** - Top tier, concierge included

Prices vary significantly by:
- Region (tier-1 cities > tier-2 > tier-3)
- Season (peak season June-Aug, Dec; off-season Oct-Nov)
- Day of week (weekends typically higher)
- Lead time (last-minute bookings premium)

---

## Guest Name Handling

The system automatically parses full names into first/last components:

✅ **Supported formats:**
- "John Smith" → first: "John", last: "Smith"
- "Li Ming" (Chinese name) → Auto-converts to pinyin for booking
- "Jean-Claude Van Damme" → Handles hyphenated names
- "Wang Hongwei" → Handles space-separated Chinese names

⚠️ **Best practice:**
- Provide full legal name as it appears on ID
- For Chinese guests, use full Chinese name; system handles pinyin conversion
- For compound surnames, provide in standard format

---

## Error Messages

Common error responses and meanings:

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid region ID" | Region doesn't exist | Verify region_id with admin |
| "No hotels found" | Region exists but no inventory | Try different dates or region |
| "Invalid date format" | Date not YYYY-MM-DD | Reformat date string |
| "Room not available" | Sold out for selected dates | Try adjacent dates or different room type |
| "Rate check failed" | Rate no longer valid | Run check_room_availability again |
| "Booking creation failed" | Guest info invalid or system error | Verify guest name format |

---

## Order Status Reference

| Status | Meaning |
|--------|---------|
| `UNPAID` | Booking created, payment not yet made |
| `PENDING` | Payment received, waiting for hotel to confirm |
| `CONFIRMED` | Hotel confirmed, booking is guaranteed |
| `CANCELLED` | Booking has been cancelled |
| `CONFIRM_FAILED` | Hotel confirmation failed, contact support |

> **Important**: `PENDING` means the payment was successful and the hotel is processing confirmation — do NOT tell the user to pay again.

---

## Authentication

This skill uses AgentAuth for identity verification. Your `user_key` is stored locally in `{baseDir}/user_key.txt` and passed automatically as the `user_key` parameter on every tool call.

**Get your user key:**
1. Visit https://aauth-170125614655.asia-northeast1.run.app/dashboard
2. Log in with Google
3. Copy your `user_key` (format: `uk_xxxxxxxx`)

On first use, the skill will prompt you to enter it. It is then saved for all future sessions.

---

## Workflow Decision Tree

```
User request for booking?
├─ Search? → search_hotels with region + dates
│  └─ Got hotel → query_room_rates with hotel_id
│     └─ Compare rates → check_room_availability for specific room
│        └─ Available? → create_booking with guest info
│           └─ Success → query_booking for confirmation
│
├─ Check status? → query_booking with booking_id
│
├─ Cancel booking? → confirm booking_id, then cancel_booking
│
└─ Need confirmation? → query_booking
```

---

## Performance Notes

- **Search latency:** ~1-2 seconds (network dependent)
- **Rate queries:** ~500ms per hotel
- **Availability checks:** Real-time, ~300ms
- **Booking creation:** 2-5 seconds (includes confirmation)

For bulk operations, consider rate-limiting to avoid API throttling.
