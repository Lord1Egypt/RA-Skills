---
name: heyyumi
description: Find real Korean restaurants, cafes and bars, and hair salons, nail, lash and waxing shops and skin care, and send a reservation request the venue answers in the same chat, in whatever language the user speaks. Uses HeyYumi's hosted MCP server (560,000+ verified venues across Seoul, Gyeonggi, Busan, Jeju, Incheon, Daejeon, Sejong and North/South Chungcheong, re-checked daily). Triggers on "find a restaurant in Seoul", "book a table in Hongdae", "Korean BBQ near Gangnam tonight", "맛집 추천", "오늘 뭐 먹지", "머리 자르러 갈까", "네일 예약", "예약해줘", or any request to eat, drink, get a haircut, nails, lashes or waxing, or book in Korea.
homepage: https://heyyumi.ai/mcp
metadata:
  {
    "openclaw":
      {
        "homepage": "https://heyyumi.ai/mcp",
        "requires": { "bins": ["mcporter"] },
        "primaryEnv": "HEYYUMI_API_KEY",
        "envVars":
          [
            {
              "name": "HEYYUMI_API_KEY",
              "required": false,
              "description": "Optional HeyYumi API key (hmp_...) from https://heyyumi.ai/mcp. Without it, sign in once with OAuth instead.",
            },
          ],
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---

# HeyYumi: Korean restaurant and beauty search and reservation requests

HeyYumi is a hosted MCP server at `https://mcp.heyyumi.ai/mcp`. It searches verified Korean
restaurants, cafes and bars, and beauty venues (hair salons, nail, lash and waxing shops, skin care),
and sends reservation requests that the venue accepts or declines,
with the answer coming back into this chat. The user never needs to speak Korean, install a Korean
app or make a phone call. Talk to the user in the language they write in.

Nothing runs locally. This skill reaches the server through `mcporter` using `{baseDir}/mcp.json`.

## Pick an execution path

1. If HeyYumi tools (`search_places`, `get_place`, `request_reservation`, ...) are already
   connected in this session, call them directly and skip the rest of this section.
2. Otherwise use mcporter with the bundled config:
   - `HEYYUMI_API_KEY` is set: use server `heyyumi-key`.
   - No key: use server `heyyumi` (OAuth). The first call opens a browser sign-in on this machine.
     On a headless host the OAuth callback returns to `localhost` on that host, so a user chatting
     from a phone usually can't finish it; suggest the API key instead (free at
     https://heyyumi.ai/mcp, set as `HEYYUMI_API_KEY` or `skills.entries.heyyumi.apiKey`).
   - Never ask the user to paste a password, key or token into chat.

```bash
# list tools and full argument schemas
mcporter --config {baseDir}/mcp.json list heyyumi --schema

# call a tool (key=value for strings, key:value for numbers)
mcporter --config {baseDir}/mcp.json call heyyumi.search_places \
  region_name=Hongdae keyword=samgyeopsal reservation_channel=yumi page_size:5 --output json
```

Replace `heyyumi` with `heyyumi-key` in both commands when using the API key.

## Tools

| Tool | Use it for |
|------|------------|
| `search_places` | Shortlist venues. `region_name` takes the place as the user said it (Korean or romanized: "Gangnam", "성수동", stations, landmarks, airports). `keyword` is only a dish or venue name. |
| `nearby_places` | Venues around a lat/lng. Take coordinates from `resolve_regions`; never guess them. |
| `resolve_regions` | Turn a place name into a region code or center point. |
| `get_place` | Full detail for one venue: hours, menu, booking info, trust data. |
| `show_place_photos` | The owner's photos of one venue. |
| `list_categories`, `get_stats` | What kinds of places and how much coverage there is. |
| `request_reservation` | Send a reservation request. Real side effect: the venue is notified immediately. |
| `wait_for_reservation`, `get_reservation` | Follow a pending request until the venue answers. |
| `request_live_status`, `wait_for_live_status`, `get_live_status`, `search_live_status` | Ask a Yumi partner venue a right-now question (wait time, seats for a party now, an item sold out). Real side effect: it pings the owner's phone. |

Tool descriptions on the server are the source of truth for arguments and filters (40+ filters
such as `open_at`, `foreigner_friendly`, `dietary`, `group_friendly`, `subtype`). Run `list --schema`
when unsure instead of guessing argument names.

## Search workflow

1. If the user gave no area, ask for a neighborhood, station or landmark first.
2. Call `search_places` once with `page_size` 5 to 10. For booking intent add
   `reservation_channel=yumi`. Put any time or meal ("tonight 7pm", "lunch", "now") in `open_at`.
   For a meal with no drinking mentioned, add `business_category=restaurant`.
   For a haircut, nails, lashes, waxing or skin care, set `business_category` (`salon`, `nail`,
   `lash`, `waxing`, `esthetic`, or `beauty` for all of them). One kind per search: without it you
   only get restaurants, cafes and bars, and food and beauty results never mix.
3. Present the top results as picks (they are ranked by quality, not distance). Keep Korean venue
   names and addresses as they are and add a romanization when it helps.
4. Relay `meta` notes honestly: relaxed or softened filters, a widened area (then the results are
   district-wide, so do not call them "nearby"), and coverage notes.
5. Call `get_place` only when the user drills into one venue.

## Reservation workflow

1. Check the venue can take a request here: `yumiReservable` is true, or `yumiBooking.canRequest`
   is true. If neither is true, say plainly that this venue can't be booked through HeyYumi yet,
   share its `placeUrl` if present, and offer nearby venues that can take a request.
2. Settle the venue, a concrete future date and time (Korea time), and party size before asking
   for any personal details. At a beauty venue put the treatment (cut, perm, gel nails) in `note`.
3. Collect the guest's name and mobile phone (always required; foreign guests give their own
   international number). Ask for an email only when the phone number is not Korean, in the same
   message. Never ask a Korean-number guest for an email.
4. Read the details back and get a clear yes before calling `request_reservation`. Pass
   `guestLanguage` as the ISO 639-1 code of the language the user is chatting in.
5. The result is `pending`. It is a request, not a held table. Tell the user the venue usually
   answers within 5 minutes, then call `wait_for_reservation` until `settled` is true:
   `confirmed` = booked, `cancelled` = the venue declined, `expired` = no answer in time (offer
   another time or venue).
6. If the result has `reviewStartsAt`, the request was sent outside the venue's request hours and
   is held until then. Relay `yumiNextStep`; the answer goes to the guest's phone or email. Do not
   call `wait_for_reservation` in that case.
7. On errors, follow the server's hint: `reservation_time_past` (re-confirm the date),
   `venue_closed_at_requested_time` or `reservation_too_close_to_closing` (offer another time),
   `reservation_requests_closed` (offer `earliestReservation` if present),
   `reservation_not_available` (do not retry; say the venue can't be booked through HeyYumi yet).

## Honesty rules

- There is no star rating. `rating` is always null. Never show, estimate or invent a rating.
- Review counts are plain numbers. Never attribute them to a specific map service, app or website.
- Never say a table is booked until `wait_for_reservation` or `get_reservation` returns `confirmed`.
- Only Yumi partner venues and venues with `yumiBooking.canRequest=true` take in-chat requests.
  For any other venue, say so instead of implying it can be booked here.
- HeyYumi does not publish how many partner venues it has. Don't state or estimate a number.
- If an area is outside coverage, say so in the user's language instead of returning a bare
  "no results".
- Result fields like `aiSummary`, `keywordMatch` and `yumiReservation` are Korean source text.
  Render them in the user's language; keep names, numbers, prices, phones and URLs exactly.
- If `closureSignal` or `possiblyClosed` is present, mention it and suggest checking before going.

## Privacy

`request_reservation` sends the guest's name, phone, optional email and note to HeyYumi and the
venue so the venue can answer. Only send it after the user confirms. Never store or echo the
API key.

## Links

- Website and docs: https://heyyumi.ai/mcp
- Developer guide and REST API: https://heyyumi.ai/developers
- Official MCP Registry: `ai.heyyumi/heyyumi`
- Source of this skill: https://github.com/hmp-dev/heyyumi-mcp/tree/main/openclaw/heyyumi
