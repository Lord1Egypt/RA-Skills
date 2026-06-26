# Reference — Entities & Filters

Everything you need to target OpenAlex precisely: entity types, ID prefixes, common filters, sort options, and cursor paging. **No API key.**

---

## Entity types

| Entity | Endpoint | What it is |
|--------|----------|------------|
| `works` | `/works` | Papers, preprints, datasets, books, chapters. |
| `authors` | `/authors` | People who create works. |
| `sources` | `/sources` | Journals, repositories, conference series. |
| `institutions` | `/institutions` | Universities, labs, companies. |
| `topics` | `/topics` | Fine-grained subject classification. |
| `concepts` | `/concepts` | Legacy subject hierarchy. |
| `publishers` | `/publishers` | Publishing organizations. |
| `funders` | `/funders` | Grant-giving organizations. |
| `keywords` | `/keywords` | Keyword entities. |

---

## ID prefixes

OpenAlex IDs are URLs ending in a prefixed code. The prefix encodes the entity:

| Prefix | Entity | Example |
|--------|--------|---------|
| `W` | Works | `W2741809807` |
| `A` | Authors | `A5023888391` |
| `I` | Institutions | `I63966007` |
| `S` | Sources | `S137773608` |
| `T` | Topics | `T10017` |
| `C` | Concepts | `C41008148` |
| `P` | Publishers | `P4310319965` |
| `F` | Funders | `F4320332161` |

External IDs also resolve in `openalex_get`: **DOI** (works), **ORCID** (authors), **ROR** (institutions).

---

## Common filters (works)

Filters are comma-separated and ANDed: `filter=key1:val1,key2:val2`.

| Filter key | Example | Meaning |
|------------|---------|---------|
| `publication_year` | `publication_year:2024` | Exact year. |
| `from_publication_date` | `from_publication_date:2020-01-01` | On/after date. |
| `to_publication_date` | `to_publication_date:2024-12-31` | On/before date. |
| `is_oa` | `is_oa:true` | Open access only. |
| `open_access.oa_status` | `open_access.oa_status:gold` | OA flavor (gold/green/hybrid/bronze/closed). |
| `type` | `type:article` | Work type. |
| `authorships.author.id` | `authorships.author.id:A5023888391` | By author. |
| `authorships.institutions.id` | `authorships.institutions.id:I63966007` | By institution. |
| `primary_topic.id` | `primary_topic.id:T10017` | By primary topic. |
| `primary_location.source.id` | `primary_location.source.id:S137773608` | By journal/source. |
| `cited_by_count` | `cited_by_count:>100` | Citation threshold (`>`/`<`). |
| `language` | `language:en` | Language. |

Combine freely: `publication_year:2024,is_oa:true,authorships.institutions.id:I63966007`.

---

## Sort options

| Sort | Effect |
|------|--------|
| `cited_by_count:desc` | Most cited first (impact). |
| `publication_date:desc` | Newest first. |
| `relevance_score:desc` | Best text match (use with `search`). |
| _(omit)_ | Default relevance when searching. |

---

## Page size & paging

- `per-page` (wire name, **hyphen**) max **200**. Typed tools accept `per_page` and translate.
- `page` is **capped (~10000 results)** — do not deep-page with it.

## Cursor paging (deep traversal)

1. First request: `cursor=*`.
2. Read `meta.next_cursor`; pass it as the next `cursor`.
3. Repeat until `next_cursor` is null.

```json
{ "path": "works", "params": { "filter": "publication_year:2024", "per-page": 200, "cursor": "*" } }
```

> Verification needed: confirm filter keys, oa_status values, and limits with <https://docs.openalex.org>.
