# Search — Discovery, and Why It Is the Last Resort

`/v1/search` is an index over the objects shared with the integration. It is the only way to discover an object whose id you do not have, and it is the wrong tool for anything else.

## The Call

```bash
curl -X POST 'https://api.notion.com/v1/search' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "roadmap",
    "filter": {"value": "page", "property": "object"},
    "sort": {"direction": "descending", "timestamp": "last_edited_time"},
    "page_size": 100
  }'
```

- `filter.value` is `page` or `database` — those are the only two. There is no block search.
- Omitting `query` (or sending `""`) lists everything shared with the integration, paginated. That is the workspace crawl.
- `sort` accepts only `last_edited_time`. There is no relevance ordering you can influence.

## What Search Does Not Do

| Expectation | Reality |
|---|---|
| Finds text inside pages | Matches titles; content matching is inconsistent and must not be relied on |
| Finds rows by property value | Property values are not searched at all — query the data source with a filter (`filters.md`) |
| Returns everything in the workspace | Returns only what the integration is connected to (`auth.md`) |
| Reflects the page you just created | It is an index and lags writes by seconds to longer |
| Is a stable list | Order and completeness can shift between calls; never paginate a mutation loop off search results |

The consequence: **search is for discovery once, ids after that**. Any code path that searches for a known object on every run is both slower and non-deterministic.

## The Discovery Pass

The legitimate use, run once per workspace or after a reorganization:

1. Empty-query search filtered to `database`, paginated, to enumerate reachable databases.
2. On `2025-09-03`, retrieve each database to resolve its data sources (`data-sources.md`).
3. Retrieve each schema and write its `schemas/<data-source>.md` box.
4. Record every id, name and purpose in `### Data Sources` in `memory.md`.

After that, everything runs from stored ids and the discovery pass becomes a `## Due` item, not a startup step.

## Finding One Object Fast

| You have | Do this |
|---|---|
| A Notion URL | Take the 32-hex id from it — no request needed (`pages.md`) |
| A row's title or external id | Query its data source with a filter; exact, fast, deterministic |
| A database name | Search filtered to `database`, then store the id |
| Nothing but a phrase | Search, accept the ambiguity, and confirm the hit by retrieving it |

## Trash and Archived Objects

Search excludes archived objects. A page a user "deleted" yesterday is invisible here but still retrievable by id — which is how a sync job can keep updating a page nobody can find. Check `archived`/`in_trash` on read before treating a retrieve as proof the page is live (`sync.md`).

**After a discovery pass**, write every id, name and purpose into `### Data Sources` in `~/Clawic/data/notion-api-integration/memory.md`, note anything reachable that the user did not expect under `### Known Gaps`, and record the pass date in `## Due`. A crawl whose result is not written down gets re-run every session.
