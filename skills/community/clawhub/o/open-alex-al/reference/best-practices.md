# Reference — Best Practices

Do these things to use OpenAlex accurately, politely, and efficiently. **No API key required**; set `OPENALEX_MAILTO` for the polite pool.

---

## Discovery

- **Resolve first.** Turn names/titles/keywords into entity IDs with `openalex_search` or `autocomplete/{entity}` before building queries.
- **Verify the match.** Confirm `display_name`, affiliation, and `works_count` before committing to an ID — names are ambiguous.
- **Cache resolved IDs** so you don't re-search the same entity.

## Filters

- **Always filter.** Never run broad, unfiltered scans of `/works`.
- Combine filters with commas (AND): `publication_year:2024,is_oa:true,authorships.institutions.id:I63966007`.
- Use **date ranges** for spans (`from_publication_date`/`to_publication_date`) and `cited_by_count:>N` for impact thresholds.
- Prefer `filter` for precise criteria; use `search` for fuzzy text.

## Polite pool

- **Set `OPENALEX_MAILTO`** in every environment. It moves traffic to the polite pool — faster and far fewer `429`s.
- Use a monitored team mailbox in production.

## Citation

- Cite **title, authors, year, source, DOI, and OpenAlex ID/URL** (`https://openalex.org/<ID>`).
- Offer `open_access.oa_url` when `is_oa` is true (free full text).
- Reconstruct abstracts from `abstract_inverted_index` before quoting.

## Caching

| Cache | TTL |
|-------|-----|
| Resolved IDs (name → `A…`/`I…`/`T…`) | Long (days). |
| Single records (`openalex_get`) | Hours–days. |
| Query results (`openalex_works`) | Short–medium. |
| Aggregates (`group_by`) | Medium. |

Caching reduces load and `429` risk; remember data refreshes frequently.

## Integrity

- Report **only** what the API returns. Never invent papers, authors, DOIs, or counts.
- Keep `meta.count` (total) separate from listed `results` (one page).
- If empty, say so and broaden — do not pad results.
- Note that figures are point-in-time (data updates often).

## Cursor paging

- For deep traversal use **cursor** (`cursor=*` → `meta.next_cursor`), never high `page` numbers (`page` is capped ~10000 results).
- Keep `per-page` ≤ 200 and request only what you need.

---

## Do / Don't

| Do | Don't |
|----|-------|
| Resolve to IDs, then query | Guess IDs |
| Filter every works query | Scan all of `/works` |
| Set `OPENALEX_MAILTO` | Run anonymous and hit `429` |
| Cite with OpenAlex ID + DOI | Cite title only |
| Use cursor for depth | Page past the cap |
| Reconstruct abstracts | Show the raw inverted index |
| Report real data | Invent papers/counts |

> Verification needed: confirm keys, limits, and field names with <https://docs.openalex.org>.
