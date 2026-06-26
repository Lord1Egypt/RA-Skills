# HIDIVE provider reconnaissance

Date: 2026-03-20

This note captures live reconnaissance against HIDIVE's current web API from the OpenClaw host using staged local credentials. It is intended to shape future MAL-Updater provider work.

## Executive summary

HIDIVE is technically accessible and looks viable as a MAL-Updater provider.

Confirmed:
- authenticated API login works from Python without browser automation
- HIDIVE exposes a usable watch history endpoint
- HIDIVE home content includes a **CONTINUE WATCHING** bucket with resume-ish metadata
- token refresh exists and is policy-gated rather than hidden/broken
- the web app is built on IMG/DICE frontoffice infrastructure with a stable API base and consistent headers

Unresolved / still needs probing:
- exact API surface for **user-created watchlists** / list enumeration
- exact endpoint(s) for **continue watching** and/or richer progress state outside the home content bucket
- whether history + continue-watching together are sufficient, or whether additional playback heartbeat state is needed for best fidelity

## Confirmed platform details

### Frontend / API stack

The current HIDIVE web app uses IMG/DICE infrastructure.

Observed values:
- API base: `https://dce-frontoffice.imggaming.com/api/v2`
- realm: `dce.hidive`
- app header: `dice`
- app version observed from frontend bundle: `6.60.0`
- API key observed from frontend bundle / realm settings bootstrap: `857a1e5d-e35e-4fdf-805b-a87b6f8364bf`

Useful request headers seen/confirmed:
- `Accept: application/json, text/plain, */*`
- `Content-Type: application/json`
- `x-api-key: 857a1e5d-e35e-4fdf-805b-a87b6f8364bf`
- `app: dice`
- `x-app-var: 6.60.0`
- `Realm: dce.hidive`
- `Authorization: Bearer <authorisationToken>` after login

### Realm settings discovery

Confirmed:
- `GET /realm-settings/domain/www.hidive.com` resolves successfully and yields realm/domain settings

This is useful for future provider bootstrap logic if we want to avoid hardcoding realm metadata forever.

## Confirmed auth flow

### Login

Working login request:
- `POST /login`
- JSON body:
  - `id`
  - `secret`

This returns at least:
- `authorisationToken`
- `refreshToken`
- `missingInformationStatus`

Important finding:
- `POST /login/auth-provider/pbr` with guessed field variants was **not** the right live path for simple email/password login
- plain `POST /login` is enough

### Refresh token behavior

Confirmed:
- refresh endpoint exists at `POST /token/refresh`
- it requires:
  - `Authorization: Bearer <current authorisationToken>`
  - JSON body with `refreshToken`

Observed successful semantic response even though refresh was too early:
- HTTP `429 TOO_MANY_REQUESTS`
- message: there were still `599` seconds left on the auth token and refresh should not occur before `90` seconds left

This is actually excellent news because it proves:
- token refresh is real
- HIDIVE exposes a clear policy for when refresh is allowed
- provider code can refresh proactively near expiry instead of relogging constantly

## Confirmed user-state endpoints

### 1) watch history

Confirmed working endpoint:
- `GET /customer/history/vod?size=<n>&page=<n>`

Observed response shape:
- top-level key: `vods`
- per-item fields include:
  - `id`
  - `type`
  - `title`
  - `description`
  - `duration`
  - `watchedAt`
  - `externalAssetId`
  - `thumbnailUrl`
  - `posterUrl`
  - `favourite`
  - `episodeInformation`
  - playback/availability fields like `accessLevel`, `onlinePlayback`, etc.

Observed nested episode metadata:
- `episodeInformation.episodeNumber`
- `episodeInformation.seasonNumber`
- `episodeInformation.seasonTitle`
- `episodeInformation.seriesInformation.id`
- `episodeInformation.seriesInformation.title`

This is enough to support a normalized HIDIVE history snapshot with:
- provider series id
- provider episode id / external asset id
- series title
- season title / season number
- episode number
- watched timestamp

### 2) favourites

Confirmed working endpoint:
- `GET /favourite/vods?size=<n>&page=<n>`

Observed response shape:
- top-level keys like:
  - `events`
  - `page`
  - `totalResults`
  - `resultsPerPage`
  - `totalPages`

Current account returned zero results during recon, but the endpoint itself is real and authenticated.

Implementation status:
- MAL-Updater now treats HIDIVE favourites as the **first implemented HIDIVE watchlist surface**
- normalized watchlist entries are emitted as:
  - `status: "favorite"`
  - `list_id: "favorites"`
  - `list_name: "Favorites"`
  - `list_kind: "system"`

This does **not** solve HIDIVE custom multi-list watchlists yet, but it means the provider and core watchlist model now support list metadata cleanly and can ingest at least one real HIDIVE watchlist surface today.

### 3) continue watching / resumable content via home content

Confirmed working endpoint:
- `GET /content/home?size=100&page=1`

Observed top-level keys:
- `heroes`
- `buckets`
- paging fields

Observed home bucket names include:
- `CONTINUE WATCHING`
- `Simulcasts`
- `Trending Now`
- `Dubs`
- `Recently Added`

The `CONTINUE WATCHING` bucket is the big find.

Observed bucket structure includes:
- `bucketId`
- `name`
- `type`
- `contentList`
- `rowTypeData`
- paging metadata

Example bucket metadata:
- `name: CONTINUE WATCHING`
- `bucketId: 25401`
- `type: VOD_VIDEO`

Observed `rowTypeData` shows standard bucket rendering metadata, not additional fetch hints.

Observed `contentList` item fields include:
- `id`
- `title`
- `duration`
- `watchedAt`
- `externalAssetId`
- `contentContext`
- `episodeInformation`
- `watchStatus`
- sometimes `watchProgress`

Important nuance:
- some continue-watching items had `watchProgress`
- some items did **not** show `watchProgress` in the sampled payloads

Observed nested `contentContext` shape:
- series context entry with series id/title
- season context entry with season number / episode number / series title

This means the home content API may already be enough to capture:
- currently in-progress items
- recent watch timestamps
- series/season/episode mapping context

It may be the simplest source of resumable state even if there is a more direct resume endpoint elsewhere.

## Endpoint probes that were confirmed *not* correct

These probes returned `404 NOT_FOUND` during direct testing:
- `/watchlist`
- `/watchlist/vods`
- `/watchlist/items`
- `/watchlist/list-of-watchlists`
- `/watchlist/system-defined`
- `/watchlist/favourites`
- `/playlist`
- `/playlist/vods`
- `/customer/watchlist`
- `/customer/watchlists`
- `/customer/playlists`
- `/continue-watching/vod`
- `/customer/continue-watching/vod`
- `/resume/vod`
- `/customer/resume/vod`

These are useful negative results: the obvious REST guesses are not the live API surface.

## Watchlist / multi-list findings so far

The frontend clearly contains concepts related to:
- watchlists
- system-defined watchlist favourites mode
- watchlist playthrough behavior
- watchlists enabled
- route-level watchlist / my-list pages

However, direct API probing has **not yet** identified the underlying endpoint that enumerates user-created watchlists.

Additional findings:
- `GET /content/my-list?size=100&page=1` returned `200` but with empty `buckets`
- `GET /content/watchlists?size=100&page=1` returned `200` but with empty `buckets`
- `GET /content/watchlist?size=100&page=1` returned `200` but with empty `buckets`
- `GET /content/favourites?size=100&page=1` returned `200` but with empty `buckets`
- `GET /content/history?size=100&page=1` returned `200` but with empty `buckets`

Interpretation:
- these content routes exist, but either:
  - this account currently has no corresponding data exposed there, or
  - additional query params / route state / bucket IDs are required, or
  - the watchlist UI resolves lists through another intermediate endpoint first

Given user guidance that HIDIVE presents multiple watchlists for selection, the likely next step is to reverse the watchlist page chunk / network behavior more precisely and identify how the chosen list id gets resolved into content.

## Practical implications for MAL-Updater provider design

### What already looks strong enough for implementation

A first HIDIVE provider can likely be built around:
- login + refresh token support
- watch history ingestion via `/customer/history/vod`
- continue-watching ingestion via `/content/home`
- optional favourites ingestion via `/favourite/vods`

That would already cover:
- recent watched episodes
- likely current in-progress shows
- decent title / season / episode metadata

### What would still improve provider quality

Still worth discovering before finalizing the provider boundary:
- exact multi-watchlist enumeration and per-list contents
- richer direct resume/progress endpoint if one exists
- whether playback heartbeat state can be queried directly instead of inferred from home content

## Additional findings from final API sweep

### Token refresh contract is now effectively confirmed

Earlier probing showed the presence of `/token/refresh`; the final sweep pinned the expected shape more tightly.

Observed behavior:
- `POST /token/refresh`
- requires header:
  - `Authorization: Bearer <authorisationToken>`
- requires JSON body:
  - `refreshToken`

Server response when called too early:
- HTTP `429 TOO_MANY_REQUESTS`
- explicit message that there were still `599 seconds` left and refresh should not happen until there are `90 seconds` left

Interpretation:
- this is the real refresh path
- provider code should not refresh aggressively
- the server gives a concrete policy window that can be respected in a token manager

### Continue-watching source is confirmed usable right now

The final sweep confirmed that the home content endpoint is already a valid source of continue-watching state.

Endpoint:
- `GET /content/home?size=100&page=1`

Important observed structure:
- top-level includes `buckets`
- one bucket has:
  - `name: CONTINUE WATCHING`
  - `bucketId: 25401`
  - `type: VOD_VIDEO`
- that bucket contains `contentList`

Observed continue-watching item fields:
- `id`
- `title`
- `duration`
- `watchedAt`
- `externalAssetId`
- `episodeInformation`
- `contentContext`
- sometimes `watchProgress`
- availability/playback metadata

Observed nuance:
- not every sampled item exposed `watchProgress`
- all sampled items still exposed enough context to identify series + season + episode + last watch timestamp

Practical implication:
- even before finding a cleaner dedicated resume endpoint, `/content/home` is already useful as a normalized HIDIVE provider input for current/in-progress state

### Watchlist / playlist guessed REST endpoints still appear wrong

A broad direct probe confirmed repeated `404 NOT_FOUND` on intuitive guesses like:
- `/watchlist...`
- `/playlist...`
- `/customer/watchlists`
- `/resume...`
- `/continue-watching...`

This reinforces the idea that HIDIVE watchlist UI is likely built through:
- route-specific content composition / bucket resolution
- or a different endpoint family not named as plainly as the page routes

### Content-route probing produced useful negatives

These content routes returned `200` but empty structures on the current account:
- `/content/my-list?size=100&page=1`
- `/content/watchlists?size=100&page=1`
- `/content/my-list/watchlists?size=100&page=1`
- `/content/favourites?size=100&page=1`
- `/content/history?size=100&page=1`
- `/content/watchlist?size=100&page=1`

Interpretation:
- these paths are accepted by the backend/content router
- but they are not enough by themselves to reveal the user-created watchlists on this account
- the watchlist page likely depends on extra routing state, bucket ids, or a secondary API lookup

### Frontend bundle clues around watchlists are strong

The final sweep of the frontend bundle produced a few important architecture clues:
- app config includes `watchlistsEnabled`
- app config includes `watchlistPlaythrough`
- app config includes `systemDefinedWatchlistFavouritesMode`
- analytics event constants exist for:
  - `watchlists.add.to.list`
  - `watchlists.remove.from.list`
  - `watchlists.create`
  - `watchlists.delete`
  - `watchlists.rename`
  - `watchlists.share`
  - `watchlists.more.content`
  - `watchlists.more.lists`
- route table includes both:
  - `my-list`
  - `watchlist`
  - `watchlists`
  - `history`

Interpretation:
- multi-list watchlists are definitely a first-class product surface in the app
- they are just not exposed through the obvious endpoint guesses

### Likely watchlist discovery strategy going forward

The next likely successful probe is not more blind REST guessing.

The best next move is:
1. load the specific route chunk(s) for `watchlist` / `my-list`
2. identify the route component's concrete fetch calls / Redux actions
3. trace the exact endpoint(s) used to:
   - enumerate watchlists
   - fetch chosen watchlist contents
   - paginate more lists / more content

In other words, the remaining gap is now mostly **frontend route archaeology**, not basic provider viability.

## Recommended next probes

1. **Watchlist page traffic / route-chunk archaeology**
   - identify the exact page chunk(s) and fetch path(s) for `my-list` / `watchlists`
   - look for list enumeration, selected list ids, and per-list content resolution

2. **Continue-watching / progress fidelity**
   - inspect whether `watchProgress` is consistently present only for partially watched items
   - determine whether missing `watchProgress` implies watched/completed versus stale/home fallback data

3. **Token lifecycle**
   - record bearer token expiry claims directly and align refresh timing to the observed server rule

4. **Pagination / volume**
   - measure history pagination depth and whether older watch events remain available for meaningful backfill

## Suggested provider architecture impact

This reconnaissance supports the plan to refactor MAL-Updater into:
- **core**
  - normalized snapshot contracts
  - ingest persistence
  - mapping / queue / planning / MAL sync
- **provider modules**
  - login / token refresh
  - provider fetchers
  - provider normalization
  - provider-specific tests and session state

HIDIVE now looks like a realistic target provider module rather than a speculative one.
