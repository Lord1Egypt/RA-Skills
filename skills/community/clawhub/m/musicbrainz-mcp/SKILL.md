---
name: musicbrainz-mcp
description: Search and browse the MusicBrainz music encyclopedia (artists, releases, recordings, labels, works), fetch Cover Art Archive images, resolve musicbrainz.org URLs, and — with OAuth configured — submit your own tags, ratings, and collection edits. Use when the user asks about music metadata, discographies, album/artist/recording details, MBIDs, cover art, or wants to tag/rate music on MusicBrainz.
---

# MusicBrainz

This server exposes the [MusicBrainz](https://musicbrainz.org) `/ws/2` API and the Cover Art Archive as MCP tools. Reads need no credentials; writes need OAuth (see the repo README).

## Picking the right tool

- **Find something by name** → `musicbrainz_search` with `entity` + a Lucene `query`. Plain text matches the name; fielded queries work too (`artist:"Miles Davis" AND country:US`). Returns MBIDs.
- **Get full detail for a known MBID** → `musicbrainz_lookup` with `entity` + `mbid`. Add `inc` for linked data, e.g. `["releases","release-groups"]` on an artist, `["recordings","labels"]` on a release, `["url-rels","tags"]` on most entities.
- **Enumerate a relationship** → `musicbrainz_browse`: every release by an artist (`entity:"release", linkedBy:"artist", mbid:<artist>`), recordings on a release, releases in a collection, etc. This is the complete paged set (max 100/page), unlike search's fuzzy ranking.
- **Cover art** → `musicbrainz_cover_art` with a release or release-group MBID. Returns image URLs (front/back/thumbnails); errors clearly when none exist.
- **A pasted musicbrainz.org link** → `musicbrainz_resolve`.
- **Check it's working** → `musicbrainz_healthcheck`.

## Typical flow

Search to get an MBID, then lookup/browse for detail:

1. `musicbrainz_search { entity: "artist", query: "Radiohead" }` → MBID
2. `musicbrainz_browse { entity: "release-group", linkedBy: "artist", mbid: <MBID>, limit: 100 }` → discography
3. `musicbrainz_cover_art { entity: "release-group", mbid: <RG-MBID> }` → album art

## Writes (OAuth, confirm-gated)

`musicbrainz_submit_tags`, `musicbrainz_submit_rating`, and `musicbrainz_modify_collection` modify the user's own MusicBrainz account. Each returns a **dry-run preview** unless called with `confirm: true` — show the preview to the user and only re-call with `confirm: true` after they approve. They require `MUSICBRAINZ_OAUTH_*` to be configured.

## Notes

- MusicBrainz limits clients to ~1 request/second; the server paces itself, so a big browse may take a few seconds — that's expected, not an error.
- Entity types: `area artist event genre instrument label place recording release release-group series work url`.
