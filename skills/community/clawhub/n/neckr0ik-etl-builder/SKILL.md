---
name: neckr0ik-etl-builder
version: 1.0.0
description: Build data pipelines for ETL (Extract, Transform, Load). Connect databases, APIs, files, and cloud storage. Transform and sync data automatically. Use when you need to move and transform data between systems.
---

# Data Pipeline Builder

Build ETL pipelines without code.

## What This Does

- **Extract** — Pull data from databases, APIs, files, cloud storage
- **Transform** — Clean, filter, aggregate, join, enrich
- **Load** — Push to databases, APIs, files, cloud storage
- **Schedule** — Run pipelines on cron schedules
- **Monitor** — Track pipeline health and performance

## Quick Start

```bash
# Create a pipeline
neckr0ik-etl-builder create --name "sync-users" --source postgres --destination sheets

# Add transformations
neckr0ik-etl-builder transform --pipeline sync-users --type filter --field "active" --value true

# Run pipeline
neckr0ik-etl-builder run --name sync-users

# Schedule pipeline
neckr0ik-etl-builder schedule --name sync-users --cron "0 * * * *"
```

## Supported Sources

| Source | Type | Auth |
|--------|------|------|
| PostgreSQL | Database | Connection string |
| MySQL | Database | Connection string |
| MongoDB | Database | Connection string |
| SQLite | Database | File path |
| Google Sheets | Cloud | OAuth / API Key |
| Airtable | Cloud | API Key |
| Notion | Cloud | API Key |
| REST API | API | Bearer / API Key |
| GraphQL | API | Bearer / API Key |
| CSV | File | File path |
| JSON | File | File path |
| S3 | Cloud | Access Key |
| GCS | Cloud | Service Account |

## Supported Destinations

Same as sources, plus:
- Webhooks
- Email
- Slack
- Discord

## Commands

### create

Create a new pipeline.

```bash
neckr0ik-etl-builder create --name <name> [options]

Options:
  --source <type>      Source type (postgres, mysql, api, csv...)
  --destination <type> Destination type
  --config <file>      Configuration file
```

### extract

Configure extraction step.

```bash
neckr0ik-etl-builder extract --pipeline <name> [options]

Options:
  --table <name>       Table to extract (for databases)
  --query <sql>        Custom query
  --endpoint <url>     API endpoint
  --file <path>        File path
```

### transform

Add transformation step.

```bash
neckr0ik-etl-builder transform --pipeline <name> [options]

Transform Types:
  filter       Filter rows by condition
  map          Map field values
  aggregate    Aggregate data (sum, count, avg...)
  join         Join with another source
  enrich       Enrich with external data
  clean        Clean nulls, trim strings
  validate     Validate data quality
```

### load

Configure load step.

```bash
neckr0ik-etl-builder load --pipeline <name> [options]

Options:
  --mode <mode>        Load mode (append, replace, upsert)
  --table <name>       Target table
  --mapping <file>     Field mapping
```

### run

Execute pipeline.

```bash
neckr0ik-etl-builder run --name <name> [options]

Options:
  --dry-run            Preview without executing
  --limit <n>          Process only N records
  --parallel           Run stages in parallel
```

### schedule

Schedule pipeline.

```bash
neckr0ik-etl-builder schedule --name <name> --cron "<expression>"
```

### status

Check pipeline status.

```bash
neckr0ik-etl-builder status --name <name>
```

## Example Pipelines

### 1. Sync PostgreSQL to Google Sheets

```bash
# Create pipeline
neckr0ik-etl-builder create --name user-sync --source postgres --destination sheets

# Configure extraction
neckr0ik-etl-builder extract --pipeline user-sync \
  --query "SELECT * FROM users WHERE updated_at > NOW() - INTERVAL '1 day'"

# Add transforms
neckr0ik-etl-builder transform --pipeline user-sync --type clean
neckr0ik-etl-builder transform --pipeline user-sync --type filter --field active --value true

# Schedule hourly
neckr0ik-etl-builder schedule --name user-sync --cron "0 * * * *"
```

### 2. API to Database

```bash
# Create pipeline
neckr0ik-etl-builder create --name api-sync --source api --destination postgres

# Configure extraction
neckr0ik-etl-builder extract --pipeline api-sync \
  --endpoint "https://api.example.com/users" \
  --auth bearer \
  --token "$API_TOKEN"

# Transform
neckr0ik-etl-builder transform --pipeline api-sync --type map --field "id" --to "user_id"
neckr0ik-etl-builder transform --pipeline api-sync --type clean

# Load
neckr0ik-etl-builder load --pipeline api-sync --table api_users --mode upsert
```

### 3. CSV to Airtable

```bash
# Create pipeline
neckr0ik-etl-builder create --name csv-import --source csv --destination airtable

# Configure
neckr0ik-etl-builder extract --pipeline csv-import --file ./data.csv
neckr0ik-etl-builder transform --pipeline csv-import --type clean
neckr0ik-etl-builder load --pipeline csv-import --table "Imports" --mapping ./mapping.json
```

## Pipeline Configuration

Pipelines are stored as JSON:

```json
{
  "name": "user-sync",
  "source": {
    "type": "postgres",
    "connection": "postgresql://...",
    "query": "SELECT * FROM users"
  },
  "transformations": [
    {"type": "filter", "field": "active", "value": true},
    {"type": "clean"},
    {"type": "map", "from": "id", "to": "user_id"}
  ],
  "destination": {
    "type": "google_sheets",
    "spreadsheet_id": "...",
    "range": "Sheet1!A1"
  },
  "schedule": "0 * * * *"
}
```

## Monitoring

```bash
# View pipeline history
neckr0ik-etl-builder history --name user-sync --limit 10

# View failed runs
neckr0ik-etl-builder failures --name user-sync

# Export logs
neckr0ik-etl-builder logs --name user-sync --output ./logs.json
```

## See Also

- `references/connectors.md` — Source/destination connectors
- `references/transforms.md` — Transformation functions
- `scripts/pipeline.py` — Main implementation