# Pagination — Connections, Cursors, And The Page Nobody Can Reach

Pick the model from the access pattern, not from fashion. The cap on page size is `max_page_size` (default 100, SKILL.md rule 3) in every model below.

Contents: Choosing A Model · The Connection Shape · Cursors · Keyset SQL · totalCount · Sorting And Filtering · Bidirectional · Nested Connections · Client Side · Traps

## Choosing A Model

| Model | Shape | Use when | Breaks on |
|---|---|---|---|
| Relay connection | `first`/`after`, `edges`, `pageInfo` | Infinite scroll, feeds, anything a client walks forward | "Jump to page 50", total-count UIs |
| Offset | `limit`/`offset` or `page`/`perPage` | Admin tables with numbered pages, small stable datasets | Concurrent inserts (skipped and duplicated rows), deep offsets |
| Simple list, bounded | plain `[T!]!` | Provably small sets: a user's roles, an order's line items | The day the set stops being small |

- Offset pagination is not wrong, it is *unstable*: an insert above the current page shifts every subsequent row down, so the reader sees one item twice and misses another. Acceptable for an admin screen, disqualifying for an append-heavy feed.
- Deep offsets are also slow: `OFFSET 100000` makes the database walk and discard 100 000 rows. Keyset does not.
- Recorded in `pagination_style`; a stated preference switches every list field this skill emits.

## The Connection Shape

```graphql
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int          # nullable on purpose — see below
}
type PostEdge { node: Post!, cursor: String! }
type PageInfo { hasNextPage: Boolean!, hasPreviousPage: Boolean!, startCursor: String, endCursor: String }
```

- `edges` exists so that the *relationship* can carry fields the node cannot: `role` on a membership edge, `addedAt` on a playlist entry, `score` on a search hit. If no relationship data exists today, edges still cost one indirection and buy you the ability to add it without a breaking change.
- A `nodes: [Post!]!` shortcut alongside `edges` is a common ergonomic addition and a permanent duplication — pick one per schema and stay consistent (recorded under Conventions).
- `pageInfo` is the termination signal. Clients loop while `hasNextPage`, never on "I got fewer items than I asked for" — a filtered page can legitimately return fewer and still have a next page.
- `hasPreviousPage` is only meaningful when paginating backwards; with `first`/`after` most servers return `false` unconditionally, which is spec-legal and surprises people.
- Arguments: `first`/`after` for forward, `last`/`before` for backward. Passing `first` and `last` together is undefined — reject it with `BAD_USER_INPUT` rather than picking one.

## Cursors

- A cursor is opaque to the client. Never document its format, never let clients construct one, never parse one client-side.
- Encode the sort key, not the offset: base64 of `{sortValue, tiebreakerId}`. An offset-in-a-cursor gives you the instability of offset pagination with the ceremony of connections.
- The tiebreaker is not optional. Sorting by `createdAt` alone with two rows sharing a timestamp makes the "after this cursor" comparison ambiguous and rows are skipped or repeated. Always append a unique column.
- Cursors are bound to the sort and filter arguments they were issued under. Changing either mid-walk invalidates them; the server should detect the mismatch and return `BAD_USER_INPUT` rather than returning nonsense.
- Sign or version the cursor if it is worth protecting: an unsigned cursor is user-controlled input reaching your `WHERE` clause. Validate it as strictly as any other argument (`security.md`).
- Cursors outlive deployments. Encode a version byte so a future sort change can reject old cursors intelligibly instead of throwing on decode.

## Keyset SQL

Forward page, sorting by `created_at DESC` with `id` as tiebreaker:

```sql
SELECT * FROM posts
WHERE (created_at, id) < ($cursor_created_at, $cursor_id)
ORDER BY created_at DESC, id DESC
LIMIT $first + 1;
```

- Fetch `first + 1` rows: the existence of the extra row *is* `hasNextPage`. Trim it before building edges. A separate `COUNT` to answer the same question is one query too many, every page.
- The row-value comparison `(a, b) < (x, y)` is what makes the tiebreaker work in one indexable predicate; expanding it into `a < x OR (a = x AND b < y)` is equivalent but frequently loses the index.
- The index must match the sort exactly, including direction and the tiebreaker column, or every page is a sort of the whole table.
- Backward pages reverse the comparison and the `ORDER BY`, then reverse the resulting array before returning it — forgetting the second reversal returns the right rows in the wrong order, which reviewers never catch.

## totalCount

- `totalCount: Int!` on every connection forces a `COUNT(*)` on every page, routinely more expensive than the page itself, and unusable on large filtered sets (SKILL.md Traps).
- Make it nullable and let the resolver decide: exact below a threshold, estimated above it, `null` when the estimate is unavailable. Say which in the field description.
- Estimates: the planner's row estimate for the query is free and roughly right; expose it as a separate field (`estimatedTotalCount`) rather than lying through `totalCount`, so a UI can choose whether "about 12,000" is acceptable.
- The honest UI answer is usually neither: `hasNextPage` powers "load more" without any count at all.

## Sorting And Filtering

- Sort belongs in the arguments as an enum (`orderBy: PostOrder = CREATED_AT_DESC`), never as a free-form string — a string is an injection surface and an unindexable surprise.
- Every sortable field needs an index that includes the tiebreaker. Publishing a sort option you have no index for is how one dropdown takes down a database.
- Filters go in one input object with documented combination semantics. Arbitrary boolean trees (`AND`/`OR`/`NOT` nested inputs) are powerful and turn your API into a query language you now have to cost-limit and index for; adopt deliberately.
- Filter arguments participate in cost: `posts(first: 100, filter: {…})` costs the same estimate whether the filter matches 3 rows or 3 million (SKILL.md Cost Model).

## Bidirectional

- `last`/`before` is real backward pagination, not "reverse the list you have". Implement it as the mirrored keyset query above.
- `last` without `before` means "the last N overall" and requires sorting the whole set descending — cap it as strictly as `first`.
- Most UIs never need backward pagination. Shipping only `first`/`after` and adding the rest when a client asks is a defensible default; the connection type is already shaped for it.

## Nested Connections

- A connection inside every node of another connection multiplies cost by page sizes and defeats a single cursor per document: each nested list has its own cursor per parent.
- The workable pattern is a second round trip: collect the parent ids from page one, then query the children keyed by those ids in one operation with its own pagination.
- Cap nested page sizes lower than top-level ones. A default of 100 posts each showing 100 comments is 10 000 rows for a screen showing three.
- Never paginate a nested connection with a cursor obtained under a different parent — cursors are scoped to the exact field and arguments that issued them.

## Client Side

- Apollo: `relayStylePagination()` (or a hand-written `merge`/`read` field policy) teaches the cache that two pages of the same field are one list. Without a field policy the second page *replaces* the first in the cache and the UI flickers back to 20 items.
- The field policy's `keyArgs` must list the arguments that make a different list (filters, sort) and exclude the ones that make a different page (`after`, `first`). Getting this backwards is the classic "filters bleed between tabs" bug (`client.md`).
- Relay handles this natively through `@connection` and the pagination container, at the price of the full Relay contract (global ids, `node` field, compiler).
- Optimistically inserting into a paginated list is a lie about ordering: with keyset pagination the new item may belong on a page the client has not loaded. Insert at the boundary you can defend (the top of a `CREATED_AT_DESC` feed) and refetch otherwise.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Client loops until it gets fewer items than requested | A filtered page returns fewer and still has more | Loop on `pageInfo.hasNextPage` |
| Offset pagination over an append-heavy feed | Inserts shift rows; readers see duplicates and gaps | Keyset cursors |
| Cursor encoding an offset | Instability of offset with the ceremony of connections | Encode the sort key plus tiebreaker |
| Sorting by a non-unique column with no tiebreaker | Ambiguous boundary; rows skipped or repeated | Append a unique column to sort and cursor |
| Uncapped `first` | Cheapest DoS in the schema | Reject above `max_page_size` (rule 3) |
| Changing sort while paginating | All outstanding cursors are meaningless | Detect the mismatch, return `BAD_USER_INPUT`, restart |
| `first` and `last` in the same call | Undefined behaviour, implementation-specific | Reject explicitly |
