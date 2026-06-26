# Prompt — Query Building

## Purpose

Turn a natural-language research request into a correct `openalex_works` (or `openalex_request`) call: resolve entities to IDs, assemble a comma-separated `filter`, pick a `sort`, and choose paging. **No API key.**

## Reusable template

```
You are querying OpenAlex (free, no key). Build the most precise query.

Request: {{user_request}}
Known constraints:
- Topic/keywords: {{topic}}
- Time window: {{from_date}} to {{to_date}} (or year {{year}})
- Open access only: {{is_oa}}        # true|false|null
- Author: {{author_name_or_id}}      # may need resolving
- Institution: {{institution_name_or_id}}  # may need resolving
- Minimum citations: {{min_citations}}      # or null
- Rank by: {{rank}}                  # citations|recency|relevance

Procedure:
1. Resolve any names to IDs via openalex_search / autocomplete; verify the match.
2. Build filter (comma = AND) from the constraints.
3. Choose sort: citations -> cited_by_count:desc; recency -> publication_date:desc; relevance -> omit + use search.
4. Set per_page (<=200); use cursor for deep paging.
5. Emit the final tool call as JSON.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{user_request}}` | The raw ask. |
| `{{topic}}` | Subject keywords or a resolved `T…` ID. |
| `{{from_date}}` / `{{to_date}}` / `{{year}}` | Time window. |
| `{{is_oa}}` | Restrict to open access. |
| `{{author_name_or_id}}` | Author (resolve to `A…`). |
| `{{institution_name_or_id}}` | Institution (resolve to `I…`). |
| `{{min_citations}}` | Threshold for `cited_by_count:>N`. |
| `{{rank}}` | Sort intent. |

## Example

Request: "Most-cited open-access deep learning papers from MIT since 2021."

Resolve: institution "MIT" → `I63966007`.

Final call:

```json
{
  "tool": "openalex_works",
  "arguments": {
    "search": "deep learning",
    "filter": "authorships.institutions.id:I63966007,from_publication_date:2021-01-01,is_oa:true",
    "sort": "cited_by_count:desc",
    "per_page": 10
  }
}
```

## Bad

```json
{ "tool": "openalex_works", "arguments": { "filter": "year=2021; oa; mit", "per_page": 5000 } }
```

Wrong: filter is not `key:value` comma-separated; `mit` is a name not an ID; `per_page` exceeds 200; no sort.

## Good

```json
{
  "tool": "openalex_works",
  "arguments": {
    "filter": "authorships.institutions.id:I63966007,publication_year:2021,is_oa:true",
    "sort": "cited_by_count:desc",
    "per_page": 25
  }
}
```

Right: resolved ID, proper `key:value` filters, valid page size, explicit sort.

> Verification needed: confirm filter keys with <https://docs.openalex.org>.
