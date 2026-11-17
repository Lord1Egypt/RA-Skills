# homes.com request recipes

Every path below is relative to `https://www.homes.com` — `fpx` needs
the full URL. All shapes are transcribed from `homes-mcp`'s
`src/tools/*.ts` (live-verified there); nothing here is guessed.

A shared helper — save once, source before the recipes that need it:

```sh
cat > /tmp/homes-jsonld.js <<'EOF'
// Usage: node /tmp/homes-jsonld.js <html-file>
// Prints the parsed JSON-LD document (the `{ "@context", "@graph" }`
// envelope, or a synthetic one-element graph if the page emits a bare
// root node) as JSON to stdout.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
// homes.com HTML-entity-encodes the `+` in the script `type` attribute
// (`application/ld&#x2B;json`) — match both forms.
const m = html.match(/<script type="application\/ld(?:\+|&#x2B;)json">([\s\S]*?)<\/script>/);
if (!m) { console.error('no JSON-LD block found'); process.exit(1); }
const doc = JSON.parse(m[1].trim());
if (!doc['@graph'] && doc['@type']) {
  console.log(JSON.stringify({ '@context': doc['@context'], '@graph': [doc] }));
} else {
  console.log(JSON.stringify(doc));
}
EOF
```

```sh
# fetch + extract in one step
fetch_jsonld() { # $1 = full URL
  fpx get "$1" -p homes > /tmp/homes-page.html
  node /tmp/homes-jsonld.js /tmp/homes-page.html
}
```

---

## 1. Search listings

`GET /<location-slug>/[<facet-segment>/[newest/]]?price-min=<n>&price-max=<n>`

Path facets (verified live; everything except the price band is
path-based — query strings for facets other than price are stripped at
the edge):

| Filter | Path segment |
| --- | --- |
| `for_sale` + `single_family` | `/<slug>/houses-for-sale/` |
| `condo` | `/<slug>/condos-for-sale/` |
| `townhouse` | `/<slug>/townhouses-for-sale/` |
| `land` | `/<slug>/land-for-sale/` |
| `mobile` | `/<slug>/mobile-homes-for-sale/` |
| `multi_family` | `/<slug>/multi-family-for-sale/` |
| `sold` | `/<slug>/sold/` |
| `for_rent` (untyped) | `/<slug>/homes-for-rent/` |
| `for_rent` + house/condo/townhouse | `/<slug>/<type>-for-rent/` |
| `open_houses` | `/<slug>/open-houses/` |
| `new_construction` | `/new-homes/for-sale/<slug>/` (own URL root) |
| sort `newest` | append `newest/` after the facet segment |
| price band (the ONE query-string facet) | append `?price-min=<n>&price-max=<n>` (either optional, integer USD) |

`<slug>` is the free-text location lowercased/slugified (e.g.
`"Atlanta, GA"` → `atlanta-ga`, a ZIP passes through as-is).

```sh
fetch_jsonld 'https://www.homes.com/atlanta-ga/houses-for-sale/?price-min=300000&price-max=500000' > /tmp/jsonld.json
jq -r '
  .["@graph"][] | select(.["@type"] == "CollectionPage")
  | .mainEntity.itemListElement[]
  | [ (.url // .["@id"]),
      .mainEntity.address.streetAddress,
      .offers.price,
      .mainEntity.numberOfBedrooms,
      .mainEntity.numberOfBathroomsTotal,
      .mainEntity.floorSize.value
    ] | @tsv
' /tmp/jsonld.json
```

Property id = last non-empty path segment of `url` (strip `?query` /
`#fragment` first — `@id` carries a `#realestatelisting` fragment,
`url` doesn't):

```sh
jq -r '.["@graph"][] | select(.["@type"]=="CollectionPage") |
  .mainEntity.itemListElement[].url' /tmp/jsonld.json \
  | sed -E 's#[?#].*$##; s#/$##' | sed -E 's#.*/##'
```

**Cap:** homes.com SSRs ~40 listings per page even when
`mainEntity.numberOfItems` reports more — band by price / sub-area to
enumerate a busy market.

Sold/market-report page is the same shape at `/<slug>/sold/`; derive
median price + avg $/sqft yourself:

```sh
fetch_jsonld 'https://www.homes.com/brooklyn-ny/sold/' > /tmp/jsonld.json
jq '[.["@graph"][] | select(.["@type"]=="CollectionPage") | .mainEntity.itemListElement[].offers.price]
    | sort | { count: length, median: .[length/2 | floor] }' /tmp/jsonld.json
```

---

## 2. Property detail

`GET /property/<address-slug>/<propertyId>/`

```sh
fetch_jsonld 'https://www.homes.com/property/3199-delmar-ln-nw-atlanta-ga/rxrzwg0kjnr32/' > /tmp/jsonld.json
jq '.["@graph"][] | select(.["@type"][0]? == "RealEstateListing" or (.["@type"] | index("RealEstateListing")))' /tmp/jsonld.json
```

```sh
jq '.["@graph"][] | select(.["@type"] | index("RealEstateListing")) | {
  url,
  name,
  address: .mainEntity.address,
  lat: .mainEntity.geo.latitude,
  lng: .mainEntity.geo.longitude,
  beds: .mainEntity.numberOfBedrooms,
  baths: .mainEntity.numberOfBathroomsTotal,
  sqft: .mainEntity.floorSize.value,
  year_built: .mainEntity.yearBuilt,
  price: .offers.price,
  status: .offers.availability,
  date_posted: .datePosted,
  date_modified: .dateModified,
  agent: (.offers.offeredBy[0] // .offers.offeredBy)
}' /tmp/jsonld.json
```

`geo` (lat/lng) is **only** on the detail page — search-page items lack
it.

### DOM-only fields (not in JSON-LD)

homes.com also renders highlights, HOA fee, lot size, parking,
utilities, MLS id/source, tax, schools, estimated payment, and total
views as plain sectioned text on the same page (`src/tools/
properties.ts::extractDomFields`). A quick grep over the raw HTML body
text gets you most of it without a full DOM parse:

```sh
node -e '
  const html = require("fs").readFileSync("/tmp/homes-page.html", "utf8");
  const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
  const grab = (re) => (re.exec(text) || [])[1];
  console.log(JSON.stringify({
    hoa: grab(/HOA Fee:\s*\$?([0-9,]+|0)/i),
    mls_id: grab(/MLS#?:?\s*([A-Z0-9-]+)/i),
    tax: grab(/(?:Annual Tax|Property Tax|Tax(?:es)?)(?: Amount)?:?\s*\$?([0-9,]+)/i),
    estimated_payment: grab(/Estimated payment\s*\$?([0-9,]+)/i),
    total_views: grab(/Total Views\s*([0-9,]+)/i),
  }, null, 2));
'
```

For anything structural (highlights `<li>` list, schools list,
matterport/floorplan `<img>`/`<a>` URLs) you need real DOM traversal —
either `npm install node-html-parser` and mirror
`src/tools/properties.ts::extractDomFields`, or just call
`homes_get_property` on the running MCP for full parity.

---

## 3. Photo gallery

Same detail page — JSON-LD carries only one photo, so scrape `<img>`
tags and filter to the homes.com CDN, deduping by `src`:

```sh
node -e '
  const html = require("fs").readFileSync("/tmp/homes-page.html", "utf8");
  const seen = new Set();
  const out = [];
  const re = /<img\b[^>]*\bsrc="([^"]+)"[^>]*>/g;
  let m;
  while ((m = re.exec(html))) {
    const src = m[1];
    if (!src.includes("homes.com") || src.startsWith("data:") || seen.has(src)) continue;
    seen.add(src);
    out.push(src);
  }
  console.log(JSON.stringify(out.map((url, i) => ({ url, position: i + 1 })), null, 2));
'
```

---

## 4. Address typeahead (structured — the ONE JSON API)

`POST /routes/res/consumer/smartsearch/autocomplete/`, `Content-Type:
application/json`. Neither the XSRF nor AT headers the live search box
sends are required — a plain JSON POST returns 200.

```sh
cat > /tmp/body.json <<'EOF'
{
  "term": "158 raven blvd lake lure",
  "fullTerm": "158 Raven Blvd Lake Lure",
  "transactionType": 1,
  "searchTermStartIndex": null
}
EOF
fpx post-json 'https://www.homes.com/routes/res/consumer/smartsearch/autocomplete/' \
  @/tmp/body.json -p homes | jq '.suggestions.places'
```

`term` (lowercased, load-bearing) + `fullTerm` = the joined
`{address, city, state, zip}`, space-separated. `transactionType: 1` =
for-sale (mirrors the live box; not required for a 200).

Response shape — each place:

```json
{
  "n": "158 Raven Blvd, Lake Lure, NC",
  "u": "/property/158-raven-blvd-lake-lure-nc/yhepckbpqstf1/",
  "g": { "k": { "key": "yhepckbpqstf1" },
         "a": { "state": "NC", "city": "Lake Lure", "postalCode": "28746",
                "street": "158 Raven Blvd", "unit": null } }
}
```

`u` is the real detail-page path — resolve straight from it, no further
lookup needed. `g.k.key` is the same opaque property hash as the URL's
trailing segment. A nonexistent address returns `places: []`.

```sh
jq -r '.suggestions.places[] | [.u, .g.a.street, .g.a.city, .g.a.state] | @tsv' /tmp/response.json
```

**Resolution order** (mirrors `homes_get_by_address`): try this
typeahead first; if it misses, `GET /<address-city-state-zip-slug>/`
(built the same way as a search-location slug — join
`address, city, state, zip` and lowercase/dashify); if that 404s or
routes to the wrong street, fall back to a plain city/zip
`fetch_jsonld` search (§1) and fuzzy-match `mainEntity.address.
streetAddress` against your input street (whole-token match, anchored
on the street number — a same-numbered different street should not
match).

---

## 5. Combined price + tax history

Same detail page — four HTML tables (`Property History`, `Purchase
History`, `Mortgage History`, `Tax History`), each row's leading
date/year cell is a `<th scope="row">`, the rest `<td>`. Needs real
table-structure parsing (heading → nearest following `<table>`), which
is impractical as a one-off grep. Two options:

- `npm install node-html-parser` and mirror `src/tools/history.ts`
  (`parsePropertyTable(root, 'Property History')` etc. — the row
  columns per table are documented in that file's JSDoc: Property
  History is `[date, event, price, list_to_sale_pct, price_per_sqft]`,
  Purchase History is `[date, deed_type, sale_price, title_company]`,
  Mortgage History is `[date, status, loan_amount, loan_type]`, Tax
  History is `[year, tax_paid, assessment_total, assessment_land,
  assessment_improvement]`); or
- call `homes_get_history` on the running MCP when you need this data
  structured — it's the same page fetch, already parsed.

Date formats: Property History is `MM/DD/YYYY`; Purchase + Mortgage are
`MM/DD/YY` (50-year window: `00–49` → `20xx`, `50–99` → `19xx`).

---

## 6. Nearby listings

Same detail page — a tabbed, **headless** (no heading) section:

```
<section class="nearby-links-section-dt-v2">
  <ul id="nb-Property">   <!-- For Sale, ~20 entries -->
  <ul id="nb-Neighborhood">
  <ul id="nb-City">
  <ul id="nb-property">   <!-- lowercase p: Rentals, ~20 entries -->
```

Each `<li>` is `<a href="/property/<slug>/<id>/" title="<address>">`.

```sh
node -e '
  const html = require("fs").readFileSync("/tmp/homes-page.html", "utf8");
  const ulMatch = /<ul[^>]*\bid="nb-Property"[^>]*>([\s\S]*?)<\/ul>/.exec(html);
  if (!ulMatch) process.exit(0);
  const out = [];
  const seen = new Set();
  const re = /<a\b[^>]*\bhref="([^"]*\/property\/[^"]+)"[^>]*\btitle="([^"]*)"/g;
  let m;
  while ((m = re.exec(ulMatch[1]))) {
    const idMatch = /\/property\/[^/]+\/([^/]+)\/?$/.exec(m[1]);
    if (!idMatch || seen.has(idMatch[1])) continue;
    seen.add(idMatch[1]);
    out.push({ property_id: idMatch[1], url: m[1], address: m[2] });
  }
  console.log(JSON.stringify(out, null, 2));
'
```

Swap `nb-Property` for `nb-property` (lowercase) to get the Rentals
tab. No price/beds/baths/sqft/photo here — call `homes_get_property` /
§2 on a row's URL to enrich it.

---

## 7. Saved homes / saved searches (auth-gated)

Requires a signed-in `www.homes.com` tab — a missing session redirects
to `/sign-in` or serves the AWS WAF challenge interstitial instead.

```sh
fpx get 'https://www.homes.com/customer/dashboard/favorites/' -p homes > /tmp/saved.html
fpx get 'https://www.homes.com/customer/dashboard/saved-searches/' -p homes > /tmp/searches.html
```

Both pages render plain HTML cards (no JSON-LD) — property-linked
`<a href="/property/...">` inside `article`/`[class*="favorite"]`/
`[class*="saved"]` containers for favorites, and non-property `<a>`
links inside `article`/`[class*="saved-search"]` for searches. Grabbing
just the property/search links + ids:

```sh
node -e '
  const html = require("fs").readFileSync("/tmp/saved.html", "utf8");
  const seen = new Set();
  const out = [];
  const re = /<a\b[^>]*\bhref="([^"]*\/property\/[^"]+)"/g;
  let m;
  while ((m = re.exec(html))) {
    const idMatch = /\/property\/[^/]+\/([^/]+)\/?$/.exec(m[1]);
    if (!idMatch || seen.has(idMatch[1])) continue;
    seen.add(idMatch[1]);
    out.push({ property_id: idMatch[1], url: m[1] });
  }
  console.log(JSON.stringify(out, null, 2));
'
```

Price/beds/baths/sqft/status per card are DOM class-name lookups
(`.price`, `.beds`, …) — best-effort on the live site; for the full
per-card fields use `node-html-parser` mirroring
`src/tools/saved.ts::parseSavedHomes`, or call `homes_get_saved_homes`
on the running MCP.

---

## 8. Bridge health check

`GET /robots.txt` — small, public, no auth. Good smoke test for "is the
bridge/tab alive" before debugging a real query:

```sh
fpx get 'https://www.homes.com/robots.txt' -p homes
```
