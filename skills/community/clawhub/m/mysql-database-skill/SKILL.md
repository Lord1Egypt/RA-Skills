---
name: mysql-database
description: "MySQL 数据库操作技能。通过 mysql CLI 连接数据库，执行 SELECT 查询、INSERT/UPDATE/DELETE 增删改、批量 SQL 执行、事务控制、数据库/表管理、JSON 格式输出。适用场景：查用户数据、统计报表、数据导入导出、数据库巡检、表结构查看、远程连接、生产环境调试。触发关键词：MySQL、数据库查询、SQL 语句执行、连接数据库、查表、数据增删改、jdbc 连接字符串、navicat、数据库迁移、DESCRIBE TABLE、查看表结构、表字段分析、查看索引、EXPLAIN 查询分析。"
license: "Copyright © 2026 少煊（年少有为，名声煊赫）<429668385@qq.com>. All rights reserved."
---

# MySQL Database Skill

Use the `mysql` CLI to connect to and interact with MySQL databases. Use the `-e` flag to execute SQL statements and the `-s` (`--silent`) flag to produce clean output suitable for processing. Combine with `-r` (`--raw`) to avoid escaping, and pipe the result to `jq` for reliable JSON formatting.

## 快速使用场景

### 场景 1: 查询数据（最常用）

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT * FROM users LIMIT 10;" 2>$null
```

### 场景 2: 查看表结构

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "DESCRIBE users;" 2>$null
```

### 场景 3: 插入/更新/删除数据

```bash
# 插入
mysql -h <host> -u <user> --database <db> -s -r -e "INSERT INTO users (name, email) VALUES ('Test', 'test@example.com');" 2>$null

# 更新
mysql -h <host> -u <user> --database <db> -s -r -e "UPDATE users SET status=1 WHERE id=1;" 2>$null

# 删除
mysql -h <host> -u <user> --database <db> -s -r -e "DELETE FROM users WHERE id=1;" 2>$null
```

### 场景 4: 统计数据报表

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT COUNT(*) as total, SUM(amount) as revenue FROM orders WHERE DATE(create_time)=CURDATE();" | jq -s '.'
```

### 场景 5: 导出数据到文件

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT * FROM users INTO OUTFILE '/tmp/users.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';" 2>$null
```

### 场景 6: 执行 SQL 脚本文件

```bash
mysql -h <host> -u <user> --database <db> -s -r < script.sql 2>$null
```

## 数据库连接

### 基础连接

```bash
mysql -h <hostname> -P <port> -u <username> --database <database-name> -s -r
```

**示例 (连接本地数据库):**
```bash
MYSQL_PWD=yourpassword mysql -h 127.0.0.1 -u app_user --database app_db -s -r
```

### 从 JDBC URL 解析连接参数

用户可能提供 JDBC URL 格式：`jdbc:mysql://host:port/database`，需要解析为 mysql CLI 参数：

```
jdbc:mysql://nexus.syrinxchina.com:3306/test3
  → -h nexus.syrinxchina.com -P 3306 --database test3
```

```bash
# 示例：从 JDBC URL 构建连接
JDBC_URL="jdbc:mysql://nexus.syrinxchina.com:3306/test3"
HOST=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\1/p')
PORT=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\2/p')
DB=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\3/p')
mysql -h "$HOST" -P "$PORT" -u root --database "$DB" -s -r
```

### 连接参数表

| Option | Description |
|--------|-------------|
| `-h` | Hostname (default: localhost) |
| `-P` | Port (default: 3306) |
| `-u` | Username |
| `-p` | Prompt for password (less secure, avoid in scripts) |
| `-D` / `--database` | Default database |
| `-e` | Execute query and exit |
| `-s` | Silent mode (no headers/borders) |
| `-r` | Raw mode (no escaping) |
| `--ssl-mode=REQUIRED` | Force SSL connection |
| `--connect-timeout=<seconds>` | Connection timeout |
| `--default-character-set=utf8mb4` | Character set |

**连接示例 (完整参数):**
```bash
MYSQL_PWD=password mysql -h 192.168.1.100 -P 3306 -u admin --database mydb --ssl-mode=REQUIRED --connect-timeout=10 -s -r
```

### 使用配置文件

创建 `~/.my.cnf` 简化频繁连接：

```ini
[client]
host = 127.0.0.1
port = 3306
user = app_user
database = app_db
password = yourpassword
ssl-mode = DISABLED
```

```bash
mysql --defaults-extra-file=~/.my.cnf -s -r -e "SELECT 1;"
```

## 数据操作

### 查询 (SELECT)

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT * FROM your_table LIMIT 5;" | jq -R -s 'split("\n") | map(select(. != "")) | map(split("\t")) | {headers: .[0], rows: .[1:]}'
```

**更推荐的方法 (在SQL内生成JSON):**
```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT JSON_OBJECT('id', id, 'name', name) FROM users LIMIT 5;" | jq -s '.'
```

输出：
```json
[
 {"id": 1, "name": "Alice"},
 {"id": 2, "name": "Bob"}
]
```

### 插入 (INSERT)

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "INSERT INTO users (name, email) VALUES ('New User', 'new@example.com'); SELECT JSON_OBJECT('last_insert_id', LAST_INSERT_ID());" | jq .
```

### 更新 (UPDATE)

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "UPDATE users SET status = 'active' WHERE signup_date < '2026-01-01'; SELECT JSON_OBJECT('rows_affected', ROW_COUNT());" | jq .
```

### 删除 (DELETE)

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "DELETE FROM sessions WHERE last_activity < DATE_SUB(NOW(), INTERVAL 30 DAY); SELECT JSON_OBJECT('rows_affected', ROW_COUNT());" | jq .
```

## 高级查询与 JSON 输出

### 统计摘要查询

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT JSON_OBJECT(
 'total_users', (SELECT COUNT(*) FROM users),
 'active_users', (SELECT COUNT(*) FROM users WHERE status = 'active'),
 'avg_posts', (SELECT AVG(post_count) FROM user_stats)
) AS report;
" | jq .
```

### 通用 JSON 输出模式

**单行结果：**
```bash
mysql ... -s -r -e "SELECT JSON_OBJECT('key1', column1, 'key2', column2) FROM ..." | jq .
```

**多行结果：**
```bash
mysql ... -s -r -e "SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'name', name)) FROM users;" | jq .
```

## 批量执行 SQL 文件

```bash
mysql -h <host> -u <user> --database <db> -s -r < script.sql 2>$null
```

**带变量执行：**
```bash
mysql -h <host> -u <user> --database <db> -s -r -e "source script.sql;"
```

**批量导入 CSV：**
```bash
mysql -h <host> -u <user> --database <db> -s -r -e "LOAD DATA LOCAL INFILE 'data.csv' INTO TABLE my_table FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' (col1, col2, col3);"
```

## 事务支持

```bash
# 提交事务
mysql -h <host> -u <user> --database <db> -s -r -e "
START TRANSACTION;
INSERT INTO orders (user_id, total) VALUES (1, 100.50);
UPDATE inventory SET stock = stock - 1 WHERE product_id = 42;
COMMIT;
SELECT JSON_OBJECT('status', 'committed') AS result;
" | jq .
```

**事务回滚：**
```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
START TRANSACTION;
INSERT INTO users (name) VALUES ('Test');
ROLLBACK;
SELECT JSON_OBJECT('rolled_back', true) AS result;
" | jq .
```

## 错误处理

### 常见错误码

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 1045 | Access denied | 检查用户名/密码是否正确 |
| 1049 | Unknown database | 检查数据库名是否存在 |
| 2003 | Can't connect to MySQL | 检查 MySQL 服务是否启动，端口是否开放 |
| 1146 | Table doesn't exist | 检查表名拼写是否正确 |

### 超时配置

```bash
mysql -h <host> -u <user> --database <db> --connect-timeout=5 --read-timeout=30 --write-timeout=30 -s -r -e "SELECT * FROM large_table;"
```

### 连接测试模式

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SELECT 1 AS connected;" 2>&1 | grep -q "connected" && echo "连接成功" || echo "连接失败"
```

## 数据库与表操作

### 创建数据库

```bash
mysql -h <host> -u <user> -s -r -e "CREATE DATABASE IF NOT EXISTS new_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 列出所有数据库

```bash
mysql -h <host> -u <user> -s -r -e "SHOW DATABASES;"
```

### 列出表

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SHOW TABLES;"
```

### 查看表结构

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "DESCRIBE users;"
```

### 查看索引

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SHOW INDEX FROM users;"
```

### 查看建表语句

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SHOW CREATE TABLE users;" | jq -s '.'
```

## DESCRIBE TABLE 详解

### 查看单表结构

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "DESCRIBE users;"
```

输出字段说明：

| 字段 | 说明 |
|------|------|
| Field | 列名 |
| Type | 数据类型（varchar(64)、int、datetime 等） |
| Null | 是否允许 NULL（YES/NO） |
| Key | 索引类型（PRI=主键、UNI=唯一索引、MUL=普通索引） |
| Default | 默认值 |
| Extra | 额外属性（auto_increment、DEFAULT_GENERATED 等） |

### 格式化输出为 JSON

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT JSON_ARRAYAGG(JSON_OBJECT(
  'column', Field,
  'type', Type,
  'nullable', NULL,
  'key', Key,
  'default', Default,
  'extra', Extra
)) AS columns FROM information_schema.columns
WHERE table_schema = '<database>' AND table_name = '<table>'
ORDER BY ordinal_position;" | jq .
```

### 查看表的所有信息（含注释）

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA, COLUMN_COMMENT
FROM information_schema.columns
WHERE table_schema = '<database>' AND table_name = '<table>'
ORDER BY ordinal_position;" | jq -s '.'
```

### 快速查看主键和自增字段

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT COLUMN_NAME, DATA_TYPE, EXTRA
FROM information_schema.columns
WHERE table_schema = '<database>'
  AND table_name = '<table>'
  AND (COLUMN_KEY = 'PRI' OR EXTRA LIKE '%auto_increment%')
ORDER BY COLUMN_KEY DESC, ordinal_position;" | jq -s '.'
```

### EXPLAIN 查询分析（重要！）

**分析 SELECT 查询执行计划：**

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "EXPLAIN SELECT * FROM users WHERE phone = '13800138000';" | jq -s '.'
```

**输出字段说明：**

| 字段 | 说明 |
|------|------|
| id | 查询编号 |
| select_type | 查询类型（SIMPLE、PRIMARY、SUBQUERY 等） |
| table | 查询的表 |
| type | 连接类型（const、ref、range、ALL 等，**ALL 表示全表扫描**) |
| possible_keys | 可能使用的索引 |
| key | 实际使用的索引 |
| key_len | 索引长度 |
| rows | 预计扫描行数（越小越好） |
| Extra | 额外信息（Using index、Using where、Using filesort 等） |

**type 性能排序（从快到慢）：**

```
const > eq_ref > ref > range > index > ALL
```

`ALL` 是全表扫描，需要优化（加索引）。

### EXPLAIN ANALYZE（MySQL 8.0+）

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "EXPLAIN ANALYZE SELECT * FROM users WHERE phone = '13800138000';" | jq -s '.'
```

比 EXPLAIN 更详细，包含**实际运行时间**和**实际行数**。

### 查看表的索引详情

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "SHOW INDEX FROM users;" | jq -s '.'
```

返回每个索引的：索引名、列名、唯一性、基数、索引类型

### 查看表大小和行数

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT
  table_name,
  table_rows,
  ROUND(data_length / 1024 / 1024, 2) AS 'data_size_mb',
  ROUND(index_length / 1024 / 1024, 2) AS 'index_size_mb',
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'total_size_mb'
FROM information_schema.tables
WHERE table_schema = '<database>'
ORDER BY (data_length + index_length) DESC;" | jq -s '.'
```

### 查看数据库中所有表的基本信息

```bash
mysql -h <host> -u <user> --database <db> -s -r -e "
SELECT
  TABLE_NAME AS 'table',
  TABLE_ROWS AS 'rows',
  ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'size_mb',
  ROUND(DATA_FREE / 1024 / 1024, 2) AS 'free_mb',
  ENGINE,
  TABLE_COMMENT
FROM information_schema.tables
WHERE table_schema = '<database>'
  AND table_type = 'BASE TABLE'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;" | jq -s '.'
```

**`free_mb` 过大说明表有碎片，可以定期 OPTIMIZE TABLE 回收空间。**

## 环境变量配置

```bash
export MYSQL_PWD="yourpassword"
export MYSQL_HOST="127.0.0.1"
export MYSQL_USER="app_user"
export MYSQL_DATABASE="app_db"

mysql -s -r -e "SELECT 1;"
```

## 完整示例脚本

```bash
#!/bin/bash
# 查询用户统计数据（带错误处理）

DB_HOST="${MYSQL_HOST:-127.0.0.1}"
DB_USER="${MYSQL_USER:-app_user}"
DB_NAME="${MYSQL_DATABASE:-app_db}"

QUERY="
SELECT JSON_OBJECT(
  'timestamp', NOW(),
  'summary', JSON_OBJECT(
    'total_users', (SELECT COUNT(*) FROM users),
    'active_users', (SELECT COUNT(*) FROM users WHERE status = 'active'),
    'new_today', (SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURDATE())
  )
) AS report;
"

mysql -h "$DB_HOST" -u "$DB_USER" --database "$DB_NAME" -s -r -e "$QUERY" 2>&1 | jq .
```

## 安全建议

1. **禁止**在命令行中直接写密码（进程列表可见）
2. **使用** `MYSQL_PWD` 环境变量或配置文件
3. 生产环境**强制**使用 SSL (`--ssl-mode=REQUIRED`)
4. 配置文件权限设置为 `chmod 600 ~/.my.cnf`
5. 查询操作使用只读账号

**重要提示:** 使用 `-s -r` (`--silent --raw`) 组合确保 mysql 客户端输出纯净数据，是生成有效 JSON 的前提。
