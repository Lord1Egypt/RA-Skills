# Data Source Adapter

## Purpose
Interface specification for connecting external market data sources to the Marketing OS.

---

## Interface Contract

### Adapter Name
`data-source`

### Supported Operations

| Operation | Method | Description |
|---|---|---|
| `fetch_search_trends` | GET | Retrieve search trend data for specified keywords |
| `fetch_competitor_data` | GET | Retrieve competitor activity and positioning data |
| `fetch_audience_signals` | GET | Retrieve audience behavior and sentiment data |
| `fetch_industry_reports` | GET | Retrieve industry report summaries |
| `fetch_social_listening` | GET | Retrieve social media mentions and sentiment |
| `fetch_channel_metrics` | GET | Retrieve performance metrics from marketing channels |

---

### Input Schema (Request)

```json
{
  "operation": "string — one of the supported operations",
  "parameters": {
    "keywords": ["string — search terms"],
    "date_range": {
      "start": "ISO 8601",
      "end": "ISO 8601"
    },
    "market": "string — geographic market (e.g., 'US', 'EU', 'APAC')",
    "competitors": ["string — competitor names"],
    "channels": ["string — channels to query"],
    "limit": "number — max results",
    "format": "json | csv"
  },
  "auth": {
    "method": "api_key | oauth2 | bearer",
    "credentials_ref": "string — reference to secure credential store"
  }
}
```

### Output Schema (Response)

```json
{
  "adapter": "data-source",
  "operation": "string",
  "timestamp": "ISO 8601",
  "status": "success | partial | error",
  "data": {
    "results": ["array of data objects — schema varies by operation"],
    "total_results": "number",
    "page": "number",
    "has_more": "boolean"
  },
  "metadata": {
    "source": "string — data provider name",
    "freshness": "string — how recent the data is",
    "reliability_score": "number (0-100)",
    "rate_limit_remaining": "number"
  },
  "error": {
    "code": "string",
    "message": "string",
    "retryable": "boolean"
  }
}
```

---

## Potential Data Sources

| Source | Type | Use Case |
|---|---|---|
| Google Trends API | Search trends | Market demand signals |
| SimilarWeb / SEMrush | Competitor data | Competitive intelligence |
| Social media APIs | Social listening | Audience sentiment |
| Industry databases | Reports | Market sizing |
| Google Analytics | Web metrics | Channel performance |
| Stripe / Payment APIs | Revenue data | Financial metrics |

---

## Integration Steps

1. Implement the adapter interface in your preferred language
2. Register the adapter in `configs/system.config.json` under `adapters.data_source`
3. Set `enabled: true` and provide the endpoint URL
4. Configure authentication method and credentials
5. Test with a `fetch_search_trends` call
6. The Virtual CMO will automatically use this adapter during Market Discovery workflow

---

## Error Handling

- **Rate limited**: Retry with exponential backoff, max 3 attempts
- **Auth failure**: Log error, halt data collection from this source, notify human
- **Partial data**: Accept partial results, flag `reliability_score` accordingly
- **Timeout**: Default 30s timeout, configurable in system.config.json
