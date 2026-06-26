---
name: hotel-price-finder
version: 1.1.0
description: Compare hotel prices across Booking.com, Agoda, Trip.com in real-time. Free multi-OTA price comparison with direct booking links. No API key required.
tags: [travel, hotel, agoda, booking, price-comparison, trip, expedia, cheapest, deal]
env:
  - APIFY_API_KEY (optional - Agoda deep search with 22+ fields)
---

# Hotel Price Finder - Multi OTA

Compare real-time hotel prices across Booking.com, Agoda, Trip.com and more. No API key required.

## When to Use

Activate when user asks about hotel search, price comparison, cheapest booking site, or accommodation recommendations.

## Step 1: Parse Query

Extract: `destination` (required), `checkIn`/`checkOut` (required, YYYY-MM-DD), `adults` (default 2), `rooms` (default 1), `currency` (default USD), `maxBudget`, `limit` (default 10). If dates missing, ask the user.

## Step 2: Resolve Destination

### Xotelo Location Key

Xotelo uses TripAdvisor keys (`g{number}`). For unlisted cities, call:
```bash
curl -s "https://data.xotelo.com/api/search?q=DESTINATION&limit=5"
```

Common keys: Seoul=g294197, Busan=g297884, Jeju=g983296, Tokyo=g298184, Osaka=g298566, Kyoto=g298564, Bangkok=g293916, Phuket=g293920, Singapore=g294265, Bali=g294226, Kuala Lumpur=g298570, Hong Kong=g294217, Taipei=g293913, Da Nang=g298085, Ho Chi Minh=g293925, Hanoi=g293924, Cebu=g294261, Manila=g298573, Paris=g187147, London=g186338, New York=g60763

### Agoda City ID (for booking links)

```bash
curl -s "https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/1/1/0/en-us/?searchText=DESTINATION&origin=US" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```
Extract `ObjectId` where `PageTypeId == 5` and `SearchType == 1`.

Common IDs: Seoul=14690, Busan=17172, Tokyo=5085, Osaka=9590, Bangkok=9395, Singapore=4064, Bali=17193, Hong Kong=16808

## Step 3: Search Hotels (Xotelo API - Free)

### Get Hotel List
```bash
curl -s "https://data.xotelo.com/api/list?location_key=${LOCATION_KEY}&limit=${LIMIT}"
```
Returns per hotel: `name`, `key`, `review_summary.rating` (out of 5), `review_summary.count`, `price_ranges.minimum/maximum`, `geo`, `image`, `url`.

### Get OTA Prices
```bash
curl -s "https://data.xotelo.com/api/rates?hotel_key=${HOTEL_KEY}&chk_in=${CHECK_IN}&chk_out=${CHECK_OUT}&currency=${CURRENCY}"
```
Returns per OTA: `code`, `name`, `rate` (before tax), `tax`. Add 1s delay between requests.

### Generate Booking Links

Xotelo doesn't provide booking URLs. Build them per OTA (URL-encode hotel name as `{H}`):

| OTA Code | Booking URL |
|----------|-------------|
| BookingCom | `https://www.booking.com/searchresults.html?ss={H}&checkin={CHECK_IN}&checkout={CHECK_OUT}&group_adults={ADULTS}&no_rooms={ROOMS}` |
| Agoda | `https://www.agoda.com/search?q={H}&city={AGODA_CITY_ID}&checkIn={CHECK_IN}&checkOut={CHECK_OUT}&los={LOS}&rooms={ROOMS}&adults={ADULTS}` |
| CtripTA | `https://www.trip.com/hotels/list?keyword={H}&checkin={CHECK_IN}&checkout={CHECK_OUT}` |
| HotelsCom | `https://www.hotels.com/search.do?q={H}&checkin={CHECK_IN}&checkout={CHECK_OUT}` |
| Expedia | `https://www.expedia.com/Hotel-Search?destination={H}&d1={CHECK_IN}&d2={CHECK_OUT}&adults={ADULTS}&rooms={ROOMS}` |

### Price Heatmap (optional, for flexible dates)
```bash
curl -s "https://data.xotelo.com/api/heatmap?hotel_key=${HOTEL_KEY}&currency=${CURRENCY}"
```

## Step 4: Apify Mode (Optional)

If `APIFY_API_KEY` is set, use for Agoda-specific deep search:
```bash
curl -s -X POST "https://api.apify.com/v2/acts/knagymate~fast-agoda-scraper/runs?token=${APIFY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"city":"'"${DESTINATION}"'","checkIn":"'"${CHECK_IN}"'","checkOut":"'"${CHECK_OUT}"'","rooms":'"${ROOMS}"',"adults":'"${ADULTS}"',"currency":"'"${CURRENCY}"'","maxItems":15}'
```
Poll `.data.status` until SUCCEEDED, then fetch from `.data.defaultDatasetId`.

## Step 5: Output Format

```
## 🏨 Hotel Search: [Destination]
📅 [CheckIn] → [CheckOut] ([N] nights) | 👤 [Adults] | 🛏️ [Rooms] room(s)

### #1 [Hotel Name] ⭐ [Rating]/5 ([Reviews] reviews)
| OTA | Rate | Tax | Total | Book |
|-----|------|-----|-------|------|
| **Agoda** | $280 | $53 | **$333 ← Best** | [Book](url) |
| Trip.com | $347 | $34 | $381 | [Book](url) |
💡 Save $82 by booking on Agoda vs Booking.com!
```

Rules: Sort OTAs cheapest first. Mark best deal. Show savings. Always include booking links. Include Agoda full search URL at bottom.

## Error Handling

- Destination not found → try Xotelo search API, then ask user
- `chk_in is invalid` → dates may be too far out, try within 1 year
- No OTA rates → show TripAdvisor link instead
- Apify fail → auto fallback to Xotelo free mode
- Rate limit → add 1s delay, limit to 5 hotels per batch
