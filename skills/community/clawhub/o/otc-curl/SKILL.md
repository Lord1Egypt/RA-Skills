---
name: otc-curl
description: Query the On the Cheap network (charlotteonthecheap.com, milehighonthecheap.com and ~12 sister city sites) from the shell with curl and jq — daily local event listings with times/prices/venues, plus searchable articles on free and cheap things to do. Use when the user wants local event or deal data and the onthecheap MCP server is not available.
---

# On the Cheap via curl

The "on the Cheap" sites are public WordPress sites with open REST APIs and no
bot wall, so they are read directly with `curl` — **no API key, no login, no
browser bridge**. Nothing needs installing beyond `curl` and `jq`.

If the `onthecheap` MCP server is available, prefer its tools; they handle the
date-format, truncation and category-id traps below for you. This skill is the
fallback.

```bash
# Pick a city — every site below works identically.
BASE=https://www.charlotteonthecheap.com     # charlotte
# BASE=https://www.milehighonthecheap.com    # denver
# BASE=https://triangleonthecheap.com        # raleigh/durham/chapel hill
# also: atlanta, chicago, columbus, greaterseattle, kansascity, miami,
#       orlando, portlandliving, rva, southernmaine  (all *onthecheap.com)
UA='onthecheap-skill (+https://github.com/chrischall/onthecheap-mcp)'
```

## Articles — JSON

```bash
# Search (slim fields; drop _fields for full records). $EXPIRED is resolved below.
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?search=free+museum&per_page=10&categories_exclude=$EXPIRED&_fields=id,slug,date,link,title,excerpt" | jq -r '.[] | "\(.date[0:10])  \(.title.rendered)"'

# One article by slug
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?slug=<slug>" | jq -r '.[0].content.rendered'

# Filter ids
curl -sA "$UA" "$BASE/wp-json/wp/v2/categories?per_page=100&orderby=count&order=desc&_fields=id,slug,count" | jq -r '.[] | "\(.id)\t\(.count)\t\(.slug)"'
```

**Always exclude the `expired` category — and look its id up first.** Retired
deals are parked there (a third to two-thirds of a site's posts), so without
the filter you show the user offers that no longer exist.

**The id differs on every site** (`2`, `379`, `4483`, `6193`, `7803`, `16289`, …),
so never hardcode one — an id from another site matches nothing and silently
disables the filter:

```bash
EXPIRED=$(curl -sA "$UA" "$BASE/wp-json/wp/v2/categories?slug=expired&_fields=id" | jq -r '.[0].id')
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?per_page=10&categories_exclude=$EXPIRED&_fields=date,title,link"
```

Titles and excerpts come back HTML-entity-encoded (`&#8217;`, `&#8212;`). See
`references/recipes.md` for a decode filter.

## Events — HTML

Events are **not** in the REST API (`/wp-json/wp/v2/event` → 404); they are
parsed from rendered HTML. Every city site uses the same markup and routing
(the national hub, livingonthecheap.com, has no local calendar).

```bash
# One day  — note the US M-D-YYYY order
curl -sLA "$UA" "$BASE/events/view-date/7-25-2026/"

# One month
curl -sLA "$UA" "$BASE/events/calendar/08-2026/"
```

### The date format fails silently — get it right

The path is US **`M-D-YYYY`**, not ISO. An ISO date does not 404; it parses to
a nonsense timestamp and renders **January 1, 1970**, so you get confidently
wrong data:

```
/events/view-date/7-25-2026/    ->  Saturday, July 25, 2026   ✅
/events/view-date/2026-07-25/   ->  Thursday, January 1, 1970 ❌
```

Always confirm the `h2.lotc-event` heading matches the date you asked for.

### Month pages are truncated

Each calendar cell shows at most **four** listings plus a `+N more events`
link. For one August the grid rendered 124 listings against a true total of
510. Use the month view to find busy days, then fetch the day page for the
complete schedule — never present the grid as the full month.

See `references/recipes.md` for ready-to-run extraction commands.
