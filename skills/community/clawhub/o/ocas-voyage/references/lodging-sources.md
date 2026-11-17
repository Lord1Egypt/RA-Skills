# Lodging Sources

Per-source patterns and failure modes for `voyage.recommend.lodging`.

## Expedia (web mode)

Always available. Navigate `expedia.com` via browser tools.

Search pattern: destination + dates + traveler count → filter by property type, budget, cancellation → open 3–5 candidates → verify fees and policies on candidate page.

Failure modes:
- Price changes between search and checkout — re-check before recommending
- Package savings hide weak flight shape — evaluate separately
- Resort fees not shown until checkout — explicitly check candidate page

## Marriott Strider MCP (`mcp-marriott`)

Requires `@striderlabs/mcp-marriott` installed and Bonvoy OAuth active.

**Installation** (run once; skip if `mcp-marriott` already in MCP config):
```bash
npm install -g @striderlabs/mcp-marriott
```
Add to platform MCP config:
```json
{
  "mcpServers": {
    "marriott": {
      "command": "mcp-marriott"
    }
  }
}
```
Run OAuth login: `marriott.mobile_key` — opens browser for Bonvoy account login. Re-run if session expires.

Key commands:
- `marriott.search_hotels` — by location, dates, room count; optional brand/points filters
- `marriott.get_bonvoy_status` — points balance and elite tier
- `marriott.request_upgrade` — suite upgrade request for eligible members
- `marriott.mobile_key` — digital room access (also used for OAuth init)

Failure modes:
- OAuth session expired — re-run `marriott.mobile_key` to re-authenticate
- MCP not installed — skip silently, continue with Expedia and Marriott AI

## Marriott AI / FlyAI

**DEAD (verified 2026-08-23):** all FlyAI domains (flyai.com, api.flyai.com,
app.flyai.com) fail DNS resolution (NXDOMAIN) — the service has shut down. Do
not attempt; do not set `FLYAI_API_KEY`. Marriott property search is covered by
the Strider MCP above; general hotel search by Google Hotels / 1Stay / LetsFG.

## Google Hotels (agent-browser)

Requires `agent-browser` CLI. Search-only; cannot complete bookings.

Pattern: encode dates → open Google Hotels URL with location and encoded dates → snapshot results → extract structured table.

Session: use `--session hotels` to isolate.

Failure modes:
- `agent-browser` not installed — skip silently
- DOM structure changes — use snapshot extraction, not fragile selectors

## 1Stay (MCP connector — Streamable HTTP)

Hotel booking MCP server by Stayker (WPF Holdings, LLC). Completes **real** hotel reservations with the hotel's own confirmation number — not search-and-redirect. 300,000+ properties across 140+ countries, loyalty program eligible. The guest pays the hotel directly; you are never the merchant of record.

**MCP endpoint:** `https://mcp.stayker.com/mcp` — Streamable HTTP transport.

**Configuration:** Add to Hermes MCP config as connector `1stay` pointing to the endpoint URL with Bearer auth header. API keys issued per application, scoped to sandbox (`sk_test_…`) or production (`1stay_live_…`). Sandbox keys use test properties and never charge guests; production keys access live inventory and create real reservations.

```json
{
  "mcpServers": {
    "1stay": {
      "url": "https://mcp.stayker.com/mcp",
      "headers": {
        "Authorization": "Bearer 1stay_live_…"
      }
    }
  }
}
```

**Tools (8):**

| Tool | Type | Purpose |
|------|------|---------|
| `search_hotels` | Read-only | Search by location (or lat/lng), dates, guests, rooms, radius, chain_code (MC=Marriott, HH=Hilton, HI=IHG, YX=Hyatt, BW=Best Western, WY=Wyndham, EL=Choice), currency, max_results. Returns hotel_id, name, address, stars, from_rate, loyalty_eligible, distance_miles. Supports cursor-based pagination via search_id. |
| `get_hotel_details` | Read-only | Room types, live rates, amenities, cancellation policies, rate_codes for a specific property. Rate codes expire in ~15 minutes. |
| `book_hotel` | Idempotent | Create reservation using hotel_id + rate_code → returns secure checkout URL where guest pays. Returns total, status (`pending_payment`), expires_at (~30 min). |
| `lookup_booking` | Read-only | Identity-verified lookup by guest name + at least one verification factor (confirmation_number, email, or last_four_card + check_in_date). |
| `get_booking` | Read-only | Developer-level lookup by booking_id (`stk_bk_xxxx`) or confirmation_number. Anonymous callers need verification_token from lookup_booking. |
| `cancel_booking` | Destructive, Idempotent | Two-step: 1st call with guest name + confirmation_number (leave cancellation_token empty) → previews terms + returns cancellation_token. 2nd call with token → cancels. |
| `resend_confirmation` | Open-world | Resend confirmation email to the email on file. |
| `search_tools` | Read-only | List available 1Stay tools, optionally filtered by keyword. |

**Booking workflow (total cost gate applies):**
1. `search_hotels` → present ranked results with from_rate
2. `get_hotel_details` → show room types, rate codes, cancellation policy, nightly breakdown
3. `book_hotel` → collect guest name + email in conversation → returns checkout URL + total
4. Guest pays on PCI-compliant checkout page (URL valid ~30 min)
5. Confirmation email sent with hotel confirmation number
6. `lookup_booking` / `get_booking` for post-booking management; `cancel_booking` for changes (no update tool — cancel + re-book pattern)

**Required params for booking:**
- `hotel_id` (from search_hotels or get_hotel_details)
- `rate_code` (from get_hotel_details — must call first, rate code expires in ~15 min)
- `check_in`, `check_out` (YYYY-MM-DD)
- `guests` (integer)
- `guest_name`, `guest_email` (full name + email for confirmation)
- `external_reference_id` (optional, for idempotency and retrieval)

**Failure modes:**
- MCP endpoint unreachable — skip 1Stay, continue with other sources
- OAuth/API key not configured — `search_hotels` and `get_hotel_details` may still work; `book_hotel` will fail
- Checkout URL expires after ~30 min — treat as booking gate failure, re-book
- Rate code expires in ~15 min — re-check via `get_hotel_details` before booking
- No update tool — changes require cancel + re-book pattern
- **Status:** Endpoint may be intermittently unavailable; verify before critical bookings

**Total cost note:** Returns live rates from hotel PMS directly — no resort fee surprises. Always surface headline price + taxes + mandatory fees + cancellation flexibility. The `nightly_breakdown` array in `get_hotel_details` provides per-night pricing. Always re-check price via `get_hotel_details` before presenting as final.

## HotelOracle (MCP connector — Glama gateway)

Hotel Intelligence MCP via Google Hotels — **informational/research only, no booking**. Connects through the Glama MCP Gateway for managed credentials and call logging. Search, price compare, area guides, price calendars, and nearby-attraction data across major booking sites.

**Server:** `ToolOracle/hoteloracle` — **direct Streamable HTTP endpoint: `https://tooloracle.io/hotel/mcp/`** (verified live 2026-08-23; free tier, 100 calls/day, no key required). Note: the old `io.tooloracle/hoteloracle` Glama path 404s and tooloracle.com is an unrelated content site — use the tooloracle.io endpoint. Configured in profile `config.yaml` as MCP server `hoteloracle`.

**Tools (8):**

| Tool | Type | Purpose |
|------|------|---------|
| `search_hotels` | Read-only | General hotel search by `query` (city, hotel name, or address). Returns results from Google Hotels. |
| `hotel_details` | Read-only | Deep details for a specific hotel: full amenities, reviews breakdown, images, eco-certification, nearby places. |
| `price_calendar` | Read-only | Price trends and cheapest dates across a date range — ideal for flexible-date planning. |
| `price_compare` | Read-only | Cross-site price comparison across Booking.com, Hotels.com, Expedia, etc. for a given hotel. |
| `area_guide` | Read-only | Best neighborhoods to stay in a city, compared by price, rating, and popular hotels. |
| `best_deals` | Read-only | Cheapest hotels in a city/area, sorted by lowest price. |
| `nearby_attractions` | Read-only | Restaurants, landmarks, transit stations near a hotel, with distances. |
| `health_check` | Read-only | Server status, API connectivity, supported features. No-op otherwise. |

**Usage in Voyage:** HotelOracle is a **research** source — it enriches hotel details, price trends, and area context that dedicated booking platforms (1Stay, Expedia, Marriott) may not surface. It should not be presented as a booking channel.

**Parameters (notable):**
- `search_hotels`: `query`, `check_in`, `check_out`, `country` (default `us`), `currency` (default `USD`), `budget` (budget/mid/luxury for `area_guide`)
- `price_calendar`: `query`, `check_in`, `check_out` — shows per-date price trends
- `price_compare`: `query`, `check_in`, `check_out` — returns rates from multiple booking sites
- `nearby_attractions`: `query` (hotel name + city), `check_in`, `check_out`

**Failure modes:**
- Glama MCP Gateway unreachable — skip HotelOracle, continue with 1Stay + Expedia + Marriott
- Google Hotels parsing changes — use snapshot extraction, not fragile selectors
- No booking capability — must redirect booking intent to 1Stay (if MCP configured) or Expedia web

**Total cost note:** HotelOracle prices are informational/research only — they represent third-party listing prices and may not match the hotel's direct rate. Do not present HotelOracle prices as booking-final; always re-check via a booking source (1Stay or Expedia) before recommending.

## HotelsByDay (web harness — day-use + night)

Day-use hotel booking platform with a separate overnight product (night.hotelsbyday.com). Specialized in daytime hotel rooms (10AM–5PM, 8AM–2PM, etc.) and "work passes" — a unique vertical not covered by 1Stay or Expedia. Uses a bundled Python harness script at `scripts/hotelsbyday_search.py`.

**Sites:**
| Site | Purpose | Base URL |
|------|---------|----------|
| **Day-use** | Daytime hotel rooms (10AM–5PM), work passes, pool/spa/gym passes | `https://www.hotelsbyday.com` |
| **Night** | Overnight stays (currently in beta with limited inventory) | `https://night.hotelsbyday.com` |
| **Media** | Hotel photos, amenity images | `https://api.hotelsbyday.com/api/media/v1/` |

**Harness usage (bundled script):**
```bash
$HERMES_PY $HERMES_HOME/../indigo/skills/ocas-voyage/scripts/hotelsbyday_search.py autocomplete "New York"
$HERMES_PY $HERMES_HOME/../indigo/skills/ocas-voyage/scripts/hotelsbyday_search.py search "New York" 2026-08-10 2026-08-11 --guests 1 --product day
$HERMES_PY $HERMES_HOME/../indigo/skills/ocas-voyage/scripts/hotelsbyday_search.py hotel-detail "https://www.hotelsbyday.com/en/hotels/united-states/new-york/m-social-hotel-times-square?date=2026-08-10"
```

**Data extraction patterns:**
- **Autocomplete:** `GET /en/search/multy_autocomplete?query=...` → JSON with `hotels` array (`hotelid`, `name`, `location`) and `countries` array (`countryid`, `name`, `code`)
- **Search results (day):** `GET /en/search/results?query=...&check_in=...&check_out=...&guests=...` → HTML with `class="card-hotel"` elements containing `data-href` (hotel URL), `card-hotel-name` (name + location + star rating), `data-price` + `data-currency` (price), `hd-room-name` (service type), `hd-room-time` (time slot), `hd-room-cancellation` (cancellation policy)
- **Hotel detail:** `GET /en/hotels/{country}/{state}/{city}/{hotel-slug}?date=...` → HTML with `hd-room-name`, `hd-room-time`, `data-price`, `data-currency`, `data-rate-type`, `hd-room-cancellation` per room; JSON-LD with hotel name/stars/description
- **Night search:** `GET /en/hotels/search?query=...&check_in=...&check_out=...&guests=...&stay_type=night` → HTML with Livewire `wire:snapshot` components; search-list component contains `totalHotels`, `hasResults`, `isLoading` in its snapshot data. Site displays beta notice and "Worldwide inventory will be available very soon."

**Output structure (JSON):**
- `autocomplete`: `{query, results: [{type, hotel_id/name, location}]}`
- `search`: `{source, query, check_in, check_out, guests, total_hotels, hotels: [{url, name, rating, price, currency, services, time_slots, cancellation, loyalty_coins}]}`
- `hotel-detail`: `{source, url, title, stars, rooms: [{name, time_slot, price, currency, rate_type, cancellation}]}`

**Failure modes:**
- Autocomplete returns empty — location may need more specificity; suggest narrowing to city or using a known hotel name
- Search returns 0 hotels — location may not have day-use inventory; try nearby cities or the night product
- **Silent NY fallback (found 2026-08-23, fixed in harness):** `/en/search/results` returns default New York hotels when it can't geocode the query (e.g. "Honolulu" → NY cards). Harness now detects the mismatch and resolves the city page (`/en/hotels/united-states/{city-slug}`) instead, reporting `source: hotelsbyday-city-page`. City-page results lack prices/ratings — call `hotel-detail` per property.
- Night site returns 0 hotels — beta phase with limited inventory; surface beta notice to user
- Hotel detail page 404 — hotel may not be bookable for the selected date; suggest adjusting dates
- Price is null in search results — rates are loaded per-hotel on detail page; call `hotel-detail` for pricing

**Total cost note:** HotelsByDay prices are from the hotel's own distribution system. Prices include taxes and fees breakdown (`+ Tax & fees` shown). Always surface full price + cancellation policy before recommending. Note the date parameter in hotel URLs defaults to the current date (not the user's requested date) — always re-fetch with the correct date.

**Booking flow:** Currently search-and-redirect only. The booking form on hotel detail pages collects guest name, email, and payment info directly. Voyage does not auto-book; it surfaces rates and directs the user to the hotel page for completion.

Delegation target for anything the lodging platforms don't cover: destination context, activity recommendations, restaurant picks, local knowledge, neighborhood comparisons.

Do not use Sift for hotel availability or pricing — use the dedicated lodging sources above.
