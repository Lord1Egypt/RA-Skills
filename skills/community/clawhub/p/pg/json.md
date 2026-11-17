# JSONB — Modeling, Querying, Indexing

`json` stores the text you sent, preserving whitespace, key order, and duplicate keys. `jsonb` parses it into a binary form: slightly slower to write, far faster to read, deduplicates keys, loses order, and is the only one with indexing operators. Use `jsonb` unless you must reproduce a payload byte for byte.

## The Modeling Decision

Put it in a column when the key is filtered, joined, sorted, or constrained. Put it in `jsonb` when the shape is genuinely open (per-tenant custom fields, third-party payloads, event bodies you archive).

The technical reason is not taste: **jsonb keys have no per-key statistics**. The planner estimates a fixed selectivity for containment, so a `WHERE data @> '{"status":"active"}'` matching 90% of rows and one matching 0.1% get the same estimate, and half your plans are wrong (SKILL.md Where Experts Disagree). Extended statistics on an expression (`CREATE STATISTICS ... ON (data->>'status') FROM t`) recover part of it for keys you query often.

Hybrid is the mature shape: promote the three keys you query into real columns, keep the rest in `jsonb`, and backfill with a generated column when a key graduates:

```sql
ALTER TABLE events ADD COLUMN status text
  GENERATED ALWAYS AS (payload->>'status') STORED;
CREATE INDEX ON events (status);
```

## Operators You Need

| Operator | Returns | Use |
|---|---|---|
| `->` | jsonb | Navigate: `data->'user'->'name'` |
| `->>` | text | Extract a scalar for comparison: `data->>'email' = ?` |
| `#>` / `#>>` | jsonb / text | Path form: `data#>>'{user,name}'` |
| `@>` | bool | Containment — the indexable workhorse: `data @> '{"status":"active"}'` |
| `?` `?|` `?&` | bool | Key existence (top-level keys, or array elements) |
| `@@` / `@?` | bool | jsonpath predicate / existence (PostgreSQL >=12) |
| `\|\|` | jsonb | Shallow merge; right side wins |
| `-` / `#-` | jsonb | Delete a key or a path |

`jsonb_set(target, path, value, create_if_missing)` updates one path. Careful: any `jsonb` operation with a NULL argument returns NULL — `jsonb_set(data, '{a}', to_jsonb(x))` with `x` NULL wipes the whole column for that row. Guard with `coalesce`.

Numbers survive round-trips as `numeric`, so no float surprises. `null` inside jsonb is a JSON null, distinct from SQL NULL: `data->>'k' IS NULL` is true both when the key is missing and when its value is JSON null — use `data ? 'k'` to tell them apart.

## Querying Shapes

```sql
-- containment (index-friendly)
SELECT * FROM events WHERE payload @> '{"type":"signup","source":{"utm":"x"}}';

-- expand an array of objects into rows
SELECT e.id, item->>'sku', (item->>'qty')::int
FROM orders e, jsonb_array_elements(e.payload->'items') AS item;

-- jsonpath: filter inside the document
SELECT * FROM events WHERE payload @? '$.items[*] ? (@.qty > 10)';

-- build rows from a document with a declared shape
SELECT * FROM jsonb_to_recordset('[{"a":1,"b":"x"}]') AS t(a int, b text);
```

`jsonb_array_elements` on a large array multiplies rows before any filter — put the selective predicate on the outer table first, and consider `LATERAL` with a `LIMIT` when you only need a few elements.

`jsonb_path_query` and friends implement SQL/JSON path; `@?` (does anything match) and `@@` (is the predicate true) are the indexable ones on a default GIN index.

## Indexing

```sql
-- default opclass: supports @>, ?, ?|, ?&, @?, @@  — larger index
CREATE INDEX ON events USING gin (payload);

-- jsonb_path_ops: supports @> (and jsonpath) only — smaller and faster
CREATE INDEX ON events USING gin (payload jsonb_path_ops);

-- a single hot key, B-tree on an expression: supports =, <, >, ORDER BY
CREATE INDEX ON events ((payload->>'status'));

-- a single hot key inside a big document, indexed only where it matters
CREATE INDEX ON events ((payload->>'status')) WHERE payload ? 'status';
```

Choose by predicate: containment queries → `jsonb_path_ops` GIN (typically around half the size of the default opclass and faster for `@>`). Key-existence queries (`?`) → default GIN, because `jsonb_path_ops` does not support them. Range or ordering on one key → B-tree on the expression; GIN can never serve `ORDER BY`.

An expression index must match the query text exactly, casts included: an index on `(payload->>'qty')` does not serve `WHERE (payload->>'qty')::int > 5`. Index the cast expression instead.

## Size, TOAST, and Update Cost

- A `jsonb` value above ~2 kB is compressed and moved out of line into TOAST. Reading one key from a 200 kB document detoasts the whole thing — this is why "just query the JSON" degrades badly at document size, not at row count.
- **Any update to a jsonb column rewrites the entire value and its TOAST chunks.** Appending one element to an array of 10,000 rewrites all of them, plus every index on the column. Documents that are updated frequently want to be rows.
- `column_name SET STORAGE EXTERNAL` disables compression for that column: bigger on disk, much faster substring/partial access. Worth it for documents read piecemeal.
- LZ4 TOAST compression (`default_toast_compression = lz4`, PostgreSQL >=14) is markedly faster than pglz at slightly worse ratios; for jsonb-heavy tables it is usually the better trade.

## Validation

`jsonb` guarantees valid JSON, nothing more. Constrain what matters:

```sql
ALTER TABLE events ADD CONSTRAINT payload_has_type
  CHECK (payload ? 'type' AND jsonb_typeof(payload->'type') = 'string');
```

PostgreSQL >=17 adds `IS JSON` predicates (`IS JSON OBJECT`, `IS JSON SCALAR`) and the SQL/JSON constructors (`JSON_TABLE`, `JSON_QUERY`, `JSON_VALUE`), which make document-to-relational mapping declarative instead of a pile of `->>` casts. Below that, `jsonb_to_recordset` is the equivalent.
