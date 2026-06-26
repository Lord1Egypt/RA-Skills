## ⚠️ 安全声明

本技能需要以下权限：
- 读取数据库凭证（`.env` 或 `~/.pgpass`）
- 写入备份文件到本地磁盘
- 执行用户提供的 SQL 语句

**请确保**：
- 仅在受信任的环境中使用
- 备份文件妥善存储
- 使用最小权限数据库账户
---
name: postgresql-db
description: description: |
  PostgreSQL 数据库操作技能（需要数据库凭证）。
  支持连接管理、表结构查询、CRUD 操作、备份恢复、pgvector 向量查询。
  
  需要环境变量：DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
  或使用~/.pgpass 文件存储凭证。
  
  使用 psql 命令行工具执行操作，适合生产环境数据库运维和开发查询。 
---

# PostgreSQL 数据库操作

## 何时使用

✅ **使用此技能当**:
- 查询数据库表结构、字段、索引
- 执行 SELECT/INSERT/UPDATE/DELETE 操作
- 创建/修改/删除表结构
- 数据库备份与恢复
- pgvector 向量相似度搜索
- 查看连接状态、锁、性能指标
- 导出/导入数据（CSV/SQL）

❌ **不使用此技能当**:
- 需要图形界面操作 → 推荐 DBeaver/pgAdmin
- 复杂 ORM 操作 → 使用 SQLAlchemy/Prisma
- 数据库集群管理 → 使用 Patroni/pgBouncer

## 数据库配置模板

连接信息存储在 `TOOLS.md` 或环境变量，**不要硬编码密码**。

```markdown
### PostgreSQL 数据库

| 项目 | 值 |
|------|-----|
| 主机 | your-db-host.example.com |
| 端口 | 5432 |
| 数据库 | your_database |
| 用户 | your_user |
| 密码 | $DB_PASSWORD (环境变量) |
```

## 基础命令

### 连接数据库

```bash
# 方式 1: 命令行参数
PGPASSWORD='密码' psql -h 主机 -p 端口 -U 用户 -d 数据库

# 方式 2: 环境变量（推荐）
export PGHOST=主机
export PGPORT=5432
export PGDATABASE=数据库
export PGUSER=用户
export PGPASSWORD=密码
psql

# 方式 3: .pgpass 文件（最安全）
echo "主机：端口：数据库：用户：密码" >> ~/.pgpass
chmod 600 ~/.pgpass
psql -h 主机 -U 用户 -d 数据库
```

### 查询表结构

```bash
# 列出所有表
\dt

# 列出所有表（含 schema）
\dt+

# 查看表结构
\d tablename

# 查看表详细结构（含索引、约束）
\d+ tablename

# 查看所有字段类型
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'tablename';
```

### 基础 CRUD

```bash
# 查询
SELECT * FROM 表名 WHERE 条件 LIMIT 10;

# 插入
INSERT INTO 表名 (字段 1, 字段 2) VALUES (值 1, 值 2);

# 更新
UPDATE 表名 SET 字段=新值 WHERE 条件;

# 删除
DELETE FROM 表名 WHERE 条件;

# 计数
SELECT COUNT(*) FROM 表名;
```

## 高级操作

### 导出/导入

```bash
# 导出为 CSV
psql -h 主机 -U 用户 -d 数据库 -c "COPY (SELECT * FROM 表名) TO STDOUT WITH CSV HEADER" > 输出.csv

# 导出整个表
pg_dump -h 主机 -U 用户 -t 表名 数据库 > 表名.sql

# 导入 SQL
psql -h 主机 -U 用户 -d 数据库 < 输入.sql

# 导入 CSV
\copy 表名 FROM '输入.csv' WITH CSV HEADER;
```

### 备份/恢复

```bash
# 完整备份
pg_dump -h 主机 -U 用户 数据库 > 备份.sql

# 压缩备份
pg_dump -h 主机 -U 用户 数据库 | gzip > 备份.sql.gz

# 恢复
psql -h 主机 -U 用户 -d 数据库 < 备份.sql

# 恢复压缩
gunzip -c 备份.sql.gz | psql -h 主机 -U 用户 -d 数据库
```

### pgvector 向量查询

```bash
# 向量相似度搜索（余弦距离）
SELECT *, embedding <-> '[0.1, 0.2, ...]'::vector AS distance
FROM your_table
ORDER BY distance
LIMIT 10;

# 余弦相似度
SELECT *, 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM your_table
WHERE 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) > 0.8
ORDER BY similarity DESC;

# 查看向量维度
SELECT vector_dims(embedding) FROM your_table LIMIT 1;
```

### 性能监控

```bash
# 当前连接
SELECT pid, usename, client_addr, query, state, query_start 
FROM pg_stat_activity WHERE datname = current_database();

# 锁信息
SELECT * FROM pg_locks WHERE NOT granted;

# 慢查询（需要 pg_stat_statements）
SELECT query, calls, total_exec_time, mean_exec_time 
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

# 表大小
SELECT relname AS table, 
       pg_size_pretty(pg_total_relation_size(relid)) AS total
FROM pg_catalog.pg_statio_user_tables 
ORDER BY pg_total_relation_size(relid) DESC;
```

## 安全实践

### 密码管理

- ✅ **推荐**: 使用 `~/.pgpass` 文件存储密码
- ✅ **推荐**: 使用环境变量 `$PGPASSWORD`
- ✅ **推荐**: 使用 `.env` 文件 + `dotenv` 加载
- ❌ **避免**: 在脚本中硬编码密码
- ❌ **避免**: 在日志中暴露密码

### 权限控制

```bash
# 查看用户权限
\du

# 创建只读用户
CREATE USER reader WITH PASSWORD '密码';
GRANT CONNECT ON DATABASE 数据库 TO reader;
GRANT USAGE ON SCHEMA public TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;

# 撤销权限
REVOKE ALL ON TABLE 敏感表 FROM reader;
```

### 审计日志

```bash
# 开启查询日志（postgresql.conf）
log_statement = 'all'  # 或 'mod' / 'ddl'
log_duration = on
log_min_duration_statement = 1000  # 记录>1s 的查询
```

## 脚本示例

### 批量查询脚本

```bash
#!/bin/bash
# scripts/query.sh
source .env
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "$1"
```

### 自动备份脚本

```bash
#!/bin/bash
# scripts/backup.sh
source .env
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > backups/${DB_NAME}_${DATE}.sql.gz
find backups/ -mtime +7 -delete  # 保留 7 天
```

## 故障排查

### 连接失败

```bash
# 检查网络
telnet 主机 5432

# 检查 pg_hba.conf
# 确保允许你的 IP 连接

# 检查防火墙
sudo ufw status | grep 5432
```

### 权限错误

```bash
# 查看当前用户
SELECT current_user;

# 查看表所有者
SELECT tablename, tableowner FROM pg_tables WHERE schemaname = 'public';
```

### 性能问题

```bash
# 分析表（更新统计信息）
ANALYZE 表名;

# 重建索引
REINDEX TABLE 表名;

# 清理死元组
VACUUM 表名;
VACUUM FULL 表名;  # 锁表，谨慎使用
```

## 参考资料

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [pgvector 文档](https://github.com/pgvector/pgvector)
- [psql 命令速查](https://postgresmeta.com/docs/psql-commands)
