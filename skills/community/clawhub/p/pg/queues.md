# Queues and Outbox — Background Work Without a Broker

Postgres is a competent queue up to roughly thousands of jobs per second on ordinary hardware. Below that, one system with one transaction beats a database plus a broker plus the consistency problem between them. Above it, or when you need fan-out to many independent consumer groups, use a real broker.

## The Claim Query

```sql
UPDATE jobs SET state = 'running', locked_at = now(), attempts = attempts + 1
WHERE id IN (
  SELECT id FROM jobs
  WHERE state = 'queued' AND run_after <= now()
  ORDER BY priority DESC, run_after
  FOR UPDATE SKIP LOCKED
  LIMIT 10
)
RETURNING *;
```

- `SKIP LOCKED` is what makes this work: each worker skips rows another worker already locked instead of queueing behind them. Without it, N workers serialize on the same head row.
- Claim in batches (5-50). One row per round trip makes the network the bottleneck long before the database is.
- `ORDER BY` inside the subquery, and index it: `CREATE INDEX ON jobs (state, run_after) WHERE state = 'queued'` — a partial index whose size tracks the backlog, not the history.
- The whole claim is one statement, so a worker that dies mid-claim leaves nothing half-claimed.

## Table Shape

```sql
CREATE TABLE jobs (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  kind        text NOT NULL,
  payload     jsonb NOT NULL,
  state       text NOT NULL DEFAULT 'queued',    -- queued|running|done|failed
  priority    int NOT NULL DEFAULT 0,
  attempts    int NOT NULL DEFAULT 0,
  max_attempts int NOT NULL DEFAULT 5,
  run_after   timestamptz NOT NULL DEFAULT now(),
  locked_at   timestamptz,
  last_error  text,
  created_at  timestamptz NOT NULL DEFAULT now()
);
```

- `run_after` gives you delays, retries with backoff, and scheduling in one column: retry is `run_after = now() + (interval '1 second' * power(2, attempts))`, state back to `queued`.
- Dead letter is a state, not another table: `state = 'failed'` when `attempts >= max_attempts`, with `last_error` kept. A separate table doubles the queries needed to answer "what is stuck".
- Stalled jobs (worker crashed while `running`): a reaper resets rows whose `locked_at < now() - interval '5 minutes'` back to `queued`. Choose the interval well above your longest legitimate job, or the reaper will duplicate work.
- Idempotency belongs in the job handler, not in the queue. Any at-least-once queue — this one included — will occasionally run a job twice.

## Keeping It From Bloating

A queue table is the worst case for MVCC: high insert, high update, high delete, tiny live set (vacuum guide). Without attention it grows to gigabytes while holding a hundred rows.

- Per-table autovacuum: `ALTER TABLE jobs SET (autovacuum_vacuum_scale_factor = 0.01, autovacuum_vacuum_cost_delay = 0);`
- Delete completed jobs on a schedule rather than keeping them "for history" — or move them to a partitioned archive table and drop old partitions.
- Keep the payload small. A `jsonb` payload updated on every attempt rewrites the whole value and every index entry (json guide); store a reference when the input is large.
- Watch `n_dead_tup` on this table specifically; it is the first place a vacuum problem shows.

## Wake-Up Without Polling

Polling every second is fine and costs almost nothing with the partial index. When latency matters, combine:

1. Worker `LISTEN`s on a channel and blocks.
2. The producer's transaction ends with `pg_notify('jobs', '')`.
3. The worker wakes, runs the claim query, and loops until it claims nothing.
4. It also polls on a slow timer (5-30s) as the safety net.

Step 4 is not optional: notifications only reach sessions already listening, so anything sent during a reconnect is lost (details in the functions-triggers guide). The poll is the correctness mechanism; NOTIFY is the latency optimization.

## The Transactional Outbox

The problem: a request must both write to the database and publish an event. Two systems, no shared transaction — a crash between them either loses the event or publishes one for a rolled-back write.

```sql
BEGIN;
  UPDATE orders SET state = 'paid' WHERE id = 42;
  INSERT INTO outbox (topic, payload) VALUES ('order.paid', '{"id":42}');
COMMIT;
```

A relay process then reads the outbox with the same `FOR UPDATE SKIP LOCKED` claim and publishes to the broker, marking rows sent. Properties worth stating plainly: the write and the event commit atomically, delivery is at-least-once, and ordering is only guaranteed per key if the relay claims in key order with one worker per key.

The alternative is reading the WAL directly with logical decoding (replication guide), which needs no outbox table and no relay writes — at the cost of coupling the consumer to the physical schema, and of a replication slot that will fill your disk if the consumer dies.

## Scheduled and Recurring Work

- `pg_cron` runs schedules inside the database (extensions guide): good for maintenance SQL (partition rollover, retention deletes, statistics refresh), not for application jobs that need retries and visibility.
- Recurring application work belongs in the same `jobs` table with a `run_after` computed at completion — one system to monitor instead of two.
- Whatever schedules it, make the job itself idempotent and safe to skip: a scheduler that misses a window must never leave permanent damage.

## Monitoring

Four numbers answer everything: backlog (`count(*) WHERE state='queued'`), oldest queued age (`now() - min(run_after)`), failure rate, and stalled count. Alert on the age, not on the depth: a queue of 10,000 that drains in 30 seconds is healthy, and a queue of 3 that has not moved in an hour is an outage.
