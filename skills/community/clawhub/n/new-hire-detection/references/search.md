# Shape the search

Everything between reading the ICP and asking the operator to approve the
search. The only paid call in this file is the count, one per candidate URL.

## The market comes from the ICP

Read the ICP in the workspace context repo before asking anything. The four
things the search needs usually sit in it already:

| Search input      | Where it usually lives in `icp.md`            | Sales Navigator facet |
| ----------------- | --------------------------------------------- | --------------------- |
| Titles to watch   | the buying committee, the personas            | `CURRENT_TITLE`       |
| Industries        | firmographics                                 | `INDUSTRY`            |
| Company headcount | firmographics, the disqualifiers above a band | `COMPANY_HEADCOUNT`   |
| Locations         | geography                                     | `REGION`              |

With no ICP file and no company domain to derive one from, ask for exactly
those four, then write the answers into the project's `context/icp.md` rather
than only into the search. The qualifier reads that file on every company,
so an ICP that lives only in a URL leaves the agent judging against nothing.

## Titles are a boolean, exclusions are words

`CURRENT_TITLE` takes one included value holding a quoted `OR` list and any
number of excluded words. Quote every title: an unquoted `VP Sales` matches any
title with both words in it, in any order. Exclude the words that bring in the
title without the mandate (`intern`, `interim`, `fractional`, `assistant`,
`recruiter`, `student`, and the job's own false friends).

## Ids, not labels

Industry and region values are LinkedIn ids, and a wrong id is ignored
silently, which widens the search to every industry or the whole world.
Resolve each one through the integration's autocompletes:

```sh
cargo-ai connection connector list                          # the Sales Navigator connector's uuid
cargo-ai connection connector autocomplete --connector-uuid <uuid> \
  --slug listIndustries --params '{}' --value "software"
cargo-ai connection connector autocomplete --connector-uuid <uuid> \
  --slug listGeoCodes --params '{}' --value "united kingdom"
cargo-ai connection connector autocomplete --connector-uuid <uuid> \
  --slug listCompanyHeadcounts --params '{}'
```

Headcount uses letters, listed in `infra/models/new-hires.ts`.

## The job-change filters are fixed

`RECENTLY_CHANGED_JOBS`, under a year at the company, and under a year in the
position. They overlap on purpose: together they drop internal promotions at
long-tenured employees, which look like job changes and are not. Do not remove
one to widen the pool; widen the market facets instead.

## Count before you extract

`infra/models/new-hires.ts` builds the URL from the `search` object. Print it,
then count it with `searchPersonMetrics`, which returns `total_leads` for one
URL. It bills per call; quote its live price with
`cargo-ai connection integration get salesNavigator` before running it.

```sh
cargo-ai orchestration action execute --wait-until-finished \
  --action '{"kind":"connector","integrationSlug":"salesNavigator","actionSlug":"searchPersonMetrics","config":{}}' \
  --data '{"url":"<the search url>"}'
```

Open the same URL in a browser with a Sales Navigator seat if one is at hand:
the people on the first page should be the people the operator meant.

## Over 2,500, split by a facet

One search returns at most 2,500 people, and `limit: 2500` is that ceiling,
per URL. A search counting more returns its first 2,500 and never shows the
rest of the market. Split it on a facet that partitions the market cleanly
(one URL per region, or per headcount band), count each, and list every URL in
the model's `urls`. Each URL carries its own 2,500.

Splitting on a facet that overlaps (two title lists sharing a title) extracts
the shared people twice. The model dedupes them on `linkedin_profile_id`, but
both extractions are billed.

## What to show for approval

- each URL, decoded, with its facets in plain words
- each URL's count, and whether it sits under the cap
- `limit` per URL and the cadence the operator chose
- the extraction price per lead, live, and what one sync costs at that count

Stop for an explicit yes. Nothing is deployed or extracted before it.
