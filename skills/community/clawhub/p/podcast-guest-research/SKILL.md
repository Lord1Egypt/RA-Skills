---
name: podcast-guest-research
description: Find podcasts suited to a proposed guest using Crawlora's podcast catalog, live show and episode data, and public show websites. Use for guest-appearance shortlists, recent-topic research, and tailored pitch angles supported by actual episodes.
---

# Podcast guest research

Find shows where the guest's expertise fits the format and recent editorial
coverage. Produce a sourced shortlist and pitch angles, preserving unknowns about
audience size, booking availability, and whether a show accepts guest proposals.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
podcast discovery, live episode lookups, and public website tools.

## Discovery and editorial fit

1. Identify the guest's expertise, credible examples, proposed subjects, language,
   audience, and geographic constraints. Use these to evaluate editorial fit.
2. Discover candidates through `/datasets/apple-podcasts-shows/search` and facets.
   Dataset `q` searches title/artist, not the episode archive. `country` describes
   the discovery storefront, not listener geography or exhaustive availability.
   `sort=popularity` follows chart seed rank; it does not measure downloads.
3. Expand topic discovery with `/apple-podcasts/episodes/search?term=...` or live
   show search. Confirm the correct show/creator and preserve the Apple show ID.
   The stored catalog is sampled from chart/search discovery, not every podcast.
4. Read `/apple-podcasts/show/{id}` and `/show/{id}/episodes` under the same
   `/apple-podcasts` prefix. Inspect recent publication dates, descriptions, and
   guest/interview evidence. Episode lists can be bounded; record what was checked.
5. When useful, resolve the same show using `/spotify-podcasts/search?q=...`.
   Pass a returned `spotify:show:...` URI to `/spotify-podcasts/show` and
   `/spotify-podcasts/show/episodes` (`offset`, `limit` up to 50). Apple numeric
   IDs and Spotify URIs are different identities; match creator/title/website
   before combining records. A show URI is needed even if marked optional.
6. Inspect the official show site or episode notes using `/web/scrape` when
   relevant. Verify booking instructions and public professional contact channels.
   Use short excerpts and distinguish descriptions from a full episode transcript;
   do not claim to have listened to an episode based only on metadata.
7. Propose an angle linked to a specific recent episode or recurring editorial
   theme. Explain the guest's contribution and the new ground it covers. A past
   interview establishes format evidence, not a promise of future bookings.

```sh
scripts/crawlora.sh /datasets/apple-podcasts-shows/search q=founder page_size=5
scripts/crawlora.sh /apple-podcasts/episodes/search \
  term="bootstrapped business" country=us limit=10
```

## Deliverable and bounds

Return show/host, canonical links and IDs, fit rationale, recent episode evidence
with dates, proposed angle, verified submission channel if available, and caveats.
Separate researched contacts from draft pitch copy; send only when requested.

- Deduplicate syndicated shows across providers using verified identity/feed
  evidence. Do not merge by a generic title alone.
- Check recency in the live episode list. A high track count or old chart seed
  does not establish an active show. Preserve missing dates and coverage gaps.
- Rankings, ratings, and episode counts do not establish audience size, audience
  demographics, sponsor rates, or conversion potential.
- Respect dataset `page_size<=100` and its 10,000-result window. Stop on repeated
  pages, exhausted offsets, or the shortlist bound. Back off on `429`, retry a
  transient `5xx` once, stop on `401`/`403`, and check application `code`.
