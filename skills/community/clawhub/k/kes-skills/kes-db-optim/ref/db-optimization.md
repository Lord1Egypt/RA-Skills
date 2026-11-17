# KingbaseES 数据库参数配置指南

本文档提供KingbaseES关键参数的配置建议和优化策略。

## 配置文件位置

```bash
# 主配置文件
$KINGBASE_HOME/data/kingbase.conf

# 动态参数配置
$KINGBASE_HOME/data/postgresql.auto.conf

# 客户端认证配置
$KINGBASE_HOME/data/sys_hba.conf

# 修改配置后重启或重新加载
-- 重启
systemctl restart kingbase

-- 或重新加载（不中断连接）
SELECT sys_reload_conf();
# 或编辑 kingbase.conf 后：
kill -HUP $(cat /var/run/kingbase/postmaster.pid)
```

---

## 内存参数配置

### shared_buffers（共享内存缓冲区）

**作用**：数据库缓存块，减少磁盘I/O

**默认**：128MB

**推荐值**
```
Shared Buffers 建议物理内存的 25%，最高不超过 40%

计算方法：
physical_memory = 16GB
shared_buffers = 4GB (16GB * 0.25)

# 示例配置
shared_buffers = 4096MB
```

**注意事项**
- 不要过大（超过物理内存 40% 会减少操作系统缓存，反而降低性能）
- 不要过小（会导致频繁磁盘I/O）
- 配合OS页面缓存

**验证方法**
```sql
-- 查看当前shared_buffers值
SHOW shared_buffers;

-- 评估是否足够
EXPLAIN ANALYZE
SELECT * FROM large_table LIMIT 1000;
-- 检查"Shared Hit" vs "Disk"比例
```

### effective_cache_size（有效缓存大小）

**作用**：优化器估算的整体缓存能力

**默认**：4GB

**推荐值**
```
有效缓存大小 = 物理内存 × 3/4

物理内存 = 16GB
effective_cache_size = 12GB

# 示例配置
effective_cache_size = 12288MB
```

**注意**
- 仅用于优化器估算，不会实际分配
- 为OS缓存预留空间

**验证方法**
```sql
-- 查看当前effective_cache_size
SHOW effective_cache_size;

-- 如果查询常走全表扫描，增大此值
EXPLAIN (COSTS OFF) SELECT COUNT(*) FROM large_table;
```

### work_mem（每个操作可用的内存）

**作用**：以下操作单次操作可用的内存：

- 外排序（`ORDER BY`, `GROUP BY`）
- 哈希JOIN
- 哈希聚合
- 差集
- 物化视图物化

**默认**：4MB

**计算方法**
```
work_mem = (预计内存需求) / (并发数)

例如：
- 有10个会话同时进行排序
- 每个会话需要500MB排序
- work_mem应该 = 500MB / 10 = 50MB

# 示例配置：保守值
work_mem = 64MB

# 示例配置：激进值（10个并发）
work_mem = 256MB
```

**调优步骤**
```sql
-- 1. 大表JOIN排序时监控
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    customer_id,
    SUM(amount) as total
FROM orders
GROUP BY customer_id
ORDER BY total DESC;

-- 2. 如果看到"Disk Sorting" -> 增大work_mem

-- 3. 根据系统负载调整
MAX_WORK_PROC = 10
SET work_mem = 256MB;  -- 每个连接的最大内存额度
```

**单表配置建议**
| 表数据量 | 建议work_mem |
|---------|------------|
| < 1GB | 16MB |
| 1-10GB | 32-64MB |
| 10-100GB | 64-256MB |
| > 100GB | 256MB+ |

### maintenance_work_mem（维护操作内存）

**作用**：维护操作可使用的内存：
- `CREATE INDEX`
- `CREATE TABLE AS`
- `CLUSTER`
- `VACUUM FULL`

**默认**：64MB

**推荐值**
```
建议值：物理内存的 1/10

物理内存 = 16GB
maintenance_work_mem = 1.6GB

# 示例配置
maintenance_work_mem = 2048MB
```

**权衡**
- 过大 → 并发维护操作可能耗尽内存
- 过小 → 长时间等待CREATE INDEX

**示例场景**
```sql
-- 长时间执行的维护操作
VACUUM FULL large_table;

-- 如果长时间卡住，可能需要增大maintenance_work_mem
```

### max_parallel_workers（最大并行工作进程）

**作用**：限制OLAP查询并行处理的进程数

**默认**：8

**推荐值**
```
max_parallel_workers = CPU核心数 × 2

CPU核心 = 16
max_parallel_workers = 32

# 示例配置
max_parallel_workers = 32
max_parallel_workers_per_gather = 4
```

### min_parallel_workers_per_gather

**作用**：每个并行查询启动的最小进程数

**默认**：1

**调优场景**
```sql
-- 大表扫描
SET min_parallel_workers_per_gather = 4;
```

---

## 连接参数配置

### max_connections（最大连接数）

**作用**：允许的最大客户端连接数

**默认**：100

**推荐值**
```
max_connections = 1 + CPU核心数 × (活跃进程+IO进程+缓存进程) / 256

CPU核心 = 8
max_connections = 1 + 8 * 5 / 256 ≈ 1.16 → 取5

# 示例配置
max_connections = 500

# 实际根据业务需求调整
max_connections = 200  # 高并发Web应用
max_connections = 50   # 内部系统
```

**注意事项**
- 每个连接消耗约30-50MB内存
- 过高占用过多资源，可能导致单连接响应变慢

**验证方法**
```sql
-- 查看当前连接数
SELECT count(*) FROM sys_stat_activity;

-- 判断是否达到上限
SELECT max_connections FROM sys_settings;
```

### shared_preload_libraries

**作用**：启动时预加载的共享库（扩展功能）

**默认**：`null`

**常用加载库**
```bash
# WAL归档 + sys_stat_statements（SQL统计）
shared_preload_libraries = 'sys_stat_statements'

# 并行列存
shared_preload_libraries = 'parallel_seqscan'

# 读写分离代理
shared_preload_libraries = 'libpqwalreceiver,libpqwalproxy'
```

**重启要求**
```
修改后必须重启数据库
systemctl restart kingbase
```

---

## 更新/删除性能参数

### wal_buffers（WAL缓冲区）

**作用**：WAL记录写入磁盘前的缓冲区

**默认**：16MB

**推荐值**
```
wal_buffers = shared_buffers × 1/256

shared_buffers = 16GB
wal_buffers = 16 + 16GB/256 = 62MB → 取64MB

# 示例配置
wal_buffers = 64MB
```

### checkpoint_completion_target

**作用**：checkpoint完成目标

**默认**：0.5

**推荐值**
```
高频率写入场景：
checkpoint_completion_target = 0.8

低频率写入场景：
checkpoint_completion_target = 0.5
```

### synchronous_commit

**作用**：事务提交模式
- `on`（默认）：提交后等待WAL落盘（安全，事务安全）
- `local`：仅等待本地WAL
- `off`：不等待WAL落盘（性能高但可能丢数据）

**推荐值**
```
重要数据：synchronous_commit = on
高并发分析：synchronous_commit = off
```

**权衡**
```bash
# 高性能场景（可接受短暂数据丢失）
synchronous_commit = off
```

### wal_keep_size

**作用**：保留的WAL大小

**默认**：0（无限制）

**推荐值**
```
设置保留大小避免auto checkpoint过早清理

wal_keep_size = 1GB
```

---

## IO性能参数

### random_page_cost（随机页面成本）

**作用**：优化器估算随机页面访问成本

**默认**：4.0

**调整场景**
```
SSD存储：random_page_cost = 1.1
HDD存储：random_page_cost = 4.0（默认）
混合存储：random_page_cost = 1.5
```

**示例**
```sql
-- SSD环境
random_page_cost = 1.1

-- HDD环境
random_page_cost = 4.0
```

### effective_io_concurrency

**作用**：估计的并发IO操作数

**默认**：1

**调整值**
```
SSD：effective_io_concurrency = 200
HDD：effective_io_concurrency = 2
NVMe SSD：effective_io_concurrency = 1000
```

---

## 查询性能参数

### casa_traversal_limit（查询优化器深度）

**作用**：优化器处理的树的深度

**默认**：0（优化器自行决定深度）

**经验值**
```
复杂查询深度 = 100个节点

# 如果查询复杂且需要避免深度查询
casa_traversal_limit = 50
```

### casa_subtree_limit（子树限制）

**作用**：优化器处理的子树大小

**默认**：0（无限制）

**经验值**
```
casa_subtree_limit = 87
```

---

## 网络性能参数

### enable_tcp_keepalives

**作用**：启用TCP keepalive

**默认**：off

**建议值**
```bash
# 启用TCP keepalive
enable_tcp_keepalives = on
```

---

## 表空间与存储参数

### default_tablespace

**作用**：默认表空间

**默认**：`sys_global`

**推荐**
```bash
# 为频繁更新的表指定表空间
default_tablespace = 'fast'  # SSD表空间
```

---

## 执行参数调优

### enable_sort（排序）

**作用**：控制是否使用排序

**默认**：on

**调整场景**
```
性能优先：enable_sort = off（提前JOIN，避免排序）

# 示例查询
SELECT * FROM huge_table
WHERE status = 'active'
ORDER BY created_at DESC;

# 启用排序（数据库不确定性或缺少合适索引）
SET enable_sort = off;
```

**注意**：多态排序可能失败

### enable_hash_join（哈希连接）

**作用**：控制是否使用哈希连接

**默认**：on

**调整场景**
```
内存受限：enable_hash_join = off（强制使用NESTLOOP）

# 示例
SET enable_hash_join = off;
```

### enable_nestloop（嵌套循环）

**作用**：控制是否使用嵌套循环JOIN

**默认**：on

**调整场景**
```
小表JOIN优化：enable_nestloop = on（小表驱动）

# 示例
SET enable_nestloop = on;
```

### enable_merge_join（归并连接）

**作用**：控制是否使用归并连接

**默认**：on

**调整场景**
```
避免排序开销：enable_merge_join = off

# 示例
SET enable_merge_join = off;
```

---

## FTS全文搜索

### default_text_search_config

**作用**：默认全文搜索配置

**默认**：`sys_catalog.simple`

**示例**
```bash
# 使用简体中文配置
default_text_search_config = 'sys_catalog.simple'
```

---

## 安全参数

### password_encryption（密码加密）

**作用**：创建用户时的默认加密方式

**默认**：`scram-sha-256`

**加密算法**
```
scram-sha-256：默认，强加密
md5：较弱的加密
```

**示例**
```sql
-- 创建用户（强制加密）
CREATE USER newuser WITH PASSWORD 'password123';

-- 使用强加密
ALTER USER newuser ENCRYPT PASSWORD 'password123';
```

---

## 日志参数配置

### logging_collector（日志收集器）

**作用**：是否启动日志收集器

**默认**：off

**启用方法**
```bash
logging_collector = on
log_directory = 'log'  # 日志目录
log_filename = 'kingbase-%Y-%m-%d_%H%M%S.log'  # 文件名格式
log_rotation_age = 1d   # 旋转周期
log_rotation_size = 100MB  # 日志大小
```

### log_min_duration_statement

**作用**：记录执行时间超过指定毫秒数的查询

**默认**：-1（不记录）

**推荐值**
```
log_min_duration_statement = 1000  # 记录慢查询（> 1秒）
```

### log_statement

**作用**：记录SQL语句类型

**默认**：`none`

**常用配置**
```bash
# 记录所有DML
log_statement = 'ddl'

# 记录所有SQL
log_statement = 'all'
```

---

## VACUUM 自动清理

### VACUUM 作用

- 清理死元组（被 DELETE/UPDATE 标记删除的行）
- 回收存储空间供后续 INSERT 重用
- 防止表膨胀导致的全表扫描变慢
- 配合 `ANALYZE` 更新统计信息

### 自动 VACUUM 配置

```sql
-- 查看自动 vacuum 参数
SHOW autovacuum;

-- 常见参数
autovacuum = on                          -- 启用自动清理
autovacuum_max_workers = 3               -- 最大后台 worker 数
autovacuum_naptime = 10s                 -- 检查间隔
autovacuum_vacuum_scale_factor = 0.2     -- 触发阈值比例（变更量/总行数）
autovacuum_vacuum_threshold = 2000       -- 触发阈值行数（绝对值）
autovacuum_analyze_scale_factor = 0.1    -- 分析阈值比例
```

### 手动 VACUUM

```sql
-- 简单 VACUUM（整理死元组）
VACUUM table_name;

-- VACUUM ANALYZE（整理+分析，推荐）
VACUUM ANALYZE table_name;

-- VACUUM FULL（重建表，释放磁盘空间，但会锁定表）
VACUUM FULL table_name;
```

### VACUUM 建议

```sql
-- 高频 DML 表定期维护
VACUUM ANALYZE users;
VACUUM ANALYZE orders;

-- 日志类表在 logrotate 时清理
VACUUM logs;

-- 大批量删除后及时 ANALYZE
DELETE FROM logs WHERE created_at < '2025-01-01';
ANALYZE logs;
```

---

## 零配置场景（简化）

**单机单租户环境参数**
```bash
# 内存
shared_buffers = 2048MB
effective_cache_size = 12288MB
work_mem = 64MB
maintenance_work_mem = 1024MB

# 连接
max_connections = 200

# IO
random_page_cost = 1.1
effective_io_concurrency = 100

# WAL
wal_buffers = 64MB
checkpoint_completion_target = 0.8
synchronous_commit = on
wal_keep_size = 1GB

# 日志
logging_collector = on
log_directory = 'log'
log_min_duration_statement = 1000
```

---

## 配置验证

### 查看当前配置

```sql
-- 查看所有参数值
SHOW ALL;

-- 查看特定参数
SHOW shared_buffers;

-- 查看参数源（有效值）
SHOW shared_buffers;
```

### 查看当前内存使用

```sql
-- 查看连接数内存分配
SELECT
    datname,
    state,
    application_name,
    mem_percent,
    wait_event_type,
    wait_event
FROM sys_stat_activity;

-- 查看表空间使用
SELECT
    sys_database.name,
    sys_database.oid,
    sys_tablespace.spcname,
    sys_tablespace.spcowner,
    sys_size_pretty(sys_database_size(c.oid), 'MB')
FROM sys_database c
JOIN sys_tablespace s ON ANY s.spclocation = ANY(SELECT oid FROM sys_tablespace)
JOIN sys_class t ON ANY t.relpages = ANY(SELECT relpages FROM sys_class)
WHERE t.relname = 'your_table';
```

---

## 动态调优流程

### 第1步：评估环境
```bash
# 1. 采集系统信息
free -h  # 内存
df -h    # 存储空间
nproc     # CPU核心数
```

### 第2步：配置基础参数
```bash
shared_buffers = 4096MB
effective_cache_size = 12288MB
work_mem = 64MB
 maintenance_work_mem = 1024MB
```

### 第3步：标记高负载场景
- 高频全表扫描（增大effective_cache_size）
- 大量排序（增大work_mem）
- 大量CREATE INDEX（增大maintenance_work_mem）
- 大量连接（增大max_connections）

### 第4步：监控与调优
```sql
-- 监控慢查询
SELECT
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM sys_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### 第5步：调整参数
```sql
-- 根据监控结果调整
ALTER SYSTEM SET work_mem = 128MB;
-- 重启生效：systemctl restart kingbase
```

---

## 参数调整案例

### 案例1：内存密集型应用

**环境**：32GB内存，50GB SSD

**配置方案**
```bash
# 内存分配
shared_buffers = 8192MB         # 32GB * 0.25
effective_cache_size = 24576MB    # 32GB / 4 (部分给os缓存)
work_mem = 256MB                 # 假设30个并发
maintenance_work_mem = 8192MB   # 32GB / 4
max_connections = 500

# WAL
wal_buffers = 64MB
checkpoint_completion_target = 0.9

# IO
random_page_cost = 1.1
effective_io_concurrency = 200
```

### 案例2：高并发OLTP

**环境**：16GB内存，100核CPU

**配置方案**
```bash
# 内存分配
shared_buffers = 4096MB         # 16GB * 0.25
effective_cache_size = 12288MB   # 16GB / 4
work_mem = 64MB                  # 100核/2 = 50并发
maintenance_work_mem = 2048MB

# 连接
max_connections = 1000

# IO
random_page_cost = 1.1
effective_io_concurrency = 1000
```

### 案例3：大量报表OLAP

**环境**：64GB内存，内部分析系统

**配置方案**
```bash
# 内存分配
shared_buffers = 16384MB         # 64GB * 0.25
effective_cache_size = 49152MB  # 64GB / 4
work_mem = 512MB                # 并发高集成分析
maintenance_work_mem = 16384MB

# 并行
max_parallel_workers = 256
min_parallel_workers_per_gather = 4

# IO
random_page_cost = 1.1
effective_io_concurrency = 1000
```

---

## 安全提醒

1. **修改参数需重启或重新加载**
   ```bash
   # 修改kingbase.conf
   systemctl restart kingbase
   # 或使用SQL语句
   ALTER SYSTEM SET parameter = value;
   ```
2. **不要超出OS限制**
   ```bash
   # 查看系统限制
   ulimit -n
   # 调整max_connections匹配系统限制
   ```
3. **备份配置文件**
   ```bash
   cp $KINGBASE_HOME/data/kingbase.conf $KINGBASE_HOME/data/kingbase.conf.bak
   ```

---

## 常见参数问题

### 问题1：共享内存不足

**错误**：`ERROR: could not allocate shared memory`

**原因**：shared_buffers过大超过系统limit

**解决**
```bash
# 查看系统共享内存限制
ipcs -l

# 临时提升
sudo sysctl -w kernel.shmmax=68719476736
sudo sysctl -w kernel.shmall=4294967296

# 永久修复（/etc/sysctl.conf）
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
```

**调整shared_buffers**
```bash
shared_buffers = 2048MB  # 降低到1/4内存
```

### 问题2：连接池耗尽

**错误**：`FATAL: sorry, too many clients already`

**原因**：达到max_connections限制

**解决**：增大max_connections
```sql
ALTER SYSTEM SET max_connections = 1000;
systemctl restart kingbase
```

### 问题3：WAL oplog满

**错误**：`WARNING: cause: WAL XXXX is not active`

**原因**：checkpoint未及时完成

**解决**
```bash
# 增大WAL缓冲、完成时间
wal_buffers = 64MB
checkpoint_completion_target = 0.9

# 检查WAL参数
SELECT * FROM sys_settings WHERE name IN ('wal_buffers', 'checkpoint_completion_target');
```

---

## 总结

参数调优原则

1. **内存分配**：shared_buffers/effective_cache_size按比例分配
2. **操作内存**：work_mem根据并发量预估
3. **IO性能**：SSD/注意IO成本参数
4. **连接控制**：cpu作为参考，预留内存
5. **安全优先**：synchronous_commit及时落盘
6. **动态调整**：循环监控+逐步调优

**黄金法则**
```
shared_buffers = 物理内存 × 0.25（最高不超过 40%）

effective_cache_size = 物理内存 × 0.75

work_mem = 预估排序/哈希需求 / 并发数

经常根据业务监控结果微调
```
