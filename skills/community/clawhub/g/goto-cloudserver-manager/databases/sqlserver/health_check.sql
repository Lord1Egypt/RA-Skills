-- SQL Server 健康检查查询集
-- 输出各项健康指标，供 report_generator.py 解析

PRINT N'===== SQL Server 健康检查 =====';
PRINT N'时间：' + CONVERT(NVARCHAR, GETDATE(), 120);

-- 版本信息
PRINT N'';
PRINT N'----- 版本信息 -----';
SELECT @@SERVERNAME AS 服务器名, @@VERSION AS 版本;

-- 数据库列表及状态
PRINT N'';
PRINT N'----- 数据库状态 -----';
SELECT
    name AS 数据库名,
    state_desc AS 状态,
    recovery_model_desc AS 恢复模式,
    CONVERT(DECIMAL(10,2), SUM(size) * 8.0 / 1024) AS 大小MB
FROM sys.databases d
LEFT JOIN sys.master_files f ON d.database_id = f.database_id
WHERE name NOT IN ('master','model','msdb','tempdb')
GROUP BY name, state_desc, recovery_model_desc
ORDER BY name;

-- 连接数
PRINT N'';
PRINT N'----- 当前连接数 -----';
SELECT
    DB_NAME(database_id) AS 数据库,
    COUNT(*) AS 连接数
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
GROUP BY database_id
ORDER BY 连接数 DESC;

-- 慢查询（最近 1 小时，执行时间 > 5 秒）
PRINT N'';
PRINT N'----- 慢查询（>5秒，最近10条）-----';
SELECT TOP 10
    total_elapsed_time / 1000 AS 总耗时ms,
    execution_count AS 执行次数,
    SUBSTRING(st.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(st.text)
         ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS SQL语句
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
WHERE total_elapsed_time / 1000 > 5000
ORDER BY total_elapsed_time DESC;

-- 磁盘 IO 等待
PRINT N'';
PRINT N'----- IO 等待统计 -----';
SELECT TOP 10
    wait_type AS 等待类型,
    waiting_tasks_count AS 等待任务数,
    wait_time_ms AS 等待时间ms,
    signal_wait_time_ms AS 信号等待ms
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'SLEEP_TASK','BROKER_TO_FLUSH','BROKER_TASK_STOP',
    'CLR_AUTO_EVENT','DISPATCHER_QUEUE_SEMAPHORE','FT_IFTS_SCHEDULER_IDLE_WAIT',
    'HADR_WORK_QUEUE','LAZYWRITER_SLEEP','ONDEMAND_TASK_QUEUE',
    'REQUEST_FOR_DEADLOCK_SEARCH','RESOURCE_QUEUE','SERVER_IDLE_CHECK',
    'SLEEP_DBSTARTUP','SLEEP_DCOMSTARTUP','SLEEP_MASTERDBREADY',
    'SLEEP_MASTERMDREADY','SLEEP_MASTERUPGRADED','SLEEP_MSDBSTARTUP',
    'SLEEP_SYSTEMTASK','SLEEP_TEMPDBSTARTUP','SNI_HTTP_ACCEPT',
    'SP_SERVER_DIAGNOSTICS_SLEEP','SQLTRACE_BUFFER_FLUSH','WAITFOR',
    'XE_DISPATCHER_WAIT','XE_TIMER_EVENT'
)
ORDER BY wait_time_ms DESC;

PRINT N'';
PRINT N'===== 健康检查完成 =====';
