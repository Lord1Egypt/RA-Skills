# Travel Time Calculation Logic

Used by: `sands.travel`

---

## Step 1 — Resolve Departure Point

Priority order:

1. Prior event within 90 minutes AND has a specific location string
   → use that location as departure
2. No prior event, or prior event has no location
   → query system for current location context (Weave → Chronicle)
3. If system indicates the user is traveling (hotel, Airbnb, out-of-town)
   → use current lodging as departure
4. If system indicates user is at home
   → use home location
5. If no location context available
   → ask the user before proceeding. Do not guess.

Never assume the user is in their home city. Never use a hardcoded address.

---

## Step 2 — Resolve Locations via Google Places API

For both departure and destination:

1. Call **Places Search / Find Place** with the location string
   (e.g., event address, hotel name, place name)
2. Extract place_id and coordinates (lat/lng)
3. If search returns ambiguous results, use the highest-confidence match
   and note it in the journal

---

## Step 3 — Determine Travel Mode

If the user specified a mode (`driving`, `transit`, `walking`, `bicycling`), use it.

If no mode specified, infer from distance between departure and destination:

1. Calculate straight-line distance between the two coordinates
2. Apply heuristic:
   - **≤ 0.5 miles / 800 meters** — same-area shortcut (see Step 7), skip travel event
   - **≤ 1 mile / 1.6 km** — suggest `walking`, offer `driving` as alternative
   - **≤ 5 miles / 8 km** — offer both `transit` and `driving`; use `default_travel_mode`
     from config if neither is specified
   - **> 5 miles / 8 km** — use `default_travel_mode` from config (default: `driving`)

If inference suggests a non-default mode, present the suggestion to the user:
"These locations are about 0.8 miles apart. Walk (~15 min) or drive (~5 min)?"

Fallback: if `default_travel_mode` is not set in config, default to `driving`.

---

## Step 4 — Get Travel Time via Distance Matrix API

Call **Distance Matrix API**:
- Origins: departure place_id or coordinates
- Destinations: destination place_id or coordinates
- Mode: selected travel mode from Step 3
- Departure time: actual departure time if known, otherwise "now"

For transit mode, also pass:
- `transit_mode`: best available (bus, subway, train, tram)
- `arrival_time`: destination event start time (for more accurate scheduling)

Extract: `duration_in_traffic` (preferred, driving only) or `duration` (fallback / other modes).

---

## Step 5 — Apply Buffer

`travel_time_total = api_duration + travel_buffer_minutes`

`travel_buffer_minutes` is read from `config.json` (default: 10 minutes).

---

## Step 6 — Check Gap

Calculate available gap:
`gap = destination_event.start - prior_event.end`

- If `gap >= travel_time_total`: create the travel event filling the gap
- If `gap < travel_time_total`: do NOT create a truncated block.
  Surface a conflict instead:
  "Travel to [destination] requires ~X min but only Y min are available
  after [prior event]."

---

## Step 7 — Create Travel Event

Title format is mode-aware:

| Mode | Title |
|---|---|
| driving | `🚗 Travel → [destination event title]` |
| transit | `🚇 Travel → [destination event title]` |
| walking | `🚶 Travel → [destination event title]` |
| bicycling | `🚲 Travel → [destination event title]` |

Calendar: same primary calendar as the destination event
Start: prior_event.end
End: destination_event.start (fills the gap exactly)
Availability: free
Description: `Travel from [departure place] to [destination place]. Estimated: X min [mode] (via Google Maps).`

---

## Same-Area Shortcut

If both locations resolve to within ~0.5 miles / 800 meters of each other,
skip travel event creation and note it to the user:
"[Destination] is very close to [departure] (~X meters). No travel block needed."

---

## API Unavailable Fallback

If Google Places API is unreachable:
1. Log the failure in decisions.jsonl
2. Notify the user: "Travel time API unavailable. Please confirm estimated
   travel time and I'll create the block manually."
3. Do not silently use a distance heuristic.
