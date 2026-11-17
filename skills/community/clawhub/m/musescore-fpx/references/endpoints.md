# MuseScore endpoints for fpx

All paths are on the apex host `musescore.com` (no `www`). Every request
needs a signed-in tab with the Cloudflare challenge cleared — plain
`curl`/Node gets a "Just a moment…" 403. Live-verified shapes; taken from
`docs/MUSESCORE-API.md` and `src/*.ts` in this repo (2026-06).

`node extract-store.mjs` below refers to `references/extract-store.mjs`
(dependency-free; run it from this `references/` directory, or adjust the
path).

---

## 1. Search

```
GET https://musescore.com/sheetmusic?text=<q>&recording_type=free-download&instrument=<id>&complexity=<id>&page=<n>
```

```sh
fpx get 'https://musescore.com/sheetmusic?text=zelda&recording_type=free-download' -p musescore \
  > /tmp/search.html
node extract-store.mjs scores < /tmp/search.html \
  | jq '.[] | {id, title, composer: .composer_name, uploader: .user.name, pages: .pages_count, is_free, downloadable: .is_downloadable}'
```

Filter params (all optional besides `text`): `instrument`, `complexity`,
`genres`, `type`, `score_format`, `instrumentation`, `license`, `page`
(1-based; page 1 is the default and can be omitted).

- **`recording_type=free-download`** is MuseScore's "Free to view, play &
  download" facet — omit it to search the whole (mostly download-paywalled)
  catalog.
- **`instrument` and `complexity` are NUMERIC ids, not words.** A word
  (`instrument=piano`) matches nothing and MuseScore silently falls back to a
  "no results" recency feed. Verified ids:

  | instrument | id | | instrument | id |
  | --- | --- | --- | --- | --- |
  | piano | 2 | | flute | 22 |
  | trombone | 4 | | bassoon | 25 |
  | soprano | 6 | | saxophone alto | 54 |
  | alto | 7 | | violin | 68 |
  | accordion | 10 | | guitar | 72 |
  | harpsichord | 11 | | trombone tenor | 21 |
  | organ | 12 | | vocals / voice | 16 |
  | cornet | 13 | | baritone | 19 |
  | euphonium | 14 | | tuba | 15 |

  `complexity`: `1`=Beginner, `2`=Intermediate, `3`=Advanced.

- **The store's results array is keyed `"scores"`** — a no-match query omits
  it and emits `see_other_scores` / `no_result_scores` (a generic "see these
  instead" feed) plus a sponsored `scores_to_be_promoted` array instead.
  Always extract `scores` specifically (as above), not "the first array of
  objects", or a genuinely empty search will look like it returned results.

Per-score fields worth knowing: `id`, `user.{id,name,is_pro,is_publisher}`,
`title` (has `[b]…[/b]` + entities — decode with `decodeText`-style cleanup if
you need clean text), `composer_name`, `parts`, `pages_count`, `duration`,
`hits`/`favorite_count`/`download_count`/`comments_count`,
`instrumentations[].name`, `rating.{rating,count}`, and the flags
`is_free`/`is_downloadable`/`is_public_domain`/`is_official`/`is_purchased`.

## 2. Score detail

```
GET https://musescore.com/user/<userId>/scores/<scoreId>
```

```sh
fpx get 'https://musescore.com/user/12345/scores/67890' -p musescore > /tmp/score.html
node extract-store.mjs license --object --id 67890 < /tmp/score.html \
  | jq '{title, license, is_free, hasAccess, is_public_domain}'
```

Always pass `--id <scoreId>`: the store can carry related scores before the
one you asked for, and without it you may read another score's entitlement
flags.

The main score object is a superset of a search card — extract it via the
enclosing-object lookup on a field only the detail page carries: `license`
(slug: `all-rights-reserved`, `publicdomain`, `cc-by-sa`, …). It adds
`subtitle`, `file_score_title`, `date_created`/`date_updated` (unix),
`revisions_count`, `is_copyright_protected`. A sibling object (identify by
`measures` + `keysig`) carries `measures`, `keysig`, `duration`, `parts`,
`pages`:

```sh
node extract-store.mjs measures --object < /tmp/score.html | jq '{measures, keysig, pages, parts, duration}'
```

## 3. Resolve the official download URL (cannot fetch the bytes via fpx)

The score-detail store carries **`type_download_list`** — one `{type, url}`
entry per artifact, a **sibling of the score object** (not nested in it):

```sh
node extract-store.mjs type_download_list < /tmp/score.html \
  | jq -r '.[] | "\(.type)\t\(.url)"'
# mscz    https://musescore.com/score/download/index?score_id=67890&type=mscz&h=...
# pdf     https://musescore.com/score/download/index?score_id=67890&type=pdf&h=...
# pdf-sample  https://musescore.com/score/download/index?score_id=67890&type=pdf-sample&h=...
# mp4-sheet, mxl, mid, mp3 similarly
```

`pdf` is the full score; `pdf-sample` is a preview only.

**Entitlement to check before trusting the link works:** `is_free === true`
OR `hasAccess === true` (from the score object above). `is_free` scores
download for free even though most report `hasAccess: false`; paid scores
also list a `pdf` url but the actual file is server-gated (never automate a
purchase).

**fpx (and any server-side request) can only RESOLVE this URL, never
download the bytes.** `score/download/index` is Cloudflare-walled — a
server-side/bridge `fetch()` gets a 403 challenge — and even when it clears,
it 302-redirects **cross-origin** to a presigned S3 URL that a `fetch()`
response can't read (opaque cross-origin redirect). The MCP solves this with
`@fetchproxy/server`'s `download` capability (`chrome.downloads.download`,
which issues the request from the browser's own network stack and can follow
the redirect) — `fpx` exposes no equivalent verb. From the shell, print the
URL and open it yourself in the signed-in `musescore.com` tab; the browser's
Download button will save the real file.

## 4. Page-1 render assets (SVG / PNG) — session + Referer-gated

```
GET https://musescore.com/static/musescore/scoredata/g/<40-hex-hash>/score_0.svg
GET https://musescore.com/static/musescore/scoredata/g/<40-hex-hash>/score_0.png@0
```

The `<hash>` comes from the score-detail HTML itself — grep the raw markup
(no store parse needed):

```sh
grep -oE 'musescore\.com/static/musescore/scoredata/g/[0-9a-f]{40}/score_0\.(svg|png)' /tmp/score.html | head -1
```

Both variants share the same hash; some scores only render one of the two
(fall back to `.png@0` if `.svg` 404s). **Only page 0 (page 1) is available
this way** — pages 2+ live behind MuseScore's token-gated `/api/jmuse` and
are not freely reachable. This host is session/Referer-gated (a plain `curl`
403s even with a valid cookie) — always fetch it through `fpx`:

```sh
fpx get 'https://musescore.com/static/musescore/scoredata/g/<hash>/score_0.svg' -p musescore > page1.svg
```

## 5. Healthcheck

```sh
fpx get 'https://musescore.com/robots.txt' -p musescore
```

A quick way to confirm the bridge + pairing + cleared-Cloudflare tab are all
working before running a real query.

---

## Not reachable this way

- **Downloading the actual score bytes** — see §3; `fpx` can only resolve the
  URL. Open it in the browser instead.
- **Pages 2+ of the render preview** — gated behind `/api/jmuse`; no public
  shape is known.
- **Anything requiring a signed-in MuseScore *account* (saved libraries,
  purchases)** — this skill only covers the same anonymous read surface the
  MCP's search/metadata/resolve tools use.
