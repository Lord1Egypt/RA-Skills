# Release Editor Seeding

Full parameter reference + recipes for pre-filling the Add Release form via POST.

Official docs: https://musicbrainz.org/doc/Development/Seeding/Release_Editor
Live example: https://musicbrainz.org/static/tests/seed-love-bug.html

## Why seed

Seeding replaces ~90% of the manual form-filling work. Instead of:
- typing the title via native input setters
- pasting the artist MBID into the autocomplete, waiting, arrow-down, enter
- dismissing the auto-triggered release-group dialog
- selecting type/status/language/script/packaging/country via evaluate
- entering date via partial-date fields
- switching to Tracklist tab, opening track parser, pasting, handling duplicate-track bug
- switching to Release info tab, typing the URL
- switching to Edit note tab, typing note

You just POST a form to `/release/add` with all fields populated. The server renders the editor pre-filled. The agent only needs to click "Enter edit".

## Endpoint

POST (or GET with query string) to: `https://musicbrainz.org/release/add`

All fields optional except `name`.

## Parameters

### Release
- `name` — release title (required)
- `comment` — disambiguation
- `annotation` — multi-line
- `barcode` — string, or `none` to indicate no barcode
- `language` — ISO 639-3 (eng, deu, jpn)
- `script` — ISO 15924 (Latn, Cyrl)
- `status` — `official` | `promotion` | `bootleg` | `pseudo-release`
- `packaging` — English packaging name (e.g. `None`, `Jewel Case`, `Digipak`)

### Release group
Pick ONE of:
- `release_group` — MBID of existing RG
- `type` — RG type name in English; repeat for multiple secondary types (e.g. `Album`, `Live`). Only one primary type is kept.

### Release events (`events.x.*`, x is 0-indexed)
- `events.x.date.year`
- `events.x.date.month`
- `events.x.date.day`
- `events.x.country` — ISO country code (`US`, `GB`, `XW` for [Worldwide])

### Labels (`labels.x.*`)
- `labels.x.mbid`
- `labels.x.catalog_number`
- `labels.x.name` — used for search if no MBID

### Artist credit (release-level)
- `artist_credit.names.x.mbid` — exact artist match
- `artist_credit.names.x.name` — credited name (defaults to artist's current name)
- `artist_credit.names.x.artist.name` — search prefill (skip if mbid provided)
- `artist_credit.names.x.join_phrase` — e.g. ` & `, ` feat. `

### Mediums & tracks
- `mediums.x.format` — English format name (e.g. `Digital Media`, `CD`, `12" Vinyl`)
- `mediums.x.name` — optional medium name
- `mediums.x.track.y.name` — track title
- `mediums.x.track.y.number` — free-form (`1`, `2`, `A1`, `B2`)
- `mediums.x.track.y.recording` — MBID of existing recording (optional)
- `mediums.x.track.y.length` — `MM:SS` or integer ms

Per-track artist credits (when track artists differ from release):
- `mediums.x.track.y.artist_credit.names.z.mbid`
- `mediums.x.track.y.artist_credit.names.z.name`
- `mediums.x.track.y.artist_credit.names.z.artist.name`
- `mediums.x.track.y.artist_credit.names.z.join_phrase`

### URL relationships (`urls.x.*`)
- `urls.x.url`
- `urls.x.link_type` — integer link type ID (optional; editor prompts otherwise)

Common release link type IDs:
- 85 — Spotify
- 50 — Discogs
- 82 — allmusic
- 78 — lyrics
- 704 — Bandcamp

When unsure, omit `link_type` — MB auto-detects well-known URLs.

### Other
- `edit_note` — the edit note text
- `redirect_uri` — redirect after submission; MBID appended as `?release_mbid=<uuid>`

## x/y/z indexing rules

- Zero-indexed
- Must be consecutive starting from 0
- Each medium must have at least one track

## Delivery: POST form submission

Seed payloads often exceed URL length limits. Use POST.

### Delivery

The `seed_release.mjs` script emits a JS payload at `/tmp/openclaw/uploads/seed-release.js`. Run it from an already-loaded MB page to preserve the session cookie:

```
browser_navigate("https://musicbrainz.org/")
# then paste the .js payload contents:
browser_console(expression=<file contents>)
```

The payload builds a hidden POST form on the current page and submits it. Because the page origin is `musicbrainz.org`, cookies are sent and you land on the pre-populated release editor logged in.

### Alternative: Playwright page.evaluate

After `page.goto('about:blank')`, inject and submit a form:

```javascript
await page.evaluate((fields) => {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = 'https://musicbrainz.org/release/add';
  form.acceptCharset = 'UTF-8';
  for (const [k, v] of Object.entries(fields)) {
    const values = Array.isArray(v) ? v : [v];
    for (const val of values) {
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = k;
      input.value = val;
      form.appendChild(input);
    }
  }
  document.body.appendChild(form);
  form.submit();
}, seedFields);
```

## Example: Digital album with Spotify link

```json
{
  "name": "Album Title",
  "artist_credit.names.0.mbid": "<artist-mbid>",
  "artist_credit.names.0.name": "Artist Name",
  "type": "Album",
  "status": "official",
  "language": "eng",
  "script": "Latn",
  "packaging": "None",
  "barcode": "none",
  "events.0.date.year": "2007",
  "events.0.date.month": "7",
  "events.0.date.day": "10",
  "events.0.country": "XW",
  "mediums.0.format": "Digital Media",
  "mediums.0.track.0.name": "Track One",
  "mediums.0.track.0.number": "1",
  "mediums.0.track.0.length": "3:47",
  "mediums.0.track.1.name": "Track Two",
  "mediums.0.track.1.number": "2",
  "mediums.0.track.1.length": "2:50",
  "urls.0.url": "https://open.spotify.com/album/<id>",
  "urls.0.link_type": "85",
  "edit_note": "Added from Spotify: https://open.spotify.com/album/<id>"
}
```

## Full workflow with seeding

1. Login (same as before — `/login`, click "Log in" button, verify redirect)
2. Build seed dict from your data source (Spotify oembed, MB artist lookup for MBID)
3. Write JSON to `/tmp/seed.json`
4. `python3 scripts/build_seed_html.py /tmp/seed.json /tmp/seed.html`
5. `browser_navigate("file:///tmp/seed.html")`
6. Browser lands on release editor pre-populated
7. `browser_snapshot()` to verify: title, artist (green bg = matched), date, track count
8. Click "Enter edit" button
9. Extract MBID from redirect URL

## What seeding does NOT cover

- Login (still required before POSTing)
- Cover art upload (separate `/release/<mbid>/add-cover-art` flow — unchanged)
- Capitalization-warning checkbox (may still appear)
- Final "Enter edit" click

## Gotchas

- **Worldwide country code is `XW`** (ISO), not the numeric `240` used in the browser form's internal `country-0` select.
- **`packaging` uses the English name** (`None`, `Digipak`), not a numeric id.
- **`type` is repeatable**: pass `type=Album` + `type=Live` for secondary types.
- **Track length** accepts `MM:SS` OR integer ms. Prefer `MM:SS`.
- **Artist MBID bypasses the wrong-autocomplete bug** — no more arrow-down/enter dance.
- **No release-group dialog interruption** — seed bypasses the auto-search popup.
- **Session must already be logged in** — seeding does not authenticate.
- If MB silently rejects a value, the field just renders blank. Always `browser_snapshot` after the POST to verify before submitting.
