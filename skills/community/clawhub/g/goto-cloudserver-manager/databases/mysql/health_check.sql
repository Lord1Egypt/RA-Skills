-- MySQL 健康检查
SELECT 'MySQL 健康检查' AS 标题, NOW() AS 检查时间;

-- 版本
SELECT VERSION() AS MySQL版本;

-- 连接数
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
SHOW VARIABLES LIKE 'max_connections';

-- 慢查询
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 缓存命中率
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_reads';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read_requests';

-- 数据库列表及大小
SELECT
    table_schema AS 数据库,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 大小MB
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema','performance_schema','mysql','sys')
GROUP BY table_schema
ORDER BY 大小MB DESC;
