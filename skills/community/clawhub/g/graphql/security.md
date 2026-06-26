# Security Traps

## Query Depth/Complexity Traps

- No depth limit = `{ user { friends { friends { friends... } } } }` DoS
- Depth limit alone not enough—wide queries still expensive
- Complexity scoring must multiply lists—`users(first:1000)` = 1000x cost
- Introspection queries can be expensive—limit or disable in prod

## Authentication Traps

- Auth in resolvers runs AFTER parsing—malformed query still parsed
- Token in header, not query—queries are often logged
- Subscription auth checked once at connect—not per message
- Schema visible without auth (introspection)—reveals attack surface

## Authorization Traps

- Field-level auth easy to forget—new field defaults to accessible
- `@auth` directives not standard—implementation varies
- Nested data may expose unauthorized parent info—check at each level
- Returning null vs error—null hides existence, error confirms it

## Input Validation Traps

- GraphQL validates types, not business rules—length, format, ranges
- Deeply nested input can crash parser—limit input depth
- Batch mutations bypass per-request limits—10 mutations = 10x load
- Variables not sanitized—injection still possible in dynamic queries

## Rate Limiting Traps

- Per-request limit not enough—one complex query = many simple ones
- Rate by complexity score, not just count
- Persisted queries bypass limits differently—known cost
- Subscriptions hold connections—limit concurrent per user

## Information Disclosure Traps

- Error messages expose internals—stack traces, SQL, paths
- Suggestions in errors helpful but revealing—"did you mean password?"
- Introspection reveals entire schema—disable or auth-protect
- Timing attacks on auth—null for missing vs unauthorized
