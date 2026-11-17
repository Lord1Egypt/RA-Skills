# LetsFG Reference — agent-native flight & hotel search/booking

Source: https://github.com/LetsFG/LetsFG · Docs: https://letsfg.co/for-agents

## What it is

Agent-native flight AND hotel search with real booking capability (real airline
PNR / hotel confirmation). Server-side engine scans airlines + major OTAs
(Skyscanner, Kiwi, Kayak, Momondo, direct carriers incl. budget). Claimed
advantages over Google Flights: stable prices across repeat searches, broader
budget-airline coverage, $15–56 cheaper per route in their 2026-08 comparison.
Complements the `fli` library (Google Flights data): use both when price
comparison matters; LetsFG additionally *books*.

## Critical guardrails

- **NEVER** call `/developers/api/v1/agents/register`, `/developers/api/v1/agents/setup-payment`,
  `letsfg register`, or `letsfg setup-payment` — those create a PAID prepaid-balance
  Developer API billing account. Agent flow is `letsfg auth` only.
- `letsfg auth` puts a **payment method on file** via zero-amount Stripe setup
  (nothing charged) → 90-day Bearer token in `~/.letsfg/config.json`. Because this
  attaches a card, get explicit user approval before running it.
- Hotel booking charges a **5% non-refundable reservation fee** immediately;
  balance paid to supplier via returned `pay_link` by `balance_due_by`. Only
  free-cancellation pay-later rates are sold. Never book without the Voyage
  booking-gate rule (price re-check, terms stated, user approval).
- **Do not retry hotel bookings blindly** — duplicate calls book twice and charge twice.
- Flight search requires the auth token too (card on file) — even search is gated.

## Setup (one-time, needs user approval for card-on-file)

```bash
pip install letsfg            # into Hermes venv if needed
letsfg auth                   # prints setup_url; human adds card OR headless Stripe SetupIntent
```

Token lives at `~/.letsfg/config.json`, valid 90 days; re-auth after expiry.

## Usage patterns

### CLI

```bash
letsfg search LHR BCN 2026-06-15 --return 2026-06-22 --sort price --json
letsfg search SFO JFK 2026-06-15 --cabin C          # M/W/C/F cabin classes
letsfg locations "lisbon"                            # resolve city → IATA
letsfg book off_xxx --passenger '{"given_name":"...","family_name":"...","born_on":"1990-01-15","gender":"m","title":"mr"}' --email user@example.com
letsfg me                                            # profile & usage
```

### Python SDK

```python
from letsfg import LetsFG
lfg = LetsFG()  # reads LETSFG_API_KEY env or ~/.letsfg/config.json
flights = lfg.search("LHR", "JFK", "2026-04-15")
print(flights.total_results, flights.cheapest.summary())
for o in flights.offers:
    if o.get("starlink") == "confirmed_all": ...   # Wi-Fi signal tiers: confirmed_all | likely_all | absent
```

### Hotels

```python
city = lfg.hotel_destinations("Warsaw")[0]
stays = lfg.search_hotels(city_id=city["Id"], city_name=city["Name"],
                          check_in="2026-11-10", check_out="2026-11-12", adults=2)
hotel, offer = stays["hotels"][0], stays["hotels"][0]["offers"][0]
booking = lfg.book_hotel_and_wait(session_id=stays["session_id"],
    hotel_code=hotel["hotel_code"], combination_id_v2=offer["combination_id_v2"],
    expected_price=offer["price"], expected_balance=offer["balance_to_supplier"],
    city_id=city["Id"], city_name=city["Name"],
    check_in="...", check_out="...",
    guests=[{"title":"Mr","first_name":"Jan","last_name":"Kowalski"}],
    email="...", phone="...")
# → booking["confirmation"], booking["pay_link"], booking["balance_due_by"]
```

Async alternative: `book_hotel` returns `booking_job_id`; poll `hotel_booking(job_id)`.

### MCP option

`npx letsfg-mcp` — tools include flight search/book plus
`resolve_hotel_city → search_hotels → book_hotel → get_hotel_booking → cancel_hotel_booking`.

## Role within Voyage

| Need | Source |
|---|---|
| Broadest price scan incl. budget carriers, stable repeat pricing | LetsFG |
| Google Flights data, date-range cheapest-day search | `fli` (default) |
| Actual booking without OTA checkout redirect | LetsFG (`book` / agent-book) |
| Free-cancellation hotel rates with hold-now/pay-later | LetsFG hotels |

Search order for flights: run `fli` first (no credentials), add LetsFG results
when the token exists or the task involves booking. Merge into the unified
comparison table with an "as of" timestamp per the total-cost rule.

## Failure modes

| Symptom | Cause | Response |
|---|---|---|
| 401 on search | Token expired (>90 days) | Re-run `letsfg auth` (user approval for card step) |
| 402 challenge | No payment method on file | Run `letsfg auth`; never the register endpoints |
| Hotel search refuses | Card on file required even for search | Expected behavior; surface to user |
| Slow search (60–90 s) | Server-side engine polls sources | Normal; poll until `status: done` |
