# Reference — Endpoints & Tools

The 6 MCP tools and the generic passthrough pattern, mapped to OpenAlex endpoints. **No API key.**

---

## The 6 tools

| Tool | Maps to | Key inputs | Use for |
|------|---------|-----------|---------|
| `openalex_search` | `GET /{entity}?search=` | `entity`, `query`, `per_page?` | Resolve names → entities/IDs. |
| `openalex_works` | `GET /works` | `search?`, `filter?`, `sort?`, `per_page?`, `page?` | Main works queries. |
| `openalex_get` | `GET /{entity}/{id}` | `entity`, `id` | One record by OpenAlex ID / DOI / ORCID / ROR. |
| `openalex_authors` | `GET /authors` | `search?`, `filter?`, `per_page?` | Author search/filter. |
| `openalex_group_by` | `GET /{entity}?group_by=` | `entity`, `group_by`, `filter?` | Aggregated counts. |
| `openalex_request` | `GET /{path}` | `path`, `params?` | Any endpoint (full coverage). |

---

## Generic passthrough pattern (`openalex_request`)

Use when the typed tools don't cover an endpoint or parameter.

```json
{ "path": "<endpoint path>", "params": { "<wire-param>": "<value>" } }
```

- `path`: relative to base, no leading slash. Examples: `sources`, `topics`, `publishers`, `funders`, `keywords`, `concepts`, `autocomplete/institutions`, `works`.
- `params`: **wire** parameter names — `filter`, `search`, `q` (autocomplete), `sort`, `group_by`, `per-page` (hyphen), `cursor`, `select`, `sample`.

Examples:

```json
{ "path": "sources", "params": { "search": "nature" } }
{ "path": "autocomplete/institutions", "params": { "q": "mit" } }
{ "path": "works", "params": { "filter": "is_oa:true,publication_year:2024", "per-page": 5 } }
{ "path": "topics" }
```

---

## Endpoint catalog (reachable via generic tool)

| Path | Returns |
|------|---------|
| `works` | Works list. |
| `authors` | Authors list. |
| `sources` | Journals/repositories/conferences. |
| `institutions` | Institutions. |
| `topics` | Topic taxonomy. |
| `concepts` | Legacy concepts. |
| `publishers` | Publishers. |
| `funders` | Funders. |
| `keywords` | Keywords. |
| `autocomplete/{entity}` | Fast typeahead resolution. |
| `{entity}/{id}` | Single record. |

For the full, authoritative list of endpoints and parameters, consult the OpenAlex API catalog.

> Verification needed: confirm endpoint paths and parameters with the API catalog at <https://docs.openalex.org>.
