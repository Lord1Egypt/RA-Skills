# NocoDB Skill for OpenClaw

Connect your OpenClaw agent to NocoDB databases with ease. Query records, manage tables, handle attachments, and automate your database workflows.

[![NocoDB](https://img.shields.io/badge/NocoDB-v3%20API-blue)](https://nocodb.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green)]()
[![License](https://img.shields.io/badge/License-AGPL--3.0-orange)]()

## What is NocoDB?

[NocoDB](https://nocodb.com) is an open-source Airtable alternative that transforms any database into a smart spreadsheet. Self-host it or use their cloud service—your data stays yours.

## What This Skill Does

This skill provides a complete CLI wrapper for the NocoDB REST API v3, enabling your OpenClaw agent to:

- 🔍 **Query records** with powerful filtering and sorting
- ➕ **Create, update, delete** records programmatically  
- 📊 **Manage database structure** (tables, fields, views)
- 🔗 **Work with linked records** and relationships
- 📎 **Upload and manage attachments**
- 👥 **Handle team collaboration** (Enterprise plans)
- 🔐 **Manage API tokens** (Enterprise plans)

## Quick Start

### 1. Get Your API Token

1. Go to [NocoDB Cloud](https://app.nocodb.com) or your self-hosted instance
2. Navigate to **Team & Settings** → **API Tokens**
3. Create a new token and copy it

### 2. Configure Environment

```bash
export NOCODB_TOKEN="your-api-token-here"
export NOCODB_URL="https://app.nocodb.com"  # Optional, defaults to cloud
```

### 3. Start Using

```bash
# List your workspaces
nc workspace:list

# List bases in a workspace
nc base:list my-workspace

# Query records
nc record:list my-base users

# Create a record
nc record:create my-base users '{"fields":{"name":"Alice","email":"alice@example.com"}}'
```

## Features

### Complete API Coverage

- ✅ **Workspaces** - Manage workspaces and members (Enterprise)
- ✅ **Bases** - List, create, update, delete databases
- ✅ **Tables** - Manage database tables
- ✅ **Fields** - Define columns and data types
- ✅ **Views** - Create grid, gallery, kanban, calendar views (Enterprise)
- ✅ **Records** - Full CRUD operations with pagination
- ✅ **Linked Records** - Handle relationships between tables
- ✅ **Filters & Sorts** - Advanced querying capabilities
- ✅ **Attachments** - Upload and manage files
- ✅ **Scripts** - Automation scripts (Enterprise)
- ✅ **Teams** - Team management (Enterprise)
- ✅ **API Tokens** - Token lifecycle management (Enterprise)

### Smart Identifier Resolution

Use **names** or **IDs** interchangeably:

```bash
# Both work:
nc record:list my-base users           # By name
nc record:list pabc123 mdef456         # By ID (faster)
```

Set `NOCODB_VERBOSE=1` to see automatic ID resolution.

### Powerful Filtering

Filter records with an intuitive syntax:

```bash
# Simple equality
nc record:list my-base users 1 25 "(status,eq,active)"

# Pattern matching
nc record:list my-base users 1 25 "(email,like,%@company.com)"

# Combined conditions
nc record:list my-base users 1 25 "(status,eq,active)~and(created_at,isWithin,pastWeek)"

# Date ranges
nc record:list my-base tasks 1 25 "(due_date,lt,today)~and(priority,eq,high)"
```

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install nocodb
```

### Manual Installation

1. Download `nocodb.skill` from the [releases page](https://github.com/yourusername/nocodb-skill/releases)
2. Place it in your OpenClaw skills directory
3. Set your `NOCODB_TOKEN` environment variable

## Requirements

- **OpenClaw** with bash tool support
- **Environment Variables:**
  - `NOCODB_TOKEN` (required) - Your NocoDB API token
  - `NOCODB_URL` (optional) - Defaults to `https://app.nocodb.com`
- **Tools:** `curl`, `jq`

## Usage Examples

### Database Operations

```bash
# Create a new table
nc table:create my-base '{"title":"Products"}'

# Add fields to the table
nc field:create my-base Products '{"title":"Price","type":"Currency"}'
nc field:create my-base Products '{"title":"Quantity","type":"Number"}'

# Insert records
nc record:create my-base Products '{"fields":{"title":"Laptop","Price":999,"Quantity":10}}'

# Query with filters
nc record:list my-base Products 1 25 "(Quantity,gt,0)~and(Price,lte,1000)"
```

### Working with Views

```bash
# Create a filtered view
nc view:create my-base Products '{"title":"Low Stock","type":"grid"}'

# Add view filter
nc filter:create my-base Products low-stock-view '{"field_id":"field123","operator":"lt","value":"5"}'

# Query through view
nc record:list my-base Products 1 25 "" "" "" low-stock-view
```

### Managing Relationships

```bash
# List linked records
nc link:list my-base Orders items 123

# Add relationship
nc link:add my-base Orders items 123 '[{"id":456},{"id":789}]'
```

### File Attachments

```bash
nc attachment:upload my-base Documents 42 file_field ./report.pdf
```

## Plan Requirements

### Free Plan Includes
- ✅ Base, Table, Field, Record APIs
- ✅ Link, Attachment, Filter, Sort APIs

### Enterprise Plan Adds
- ✅ Workspace management
- ✅ Views (grid, gallery, kanban, calendar)
- ✅ Scripts automation
- ✅ Team management
- ✅ Advanced collaboration features
- ✅ API token management

## Filter Syntax Reference

### Basic Filters
```
(field,operator,value)
```

### Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `(status,eq,active)` |
| `neq` | Not equal | `(status,neq,archived)` |
| `like` | Contains | `(name,like,%john%)` |
| `in` | In list | `(status,in,active,pending)` |
| `gt`/`lt` | Greater/Less than | `(price,gt,100)` |
| `blank` | Is empty | `(notes,blank)` |
| `checked` | Boolean true | `(is_active,checked)` |

### Logical Operators
Use `~and`, `~or`, `~not` (with tilde prefix):

```bash
# AND condition
(status,eq,active)~and(age,gte,18)

# OR condition  
(priority,eq,high)~or(priority,eq,urgent)

# NOT condition
~not(is_deleted,checked)

# Complex
(status,in,active,pending)~and(country,eq,USA)~and(created_at,isWithin,pastMonth)
```

### Date Operators
```bash
(created_at,eq,today)
(created_at,isWithin,pastWeek)
(created_at,isWithin,pastNumberOfDays,14)
(due_date,lt,today)
(event_date,eq,exactDate,2024-06-15)
```

## Troubleshooting

### Common Issues

**"NOCODB_TOKEN required"**
```bash
export NOCODB_TOKEN="your-token-here"
```

**"workspace/base/table not found"**
- Check spelling or use IDs directly
- Enable verbose mode: `export NOCODB_VERBOSE=1`

**"401 Unauthorized"**
- Verify your API token is valid
- Check token permissions in NocoDB dashboard

### Debug Mode

```bash
export NOCODB_VERBOSE=1
nc record:list my-base my-table
```

This shows resolved IDs:
```
→ workspace: MyWorkspace → wabc123xyz
→ base: MyBase → pdef456uvw
→ table: MyTable → mghi789rst
```

## API Compatibility

- **NocoDB v3 API** - Fully supported
- **Cloud & Self-Hosted** - Works with both
- **Free & Enterprise** - All features available based on your plan

## Links

- 📖 [NocoDB Documentation](https://docs.nocodb.com/)
- 🔧 [NocoDB API Reference](https://docs.nocodb.com/developer-resources/rest-APIs/)
- 🐙 [NocoDB GitHub](https://github.com/nocodb/nocodb)
- 🏠 [NocoDB Website](https://nocodb.com)

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

## License

This skill is released under the same license as NocoDB (AGPL-3.0). See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for the OpenClaw community**
