---
name: research
description: Run deep, multi-source research queries via the kenkyu API and get back the sources with verbatim extracts relevant to the question. Use for any question that benefits from a thorough, sourced investigation rather than a quick answer.
---

# kenkyu research API

kenkyu turns a natural-language research request into a plan, fans out parallel
searches (papers, books, web, twitter, reddit, facebook), filters and ranks the sources, and returns
every kept source with the verbatim passages relevant to your request. Read the extracts
and write the answer yourself, citing the links.

Base URL: `https://kenkyu.dev`. All endpoints are `POST` with a JSON body that
must include your `token`.

## POST /research

Body:

```json
{
  "token": "YOUR_TOKEN",
  "query": "string — an opinionated natural-language research request; be specific about the sources or angle you care about",
  "time_limit_s": "int — seconds the run may spend, minimum 40; longer = more thorough; allow more than 180 for reasonable responses and more than 500 for a serious question that is pivotal to what the user is trying to do",
  "background": "bool, default false — false blocks until the run finishes and returns the full result; true returns {research_id} immediately, poll POST /check/research; prefer true for time_limit_s over ~60 so your HTTP call doesn't sit open",
  "extra_filter": "string, default \"primary-only\" — a filter applied to every source on top of the filters the planner writes; \"primary-only\" keeps only primary sources (papers, original data, filings, listings, firsthand accounts — not journalism or summaries of them); \"for-learning\" biases toward primary sources but keeps substantive secondary ones (review papers, Wikipedia, rich explainers); \"\" applies nothing; any other string is used directly as a custom filter rule the sources must satisfy",
  "followup": "int, default 0 — research_id of one of your finished runs to build on; the new run starts with that run's kept sources already loaded, the planner reads their extracts and only searches for what the new query still misses; the result holds the combined sources; use it to drill into, extend, or re-angle a prior result without paying for the ground already covered; the original run is not modified"
}
```

Returns:

```json
{
  "research_id": "int",
  "query": "string — the request as run",
  "followup_of": "int — research_id of the run this one followed up on, 0 if standalone",
  "status": "complete | running | refused | failed | stopped",
  "cost_usd": "float — what the run cost your balance",
  "elapsed_s": "float",
  "total_sources_considered": "int — sources fetched and judged, whether kept or not",
  "errors_parsing_source": "int — non-fatal source parse failures",
  "errors_executing_queries": "int — non-fatal subquery failures",
  "sources": [
    {
      "link": "string",
      "title": "string",
      "extract": "string — verbatim passages relevant to the query",
      "content": "string — full text when available",
      "weight": "high | medium | low — importance of the subquery that found it"
    }
  ]
}
```

Errors: `401` invalid token; `402` balance too low (`/research` requires a balance
above $10); `422` the planner refused the query (detail says why — rephrase and
retry); `404` the run failed (detail holds the error).

## POST /check/research

Body:

```json
{
  "token": "YOUR_TOKEN",
  "research_id": "int — from a background: true research call",
  "include_excluded_sources": "bool, default false — when true and the run is complete, also returns an excluded_sources array of sources that were fetched but rejected by the filters"
}
```

Returns: while the run is in progress, `{research_id, query, status, error,
created_at, time_limit_s}` with `status` one of `running | refused | failed |
stopped`. Once `status` is `complete`, the same full result shape as `/research`
(plus `excluded_sources` if you asked for it). Poll every few seconds until the
status leaves `running`.

## POST /researches

Body: just `{"token": "YOUR_TOKEN"}`.

Returns every run you own, newest first:

```json
[
  {
    "research_id": "int",
    "query": "string",
    "followup_of": "int — research_id this run followed up on, 0 if standalone",
    "status": "complete | running | refused | failed | stopped",
    "created_at": "float — unix epoch seconds",
    "time_limit_s": "int",
    "icon_url": "string — cosmetic icon, may be empty"
  }
]
```

Use it to find a `research_id` you lost, see which runs are still running, or pick
a finished run to pass as `followup`. Fetch a run's full result (sources and
extracts) via `POST /check/research`.

## POST /user

Returns account info for the token, including `balance_usd`. Check it before
starting runs; `/research` needs a balance above $10.
