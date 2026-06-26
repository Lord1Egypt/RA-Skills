# 数据库优化

## MySQL

```sql
-- 慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- EXPLAIN 分析
EXPLAIN SELECT * FROM users WHERE name = 'Alice';
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'Alice';

-- 查看索引
SHOW INDEX FROM users;

-- 查看进程
SHOW PROCESSLIST;
SHOW FULL PROCESSLIST;

-- 查看状态
SHOW STATUS LIKE 'Handler%';
SHOW STATUS LIKE 'Innodb%';
```

```bash
# 分析慢查询日志
mysqldumpslow -s t /var/log/mysql/slow.log
mysqldumpslow -s c /var/log/mysql/slow.log
```

## PostgreSQL

```sql
-- EXPLAIN 分析
EXPLAIN SELECT * FROM users WHERE name = 'Alice';
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'Alice';
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE name = 'Alice';

-- 查看活动查询
SELECT * FROM pg_stat_activity;
SELECT pid, query, state FROM pg_stat_activity;

-- 终止查询
SELECT pg_cancel_backend(pid);
SELECT pg_terminate_backend(pid);

-- 表统计
SELECT * FROM pg_stat_user_tables;
SELECT * FROM pg_stat_user_indexes;
```

## Redis

```bash
# 慢查询日志
redis-cli SLOWLOG GET 10
redis-cli SLOWLOG RESET

# 查看信息
redis-cli INFO
redis-cli INFO stats
redis-cli INFO memory

# 实时监控
redis-cli MONITOR

# 压测
redis-benchmark -t set,get -n 100000 -c 50
```
