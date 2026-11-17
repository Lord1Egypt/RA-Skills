# Ready-to-run recipes

All verified live on 2026-07-19. Set once:

```bash
BASE=https://www.charlotteonthecheap.com   # or any sister site, see SKILL.md
UA='onthecheap-skill (+https://github.com/chrischall/onthecheap-mcp)'

# Resolve the "expired" category for THIS site — the id differs on every one
# (2, 379, 4483, 6193, 7803, 16289, …), so a hardcoded value silently matches
# nothing and serves dead deals as live.
EXPIRED=$(curl -sA "$UA" "$BASE/wp-json/wp/v2/categories?slug=expired&_fields=id" | jq -r '.[0].id // empty')
echo "expired category on this site: ${EXPIRED:-none}"
```

## Articles

### Search, formatted

```bash
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?search=free+concert&per_page=10&categories_exclude=$EXPIRED&_fields=id,slug,date,link,title,excerpt" \
| jq -r '.[] | "\(.date[0:10])  \(.title.rendered)\n    \(.link)"'
```

### Decode HTML entities

WordPress leaves entities in rendered fields (`Bashes &#8212; free supplies`).
`jq` has no HTML decoder, so pipe through Python:

```bash
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?per_page=5&categories_exclude=$EXPIRED&_fields=date,title" \
| python3 -c 'import sys,json,html
for p in json.load(sys.stdin):
    print(p["date"][:10], html.unescape(p["title"]["rendered"]))'
```

### Total match count

The count is in a header, not the body:

```bash
curl -sIA "$UA" "$BASE/wp-json/wp/v2/posts?search=free+museum&categories_exclude=$EXPIRED" | grep -i x-wp-total
```

### Filter by category and location

```bash
# Discover ids
curl -sA "$UA" "$BASE/wp-json/wp/v2/categories?per_page=100&orderby=count&order=desc&_fields=id,slug,count" | jq -r '.[] | "\(.id)\t\(.count)\t\(.slug)"'
curl -sA "$UA" "$BASE/wp-json/wp/v2/locations?per_page=100&orderby=count&order=desc&_fields=id,slug,count"  | jq -r '.[] | "\(.id)\t\(.count)\t\(.slug)"'

# Kids events (4) in Lake Norman (6264), published this year
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?categories=4&locations=6264&after=2026-01-01T00:00:00&per_page=20&categories_exclude=$EXPIRED&_fields=date,title,link" \
| jq -r '.[] | "\(.date[0:10])  \(.title.rendered)"'
```

The `jq` one-liners above print titles exactly as WordPress returns them, so
entities show through (`Turtle &amp; Tortoise`, `Birkdale Buds &#8212; free`).
Swap in the Python decoder from "Decode HTML entities" before showing titles to
a user.

**Term ids are per-site — always look them up rather than reusing these.** For
Charlotte (2026-07-19) they happened to be: categories `charlotte-kids` 4,
`charlotte-music` 35, `charlotte-food` 5, `festivals` 45, `museums` 13;
locations `center-city` 6276, `lake-norman` 6264, `south-end` 6260. The same
slugs carry completely different ids on Denver or Atlanta, so the discovery
commands above are the reliable path.

`after`/`before` compare against a full timestamp, so widen a bare date:
`after=YYYY-MM-DDT00:00:00`, `before=YYYY-MM-DDT23:59:59`. Without the time on
`before`, that day's own posts are dropped.

### Full text of one article

```bash
curl -sA "$UA" "$BASE/wp-json/wp/v2/posts?slug=dippin-dots-ice-cream-day" \
| python3 -c 'import sys,json,html,re
p=json.load(sys.stdin)[0]
print(html.unescape(p["title"]["rendered"])); print(p["link"]); print()
print(re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",p["content"]["rendered"]))).strip())'
```

## Events

### One day, as a table

Convert the ISO date to `M-D-YYYY` first — an ISO path silently returns 1970.

```bash
day() {                       # usage: day 2026-07-25
  local iso="$1"
  local path
  path=$(python3 -c "import sys;y,m,d=sys.argv[1].split('-');print(f'{int(m)}-{int(d)}-{y}')" "$iso")
  curl -sLA "$UA" "$BASE/events/view-date/$path/" \
  | python3 -c '
import sys,re,html
h=sys.stdin.read()
head=re.search(r"<h2 class=\"lotc-event\">(.*?)</h2>",h,re.S)
print("==", html.unescape(re.sub("<[^>]+>","",head.group(1))).strip() if head else "(no heading)")
# Split on the row marker as a REGEX, not a literal string: a featured listing
# carries an extra class ("lotc-v2 row event featured"), so an exact-string
# split silently drops it. Then read each row via its anchor and meta, since a
# featured row also nests its text beside an image column.
for row in re.split(r"<div class=\"lotc-v2 row event[^\"]*\">",h)[1:]:
    a=re.search(r"<h3><a href=\"([^\"]+)\"[^>]*>(.*?)</a>",row,re.S)
    m=re.search(r"<p class=\"meta\">(.*?)</p>",row,re.S)
    if not a: continue
    title=html.unescape(re.sub("<[^>]+>","",a.group(2))).strip()
    segs=[s.strip() for s in html.unescape(re.sub("<[^>]+>","",m.group(1))).split("|") if s.strip()] if m else []
    time=segs[0] if segs else ""
    if len(segs)>=3: price,venue=segs[1],segs[2]
    elif len(segs)==2: price,venue=("",segs[1]) if not re.match(r"^(FREE|\$)",segs[1],re.I) else (segs[1],"")
    else: price=venue=""
    print(f"{time:22} {price:14} {title[:58]:60} {venue[:34]}")'
}

day 2026-07-25
```

Two shapes the parsing must survive, both present on the live site:

- **Two-segment meta.** A listing with no price emits `All Day | AMC Theatres,
  participating locations`. Reading segment two positionally reports the venue
  as the price — hence the `FREE|$` check above.
- **Featured listings** differ twice over: they carry an extra class
  (`lotc-v2 row event featured`) and nest their text in a `col-sm-9` column
  beside an image column instead of a plain `col-sm-12`. Matching the row class
  as an exact string drops them — 2026-07-25 has 38 listings but reports 37.
  Hence the `[^"]*` in the split pattern above.

### Free listings only

```bash
day 2026-07-25 | grep -i 'FREE'
```

### Month overview with true per-day counts

```bash
month() {                     # usage: month 2026-08
  local mm=${1#*-} yyyy=${1%-*}
  curl -sLA "$UA" "$BASE/events/calendar/$mm-$yyyy/" \
  | python3 -c '
import sys,re
h=sys.stdin.read()
total=0
for cell in re.findall(r"<td class=\"calendar-day\">(.*?)</td>",h,re.S):
    d=re.search(r"view-date/(\d{1,2})-(\d{1,2})-(\d{4})",cell)
    if not d: continue
    shown=len(re.findall(r"<div class=\"lotc-v2 row event[^\"]*\">",cell))
    more=re.search(r"\+\s*(\d+)\s*more",cell)
    n=shown+(int(more.group(1)) if more else 0)
    total+=n
    print(f"{d.group(3)}-{int(d.group(1)):02d}-{int(d.group(2)):02d}  {n:3d} events" + ("  (cell shows %d)"%shown if more else ""))
print(f"\nmonth total: {total}")'
}

month 2026-08
```

Expected for Charlotte in one August: 31 days, **510** events total, while the
grid itself rendered only 124 — the difference is the `+N more` overflow. Always report the
computed total, and fetch the day page for a complete listing.
