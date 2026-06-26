# Aggregation Pipeline

## Pipeline Philosophy

- Think of data as flowing through transformation stages
- Each stage receives documents from previous stage
- Order matters enormously—for both correctness and performance
- Build incrementally—add one stage, verify, add next

## Stage Order for Performance

- `$match` FIRST—reduce document count before anything else
- `$project` early—drop unneeded fields to reduce memory
- Only `$match` at START can use indexes—after any transformation, no index
- `$sort` with `$limit` together—can use index efficiently

## Memory Limits

- 100MB memory limit per stage—hits faster than you expect
- `allowDiskUse: true` for large aggregations—slower but won't fail
- `$group` on high cardinality field = memory explosion
- `$unwind` on large arrays multiplies documents—memory spikes

## $unwind Traps

- Creates one document per array element—100 element array = 100 documents
- Empty/missing array = document DROPPED—use `preserveNullAndEmptyArrays: true`
- Order in array is lost—use `includeArrayIndex` if position matters
- Think before unwinding—maybe `$filter` or `$reduce` is enough

## $group Patterns

- `_id: null` aggregates entire collection—single output document
- `$first`/`$last` depend on input order—need `$sort` before for meaningful results
- `$push` creates array in output—watch for 16MB limit on result
- `$sum` of non-numeric field = 0—silent wrong result, no error

## $lookup (Join)

- No index on foreign collection until 5.0—full collection scan each time
- Results in array even for 1:1—often need `$unwind` after
- Pipeline syntax (5.0+) filters foreign BEFORE joining—much faster
- Recursive lookup via `$graphLookup`—for tree/graph structures

## $facet

- Multiple parallel pipelines on same input documents
- All facets process ALL input documents—can be expensive
- Results in single document—watch 16MB limit
- Great for dashboards with multiple aggregations

## $merge and $out

- `$out` replaces target collection—atomic but destructive
- `$merge` can upsert/update—more flexible but complex
- Use for materialized views—pre-aggregate expensive reports
- Schedule with cron, read from materialized collection

## Debugging Aggregations

- Add `$limit: 1` at end while developing—see one result quickly
- Use `$project` to see intermediate state—remove it after
- Comment out stages to isolate problems
- `explain()` works on aggregations too—check index usage
