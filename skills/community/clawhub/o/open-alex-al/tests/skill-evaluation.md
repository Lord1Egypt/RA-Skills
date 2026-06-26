# Tests — Skill Evaluation

Use this checklist to verify an agent applies the OpenAlex skill correctly. **No API key** should ever be requested. Setting `OPENALEX_MAILTO` (polite pool) is expected in production.

---

## Evaluation checklist

| # | Capability | Pass criteria |
|---|-----------|---------------|
| 1 | Source selection | Uses OpenAlex for scholarly metadata; uses web/PDF sources for full text or non-academic info. |
| 2 | Entity resolution | Resolves names to IDs via `openalex_search` / `autocomplete` and verifies the match before querying. |
| 3 | Filter construction | Builds comma-separated `key:value` filters; never scans `/works` unfiltered. |
| 4 | Sorting | Chooses `cited_by_count:desc` for impact, `publication_date:desc` for recency. |
| 5 | Paging | Uses `per-page` ≤ 200; uses **cursor** for deep paging, not high `page`. |
| 6 | Result reading | Distinguishes `meta.count` (total) from `results` (page); uses `group_by` for aggregates. |
| 7 | Abstracts | Reconstructs `abstract_inverted_index` into text before quoting. |
| 8 | Citation | Cites title + authors + year + DOI + **OpenAlex ID/URL**; offers `oa_url` when OA. |
| 9 | Integrity | Reports only returned data; states when results are empty; never invents. |
| 10 | Polite pool | Sets/relies on `OPENALEX_MAILTO`; backs off on `429`. |
| 11 | Error handling | Re-resolves on HTML 404; broadens on empty; fixes filter on `400`. |
| 12 | Freshness | Notes that counts are point-in-time. |

---

## Scenario tests

### S1 — Topic literature search
Prompt: "Top open-access papers on diffusion models since 2022."
Expect: resolve topic → `openalex_works` with `primary_topic.id`, `from_publication_date`, `is_oa:true`, `sort=cited_by_count:desc`; cited list with OpenAlex IDs; total count reported.

### S2 — Author profile
Prompt: "Profile Geoffrey Hinton's research."
Expect: resolve `A…` (disambiguate) → `openalex_get` author → top works by `authorships.author.id`; metrics + cited top works.

### S3 — Trend
Prompt: "How has research on transformers grown by year?"
Expect: `openalex_group_by` on `publication_year` with a topic filter; year-count table; filter stated.

### S4 — Generic endpoint
Prompt: "Which journal is 'Nature' in OpenAlex?"
Expect: `openalex_request` on `sources` (or `autocomplete/sources`); returns `S…` ID.

### S5 — Bad ID recovery
Prompt: "Get work W0000000000."
Expect: HTML-404 handled; agent re-resolves by title or reports not found — no fabricated data.

---

## Scoring

- **Pass:** meets the pass criteria for the capability.
- **Partial:** correct tool but missing citation/ID, or wrong paging.
- **Fail:** invents data, requests a key, scans unfiltered, or ignores `429`.

Target: all checklist items Pass; zero fabrication.
