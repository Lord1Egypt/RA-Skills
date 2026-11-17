---
name: onthecheap-mcp
description: Find free and cheap things to do in a US city — daily event listings with times, prices and venues, plus searchable deals, festivals, kids activities and local guides from the On the Cheap network (Charlotte, Denver, Atlanta, Chicago, Columbus, Seattle, Kansas City, South Florida, Orlando, Portland, Richmond, Southern Maine, the Triangle). Use when the user asks what's happening locally, wants free or cheap things to do on a date or weekend, or asks about local deals, festivals, or family activities.
---

# On the Cheap

Reads the [On the Cheap](https://livingonthecheap.com) network — local guides to
free and cheap things to do across ~14 US cities. Everything is read-only and
needs no credentials.

## Always name the city

**Every tool except `otc_list_sites` takes a required `site` argument, and there
is no default.** Pick the key that matches the city the user means; if you're not
sure one exists, call `otc_list_sites` first. Common aliases work (`milehigh`,
`raleigh`, `rva`, `kc`, `southflorida`).

An unknown key is refused with the valid ones listed, so you'll never silently
read the wrong city — but do check that the key you picked is the city the user
actually asked about. Every result echoes back `site` and `site_name`.

Because the whole network is reachable, you can answer across cities in one go —
comparing a weekend in Denver and Portland is just two calls.

**Category and location ids are per-site.** Each site is a separate WordPress
install, so an id from `otc_list_categories` is only meaningful against that
same `site`. Reusing one across cities filters to something unrelated rather
than erroring.

The `national` site (Living On The Cheap) covers US-wide deals and has **no
local events calendar**. The event tools reject it with an explanatory error;
use `otc_search_posts` with `site: "national"` for national deals.

## In context groups

On an mcp-host gateway with context groups, this server is in the **family**
group. Every tool except `otc_healthcheck` carries a `_meta.mint` hint:
`otc_list_events` and `otc_events_month_overview` are `whats-on`; the article,
taxonomy and site reads are `lookup`. There are no writes.

**Nothing here is a canonical read, on purpose.** The group's "what's on?"
intent tool calls a canonical read by itself, and every events read needs a
`site` the person has not named — there is no default city, and the thirteen
sites are the network's cities rather than the person's own subjects, so they
are not published as a subject enum (that would ask the whole country). A
compound ask like "what's on for the kids this weekend, and anything cheap in
Charlotte?" therefore reaches this server through the model, which names the
city and calls `otc_list_events` per date, not through the intent tool's
fan-out. The server is a public API with no browser bridge, so the group never
answers "needs your browser open" for it.

## Picking the right tool

- **What's on for a date** → `otc_list_events` with an ISO `date`
  (defaults to today). Each listing has its time, price and venue. Add
  `free_only: true` for no-cost listings only.
- **Scan or compare a whole month** → `otc_events_month_overview`.
- **Find articles by topic, place or text** → `otc_search_posts`
  (`query`, `category`, `location`, `after`/`before`, `view?`).
- **Read one article in full** → `otc_get_post` with an id, slug, or URL.
  Add `format: "markdown"` when you need the article's links (tickets, venue
  sites, sign-up pages) or its lists and headings; plain text drops them.
- **Discover filter ids** → `otc_list_categories`, `otc_list_locations`.
- **Find which cities exist** → `otc_list_sites` (the only tool with no `site`).

## Typical flow

Pass `site` on every one of these calls.

For "what's free this weekend?", call `otc_list_events` once per date with
`free_only: true` — the events calendar is per-day, so a weekend is two calls
(three over a long weekend). Give the user the title, time and venue, and offer
`otc_get_post` on anything they want details for.

For a topic ("free museum days", "kids stuff in Lake Norman"), search instead:
resolve the category or location id first if you need to filter — against the
same `site` — then `otc_search_posts`.

## Response shape (`view`)

`otc_search_posts` takes `view: "compact" | "full"`, and **`compact` is the
default** — you get the slim shape without asking. It is the only tool here
that takes one; the other seven are covered at the end of this section.

Compact projects each result down to the fields a caller ranks or browses on:
`id`, `slug`, `date` (the day, not the timestamp), `url`, `title`, `excerpt`
(plain text, capped at 280 characters), `image`, `categories`, `locations`, and
`expired`. What it drops is the rendered `content` body — roughly 20 KB of HTML
per post, on a page of up to 100 of them. Compact also narrows the WordPress
`_fields` query parameter to that same list, so the cheap rung is cheap **on
the wire** and not merely in the response; `view: "full"` is a bigger request,
not just a bigger answer.

**Two things about the rungs that will surprise you if you don't know them:**

- **`expired` exists only on compact.** Retired deals are not deleted, they are
  recategorised — so telling a dead offer from a live one means knowing the
  site's `expired` category id, and that id differs on every install in the
  network (2, 3, 4, 379, … 16289). Compact resolves it per site and hands you
  the boolean. `full` gives you `categories` as bare numeric ids and no way to
  read them without a second lookup.
- **`full` is untouched WordPress, entities and all.** Titles and excerpts come
  back HTML-encoded (`Bashes &#8212; free supplies`) and `content.rendered` is
  raw markup, because the entity decoding and the HTML-to-text pass live in the
  projection. Full costs you legibility as well as bytes; reach for it when you
  need a field compact dropped, not as a general "give me everything".

There is deliberately **no `raw` rung**: `full` already returns the upstream
records unprojected, so a third value would silently alias one that exists.

The seven tools with no `view` each have a reason, and none of them is an
oversight:

- **`otc_get_post`** — its product *is* the article body. A projection would
  delete the thing you called it for. Its size knob is `format` instead:
  readable plain text by default, `"markdown"` to keep links, headings and
  lists (somewhat larger), `"html"` for the original markup.
- **`otc_list_events`, `otc_events_month_overview`** — the events calendar is
  not JSON. It is scraped out of server-rendered HTML into a six-field listing
  (`title`, `url`, `time`, `price`, `venue`, `is_free`), so there is no fat
  upstream payload to project away.
- **`otc_list_categories`, `otc_list_locations`** — WordPress terms, four
  fields apiece (`id`, `name`, `slug`, `count`). The ids are what you came for.
- **`otc_list_sites`** — a fixed table of the network, shipped in the server.
- **`otc_healthcheck`** — a connectivity verdict.

## Two behaviours to get right

**Month overviews are previews.** The calendar renders at most four listings
per day. In `otc_events_month_overview`, each day's `events` is a *preview*
while `total` is the day's real count — for one August that was 124 previewed
against 510 actual. Use `total` when telling the user how much is on, and call
`otc_list_events` for a date to get that day's full schedule. Never present the
preview as the complete list.

**Expired deals are hidden by default.** Retired offers are parked in an
`expired` category and excluded from searches, so results reflect things still
available. Only pass `include_expired: true` when the user is explicitly
researching past deals or history — and say so when those results are shown,
since the offers no longer stand.

## Dates

Pass dates as ISO `YYYY-MM-DD` (and months as `YYYY-MM`). The tools convert to
whatever the site expects and reject a malformed date rather than guessing.
Resolve relative dates ("this Saturday") against today before calling.
