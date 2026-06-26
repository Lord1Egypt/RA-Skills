---
name: moltsheet
description: >-
  Use the Moltsheet CLI to manage spreadsheet-style data for AI workflows: create sheets, inspect schemas, import rows, update cells, share sheets, and run read-only SQL queries over accessible sheets. Use when Codex needs Moltsheet data access, filtered reads, selected columns, joins, aggregates, or spreadsheet mutations. Prefer the CLI over raw HTTP, authenticate once, use `--json`, and use files or stdin for structured payloads.
version: 1.0.8
---

# Moltsheet

Moltsheet is a spreadsheet API for AI agents with a CLI designed to be easier and safer for agents than handwritten HTTP requests.

If you need to create sheets, inspect data, query filtered data, import rows, update cells, or share sheets with another agent, use the CLI first.

## Default Agent Procedure

When handling Moltsheet as an agent, follow this order:

1. Confirm the CLI is available: `moltsheet --version`
2. If it is not installed, use `npx moltsheet@latest ...` or install it globally
3. Authenticate once with `moltsheet auth login`
4. Confirm your agent identity with `moltsheet whoami --json`
5. Prefer `--json` whenever another tool, script, or agent will read the output
6. Use `sql tables` before SQL queries, so you know the accessible table and column names
7. Use `sheet list` and `sheet get` before writing, so you understand the target schema
8. Use stdin or JSON files for structured inputs instead of hand-escaped inline JSON
9. Use raw HTTP only if the CLI cannot be run

## Install

Preferred global install:

```bash
npm install -g moltsheet
```

One-off usage without installing:

```bash
npx moltsheet@latest auth status
```

If you are working inside the Moltsheet repository itself, you can also run the local build:

```bash
npm --prefix cli install
npm run build:cli
npm run cli -- auth status
```

## Authentication

Authenticate once:

```bash
moltsheet auth login
```

Or pass the API key directly:

```bash
moltsheet auth login --api-key YOUR_API_KEY
```

Check current auth state:

```bash
moltsheet auth status --json
```

Show the current agent identity without exposing the API key:

```bash
moltsheet whoami --json
```

Clear stored auth:

```bash
moltsheet auth logout
```

Credential resolution order:

1. `--api-key`
2. `MOLTSHEET_API_KEY`
3. Stored local credential from `auth login`

Storage behavior:

- Preferred: OS credential storage through `keytar`
- Windows: Credential Manager
- macOS: Keychain
- Linux: Secret Service or libsecret
- Fallback: local config file if secure storage is unavailable

The CLI targets the production Moltsheet service by default:

```bash
https://www.moltsheet.com
```

## Commands Agents Should Reach For First

Register an agent:

```bash
moltsheet agent register --display-name "Research Bot" --slug research.bot --json
```

Identify the authenticated agent:

```bash
moltsheet whoami --json
```

List sheets:

```bash
moltsheet sheet list --json
```

Inspect one sheet:

```bash
moltsheet sheet get SHEET_ID --json
```

Read a filtered subset of a sheet:

```bash
moltsheet sheet get SHEET_ID --columns "Company,Qualified" --filter "Qualified:eq:true" --json
```

List SQL table names for accessible sheets:

```bash
moltsheet sql tables --json
```

Run a read-only SQL query against those sheet-like tables:

```bash
moltsheet sql query --query "select company, website from leads where qualified = true limit 10" --json
```

Read SQL from a file:

```bash
moltsheet sql query --file query.sql --json
```

Read SQL from stdin with a lower result cap:

```bash
cat query.sql | moltsheet sql query --stdin --limit 500 --json
```

## SQL Query Workflow

Use SQL when you need filtered rows, selected columns, joins, grouping, counts, sorting, or other read-only analysis without downloading full sheet rows.

1. Run `moltsheet sql tables --json`.
2. Pick a table name from `sqlName` or `sqlNames`.
3. Use the listed `sqlName` values for columns, not display names with spaces.
4. Select only the columns needed.
5. Add `where`, `order by`, and `limit` clauses when possible.
6. Keep SQL read-only.

Moltsheet exposes each accessible sheet as a logical SQL table. Every table includes:

- `__row_id`: the Moltsheet row UUID
- `__row_order`: the sheet row order
- Sheet columns using sanitized SQL identifiers

Example filtered projection:

```bash
moltsheet sql query --query "select company, ceo_name from sidewalk_robotics_companies_top_50 where company ilike '%robot%' order by __row_order limit 10" --json
```

Example aggregate:

```bash
moltsheet sql query --query "select commented, count(*)::int as total from linkedin_posts_20260223_023644 group by commented" --json
```

Example join across accessible sheets:

```bash
moltsheet sql query --query "select a.company, b.post_url from sidewalk_robotics_companies_top_50 a cross join linkedin_posts_20260223_023644 b limit 5" --json
```

SQL safety model:

- Queries can only reference sheets the current API key owns or can read as a collaborator.
- SQL is read-only `SELECT` only.
- Raw base tables such as `agents`, `sheets`, `rows`, `cells`, `columns`, and `collaborators` are not available.
- DML, DDL, multiple statements, schema-qualified table names, unsafe functions, unknown tables, and CTE shadowing are rejected.
- Results are capped by the server; use `--limit` to request a smaller cap.
- `read` and `write` collaborators can query shared sheets, but SQL never grants write access.

Update a sheet:

```bash
moltsheet sheet update SHEET_ID --name "Leads v2" --json
```

Update a schema and allow destructive changes:

```bash
cat schema.json | moltsheet sheet update SHEET_ID --schema-stdin --confirm-data-loss --json
```

Delete a sheet:

```bash
moltsheet sheet delete SHEET_ID --json
```

Create a sheet from schema stdin:

```bash
cat schema.json | moltsheet sheet create "Leads" --schema-stdin --json
```

Create empty rows:

```bash
moltsheet row add SHEET_ID --count 10 --json
```

Add one row from stdin:

```bash
cat row.json | moltsheet row add SHEET_ID --data-stdin --json
```

Import multiple rows:

```bash
cat rows.json | moltsheet row import SHEET_ID --stdin --json
```

Import multiple JSON rows through the dedicated sheet import route:

```bash
cat rows.json | moltsheet sheet import SHEET_ID --stdin --json
```

Import a CSV file into an existing sheet:

```bash
moltsheet sheet import SHEET_ID --csv-file data.csv --json
```

Import CSV from stdin:

```bash
cat data.csv | moltsheet sheet import SHEET_ID --csv-stdin --json
```

Large JSON and CSV imports are batched automatically by the CLI. Use `--batch-size` only when you need smaller server requests:

```bash
moltsheet sheet import SHEET_ID --csv-file data.csv --batch-size 500 --json
```

CSV import rules:

- The target sheet must already exist
- The first CSV row must contain column headers
- CSV headers must exactly match existing sheet column names
- Unknown CSV headers fail before rows are imported
- Missing sheet columns are imported as empty values
- Do not convert large CSV files into one huge JSON payload; use `--csv-file` or `--csv-stdin`

List rows:

```bash
moltsheet row list SHEET_ID --json
```

Delete rows by ID:

```bash
cat row-ids.json | moltsheet row delete SHEET_ID --stdin --json
```

Delete one row by index:

```bash
moltsheet row delete-index SHEET_ID 0 --json
```

Update cells:

```bash
cat updates.json | moltsheet cell update SHEET_ID --stdin --json
```

Add columns:

```bash
cat columns.json | moltsheet column add SHEET_ID --stdin --json
```

Delete columns by index list:

```bash
cat indices.json | moltsheet column delete SHEET_ID --stdin --json
```

Delete one column by index:

```bash
moltsheet column delete-index SHEET_ID 1 --json
```

Rename a column:

```bash
moltsheet column rename SHEET_ID 0 --name "Company Name" --json
```

Share a sheet:

```bash
moltsheet share add SHEET_ID --slug analyst.bot --access write --json
```

List collaborators:

```bash
moltsheet share list SHEET_ID --json
```

Remove a collaborator:

```bash
moltsheet share remove SHEET_ID --slug analyst.bot --json
```

## Structured Input Patterns

Prefer files or stdin for anything shaped like JSON.

Sheet schema example:

```json
[
  { "name": "Company", "type": "string" },
  { "name": "Website", "type": "url" },
  { "name": "Qualified", "type": "boolean" }
]
```

Single row example:

```json
{
  "Company": "Moltsheet",
  "Website": "https://www.moltsheet.com",
  "Qualified": true
}
```

Multiple rows example:

```json
[
  {
    "Company": "Moltsheet",
    "Website": "https://www.moltsheet.com",
    "Qualified": true
  },
  {
    "Company": "Example",
    "Website": "https://example.com",
    "Qualified": false
  }
]
```

Column definitions example:

```json
[
  { "name": "Company", "type": "string" },
  { "name": "Website", "type": "url" }
]
```

Row ID list example:

```json
[
  "123e4567-e89b-12d3-a456-426614174000",
  "123e4567-e89b-12d3-a456-426614174001"
]
```

Column index list example:

```json
[
  0,
  2
]
```

Cell updates example:

```json
[
  {
    "rowId": "123e4567-e89b-12d3-a456-426614174000",
    "column": "Qualified",
    "value": true
  }
]
```

## How Agents Should Handle the CLI

Use this operating style:

- Prefer `--json` for machine-readable output
- Read before writing: use `sheet list` or `sheet get` before mutating data
- Trust schema types and let the CLI or API validation guide corrections
- Prefer stdin or files over complex shell escaping
- Reuse stored auth rather than passing secrets repeatedly
- Use collaborator slugs for sharing, never API keys
- Use `sheet import` for the dedicated sheet import route and `row import` for rows-endpoint bulk insert behavior
- Use `sheet import --csv-file` or `--csv-stdin` for CSV files instead of converting large CSVs to JSON
- Let the CLI batch large CSV and JSON imports automatically; lower `--batch-size` if the server asks for smaller batches
- Use `sql query` for filtered/projection reads so you avoid fetching full rows when only selected columns or matching rows are needed
- If a command fails, inspect the error payload before retrying

Recommended write workflow:

1. Run `moltsheet auth status --json`
2. Run `moltsheet whoami --json`
3. Run `moltsheet sheet list --json`
4. Run `moltsheet sheet get SHEET_ID --json`
5. Confirm column names and expected types
6. Prepare JSON input
7. Run the write command with `--json`
8. Re-run `sheet get` or `sheet list` to verify the result

## Output and Validation

Supported schema types:

- `string`
- `number`
- `boolean`
- `date`
- `url`

Validation behavior:

- Empty values are allowed
- Invalid types return an error
- Bulk row imports reject the full request if any row is invalid
- Cell updates require valid `rowId` values and valid column names

Important note:

- Returned row values are stored and returned as strings, even when validated against number, boolean, date, or url schema types

## Agentic Import Error Handling

Import errors are designed to tell an agent what to do next. In `--json` mode, inspect:

- `error.code` - stable machine-readable failure code
- `error.message` - what failed
- `error.action` - the adjustment to make before retrying
- `error.retryable` - whether retrying without changing input may help
- `error.batch` and `error.rowRange` - which batch or source rows failed
- `error.column` - the relevant column when validation fails

Common adjustments:

- `unknown_csv_headers`: rename CSV headers to match sheet columns exactly, or update the sheet schema first
- `type_validation_failed`: fix the listed row and column value to match the sheet type
- `batch_too_large` or server payload errors: rerun with a smaller `--batch-size`
- `schema_lookup_failed`: verify authentication, sheet ID, and access before retrying

After correcting schema or data issues, rerun the same source import command. Previously successful batches remain committed; the failed batch writes zero rows.

## Collaboration Model

- Sheets are shared by agent slug
- Access levels are `read` and `write`
- API keys are never exposed through collaboration commands
- Collaboration responses expose only `slug` and `displayName`

## Troubleshooting

If `moltsheet` is not installed:

```bash
npx moltsheet@latest sheet list --json
```

If you suspect auth problems:

```bash
moltsheet auth status --json
moltsheet whoami --json
```

If you need to bypass stored auth for one call:

```bash
moltsheet sheet list --api-key YOUR_API_KEY --json
```

If you are working inside the repo and the published CLI is unavailable:

```bash
npm run cli -- sheet list --json
```

## HTTP Fallback

Use raw HTTP only if you cannot run the CLI.

Base URL:

```bash
https://www.moltsheet.com/api/v1
```

Example list sheets request:

```bash
curl https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Example create sheet request:

```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Leads",
    "description": "Outbound leads",
    "schema": [
      { "name": "Company", "type": "string" },
      { "name": "Website", "type": "url" }
    ]
  }'
```

Example SQL tables request:

```bash
curl https://www.moltsheet.com/api/v1/sql/tables \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Example SQL query request:

```bash
curl -X POST https://www.moltsheet.com/api/v1/sql/query \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "select company, website from leads where qualified = true limit 10",
    "limit": 100
  }'
```

## Short Rules For Agents

- Prefer the CLI over `curl`
- Prefer `--json`
- Prefer files or stdin for structured payloads
- Read the sheet schema before writing
- Use SQL for read-only filtered data retrieval, selected columns, joins, and aggregates
- Verify writes by reading the sheet again
- Use `npx moltsheet@latest` when the binary is not installed
