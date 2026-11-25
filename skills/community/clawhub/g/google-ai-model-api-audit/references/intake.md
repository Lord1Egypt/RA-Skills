# Intake — the six answers you need first

Ask these in one message. Every one of them has changed a real audit's answer, so do not
infer any of them from context.

| # | Question | Why it matters | How the user finds it |
|---|---|---|---|
| 1 | Which Google account owns the billing? (email) | Cost data is scoped to the account, not the machine. A second signed-in account silently returns `$0` or a sign-in wall. | The avatar in the top-right of console.cloud.google.com, or myaccount.google.com |
| 2 | Billing account ID (`XXXXXX-XXXXXX-XXXXXX`) | Every Reports URL and every export table name is keyed to it. | Billing → Account management → the ID under the account name |
| 3 | Which project ID receives the billing export? | Exports write into one dataset in one project. Display names are not IDs. | The project picker; the ID appears under "Project ID" on the project dashboard |
| 4 | Are you Billing Account Administrator on that account? | The export cannot be enabled without it. Any lesser role will show the page but refuse Save. | IAM on the billing account (Billing → Account management → Permissions) |
| 5 | Is Cloud Billing → BigQuery export already on? Which dataset? | Re-enabling an existing export creates a duplicate dataset or none at all. | Billing → Billing export |
| 6 | Alert thresholds — and gross or net? | With credits active, gross and net differ by an order of magnitude. Alerting on net tells you nothing until the buffer is gone. | Ask; propose defaults: flag gross > $25/day, and always report net |

## Ask a seventh when the answer is "I don't see a large bill"

Ask what *they* are looking at. A "large spend" sighting is often one of:

- a Google One / AI plan subscription charge on the card (not Google Cloud and not in any billing account),
- a different billing account or a different Google account,
- the Estimator page, which is a projection, not a bill.

Getting this wrong sends you auditing the wrong ledger for a day.

## Persist the answers

Write them once, then read them on every later run:

```json
// state/google-ai-audit.json  (inside the agent's working workspace, not the skill dir)
{
  "owner_email": "someone@example.com",
  "billing_account_id": "<BILLING_ACCOUNT_ID>",
  "export_project_id": "<EXPORT_PROJECT>",
  "export_dataset": "billing_export",
  "export_enabled": true,
  "export_enabled_at": "2026-11-23",
  "service_account_email": "billing-reader@<EXPORT_PROJECT>.iam.gserviceaccount.com",
  "key_path": "~/.config/gcp/billing-reader.json",
  "thresholds": { "daily_gross_usd": 25, "weekly_gross_usd": 100, "alert_on_net_nonzero": true }
}
```

**Done when** all six answers are recorded and the file exists.
