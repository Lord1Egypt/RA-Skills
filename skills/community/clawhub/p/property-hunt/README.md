# property-hunt

Text Plow a photo of a house for sale. It figures out which house, looks up
everything the photo doesn't show, and puts it on a private map you can open
from your Plow folder.

<!-- Requires Plow — https://plow.co -->

## What it does

- **Text a screenshot.** Zillow, Compass, a Redfin listing, a photo of a flyer —
  anything with an address on it. Plow reads the image, finds the real listing,
  and saves it.
- **Talk to it normally.** *"The one on Elm — 3 stars, needs a new roof."*
  *"Mark Oak as passed."* *"Did the Greenwich place drop?"*
- **Open the map.** `~/Plow/properties/index.html`. Every house is a pin showing
  its photo, price, and bed count, coloured by whether you're interested, have
  toured it, or passed. Click one to open the listing.

## What it doesn't need

No server. No API key. No account. No build step. Open the HTML file from Finder
and it works — the map is [Leaflet](https://leafletjs.com), bundled, and your
data is a plain JSON file the page loads directly.

Four things do go out over the network, and nothing else: the listing lookup
itself, one download of that listing's photo from whatever host it lives on,
one [Nominatim](https://nominatim.org) geocoding request per property to turn
its address into a pin, and [OpenStreetMap](https://www.openstreetmap.org/copyright)
map tiles fetched while you have the map open. Your notes and ratings never
leave your Mac.

## Requirements

This skill requires Plow — download at https://plow.co/private-preview — with
**Plow Browser enabled** (Settings → Plow Browser). Listing sites refuse plain
HTTP requests, so the lookup runs through Plow's real browser, and the map is
written to your `~/Plow` folder so you can open it in Finder.

## Your data

Everything lives in `~/Plow/properties/`:

```
data.js      every property — the file the map reads, and a readable JSON diff
photos/      one hero photo per house
index.html   the map
```

It's yours. Upgrading or removing the skill never touches it. `data.js` is plain
JSON, so you can read it, diff it, or keep it in git.

## Development

No dependencies and no build — Node 24 runs the TypeScript directly. From a repo
checkout — `install-local.ts` is not part of the published skill:

```sh
just test                         # the suite
node scripts/install-local.ts     # install this working copy into ~/Plow/skills
```

## License

MIT-0 — see [LICENSE](LICENSE).
