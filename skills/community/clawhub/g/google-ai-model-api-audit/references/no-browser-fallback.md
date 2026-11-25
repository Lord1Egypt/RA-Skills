# When there is no browser to drive

scripts/console-report.mjs needs a Chrome with `--remote-debugging-port`. Sometimes there is none,
or the profile has no authenticated Google session. Escalate in this order.

## 1. Ask the owner for the number, precisely

Give them the URL, not a description:

```
https://console.cloud.google.com/billing/<BILLING_ACCOUNT_ID>/reports;timeRange=CUSTOM_RANGE;from=YYYY-MM-DD;to=YYYY-MM-DD;timeGrouping=GROUP_BY_DAY
```

Ask for the two sentences at the top of the page:

- `You spent -$X between ...` → **net**, after credits
- `You saved -$Y during this period` → **gross paid by credits**, i.e. the real spend

Those two lines answer the question. The chart does not add anything.

## 2. CSV export from the same page

`Download CSV` sits above the cost table. It exports the current view — so set the date range and the
grouping **before** clicking. This is the only way to recover history from before the BigQuery export
was enabled, because the export cannot backfill.

## 3. Command-line routes, and why they usually fail

| Attempt | Result |
|---|---|
| `bq ls --service_account_credential_file=key.json` | Refuses when the user's gcloud OAuth token is expired, even though the key is valid. `Reauthentication failed` |
| `gcloud billing accounts list` | Works for account IDs, gives **no cost data** |
| Cloud Billing REST API | Account/project/budget metadata only. **No cost figures.** |
| Budget API | Budget config and alerts, not actual spend readings |
| Monitoring API | Works only with a project-scoped monitoring role; noisy and not billing-accurate |

The reliable programmatic path is the BigQuery export (see console-walkthrough.md) read with
`scripts/bigquery.py`, which mints its own token and never touches gcloud.

## 4. Local token ledgers as a last resort

If an agent platform keeps its own per-call usage log, that ledger can estimate spend. Treat it as an
estimate and label it as one:

- it usually misses some priced entries (report the count),
- it depends on a price table that drifts from the vendor's,
- it cannot see credits, so it cannot tell you what will actually be charged.

Real case: a token ledger estimated ~$13.89/day while the console showed $20.04 for the same day.
The estimate was directionally right and numerically wrong. Get the ledger's number only to decide
whether to escalate to the console.
