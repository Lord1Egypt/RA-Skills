# OpenAlex Skill

> **FEATURED** — Teaches an agent how to use OpenAlex (the open scholarly graph) correctly: discover entities, query works with filters, read results, and cite accurately. **No API key required.** Set `OPENALEX_MAILTO` for the polite pool.

This skill pairs with the **OpenAlex MCP server** (see `../mcp/`), which provides the 6 callable tools. The skill provides the *know-how*. Use imperative voice; do what each step says.

---

## 1. Name

`openalex` — Open scholarly metadata: works, authors, institutions, sources, topics, concepts, publishers, funders.

## 2. Purpose

Answer research questions using authoritative bibliographic data: find papers, authors, citations, open-access status, and bibliometric trends — and cite them precisely. OpenAlex is **free** and **open**.

## 3. When to use OpenAlex

Use OpenAlex when the task involves:

- Scholarly **works** (papers, preprints, datasets, books) and their metadata.
- **Authors** and their output, affiliations, and citation counts.
- **Citations** and impact (cited_by_count, FWCI).
- **Open-access** status and finding free full-text links.
- **Bibliometrics / trends**: counts by year, institution, topic, OA status.
- Institutions, journals/sources, topics, concepts, publishers, funders.

It is free — prefer it for any academic-metadata need.

## 4. When NOT to use OpenAlex

- **Full-text PDFs / reading the paper body** → OpenAlex gives metadata + `open_access.oa_url`; follow that URL to the file. OpenAlex does not serve full text.
- **General/non-academic web information** → use a web search API, not OpenAlex.
- **Paywalled full text** → OpenAlex can tell you if/where an OA copy exists, but cannot bypass paywalls.

## 5. Environment

- **No API key. No required environment variables.**
- **Recommended:** set `OPENALEX_MAILTO=you@example.com` to join the **polite pool** (faster, fewer `429`s). Not a secret.
- Optional: `OPENALEX_API_BASE_URL`, `OPENALEX_TIMEOUT_MS` (30000), `OPENALEX_MAX_RETRIES` (3), `LOG_LEVEL`.

## 6. Operations (the 6 tools + generic)

| Tool | Use it to |
|------|-----------|
| `openalex_search` | Resolve a name/title/keyword to entities (and IDs). |
| `openalex_works` | Query works with `filter`, `sort`, paging — the main tool. |
| `openalex_get` | Fetch one entity by OpenAlex ID / DOI / ORCID / ROR. |
| `openalex_authors` | Search/filter authors. |
| `openalex_group_by` | Counts grouped by a field (analytics). |
| `openalex_request` | Generic passthrough to **any** endpoint (sources, topics, autocomplete, …). |

## 7. Discovery workflow

1. Start from human input (a name, title, keyword).
2. Resolve to an **entity ID** with `openalex_search` or `openalex_request` → `autocomplete/{entity}`.
3. Verify you picked the right entity (check `display_name`, affiliation, works_count).
4. Note the ID prefix → entity type:

| Prefix | Entity | Prefix | Entity |
|--------|--------|--------|--------|
| `W` | Works | `T` | Topics |
| `A` | Authors | `C` | Concepts |
| `I` | Institutions | `P` | Publishers |
| `S` | Sources | `F` | Funders |

Entity types: `works`, `authors`, `sources`, `institutions`, `topics`, `concepts`, `publishers`, `funders`, `keywords`.

## 8. Query workflow

Build a `filter` (comma-separated, ANDed) and pick a `sort`:

| Need | Filter |
|------|--------|
| Year | `publication_year:2024` |
| Date range | `from_publication_date:…,to_publication_date:…` |
| Open access | `is_oa:true` |
| By author | `authorships.author.id:A…` |
| By institution | `authorships.institutions.id:I…` |
| By topic | `primary_topic.id:T…` |
| Highly cited | `cited_by_count:>100` |
| Type | `type:article` |

- Sort by impact: `cited_by_count:desc`. Sort by recency: `publication_date:desc`.
- `per-page` ≤ **200**.
- For deep traversal, use **cursor** (`cursor=*` then `meta.next_cursor`), not high `page` numbers.

## 9. Reading results

- `meta.count` = total matches (not the number returned).
- `results` = the current page only.
- `group_by` = `[{key, key_display_name, count}]` for aggregations.
- **Abstract:** works carry `abstract_inverted_index` (a `{word: [positions]}` map), not plain text. Reconstruct by placing each word at its positions and joining in order.
- **Full text:** follow `open_access.oa_url` for the free PDF/HTML.

## 10. Citation rules

Cite every claim with: **title, authors, year, DOI, and the OpenAlex ID + URL** `https://openalex.org/<ID>`.

```
<Authors> (<year>). <Title>. <Source>. DOI: <doi>. OpenAlex: https://openalex.org/<WID>
```

The OpenAlex URL is mandatory for traceability, in addition to the DOI.

## 11. Freshness

OpenAlex data updates **frequently** (new works, citation counts, affiliations). Counts you report are point-in-time. When precision matters, note the access date and that figures may change.

## 12. Integrity

- Report **only** what the API returns. **Never invent** papers, authors, DOIs, or citation counts.
- If results are empty, say so and broaden — do not fabricate to satisfy a requested count.
- Keep totals (`meta.count`) distinct from listed `results`.

## 13. Error handling

| Error | Cause | Reaction |
|-------|-------|----------|
| HTML 404 | Bad/typo ID | Fix the ID prefix/value; re-resolve via search/autocomplete. |
| `429` | Not in polite pool / too fast | Set `OPENALEX_MAILTO`; back off; reduce volume. |
| Empty results | Filter too narrow | Broaden filter; check key spelling; try `search`. |
| `400` | Bad filter syntax | Comma-separate; use `key:value`; verify keys. |
| Timeout | Query too broad | Add a filter; lower `per-page`. |

## 14. Cost / etiquette

- **Free.** Be polite: set `OPENALEX_MAILTO`.
- **Cache** resolved IDs and stable records.
- **Avoid huge unfiltered scans.** Always filter first.
- **Use cursor**, not high page numbers (`page` is capped ~10000 results).

## 15. Security

- No secrets to manage. `OPENALEX_MAILTO` is not sensitive but keep configs clean.
- Read-only API; outbound HTTPS only. Keep logs on stderr; protocol on stdout.

## 16. Agent checklist

- [ ] Resolved names to IDs (and verified the right entity)?
- [ ] Built a `filter` instead of scanning everything?
- [ ] Chose an appropriate `sort`?
- [ ] Used cursor for deep paging?
- [ ] Read `meta.count` vs `results` correctly?
- [ ] Reconstructed abstracts from the inverted index if needed?
- [ ] Cited title + authors + year + DOI + OpenAlex ID/URL?
- [ ] Set `OPENALEX_MAILTO` to avoid `429`?
- [ ] Reported only real, returned data?

## 17. Example workflows

- **Literature review:** resolve topic → `openalex_works` (topic + year + `is_oa`, sort by citations) → `openalex_get` top work → author/institution profiles → cited summary. See `recipes/literature-search.md`.
- **Author profile:** resolve author → `openalex_get` author → `openalex_works` filtered by `authorships.author.id` → top works + metrics. See `recipes/author-profile.md`.
- **Trend by year:** `openalex_group_by` on `publication_year` with a topic/OA filter. See `recipes/citation-trends.md`.

## 18. Common mistakes

- Using `per_page` on the wire instead of **`per-page`** (hyphen) in `openalex_request`.
- Deep-paging with high `page` numbers (capped ~**10000** results) instead of **cursor**.
- Treating `abstract_inverted_index` as plain text.
- Reporting `meta.count` as the number of items returned.
- Forgetting the OpenAlex ID/URL in citations.
- Skipping `OPENALEX_MAILTO` and hitting `429`.

## 19. Maintenance

- Re-resolve IDs periodically; entities can merge/change.
- Re-check filter keys and limits against <https://docs.openalex.org> when behavior changes.
- Update cached records given frequent data refreshes.

> Verification needed: confirm filter keys, limits, and field names with <https://docs.openalex.org>.
