# KingbaseES 系统监控与告警指南

包括系统监控、性能监控、告警配置、监控工具和常见问题。

## 1. 监控概述

### 监控层次

| 层次 | 内容 | 工具 |
|------|------|------|
| 实例级 | CPU/内存/磁盘/网络 | 系统监控工具、Zabbix |
| 数据库级 | 连接数/事务/锁 | sys视图、KWR |
| 查询级 | 慢查询/执行计划 | sys_stat_statements、KSH |
| 业务级 | 自定义指标 | 应用埋点、KDDM |

### 监控目标

- **可用性**：实例运行状态、磁盘空间、连接数
- **性能**：响应时间、吞吐量、资源利用率
- **安全**：异常登录、权限变更、违规访问
- **容量**：存储增长趋势、连接趋势

## 2. KES 原生监控视图

### 系统视图速查

| 视图 | 用途 | 关键字段 |
|------|------|---------|
| `sys_stat_database` | 数据库级统计 | xact_commit, xact_rollback, blks_read, blks_hit, tup_returned, deadlocks |
| `sys_stat_activity` | 会话级活动 | pid, usename, datname, state, query, query_start, wait_event |
| `sys_stat_user_tables` | 用户表统计 | relname, seq_scan, idx_scan, n_live_tup, n_dead_tup |
| `sys_stat_user_indexes` | 用户索引统计 | indexrelname, idx_scan, idx_tup_read, idx_tup_fetch |
| `sys_stat_io_user_tables` | 表 I/O 统计 | heap_blks_read, heap_blks_hit, idx_blks_read, idx_blks_hit |
| `sys_stat_io_user_indexes` | 索引 I/O 统计 | idx_blks_read, idx_blks_hit |
| `sys_locks` | 锁信息 | pid, relation, mode, granted |
| `sys_stat_statements` | SQL 统计（需扩展） | query, calls, total_exec_time, mean_exec_time, rows |
| `sys_tablespace` | 表空间 | spcname, spclocation |
| `sys_stat_replication` | 复制状态 | client_addr, state, sent_lsn, replay_lsn, sync_state |
| `sys_replication_slots` | 复制槽 | slot_name, active, restart_lsn |
| `sys_kwr_snapshot` | KWR 快照 | snap_time, dbid, instance_number |

### 标准监控数据采集流程

```
1. 定义监控指标 -> 2. 选择数据源 -> 3. 配置采集频率 -> 4. 设置阈值 -> 5. 输出报告

数据源选择指南：
  +-- 实例级指标（CPU/内存/磁盘/网络） --> 系统命令 + /proc
  +-- 数据库级指标（连接/事务/锁/缓存） --> sys_stat_* 视图
  +-- SQL 级指标（慢查询/执行计划）     --> sys_stat_statements 扩展
  +-- 复制级指标（延迟/状态/槽）         --> sys_stat_replication + sys_replication_slots
  +-- 综合报告（AWR 类分析）             --> KWR (sys_wrsql)
  +-- 诊断采集（一次性全面检查）          --> KDDM (sys_diagnose)
```

### KWR 报告关联分析

KWR（Kingbase Workload Reporter）报告与系统监控视图的关联关系：

| KWR 报告模块 | 数据来源视图 | 关联分析 |
|-------------|-------------|---------|
| 负载概况 | `sys_stat_database`, `sys_stat_activity` | 对比 KWR 快照与实时统计，确认负载趋势 |
| 等待事件 | `sys_kwr_wait` | 与 `sys_stat_activity.wait_event` 交叉验证当前等待 |
| SQL 统计 | `sys_stat_statements` | KWR 提供时间段聚合，sys_stat_statements 提供实时 Top SQL |
| I/O 统计 | `sys_stat_io_user_tables` | KWR 快照间隔内的 I/O 变化量 vs 实时累积值 |
| 实例活动 | `sys_kwr_snapshot` | 时间线对照，确定问题发生的具体采样点 |

```sql
-- KWR 与 sys_stat_statements 关联查询示例
-- 找出 KWR 报告期间最耗时的 SQL
SELECT s.query, s.calls, s.total_exec_time
FROM sys_stat_statements s
ORDER BY s.total_exec_time DESC
LIMIT 20;

-- 确认 KWR 快照时间点
SELECT snap_time, snap_type
FROM sys_kwr_snapshot
ORDER BY snap_time DESC
LIMIT 10;
```

---

## 3. 系统监控

### 关键系统视图

```sql
-- 1. 数据库活动
SELECT
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM sys_stat_database
WHERE datname IS NOT NULL
ORDER BY xact_commit DESC;

-- 2. 缓存命中率
SELECT
    datname,
    CASE WHEN (blks_hit + blks_read) > 0
        THEN ROUND(blks_hit::DECIMAL / (blks_hit + blks_read) * 100, 2)
        ELSE 0
    END AS hit_ratio
FROM sys_stat_database
WHERE datname IS NOT NULL;

-- 3. 活跃会话
SELECT
    pid,
    usename,
    datname,
    client_addr,
    state,
    query_start,
    NOW() - query_start AS duration,
    LEFT(query, 100) AS query_preview
FROM sys_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

### 磁盘空间监控

```sql
-- 1. 表空间使用
SELECT
    spcname,
    sys_size_pretty(sys_tablespace_size(spcname)),
    sys_tablespace_size(spcname) AS size_bytes
FROM sys_tablespace
ORDER BY size_bytes DESC;

-- 2. 大表识别（前10）
SELECT
    relname,
    sys_size_pretty(sys_relation_size(relid)),
    sys_relation_size(relid) AS size_bytes,
    n_live_tup,
    n_dead_tup
FROM sys_stat_user_tables
ORDER BY size_bytes DESC
LIMIT 10;

-- 3. 索引大小
SELECT
    indexrelname,
    relname AS table_name,
    sys_size_pretty(sys_relation_size(i.indexrelid)),
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM sys_stat_user_indexes i
JOIN sys_indexes idx ON i.indexrelid = idx.indexrelid
ORDER BY sys_relation_size(i.indexrelid) DESC
LIMIT 10;

-- 4. WAL文件大小
SELECT
    sys_size_pretty(sys_current_wal_lsn()),
    sys_current_wal_lsn();
```

### 连接数监控

```sql
-- 1. 总连接数
SELECT count(*) AS total_connections FROM sys_stat_activity;

-- 2. 当前限制
SHOW max_connections;

-- 3. 按用户分布
SELECT usename, count(*) AS connections
FROM sys_stat_activity
GROUP BY usename
ORDER BY connections DESC;

-- 4. 按数据库分布
SELECT datname, count(*) AS connections
FROM sys_stat_activity
WHERE datname IS NOT NULL
GROUP BY datname
ORDER BY connections DESC;

-- 5. 空闲连接
SELECT count(*) FROM sys_stat_activity WHERE state = 'idle';

-- 6. 长时间运行查询
SELECT pid, usename, NOW() - query_start AS running_time, query
FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '5 minutes'
ORDER BY running_time DESC;
```

### 锁监控

```sql
-- 1. 活跃锁
SELECT
    pid,
    mode,
    granted,
    relation::regclass AS locked_table,
    a.usename,
    a.query
FROM sys_locks l
JOIN sys_stat_activity a ON l.pid = a.pid
WHERE NOT granted
ORDER BY a.query_start;

-- 2. 锁等待
SELECT
    blocked.pid AS blocked_pid,
    blocked.usename AS blocked_user,
    blocking.pid AS blocking_pid,
    blocking.usename AS blocking_user,
    NOW() - blocked.query_start AS wait_time,
    LEFT(blocked.query, 100) AS blocked_query,
    LEFT(blocking.query, 100) AS blocking_query
FROM sys_locks blocked_lock
JOIN sys_stat_activity blocked ON blocked_lock.pid = blocked.pid
JOIN sys_locks blocking_lock ON blocked_lock.relation = blocking_lock.relation
JOIN sys_stat_activity blocking ON blocking_lock.pid = blocking.pid
WHERE NOT blocked_lock.granted
  AND blocking_lock.granted;

-- 3. 终止阻塞会话
SELECT sys_terminate_pid(blocked_pid) FROM sys_locks WHERE NOT granted;
```

---

## 4. 性能监控

### sys_stat_statements

```sql
-- 1. 启用扩展
CREATE EXTENSION IF NOT EXISTS sys_stat_statements;

-- 2. 最耗时的查询（按总时间）
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows,
    shared_blks_hit,
    shared_blks_read
FROM sys_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 3. 平均耗时最高的查询
SELECT query, calls, mean_exec_time, rows
FROM sys_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;

-- 4. 调用频率最高的查询
SELECT query, calls, total_exec_time, mean_exec_time
FROM sys_stat_statements
ORDER BY calls DESC
LIMIT 20;

-- 5. 缓存命中率低的查询
SELECT
    query,
    calls,
    ROUND(shared_blks_hit::DECIMAL / NULLIF(shared_blks_hit + shared_blks_read, 0) * 100, 2) AS hit_ratio
FROM sys_stat_statements
WHERE shared_blks_read > 0
ORDER BY hit_ratio ASC
LIMIT 20;

-- 6. 重置统计
SELECT sys_stat_statements_reset();
```

### I/O监控

```sql
-- 1. 表I/O统计
SELECT
    relname,
    heap_blks_read,
    heap_blks_hit,
    idx_blks_read,
    idx_blks_hit,
    CASE WHEN (heap_blks_hit + heap_blks_read) > 0
        THEN ROUND(heap_blks_hit::DECIMAL / (heap_blks_hit + heap_blks_read) * 100, 2)
        ELSE 0
    END AS heap_hit_ratio
FROM sys_stat_io_user_tables
ORDER BY heap_blks_read DESC
LIMIT 20;

-- 2. 索引I/O统计
SELECT
    relname,
    indexrelname,
    idx_blks_read,
    idx_blks_hit,
    idx_scan
FROM sys_stat_io_user_indexes
WHERE idx_blks_read > 0
ORDER BY idx_blks_read DESC
LIMIT 20;

-- 3. 未使用的索引（零扫描）
SELECT
    relname,
    indexrelname,
    idx_scan,
    sys_size_pretty(sys_relation_size(indexrelid))
FROM sys_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY sys_relation_size(indexrelid) DESC;
```

### 慢查询追踪

```sql
-- 1. 启用慢查询日志
-- kingbase.conf
log_min_duration_statement = 1000    -- 毫秒，>1s记录
log_line_prefix = '%m [%p] %u@%d '   -- 时间戳 PID 用户@库

-- 2. 实时追踪
SELECT
    pid,
    usename,
    datname,
    NOW() - query_start AS duration,
    state,
    wait_event_type,
    wait_event,
    query
FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '30 seconds'
ORDER BY duration DESC;

-- 3. 终止慢查询
SELECT sys_cancel_pid(pid) FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '5 minutes';
```

### 事务监控

```sql
-- 1. 事务统计
SELECT
    datname,
    xact_commit AS commits,
    xact_rollback AS rollbacks,
    deadlocks,
    conflicts
FROM sys_stat_database
WHERE datname IS NOT NULL;

-- 2. 长事务
SELECT
    pid,
    usename,
    xact_start,
    NOW() - xact_start AS duration,
    query
FROM sys_stat_activity
WHERE xact_start IS NOT NULL
  AND NOW() - xact_start > INTERVAL '5 minutes'
ORDER BY duration DESC;

-- 3. 死锁检测
SELECT count(*) AS deadlock_count FROM sys_stat_database WHERE deadlocks > 0;
```

---

## 5. 监控工具

### KWR (Kingbase Workload Reporter)

```bash
# 1. 启用KWR
ALTER SYSTEM SET kwr_enabled = on;
ALTER SYSTEM SET kwr_interval = 300;      -- 采样间隔(秒)
ALTER SYSTEM SET kwr_duration = 3600;     -- 报告时长(秒)
SELECT sys_reload_conf();

# 2. 生成报告
sys_wrsql -f /path/to/report.html

# 3. 查看快照
SELECT * FROM sys_kwr_snapshot ORDER BY snap_time DESC LIMIT 10;

# 4. 查看等待事件
SELECT * FROM sys_kwr_wait ORDER BY wait_time DESC;
```

### KDDM (Kingbase Data Diagnostic Monitor)

```bash
# 1. 启动诊断
sys_diagnose -h localhost -p 54321 -U SYSTEM -d test -o /path/to/diagnostic

# 2. 采集信息包括
# - 系统配置
# - 性能统计
# - 锁信息
# - 慢查询
# - 表空间使用

# 3. 定期采集
# 添加到cron
0 */4 * * * sys_diagnose -h localhost -p 54321 -U SYSTEM -d test -o /var/log/kddm/$(date +\%Y\%m\%d_\%H)
```

### KSH (Kingbase SQL Health)

```bash
# 1. SQL健康检查
sys_sqlhealth -h localhost -p 54321 -U SYSTEM -d test \
    --sql "SELECT * FROM large_table WHERE name = 'test'" \
    -o /path/to/analysis.html

# 2. 批量SQL分析
sys_sqlhealth --batch /path/to/sql_list.txt -o /path/to/report/

# 3. 分析内容
# - 执行计划分析
# - 索引使用检查
# - 统计信息检查
# - 改写建议
```

---

## 6. 告警配置

### 告警指标

| 指标 | 警告阈值 | 严重阈值 | 检查频率 |
|------|---------|---------|---------|
| 磁盘使用率 | > 80% | > 90% | 5分钟 |
| 连接数使用率 | > 70% | > 90% | 1分钟 |
| 缓存命中率 | < 90% | < 80% | 5分钟 |
| 复制延迟 | > 10s | > 30s | 10秒 |
| 活跃锁等待 | > 5 | > 20 | 30秒 |
| 死锁计数 | > 0 | > 3/h | 持续 |
| 慢查询数 | > 10/min | > 50/min | 1分钟 |
| WAL增长 | > 1GB/h | > 5GB/h | 10分钟 |

### 告警脚本

```bash
#!/bin/bash
# /opt/kingbase/bin/alert_monitor.sh
# 综合告警监控脚本

DB_HOST="localhost"
DB_PORT="54321"
DB_USER="SYSTEM"
DB_NAME="test"
ALERT_EMAIL="dba@company.com"
LOG_FILE="/var/log/kingbase/alert.log"

send_alert() {
    local level=$1
    local message=$2
    echo "$(date +'%Y-%m-%d %H:%M:%S') [$level] $message" >> "$LOG_FILE"
    echo "$message" | mail -s "KES Alert [$level]" "$ALERT_EMAIL"
}

# 1. 实例可达性检查
if ! sys_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; then
    send_alert "CRITICAL" "Database instance is not responding!"
    exit 1
fi

# 2. 磁盘空间检查
USAGE=$(df -h /data/kingbase | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
    send_alert "CRITICAL" "Disk usage critical: ${USAGE}%"
elif [ "$USAGE" -gt 80 ]; then
    send_alert "WARNING" "Disk usage high: ${USAGE}%"
fi

# 3. 连接数检查
CONN_COUNT=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT count(*) FROM sys_stat_activity")
MAX_CONN=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "SHOW max_connections")
CONN_RATIO=$((CONN_COUNT * 100 / MAX_CONN))
if [ "$CONN_RATIO" -gt 90 ]; then
    send_alert "CRITICAL" "Connection usage: ${CONN_COUNT}/${MAX_CONN} (${CONN_RATIO}%)"
elif [ "$CONN_RATIO" -gt 70 ]; then
    send_alert "WARNING" "Connection usage: ${CONN_COUNT}/${MAX_CONN} (${CONN_RATIO}%)"
fi

# 4. 缓存命中率检查
HIT_RATIO=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "
    SELECT ROUND(sum(blks_hit)::DECIMAL / NULLIF(sum(blks_hit + blks_read), 0) * 100, 0)
    FROM sys_stat_database WHERE datname IS NOT NULL")
if [ "${HIT_RATIO%%.*}" -lt 80 ]; then
    send_alert "CRITICAL" "Cache hit ratio critical: ${HIT_RATIO}%"
elif [ "${HIT_RATIO%%.*}" -lt 90 ]; then
    send_alert "WARNING" "Cache hit ratio low: ${HIT_RATIO}%"
fi

# 5. 死锁检查
DEADLOCKS=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "
    SELECT sum(deadlocks) FROM sys_stat_database WHERE datname IS NOT NULL")
if [ "$DEADLOCKS" -gt 0 ]; then
    send_alert "WARNING" "Deadlocks detected: ${DEADLOCKS}"
fi

# 6. 锁等待检查
LOCK_WAIT=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "
    SELECT count(*) FROM sys_locks WHERE NOT granted")
if [ "$LOCK_WAIT" -gt 20 ]; then
    send_alert "CRITICAL" "Lock wait count critical: ${LOCK_WAIT}"
elif [ "$LOCK_WAIT" -gt 5 ]; then
    send_alert "WARNING" "Lock wait count high: ${LOCK_WAIT}"
fi

# 7. 慢查询检查
SLOW_QUERIES=$(ksql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "
    SELECT count(*) FROM sys_stat_activity
    WHERE state = 'active'
      AND NOW() - query_start > INTERVAL '30 seconds'")
if [ "$SLOW_QUERIES" -gt 0 ]; then
    send_alert "WARNING" "Slow queries running: ${SLOW_QUERIES}"
fi

echo "$(date +'%Y-%m-%d %H:%M:%S') [INFO] Monitoring check completed" >> "$LOG_FILE"
```

### Cron定时任务

```bash
# /etc/cron.d/kingbase-monitor
# 每分钟检查实例状态
*/1 * * * * root /opt/kingbase/bin/alert_monitor.sh

# 每5分钟深度检查
*/5 * * * * root /opt/kingbase/bin/deep_monitor.sh

# 每小时生成KWR报告
0 * * * * kingbase sys_wrsql -f /var/log/kingbase/kwr/$(date +\%Y\%m\%d_\%H).html

# 每天凌晨采集诊断信息
0 2 * * * kingbase sys_diagnose -h localhost -p 54321 -U SYSTEM -d test -o /var/log/kddm/$(date +\%Y\%m\%d)
```

---

## 7. 集成监控

### Prometheus + Grafana

```yaml
# kingbase_exporter配置
# kingbase_exporter.yaml
databases:
  - host: localhost
    port: 54321
    user: monitor_user
    password: "monitor_pass"
    dbname: test
    metrics:
      - stat_activity
      - stat_database
      - stat_statements
      - stat_tables
      - bgwriter
      - settings
```

```bash
# 启动exporter
kingbase_exporter --config.kingbase kingbase_exporter.yaml --web.listen-address=":9187"
```

```promql
# PromQL示例
# 连接数使用率
kingbase_stat_activity_count / kingbase_settings_max_connections * 100

# 缓存命中率
kingbase_stat_database_blks_hit / (kingbase_stat_database_blks_hit + kingbase_stat_database_blks_read) * 100

# 活跃查询数
kingbase_stat_activity_count{state="active"}

# 锁等待数
kingbase_locks_count{granted="false"}
```

### Zabbix集成

```xml
<!-- zabbix_kingbase_template.xml -->
<!-- 自定义UserParameter -->
<!-- /etc/zabbix/zabbix_agentd.d/kingbase.conf -->
```

```bash
# UserParameter配置
UserParameter=kingbase.ping,sys_isready -h localhost -p 54321 2>&1 | grep -c "accepting connections"
UserParameter=kingbase.connections,ksql -U SYSTEM -tAc "SELECT count(*) FROM sys_stat_activity"
UserParameter=kingbase.hit_ratio,ksql -U SYSTEM -tAc "SELECT ROUND(sum(blks_hit)::DECIMAL/NULLIF(sum(blks_hit+blks_read),0)*100,0) FROM sys_stat_database WHERE datname IS NOT NULL"
UserParameter=kingbase.deadlocks,ksql -U SYSTEM -tAc "SELECT sum(deadlocks)::int FROM sys_stat_database"
UserParameter=kingbase.table_space_usage,*,-tAc "SELECT sys_tablespace_size('sys_default')"
```

---

## 8. 监控仪表盘

### 核心仪表盘布局

```
┌─────────────────────────────────────────────────────────┐
│ 实例状态    连接数: 150/300   运行时间: 30d   磁盘: 65%  │
├──────────────┬──────────────┬──────────────────────────┤
│ QPS趋势      │ TPS趋势      │ 缓存命中率               │
│ (实时折线)   │ (实时折线)   │ (仪表盘 95%)            │
├──────────────┼──────────────┼──────────────────────────┤
│ Top 10慢查询 │ Top 10大表   │ 锁等待                   │
│ (查询/耗时)  │ (表名/大小)   │ (PID/等待时间/SQL)       │
├──────────────┴──────────────┴──────────────────────────┤
│ 复制延迟    WAL速率    事务提交/回滚    死锁计数         │
└─────────────────────────────────────────────────────────┘
```

### 关键SQL汇总

```sql
-- 仪表盘汇总查询
SELECT
    (SELECT count(*) FROM sys_stat_activity) AS connections,
    (SELECT extract(epoch FROM NOW() - sys_postmaster_start_time()))::int AS uptime_seconds,
    (SELECT round(sum(xact_commit) + sum(xact_rollback)) FROM sys_stat_database) AS total_txns,
    (SELECT round(sum(blks_hit)::DECIMAL / NULLIF(sum(blks_hit + blks_read), 0) * 100, 2)
     FROM sys_stat_database WHERE datname IS NOT NULL) AS hit_ratio,
    (SELECT sum(deadlocks)::int FROM sys_stat_database) AS deadlocks,
    (SELECT count(*) FROM sys_locks WHERE NOT granted) AS lock_waits,
    (SELECT count(*) FROM sys_stat_activity WHERE state = 'active') AS active_queries;
```

---

## 9. 常见问题

### 问题1：监控数据不准确

**排查**：
```sql
-- 1. 检查统计收集器
SHOW stats;

-- 2. 重置统计（基准测试时）
SELECT sys_stat_reset();

-- 3. 检查采样间隔
SHOW kwr_interval;
```

### 问题2：告警脚本无法连接

**排查**：
```bash
# 1. 检查PGPASSFILE
echo "localhost:54321:SYSTEM:alert_user:password" > ~/.pgpass
chmod 600 ~/.pgpass

# 2. 或使用sys_hba.conf本地信任
# local all alert_user trust
```

### 问题3：监控性能开销过大

**解决**：
```sql
-- 1. 调整KWR采样间隔
ALTER SYSTEM SET kwr_interval = 600;  -- 增大到10分钟

-- 2. 限制sys_stat_statements
ALTER SYSTEM SET sys_stat_statements.max = 5000;
ALTER SYSTEM SET sys_stat_statements.track = top;  -- 只追踪顶层

-- 3. 关闭不必要的日志
ALTER SYSTEM SET log_min_duration_statement = 5000;  -- 只记录>5s
```

---

## 最佳实践

1. **分层监控**：系统 → 实例 → 查询 → 业务四层覆盖
2. **告警分级**：Warning（邮件）/ Critical（短信+电话）
3. **定期巡检**：每日自动报告 + 每周人工审查
4. **基线建立**：记录正常时期的指标作为对比基准
5. **容量规划**：跟踪增长趋势，提前3个月预警
6. **日志轮转**：监控日志定期清理，保留90天
7. **告警收敛**：避免告警风暴，设置静默期
