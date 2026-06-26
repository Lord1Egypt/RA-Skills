---
name: opentable
description: MUST use for any OpenTable / restaurant reservation request. Two entry points — (A) discovery ("find me 3 italian places tonight"): call `list_restaurants.py` for a filtered list; (B) direct book ("reserve Carbone at 8pm", "book Park Rose for 2"): call `book.py` DIRECTLY without searching first. `book.py` is pure URL construction, no verification needed. FORBIDS writing /tmp/cdp_*.js, using exec+node for Chrome automation, web_fetch on opentable.com, raw CDP scripting, or calling list_restaurants.py to "verify" before book.py. Agent must STOP after producing the booking deep link — never click checkout, never fill forms, never submit reservations.
homepage: https://www.opentable.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "🍽️",
        "requires": { "bins": ["python3"] }
      }
  }
---

# OpenTable

## READ THIS FIRST (before any tool call)

There are two entry points. Pick ONE based on what the user gave you:

### Entry A — user is discovering ("find me...", "what's available...")
The user has NOT named a specific restaurant. Your first tool call MUST be:

```bash
python3 ~/.openclaw/skills/opentable/scripts/list_restaurants.py \
  --location "<city>" --date-time "<YYYY-MM-DDTHH:MM>" \
  --party <N> --query "<cuisine>" --limit 5
```

### Entry B — user already named a restaurant ("book Park Rose...", "reserve Carbone...")
The user HAS named a specific restaurant by name or slug. **SKIP Phase 2 entirely and go straight to Phase 4.** Call `book.py` directly — do NOT search to "verify" first:

```bash
python3 ~/.openclaw/skills/opentable/scripts/book.py \
  --rid "<slug-or-name>" \
  --date-time "<YYYY-MM-DDTHH:MM>" \
  --party <N> \
  --name "<display name>" \
  --url-path "<slug if known, else guess from name: lowercase+hyphenate+append -new-york>"
```

`book.py` is **pure URL construction** — it does not fetch OpenTable, does not verify the slot is still open, does not guarantee the restaurant exists. It builds a deep link. The user completes the reservation in OpenTable and sees any errors there. **Do NOT call `list_restaurants.py` to "verify" before calling `book.py` when the user has named a specific restaurant** — you will waste tokens and block on OpenTable rate limits.

---

**For both entry points: Do not read any HTML. Do not write any CDP script. Do not call `web_fetch` on opentable.com.** This is enforced by the skill's hard rules below.

**You are NOT allowed to:**
- Write `/tmp/cdp_*.js` or any JS file that talks to Chrome DevTools Protocol
- Run `exec node ...` or `exec python ...` where the command drives a browser
- Call `web_fetch` on any `opentable.com` URL
- Call `openclaw browser snapshot` / `click` / `fill` / `navigate` / `evaluate` directly — the skill's primitives already wrap these
- Read SKILL.md scripts via `read` — the CLI contracts in this file are authoritative

If you hit any error from `list_restaurants.py`, **stop and tell the user the error**. Do not invent a workaround.

---

## Context (one-shot OpenTable reservation workflow)

Three Python scripts do all the work; you glue them together with short user-facing messages and **stop early and often**.

## Non-negotiable definition

When the user says "**book it for me**", "**make the reservation**", "**reserve it**", or any variant, it means:

> Produce a booking deep link that the user taps in OpenTable to complete the reservation with their account and card.

It does **NOT** mean:
- ❌ Click the "Reserve" / "Confirm" / "Complete Reservation" button on OpenTable
- ❌ Fill out the diner name, phone, country code form
- ❌ Select a Standard Reservation vs Experience option
- ❌ Navigate past the search results page on the user's behalf
- ❌ Write JS / CDP scripts that drive Chrome through the booking flow

Your job ends at `book.py`'s output. The user takes it from there.

## Hard forbid list (read this first)

These are **disqualifying** — if you're about to do any of them, stop and re-read this file.

1. **Do not `exec` `node`, `python`, `curl`, or any other shell command to drive Chrome or talk to the Chrome DevTools Protocol.** OpenClaw has a native browser plugin (`openclaw browser …`). Use it. If it errors, report the error to the user — **do not** hand-roll a workaround.
2. **Do not `write` temporary JS files to `/tmp/` for browser automation.** The only scripts allowed in this flow are the three in `~/.openclaw/skills/opentable/scripts/`. No others.
3. **Do not `WebFetch` any `opentable.com` URL.** Akamai blocks it and burns your context on failure.
4. **Do not `Read` the skill's Python scripts.** The CLI contracts below are authoritative; reading the scripts wastes tokens.
5. **Do not call `openclaw browser click`, `openclaw browser fill`, `openclaw browser press`, or any other mutating browser subcommand.** Only `open`, `navigate`, and `evaluate` (the read-only ones, used by the primitive) are allowed in this skill.
6. **Do not `openclaw browser navigate` to any page under `opentable.com/booking/`, `/restref/`, or `/restaurant/profile/`.** Those are booking-flow pages. The user opens them by tapping the link `book.py` produces.
7. **Cap: max 3 `openclaw browser …` subcommand invocations per user request.** If you hit that limit and still don't have what you need, stop and report.

If the agent's reasoning ever says "let me try this a different way using CDP / exec / a JS file", **stop**. The rule is: one primitive, or a clear error back to the user. No fallbacks.

## Critical: the right profile

**Always pass `--browser-profile attached` as a top-level flag on `openclaw browser`, before the subcommand.**

| Profile | Driver | State | Use it? |
|---|---|---|---|
| `attached` | `existing-session` (chrome-mcp) | **running** with user tabs | ✅ yes |
| `openclaw` | cdp launcher port 18800 | flaky | ❌ |
| `manual` | default launcher | stopped | ❌ |
| `user` | existing-session | stopped | ❌ |

Correct: `openclaw browser --browser-profile attached open <url>`
Wrong:   `openclaw browser open --browser-profile attached <url>` (CLI syntax error)

`browser.defaultProfile = "attached"` is set in `~/.openclaw/openclaw.json`, but **still pass the flag explicitly** as insurance.

## Workflow — four phases, strict

### Phase 1 — Gather requirements (one question max)

| Field | Format | Default |
|---|---|---|
| `location` | city / neighborhood / ZIP | required |
| `date_time` | `YYYY-MM-DDTHH:MM` local | required — you parse natural language |
| `party` | integer | 2 |
| `query` | cuisine / vibe keywords | "" |

Parse "tonight 8pm" / "tomorrow 7:30" / "Friday dinner" yourself. Do not ask a separate date vs. time question — combine them.

If location is missing, ask **one** combined question: *"Where should I look and any cuisine preference? (Defaults: 2 people, tonight if you said 'tonight', otherwise tomorrow 7:30pm)"*

Stop asking questions after one clarification round. Pick reasonable defaults and move on.

### Phase 2 — Get the restaurant list (SINGLE primitive call)

Run **one command**. This navigates OpenClaw's attached browser, queries the OpenTable DOM via `evaluate`, and returns structured JSON.

```bash
python3 ~/.openclaw/skills/opentable/scripts/list_restaurants.py \
  --location "<city or neighborhood>" \
  --date-time "<YYYY-MM-DDTHH:MM>" \
  --party <N> \
  --query "<cuisine keyword, or empty>" \
  --limit 5
```

Typical latency: **~8 seconds** (navigate + evaluate). Typical output size: **<1 KB of JSON**.

If you already opened the search page in Phase 2 and just need to re-extract (e.g., the user changed filters in their tab), call it with no navigation flags and it will use the current tab:

```bash
python3 ~/.openclaw/skills/opentable/scripts/list_restaurants.py --limit 5
```

**Never orchestrate this by hand with separate `search.py` → `openclaw browser open` → `openclaw browser snapshot` calls.** The primitive does it correctly in one shot; the hand-rolled path is where the old skill burned 233 messages.

`list_restaurants.py` returns a single-line JSON:
```json
{
  "restaurants": [
    {
      "name": "Little Alley",
      "cuisine": "Chinese",
      "neighborhood": "Midtown East",
      "price": "$$$$",
      "reviews": 43,
      "slots": ["7:45 PM", "8:00 PM", "8:15 PM"],
      "url_path": "little-alley-new-york"
    },
    ...
  ],
  "count": 3
}
```

On `{"error": "...", "restaurants": [], "count": 0}`: tell the user the error and suggest adjusting criteria. **Do not retry with different params automatically** — ask first.

**Show the user a compact numbered list**, summarized to at most 5 lines total:

```
1. Little Alley — Chinese · Midtown East · $$$$ · 43 reviews
   Slots: 7:45, 8:00, 8:15
2. Hutong — Chinese · Midtown East · $$$$ · 312 reviews
   Slots: 7:45, 8:00, 8:15
3. Jaba — Taiwanese · Midtown East · $$$$ · 36 reviews
   Slots: 7:30, 8:00, 8:30
```

Ask **exactly one** question: *"Which one and what time?"* Do not recommend a pick unless the user asked. Do not describe the restaurants beyond the compact row — the user can look at OpenTable for more.

**This is a hard STOP point.** You have now used one `openclaw browser … open` and one `openclaw browser … evaluate`. That is 2 of your 3 allowed calls. **Do not make further browser calls until the user replies.**

### Phase 3 — (Skippable) parse a URL the user pasted

If the user picks a restaurant by name/number from the list, skip this phase — you already have the `url_path` from Phase 2.

If the user pastes a different OpenTable URL instead:

```bash
python3 ~/.openclaw/skills/opentable/scripts/extract_rid.py "<url>"
```

Output: `{"rid": "12345"|null, "url_path": "...", "source": "..."}`

### Phase 4 — Build the booking deep link and stop

```bash
python3 ~/.openclaw/skills/opentable/scripts/book.py \
  --rid "<rid-or-slug>" \
  --date-time "<YYYY-MM-DDTHH:MM>" \
  --party <N> \
  --name "<restaurant name>" \
  --url-path "<url_path from Phase 2>"
```

Output:
```json
{
  "restaurant": "Little Alley",
  "date_time": "2026-04-11T20:00",
  "party": 2,
  "confirm_url": "https://www.opentable.com/booking/details?...",
  "profile_url": "https://www.opentable.com/r/..."
}
```

Present it to the user **under 4 lines**:

> **Little Alley** — Saturday, April 11 at 8:00 PM for 2
>
> Tap to confirm on OpenTable: `<confirm_url>`
>
> Restaurant page: `<profile_url>`

**STOP.** Do not navigate the browser to `confirm_url`. Do not click anything. Do not verify the reservation succeeded. The user's OpenTable app or browser handles the rest.

If you're tempted to "just check if it worked" by snapshotting the page — **don't**. That's the failure mode that burned 233 messages and accidentally booked a real table last time.

## Budget tracker (re-check before every tool call)

| Resource | Limit | Why |
|---|---|---|
| `openclaw browser` invocations | **3** per user request | Anything more means you're hand-rolling a workaround |
| Clarification questions | **1** per user request | Combine or pick defaults |
| User-facing message length | **≤ 4 lines** | Bulleted lists are fine; paragraphs aren't |
| Total turn latency | **< 30 seconds** | If slower, stop and report what you have |

## Troubleshooting — the exact errors you might see

### `Navigation blocked: strict browser SSRF policy requires an IP-literal URL`

`www.opentable.com` is missing from the SSRF allowlist. One-command fix:
```bash
openclaw config set browser.ssrfPolicy.hostnameAllowlist \
  '["opentable.com","*.opentable.com","www.opentable.com"]' --strict-json \
  && openclaw gateway restart
```

### `Chrome CDP websocket for profile "openclaw" is not reachable after start`

You used `--browser-profile openclaw` (or no profile flag → it defaulted to `openclaw` before the fix). Always use `--browser-profile attached`. If you did and still see this, run:
```bash
openclaw browser reset-profile
```
…but this is a last resort; prefer fixing the command.

### `browser.request cannot mutate persistent browser profiles`

You ran a mutating browser subcommand (`click`, `fill`, `press`, etc.) against a persistent profile. This is **forbidden by this skill's hard rules** — you should only be using `open`, `navigate`, and `evaluate`. Re-read the hard forbid list.

### `list_restaurants.py` returns `{"count": 0}`

Either the location string is too narrow, the current tab isn't an OpenTable search results page, or OpenTable is showing an empty result. Common causes ranked:

1. **Narrow neighborhood names return empty.** OpenTable's search engine is picky: "Lower Manhattan" returned 0, "Manhattan" / "New York" returned 3+ for the same time+query. **If count is 0 and the location is a neighborhood, automatically widen to the city once and retry** — that's the only auto-retry allowed by this skill.
2. The tab is stuck mid-booking-flow (leftover from a prior session). Fix by re-running `list_restaurants.py` with `--location/--date-time/--party/--query` so it re-navigates.
3. The time is outside OpenTable's operating hours window (e.g. 3 AM).

Do **not** issue more browser commands beyond the single auto-widen retry to "figure out what's on the page". That path leads to runaway.

### Multi-page booking flow (for reference only — the skill doesn't automate this)

If the user manually taps the `confirm_url` from Phase 4, OpenTable routes them through:

1. `/r/<slug>` — profile page with slot buttons
2. `/booking/seating-options` — pick Atrium / Lounge / Dining Room (when restaurant has multiple rooms)
3. `/booking/details` — final form (diner pre-filled for logged-in users, card optional if `creditCardRequired=false`)
4. `/booking/confirmation?confirmationNumber=…&securityToken=…` — success page with Modify / Cancel / Add-to-calendar buttons

The URL parameter `st=Standard` vs `st=Experience` tells you whether it's a normal reservation or a prepaid menu. Prefer Standard. If the link lands on a seating page with only Experience options, warn the user that a prepaid experience is the only way in at that time.

**This is reference information for explaining to the user what they'll see after tapping the link.** The skill itself never navigates past `/r/<slug>`.

## What this skill does NOT do

- **Complete reservations automatically.** Forbidden by design. See the "Non-negotiable definition" at the top.
- **Modify or cancel existing reservations.** Send the user to OpenTable.
- **Handle waitlists / notify-me / prepaid experiences.** Skip prepaid experience rows if the user asked for a standard reservation.
- **Search beyond OpenTable.** Resy, Tock, Yelp Reservations are separate systems.
- **Fetch or parse OpenTable pages via `WebFetch`, `curl`, `urllib`, or `requests`.** Akamai blocks them. Use `list_restaurants.py` exclusively.
