# Performance Traps

## N+1 Traps

- No DataLoader = each resolver queries independently—100 items = 100 queries
- DataLoader per-request only—shared loader caches across requests = stale data
- Batch function must return same order as input—mismatch = wrong data
- Nested N+1—posts → comments → users chains multiply

## DataLoader Traps

- Missing item must return null in position—not filtered out
- DataLoader dedupes within request—same ID twice = one DB query
- Doesn't work across async boundaries without context
- Cache doesn't invalidate—mutation needs manual clear

## Resolver Traps

- Resolver runs even if field not selected—use `info` to check
- Parent object may be partial—don't assume all fields populated
- Async resolver without await still runs—but returns promise not value
- Throwing in resolver nulls field—may cascade up if non-null

## Caching Traps

- HTTP caching only for GET—mutations always POST
- `max-age` in response works but GraphQL responses vary
- CDN cache key must include query hash—not just URL
- Persisted queries enable better caching—but need setup

## Pagination Traps

- Cursor pagination doesn't allow "jump to page 50"—sequential only
- `totalCount` costs extra query—make optional or estimate
- Changing sort order invalidates all cursors—client must refetch
- `offset` + concurrent inserts = skipped or duplicate items

## Response Size Traps

- No built-in response size limit—giant query returns giant response
- Depth limit doesn't limit breadth—shallow but wide still big
- `@defer` and `@stream` help but not widely supported
- Compression helps but still need query limits
