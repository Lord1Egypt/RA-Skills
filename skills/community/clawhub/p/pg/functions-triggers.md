# Functions, Triggers, and NOTIFY — Logic Inside the Database

Put logic in the database when it must hold for **every** writer regardless of which service or console produced the write, and when it needs the transaction's atomicity. Keep it in the application when it is business policy that changes with product decisions — a rule in a trigger is invisible to every developer who greps the application code.

## Function Volatility Is Not Documentation

| Marker | Means | Consequence |
|---|---|---|
| `IMMUTABLE` | Same arguments always give the same result, forever | Can be used in an expression index and folded at planning time |
| `STABLE` | Constant within one statement (reads tables, no writes) | Usable in an index scan predicate; not indexable |
| `VOLATILE` (default) | Anything | Re-evaluated per row, blocks parallelism, cannot be indexed |

Getting this wrong is a correctness bug, not a hint: marking a function `IMMUTABLE` when it reads a table lets Postgres cache a result and build an index on values that later change — the index silently disagrees with the data. `now()` is STABLE, `clock_timestamp()` and `random()` are VOLATILE (SKILL.md Query Patterns).

Also declare `PARALLEL SAFE` where true: one un-marked function in a SELECT list disables parallelism for the whole query (parallelism notes in the slow-query guide).

## plpgsql That Behaves

```sql
CREATE FUNCTION apply_credit(p_user bigint, p_amount numeric) RETURNS numeric
LANGUAGE plpgsql AS $$
DECLARE v_balance numeric;
BEGIN
  UPDATE accounts SET balance = balance + p_amount
   WHERE user_id = p_user RETURNING balance INTO v_balance;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'no account for user %', p_user USING ERRCODE = 'no_data_found';
  END IF;
  RETURN v_balance;
END $$;
```

- Every `BEGIN ... EXCEPTION` block creates a **subtransaction**, which costs an XID and, in a loop over many rows, is a documented performance cliff. Catch exceptions around a batch, never inside the per-row loop.
- A function runs inside the caller's transaction and cannot commit. **Procedures** (`CALL`, PostgreSQL >=11) can commit and are what batch loops need (the backfill loop in the migrations guide).
- `RETURNS SETOF` / `RETURNS TABLE` materializes the whole result before returning it unless the function is inlinable. A simple SQL function (`LANGUAGE sql`, single statement) *is* inlined into the calling query and keeps its plan — prefer plain SQL functions over plpgsql whenever one statement suffices.
- `RAISE EXCEPTION ... USING ERRCODE` gives clients a real SQLSTATE to branch on instead of string-matching a message (errors guide).
- Name parameters `p_*` and variables `v_*`: an unqualified identifier that matches a column name resolves to the column, silently.
- `SECURITY DEFINER` requires a pinned `search_path` — that is a security requirement, covered in the security guide.

## Triggers

| Trigger form | Fires | Use |
|---|---|---|
| `BEFORE INSERT/UPDATE ... FOR EACH ROW` | Before the write, can modify `NEW` or return NULL to skip | Normalization, `updated_at` stamps, validation needing the row |
| `AFTER ... FOR EACH ROW` | After the write, sees the final row | Audit rows, denormalized counters, queueing work |
| `FOR EACH STATEMENT` (with `REFERENCING ... TABLE`, PostgreSQL >=10) | Once per statement, with transition tables | Bulk-safe auditing and aggregate maintenance |
| `INSTEAD OF` on a view | Per row | Making a view writable |
| Constraint trigger (`DEFERRABLE`) | At commit | Cross-row invariants that are temporarily violated mid-transaction |

- **Row triggers on bulk operations are the hidden cost of a slow load**: a 1M-row COPY into a table with one row trigger runs the function a million times. Prefer a statement trigger with transition tables when the logic can aggregate (bulk-load guide).
- `BEFORE` triggers that return NULL cancel the row silently — a legitimate technique that looks exactly like data loss to whoever debugs it next year. Comment it in the trigger body.
- Trigger execution order among triggers on the same event is **alphabetical by trigger name**. If order matters, encode it in the name (`10_normalize`, `20_audit`) instead of hoping.
- The `updated_at` trigger is the standard example and worth writing once:
  ```sql
  CREATE FUNCTION set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
  BEGIN NEW.updated_at = now(); RETURN NEW; END $$;
  CREATE TRIGGER t_updated BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
  ```
  Note the cost: it touches a column on every update, so keep `updated_at` out of indexes or accept the index write per update (SKILL.md Indexing Essentials).
- Logical replication does **not** fire triggers on the subscriber unless the table is `ALTER TABLE ... ENABLE ALWAYS TRIGGER`. Audit triggers on a replicated table therefore record nothing after a cutover.
- Recursion: a trigger that updates its own table fires itself. Guard with a condition (`WHEN (OLD.* IS DISTINCT FROM NEW.*)`), which also skips no-op updates and their dead tuples.

## LISTEN / NOTIFY

```sql
-- writer, inside the transaction that made the change
SELECT pg_notify('orders_new', json_build_object('id', 42)::text);
-- reader
LISTEN orders_new;
```

- Notifications are **delivered at commit** and only to sessions already listening. A consumer that reconnects misses everything sent while it was away — this is a signal bus, not a queue. Pair it with a table poll on reconnect, or use `FOR UPDATE SKIP LOCKED` as the actual queue (SKILL.md Query Patterns) and NOTIFY only as the wake-up.
- Payload limit is 8000 bytes; send an id, not the object.
- Identical notifications (same channel and payload) inside one transaction are collapsed into one delivery.
- `LISTEN` is session state: it does not survive a transaction-mode pooler (connections guide). Give listeners a dedicated direct connection.
- The queue is cluster-wide and bounded; a listener that never reads causes a growing backlog and eventually errors for the writers.

## Where This Belongs, and Where It Does Not

Good candidates: `updated_at` stamps, audit trails, denormalized counters maintained transactionally, validation that must hold against manual console writes, and generated values that need the row's other columns (a stored `tsvector`, in the search guide — use a generated column rather than a trigger where the expression allows it).

Bad candidates: business workflows spread across chained triggers (unreadable, untestable, undebuggable), calls to external services (there is no rollback for an HTTP request already sent), and anything whose failure should not abort the user's transaction. Version function definitions in migrations like any other schema object — a function edited in a console exists in production and in no repository.
