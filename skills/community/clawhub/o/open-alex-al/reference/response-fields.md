# Reference — Response Fields

How to read OpenAlex responses: the envelope, work and author fields, the abstract inverted index, and how to cite. **No API key.**

---

## Response envelope

```json
{
  "meta": { "count": 12345, "page": 1, "per_page": 25, "next_cursor": "Iy..." },
  "results": [ { "id": "https://openalex.org/W…", "...": "..." } ],
  "group_by": [ { "key": "2024", "key_display_name": "2024", "count": 987 } ]
}
```

| Field | Meaning |
|-------|---------|
| `meta.count` | **Total** matches (not the number returned). |
| `meta.page` / `meta.per_page` | Current page and page size. |
| `meta.next_cursor` | Cursor for the next page (null when done). |
| `results` | The current page of records. |
| `group_by` | Aggregated counts (only for group-by calls; `results` empty then). |

A single `openalex_get` returns the record object directly (no `meta`/`results` wrapper).

---

## Work fields (most useful)

| Field | Description |
|-------|-------------|
| `id` | OpenAlex ID URL (`https://openalex.org/W…`). |
| `doi` | DOI URL. |
| `display_name` / `title` | Title. |
| `publication_year` | Year. |
| `type` | e.g. `article`, `preprint`, `dataset`. |
| `open_access` | `{ is_oa, oa_status, oa_url }` — `oa_url` is the free full text. |
| `authorships` | `[{ author{ id, display_name, orcid }, institutions[…] }]`. |
| `cited_by_count` | Citation count. |
| `fwci` | Field-Weighted Citation Impact. |
| `primary_location` | `{ source{ display_name, id } }` — where published. |
| `topics` / `concepts` | Subject classification. |
| `referenced_works` | OpenAlex IDs this work cites. |
| `abstract_inverted_index` | Abstract as a word→positions map (see below). |

## Author fields (most useful)

| Field | Description |
|-------|-------------|
| `id` | OpenAlex ID (`A…`). |
| `display_name` | Name. |
| `orcid` | ORCID URL. |
| `works_count` | Number of works. |
| `cited_by_count` | Total citations. |
| `last_known_institutions` | Current affiliation(s) (`I…`). |
| `affiliations` | Institution history. |

---

## Abstract inverted index → text

Works expose `abstract_inverted_index`, **not** plain text. It maps each word to the positions where it appears:

```json
"abstract_inverted_index": {
  "Open": [0],
  "access": [1],
  "improves": [2],
  "citation": [3, 6],
  "impact": [4]
}
```

To reconstruct:

1. Build an array sized to the max position + 1.
2. Place each word at every listed position.
3. Join with spaces in position order.

Result: `"Open access improves citation impact … citation"`. Reconstruct before quoting or summarizing an abstract — never present the raw index as text.

---

## How to cite

Combine work fields into a full citation that includes the **OpenAlex ID/URL**:

```
<authorships[].author.display_name> (<publication_year>). <display_name>.
<primary_location.source.display_name>. DOI: <doi>. OpenAlex: https://openalex.org/<WID>
```

If `open_access.is_oa` is true, also offer `open_access.oa_url` as the free full-text link.

> Verification needed: confirm field names with <https://docs.openalex.org>.
