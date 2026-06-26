# Database connections schema

This specification defines a JSON-based schema for managing a heterogeneous
registry of data sources. It supports traditional networked databases, local
flat files, and cloud-hosted objects (S3) with support for shared credential
profiles and globbing patterns.

---

## 1. Structural Overview

The schema is composed of three top-level objects:

1. **`credentials`**: A map of authentication profiles used by cloud providers.
2. **`databases`**: A map of data source configurations where the key is a
   unique identifier.
3. **`semantic_context`**: (Optional) Configuration for semantic context
   enrichment.

---

## 2. Field Definitions

### 2.1 The `credentials` Object

Stores shared authentication metadata to prevent redundancy across multiple
sources.

| Field            | Type   | Description                                                 |
| ---------------- | ------ | ----------------------------------------------------------- |
| `access_key_env` | String | Name of the environment variable for the Access Key ID.     |
| `secret_key_env` | String | Name of the environment variable for the Secret Access Key. |
| `key_file`       | String | Path to a Google service account JSON key file.             |

Each credential entry must contain **either** S3 fields (`access_key_env` +
`secret_key_env`) **or** the gsheet field (`key_file`), not both.

### 2.2 The `databases` Object

Each entry in this map contains common metadata and type-specific connection
details. **Keys must consist of lowercase letters (`a`–`z`), digits (`0`–`9`),
and underscores (`_`) only.**

#### A. Common Fields (All Types)

- **`metadata`**: Object containing `name` (String) and `description` (String).
- **`type`**: String. One of: `postgresql`, `mysql`, `file`, `sqlite`, `duckdb`,
  `s3`, or `gsheet`.

#### B. Networked Database Fields (`type: "postgresql" | "mysql" | etc.`)

- **`host`**: Server address.
- **`port`**: Network port (Integer).
- **`database_name`**: The target schema/database name.
- **`username`**: Login identity.
- **`password_env_var`**: Name of the env var holding the secret.

#### C. SQLite Database Fields (`type: "sqlite"`)

- **`path`**: Path to the SQLite database file (`.sqlite`, `.db`, etc.).

#### D. DuckDB Database Fields (`type: "duckdb"`)

- **`path`**: Path to the DuckDB database file (`.duckdb`, `.db`, etc.).

#### E. Local File Fields (`type: "file"`)

- **`path`**: Unix-style path to the file.
- **`format`**: (Optional if inferred from extension) `csv`, `xlsx`, `parquet`,
  `json`.
- **`delimiter`**: (CSV only) The separator character.
- **`header_row`**: (CSV/XLSX) Boolean; indicates if row 1 is the header.
- **`sheet_name`**: (XLSX only) The tab to read.

#### F. S3 Cloud Storage Fields (`type: "s3"`)

- **`uri`**: S3 URI (e.g., `s3://bucket/path/`). Supports globbing patterns
  (`*`, `?`, `[]`).
- **`credential_profile`**: Key matching an entry in the top-level `credentials`
  map.
- **`region`**: AWS region (e.g., `us-east-1`).
- **`format`**: **Required.** The file format (`csv`, `parquet`, etc.).
- **`delimiter` / `header_row` / `sheet_name`**: Same as Local File fields.

#### G. Google Sheets Fields (`type: "gsheet"`)

- **`spreadsheet_id`**: The Google Sheets spreadsheet ID (from the sheet URL).
- **`credential_profile`**: (Optional) Key matching an entry in the top-level
  `credentials` map (must reference a credential with `key_file`). If omitted,
  browser-based OAuth is used (interactive Google login flow).
- **`sheet_name`**: (Optional) The tab/sheet name. If omitted, the table name
  from the SQL query is used as the sheet name.
- **`header_row`**: (Optional) Boolean; indicates if row 1 is the header.
  Defaults to true if omitted.

### 2.3 The `semantic_context` Object

Provides static enrichment layers on top of the auto-scanned semantic context.
This is equivalent to supplying `--semantic-context-overlay` on the CLI, but
embedded in the config file.

| Field      | Type             | Description                                                                                                                                                                  |
| ---------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `overlays` | Array of Strings | Ordered list of paths to [Open Semantic Interchange (OSI)](https://github.com/open-semantic-interchange/OSI) YAML files. Applied after auto-scan semantic context, in order. |

Overlays specified here are applied before any `--semantic-context-overlay`
flags supplied on the CLI.

---

## 3. Reference Implementation

```json
{
  "credentials": {
    "aws_marketing_user": {
      "access_key_env": "AWS_ACCESS_KEY_ID",
      "secret_key_env": "AWS_SECRET_ACCESS_KEY"
    },
    "gsheet_service_account": {
      "key_file": "/etc/secrets/gsheet-sa-key.json"
    }
  },
  "databases": {
    "db_prod_analytics": {
      "metadata": {
        "name": "Production Analytics",
        "description": "Primary read-replica for data warehousing."
      },
      "type": "postgresql",
      "host": "db-prod-01.example.com",
      "port": 5432,
      "database_name": "analytics_main",
      "username": "bi_user",
      "password_env_var": "DB_PROD_PASSWORD"
    },
    "app_sqlite": {
      "metadata": {
        "name": "Application Database",
        "description": "SQLite database backing the mobile app."
      },
      "type": "sqlite",
      "path": "/data/app.sqlite"
    },
    "analytics_duckdb": {
      "metadata": {
        "name": "Analytics Database",
        "description": "DuckDB analytics database with pre-aggregated metrics."
      },
      "type": "duckdb",
      "path": "/data/analytics.duckdb"
    },
    "local_budget_report": {
      "metadata": {
        "name": "FY2026 Budget Plan",
        "description": "Local Excel workbook for department budget allocations."
      },
      "type": "file",
      "path": "/Users/sarah/Documents/Finance/budget_2026.xlsx",
      "sheet_name": "Final_Approval",
      "header_row": true
    },
    "s3_sensor_data_glob": {
      "metadata": {
        "name": "IoT Sensor Data",
        "description": "Partitioned sensor data using glob patterns."
      },
      "type": "s3",
      "credential_profile": "aws_marketing_user",
      "uri": "s3://iot-bucket/2026/*/device_id_100?/sensor_*.parquet",
      "format": "parquet",
      "region": "us-west-2"
    },
    "inventory_snapshot": {
      "metadata": {
        "name": "Warehouse Inventory",
        "description": "Global inventory levels exported as CSV to S3."
      },
      "type": "s3",
      "credential_profile": "aws_marketing_user",
      "uri": "s3://corporate-reports/inventory/daily_snapshot.csv",
      "format": "csv",
      "delimiter": ",",
      "header_row": true,
      "region": "us-east-1"
    },
    "gsheet_sales_forecast": {
      "metadata": {
        "name": "Sales Forecast",
        "description": "Q3 sales forecast shared via Google Sheets."
      },
      "type": "gsheet",
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
      "credential_profile": "gsheet_service_account",
      "sheet_name": "Forecast",
      "header_row": true
    },
    "gsheet_personal": {
      "metadata": {
        "name": "Personal Tracker",
        "description": "Ad-hoc personal sheet accessed via browser OAuth."
      },
      "type": "gsheet",
      "spreadsheet_id": "1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789abcdefg"
    }
  },
  "semantic_context": {
    "overlays": [
      "/path/to/business_glossary.yaml",
      "/path/to/column_descriptions.yaml"
    ]
  }
}
```
