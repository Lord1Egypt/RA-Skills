# OpenTable requests for fpx

All paths are relative to `https://www.opentable.com`. Bodies, headers, and
persisted-query hashes below are transcribed verbatim from opentable-mcp's
`src/client.ts`, `src/tools/*.ts`, and `src/tools/booking-flow.ts` — not
guessed. If a shape here stops working, re-check those files (or re-capture
per the note at the end) before assuming this doc is stale.

Two response families:
- **SSR HTML** pages embed the page's data as `window.__INITIAL_STATE__ =
  {...};` or `"__INITIAL_STATE__":{...}` inside the HTML. Pipe through
  `extract-initial-state.mjs` (same directory) before `jq`.
- **`/dapi/...` JSON/GraphQL** endpoints return plain JSON on stdout — `jq`
  directly.

Every write here (favorites add/remove, slot-lock, make-reservation,
cancel) is a REAL action against the signed-in account — there is no
confirm-gate or preview-then-`confirmToken` step like the MCP's write tools
have. Preview before you commit.

---

## 1. Search restaurants

`GET /s` — SSR. Data lives at `state.multiSearch.restaurants[]`
(`state.multiSearch.totalRestaurantCount`, `.metro.name`, `.metroId` for
the search's resolved metro). No slot/availability data here — that's §3.

```sh
fpx get 'https://www.opentable.com/s?term=Italian%20Charlotte&covers=2&dateTime=2026-08-01T19:00' \
  -p opentable | node extract-initial-state.mjs \
  | jq '.multiSearch.restaurants[] | {id: .restaurantId, name, cuisine: .primaryCuisine.name, url: .urls.profileLink.link, rating: .statistics.reviews.ratings.overall.rating}'
```

Query params (all optional, build the ones you have): `term` (free text —
join `"<term> <location>"` yourself, OpenTable does), `covers` (party
size), `dateTime` (`YYYY-MM-DDTHH:MM`, defaults the ranking not the
results), `latitude`, `longitude`, `metroId` (e.g. `8` = SF Bay Area, `31`
= Charlotte).

## 2. Restaurant detail

`GET /r/{slug}` — SSR. Data lives at `state.restaurantProfile.restaurant`.
A subset of (older) listings 404 here and are served at the **root**
path `/{slug}` instead (e.g. `/the-cellar-at-duckworths`) — try `/r/{slug}`
first, fall back to `/{slug}` on a 404. **Numeric ids route to
`/restaurant/profile/{id}`** instead of either — you
need the slug (from §1's `urls.profileLink.link`, or the venue's known
URL).

```sh
fpx get 'https://www.opentable.com/r/state-of-confusion-charlotte' -p opentable \
  | node extract-initial-state.mjs \
  | jq '.restaurantProfile.restaurant | {id: .restaurantId, name, type, bookable: (.type != "Listing"), phone: .contactInformation.formattedPhoneNumber}'
```

`type: "Listing"` (vs `"GuestCenter"`) means info-only — no slot picker,
no booking flow; surface the phone number instead of trying §6–8.

## 3. Find available slots

`POST /dapi/fe/gql?optype=query&opname=RestaurantsAvailability` — Apollo
persisted query (hash only, no GraphQL text sent). Response:
`data.availability[].availabilityDays[].slots[]`, each slot carrying
`timeOffsetMinutes` (relative to the `time` you sent, NOT absolute),
`slotHash`, `slotAvailabilityToken`, `type` (`Standard`|`Experience`|`POP`),
`attributes` (`default`|`bar`|`highTop`|`outdoor`), and — for Experience
slots — `experienceIds`.

```sh
cat > /tmp/ot-avail.json <<'JSON'
{
  "operationName": "RestaurantsAvailability",
  "variables": {
    "onlyPop": false,
    "forwardDays": 0,
    "requireTimes": false,
    "requireTypes": [],
    "useCBR": false,
    "privilegedAccess": ["UberOneDiningProgram", "VisaDiningProgram", "VisaEventsProgram", "ChaseDiningProgram"],
    "restaurantIds": [54232],
    "restaurantAvailabilityTokens": ["eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ"],
    "date": "2026-08-01",
    "time": "19:00",
    "partySize": 2,
    "databaseRegion": "NA"
  },
  "extensions": {
    "persistedQuery": { "version": 1, "sha256Hash": "cbcf4838a9b399f742e3741785df64560a826d8d3cc2828aa01ab09a8455e29e" }
  }
}
JSON
fpx post-json 'https://www.opentable.com/dapi/fe/gql?optype=query&opname=RestaurantsAvailability' \
  @/tmp/ot-avail.json -p opentable \
  -H 'ot-page-type: home' -H 'ot-page-group: seo-landing-home' \
  | jq -r '.data.availability[].availabilityDays[].slots[] | select(.isAvailable) | "\(.slotHash)\t\(.type)\t\(.timeOffsetMinutes)min\t\(.slotAvailabilityToken)"'
```

Notes:
- `restaurantAvailabilityTokens` is one array entry per id in
  `restaurantIds`, in the same order — the literal
  `eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ` value works for a single
  fresh lookup (it's a generic anonymous token, not tied to the
  restaurant).
- `databaseRegion` defaults to `"NA"` (North America). Non-NA
  (UK/EU/APAC) restaurants shard elsewhere — OpenTable doesn't surface the
  shard id anywhere reachable from search/availability/booking-details, so
  if a booking/cancel against a non-US venue opaquely fails, that's the
  first thing to suspect (the MCP has the same limitation — see the repo's
  `CLAUDE.md` → "Hot spots / gotchas").
- Convert `timeOffsetMinutes` to an absolute time yourself: add it to the
  `time` you sent (wrapping past midnight rolls the date forward a day).

## 4. Reservations, profile, favorites (all SSR)

One dashboard page serves both reservations and profile:

```sh
fpx get 'https://www.opentable.com/user/dining-dashboard' -p opentable \
  | node extract-initial-state.mjs > /tmp/ot-dash.json

# Reservations — state.diningDashboard.{upcomingReservations,pastReservations}[]
jq -r '.diningDashboard.upcomingReservations[] | "\(.confirmationNumber)\t\(.dateTime)\t\(.restaurantName)\tparty \(.partySize)\tsecurityToken=\(.securityToken)"' /tmp/ot-dash.json

# Profile — state.header.userProfile
jq '.header.userProfile | {name: "\(.firstName) \(.lastName)", email, mobile: .mobilePhoneNumber, points, metro: .metro.displayName}' /tmp/ot-dash.json
```

Favorites live on a separate SSR page (`state.userProfile.favorites.restaurants[]`):

```sh
fpx get 'https://www.opentable.com/user/favorites' -p opentable \
  | node extract-initial-state.mjs \
  | jq '.userProfile.favorites.restaurants[] | {id: (.id // .restaurantId), name: (.name // .restaurantName)}'
```

Add / remove a favorite — plain JSON POST (204 No Content on success, no
body to parse). A fresh add can take ~10s to show up in the SSR page above
— treat the 204 as authoritative, don't round-trip to verify.

```sh
fpx post-json 'https://www.opentable.com/dapi/wishlist/add' \
  '{"restaurantId": 54232, "wishListName": "Favorites"}' -p opentable
fpx post-json 'https://www.opentable.com/dapi/wishlist/remove' \
  '{"restaurantId": 54232, "wishListName": "Favorites"}' -p opentable
```

## 5. Book — step 1: preview (`/booking/details` + slot-lock)

Booking is two POSTs after one SSR fetch. Do the SSR fetch first — it's
also where the numeric `diningAreaId` comes from (not in §3's response at
all):

```sh
fpx get 'https://www.opentable.com/booking/details?rid=54232&datetime=2026-08-01T19:00&covers=2&partySize=2&seating=default&slotHash=<slot_hash>&slotAvailabilityToken=<reservation_token>' \
  -p opentable | node extract-initial-state.mjs > /tmp/ot-details.json

# CC-required? cancellation policy? saved card? dining areas?
jq '{
  ccRequired: .timeSlot.creditCardRequired,
  policy: .messages.cancellationPolicyMessage.cancellationMessage.message,
  defaultCard: (.wallet.savedCards[] | select(.default == true)),
  diningAreas: .timeSlot.diningAreasBySeating,
  conflicts: .upcomingReservationConflicts
}' /tmp/ot-details.json
```

Add `&diningAreaId=<id>` to the URL to pin a specific room (otherwise
OpenTable still returns the full `diningAreasBySeating[]` list — take
`[0].diningAreaId`, or match `.tableCategory` to the seating you want).

**Experience-mandatory slots** (§3's `type == "Experience"`, one or more
`experienceIds`) need four extra query params:
`&experienceIds=<id>&selectedExperience=<id>&tableCategory=default&st=Experience&isMandatory=true`
— this lands on the same page the seating-options/specials click-through
would. Read `.experiences.experiences[]` for the bookable Experience's
`name`/`pricePerCover`/`version` (the `version` is required on the slot-lock
below).

**Same-day conflict check** — before locking, check
`.upcomingReservationConflicts` for any entry whose `dateTime` falls on the
date you're booking. OpenTable hard-refuses two reservations on the same
day; catching it here avoids an opaque 409 later.

Then slot-lock (holds the slot ~90s). Standard vs Experience are
**different GraphQL input types** — don't mix fields:

```sh
# Standard
cat > /tmp/ot-lock.json <<'JSON'
{
  "operationName": "BookDetailsStandardSlotLock",
  "variables": {
    "input": {
      "restaurantId": 54232,
      "seatingOption": "DEFAULT",
      "reservationDateTime": "2026-08-01T19:00",
      "partySize": 2,
      "databaseRegion": "NA",
      "slotHash": "<slot_hash>",
      "reservationType": "STANDARD",
      "diningAreaId": 12345
    }
  },
  "extensions": { "persistedQuery": { "version": 1, "sha256Hash": "1100bf68905fd7cb1d4fd0f4504a4954aa28ec45fb22913fa977af8b06fd97fa" } }
}
JSON
fpx post-json 'https://www.opentable.com/dapi/fe/gql?optype=mutation&opname=BookDetailsStandardSlotLock' \
  @/tmp/ot-lock.json -p opentable \
  -H 'ot-page-type: network_details' -H 'ot-page-group: booking' \
  | jq '.data.lockSlot | {success, slotLockId: .slotLock.slotLockId}'
```

```sh
# Experience — note the different field set (experienceId/experienceVersion/
# bookingType/slotAvailabilityToken; NO reservationType)
cat > /tmp/ot-lock-exp.json <<'JSON'
{
  "operationName": "BookDetailsExperienceSlotLock",
  "variables": {
    "input": {
      "restaurantId": 54232,
      "seatingOption": "DEFAULT",
      "reservationDateTime": "2026-08-01T19:00",
      "partySize": 2,
      "databaseRegion": "NA",
      "slotHash": "<slot_hash>",
      "experienceId": 987,
      "experienceVersion": 1,
      "diningAreaId": 12345,
      "bookingType": "Table",
      "slotAvailabilityToken": "<reservation_token>"
    }
  },
  "extensions": { "persistedQuery": { "version": 1, "sha256Hash": "363af9e3bd17efa82ad71c5808c5272603b5f1abe13b535d3beed1e6258ce504" } }
}
JSON
fpx post-json 'https://www.opentable.com/dapi/fe/gql?optype=mutation&opname=BookDetailsExperienceSlotLock' \
  @/tmp/ot-lock-exp.json -p opentable \
  -H 'ot-page-type: network_details' -H 'ot-page-group: booking' \
  | jq '.data.lockExperienceSlot | {success, slotLockId: .slotLock.slotLockId}'
```

## 6. Book — step 2: commit (`/dapi/booking/make-reservation`)

Plain JSON POST (not a persisted query). Consumes the `slotLockId` from
§5, plus your own profile fields (from §4's `.header.userProfile` —
`mobilePhoneNumber.number` with the country code stripped) and a fresh
`correlationId` (any UUID). **This makes a real reservation — no
dry-run.**

```sh
cat > /tmp/ot-book.json <<'JSON'
{
  "restaurantId": 54232,
  "reservationDateTime": "2026-08-01T19:00",
  "partySize": 2,
  "slotHash": "<slot_hash>",
  "slotAvailabilityToken": "<reservation_token>",
  "slotLockId": 999999,
  "diningAreaId": 12345,
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane@example.com",
  "phoneNumber": "5551234567",
  "phoneNumberCountryId": "US",
  "country": "US",
  "reservationAttribute": "default",
  "pointsType": "Standard",
  "points": 100,
  "tipAmount": 0,
  "tipPercent": 0,
  "confirmPoints": true,
  "optInEmailRestaurant": false,
  "additionalServiceFees": [],
  "nonBookableExperiences": [],
  "katakanaFirstName": "",
  "katakanaLastName": "",
  "correlationId": "<uuid>",
  "isModify": false,
  "reservationType": "Standard"
}
JSON
fpx post-json 'https://www.opentable.com/dapi/booking/make-reservation' \
  @/tmp/ot-book.json -p opentable \
  | jq '{confirmationNumber, reservationId, securityToken, points, errorCode, partnerScaRequired}'
```

Variants (merge these keys into the body above — never send all three sets
at once):

- **Experience booking**: replace `"reservationType": "Standard"` with
  `"reservationType": "Experience"` and add `"experienceId": 987,
  "experienceVersion": 1`. Do **not** send `tableCategory` here — it
  belongs on the slot-lock body only and 400s make-reservation.
- **CC-required slot** (from §5's `ccRequired: true`): add
  `"creditCardToken": "<wallet card id>", "creditCardLast4": "4242",
  "creditCardMMYY": "1028", "creditCardProvider": "spreedly",
  "scaRedirectUrl": "https://www.opentable.com/booking/payments-sca"`. All
  four card fields come from §5's `.wallet.savedCards[]` entry (`cardId`,
  `last4`, `expiryMonth`+`expiryYear` → `MMYY`); `creditCardProvider` is
  always the literal `"spreedly"` (OpenTable's tokenization vendor — saved
  cardIds are already Spreedly tokens, nothing to tokenize yourself).
- **Modify an existing reservation**: replace `"isModify": false` with
  `"isModify": true, "securityToken": "<existing security_token>",
  "confnumber": <existing confirmation_number>` (note: lowercase, no
  underscore — OpenTable's own inconsistency). Do **not** send
  `reservationId` on a modify — it 400s ("reservationId is not allowed")
  even though it looks like the natural identifier. Everything else
  (slotHash/slotLockId/diningAreaId/etc.) is the **new** slot's values —
  re-run §5 for the new slot's `/booking/details` + slot-lock first, and
  re-check `ccRequired`/the cancellation policy since they can differ from
  the original booking.

Response fields worth checking before trusting `confirmationNumber`:
- `partnerScaRequired: true` — the card needs 3-D Secure; can't be
  completed outside a real browser. `partnerScaRedirectUrl` is where a
  human would have to go to finish it.
- `errorCode` (with `errorMessage`) — `SLOT_LOCK_EXPIRED` means the ~90s
  lock from §5 timed out; re-run §3 → §5 → §6 with a fresh slot.

## 7. Cancel a reservation

`POST /dapi/fe/gql?optype=mutation&opname=CancelReservation` — persisted
query. Needs the `restaurantId` + `confirmationNumber` + `securityToken`
triple from §4's reservation list (or from §6's response).

```sh
cat > /tmp/ot-cancel.json <<'JSON'
{
  "operationName": "CancelReservation",
  "variables": {
    "input": {
      "restaurantId": 54232,
      "confirmationNumber": 123456789,
      "securityToken": "<security_token>",
      "databaseRegion": "NA",
      "reservationSource": "Online"
    }
  },
  "extensions": { "persistedQuery": { "version": 1, "sha256Hash": "4ee53a006030f602bdeb1d751fa90ddc4240d9e17d015fb7976f8efcb80a026e" } }
}
JSON
fpx post-json 'https://www.opentable.com/dapi/fe/gql?optype=mutation&opname=CancelReservation' \
  @/tmp/ot-cancel.json -p opentable \
  -H 'ot-page-type: network_confirmation' -H 'ot-page-group: booking' \
  | jq '.data.cancelReservation | {statusCode, state: .data.reservationState, errors}'
```

A cancel succeeded when `statusCode == 200`, `state` matches
`/cancel/i`, and `errors` is null/empty — a 200 HTTP status alone isn't
proof.

---

## Persisted-query hashes (re-capture if `PersistedQueryNotFound`)

| Operation | Hash |
|---|---|
| `RestaurantsAvailability` | `cbcf4838a9b399f742e3741785df64560a826d8d3cc2828aa01ab09a8455e29e` |
| `BookDetailsStandardSlotLock` | `1100bf68905fd7cb1d4fd0f4504a4954aa28ec45fb22913fa977af8b06fd97fa` |
| `BookDetailsExperienceSlotLock` | `363af9e3bd17efa82ad71c5808c5272603b5f1abe13b535d3beed1e6258ce504` |
| `CancelReservation` | `4ee53a006030f602bdeb1d751fa90ddc4240d9e17d015fb7976f8efcb80a026e` |

These are Apollo persisted queries — OpenTable's client sends only the
operation name + `sha256Hash`, never GraphQL text. If OpenTable redeploys
and invalidates one, the response is `PersistedQueryNotFound` instead of
data. Re-capture in the bridged Chrome tab: navigate to the page where the
op fires (e.g. `/booking/details` for the slot-lock ops), trigger it once,
then in DevTools run
`window.__APOLLO_CLIENT__.queryManager.mutationStore['1'].mutation.documentId`
(mutations) or iterate `queryManager.queries.forEach(q =>
console.log(q.document.documentId))` (queries) — Apollo's `documentId` IS
the persisted-query `sha256Hash`. `make-reservation` and the wishlist
add/remove endpoints are plain JSON REST, not GraphQL — they have no hash
to re-capture.
