# Google Analytics skill — research notes

## 1. Findings

### GA4 Data API v1

Official API for GA4 reporting. **GA4 only** (not Universal Analytics).

**Notable properties:**

- Mature, stable surface area for core reporting  
- REST and gRPC  
- Client libraries for several languages  
- Auth: OAuth 2.0 (user) or service account (server)  

### API methods (selection)

| Method | Use |
|--------|-----|
| `runReport` | Standard historical reports |
| `runRealtimeReport` | Last ~30 minutes (up to ~60 on GA360) |
| `getMetadata` | List valid dimension/metric API names |
| `batchRunReports` | Multiple reports in one call |
| `runPivotReport` | Pivot-style layout |
| `runFunnelReport` | Funnels (check product status / quota) |

### Authentication

**Recommended: service account** for automation — no interactive login, good for servers and CI.

Steps (summary):

1. Create SA in Google Cloud.  
2. Download JSON key.  
3. Add SA email in GA4 property access (Viewer+).  
4. Point `GOOGLE_APPLICATION_CREDENTIALS` at the JSON path (or use ADC).  

**OAuth 2.0** fits user-consent flows; more moving parts (refresh tokens).

### Python library

Package: `google-analytics-data`

```bash
pip install google-analytics-data
```

Minimal example:

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest
)

client = BetaAnalyticsDataClient()
request = RunReportRequest(
    property="properties/123456789",
    dimensions=[Dimension(name="country")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")]
)
response = client.run_report(request)
```

### Common metrics

| Name | Type | Note |
|------|------|------|
| `activeUsers` | int | Users |
| `sessions` | int | Sessions |
| `eventCount` | int | Events |
| `screenPageViews` | int | Views |
| `engagementRate` | float | 0–1 |
| `averageSessionDuration` | float | Seconds |
| `conversions` | int | Configured conversions |
| `totalRevenue` | currency | If ecommerce enabled |
| `newUsers` | int | New users |
| `bounceRate` | float | Where supported |

### Common dimensions

Examples: `country`, `city`, `deviceCategory`, `date`, `pagePath`, `pageLocation`, `pageTitle`, `source`, `medium`, `campaign`, `eventName`, `browser`, `operatingSystem`, `language`.

### Date formats

- Absolute: `YYYY-MM-DD`  
- Relative: `today`, `yesterday`, `NdaysAgo`  

### References reviewed

- [google-analytics-data-python](https://github.com/googleanalytics/google-analytics-data-python)  
- [Data API docs](https://developers.google.com/analytics/devguides/reporting/data/v1)  

## 2. Skill design

### Layout (conceptual)

- `SKILL.md` — setup  
- `README.md` — quick start  
- `QUICK_REFERENCE.md` — cheatsheet  
- `EXAMPLES.md` — recipes  
- `ga_query.py` — CLI  
- `openclaw_ga.py` — integration helper  
- `test_connection.py` — credential/API checks  
- `ga-credentials.json.example` — shape of the key file (no secrets)  
- `.gitignore` — keys, local `config.json`, generated reports  

### Features

1. **Realtime** — metrics, dimensions, minute range, Markdown/JSON  
2. **Historical** — date range, limit/offset, Markdown/JSON  
3. **Metadata** — enumerate dimensions/metrics  
4. **Connection test** — metadata + small realtime pull  

### Security / privacy

- Never commit real `ga-credentials.json`.  
- Do not hard-code chat webhooks or signing secrets; use environment variables.  
- Treat exported reports like production analytics: may include IPs or campaign detail — avoid publishing raw exports.  

### Quotas (high level)

- Property-level daily request caps apply; check current Google documentation.  
- Per-request dimension/metric counts are capped (typically 9 dimensions / 10 metrics).  
- Expect some **processing latency** for recent dates (often 24–48h for full fat-finger accuracy on some fields).  

## 3. Optional next steps

- Caching for repeat pulls  
- Funnel / pivot where product allows  
- Chart generation layer  
- Stronger redaction for shared reports  

## 4. References

- [Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)  
- [Python client](https://github.com/googleapis/google-analytics-data-python)  
- [Schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)  
- [Authorization](https://developers.google.com/analytics/devguides/reporting/data/v1/authorization)  
