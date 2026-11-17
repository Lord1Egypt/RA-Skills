# KingbaseES 动态性能视图与日志分析

## 性能调优工具概述

KingbaseES 提供了一套全面的性能调优工具，协同工作以捕获、分析和报告数据库性能指标。

**工具生态系统**

1. **kbbadger** -- 基于日志的性能分析，从数据库日志文件中提取数据
2. **动态性能视图** -- SQL 执行、等待事件和 IO 的实时与累积统计
3. **KWR 快照** -- 按时间间隔自动采集动态视图数据
4. **KWR 报告** -- 基于数据库时间模型的多维度性能分析
5. **KDDM 报告** -- 自动化诊断和优化建议
6. **KWR DIFF 报告** -- 两组 KWR 快照之间的对比分析
7. **KSH 报告** -- 基于采样的活跃会话历史统计

此外，操作系统级工具（火焰图、top、free、iostat）可配合这些数据库工具进行系统资源分析。

## kbbadger 日志分析工具

### 工具简介

kbbadger 是一个命令行工具，用于分析 KingbaseES 运行期间产生的大型日志文件，并生成图形化的 HTML 性能报告。它解析数据库日志以提取连接、会话、检查点、临时文件、VACUUM 操作、锁、查询和事件的统计数据。

### 支持的日志格式

- stderr（kbbadger 默认格式）
- syslog
- CSV log
- JSON log

### 必需的日志配置

在 kingbase.conf 中设置以下参数以启用 kbbadger 兼容的日志：

```sql
log_min_duration_statement = 0
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,remote=%h '
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
lc_messages = 'en_US.UTF-8'
```

### 生成报告

```shell
kbbadger ./sys_log/kingbase* -f stderr -J 12 -j 32
```

参数说明：
- `-f stderr` -- 日志格式（stderr、syslog、csvlog、json）
- `-J 12` -- 初始解析使用的进程数
- `-j 32` -- 报告生成使用的进程数

输出：当前目录下的 `out.html`。

### 报告内容

**摘要部分：**
- 整体统计
- 持续时间最长的查询（Top 查询）
- 频率最高的查询
- 频率最高的错误
- 查询时间直方图
- 会话时间直方图
- 查询用户和应用程序排行
- 被取消的查询
- 代价最高的 prepare/bind 查询

**每小时时间图表：**
- SQL 查询统计
- 临时文件使用情况
- 检查点统计
- Autovacuum 和 Autoanalyze 统计
- 被取消的查询
- 错误事件（panic、fatal、error、warning）
- 错误类别分布

### 何时使用 kbbadger

kbbadger 适用于以下场景：
- KWR 不可用（旧版本 KingbaseES 不支持 KWR）
- 需要跨环境通用的日志分析
- 希望从现有日志数据生成可视化 HTML 报告

注意事项：生成详细日志会增加 sys_log 磁盘消耗并影响服务器性能。分析完成后应关闭日志追踪。

## 动态性能视图

动态性能视图以哈希表和动态数组的形式呈现存在于共享内存或本地内存中的统计数据（等待事件、IO 操作、SQL 执行），而非以传统关系表存储。数据由 GUC 参数控制，通过 SQL 函数进行管理。

### 分类

**按统计范围划分：**
- **实例级** -- 所有数据库中数据相同（如 `sys_stat_transaction`、`sys_stat_instio`）。通过 `SELECT sys_stat_reset_shared('all')` 重置
- **当前数据库级** -- 对象级统计仅限定于当前连接的数据库（如表、索引、函数）。通过 `SELECT sys_stat_reset()` 重置

**按时间维度划分：**
- **实时** -- 反映当前会话和任务的状态（如 `sys_stat_activity`）。通常不可重置
- **累积** -- 随时间累积，在 DATA/sys_stat 中跨重启持久化。可通过 SQL 函数重置

### 第一类：实时状态视图

| 视图 | 说明 |
|------|------|
| `sys_stat_activity` | 每个服务器进程一行：状态、等待事件、当前查询、后端类型 |
| `sys_stat_gssapi` | 每个连接的 GSSAPI 认证和加密信息 |
| `sys_stat_ssl` | 每个连接的 SSL 信息 |
| `sys_stat_subscription` | 订阅工作进程信息 |
| `sys_stat_progress_cluster` | CLUSTER 或 VACUUM FULL 的进度 |
| `sys_stat_progress_create_index` | CREATE INDEX 或 REINDEX 的进度 |
| `sys_stat_progress_vacuum` | VACUUM（包括 autovacuum）的进度 |
| `sys_stat_replication` | WAL 发送和备库复制统计 |
| `sys_stat_wal_buffer` | WAL 缓冲区实时操作统计 |
| `sys_stat_wal_receiver` | WAL 接收连接统计 |

**实时 TPS/QPS 视图：**
| 视图 | 说明 |
|------|------|
| `sys_stat_metric` | 实时 TPS 和 QPS 结果 |
| `sys_stat_metric_history` | 最近一小时的指标数据（15 秒间隔） |
| `sys_stat_sysmetric` | 系统级实时指标 |
| `sys_stat_sysmetric_summary` | 系统级聚合指标（最大、最小、平均） |

**关键 GUC 参数：**
- `track_activities = on`（默认）-- 启用 `sys_stat_activity` 和进度视图
- `track_activity_query_size = 1024` -- sys_stat_activity 中 query 字段的最大长度
- `track_real_stats = off`（默认）-- 启用实时 TPS/QPS 视图

### 第二类：实例级统计视图

| 视图 | 说明 |
|------|------|
| `sys_stat_archiver` | WAL 归档进程活动 |
| `sys_stat_bgwriter` | 后台写进程活动（检查点、写入缓冲区） |
| `sys_stat_database` | 每个数据库的统计：连接、事务、元组 |
| `sys_stat_database_conflicts` | 因备库冲突而取消的查询 |
| `sys_stat_sqlcount` | 按类型（DML/DCL/DDL/TCL）统计的 SQL 语句计数 |
| `sys_stat_dmlcount` | DML 语句计数和时间 |
| `sys_stat_transaction` | 事务计数统计 |
| `sys_stat_shmem` | 共享内存分配统计 |
| `sys_stat_cached_plans` | 执行计划缓存统计 |
| `sys_stat_pre_archivewal` | 预归档 WAL 日志信息 |

这些视图持续更新，无需 GUC 参数控制。

### 第三类：对象级统计视图

统计范围仅限当前数据库，不能跨数据库。

| 视图 | 说明 |
|------|------|
| `sys_stat_all_tables` | 所有表的访问统计（顺序扫描、索引扫描、元组） |
| `sys_stat_user_tables` | 同上，仅限用户表 |
| `sys_stat_all_indexes` | 所有索引的访问统计 |
| `sys_stat_user_indexes` | 同上，仅限用户索引 |
| `sys_stat_user_functions` | 每个被追踪函数的执行次数和时间 |
| `sys_stat_xact_all_tables` | 与 all_tables 相同，但作用域为当前事务 |
| `sys_statio_all_tables` | 每个表的 IO 统计（命中、读取、写入） |
| `sys_statio_all_indexes` | 每个索引的 IO 统计 |
| `sys_statio_all_sequences` | 每个序列的 IO 统计 |

重置：`SELECT sys_stat_reset()`（所有对象），`SELECT sys_stat_reset_single_table_counters(OID)`（单个对象）

**关键 GUC 参数：**
- `track_counts = on`（默认）-- 启用对象统计；autovacuum 需要此功能
- `track_io_timing = off`（默认）-- 在块读写时间字段中记录 IO 计时
- `track_functions = 'none'`（默认）-- 设置为 'pl' 或 'all' 以追踪函数统计
- `stats_temp_directory` -- 统计文件路径（默认 DATA/sys_stat_tmp）；建议使用 tmpfs 以降低 IO

### 第四类：时间模型视图

KWR 报告的核心数据源。从多个维度分解数据库时间。

| 视图 | 说明 |
|------|------|
| `sys_stat_sqltime` | SQL 消息统计（Parse、Bind、Execute、Describe、Sync、Flush） |
| `sys_stat_sqlwait` | 与 SQL 语句关联的等待事件 |
| `sys_stat_sqlio` | 每个 SQL 语句的 IO 块和时间 |
| `sys_stat_instevent` | 关键实例活动（Buffer、Executor、Lock、Transaction、WAL 等） |
| `sys_stat_instio` | 实例级 IO 统计 |
| `sys_stat_instlock` | 实例级轻量级锁统计 |
| `sys_stat_dbtime` | 数据库时间模型，基本时间分解 |
| `sys_stat_wait` | 数据库时间模型，按等待事件分解 |
| `sys_stat_sql` | 数据库时间模型，按 SQL 语句分解 |
| `sys_stat_msgaccum` | 与 sys_stat_sqltime 相同，已废弃 |
| `sys_stat_waitaccum` | 与 sys_stat_sqlwait 相同，已废弃 |

**关键 GUC 参数：**
- `track_sql = off`（默认）-- 启用 sqltime、sqlwait、sqlio 追踪
- `track_sql_item = 'sqltime, sqlwait, sqlio'` -- 建议不包含 queryid，以避免统计膨胀
- `track_instance = off`（默认）-- 启用 instevent、instio、instlock 追踪
- `track_instance_item = 'instevent, instio, instlock'` -- 建议使用默认粒度

### 第五类：TOP SQL 视图

| 视图 | 说明 |
|------|------|
| `sys_stat_statements` | 顶层 SQL 语句统计（解析、计划、执行时间、IO） |
| `sys_stat_statements_all` | 所有 SQL，包括嵌套子语句 |

**关键 GUC 参数：**
- `sys_stat_statements.track = 'none'`（默认）-- 设置为 'top' 用于常规使用，'all' 用于 PLSQL 调试
- `sys_stat_statements.max = 5000` -- 容量不足时增加至 10000-20000
- `sys_stat_statements.track_utility = on` -- 如实用语句占比过高（>30%）可关闭
- `sys_stat_statements.track_parse = on` -- 包含解析时间追踪
- `sys_stat_statements.track_plan = on` -- 包含计划时间追踪
- `sys_stat_statements.save = on` -- 重启后持久化统计

重置：`SELECT sys_stat_statements_reset()`

### 第六类：主机信息视图

主机指标通过 `perf` 模式下的 SQL 函数访问（需要 `sys_kwr` 扩展）：

| 函数 | 说明 |
|----------|-------------|
| `perf.sys_cpu_stats_info()` | CPU 使用信息 |
| `perf.sys_load_avg_info()` | CPU 负载平均值 |
| `perf.sys_cpu_stat_by_process(int pid)` | 特定进程的 CPU 统计 |
| `perf.sys_io_stat_info()` | 磁盘设备 IO 统计 |
| `perf.sys_io_stat_byprocess(int pid)` | 特定进程的 IO 统计 |
| `perf.sys_memory_info()` | 主机内存和交换分区统计 |
| `perf.sys_mempage_stat_byprocess(int pid)` | 特定进程的内存统计 |
| `perf.sys_network_info()` | 网络流量统计 |

示例：
```sql
SELECT total_memory, used_memory, free_memory, swap_total, swap_used, swap_free
FROM perf.sys_memory_info();
```

## 管理动态性能视图

### 启用所有统计

用于全面的性能数据采集：
```
track_activities = on
track_counts = on
track_functions = 'all'
track_sql = on
track_instance = on
track_io_timing = on
sys_stat_statements.track = 'all'
```

### 禁用所有统计

用于追求最大性能、零开销的场景：
```
track_activities = off
track_counts = off
track_functions = 'none'
track_sql = off
track_instance = off
track_io_timing = off
sys_stat_statements.track = 'none'
```

### 无需重启应用配置

```sql
ALTER SYSTEM SET track_sql TO on;
SELECT sys_reload_conf();
```

### 重置统计

```sql
SELECT sys_stat_reset_shared('all');    -- 所有共享对象统计
SELECT sys_stat_reset();                 -- 当前数据库对象统计
SELECT sys_stat_statements_reset();      -- 所有 SQL 语句统计
```

## 常见问题

**kbbadger 日志格式不匹配**：确保 `log_line_prefix` 符合 kbbadger 预期。对默认 KingbaseES 日志格式使用 `-f stderr`。

**动态视图无数据**：验证对应的 `track_*` GUC 参数是否已启用。例如 `sys_stat_statements` 需要 `sys_stat_statements.track = 'top'` 或 `'all'`。

**KWR 报告缺少时间模型数据**：在快照采集前启用 `track_sql = on` 和 `track_instance = on`。

**统计信息膨胀**：设置 `track_sql_item = 'sqltime, sqlwait, sqlio'` 而不带 `_queryid` 后缀，以避免按 queryid 追踪。

**sys_stat_statements 占用内存过高**：仅在必要时增加 `sys_stat_statements.max`；或者禁用实用语句追踪以保留更多 DML 条目。

## 最佳实践

1. 在生产系统上使用 KWR/KDDM 时启用 `track_sql` 和 `track_instance`
2. 默认使用 `sys_stat_statements.track = 'top'`；仅在深度 PLSQL 分析时切换为 `'all'`
3. 批量数据加载后运行 `ANALYZE`，保持优化器统计信息最新
4. KWR 不可用时使用 kbbadger，或进行离线日志分析
5. 性能分析完成后禁用所有追踪功能以降低开销
6. 需要 IO 性能分析时设置 `track_io_timing = on`
