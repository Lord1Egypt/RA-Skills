-- PostgreSQL 健康检查
\echo '===== PostgreSQL 健康检查 ====='
\echo ''

-- 版本
SELECT version() AS pg_version;

-- 数据库列表及大小
SELECT
    datname AS 数据库,
    pg_size_pretty(pg_database_size(datname)) AS 大小,
    numbackends AS 当前连接数
FROM pg_database
WHERE datname NOT IN ('template0', 'template1')
ORDER BY pg_database_size(datname) DESC;

-- 连接统计
SELECT
    state AS 状态,
    COUNT(*) AS 数量
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY state;

-- 长时间运行的查询（> 30 秒）
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '30 seconds'
  AND state <> 'idle';

-- 表膨胀检查（前10大表）
SELECT
    schemaname || '.' || tablename AS 表名,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS 总大小
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 10;

\echo ''
\echo '===== 健康检查完成 ====='
