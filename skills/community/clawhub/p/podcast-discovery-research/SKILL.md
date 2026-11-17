---
name: podcast-discovery-research
description: Discovers and compares public podcast shows, episodes, charts, rankings, and related programs using Apple Podcasts and Spotify Podcasts through the Crawlora API. Use for show research, guest discovery, and listening-market snapshots.
---

# Podcast discovery research

Find public podcast shows and episodes across Apple Podcasts and Spotify
Podcasts. Preserve platform IDs, chart definitions, release dates, and source
URLs when comparing programs.

## When to use this skill

- Discover shows by topic, host, language, or category.
- Inspect a show's metadata, episodes, related shows, and recent publishing.
- Compare chart or ranking snapshots within the same platform and market.
- Build a bounded guest or partnership shortlist from public episode evidence.

## Research workflow

1. Search each platform separately and resolve the platform's show ID before
   fetching episodes or related programs. Do not merge IDs across platforms.
2. Capture title, publisher, description, category, language, episode date,
   duration, URL, and retrieval time. A chart rank is a relative snapshot.
3. Compare shows only within aligned country, category, chart, and date windows.
   Do not infer downloads, audience size, or revenue from rankings.
4. For guest discovery, verify the guest in the episode metadata or linked show
   notes. Similar names and search snippets are insufficient evidence.

## Examples

```sh
scripts/crawlora.sh /apple-podcasts/search term="climate tech" | jq '.'
scripts/crawlora.sh /apple-podcasts/show/<id> | jq '.'
scripts/crawlora.sh /spotify-podcasts/search q="climate tech" | jq '.'
scripts/crawlora.sh /spotify-podcasts/show/episodes uri=<spotify-show-uri> | jq '.'
```

## Notes and limits

- Public show and episode metadata only; no playback, subscription, account,
  or download actions occur.
- Chart coverage, ranking definitions, and episode availability vary by
  platform and locale. Report the exact surface used.
- Descriptions and show notes can be promotional or incomplete; distinguish
  source claims from independently corroborated facts.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
