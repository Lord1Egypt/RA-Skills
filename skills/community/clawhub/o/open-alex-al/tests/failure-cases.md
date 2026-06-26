# Tests — Failure Cases

Known bad behaviors when using OpenAlex, why they are wrong, and the corrected behavior. Use these as negative tests. **No API key is ever needed.**

---

## F1 — Inventing papers

**Bad:** the agent lists plausible-sounding papers/DOIs that were not returned by the API to satisfy a requested count.

**Why wrong:** fabrication; violates integrity; citations are untraceable.

**Corrected:** report only works in `results`. If fewer than requested, say so and broaden the filter:
```json
{ "tool": "openalex_works", "arguments": { "filter": "primary_topic.id:T11689,is_oa:true", "sort": "cited_by_count:desc", "per_page": 10 } }
```
"Only 4 OA works matched; here they are, fully cited."

---

## F2 — No citation / missing OpenAlex ID

**Bad:** "There's a famous 2018 OA study showing X." — no DOI, no OpenAlex ID.

**Why wrong:** not traceable; fails citation rules.

**Corrected:**
```
Piwowar et al. (2018). The state of OA…. PeerJ.
DOI: 10.7717/peerj.4375. OpenAlex: https://openalex.org/W2741809807
```

---

## F3 — Wrong / malformed filter

**Bad:** `filter: "year=2024 and oa and author=lecun"`.

**Why wrong:** OpenAlex filters are `key:value` comma-separated; `lecun` is a name, not an ID; `year`/`and` are invalid.

**Corrected:** resolve LeCun → `A5023888391`, then:
```json
{ "filter": "publication_year:2024,is_oa:true,authorships.author.id:A5023888391" }
```

---

## F4 — Ignoring the polite pool

**Bad:** runs many anonymous requests, hits `429`, gives up or reports failure.

**Why wrong:** avoidable throttling; bad etiquette.

**Corrected:** set `OPENALEX_MAILTO=you@example.com`, rely on built-in retry/backoff, reduce volume, use cursor paging.

---

## F5 — `per-page` typo

**Bad:** `openalex_request { path:"works", params:{ "per_page": 50 } }` (underscore) — silently ignored.

**Why wrong:** the wire param is **`per-page`** (hyphen); `per_page` does nothing in the generic tool.

**Corrected:**
```json
{ "path": "works", "params": { "per-page": 50, "filter": "is_oa:true" } }
```
(Max 200. The typed `openalex_works` accepts `per_page` and translates it; only the generic tool needs the hyphen.)

---

## F6 — Deep paging with high `page`

**Bad:** requesting `page: 600` to reach result ~15,000.

**Why wrong:** `page` is capped (~10000 results); the request fails or truncates.

**Corrected:** use cursor:
```json
{ "path": "works", "params": { "filter": "publication_year:2024", "per-page": 200, "cursor": "*" } }
```
then pass `meta.next_cursor` each round.

---

## F7 — Raw inverted index as abstract

**Bad:** pasting `{"Open":[0],"access":[1],...}` as the abstract.

**Why wrong:** that's the inverted index, not text.

**Corrected:** reconstruct words by position into a sentence before quoting.

---

## F8 — Retrying a bad ID

**Bad:** repeatedly calling `openalex_get` with the same wrong `W…` ID after an HTML-404.

**Why wrong:** deterministic failure; wastes requests.

**Corrected:** re-resolve via `openalex_search`/`autocomplete`, then use the correct ID.

---

## Summary

| Case | Bad behavior | Fix |
|------|--------------|-----|
| F1 | Invent papers | Report only returned data; broaden filter |
| F2 | No citation/ID | Cite with DOI + OpenAlex ID/URL |
| F3 | Bad filter | `key:value`, comma-AND, resolved IDs |
| F4 | Ignore polite pool | Set `OPENALEX_MAILTO`; back off |
| F5 | `per_page` typo | Use `per-page` (hyphen), max 200 |
| F6 | High `page` | Use cursor |
| F7 | Raw inverted index | Reconstruct abstract text |
| F8 | Retry bad ID | Re-resolve the entity |
