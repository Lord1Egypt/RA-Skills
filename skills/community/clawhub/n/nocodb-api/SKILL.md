---
name: nocodb
description: Connect to NocoDB databases via REST API v3. Query records, manage database structure (tables, fields, views), handle linked records, filters, sorts, and attachments. Use when working with NocoDB (open-source Airtable alternative) to read or manipulate data, create or update records, manage database schema, or upload files.
license: AGPL-3.0
metadata:
  openclaw:
    requires:
      env:
        - NOCODB_TOKEN
        - NOCODB_URL
      bins:
        - curl
        - jq
    primaryEnv: NOCODB_TOKEN
---

# NocoDB Skill

CLI wrapper for NocoDB API v3. Supports both NocoDB Cloud (app.nocodb.com) and self-hosted instances.

NocoDB is an open-source Airtable alternative that turns any database into a smart spreadsheet. This skill provides complete access to NocoDB's REST API for managing workspaces, bases, tables, records, and more.

## Setup

### Required Environment Variables

```bash
export NOCODB_TOKEN="your-api-token"  # Required - API authentication token
export NOCODB_URL="https://app.nocodb.com"  # Optional - defaults to cloud
```

### Getting Your API Token

1. Open NocoDB dashboard
2. Go to **Team & Settings** → **API Tokens**
3. Click **Add New Token**
4. Copy the token and set it as `NOCODB_TOKEN`

### Verification

Test your connection:
```bash
nc workspace:list
```

## Quick Start

```bash
# List all workspaces
nc workspace:list

# List bases in a workspace
nc base:list <workspace-name-or-id>

# List tables in a base
nc table:list <base-name-or-id>

# Query records
nc record:list <base> <table>

# Create a record
nc record:create <base> <table> '{"fields":{"Name":"Alice"}}'
```

## Usage

The skill provides the `nc` command with a hierarchical structure:

```
WORKSPACE → BASE → TABLE → VIEW/FIELD → RECORD
```

### Identifier Formats

You can use **names** (human-readable) or **IDs** (faster performance):

| Resource | ID Prefix | Example |
|----------|-----------|---------|
| Workspace | `w` | `wabc123xyz` |
| Base | `p` | `pdef456uvw` |
| Table | `m` | `mghi789rst` |
| Field | `c` | `cjkl012opq` |
| View | `vw` | `vwmno345abc` |

**Tip:** Use IDs directly for better performance. Set `NOCODB_VERBOSE=1` to see ID resolution in action.

## Commands

### Workspaces

**Note:** Workspace APIs require Enterprise plan (self-hosted or cloud-hosted).

```bash
nc workspace:list
nc workspace:get <workspace>
nc workspace:create '{"title":"New Workspace"}'
nc workspace:update <workspace> '{"title":"Renamed"}'
nc workspace:delete <workspace>
```

**Workspace Collaboration (Enterprise):**
```bash
nc workspace:members <workspace>
nc workspace:members:add <workspace> '{"email":"user@example.com","roles":"workspace-creator"}'
nc workspace:members:update <workspace> '{"email":"user@example.com","roles":"workspace-viewer"}'
nc workspace:members:remove <workspace> '{"email":"user@example.com"}'
```

### Bases

```bash
nc base:list <workspace>
nc base:get <base>
nc base:create <workspace> '{"title":"New Base"}'
nc base:update <base> '{"title":"Renamed"}'
nc base:delete <base>
```

**Base Collaboration (Enterprise):**
```bash
nc base:members <base>
nc base:members:add <base> '{"email":"user@example.com","roles":"base-editor"}'
nc base:members:update <base> '{"email":"user@example.com","roles":"base-viewer"}'
nc base:members:remove <base> '{"email":"user@example.com"}'
```

### Tables

```bash
nc table:list <base>
nc table:get <base> <table>
nc table:create <base> '{"title":"New Table"}'
nc table:update <base> <table> '{"title":"Renamed"}'
nc table:delete <base> <table>
```

### Fields

```bash
nc field:list <base> <table>
nc field:get <base> <table> <field>
nc field:create <base> <table> '{"title":"Email","type":"Email"}'
nc field:update <base> <table> <field> '{"title":"Contact Email"}'
nc field:delete <base> <table> <field>
```

**Field Types:**
- `SingleLineText`, `LongText`, `Number`, `Decimal`, `Currency`, `Percent`
- `Email`, `URL`, `PhoneNumber`
- `Date`, `DateTime`, `Time`
- `SingleSelect`, `MultiSelect`
- `Checkbox`, `Rating`
- `Attachment`, `Links`, `User`, `JSON`

### Views

**Note:** View APIs require Enterprise plan.

```bash
nc view:list <base> <table>
nc view:get <base> <table> <view>
nc view:create <base> <table> '{"title":"Active Users","type":"grid"}'
nc view:update <base> <table> <view> '{"title":"Renamed"}'
nc view:delete <base> <table> <view>
```

**View Types:** `grid`, `gallery`, `kanban`, `calendar`, `form`

### Records

```bash
# List records (pagination)
nc record:list <base> <table> [page] [pageSize] [where] [sort] [fields] [viewId]

# Get single record
nc record:get <base> <table> <recordId> [fields]

# Create record
nc record:create <base> <table> '{"fields":{"Name":"Alice","Email":"alice@example.com"}}'

# Update record
nc record:update <base> <table> <recordId> '{"Status":"active"}'

# Update multiple records
nc record:update-many <base> <table> '[{"id":1,"fields":{"Status":"done"}}]'

# Delete record
nc record:delete <base> <table> <recordId>

# Delete multiple records
nc record:delete <base> <table> '[1,2,3]'

# Count records
nc record:count <base> <table> [where] [viewId]
```

**Pagination Parameters:**
- `page`: Page number (default: 1)
- `pageSize`: Records per page (default: 25)
- `where`: Filter expression (see Filter Syntax)
- `sort`: Sort expression (see Sort Syntax)
- `fields`: Comma-separated field names to return
- `viewId`: Filter by view

### Linked Records

```bash
# List linked records
nc link:list <base> <table> <linkField> <recordId> [page] [pageSize] [where] [sort] [fields]

# Add links
nc link:add <base> <table> <linkField> <recordId> '[{"id":42}]'

# Remove links
nc link:remove <base> <table> <linkField> <recordId> '[{"id":42}]'
```

### Filters & Sorts

**View-level Filters:**
```bash
nc filter:list <base> <table> <view>
nc filter:create <base> <table> <view> '{"field_id":"field123","operator":"eq","value":"active"}'
nc filter:replace <base> <table> <view> '<json>'
nc filter:update <base> <filterId> '<json>'
nc filter:delete <base> <filterId>
```

**View-level Sorts:**
```bash
nc sort:list <base> <table> <view>
nc sort:create <base> <table> <view> '{"field_id":"field123","direction":"desc"}'
nc sort:update <base> <sortId> '<json>'
nc sort:delete <base> <sortId>
```

### Attachments

```bash
nc attachment:upload <base> <table> <recordId> <field> <filepath>
```

### Scripts (Enterprise)

```bash
nc script:list <base>
nc script:get <base> <scriptId>
nc script:create <base> '{"title":"My Script"}'
nc script:update <base> <scriptId> '<json>'
nc script:delete <base> <scriptId>
```

### Teams (Enterprise)

```bash
nc team:list <workspace>
nc team:get <workspace> <teamId>
nc team:create <workspace> '{"title":"Engineering"}'
nc team:update <workspace> <teamId> '<json>'
nc team:delete <workspace> <teamId>
nc team:members:add <workspace> <teamId> '<json>'
nc team:members:update <workspace> <teamId> '<json>'
nc team:members:remove <workspace> <teamId> '<json>'
```

### API Tokens (Enterprise)

```bash
nc token:list
nc token:create '{"title":"CI Token"}'
nc token:delete <tokenId>
```

## Filter Syntax

### Basic Syntax

```
(field,operator,value)
```

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `(name,eq,John)` |
| `neq` | Not equal | `(status,neq,archived)` |
| `like` | Contains (% wildcard) | `(name,like,%john%)` |
| `nlike` | Does not contain | `(name,nlike,%test%)` |
| `in` | In list | `(status,in,active,pending)` |
| `gt` | Greater than | `(price,gt,100)` |
| `lt` | Less than | `(stock,lt,10)` |
| `gte` | Greater or equal | `(rating,gte,4)` |
| `lte` | Less or equal | `(age,lte,65)` |
| `blank` | Is null/empty | `(notes,blank)` |
| `notblank` | Is not null/empty | `(email,notblank)` |
| `null` | Is null | `(deleted_at,null)` |
| `notnull` | Is not null | `(created_by,notnull)` |
| `checked` | Is checked/true | `(is_active,checked)` |
| `notchecked` | Is not checked/false | `(is_archived,notchecked)` |

### Logical Operators

**Important:** Use tilde prefix (`~and`, `~or`, `~not`)

```bash
# AND
(name,eq,John)~and(age,gte,18)

# OR
(status,eq,active)~or(status,eq,pending)

# NOT
~not(is_deleted,checked)

# Complex
(status,in,active,pending)~and(country,eq,USA)
```

### Date Filters

```bash
# Today
(created_at,eq,today)

# Past week
(created_at,isWithin,pastWeek)

# Last 14 days
(created_at,isWithin,pastNumberOfDays,14)

# Exact date
(event_date,eq,exactDate,2024-06-15)

# Overdue
(due_date,lt,today)
```

### Complex Examples

```bash
# Active users created this month
"(status,eq,active)~and(created_at,isWithin,pastMonth)"

# Overdue high-priority tasks
"(due_date,lt,today)~and(priority,eq,high)~and(completed,notchecked)"

# Orders $100-$500 in pending/processing
"(amount,gte,100)~and(amount,lte,500)~and(status,in,pending,processing)"

# Recently updated, not archived
"(updated_at,isWithin,pastNumberOfDays,14)~and~not(is_archived,checked)"
```

## Sort Syntax

```bash
# Single field ascending (default)
'[{"field":"name"}]'

# Single field descending
'[{"field":"created_at","direction":"desc"}]'

# Multiple fields
'[{"field":"status"},{"field":"created_at","direction":"desc"}]'
```

## Plan Requirements

**Free Plans:** Base, Table, Field, Record, Link, Attachment, Filter, Sort APIs

**Enterprise Plans (self-hosted or cloud-hosted):**
- Workspace and Workspace Collaboration APIs
- View APIs
- Script APIs
- Team APIs
- API Token APIs
- Base Collaboration APIs

## Examples

### Basic Queries

```bash
# List all records in a table
nc record:list MyBase Users

# Get specific record
nc record:get MyBase Users 42

# Paginated query
nc record:list MyBase Users 1 50

# Query with fields selection
nc record:list MyBase Users 1 25 "" "" "name,email,phone"
```

### Filtering

```bash
# Simple filter
nc record:list MyBase Users 1 25 "(status,eq,active)"

# Like search
nc record:list MyBase Users 1 25 "(name,like,%john%)"

# Combined filters
nc record:list MyBase Users 1 25 "(status,eq,active)~and(age,gte,18)"

# Date filter
nc record:list MyBase Tasks 1 25 "(due_date,lt,today)"
```

### Sorting

```bash
# Sort by name ascending
nc record:list MyBase Users 1 25 "" '[{"field":"name"}]'

# Sort by date descending
nc record:list MyBase Users 1 25 "" '[{"field":"created_at","direction":"desc"}]'

# Multiple sorts
nc record:list MyBase Users 1 25 "" '[{"field":"status"},{"field":"name"}]'
```

### Creating Data

```bash
# Create single record
nc record:create MyBase Users '{"fields":{"name":"Alice","email":"alice@example.com","status":"active"}}'

# Create with number fields
nc record:create MyBase Products '{"fields":{"name":"Widget","price":29.99,"quantity":100}}'
```

### Updating Data

```bash
# Update single field
nc record:update MyBase Users 42 '{"status":"inactive"}'

# Update multiple fields
nc record:update MyBase Users 42 '{"status":"active","last_login":"2024-01-15"}'

# Update multiple records
nc record:update-many MyBase Users '[{"id":1,"fields":{"status":"done"}},{"id":2,"fields":{"status":"done"}}]'
```

### Working with Linked Records

```bash
# List linked records
nc link:list MyBase Orders order_items 123

# Add link
nc link:add MyBase Orders order_items 123 '[{"id":456}]'

# Remove link
nc link:remove MyBase Orders order_items 123 '[{"id":456}]'
```

### Using Views

```bash
# List records through a view
nc record:list MyBase Users 1 25 "" "" "" view123

# Count records in a view
nc record:count MyBase Users "" view123
```

### Uploading Files

```bash
nc attachment:upload MyBase Documents 42 file_field ./report.pdf
```

## Troubleshooting

### Connection Issues

```bash
# Check environment variables
echo $NOCODB_TOKEN
echo $NOCODB_URL

# Test connection
nc workspace:list
```

### Verbose Mode

Enable verbose output to see resolved IDs:

```bash
export NOCODB_VERBOSE=1
nc field:list MyBase Users
# Output: → base: MyBase → pdef5678uvw
#         → table: Users → mghi9012rst
```

### Common Errors

| Error | Solution |
|-------|----------|
| `NOCODB_TOKEN required` | Set the environment variable |
| `workspace not found` | Check workspace name or use ID |
| `base not found` | Check base name or use ID |
| `table not found` | Check table name or use ID |
| `401 Unauthorized` | Check your API token |

## Help

Show complete command reference:

```bash
nc
```

Show filter syntax help:

```bash
nc where:help
```

## Resources

- **NocoDB Documentation:** https://docs.nocodb.com/
- **API Reference:** https://docs.nocodb.com/developer-resources/rest-APIs/
- **GitHub:** https://github.com/nocodb/nocodb

## License

This skill wraps the NocoDB API. NocoDB is open-source under the AGPL-3.0 license.
