# Google Analytics OpenClaw skill

Call the Google Analytics **Data API v1** from the command line to read **GA4** data (not Universal Analytics).

## Quick start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Credentials

Follow [SKILL.md](SKILL.md) to create a service account, download JSON, and grant the account **Viewer** on your GA4 property.

### 3. Run a query

```bash
# Realtime active users
python ga_query.py --action realtime --property-id YOUR-PROPERTY-ID

# Historical
python ga_query.py --action historical \
  --property-id YOUR-PROPERTY-ID \
  --start-date 7daysAgo \
  --end-date yesterday \
  --metrics activeUsers,sessions \
  --dimensions country
```

## Layout

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Full setup and reference |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet |
| [EXAMPLES.md](EXAMPLES.md) | Example queries |
| `ga_query.py` | Main CLI |
| `openclaw_ga.py` | Thin wrapper for OpenClaw-style invocation |
| `test_connection.py` | Validate credentials and API access |
| `traffic_source_report.py` | Optional period-over-period source report (needs `config.json` or env) |
| `ga-credentials.json` | **Local only** — create from GCP (not in git) |

## Output

Markdown tables by default; add `--output json` for JSON.

## Troubleshooting

### Missing credentials

```
Error: Your default credentials were not found.
```

1. Add `ga-credentials.json` beside the scripts, or  
2. `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

### Permission errors

Add the service account email under **Property access management** with at least **Viewer**.

### API disabled

In Google Cloud: **APIs & Services** → **Library** → enable **Google Analytics Data API**.

## References

- [SKILL.md](SKILL.md)  
- [GA4 Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)  
- [Schema (dimensions/metrics)](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)  
