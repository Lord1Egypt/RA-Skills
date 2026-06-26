---
name: ops-mysql-master-slave
description: MySQL Master-Slave Setup & Troubleshooting SOP. Covers replication setup, Percona XtraBackup large-volume migration, replica lag investigation, and cross-cloud database acceleration.
triggers:
  - "mysql master slave"
  - "mysql replication"
  - "master slave sync"
  - "mysql replica lag"
  - "mysql migration"
  - "percona xtrabackup"
  - "xtrabackup"
  - "database migration"
  - "mysql backup"
category: ops
tags: [mysql, replication, database, backup, percona, ops]
version: 1.0.0
created: 2026-05-06
---

# MySQL Master-Slave Setup & Troubleshooting SOP

## Scenario 1: Set Up MySQL Master-Slave Replication

Applicable to: Read replica setup, cross-region database acceleration, analytics query isolation.

### Prerequisites
- Master and slave running the same MySQL version (recommend 5.7 or 8.0)
- Network connectivity between master and slave
- Sufficient disk space on slave

### Standard Steps

**1. Configure master MySQL**
```bash
vim /etc/my.cnf
```
Add the following:
```ini
[mysqld]
server-id = 1  # Must be unique
log-bin = mysql-bin
binlog_format = ROW
```
```bash
systemctl restart mysqld
```

**2. Configure slave MySQL**
```bash
vim /etc/my.cnf
```
Add the following:
```ini
[mysqld]
server-id = 2  # Must be unique, different from master
relay-log = relay-bin
read-only = 1  # Recommended for slave
```
```bash
systemctl restart mysqld
```

**3. Create replication user on master**
```sql
CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
```

**4. Lock tables and get binlog position**
```sql
FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
-- Record File and Position
```
**Important**: Do not close this session or stop MySQL before unlocking.

**5. Export data from master**
```bash
# Export all databases
mysqldump -u root -p --all-databases > /tmp/all_db.sql

# Export specific databases only
mysqldump -u root -p --databases db1 db2 > /tmp/db.sql
```

**6. Record binlog info and unlock**
```sql
SHOW MASTER STATUS;
-- Record mysql-bin.000001 and Position
UNLOCK TABLES;
```

**7. Import data on slave**
```bash
mysql -u root -p < /tmp/all_db.sql
```

**8. Establish replication on slave**
```sql
CHANGE MASTER TO
  MASTER_HOST = 'master_ip',
  MASTER_USER = 'repl',
  MASTER_PASSWORD = 'password',
  MASTER_LOG_FILE = 'mysql-bin.000001',
  MASTER_LOG_POS = 1234;

START SLAVE;
SHOW SLAVE STATUS\G;
```

**9. Verify replication**
```sql
SHOW SLAVE STATUS\G;
```
Check that both `Slave_IO_Running` and `Slave_SQL_Running` are `Yes`.

---

## Scenario 2: Percona XtraBackup Large-Volume Migration

Applicable to: Database sizes too large for `mysqldump` (hundreds of GB), or when downtime must be minimized.

### Why XtraBackup
- Hot backup — no database downtime required
- Supports parallel compression
- Based on InnoDB crash recovery — guarantees data consistency

### Environment Setup

**Install XtraBackup (CentOS/RHEL 7)**
```bash
yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
yum install -y percona-xtrabackup-24
```

For Ubuntu/Debian:
```bash
apt install percona-xtrabackup-24
```

**Database user privileges**
```sql
GRANT BACKUP_ADMIN ON *.* TO 'backup_user'@'localhost';
GRANT PROCESS, RELOAD, REPLICATION CLIENT ON *.* TO 'backup_user'@'localhost';
-- Or use root if privileges are sufficient
```

### Backup Steps

**1. Full backup + compression**
```bash
xtrabackup --backup \
  --target-dir=/tmp/backup_full \
  --compress \
  --compress-threads=4 \
  --user=root \
  --password=password
```

**2. Transfer to target server**
```bash
scp -r /tmp/backup_full target_server:/tmp/
```

### Restore Steps

**1. Decompress (on target server)**
```bash
xtrabackup --decompress --target-dir=/tmp/backup_full
```

**2. Prepare (consistency check)**
```bash
xtrabackup --prepare --target-dir=/tmp/backup_full
```
**Important**: Unprepared backups are inconsistent. Starting MySQL with unprepared files will fail.

**3. Restore**
> ⚠️ 执行前请确认：目标机器 IP 正确、数据库名正确、备份文件已 prepare 且可用。生产环境建议先快照或备份旧数据目录。

```bash
# Stop MySQL
systemctl stop mysqld

# Clear data directory
rm -rf /var/lib/mysql/*

# Copy back
xtrabackup --copy-back --target-dir=/tmp/backup_full

# Fix permissions
chown -R mysql:mysql /var/lib/mysql

# Start MySQL
systemctl start mysqld
```

---

## Scenario 3: Replica Lag Investigation

### Diagnostic Commands
```sql
SHOW SLAVE STATUS\G;
```

Key metrics:
| Field | Meaning |
|-------|---------|
| `Slave_IO_Running` | IO thread status |
| `Slave_SQL_Running` | SQL thread status |
| `Seconds_Behind_Master` | Lag in seconds (0 = no lag) |
| `Read_Master_Log_Pos` | Master binlog position read |
| `Relay_Log_Space` | Total relay log size |

### Common Causes

| Cause | Symptom | Resolution |
|-------|---------|------------|
| Slave machine underpowered | High CPU/IO | Upgrade slave hardware |
| Large transaction blocking | SQL thread stuck | Split large transactions |
| Network latency | IO thread slow | Check master-slave network |
| Replication stopped | SQL thread Stopped | `START SLAVE` to retry |

### Cross-Cloud Database Acceleration

Applicable when: Remote servers need to access a central database with high latency (e.g., overseas servers accessing a domestic database).

```
Remote server → Cloud Global Accelerator → Domestic source ECS
```

**Configuration steps**:
1. Create a global acceleration instance in your cloud provider's console
2. Configure acceleration region (remote) and source IP (domestic MySQL)
3. Obtain the accelerated IP
4. Configure security group on source server to allow the accelerator's backend nodes (note: IP group may be dynamic)
5. Test: `telnet accelerated_ip 3306`

---

## Scenario 4: MySQL Memory Usage Investigation

Applicable to: Self-managed MySQL with high memory usage causing performance degradation.

### Investigation Steps

**1. Confirm MySQL memory usage**
```bash
ps -eo pid,rss,vsz,comm | grep mysql
top -b -n 1 | grep mysql
```

**2. Buffer Pool usage by database**
```sql
SELECT
    SUBSTRING_INDEX(table_name, '/', 1) AS db,
    COUNT(*) * 16 / 1024 AS size_mb
FROM information_schema.innodb_buffer_page_lru
WHERE table_name IS NOT NULL
GROUP BY db
ORDER BY size_mb DESC
LIMIT 20;
```

**3. Buffer Pool total usage**
```sql
SELECT COUNT(*) * 16 / 1024 AS total_mb
FROM information_schema.innodb_buffer_page_lru;
```

**4. MySQL memory distribution (non-buffer pool)**
```sql
SELECT
    event_name,
    CURRENT_NUMBER_OF_BYTES_USED / 1024 / 1024 AS current_mb,
    HIGH_NUMBER_OF_BYTES_USED / 1024 / 1024 AS high_mb
FROM performance_schema.memory_summary_global_by_event_name
ORDER BY CURRENT_NUMBER_OF_BYTES_USED DESC
LIMIT 20;
```

**5. Active connections**
```sql
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
```

**6. Identify high-memory tables**
```sql
SELECT
    table_schema AS 'db',
    table_name AS 'table',
    ROUND(data_length / 1024 / 1024, 2) AS 'data_size_mb',
    ROUND(index_length / 1024 / 1024, 2) AS 'index_size_mb'
FROM information_schema.tables
WHERE table_schema NOT IN ('mysql', 'information_schema', 'performance_schema')
ORDER BY data_length DESC
LIMIT 20;
```

### Common Findings

| Scenario | Indicator | Recommendation |
|----------|-----------|----------------|
| Single db high buffer pool | Normal, frequently accessed | Acceptable |
| Buffer pool near limit | `innodb_buffer_pool_size` too large | Reduce or upgrade memory |
| Non-buffer pool abnormal | Temp tables / large sorts / big queries | Optimize SQL |
| Many connections | Connection pool leak or unclosed connections | Check application connection pool |

---

## Scenario 5: Cross-Server Database Migration (Comprehensive)

Applicable to: Game server migration, server upgrades, regional data transfers.

### Standard Flow

```
1. Export cross-server data
         ↓
2. Upload to target machine
         ↓
3. Create database and import data
         ↓
4. Migrate game/service directory
         ↓
5. Modify configuration files
         ↓
6. Update ops/management database records
         ↓
7. Batch update related service configurations
         ↓
8. Restart service
```

### Key Checkpoints

| Step | Check |
|------|-------|
| Data export | Stop writes, lock tables or shut down service |
| Data transfer | Verify md5sum |
| Data import | Check error logs |
| Config update | Confirm IP, port, database name |
| Database update | ops_server table, management config |
| Service restart | Verify process and port |

---

## Command Cheatsheet

```bash
# Check replica status
SHOW SLAVE STATUS\G;

# Check master binlog position
SHOW MASTER STATUS;

# Stop/start replica
STOP SLAVE;
START SLAVE;

# Reset replica configuration
RESET SLAVE ALL;

# Check connections
SHOW STATUS LIKE 'Threads_connected';

# Check max connections
SHOW VARIABLES LIKE 'max_connections';

# MySQL buffer pool usage by db
SELECT
    SUBSTRING_INDEX(table_name, '/', 1) AS db,
    COUNT(*) * 16 / 1024 AS size_mb
FROM information_schema.innodb_buffer_page_lru
WHERE table_name IS NOT NULL
GROUP BY db;

# XtraBackup backup
xtrabackup --backup --target-dir=/tmp/backup --user=root --password=password

# XtraBackup restore
xtrabackup --prepare --target-dir=/tmp/backup
xtrabackup --copy-back --target-dir=/tmp/backup
```

---

## Notes

1. **server-id must be unique** — master and slave cannot have the same value
2. **Set `read-only=1` on slave** — prevents accidental writes
3. **Use XtraBackup for large volumes** — mysqldump may fail or take too long
4. **High replica lag** — check slave machine performance and network first
5. **Always confirm IP, port, database name before migration** — wrong values will break connectivity
6. **Cross-cloud migration has network latency** — consider using a cloud global acceleration service
