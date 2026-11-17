---
name: news-briefing-research
description: Builds source-aware news briefings from GDELT, BBC, CNN, The Guardian, and Yahoo News using the Crawlora API. Use for recent headlines, topic monitoring, source comparison, and coverage timelines with links, dates, and uncertainty preserved.
---

# News briefing research

Gather recent public news from multiple publishers and GDELT, then return a
dated briefing with source links and clearly separated reporting from inference.

## When to use this skill

- Summarize recent coverage of a topic, company, person, or event.
- Compare how multiple outlets frame the same story.
- Track coverage volume, sentiment, entities, or timelines in a bounded window.
- Find original article pages and live-story updates.

## Research workflow

1. Define topic terms, geography, language, date window, source set, and update
   cutoff before searching. A headline query is not a complete news corpus.
2. Search GDELT and publisher-specific endpoints separately. Deduplicate by
   canonical URL, title, publisher, and publication timestamp while retaining
   syndicated versions when they add distinct reporting.
3. Prefer the original article and record publication/update times, author,
   outlet, URL, and whether the item is an opinion, live update, or report.
4. Compare claims across sources and label unverified allegations, corrections,
   missing context, and model-generated summaries. Do not infer causality from
   co-occurrence or coverage volume.

## Examples

```sh
scripts/crawlora.sh /gdelt/search query="semiconductor exports" | jq '.'
scripts/crawlora.sh /bbc/search query="semiconductor exports" | jq '.'
scripts/crawlora.sh /cnn/search query="semiconductor exports" | jq '.'
scripts/crawlora.sh /guardian/search query="semiconductor exports" | jq '.'
scripts/crawlora.sh /yahoo-news/search query="semiconductor exports" | jq '.'
```

## Notes and limits

- Public articles and feeds only; no paywall bypass, private account access,
  or publication actions occur.
- Search indexes differ by source, region, and freshness. State the collection
  window and coverage limits rather than calling the result exhaustive.
- Quote sparingly, link the original page, and preserve corrections or updates.
- Treat sentiment and entity extraction as source-derived signals, not facts.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
