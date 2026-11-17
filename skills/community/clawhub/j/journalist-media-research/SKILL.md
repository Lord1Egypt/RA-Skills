---
name: journalist-media-research
description: Build a relevant journalist and media shortlist for a story or PR brief using Crawlora's journalists dataset, news search, and public author pages. Use to find reporters by beat or outlet, verify recent coverage, and collect published work contact channels with supporting evidence.
---

# Journalist and media research

Find reporters whose actual coverage fits a story, and explain the match.
The output is a researched media list; sending pitches is a separate action
requiring the user's request.

## Setup and requests

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It calls `https://api.crawlora.net/api/v1` with `x-api-key` and prints JSON.
Keep the key in the environment. Consult [reference/endpoints.md](reference/endpoints.md)
for exact parameters and supported enum values.

## Workflow

1. Identify the story angle, relevant beats, target audience/geography, and
   requested list size. A product category alone may need a more specific angle;
   use the user's supplied brief before asking for additional information.
2. Inspect `/datasets/journalists/facets` with `facet=outlet`, `vertical`, or
   `topic` to discover the supported roster and filter values. Search by `q`,
   `vertical`, and/or returned exact `topic`/`outlet` values. `q` searches name,
   title, and bio, not article text. Use `page_size` up to 100, within the
   10,000-record result window.
3. Retrieve promising records from `/datasets/journalists/items/{outlet}/{slug}`
   using identifiers returned by search. Keep the outlet-specific identity:
   people can change outlets or contribute to more than one.
4. Verify current affiliation and recent relevant work using `profile_url`,
   `/bing/search`, `/bing/news`, and `/web/scrape`. Search a name together with
   its outlet/domain to avoid namesakes. Confirm bylines and article dates on
   the source pages; search snippets alone are leads, not verified coverage.
5. Rank by demonstrated story fit and recency. Cite one or two relevant pieces
   per strong match when available. Mark candidates with only bio-level evidence
   as unverified rather than asserting they recently covered the topic.

```sh
scripts/crawlora.sh /datasets/journalists/facets facet=outlet vertical=tech
scripts/crawlora.sh /datasets/journalists/search vertical=tech page_size=10
# Refine with the story's terms; a topic label must come from facets:
scripts/crawlora.sh /datasets/journalists/search q=security page_size=10
```

## Output and coverage

Return a table or CSV with `name`, `outlet`, `title`, `beat`, `profile_url`,
`relevant_article_urls`, `article_dates`, `fit_reason`, `public_contact`,
`contact_source_url`, `retrieved_at`, and `verification_status`.

- The dataset covers a curated roster of supported outlets. An empty result
  does not mean no journalist covers the topic. Use public search to supplement
  the roster and label externally discovered candidates.
- Beat topics are best-effort labels. Current bylined work is stronger evidence
  than an old profile bio. Keep unknown affiliation or dates explicit.
- `contact_type=email` means an address was published on the outlet's page;
  it does not mean the mailbox is verified or the person wants a pitch.
  `social` means only a social contact channel was found; `none` means neither.
  Do not invent addresses from an outlet's email pattern.
- Preserve contactless candidates when they are strong editorial matches,
  unless contact availability is a requirement in the user's brief.
- Bound the search to the requested list size and explain any shortfall. On
  `429`, back off; retry a transient `5xx` once. Stop on `401`/`403`, check the
  application `code`, and retain successful evidence if another source fails.
