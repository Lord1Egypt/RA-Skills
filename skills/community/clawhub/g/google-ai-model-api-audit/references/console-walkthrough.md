# Console walkthrough — enabling the billing export

The export is the difference between guessing and querying. It is also the step most likely to
be done half-right, so verify visually.

## Where

Billing → select the billing account → **Billing export** (left nav, under Cost management).

## What to enable

Enable **both**, they are not the same table:

| Option | Table produced | Contains |
|---|---|---|
| Standard usage cost | `gcp_billing_export_v1_<ACCOUNT>` | Cost, credits, SKU, project, labels |
| Detailed usage cost | `gcp_billing_export_resource_v1_<ACCOUNT>` | Everything above **plus** resource-level and system labels |

`<ACCOUNT>` is the billing account ID with dashes replaced by underscores:
`<BILLING_ACCOUNT_ID>` → `<ACC>`.

Detailed is the one that answers "which workload", so enable it even when standard already exists.

## How

For each option: **Edit settings** → Project = the target project → Dataset ID = a new dataset
(e.g. `billing_export`) → **Save**.

Then verify on the same page, for each option:

1. Status reads **Enabled**.
2. The row shows the project you chose.
3. The dataset ID is exactly what you typed.

BigQuery dataset IDs are lowercase. Typing `Billing_export` in a form and reading back
`billing_export` is correct behaviour, not a bug — do not "fix" it.

## Rules that surprise people

- **Per billing account, not per project.** One export covers every project charged to that account.
  Do not enable one per project.
- **No backfill.** The export begins at enable time. History before that only exists in
  Billing → Reports (see console-report.mjs) or an invoice.
- **~24 hour lag** before the first table appears, then it updates through the day.
- The dataset lives in a **US** multi-region by default; a query must run in a location compatible
  with the data (omit the location and BigQuery infers it).
- Deleting and re-enabling creates a **new** export with a fresh start date. Do not toggle it casually.

## Verify table creation the day after

```bash
python3 scripts/bigquery.py --key <KEY> --project <EXPORT_PROJECT> \
  --sql "SELECT table_name FROM \`<EXPORT_PROJECT>.<DATASET>\`.INFORMATION_SCHEMA.TABLES ORDER BY table_name"
```

Empty `totalRows` on day one is expected. Empty on day three is a failure: check that the billing
account still has the export marked Enabled and that the chosen project has never been deleted.

## Verified console states (2026-11-23, account <BILLING_ACCOUNT_ID>)

- Standard + Detailed both Enabled → `billing_export` in project `<EXPORT_PROJECT>`.
- Table list immediately after enabling: `totalItems: 0` — correct, tables appear next day.
- `billing-reader` service account with BigQuery Data Viewer + Job User ran `SELECT 1` successfully
  from outside Google Cloud, using an exported JSON key.
