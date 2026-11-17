---
name: news-media-research
description: Researches public news from international, regional, business, technology, sports, science, and entertainment publishers through the Crawlora API — headlines, article text, search, live coverage, and section/topic archives — returning clean JSON. Use when the user wants source-specific coverage or article content without scraping pages directly.
---

# News media research

Search and read public publisher coverage as normalized JSON. This skill is
for outlet-native retrieval; use `news-briefing-research` when the task needs a
multi-source synthesis, coverage timeline, or GDELT context.

## When to use this skill

- Get the latest headlines for a section, topic, or publisher.
- Read a public article's body and metadata from its canonical URL.
- Search Financial Times or Google News, or browse a publisher's section/topic
  archive after discovering its current slugs.
- Inspect BBC/CNN live coverage or Foreign Policy project/live surfaces.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests
  to `https://api.crawlora.net/api/v1`.

## Research workflow

1. Start with the publisher's discovery surface when one exists: categories,
   sections, or topics return the current accepted slugs for the matching
   headline route. Do not invent section values.
2. Fetch a bounded headline/search page, preserve each result's canonical URL,
   publication/update time, author, and section, then pass that URL to the
   publisher's article endpoint when full text is needed.
3. Treat feeds as publisher-specific snapshots, not an exhaustive news corpus.
   For a comparison across outlets, keep each publisher's result set and
   timestamps separate before synthesizing.
4. Use live-story, project, or conversation routes only for the publisher
   surfaces that expose them; they are snapshots, not subscriptions.

Use [`reference/endpoints.md`](reference/endpoints.md) for exact parameters.

## Examples

```sh
scripts/crawlora.sh /nyt/sections | jq '.'
scripts/crawlora.sh /nyt/headlines section=world | jq '.'
scripts/crawlora.sh /nyt/article url="https://www.nytimes.com/example" | jq '.'
scripts/crawlora.sh /ft/search q="semiconductor exports" sort=date | jq '.'
scripts/crawlora.sh /reuters/news page=1 | jq '.'
scripts/crawlora.sh /foreignpolicy/live | jq '.'
```

## Limits

- Public publisher content only; subscriber-only, metered, challenged, video,
  podcast, and live-blog surfaces may be unavailable or partial.
- Preserve the source URL and the publisher's timestamps. Do not present a
  bounded feed as complete coverage or infer truth from headline agreement.
- Quote sparingly and link the original article. Use `news-briefing-research`
  for cross-source comparison and uncertainty-aware synthesis.

## Expanded publisher coverage

The reference includes regional outlets and specialist technology, science,
sports, entertainment, and business publishers in addition to the original
international set. Search it for the requested outlet before choosing a tool:
not every publisher has search, article, author, or discovery endpoints. Some
only expose a public news list. Use only that outlet's returned section/category
values and available routes; do not promise full article text from a headline
or listing-only response. Publisher archive/page filters differ across outlets.

```sh
scripts/crawlora.sh /apnews/sections
scripts/crawlora.sh /techcrunch/sections
scripts/crawlora.sh /ndtv/sections
```

If HTTP succeeds but application `code` is an error, or content is challenged,
empty, or partial, record what was actually retrieved. An unavailable article
is not proof the story does not exist. Keep source URLs and timestamps and
report bounded coverage. A section discovery result is not a complete archive.
