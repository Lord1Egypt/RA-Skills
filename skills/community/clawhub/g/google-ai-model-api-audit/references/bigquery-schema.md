# BigQuery billing export — schema and the queries that matter

Placeholders used below: `<PROJ>` export project, `<DS>` dataset, `<ACC>` billing account ID with
dashes replaced by underscores. Both tables share the same prefix pattern:

- Standard: `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
- Detailed: `<PROJ>.<DS>.gcp_billing_export_resource_v1_<ACC>`

## Columns worth knowing

| Column | Notes |
|---|---|
| `cost` | **Gross** usage cost for the row, in `currency`. Does not include credits. |
| `credits` | Repeated field: `credits.amount` (negative), `credits.type`, `credits.name`, `credits.full_name`, `credits.id` |
| `cost_type` | `regular`, `tax`, `adjustment`, `rounding`. Filter `= 'regular'` for usage analysis. |
| `service.description` | e.g. `Gemini API`, `Vertex AI`, `Cloud Run Functions` |
| `sku.description` | Where the model actually appears, e.g. `Gemini 2.5 Pro Input Tokens` |
| `project.id` / `project.name` | Which project spent it |
| `usage.amount` / `usage.unit` | Quantity, e.g. tokens or requests |
| `invoice.month` | `YYYYMM`, cheap partition-friendly filter |
| `export_time`, `usage_start_time` | UTC. Daily grouping needs a timezone decision. |

Detailed table adds `resource.name`, `resource.global_name`, `labels`, `system_labels` —
use `labels` to attribute spend to an environment, team, or agent.

## Net vs gross — do this correctly or the audit is worthless

```sql
net_usd = SUM(cost) + SUM(SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)
```

The standard pattern for a per-day table:

```sql
SELECT
  DATE(usage_start_time) AS day,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS credits_usd,
  ROUND(SUM(cost) + SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS net_usd
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY day
ORDER BY day DESC
```

A month of gross spend fully offset by credits shows `net_usd = 0.00` while `gross_usd` keeps
climbing. **Gross is the trend; net is the cash flow.** Report both, every time.

## The four queries

### 1. Daily gross / credits / net — `sql/daily-gross-net.sql`
The headline series. Use it for trend and for the daily audit.

### 2. By SKU — `sql/by-sku.sql`
`sku.description` is where the model name lives for Generative Language and Vertex AI.
Run this first when someone asks "what is expensive".

### 3. By token type — `sql/by-token-type.sql`
Splits input vs output vs cached tokens (`usage.unit` + `sku.description`). Output tokens are
typically 4-8x the price of input, so a chatty agent shows up here, not in project totals.

### 4. By project — `sql/by-project.sql`
Separates the experiment from production. If one project is 90% of spend, the fix is that project.

### 5. Gemini only, by model — `sql/gemini-models.sql`
Filters to `service.description IN ('Gemini API','Vertex AI','Generative Language API')` and groups
by a model name parsed out of `sku.description`.

## Cost-control levers, in order of leverage

1. **Routing.** Send routine work to the cheapest capable model. Model tier is the biggest single lever.
2. **Output length.** Output tokens dominate cost; cap them.
3. **Caching.** Cached input tokens are discounted heavily where supported.
4. **Call volume.** Retries, fan-outs and polling loops are usually waste, not work.
5. **Region/SKU choice.** Rarely the issue for API-first workloads.

Do not propose a lever without the SKU-level numbers that justify it.
