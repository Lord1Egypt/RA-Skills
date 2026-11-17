# open_library — books, ISBNs, authors, editions

## What this source has

Open Library is the Internet Archive's universal bibliographic catalog — ~40M editions of ~25M unique works by ~10M authors. Every book has an OLID: works are `OL12345W`, editions are `OL12345M`, authors are `OL12345A`. The model separates abstract works (the novel "1984") from concrete editions (specific printings with their own ISBNs).

Records carry: title, subtitle, authors, publish date, publisher(s), ISBN-10/13, LCCN, OCLC, page count, subjects, cover images, table of contents (sometimes), description (often pulled from Wikipedia). Many editions link to scanned full text via the Internet Archive's Lending Library.

Use Open Library for: ISBN → book metadata, author bibliographies, "books on subject X". Pair with `crossref` for academic works (DOIs); pair with `wikidata` for cross-source ID resolution (Wikidata stores Open Library IDs as P648/P648).

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 100 req/min recommended; bulk dumps are the preferred path for >1000 records |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search books/works by title/author/keyword | `q` (or `title`, `author`) |
| `isbn` | Fetch edition by ISBN | `isbn` |
| `author` | Author record by OLID | `key` (e.g. `OL26320A`) |
| `work` | Work record by OLID | `key` (e.g. `OL45804W`) |

## Worked examples

```bash
# Search by title + author
python3 scripts/reach.py query open_library search '{
  "title": "snow crash",
  "author": "stephenson",
  "limit": 5
}'

# ISBN lookup
python3 scripts/reach.py query open_library isbn '{"isbn": "9780553380958"}'

# Get the canonical work record
python3 scripts/reach.py query open_library work '{"key": "OL45804W"}'

# Author bibliography
python3 scripts/reach.py query open_library author '{"key": "OL26320A"}'
```

## Response shape

- `search`: `{numFound, start, docs: [{key, title, author_name: [...], author_key: [...], first_publish_year, isbn: [...], cover_i, edition_count, language: [...], subject: [...], publisher: [...]}, ...]}`. `key` is `/works/OL45804W` — strip the `/works/` prefix to get the bare OLID.
- `isbn`: redirects to the canonical edition record. Returns `{title, authors: [{key: "/authors/OL12345A"}], publishers, publish_date, number_of_pages, isbn_10, isbn_13, covers, works: [{key: "/works/OL45804W"}], ...}`.
- `work`: `{title, authors: [{author: {key: ...}, type: ...}], description (string or {value, type}), subjects, subject_places, subject_times, first_publish_date, covers, key}`.
- `author`: `{name, alternate_names, birth_date, death_date, bio (string or {value, type}), photos, key, ...}`.

## Pitfalls

- **OLID suffix encodes the type.** `W` = work (the abstract book), `M` = edition (one printing), `A` = author. Don't pass an `M` to the `work` action.
- **ISBN endpoint redirects.** The connector follows redirects automatically — but the URL you got the ISBN from may differ from the canonical edition.
- **`description` may be a string OR a `{value, type}` object.** Earlier records use the string form; newer use structured. Check `type(description) is dict` before reading `.value`.
- **Author search inside `search` is loose.** `author: stephenson` may surface unrelated Stephensons. Use `author_key` for exact match if you have the OLID.
- **`isbn_10` and `isbn_13` are arrays**, not scalars — an edition can have both.
- **Cover IDs are integers**, fetched separately via `https://covers.openlibrary.org/b/id/<cover_i>-L.jpg`. The API returns the ID, not the URL.
- **Subjects are uncontrolled.** Mix of LCSH, BISAC, and user-tagged values. Don't expect a clean taxonomy.
- **Some ISBNs return 404** even when the book is in the catalog — only the *edition* with that exact ISBN is found. Search by title/author to find related editions.

## Source links

- API docs: https://openlibrary.org/developers/api
- Books API: https://openlibrary.org/dev/docs/api/books
- Search API: https://openlibrary.org/dev/docs/api/search
