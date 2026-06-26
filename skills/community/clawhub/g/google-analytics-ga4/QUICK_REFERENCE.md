# Google Analytics skill — quick reference

## Install

```bash
pip install google-analytics-data
```

## Configure

1. Create a service account in Google Cloud.  
2. Save the JSON key as `ga-credentials.json`.  
3. In GA4, grant that account access to the property.

## Common commands

### Realtime

```bash
python ga_query.py --action realtime --property-id YOUR-ID
```

### Historical

```bash
python ga_query.py --action historical \
  --property-id YOUR-ID \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions \
  --dimensions country
```

### Metadata

```bash
python ga_query.py --action metadata --property-id YOUR-ID
```

## Metrics (examples)

| API name | Meaning |
|----------|---------|
| `activeUsers` | Active users |
| `sessions` | Sessions |
| `eventCount` | Events |
| `screenPageViews` | Page views |
| `engagementRate` | Engagement rate |
| `conversions` | Conversions |
| `totalRevenue` | Revenue |

## Dimensions (examples)

| API name | Meaning |
|----------|---------|
| `country` | Country |
| `city` | City |
| `deviceCategory` | Device class |
| `date` | Date |
| `pagePath` | Path |
| `source` | Source |
| `medium` | Medium |
| `eventName` | Event |

## Dates

- `today`, `yesterday`, `7daysAgo`  
- Or `YYYY-MM-DD`

## Output

```bash
# Markdown (default)
python ga_query.py --action realtime --property-id YOUR-ID

# JSON
python ga_query.py --action realtime --property-id YOUR-ID --output json
```

## Debug

```bash
python test_connection.py --property-id YOUR-ID
```

## Docs

- [SKILL.md](SKILL.md)  
- [EXAMPLES.md](EXAMPLES.md)  
- [README.md](README.md)  
