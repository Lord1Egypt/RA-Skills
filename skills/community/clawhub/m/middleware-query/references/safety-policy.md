# Safety Policy

- Default read-only.
- Enforce timeout and result limits for all queries.
- Mask sensitive fields in output (`password`, `token`, `secret`, `phone`, `email`).
- Never print raw credentials in logs.

## SQL denylist

Reject SQL containing:

- `INSERT`, `UPDATE`, `DELETE`, `REPLACE`, `UPSERT`, `MERGE`
- `DROP`, `TRUNCATE`, `ALTER`, `CREATE`, `RENAME`
- `GRANT`, `REVOKE`

## Redis denylist

Reject commands:

- `SET`, `DEL`, `FLUSHDB`, `FLUSHALL`, `EXPIRE`, `PERSIST`
- `HSET`, `SADD`, `ZADD`, `LPUSH`, `RPUSH`

## Mongo denylist

Reject operations:

- `insert*`, `update*`, `replace*`, `delete*`
- `findOneAndUpdate`, `findOneAndDelete`, `bulkWrite`
- aggregation write stages like `$out`, `$merge`
