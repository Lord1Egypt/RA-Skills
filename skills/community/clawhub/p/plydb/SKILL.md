---
name: plydb
description:
  Skill for using the PlyDB CLI to perform SQL analysis of connected data
  sources. Use for SQL queries across heterogeneous databases and files such as
  Postgres, MySQL, CSV, Parquet, JSON, Excel, SQLite, DuckDB, Google Sheets.
  Triggers on "plydb", "sql", "query", "data analysis", "parquet", "csv",
  "excel", "database".
---

# PlyDB CLI skill

The `plydb` CLI can be used to query across heterogenous data sources.

## Dependencies

The `plydb` binary must be available on the system.

If it is not, installation instructions can be found
[here](https://github.com/kineticloom/plydb?tab=readme-ov-file#installation)

## Instructions

### Configure data sources

First, the data sources to make available to PlyDB must be configured in a
config file as per the specification in `references\config_schema.md`.

### Query with SQL

Once you have a data source config file, PlyDB can query across all of the
configured data sources. Use fully qualified table names: catalog.schema.table.

```sh
plydb query \
  --config path/to/config/file/config.json \
  "SELECT * FROM customers.default.customers c
   JOIN orders.default.orders o
   ON c.id = o.customer_id"
```

### Fetching semantic context of the data

To provide context to understand the domain and write correct SQL - PlyDB can
build and provide semantic context from database `COMMENT` metadata alongside
column types and foreign keys as structured YAML that follows the
[Open Semantic Interchange (OSI)](https://github.com/open-semantic-interchange/OSI)
specification.

```sh
plydb semantic-context --config path/to/config/file/config.json
```

#### Enriching auto-scanned context with overlays

When the database lacks comments or you need to add relationships and metrics
not captured from source metadata, use `--semantic-context-overlay` to supply
one or more OSI YAML files that are merged on top of the auto-scanned model:

```sh
plydb semantic-context \
  --config path/to/config/file/config.json \
  --semantic-context-overlay path/to/overlay.yaml
```

The flag is repeatable; overlays are applied in the order given:

```sh
plydb semantic-context \
  --config path/to/config/file/config.json \
  --semantic-context-overlay base_overlay.yaml \
  --semantic-context-overlay team_overlay.yaml
```

Overlay files must be valid
[Open Semantic Interchange (OSI)](https://github.com/open-semantic-interchange/OSI)
YAML.

Overlays can add descriptions to existing datasets and fields, define
relationships between existing datasets, and add or update metrics. They cannot
introduce new datasets or fields - only enrich what was already discovered by
the auto-scanner.

Good opportunities to create or edit an overlay file are when encountering a new
dataset or after a session of data analysis with the user. These are great
opportunities to distill your learnings about the data's semantics and record
them into an overlay file for future sessions. Ask the user first.

#### Embedding overlays in the config file

Overlays can also be specified in the config file under
`semantic_context.overlays` instead of (or in addition to) the CLI flag:

```json
{
  "databases": { ... },
  "semantic_context": {
    "overlays": [
      "path/to/base_overlay.yaml",
      "path/to/team_overlay.yaml"
    ]
  }
}
```

With overlays in the config, no extra flags are needed:

```sh
plydb semantic-context --config path/to/config.json
```

Config-file overlays are applied before any `--semantic-context-overlay` flags.

## Troubleshooting

- [gsheet data source with interactive OAuth](./references/troubleshooting.md#gsheet-data-source-with-interactive-oauth)
