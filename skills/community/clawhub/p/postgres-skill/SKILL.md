---
name: postgres-skill
description: PostgreSQL 数据库管理技能。通过自然语言查询、管理 PostgreSQL 数据库，支持复杂查询、性能分析、JSON 操作、全文搜索等高级功能。当用户提到 PostgreSQL、Postgres、复杂查询、性能优化时使用此技能。
---

# PostgreSQL Skill - 高级数据库管理

通过自然语言，轻松管理 PostgreSQL，利用其强大特性！

---

## 🎯 功能特点

### 核心能力
- **🔍 智能查询** - 自然语言描述，自动生成 SQL
- **📊 高级分析** - 窗口函数、CTE、复杂聚合
- **📝 JSON 操作** - JSONB 查询、更新、索引
- **🔎 全文搜索** - PostgreSQL 强大的全文搜索能力
- **⚡ 性能分析** - EXPLAIN ANALYZE、索引优化
- **💾 备份恢复** - pg_dump/pg_restore 完整方案

---

## 📋 使用场景

### 查询场景
- "查询每个部门薪资前三的员工"（窗口函数）
- "找出重复的订单号"（HAVING 子句）
- "统计用户留存率"（复杂分析查询）

### JSON 数据场景
- "查询 JSON 字段中特定路径的值"
- "更新 JSONB 数据中的嵌套字段"
- "为 JSON 字段创建 GIN 索引"

### 全文搜索场景
- "搜索包含特定关键词的文章"
- "按相关度排序搜索结果"
- "中文全文搜索配置"

---

## 🔧 前置条件

### 1. 安装 PostgreSQL 客户端

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql-client
```

**macOS:**
```bash
brew install libpq
```

**Windows:**
下载并安装 PostgreSQL 官方客户端工具

### 2. 配置数据库连接

**使用环境变量：**
```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=your_username
export PGPASSWORD=your_password
export PGDATABASE=your_database
```

**或使用连接字符串：**
```
postgresql://username:password@localhost:5432/database
```

---

## 💻 常用操作

### 高级查询示例

#### 窗口函数 - 每部门薪资前3的员工
```sql
SELECT 
    department,
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees
QUALIFY rank <= 3;
```

#### CTE (Common Table Expression)
```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    total,
    LAG(total) OVER (ORDER BY month) as prev_month,
    ROUND(
        (total - LAG(total) OVER (ORDER BY month))::numeric / 
        LAG(total) OVER (ORDER BY month) * 100, 
        2
    ) as growth_pct
FROM monthly_sales;
```

---

### JSONB 操作

#### 查询 JSONB 字段
```sql
-- 查询 JSON 中的嵌套值
SELECT 
    id,
    metadata->>'user_id' as user_id,
    metadata->'preferences'->>'theme' as theme
FROM users
WHERE metadata->>'status' = 'active';
```

#### 更新 JSONB 字段
```sql
UPDATE users
SET metadata = jsonb_set(
    metadata,
    '{preferences,theme}',
    '"dark"'
)
WHERE id = 123;
```

#### 为 JSONB 创建索引
```sql
-- GIN 索引支持高效的 JSONB 查询
CREATE INDEX idx_users_metadata_gin ON users USING gin (metadata jsonb_path_ops);
```

---

### 全文搜索

#### 配置中文全文搜索
```sql
-- 创建全文搜索索引
CREATE INDEX idx_articles_content_fts ON articles
USING gin(to_tsvector('chinese', content));

-- 全文搜索
SELECT title, ts_headline('chinese', content, query) as snippet
FROM articles, to_tsquery('chinese', '人工智能') as query
WHERE to_tsvector('chinese', content) @@ query
ORDER BY ts_rank(to_tsvector('chinese', content), query) DESC;
```

---

### 性能分析

#### EXPLAIN ANALYZE 查询计划
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM orders
WHERE status = 'completed'
ORDER BY created_at DESC
LIMIT 100;
```

#### 查找缺失的索引
```sql
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE tablename = 'your_table'
ORDER BY n_distinct DESC;
```

#### 索引使用率分析
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE idx_scan < 50  -- 很少使用的索引
ORDER BY idx_scan;
```

---

## 💾 备份恢复

### 备份

**完整备份：**
```bash
pg_dump -F c -f backup_$(date +%Y%m%d).dump your_database
```

**仅结构备份：**
```bash
pg_dump -s -f schema_only.sql your_database
```

**仅数据备份：**
```bash
pg_dump -a -f data_only.sql your_database
```

**单表备份：**
```bash
pg_dump -t table_name -f table_backup.sql your_database
```

### 恢复

**恢复完整备份：**
```bash
pg_restore -d target_database backup_file.dump
```

**列出备份内容：**
```bash
pg_restore -l backup_file.dump
```

**选择性恢复：**
```bash
pg_restore -d target_database -t table_name backup_file.dump
```

---

## 🔍 监控与维护

### 数据库大小查询
```sql
SELECT 
    datname as database_name,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

### 表大小查询
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### 活跃连接查询
```sql
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

---

## ⚠️ 注意事项

### 性能优化建议
1. **使用合适的索引** - 为 WHERE、JOIN、ORDER BY 字段创建索引
2. **避免 SELECT *** - 只查询需要的字段
3. **使用 EXPLAIN** - 复杂查询先分析执行计划
4. **定期 VACUUM** - 清理死元组，回收空间
5. **统计信息更新** - `ANALYZE table` 更新统计信息

### 安全建议
1. **使用参数化查询** - 防止 SQL 注入
2. **最小权限原则** - 使用只读用户进行查询
3. **定期备份** - 生产环境必须开启定时备份
4. **连接池配置** - 使用 PgBouncer 管理连接

---

## 🎓 示例对话

### 示例 1：复杂分析查询
**用户：** "查询每个部门员工的薪资排名"

**AI：** "使用窗口函数查询每个部门的员工薪资排名"
```sql
SELECT 
    department,
    name,
    salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
FROM employees
ORDER BY department, salary_rank;
```

### 示例 2：JSONB 查询
**用户：** "查询用户偏好设置中主题为 dark 的用户"

**AI：** "查询 JSONB 字段中的嵌套值"
```sql
SELECT id, username, metadata->'preferences' as preferences
FROM users
WHERE metadata->>'theme' = 'dark';
```

### 示例 3：性能优化
**用户：** "帮我分析这个查询为什么慢"

**AI：** "使用 EXPLAIN ANALYZE 分析查询执行计划"
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders o
JOIN users
WHERE o.user_id = users.id
  AND o.created_at >= NOW() - INTERVAL '7 days';
```

---

## 📚 参考资料

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [PostgreSQL 性能优化](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [PostgreSQL JSONB 使用指南](https://www.postgresql.org/docs/current/datatype-json.html)

---

**开始使用：** 告诉我你的查询需求，我会利用 PostgreSQL 的强大特性帮你完成！🚀
