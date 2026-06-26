# Google Analytics skill

Query GA4 properties using the [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1).

## Capabilities

- **Realtime metrics** — e.g. active users in the last N minutes  
- **Historical reports** — custom date ranges, metrics, dimensions, paging  
- **Metadata** — discover valid dimension and metric API names  
- **Property list hint** — Data API alone cannot enumerate properties; doc explains where to find the numeric ID  

## Setup

### 1. Create a service account

1. Open [Google Cloud Console](https://console.cloud.google.com/).  
2. Create or select a project.  
3. Enable **Google Analytics Data API**.  
4. Create a service account: **IAM & Admin** → **Service Accounts** → **Create service account**.  
   - Optional GCP role: **BigQuery Job User** (only if you also use BigQuery).  
5. Finish the wizard.

### 2. Create a JSON key

1. Open the service account → **Keys**.  
2. **Add key** → **Create new key** → **JSON**.  
3. Download the file and save it as `ga-credentials.json` (or any path you pass via `--credentials` / `GOOGLE_APPLICATION_CREDENTIALS`).

### 3. Grant GA4 access

1. Open [Google Analytics](https://analytics.google.com/).  
2. Select the property.  
3. **Admin** (gear) → **Property access management**.  
4. **Add users** → enter the service account email (`…@….iam.gserviceaccount.com`).  
5. Role: at least **Viewer**.

### 4. Credentials location

Either:

- **A.** Place `ga-credentials.json` in this skill directory, or  
- **B.** Set `GOOGLE_APPLICATION_CREDENTIALS` to the absolute path of the JSON key.

Never commit real keys. `.gitignore` excludes `ga-credentials.json` and `config.json`.

## Examples

### Property list guidance

```bash
python ga_query.py --action list-properties
```

### Realtime (active users)

```bash
python ga_query.py --action realtime \
  --property-id YOUR-GA4-PROPERTY-ID
```

### Historical

```bash
python ga_query.py --action historical \
  --property-id YOUR-GA4-PROPERTY-ID \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions,eventCount \
  --dimensions country,deviceCategory
```

### Metadata

```bash
python ga_query.py --action metadata \
  --property-id YOUR-GA4-PROPERTY-ID
```

## Arguments

### Common

| Argument | Description | Default |
|----------|-------------|---------|
| `--property-id` | Numeric GA4 property ID | Required (except `list-properties`) |
| `--credentials` | Service account JSON path | `ga-credentials.json` |

### Realtime

| Argument | Description | Default |
|----------|-------------|---------|
| `--metrics` | Comma-separated metrics | `activeUsers` |
| `--dimensions` | Comma-separated dimensions | (none) |
| `--minute-range` | Minutes ago window, e.g. `0-30` | `0-30` |

### Historical

| Argument | Description | Default |
|----------|-------------|---------|
| `--start-date` | Start (`YYYY-MM-DD` or relative) | Required |
| `--end-date` | End | Required |
| `--metrics` | Comma-separated metrics | `activeUsers` |
| `--dimensions` | Comma-separated dimensions | (none) |
| `--limit` | Max rows | `10000` |
| `--offset` | Paging offset | `0` |

## Common metrics

| Name | Meaning                                              |
|------|------------------------------------------------------|
| `activeUsers` | Active users                                    |
| `sessions` | Sessions                                            |
| `eventCount` | Event count                                       |
| `engagementRate` | Engagement rate                               |
| `averageSessionDuration` | Avg session duration (seconds)      |
| `screenPageViews` | Page / screen views                         |
| `conversions` | Conversions                                     |
| `totalRevenue` | Revenue                                        |

## Common dimensions

| Name | Meaning |
|------|---------|
| `country` | Country |
| `city` | City |
| `deviceCategory` | desktop / mobile / tablet |
| `eventName` | Event name |
| `pagePath` | Page path |
| `source` | Traffic source |
| `medium` | Medium |
| `campaign` | Campaign |
| `date` | Date |

## Date expressions

- Absolute: `2024-01-15`  
- Relative: `today`, `yesterday`, `7daysAgo`, `30daysAgo`  

## Output

Default: Markdown tables. Use `--output json` for machine-readable output.

## Dependencies

```bash
pip install google-analytics-data
```

Optional (traffic source report + DingTalk): `pip install requests` and set `DINGTALK_WEBHOOK` / `DINGTALK_SECRET`.

## References

- [Data API docs](https://developers.google.com/analytics/devguides/reporting/data/v1)  
- [Python client](https://github.com/googleapis/google-analytics-data-python)  
- [Dimensions & metrics schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)  
