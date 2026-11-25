---
name: google-ai-model-api-audit
description: "Establish and monitor real billed spend and token use for Google AI models (Gemini API, Generative Language API, Vertex AI). Use when asked what Google AI/Gemini is costing, to verify a Google Cloud bill, to find which model or project is expensive, or to set up a recurring Google cost audit."
---

# Google AI Model API Audit

Turn "Google feels expensive" into a billed number, then into a query you can run daily.

Two rules decide whether the audit is worth anything:

1. **The source of truth is the billing ledger, not a token counter.** Platform-side usage logs
   estimate; they cannot see credits, price drift, or unpriced entries.
2. **Report gross and net separately.** When credits are active, net is $0.00 while gross climbs.
   Alerting on net hides the whole problem until the buffer runs out.

## Step 0 — Intake

Ask the six questions in `references/intake.md` before touching any console. Record the answers in
`state/google-ai-audit.json` in the working workspace.

**Done when** owner email, billing account ID, export project ID, export state, admin status, and
thresholds are all recorded. Never proceed on an inferred billing account ID.

## Step 1 — Ground truth in five minutes (no setup)

The Reports page holds history that a new BigQuery export cannot backfill:

```
https://console.cloud.google.com/billing/<BILLING_ACCOUNT_ID>/reports
  ;timeRange=CUSTOM_RANGE;from=YYYY-MM-DD;to=YYYY-MM-DD;timeGrouping=GROUP_BY_DAY
```

Read it with a browser already signed in:

```bash
node scripts/console-report.mjs --account <BILLING_ACCOUNT_ID> \
  --from 2026-11-16 --to 2026-11-22 --authuser 1 --json
```

Output fields that matter:

- `spent` — **net**, after credits. Often `-$0.00`, and that is not good news by itself.
- `saved` — **gross usage paid by credits**. This is the real spend.
- `table` — per-day Usage cost / savings / Subtotal rows.

No browser available: `references/no-browser-fallback.md` (ask for two sentences, or a CSV).

**Done when** you can state gross and net for the last 7 and 30 days, and name the daily peak.

### The account trap

`authuser` is the 0-based index of the Google account in that Chrome profile. The wrong index
returns a sign-in wall or a different (empty) billing account. Confirm the identity before trusting
`$0` results: open `https://myaccount.google.com/?authuser=<N>` and check the email.

## Step 2 — Enable the billing export (makes monitoring a query)

Follow `references/console-walkthrough.md`. Enable **standard and detailed** usage cost into one
dataset in a project you control.

Non-negotiables:

- It is **per billing account**, not per project.
- **No backfill.** Data starts at enable time; ~24h before the first table appears.
- Requires **Billing Account Administrator**.
- Dataset IDs are lowercase; table suffix is the account ID with dashes to underscores.

**Done when** both exports read Enabled with the right project and dataset, recorded in state.

## Step 3 — Read-only credentials for the agent

Create a service account in the export project with exactly two roles:

- **BigQuery Data Viewer** — read the tables.
- **BigQuery Job User** — run queries.

Download a JSON key, store it outside any repo, `chmod 600`. Then:

```bash
python3 scripts/bigquery.py --key <KEY> --project <EXPORT_PROJECT> --sql "SELECT 1 AS ok"
```

This mints its own token, so it works when the user gcloud session is expired — the usual reason
the `bq` CLI refuses a service-account key.

**Done when** the probe query returns a row and no key material is printed into chat or logs.

## Step 4 — Query what actually costs money

Read `references/bigquery-schema.md`, then run in this order:

1. `references/sql/daily-gross-net.sql` — trend, and the audit baseline.
2. `references/sql/by-sku.sql` — where the money goes. Model names live in `sku.description`.
3. `references/sql/by-token-type.sql` — input vs output vs cached.
4. `references/sql/by-project.sql` — experiment vs production.
5. `references/sql/gemini-models.sql` — Gemini only, by model.

Substitute `<PROJ>`, `<DS>`, `<ACC>` in every file. Never paste a query with placeholders left in.

**Done when** you have gross by day, the top three SKUs with dollar amounts, and the model that
accounts for the largest share.

## Step 5 — Recommend from the numbers, in leverage order

Routing (model tier) > output length > caching > call volume > region. Each recommendation must
cite the SKU row that justifies it. "Use a cheaper model" without the dollar split is noise.

## Step 6 — Daily audit so this never has to be re-derived

Install a scheduled job that reads the same source and posts: gross, credits, net, driver services,
plus a flag when `net != 0.00` or `gross > threshold`.

Until the export exists, drive `scripts/console-report.mjs` for the current day; after it exists,
prefer `scripts/bigquery.py` with `sql/daily-gross-net.sql`.

**Done when** the job exists, has run once, and delivered a message the owner confirmed receiving.

## Verification — run this before reporting success

1. Console gross for a completed day equals the export gross for the same day (within one day of lag).
2. `gross + credits == net` for every row you publish.
3. Net of `0.00` is never reported as "no spend"; report gross alongside it.
4. Any estimate from a token ledger is labelled as an estimate, with its unpriced-entry count.
5. No key, token, or private key path is echoed into a shared channel.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `$0` for an account that is clearly billing | Wrong `authuser` index, or a different Google account | Verify identity at `myaccount.google.com/?authuser=N` |
| Sign-in wall in automation | Profile not authenticated for that Google account | Sign in once in that profile, or use another profile |
| `bq` refuses service-account key | Expired user gcloud OAuth token | Use `scripts/bigquery.py`; do not fight gcloud |
| Export table missing after 3 days | Export toggled off, or project deleted | Re-check Billing export status; re-enable knowingly (new start date) |
| Console says spend, Report says `$0.00` | Looking at net while credits are active | Read `saved` / gross |
| Costs appear a day late | Export and console both lag ~24h | Compare completed days only |
| Someone else "sees a large Google charge" | It may be an AI/One subscription on the card, not Cloud | Ask what page they are looking at before auditing |

## Proof this works (2026-11-23)

On billing account `<BILLING_ACCOUNT_ID>`, the console showed Nov 22 gross `$20.04`, a 7-day gross
of `$34.21`, and a 30-day gross of `$98.30` with net `$0.00` — a token-ledger estimate for the same
period was ~30% low. Same day, `billing_export` was enabled, a `billing-reader` service account
queried `SELECT 1` successfully from outside Google Cloud, and the table list read 0 tables (correct,
first tables land next day).

## Resources

- `scripts/console-report.mjs` — read Billing Reports as JSON via Chrome DevTools Protocol.
- `scripts/bigquery.py` — run SQL with a service-account key, no gcloud.
- `scripts/bigquery_token.py` — mint a scoped token from a key (importable).
- `references/intake.md` — the six questions, and the "large spend" false alarms.
- `references/console-walkthrough.md` — enable and verify the export.
- `references/bigquery-schema.md` — columns, gross/net arithmetic, levers.
- `references/no-browser-fallback.md` — when there is no browser to drive.