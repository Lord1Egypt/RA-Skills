---
name: music-release-landscape
description: Map artist discographies and comparable music releases through Crawlora Spotify artist, album, and track tools. Use for a release-cohort or catalog-positioning brief with artist/recording identity, release types, date precision, editions, and public-metric limits preserved.
---

# Music release landscape

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare public catalog releases for a specified artist/cohort, genre/topic,
release window, and album/single/appearance scope. Use supplied artists first;
search/related results are discovery leads rather than a complete scene or genre census.

## Resolve catalog identities and release types

1. Search artists and verify returned artist ID/URI, credited names, profile URL,
   and selected releases. Artist, album, track, and profile IDs/URIs are separate
   namespaces. Name similarity, related-artist suggestions, or shared playlist
   placement do not establish collaboration, label ownership, or creative influence.
2. Retrieve artist discography with explicit `type` (`album`, `single`,
   `compilation`, `appears_on`, `all`) and order, plus bounded offset/limit.
   Featured appearances and compilation credits are not the artist's own primary
   releases. Selected overview discography is not automatically the full archive.
3. Resolve selected albums and track lists with returned IDs/URIs. Preserve title,
   credited artists, release type, supplied date/date precision, label/identifiers
   when present, track sequence, duration units, edition/version cues, and sources.
   An artist/album lookup needs an identifier even when schema fields are optional.
4. Group duplicate/variant releases only with recording/edition evidence. Use an
   actual returned recording identifier when available, otherwise documented
   credits/duration/release corroboration; equal titles alone are insufficient.
   Originals, deluxe editions, remasters, live versions, clean/explicit versions,
   translations, and territorial releases can be distinct catalog objects.

```sh
scripts/crawlora.sh /spotify/artists/search q="jazz trio" limit=5
scripts/crawlora.sh /spotify/albums/search q="jazz trio" limit=5
# Use verified returned artist IDs/URIs before discography:
# scripts/crawlora.sh /spotify/artist/albums id="$ARTIST_ID" type=all order=date_desc limit=20 offset=0
```

## Compare catalog structure and observed positioning

Build a release-by-type/theme/format matrix from available catalog metadata,
keeping primary releases versus appearances and unique recordings versus edition
counts separate. Preserve year-only/month-only date precision; do not invent an
exact date or chronological order among ambiguous releases. Duration is not
listening time or streaming revenue. No guaranteed transcript/lyric/full-audio
analysis is provided here, so do not invent musical or lyrical claims from a title.

Public popularity, play/listener fields, recommendations, or charts may have
different scopes and dates. Report only supplied fields with attribution, and
do not sum duplicate-recording metrics, infer historical momentum from a single
snapshot, or treat a rank as audited streams/revenue. These routes do not supply
a complete time-series of royalties, sales, listeners, or market availability.
Return identity/grouping and date/coverage ledgers, the catalog matrix, sourced
positioning hypotheses, and unknowns. Do not reproduce copyrighted songs, download
restricted audio, contact artists, or alter playlists/accounts from this task.
