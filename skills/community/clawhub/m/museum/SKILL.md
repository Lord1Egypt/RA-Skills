# Museum Skill - Museum Data Operations

A skill for reading, querying, and managing museum database operations.

---

## Overview

This skill provides standardized interfaces for operating a museum database, supporting:
- Querying museum lists and details
- Checking data collection progress
- Validating data integrity
- Exporting data

Perfect for museum data collection projects that need to track and manage information about museums, their collections, and related media.

---

## Installation

```bash
# Via clawhub
clawhub install museum

# Or manually
git clone <repository>
cd museum-skill
clawhub link .
```

---

## Configuration

Set these environment variables in your shell or agent configuration:

```bash
export MYSQL_HOST="your-database-host"
export MYSQL_USER="your-username"
export MYSQL_PSWD="your-password"
export DATABASE="museumcheck"  # default name
```

Or add to your agent's workspace `TOOLS.md` for automatic loading.

---

## Quick Start

```bash
# List all museums
museum list

# Get details of a specific museum
museum get "Museum Name"

# Check collection statistics
museum stats

# Find museums with missing data
museum check
```

---

## Commands

### 1. List Museums

```bash
museum list [options]

Options:
  --status=STATUS     Filter by status (complete, partial, pending)
  --location=LOC      Filter by location/province
  --limit=N          Limit results (default: 50)
  --offset=N         Pagination offset

Examples:
  museum list --status=complete --limit=10
  museum list --location=Beijing
  museum list --limit=20 --offset=20
```

### 2. Get Museum Details

```bash
museum get <ID|NAME>

Examples:
  museum get "Shaanxi History Museum"
  museum get dd44a9d7c1ad4a4ba21e00e5f60a7b7e
```

### 3. View Statistics

```bash
museum stats

Shows:
- Total museum count
- Completed/partial/pending breakdown
- Distribution by location
- Data completeness metrics
```

### 4. Check Data Integrity

```bash
museum check [ID]

Without ID: Shows museums with missing data
With ID: Checks specific museum completeness
```

### 5. Export Data

```bash
museum_export --format=FORMAT --output=FILE

Formats:
  json  - JSON format
  csv   - CSV format
  sql   - SQL INSERT statements

Examples:
  museum export --format=json --output=museums.json
  museum export --format=csv --output=museums.csv
```

### 6. Custom Query

```bash
museum query "SQL_STATEMENT"

Example:
  museum query "SELECT name, location FROM museums WHERE status='complete';"
```

---

## Database Schema

The skill expects this database structure:

```sql
CREATE DATABASE IF NOT EXISTS museumcheck 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS museums (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(100),
    type VARCHAR(100),
    visitors VARCHAR(50),
    is_free VARCHAR(10),
    precious_artifacts VARCHAR(50),
    total_artifacts VARCHAR(50),
    exhibitions VARCHAR(50),
    introduction TEXT,
    top3_artifacts JSON,
    building_photo VARCHAR(500),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    data_sources TEXT,
    INDEX idx_location (location),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Initialize with:
```bash
# The skill will auto-create tables, or you can use:
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PSWD < schema.sql
```

---

## Use Cases

### Data Collection Workflow

```bash
# 1. Check current progress
museum stats

# 2. Get pending items for batch processing
museum list --status=pending --limit=5

# 3. After collecting data, verify completeness
museum check <museum_id>

# 4. Export for backup
museum export --format=json --output=backup.json
```

### Finding Incomplete Records

```bash
# Museums missing introductions
museum query "SELECT name, location FROM museums WHERE introduction IS NULL;"

# Museums missing photos
museum query "SELECT name, location FROM museums WHERE building_photo IS NULL;"

# Count by status
museum query "SELECT status, COUNT(*) FROM museums GROUP BY status;"
```

### Batch Operations

```bash
# Export only complete records
museum query "SELECT * FROM museums WHERE status='complete';" > complete.csv

# Find museums in a specific region
museum list --location=Shaanxi
```

---

## Integration with Agent Workflows

### In an Agent Task

```markdown
## Data Collection Task

Use the museum skill to track your progress:

1. Check what's already done:
   ```bash
   museum stats
   ```

2. Get items to work on:
   ```bash
   museum list --status=pending --limit=5
   ```

3. After collecting data for each item:
   - Update the database
   - Verify with `museum check <id>`

4. Report progress:
   ```bash
   museum stats
   ```
```

### Automation Example

```bash
#!/bin/bash
# daily_backup.sh

# Export complete data
museum export --format=json --output="backups/museums_$(date +%Y%m%d).json"

# Check for incomplete items
museum check > "reports/incomplete_$(date +%Y%m%d).txt"
```

---

## Troubleshooting

### Connection Failed

```bash
# Check environment variables
echo $MYSQL_HOST $MYSQL_USER

# Test connection manually
mycli -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PSWD -e "SELECT 1;"
```

### No Results

- Verify database name: `echo $DATABASE`
- Check if table exists: `museum query "SHOW TABLES;"`
- Verify data exists: `museum query "SELECT COUNT(*) FROM museums;"`

### Permission Denied

Ensure your MySQL user has:
- SELECT, INSERT, UPDATE, DELETE on the database
- Or full privileges: `GRANT ALL ON museumcheck.* TO 'user'@'%';`

---

## Tips

1. **Batch Processing**: Use `--limit` and `--offset` for pagination
2. **Status Tracking**: Use `status` field to track collection progress
3. **JSON Fields**: `top3_artifacts` stores array data; query with JSON functions
4. **UTF8 Support**: Database uses utf8mb4 for international character support

---

## Contributing

Contributions welcome! Please submit issues and pull requests.

---

## License

MIT License
