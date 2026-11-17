# Search — Substring, Fuzzy, Full-Text, and Vectors

Four different problems that people call "search". Pick by what the user types.

| The user types | Mechanism | Index |
|---|---|---|
| A known prefix (`"acme co"` for autocomplete) | `LIKE 'acme co%'` | B-tree; `text_pattern_ops` if the collation is not C |
| A substring anywhere (`"%cme%"`) | `LIKE`/`ILIKE` with pg_trgm | GIN trigram |
| A misspelling (`"acme corp"` vs `"akme corp"`) | `similarity()`, `word_similarity()`, `levenshtein()` | GIN/GiST trigram |
| Words, phrases, stemming, ranking | `tsvector @@ tsquery` | GIN on a stored tsvector |
| Meaning without shared words | Embeddings, cosine distance | pgvector HNSW |
| Anything else | Start with trigram; it is the cheapest thing that handles real typing | — |

## Trigram (pg_trgm)

```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX ON customers USING gin (name gin_trgm_ops);

SELECT name, similarity(name, 'akme corp') AS s
FROM customers WHERE name % 'akme corp'      -- % uses pg_trgm.similarity_threshold (0.3)
ORDER BY s DESC LIMIT 10;
```

- Trigram indexes serve `LIKE '%x%'` and `ILIKE` — the only structure that does. A B-tree cannot, because a leading wildcard has no prefix to seek.
- Strings shorter than 3 characters produce no trigrams; a two-letter search falls back to a scan. Handle short input with a prefix query instead.
- `%` (similarity above threshold) is settable per session with `pg_trgm.similarity_threshold`; `<->` is the distance operator for `ORDER BY` nearest-match, and `word_similarity()` scores a short needle against a long haystack (product name inside a description).
- GIN is the default; GiST is smaller and supports `ORDER BY <->` nearest-neighbour scans directly, at slower lookup.
- `levenshtein()` (from `fuzzystrmatch`) is exact edit distance but has no index support — use it to re-rank a trigram candidate set, never to filter a whole table.

## Full-Text Search

```sql
ALTER TABLE articles ADD COLUMN search tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('english', coalesce(body,'')),  'B')
  ) STORED;
CREATE INDEX ON articles USING gin (search);

SELECT id, ts_rank_cd(search, q) AS rank
FROM articles, websearch_to_tsquery('english', $1) q
WHERE search @@ q ORDER BY rank DESC LIMIT 20;
```

- **Store the tsvector, do not compute it per query.** `WHERE to_tsvector(body) @@ ...` recomputes for every row and cannot use an index; a stored generated column (PostgreSQL >=12) is maintained automatically and indexable.
- Parse user input with `websearch_to_tsquery` (PostgreSQL >=11): it accepts quotes, `-` negation and `or`, and never throws on junk. `to_tsquery` raises a syntax error on ordinary user text; `plainto_tsquery` ANDs everything and ignores operators.
- Configuration matters: `'english'` stems and drops stop words ("the" is unsearchable); `'simple'` matches exact tokens and keeps everything. Store and query with the **same** configuration or the stems will not match — and set `default_text_search_config` so nobody relies on the session default.
- `setweight` A/B/C/D plus `ts_rank_cd` lets a title hit outrank a body hit. Ranking without weights ranks by term density, which favours short documents.
- Prefix matching inside FTS: `to_tsquery('acm:*')`. Phrase search: `<->` (`'quick' <-> 'brown'`) or `phraseto_tsquery`.
- FTS is word-based. "part of a word" is a trigram problem, and combining both — trigram for the fragment, FTS for the phrase — is a normal design, not a failure.
- Highlighting: `ts_headline` re-parses the original document per row, so run it only on the final page of results, never before the LIMIT.
- Multi-language content: one tsvector column per language, or a language column plus `to_tsvector(lang_config, body)` with the config stored per row (the generated-column form then needs a trigger, because generated columns must be immutable).

## Vector Search

Embeddings answer "semantically close", which no lexical index can. Setup, index choice, and the `lists`/`probes` formulas are in the pgvector entry of the extensions guide; the search-side decisions are:

- **Hybrid beats either alone.** Run FTS and vector search separately, take the top ~50 of each, and fuse with Reciprocal Rank Fusion (`score = Σ 1/(60 + rank_i)`). Lexical catches exact identifiers and rare words that embeddings blur; vectors catch paraphrase.
- Normalize what you embed the same way at write and query time (same model, same preprocessing, same truncation). A retrieval quality drop after a model change is not a tuning problem.
- Chunk documents before embedding; a single vector for a 40-page PDF matches everything weakly.
- Store the source text next to the vector. The result of a vector search is useless without the passage.

## Ranking and Pagination

- `ORDER BY rank DESC LIMIT 20` with a GIN index means Postgres computes the rank for every match. On broad queries that is the actual cost — bound the candidate set first (a subquery with a filter and a limit, then rank) when the corpus is large.
- Deep pagination over ranked results has no keyset equivalent, because rank is not a stable indexed key. Cap the reachable depth (search UIs almost always can) rather than pretending page 500 is meaningful.
- Facet counts over a large filtered set are a separate query and usually the slowest part of the page; consider approximate counts or precomputed rollups.

## When to Leave Postgres

Postgres full-text search comfortably serves corpora in the millions of documents with one language, straightforward ranking, and modest query rates. Move to a dedicated engine when you need per-field analyzers per language, learning-to-rank, synonym management as an operational feature, or search traffic that would dominate your transactional server. Below that line, an external engine adds a synchronization problem — and stale search results — for no measured gain.
