---
name: podcast-topic-landscape
description: Map podcast topics across public show and episode samples with Crawlora Apple Podcasts and Spotify tools. Use for a podcast editorial landscape, comparable-show topic matrix, or reading/listening shortlist with identity, sampling, description-only evidence, and audience limits preserved.
---

# Podcast topic landscape

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare editorial coverage of a topic across a specified or discovered show set.
Establish topic/synonyms, language/market, date window, show scope, and balanced
per-show episode budget. Search results and recommendations are discovery
samples rather than an exhaustive podcast universe.

## Resolve shows and sample episodes consistently

1. Discover shows through stored Apple Podcasts facets/search or live Apple/
   Spotify discovery. Resolve Apple show/episode IDs separately from Spotify
   show/episode URIs. A show URL, publisher, title, and feed URL when supplied
   can corroborate a cross-platform match; similarly named shows are insufficient.
2. Use episode search for leads, then retrieve a bounded archive from each
   selected show. Apple show episodes use its show ID; Spotify show routes use
   a returned URI, even where the schema marks it individually optional. Preserve
   each route's page/offset/limit and stopping rule; do not invent pagination fields.
3. Select comparable dates and episode types rather than only the most popular
   hits. Preserve release date, episode identity, description/title, duration,
   language, and original show/source link. A trailer, bonus, rerun, excerpt,
   and full episode should not silently count as equivalent editorial outputs.
4. Cross-platform duplicate episodes need a returned GUID/feed identity or
   corroborating title/date/duration evidence. Preserve uncertain matches and
   syndicated versions; do not double-count the same episode merely because
   Apple and Spotify both return it. Convert duration milliseconds deliberately.

```sh
scripts/crawlora.sh /apple-podcasts/episodes/search term="climate adaptation" country=us limit=10
scripts/crawlora.sh /spotify-podcasts/search q="climate adaptation" limit=10
# Resolve discovered show IDs/URIs before sampling their episode archives.
```

## Code topics without inventing the spoken content

Build a shared topic/frame rubric with multi-label and uncertain states. Mark
whether each label comes from title, publisher description, or separately verified
content. These tools do not guarantee full transcripts: do not invent quotations,
spoken arguments, guest affiliations, or sponsor endorsements from metadata.
Duration is a supplied episode measurement, not listening time or audience reach.

Return a show-by-topic matrix, episode evidence ledger with dates/URLs and coding
basis, notable positioning differences, and a listening shortlist. Topic shares
need explicit unique-episode denominators and unavailable-description counts;
multi-label counts can exceed total episodes. A missing topic is a sample gap,
not proof the show never covers it or that a new podcast has market demand.
Ratings, chart ranks, recommendations, and archive counts do not supply downloads,
listeners, revenue, or demographic composition. Do not message hosts, download
restricted audio, subscribe, or create a recurring monitor unless requested.
