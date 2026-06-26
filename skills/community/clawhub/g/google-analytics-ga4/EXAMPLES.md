# Google Analytics skill — examples

How to run the skill from OpenClaw or any shell.

## Prerequisites

1. `pip install google-analytics-data`  
2. Service account JSON configured (see [SKILL.md](SKILL.md))  
3. Numeric GA4 property ID  

## Invoking from OpenClaw

### Option A — `ga_query.py`

```bash
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id YOUR-PROPERTY-ID

python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id YOUR-PROPERTY-ID \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions,eventCount \
  --dimensions country,deviceCategory
```

### Option B — `openclaw_ga.py`

```bash
python skills/google-analytics/openclaw_ga.py realtime \
  --property-id YOUR-PROPERTY-ID

python skills/google-analytics/openclaw_ga.py historical \
  --property-id YOUR-PROPERTY-ID \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions
```

## Scenarios

### Site overview (yesterday)

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date yesterday \
  --end-date yesterday \
  --metrics activeUsers,sessions,eventCount,screenPageViews,engagementRate
```

**Sample output:**

```
### 📈 Historical (yesterday to yesterday)

**Totals:**
- activeUsers: 1234
- sessions: 2345
...

| activeUsers | sessions | eventCount | screenPageViews | engagementRate |
|-------------|----------|------------|-----------------|----------------|
| 1234        | 2345     | 12345      | 5678            | 0.65           |

*1 rows total*
```

### By country (7 days)

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions \
  --dimensions country \
  --limit 20
```

### Device category

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 30daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions,engagementRate \
  --dimensions deviceCategory
```

### Realtime active users

```bash
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id 123456789 \
  --metrics activeUsers
```

### Realtime by country

```bash
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id 123456789 \
  --metrics activeUsers \
  --dimensions country
```

### Daily trend

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 30daysAgo \
  --end-date yesterday \
  --metrics activeUsers \
  --dimensions date
```

### Source / medium

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics sessions,conversions,totalRevenue \
  --dimensions source,medium
```

### Top pages

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics screenPageViews \
  --dimensions pagePath \
  --limit 20
```

### Events

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics eventCount \
  --dimensions eventName \
  --limit 30
```

## Advanced

### Pagination

```bash
python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 90daysAgo \
  --end-date yesterday \
  --metrics activeUsers \
  --dimensions date \
  --limit 100 \
  --offset 0

python skills/google-analytics/ga_query.py \
  --action historical \
  --property-id 123456789 \
  --start-date 90daysAgo \
  --end-date yesterday \
  --metrics activeUsers \
  --dimensions date \
  --limit 100 \
  --offset 100
```

### JSON output

```bash
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id 123456789 \
  --output json
```

### `GOOGLE_APPLICATION_CREDENTIALS`

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id 123456789
```

## Troubleshooting

### Verbose errors

```bash
export DEBUG=1
python skills/google-analytics/ga_query.py \
  --action realtime \
  --property-id 123456789
```

### Smoke test

```bash
python skills/google-analytics/ga_query.py \
  --action metadata \
  --property-id 123456789
```

## Tips

1. Property ID is numeric only (e.g. `123456789`).  
2. Dates: `YYYY-MM-DD` or relative (`7daysAgo`, `yesterday`).  
3. Up to **10 metrics** and **9 dimensions** per request (API limits).  
4. Large exports may require paging with `--limit` / `--offset`.  
5. Realtime covers roughly the last **30 minutes** (60 for GA360).  
