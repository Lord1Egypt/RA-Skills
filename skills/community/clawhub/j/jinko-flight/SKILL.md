---
name: jinko-cli
description: >-
  Guide for using the Jinko CLI (@gojinko/cli) — a terminal tool for searching
  flights, discovering destinations, managing trips, and booking travel.
  Use when: running jinko commands, searching flights from terminal, price-checking
  offers, building trips, or booking travel via CLI. Triggers: any mention of
  "jinko cli", "jinko command", "flight search cli", or when the user wants to
  use the jinko terminal tool instead of MCP tools.
version: "1.0.0"
metadata: {"openclaw":{"requires":{"bins":["jinko","node"]},"primaryEnv":"JINKO_API_KEY","emoji":"✈️","install":[{"type":"node","package":"@gojinko/cli","global":true}]}}
---

# Jinko CLI Usage Guide

Installed at: `/usr/local/lib/node_modules/@gojinko/cli/`
Binary: `jinko` (symlinked to `/usr/local/bin/jinko`)

## Authentication

You must authenticate before using any Jinko CLI commands.

### Option 1: OAuth (Recommended)

The primary and recommended way to authenticate. Opens a browser-based OAuth flow to securely link your Jinko account.

```bash
jinko auth login
```

This opens your default browser, prompts you to sign in to your Jinko account, and stores the credentials locally. No API key management required.

### Option 2: API Key

Alternatively, you can authenticate using an API key (prefixed `jnk_...`). Use this for CI/CD pipelines, scripts, or headless environments where a browser is not available.

```bash
# Set the API key via config
jinko config set api_key jnk_your_api_key_here

# Or pass it per-command
jinko find-flight --api-key jnk_your_api_key_here --from SFO --to NYC --date 2026-04-01

# Or set it as an environment variable
export JINKO_API_KEY=jnk_your_api_key_here
```

### Auth Management

```bash
jinko auth login          # Authenticate via OAuth (recommended)
jinko auth logout         # Clear stored credentials
jinko auth status         # Show current auth status
```

---

## Global Options

| Option | Description |
|---|---|
| `--format <format>` | Output format: `json` (default) or `table` |
| `--api-key <key>` | API key (jnk_...) — overrides env/config |
| `-V, --version` | Show version |

## Important: Command Priority

**Always prefer `find-flight` and `flight-calendar` over `flight-search` when possible.** These commands use cached/indexed data and are ideal for:
- Finding the cheapest dates to fly on a route
- Setting up deal alerts and monitoring prices over time
- Quickly comparing fares across multiple dates or destinations

Only fall back to `flight-search` (live search) when `find-flight` returns no results for the given route/date, or when you need real-time pricing to confirm an offer before booking.

## Commands Overview

### 1. `jinko find-flight` — Cached Flight Search

Finds cheapest flights from cached/indexed data. Fast but prices may be stale. Returns `offer_token` for live pricing via `flight-search`.

```bash
jinko find-flight --from <IATA> --to <IATA> --date <YYYY-MM-DD> [options]
```

| Option | Description |
|---|---|
| `--from <origin>` | Origin IATA code (e.g. PAR, SFO) |
| `--to <destination>` | Destination IATA code (e.g. NYC, BKK) |
| `--date <date>` | Departure date (YYYY-MM-DD) |
| `--return <date>` | Return date for round-trip |
| `--cabin <class>` | economy, premium_economy, business, first (default: economy) |
| `--direct-only` | Only show direct/nonstop flights |
| `--max-price <amount>` | Maximum price filter |
| `--sort <sort>` | lowest (default) or recommendation |
| `--limit <n>` | Max results (default: 10) |

**Response fields:** `itineraries[]` with `id`, `offer_token` (for price-check), `total_amount`, `slices[]` (segments), `jinko_advice` (price guidance).

**Example:**
```bash
jinko find-flight --from SFO --to NYC --date 2026-03-26 --sort lowest
jinko find-flight --from PAR --to BKK --date 2026-05-01 --return 2026-05-08 --direct-only
```

---

### 2. `jinko find-destination` — Destination Discovery

Discover where to fly from one or more origins. Use when the user doesn't know where to go.

```bash
jinko find-destination --from <IATA...> [options]
```

| Option | Description |
|---|---|
| `--from <origins...>` | One or more origin IATA codes (e.g. PAR CDG) |
| `--date <date>` | Departure date |
| `--return <date>` | Return date |
| `--direct-only` | Only direct flights |
| `--cabin <class>` | Cabin class (default: economy) |
| `--max-price <amount>` | Max price filter |
| `--sort <sort>` | lowest or recommendation |
| `--limit <n>` | Max destinations (default: 20) |

**Response fields:** `origin`, `destinations[]` with `iata_code`, `city_name`, `lowest_fare_flight`, `flights[]`.

**Example:**
```bash
jinko find-destination --from SFO --date 2026-04-01 --max-price 300
jinko find-destination --from CDG ORY --direct-only --sort lowest
```

---

### 3. `jinko flight-search` — Live Search / Price Check

Two modes:
- **Search mode:** Live flight search with real-time pricing
- **Price-check mode:** Verify current price for a specific offer from `find-flight`

```bash
# Mode A: Live search
jinko flight-search --from <IATA> --to <IATA> --date <YYYY-MM-DD> [options]

# Mode B: Price-check a specific offer
jinko flight-search --offer-token <token>
```

| Option | Description |
|---|---|
| `--from <origin>` | Origin IATA code |
| `--to <destination>` | Destination IATA code |
| `--date <date>` | Departure date |
| `--return <date>` | Return date for round-trip |
| `--passengers <n>` | Number of passengers (default: 1) |
| `--cabin <class>` | Cabin class (default: economy) |
| `--direct-only` | Only direct flights |
| `--max-price <amount>` | Max price filter |
| `--offer-token <token>` | Price-check a specific offer (from find-flight) |

**Response fields:** `mode` (search/price_check), `status` (confirmed/sold_out/price_changed), `flights[]` with `fares[]` containing `trip_item_token` (needed for trip creation), `brand_name`, `total_price`, `refund_policy`, `change_policy`, `included_baggage`.

**Example:**
```bash
jinko flight-search --from SFO --to JFK --date 2026-04-01 --direct-only
jinko flight-search --offer-token "es-abc123_AMD"
```

---

### 4. `jinko flight-calendar` — Price Calendar

Show cheapest prices across a month for a route. Great for finding the best travel dates.

```bash
jinko flight-calendar --from <IATA> --to <IATA> [options]
```

| Option | Description |
|---|---|
| `--from <origin>` | Origin IATA code |
| `--to <destination>` | Destination IATA code |
| `--month <month>` | Month to display (YYYY-MM), defaults to current |
| `--cabin <class>` | Cabin class (default: economy) |
| `--direct-only` | Only direct flights |

**Example:**
```bash
jinko flight-calendar --from PAR --to NYC --month 2026-05
jinko flight-calendar --from SFO --to BKK --month 2026-06 --direct-only
```

---

### 5. `jinko trip` — Trip Management

Create a trip, add flights, and set travelers. All in one command.

```bash
jinko trip [options]
```

| Option | Description |
|---|---|
| `--trip-id <id>` | Existing trip ID (omit to create new) |
| `--trip-item-token <token>` | Add a flight item (from flight-search fares) |
| `--travelers <json>` | Travelers as JSON array |
| `--contact <json>` | Contact as JSON `{email, phone}` |

**Response fields:** `trip_id`, `status`, `items[]`, `travelers[]`, `contact`, `totals`, `actions_performed[]`.

**Traveler JSON format:**
```json
[{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "gender": "MALE",
  "passenger_type": "ADULT"
}]
```

**Example:**
```bash
# Create trip with a flight
jinko trip --trip-item-token "offer__abc123:0-1-0"

# Add travelers to existing trip
jinko trip --trip-id trip_xyz --travelers '[{"first_name":"John","last_name":"Doe","date_of_birth":"1990-05-15","gender":"MALE","passenger_type":"ADULT"}]' --contact '{"email":"john@example.com","phone":"+1-555-123-4567"}'
```

---

### 6. `jinko book` — Checkout

Generate a checkout URL (Stripe) for a trip. Returns a payment link.

```bash
jinko book --trip-id <id>
```

| Option | Description |
|---|---|
| `--trip-id <id>` | Trip ID from the trip command |

**Response fields:** `checkout_url`, `session_id`, `status` (ready/pending/failed), `expires_at`.

**Example:**
```bash
jinko book --trip-id trip_xyz789
```

---

### 7. `jinko config` — Configuration

```bash
jinko config show         # Show current config
jinko config set api_key jnk_xxx  # Set API key
```

---

## Typical Workflow

The standard booking flow follows this pipeline:

```
find-flight (cached, fast)
    → get offer_token
        → flight-search --offer-token (live pricing)
            → get trip_item_token from fares
                → trip --trip-item-token (create trip)
                    → trip --trip-id --travelers (add travelers)
                        → book --trip-id (get checkout URL)
```

**Step-by-step:**

1. **Search** — `jinko find-flight --from SFO --to NYC --date 2026-04-01`
2. **Price-check** — `jinko flight-search --offer-token "<offer_token_from_step_1>"`
3. **Create trip** — `jinko trip --trip-item-token "<trip_item_token_from_step_2>"`
4. **Add travelers** — `jinko trip --trip-id <trip_id> --travelers '<json>' --contact '<json>'`
5. **Book** — `jinko book --trip-id <trip_id>`
6. **User pays** via the returned `checkout_url`

## IATA Code Tips

- Use city codes for multi-airport cities: NYC (all NY airports), PAR (CDG+ORY), LON (all London)
- Use airport codes for specific airports: JFK, CDG, LHR
- Common codes: SFO, LAX, ORD, ATL, MIA, BOS, SEA, DEN, DFW
