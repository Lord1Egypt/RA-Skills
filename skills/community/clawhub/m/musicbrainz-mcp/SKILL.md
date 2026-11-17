---
name: musicbrainz-mcp
description: Search and browse the MusicBrainz music encyclopedia (artists, releases, recordings, labels, works), fetch Cover Art Archive images, resolve musicbrainz.org URLs, and — with OAuth configured — submit your own tags, ratings, and collection edits. Use when the user asks about music metadata, discographies, album/artist/recording details, MBIDs, cover art, or wants to tag/rate music on MusicBrainz.
---

# MusicBrainz

This server exposes the [MusicBrainz](https://musicbrainz.org) `/ws/2` API and the Cover Art Archive as MCP tools. Reads need no credentials; writes need OAuth (see the repo README).

## Picking the right tool

- **Find something by name** → `musicbrainz_search` with `entity` + a Lucene `query` (+ `view?`). Plain text matches the name; fielded queries work too (`artist:"Miles Davis" AND country:US`). Returns MBIDs.
- **Get full detail for a known MBID** → `musicbrainz_lookup` with `entity` + `mbid` (+ `view?`). Add `inc` for linked data, e.g. `["releases","release-groups"]` on an artist, `["recordings","labels"]` on a release, `["url-rels","tags"]` on most entities.
- **Enumerate a relationship** → `musicbrainz_browse`: every release by an artist (`entity:"release", linkedBy:"artist", mbid:<artist>`), recordings on a release, releases in a collection, etc. Takes `view?` too. This is the complete paged set (max 100/page), unlike search's fuzzy ranking.
- **Cover art** → `musicbrainz_cover_art` with a release or release-group MBID. Returns image URLs (front/back/thumbnails); errors clearly when none exist.
- **A pasted musicbrainz.org link** → `musicbrainz_resolve` with the `url` (+ `view?`).
- **Check it's working** → `musicbrainz_healthcheck`.

`view?` is optional everywhere it appears and defaults to `compact` — see [Response shape](#response-shape-view).

## Typical flow

Search to get an MBID, then lookup/browse for detail:

1. `musicbrainz_search { entity: "artist", query: "Radiohead" }` → MBID
2. `musicbrainz_browse { entity: "release-group", linkedBy: "artist", mbid: <MBID>, limit: 100 }` → discography
3. `musicbrainz_cover_art { entity: "release-group", mbid: <RG-MBID> }` → album art

## Writes (OAuth, confirmation-gated)

`musicbrainz_submit_tags`, `musicbrainz_submit_rating`, and `musicbrainz_modify_collection` modify the user's own MusicBrainz account. Each asks the user to confirm first: a confirmation prompt where the client supports one (unless the server sets `MCP_CONFIRM_ELICITATION=off`); otherwise the first call sends nothing and returns `status: "confirmation-required"` with a `preview` and a `confirmToken` — show the preview to the user and only repeat the same call with that `confirmToken` after they approve. A token works once, and changing any argument invalidates it (`DRAFT_CHANGED`: re-confirm the fresh preview). They require `MUSICBRAINZ_OAUTH_*` to be configured.

## Response shape (`view`)

`musicbrainz_lookup`, `musicbrainz_search`, `musicbrainz_browse` and
`musicbrainz_resolve` take `view: "compact" | "full"`, and **`compact` is the
default** — you get the slim shape without asking, and an unrecognised value
falls back to it rather than erroring.

**Compact here is media stripping, not a field projection.** It removes keys
named like a picture — `image`, `images`, `thumbnail`/`thumbnails`, `logo`,
`icon`, `banner`, `avatar`, and their `…Url`/`…Link`/`…Uri`/`…Src` spellings —
plus any string value that is a URL ending in an image extension. Nothing else
is touched. This server keeps **no** hand-written field list, deliberately:
there is no captured fixture of a MusicBrainz payload here, so nothing could
honestly say which of its fields are noise, and an invented list would hand you
a record with holes in it that reads like a verified answer. Do not expect
compact to name the fields it kept — it kept all of them.

**The consequence that will surprise you: on most calls compact and full come
back identical.** MusicBrainz's `/ws/2` JSON carries almost no pictures — they
live in the Cover Art Archive, behind `musicbrainz_cover_art`, which has no
`view` at all. A release's `cover-art-archive` block survives compact whole
(`artwork`, `count`, `front`, `back`): those are facts about the art, not the
art, and none of those keys is a picture name.

The one place compact does bite is `inc: ["url-rels"]`. The bare-image-URL rule
matches on the *value*, not the key, so a relation whose target ends in
`.jpg`/`.png` comes back as `url: { id }` with its **`resource` gone**, while
the wikidata relation beside it keeps its `resource` untouched. If you are
chasing image relations, ask for `view: "full"`.

`view: "full"` returns MusicBrainz's payload untouched. One shape note:
`musicbrainz_resolve` wraps it as `{entity, mbid, data}` — `data` is the lookup
payload verbatim — because resolve *is* `musicbrainz_lookup` with the MBID
parsed out of a URL, and answering it in a different shape would make the
response depend on which of two identical routes you took.

There is deliberately **no `raw` rung**. Nothing is rewritten on the way out
here, so `full` already *is* the unprojected upstream payload; a third value
would silently alias it. `view` is also never forwarded to MusicBrainz — it is
consumed by this server, not added to the query string.

The other five tools take no `view`, for three different reasons:

- **`musicbrainz_cover_art`** — its product IS the image URLs. Compact strips
  `images`/`thumbnails`, which on this tool would not shrink the response, it
  would empty it.
- **`musicbrainz_healthcheck`** — `{ok, reachable, oauth_configured, hint}` is
  already narrower than any projection.
- **`musicbrainz_submit_tags` / `musicbrainz_submit_rating` /
  `musicbrainz_modify_collection`** — a write's response is a receipt (the
  confirmation preview, or `{submitted, …}`): nothing to strip and everything
  to keep.

## In context groups

On a host that groups MCPs by context (mcp-host's context groups), this server
sits in the **family** group. It carries `lookup` hints on its reads (search,
lookup, browse, resolve, cover art) and `change` hints on its three OAuth
writes, with the words people say ("album", "artist", "song", "album art",
"rate", "my collection") as aliases.

It has **no canonical read and no subject**: MusicBrainz is a music
encyclopedia, so nothing in it answers "what's new", "what's due" or "what's
on" for a person, and it has no listable set of people or accounts to fan out
over. A compound family ask ("what's on this weekend, and who sang that song
from the party?") reaches it only for the second half, as an ordinary lookup.
It needs no browser, so it never answers "needs your browser open".

## Notes

- MusicBrainz limits clients to ~1 request/second; the server paces itself, so a big browse may take a few seconds — that's expected, not an error.
- Entity types: `area artist event genre instrument label place recording release release-group series work url`.
