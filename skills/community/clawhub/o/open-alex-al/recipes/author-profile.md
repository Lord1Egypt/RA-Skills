# Recipe — Author Profile

## Goal

Build a profile for a researcher: identity, affiliation, output volume, citation impact, and top works.

## When

The user asks "who is X / what has X published / how cited is X / what's X's most influential work".

## Inputs

- Author name (free text), or an ORCID, or an OpenAlex `A…` ID.

## Steps

1. **Resolve the author** (disambiguate — names collide):
   ```json
   { "tool": "openalex_search", "arguments": { "entity": "authors", "query": "Yann LeCun", "per_page": 5 } }
   ```
   Pick the right `A…` by checking affiliation and `works_count`. (If you have an ORCID, skip to step 2 with `id` = the ORCID URL.)
2. **Fetch the full author record:**
   ```json
   { "tool": "openalex_get", "arguments": { "entity": "authors", "id": "A5023888391" } }
   ```
   → `display_name`, `orcid`, `works_count`, `cited_by_count`, `last_known_institutions`.
3. **Get top works** by that author:
   ```json
   {
     "tool": "openalex_works",
     "arguments": {
       "filter": "authorships.author.id:A5023888391",
       "sort": "cited_by_count:desc",
       "per_page": 5
     }
   }
   ```
4. **Optional trend:** works per year:
   ```json
   { "tool": "openalex_group_by", "arguments": { "entity": "works", "group_by": "publication_year", "filter": "authorships.author.id:A5023888391" } }
   ```
5. **Cite** the top works fully (title, year, DOI, OpenAlex ID/URL).

## Output

A short profile: name, ORCID, current affiliation, works_count, total citations, top 3–5 cited works (each cited), and optionally an output-by-year sparkline.

## Example

> **Yann LeCun** (ORCID 0000-0002-0387-7440) — OpenAlex A5023888391.
> Works: 412 · Citations: 312,045 · Affiliation: New York University (OpenAlex I…).
> Top work: *Gradient-based learning applied to document recognition* (1998). Proc. IEEE.
> DOI: 10.1109/5.726791 · OpenAlex: https://openalex.org/W2151103935 · Cited 60,000+.

## Edge cases

- **Wrong author picked** → verify via affiliation/works before reporting; re-resolve if needed.
- **Disambiguation merges/splits** → IDs can change; re-resolve periodically.
- **Empty works list** → confirm the `A…` ID is correct (HTML 404 means a bad ID).

## Production notes

- Set `OPENALEX_MAILTO`; cache the resolved `A…` ID.
- Citation totals are point-in-time — note the access date.
- Report only real figures from the API.

> Verification needed: confirm author fields with <https://docs.openalex.org>.
