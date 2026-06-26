# Recipe — Literature Search

## Goal

Produce a ranked, cited shortlist of works on a topic, optionally restricted to open access and a time window.

## When

The user wants "top papers / recent research / key works on X", a reading list, or a mini literature review.

## Inputs

- Topic / keywords (free text).
- Optional: year or date range, OA-only, minimum citations, language.

## Steps

1. **Resolve the topic** to an ID (more precise than keyword search):
   ```json
   { "tool": "openalex_search", "arguments": { "entity": "topics", "query": "graph neural networks", "per_page": 1 } }
   ```
   → topic `id` (`T…`).
2. **Query works** with filters and sort by impact:
   ```json
   {
     "tool": "openalex_works",
     "arguments": {
       "filter": "primary_topic.id:T11689,from_publication_date:2022-01-01,is_oa:true",
       "sort": "cited_by_count:desc",
       "per_page": 10
     }
   }
   ```
   (If no clean topic match, use `openalex_works` with `search` instead of `primary_topic.id`.)
3. **Read** `meta.count` (total) and `results` (the page).
4. **Optionally deepen** a top work: `openalex_get { entity:"works", id:"W…" }` for full authorship and references.
5. **Cite** each item with title, authors, year, source, DOI, OpenAlex ID/URL, and `oa_url` if OA.

## Output

A numbered list ranked by citations, each fully cited, plus the total match count.

## Example

> Top OA GNN papers since 2022 (of 6,470 matches):
> 1. *Scalable GNNs* — Researcher et al. (2022). ICML. DOI: 10.xxxx/… · OpenAlex: https://openalex.org/W4402345678 · Cited 1,204 · OA PDF: https://…
> 2. *Heterogeneous GNNs* — Author et al. (2023). NeurIPS. DOI: 10.xxxx/… · OpenAlex: https://openalex.org/W4403456789 · Cited 832

## Edge cases

- **Topic not resolvable** → fall back to `search` over works.
- **Empty results** → drop `is_oa` or widen the date range; report that it was empty.
- **Too many results to page** → use cursor (`cursor=*` → `meta.next_cursor`).

## Production notes

- Set `OPENALEX_MAILTO` to avoid `429` during multi-step runs.
- Cache the resolved topic ID and the result page.
- Never invent papers to reach a requested count — report what exists.

> Verification needed: confirm filter keys with <https://docs.openalex.org>.
