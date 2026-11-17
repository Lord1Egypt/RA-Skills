# KingbaseES 性能报告（KWR/KDDM/KSH）

## KWR 快照

### 概述

KWR 快照记录两个时间点之间动态性能视图数据的差异，保存历史统计数据。`kwr collector` 后台进程按可配置的时间间隔（默认：每小时）自动创建快照。快照默认保留 8 天，之后在创建新快照时自动清理。

快照是 KWR 报告、KDDM 报告和 KWR DIFF 报告的数据基础。

### 创建 sys_kwr 扩展

```sql
\c benchmarksql
CREATE EXTENSION sys_kwr;
```

这将创建 `perf.*` 表，包括 `kwr_snapshots`、`ksh_history_data` 和各种快照数据表。连接到创建扩展的数据库即可查看快照和生成报告。

### 推荐的 GUC 配置

在 kingbase.conf 中：
```
track_counts = on
track_io_timing = on
track_functions = 'all'
track_sql = on
track_instance = on
track_sql_item = 'sqltime, sqlwait, sqlio'
track_instance_item = 'instevent, instio, instlock'
sys_stat_statements.track = 'top'
```

### 自动快照采集

```
sys_kwr.enable = on
sys_kwr.interval = 60        # 快照间隔（分钟），默认 60
```

KingbaseES 启动时会检查 `sys_kwr` 扩展。如果不存在，会自动创建一个。

### 手动创建快照

```sql
SELECT perf.create_snapshot();
```

### 查看和清理快照

```sql
SELECT snap_id, sess_count FROM perf.kwr_snapshots;
```

清理所有快照：
```sql
SELECT perf.reset_snapshots();
```

或重新创建扩展：
```sql
DROP EXTENSION sys_kwr;
CREATE EXTENSION sys_kwr;
```

## 生成 KWR 报告

### 报告函数

```sql
-- 在快照 1 和 2 之间生成 KWR 报告
SELECT * FROM perf.kwr_report(1, 2, 'html');

-- 生成 KWR DIFF 报告，对比快照对 (1,2) 与 (3,4)
SELECT * FROM perf.kwr_diff_report(1, 2, 3, 4);
SELECT * FROM perf.kwr_diff_report_to_file(1, 2, 3, 4, 'diff.html');

-- 生成 KDDM 报告
SELECT * FROM perf.kddm_report(1, 2);

-- 为特定 queryid 生成 KDDM SQL 报告
SELECT * FROM perf.kddm_sql_report(1, 2, 3278935302158814650);
```

## KWR 数据库时间模型

数据库时间（DB Time）= 非空闲等待时间 + CPU 时间。时间模型从六个维度分解 DB Time。

### 按 SQL 消息分解

客户端 SQL 语句通过两种协议发送：
- **简单协议（Q 消息）** -- 发送原始 SQL 直接执行
- **扩展协议（P/B/D/E/S 消息）** -- Parse、Bind、Describe、Execute、Sync，使用绑定变量

KWR 按消息类型追踪时间：Simple、Parse、Bind、Execute、Sync、Flush、Describe、Fastpath、Wait、Close。

### 按 SQL 语句类型分解

类别：DML（SELECT、UPDATE、INSERT、DELETE、MERGE）、DDL、DCL、TCL、其他。识别哪些语句类型消耗最多数据库时间。

### 按等待事件分解

当等待事件超过总 DB Time 的 5% 时，表明存在性能瓶颈。分解显示哪些等待事件（如 WALWriteLock、DataFileRead、extend）占主导地位。

### 按关键活动分解

预定义活动的累积统计（比基于采样的火焰图更精确）：
- Buffer -- 内存缓冲区操作
- Executor -- 查询执行器操作
- Lock -- 对象锁操作
- Maintenance -- 索引创建和其他维护
- SMGR -- 存储管理器操作
- Transaction -- 提交、中止操作
- WAL -- WAL 日志操作
- Checkpoint -- 检查点操作
- Misc -- 登录、登出等

### 按 SQL 执行阶段分解

阶段：Parse、Analyze、Rewrite、Plan、Initialize Plan、Execute、Commit Transaction。

### 按 TOP SQL 分解

基于 `sys_stat_statements`。子报告包括：
- 按数据库时间、CPU 时间、解析时间、计划时间、执行时间排序的 SQL
- 按执行次数、返回元组数排序的 SQL
- 按 IO 时间、逻辑读、物理读、逻辑写、物理写排序的 SQL
- 按临时块、本地数据块排序的 SQL
- 完整 SQL 列表

KDDM 额外显示 PLSQL 语句的父子调用层级关系。

## KWR 其他性能指标

### 快照时间（经过时间）

两个快照之间的时间间隔。用于计算实例级统计的每秒值。

**推导 TPS 和 QPS：**
- QPS = Execute Calls / 快照时间（秒）
- TPS = Transactions / 快照时间（秒）

### 实例效率百分比

目标为 100% 的指标（低于 90% 表示潜在问题）：

**Buffer 命中率：**
```
(Shared and local block Hits * 100.00) / (Hits + Reads)
```

**解析复用率：**
```
(1 - Parse Calls / Execute Calls) * 100.00
```

**计划复用率：**
```
(1 - Plan Calls / Execute Calls) * 100.00
```

**计划缓存命中率：**
```
Soft Parses * 100.00 / (Soft Parses + Hard Parses)
```

### IO 性能指标

四个分析层级：

1. **主机 IO** -- 机器宏观磁盘 IO。使用 `show data_directory` 定位数据目录，然后用 `df` 和 `lsblk` 识别设备。

2. **实例 IO** -- 来自 IO 类等待事件，按进程类型、文件类型、数据库名、表空间和对象类型细分。数据来源：`kwr_snap_inst_io`。

3. **SQL 级 IO** -- 每个 SQL 语句的共享块、本地块和临时块读写，以及 WAL 读写。数据来源：`kwr_snap_sql_io`。

4. **数据库对象 IO** -- 每个表和索引的物理读、逻辑读（命中）和缓存命中率。

### 内存统计

- **主机内存** -- 快照开始和结束时的总内存、已用内存和空闲内存
- **数据库内存** -- 主机上共享内存占比
- **Top 10 共享内存** -- KingbaseES 共享内存使用分解

### 数据库对象指标

仅针对当前数据库的报告（其他所有 KWR 指标均为实例级）：
- 按顺序扫描页数、逻辑读、物理读、DML 行数、命中率排序的表
- 按逻辑读、物理读、命中排序的索引
- 未使用的索引
- 按执行时间和次数排序的函数

## KDDM 报告

KDDM（KingbaseES 数据库诊断监控器）基于 KWR 快照数据提供自动化的性能诊断和优化建议。

### 报告结构

```
[建议列表]
    数据库时间分解
    等待相关建议
        TOP 等待事件建议
        轻量级锁等待事件
        IO 等待事件
        客户端等待事件
    CPU 相关建议
        TOP SQL 建议
        堆页修剪建议
    完整 SQL 列表
```

等待与 CPU 建议的顺序取决于哪方面占主导地位。

### 数据库时间分解

三层分解：
```
等待事件类别
    等待事件
        SQL 语句  | 数据库时间占比  | 等待事件占比  | QueryID
```

示例：COMMIT 语句因 WALWriteLock 消耗 73.62% 的数据库时间 -- 这识别出 COMMIT 为瓶颈。

### 自动化建议

每条建议包含：
- **依据** -- 为何需要优化
- **操作** -- 具体的配置更改或解决方案
- **参考** -- 相关的数据库时间占比和参数值

KDDM 给出的 WALWriteLock 优化示例：
```
commit_delay = 10
commit_siblings = 16
synchronous_commit = off
full_page_writes = off
```

迭代应用 KDDM 建议，直到没有更多建议或达到目标。

### KDDM SQL 报告

显示 PLSQL 语句的父子调用层级关系，识别问题源于 PLSQL 容器还是特定的子 SQL。

注意：如果 SQL 显示为 "Unknown"，表示已采集到等待事件但未捕获 SQL 文本（通常因为 `sys_stat_statements.max` 太小）。

## KWR DIFF 报告

比较两组 KWR 快照以分析性能差异。

### 字段说明

- **1st** -- 第一组快照统计
- **2nd** -- 第二组快照统计
- **% Diff** -- 变化百分比：(2nd - 1st) * 100 / 1st
- **Per-Second** -- 按经过时间归一化的值，便于公平比较

### 分析示例

| 指标 | 1st/s | 2nd/s | % Diff |
|------|-------|-------|--------|
| DB CPU(s) | 1185 | 4334 | +265% |
| Foreground Wait(s) | 22884 | 19057 | -17% |
| WAL Size(MB) | 8694 | 4527 | -48% |
| TPS | 352832 | 1240028 | +251% |

比较每秒值（而非总计值），因为快照间隔不同。与基准测试结果交叉引用以验证发现。

## KSH 报告

KSH（KingbaseES 会话历史）使用基于采样的统计方法，每秒捕获活跃会话状态。它与 KWR 互补：KWR 显示一段时间内的累积变化（默认 1 小时），而 KSH 捕获会被平均掉的短暂事件。

### KWR 与 KSH 对比

| 方面 | KWR | KSH |
|------|-----|-----|
| 用途 | 一段时间内的累积变化 | 特定秒的实时值 |
| 方法 | 累积计数 | 每秒采样 |
| 场景 | 升级后的整体改进 | 某时刻发生了何种异常 |
| 保留策略 | 1 小时快照，保留 8 天 | 1 秒实时数据保留 1 小时，之后按 1/10 历史存储 |

### 配置

```
track_activities = on
sys_stat_statements.track = 'top'
sys_kwr.collect_ksh = on
```

### 内部表

- `ksh_history_data` -- 来自 `sys_stat_activity` 的 KSH 采样数据
- `ksh_history` -- `ksh_history_data` 上的视图
- `ksh_statements` -- SQL 文本存储

数据保留由 `sys_kwr.history_days` 控制（默认 8 天）。如果 `ksh_history_data` 超过 10GB，将保留时间减少至 3 天或 1 天。

### 生成 KSH 报告

```sql
SELECT * FROM perf.ksh_report();                                  -- 当前区间
SELECT * FROM perf.ksh_report_by_snapshots(3, 4);                 -- 按快照 ID
SELECT * FROM perf.ksh_report_to_file(file_path => '/data/ksh.txt');
SELECT * FROM perf.ksh_report_to_file_by_snapshots(3, 4, file_path => '/data/ksh.txt');
```

### KSH 报告结构

**报告头部：** 版本、主机摘要、采样信息

关键字段：
- **Seconds Count** -- 采样持续时间（秒）
- **Sample Count** -- 总活跃会话采样数
- **Avg Act Ses** -- Sample Count / Seconds Count（每秒平均活跃会话数）

**报告主体：**
- Top 用户事件、后台事件
- Top 数据库、PL/SQL 过程
- Top 简单查询、高等待 SQL
- Top 会话、客户端
- Top 并行 SQL 等待事件
- Top 阻塞会话事件
- Top 重量级和轻量级锁等待事件
- Top SQL 命令类型和执行阶段
- 时间区间等待事件统计
- 完整 SQL 列表

### 解读 KSH 报告

**事件占比（类别百分比）：** 事件计数 * 100.0 / 总类别采样数

**活动占比（所有采样百分比）：** 事件计数 * 100.0 / 总采样数

**平均会话数：** 事件计数 / 采样持续时间（秒）

## 常见问题

**KWR 报告时间模型数据为空**：快照采集前未启用 `track_sql` 和 `track_instance`。重新启用并重新生成快照。

**KDDM 显示 "Unknown" SQL**：`sys_stat_statements.max` 太小。增加该值（如设为 10000）并重置统计。

**KSH 数据增长过大**：将 `sys_kwr.history_days` 从 8 减少到 3 或 1。

**短暂的性能尖峰在 KWR 中不可见**：改用 KSH -- 1 小时的 KWR 快照会平均掉短时问题。

## 最佳实践

1. 在生产部署早期启用 `sys_kwr` 以获取基线数据
2. 使用 KWR 进行趋势分析，使用 KSH 进行事件排查
3. 迭代应用 KDDM 建议，使用 KWR DIFF 报告衡量影响
4. 分析不同长度的快照时段时，比较每秒值（而非总计）
5. 保持 `track_sql_item` 不带 queryid 后缀，以避免统计膨胀
6. 监控 `ksh_history_data` 表大小；在超过 10GB 之前减少保留时间
