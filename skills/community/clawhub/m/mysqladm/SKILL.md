---
name: mysqladm
description: MySQL database management via mysql CLI or Python mysql-connector. Use when: (1) executing queries and displaying results, (2) managing schemas (create/alter tables, indexes), (3) database backup/restore, (4) performance analysis (slow queries, index usage), (5) user and permission management. NOT for: complex ETL workflows (use specialized tools), real-time streaming (use CDC tools), or when mysql CLI is not installed/accessible.
homepage: https://dev.mysql.com/doc/
metadata:
  {
    "openclaw":
      {
        "emoji": "🐬",
        "requires":
          {
            "anyBins": ["mysql", "mysqlcheck", "mysqldump"],
            "optionalBins": ["python3"],
          },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "package": "mysql-client",
              "bins": ["mysql", "mysqlcheck", "mysqldump"],
              "label": "Install MySQL client (apt)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "formula": "mysql-client",
              "bins": ["mysql", "mysqlcheck", "mysqldump"],
              "label": "Install MySQL client (brew)",
            },
          ],
      },
  }
---

# MySQL Administration

Manage MySQL databases using the mysql CLI or Python mysql-connector.

## When to Use

✅ **USE this skill when:**

- "Query users who registered today"
- "Add an index to the orders table"
- "Backup the production database"
- "Check slow query logs"
- "Grant permissions to a new user"
- "Analyze table size and storage usage"

## When NOT to Use

❌ **DON'T use this skill when:**

- Complex ETL workflows → use specialized ETL tools (Airflow, dbt)
- Real-time data streaming → use CDC tools (Debezium, Maxwell)
- Graph database queries → use Neo4j or graph-specific tools
- Time-series analytics → use TimescaleDB or InfluxDB
- Large-scale data processing → use Spark or distributed systems

## Setup

### Connection Configuration

Set environment variables or use command-line flags:

```bash
# Environment variables (recommended)
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_USER="root"
export MYSQL_PASSWORD="password"
export MYSQL_DATABASE="mydb"

# Or use flags directly
mysql -h localhost -P 3306 -u root -p mydb
```

### Test Connection

```bash
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT VERSION();"
```

## Quick Start

### Execute Query

```bash
# Using environment variables
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SELECT * FROM users LIMIT 10"

# Direct connection
mysql -h localhost -u root -p -e "SHOW DATABASES;"
```

### Schema Information

```bash
# List all databases
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SHOW DATABASES;"

# Show tables
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SHOW TABLES;"

# Describe table structure
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "DESCRIBE users;"
```

## Common Operations

### Query Execution

```bash
# Simple query
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SELECT id, name FROM users WHERE created_at > '2026-01-01';"

# Query with formatting (table output)
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -t -e "SELECT * FROM orders LIMIT 5;"

# Query with JSON output
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE --json -e "SELECT * FROM products;"
```

### Schema Management

```bash
# Create table
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE << 'SQL'
CREATE TABLE IF NOT EXISTS events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  event_type VARCHAR(50),
  payload JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SQL

# Add index
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "CREATE INDEX idx_user_email ON users(email);"

# Alter table
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "ALTER TABLE orders ADD COLUMN status VARCHAR(20);"
```

### Database Backup

```bash
# Using bundled script
{baseDir}/scripts/mysql_backup.sh --host $MYSQL_HOST --user $MYSQL_USER --password $MYSQL_PASSWORD --database $MYSQL_DATABASE --output /tmp/backup.sql

# Or using mysqldump directly
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > /tmp/backup.sql

# Backup with specific tables
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE users orders > /tmp/partial_backup.sql
```

### Database Restore

```bash
# Using bundled script
{baseDir}/scripts/mysql_restore.sh --host $MYSQL_HOST --user $MYSQL_USER --password $MYSQL_PASSWORD --database $MYSQL_DATABASE --input /tmp/backup.sql

# Or using mysql directly
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < /tmp/backup.sql
```

### Performance Analysis

```bash
# Check table sizes
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD information_schema -e "
SELECT
  table_schema,
  table_name,
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM tables
WHERE table_schema = '$MYSQL_DATABASE'
ORDER BY size_mb DESC;
"

# Show indexes
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SHOW INDEX FROM users;"

# Analyze table
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "ANALYZE TABLE users;"

# Check slow queries (requires slow query log enabled)
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SHOW VARIABLES LIKE 'slow_query_log';"
```

### User Management

```bash
# Create user
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD << 'SQL'
CREATE USER 'app_user'@'%' IDENTIFIED BY 'secure_password';
SQL

# Grant permissions
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD << 'SQL'
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
SQL

# Show users
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT user, host FROM mysql.user;"
```

## Script Usage

### mysql_query.sh

Execute queries with formatted output:

```bash
{baseDir}/scripts/mysql_query.sh \
  --host $MYSQL_HOST \
  --user $MYSQL_USER \
  --password $MYSQL_PASSWORD \
  --database $MYSQL_DATABASE \
  --query "SELECT COUNT(*) FROM users"
```

### mysql_backup.sh

Backup database with timestamp:

```bash
{baseDir}/scripts/mysql_backup.sh \
  --host $MYSQL_HOST \
  --user $MYSQL_USER \
  --password $MYSQL_PASSWORD \
  --database $MYSQL_DATABASE \
  --output /backups/$(date +%Y%m%d)_backup.sql
```

### mysql_restore.sh

Restore from backup:

```bash
{baseDir}/scripts/mysql_restore.sh \
  --host $MYSQL_HOST \
  --user $MYSQL_USER \
  --password $MYSQL_PASSWORD \
  --database $MYSQL_DATABASE \
  --input /backups/20260115_backup.sql
```

## Advanced Queries

### Aggregate Functions

```bash
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE << 'SQL'
SELECT
  DATE(created_at) as date,
  COUNT(*) as daily_users,
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_users
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;
SQL
```

### Join Queries

```bash
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE << 'SQL'
SELECT
  u.name,
  u.email,
  COUNT(o.id) as order_count,
  SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email
HAVING total_spent > 1000
ORDER BY total_spent DESC;
SQL
```

## Security Notes

- **Never hardcode passwords** in scripts or queries. Use environment variables.
- **Use least-privilege principle**: Grant only necessary permissions to application users.
- **Encrypt connections**: Use SSL/TLS for remote connections (`--ssl-mode=REQUIRED`).
- **Validate inputs**: When constructing queries dynamically, always sanitize inputs to prevent SQL injection.
- **Backup before modifications**: Always create a backup before schema changes or bulk updates.

## Troubleshooting

### Connection Issues

```bash
# Test connectivity
telnet $MYSQL_HOST $MYSQL_PORT

# Check MySQL service
systemctl status mysql  # or: service mysql status

# Check firewall
sudo ufw status
```

### Permission Denied

```bash
# Check current user
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT CURRENT_USER();"

# Check grants
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SHOW GRANTS FOR CURRENT_USER();"
```

### Slow Queries

```bash
# Enable slow query log
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD << 'SQL'
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
SQL

# View slow queries
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;"
```

## References

For detailed schema analysis and performance tuning, see:

- [Schema Analysis](references/schema-analysis.md) - Table structure analysis and optimization
- [Performance Tuning](references/performance-tuning.md) - Query optimization and indexing strategies

## Notes

- Always use transactions for multi-step operations: `START TRANSACTION; ... COMMIT;` or `ROLLBACK;`
- Use `EXPLAIN` to analyze query execution plans before running complex queries
- Monitor database size and growth regularly
- Keep backups in multiple locations for disaster recovery
- Test backup/restore procedures regularly to ensure they work when needed
