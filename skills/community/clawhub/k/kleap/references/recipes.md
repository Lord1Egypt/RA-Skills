# Kleap recipes

`kleap` = `npx -y kleap-cli@latest`. Add `--json` whenever you need to parse a value.

## 1. Launch a site with a lead form, then read the leads

```bash
kleap create "landing page for Sunny Paws, a dog-walking business in Austin: warm tone, services + pricing + a contact form (name, email, phone, message)"
# ✓ created app 5310 — https://sunny-paws-walk.kleap.io      ← only now is it live
```

Later (the user asks "did anyone contact me?"):

```bash
kleap forms 5310 --limit 20
# 2026-09-25T10:00:00Z	name=Ada · email=ada@example.com · message=Walk on Tuesdays?
kleap forms 5310 --since 2026-09-24T00:00:00Z --json    # only new ones, flat objects
```

To follow up regularly, remember the newest `submitted_at` you have seen and
pass it as `--since` next time (it is inclusive: drop `submission_id`s you
already handled). An empty list on a new site is normal.

## 2. Database CRUD

```bash
kleap db schema 5310
# leads (~2 rows): id integer pk, email text not null, status text, created_at timestamptz
kleap db rows 5310 leads --where '{"status":"new"}' --order-by created_at --order desc --limit 50
kleap db insert 5310 leads '[{"email":"a@b.co","status":"new"},{"email":"c@d.co","status":"new"}]'
kleap db update 5310 leads --where '{"id":12}' --set '{"status":"contacted"}'
kleap db delete 5310 leads --where '{"id":13}'
kleap db sql 5310 "select status, count(*) from leads group by status"
```

- `rows` prints one JSON object per line; `… more rows — next page: --offset N` means page on.
- `update`/`delete` need a non-empty `--where` (equality on columns). For
  anything else (ranges, joins) use `db sql` with `--params '[...]'` for values.
- Creating a table with `db sql`: include
  `ALTER TABLE <t> ENABLE ROW LEVEL SECURITY;` or you get `RLS_REQUIRED`.
  For a table the site itself should use (forms, dashboards), prefer
  `kleap edit <app> "<describe the feature>"` — Kleap's AI wires the schema,
  the policies and the pages together.
- `DATABASE_NOT_PROVISIONED` → `kleap edit <app> "add a database"`, then retry.
- `db sql` is owner-level and always needs `database:write` (a read-only key
  can still use `db schema` and `db rows`). `db schema` row counts are estimates.

## 3. Buy a domain and connect it

```bash
kleap domains search sunnypaws --tlds .com,.co
# sunnypaws.co	14.99 USD
kleap domains buy sunnypaws.co --app 5310
# → checkout for sunnypaws.co (14.99 USD, 1 year): https://checkout.stripe.com/...
#   NOT bought yet — the user must open this link and pay. ...
```

Tell the user: "Here is the payment link for sunnypaws.co — once you pay, it is
registered and connected to your site." Do **not** say it is bought. After
they confirm payment:

```bash
kleap domains check sunnypaws.co
# ✓ sunnypaws.co active — https://sunnypaws.co (TLS provisioning)
# … sunnypaws.co pending DNS — …   ← not ready yet: check again later
```

A domain the user **already owns** elsewhere: `kleap domains connect mybakery.com 5310`
→ relay the A record it prints; then `kleap domains check mybakery.com` until active.

## 4. Non-blocking flows

```bash
kleap create "…" --no-wait --json      # → {"task_id":"task_…","app_id":5310,…}
# … do other work …
kleap task task_abc --wait             # long-polls to completed / failed (≤20 min)
kleap task task_abc --json             # instant snapshot: status queued|processing|completed|failed
```

- `completed` → the change is built and live (`result.production_url`).
- `failed` → exit 1 with the code: `kleap task retry <task_id> --wait`
  (returns a NEW task id). `TASK_TIMEOUT`/`STALE_TASK`: up to 2 retries.
  `TASK_FAILED`: 1 retry, then stop and report the message.
- `kleap publish <app> --no-wait` starts a deploy; `kleap status <app>` shows
  the live URL once it is serving.

## 5. Precise copy fix without the AI

```bash
kleap files ls 5310 | grep src/components
kleap files cat 5310 src/components/Footer.astro
kleap files edit 5310 src/components/Footer.astro --find "+1 512 555 0100" --replace "+1 512 555 0199"
kleap publish 5310
# ✓ published https://sunny-paws-walk.kleap.io
```
