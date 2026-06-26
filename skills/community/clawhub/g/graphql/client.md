# Client-Side Traps

## Cache Normalization Traps

- Without `id`, objects not deduplicated—fetching same user twice = two cache entries
- `id` must be globally unique—`User:1` and `Post:1` need `__typename`
- Nested object without `id` not individually cached—updates don't propagate
- Cache doesn't know about server deletions—manual removal needed

## Optimistic Update Traps

- Optimistic response needs `__typename`—cache won't normalize without it
- Rollback on error can flash old state—handle loading state
- Optimistic ID must match server ID—or use merge functions
- List additions need to update queries—cache doesn't know position

## Fragment Traps

- Fragment on wrong type silently matches nothing—no error
- Fragment spread without `...` is syntax error—easy typo
- Collocated fragments need unique names—duplicates error
- Fragment can reference field that query doesn't fetch—runtime null

## Query Traps

- `skip: true` doesn't remove from response—field is undefined
- `include: false` same as skip—conditional including
- Variable not passed but required—runtime error not compile error
- Watching query with different variables—multiple cache entries

## Subscription Traps

- Reconnect doesn't re-establish subscriptions—must re-subscribe
- Subscription returns one item at a time—no batching like query
- Error in subscription handler can kill connection
- Server restart requires client reconnect logic

## Error Handling Traps

- Partial data with errors is valid—check both `data` and `errors`
- `error.graphQLErrors` for field errors—`error.networkError` for transport
- Error policy determines behavior—`none` throws, `all` returns both
- Subscription error handling different—`onError` callback
