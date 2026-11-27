# Sources and licences

Confidence labels: **verified** (read from the provider's own page in Nov 2026), **unverified** (general knowledge; the page could not be fetched), **check per file**. Terms change: confirm on the provider's page before a commercial channel depends on them. This is not legal advice.

| Source | Kind | Access | Key limits and duties | Confidence |
|---|---|---|---|---|
| Pexels | video, photo | API, free key, header `Authorization: KEY` | 200 requests/hour, 20,000/month; link to Pexels and credit the creator when possible; do not try to get around limits | verified |
| Pixabay | video, photo | API, free key in query | 100 requests/60 s; cache responses 24 h; no systematic bulk downloading; no permanent hotlinking; show the source | verified |
| Mixkit | video, music, sfx | website only (no API found) | "Free License" allows commercial use including YouTube without attribution; "Restricted" assets are non-commercial only, check each asset; no reselling unaltered | verified |
| Unsplash | photo | API, free key | use hotlinked URLs, call the download endpoint, credit photographer and Unsplash with UTM links; baking photos into a rendered video is not addressed, contact api@unsplash.com | verified (gap noted); opt-in only |
| Wikimedia Commons | image, video, audio | public API, no key | licence differs per file: public domain, CC BY (credit), CC BY-SA (credit and share-alike); send a descriptive User-Agent | unverified; check per file |
| Internet Archive | video, audio | public search API, no key | not automatically public domain; the uploader's rights statement is unverified; check each item | verified (caveat); check per file |

## Behaviour of the scripts

- `stock_search.py` caches every response on disk for 24 hours, stops at `--max-requests` (default 120), and never prints URLs that contain keys.
- `fetch_clips.py pick` downloads only the files chosen for scenes, with a short pause between downloads and a cap (`--max-downloads`). It does not mirror search results.
- Every used file is stored in `scene.media` with `source`, `creator`, `page_url`, `license`, `license_status`. Commons, Archive and Unsplash entries start as `check`; set `ok` only after opening `page_url` and reading the licence.
- `package_youtube.py credits` turns this into description lines and warns about unchecked files.

## Attribution text

- Pexels: `Video by NAME on Pexels - PAGE_URL`
- Pixabay: `Video by NAME on Pixabay - PAGE_URL`
- Unsplash: `Photo by NAME on Unsplash` with the photographer and Unsplash profile links (UTM parameters `utm_source=APP&utm_medium=referral`)
- Commons: creator, licence name and file page, for example `Photo by NAME, CC BY-SA 4.0, via Wikimedia Commons - PAGE_URL`. CC BY-SA can require the derivative work to carry the same licence; read the file page before using such material in a video you want to license differently.
- Even when a licence does not require credit (Mixkit Free, Pexels), crediting is good practice and costs one line.

## Practical tips

- Search with 2 to 3 concrete words ("fishing boat harbor", not "perseverance"). Abstract ideas need a visual metaphor you choose.
- Landscape clips of at least 1920 px wide look right at 1080p; the ranking prefers them. Pixabay photos are capped near 1280 px in this script, so they look soft when zoomed; use them sparingly.
- Historic or news claims: stock footage is not evidence. Use Commons or Archive items that really show the event, with licence checked, or leave it to narration and on-screen text.
- Do not use footage with recognisable logos, brands or private individuals in a context that implies endorsement or misleads. Do not use any clip whose licence you could not confirm.
- Music: use a file the user is licensed to use (Mixkit Free-licence tracks, YouTube Audio Library, their own). Put its licence and credit text in `project.json -> music`.
