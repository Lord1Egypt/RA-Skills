# KingbaseES 系统目录参考

系统目录视图、information_schema、性能统计视图和 Oracle 兼容视图速查。

## 1. 系统目录概述

### 命名空间对照

| 模式 | 说明 |
|------|------|
| `sys` | KingbaseES 系统目录（如 PostgreSQL 的 `sys_catalog`） |
| `sys_information_schema` | 标准信息模式 |
| `public` | 用户默认模式 |
| `kdb` | 金仓特有扩展视图（如存在） |

### 查询系统目录

```sql
-- 统一使用 sys_ 前缀
SELECT * FROM sys_tables WHERE tablename = 'employees';
SELECT * FROM sys_columns WHERE tablename = 'employees';

-- 或直接引用系统表
SELECT * FROM sys_class WHERE relname = 'employees';
```

---

## 2. 核心系统表

### sys_class — 所有数据库对象

```sql
-- 对象类型对照
-- relkind: r=普通表, v=视图, S=序列, i=索引, c=复合类型, f=分区表, m=物质化视图

SELECT
    relname,
    relkind,
    CASE relkind
        WHEN 'r' THEN '普通表'
        WHEN 'v' THEN '视图'
        WHEN 'S' THEN '序列'
        WHEN 'i' THEN '索引'
        WHEN 'c' THEN '复合类型'
        WHEN 'f' THEN '分区表'
        WHEN 'm' THEN '物质化视图'
    END AS type_desc,
    relpages,
    reltuples,
    relowner AS owner_oid
FROM sys_class
WHERE relnamespace != (SELECT oid FROM sys_namespace WHERE nspname = 'sys')
  AND relnamespace != (SELECT oid FROM sys_namespace WHERE nspname = 'sys_information_schema')
ORDER BY reltuples DESC;
```

### sys_namespace — 模式信息

```sql
SELECT
    nspname,
    sys_get_userbyid(nspowner) AS owner
FROM sys_namespace
WHERE nspname NOT LIKE 'sys%'
  AND nspname != 'information_schema'
ORDER BY nspname;
```

### sys_user — 用户信息

```sql
SELECT
    usename,
    usesuper,
    usecreatedb,
    usecatcreate,
    valuntil,
    useconfig
FROM sys_user
WHERE usehavelogin
ORDER BY usename;
```

### sys_authid — 角色/权限主体

```sql
SELECT
    rolname,
    rolsuper,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin,
    rolconnlimit,
    rolvaliduntil
FROM sys_authid
ORDER BY rolname;
```

---

## 3. 表结构查询

### sys_tables — 表列表

```sql
SELECT
    schemaname,
    tablename,
    tableowner,
    HAS_TABLE_PRIVILEGE(tablename, 'SELECT') AS can_select
FROM sys_tables
WHERE schemaname NOT IN ('sys', 'sys_information_schema', 'information_schema')
ORDER BY schemaname, tablename;
```

### sys_columns — 列信息

```sql
SELECT
    table_name,
    column_name,
    ordinal_position,
    data_type,
    character_maximum_length,
    numeric_precision,
    numeric_scale,
    is_nullable,
    column_default
FROM sys_information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'employees'
ORDER BY ordinal_position;
```

### sys_class 获取列详情

```sql
-- 通过 sys_attribute 查看列信息
SELECT
    c.relname AS table_name,
    a.attname AS column_name,
    a.attnum,
    a.atttypid,
    t.typname AS type_name,
    a.attnotnull AS not_null,
    a.atthasdef AS has_default,
    a.attlen AS attlen,
    a.atttypmod AS typmod
FROM sys_attribute a
JOIN sys_class c ON a.attrelid = c.oid
JOIN sys_type t ON a.atttypid = t.oid
WHERE c.relname = 'employees'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

### 获取列注释

```sql
SELECT
    c.relname AS table_name,
    a.attname AS column_name,
    descr.description
FROM sys_attribute a
JOIN sys_class c ON a.attrelid = c.oid
LEFT JOIN sys_description descr ON a.attrelid = descr.objoid AND a.attnum = descr.objsubid
WHERE c.relname = 'employees'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

---

## 4. 索引查询

### sys_indexes — 索引列表

```sql
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM sys_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

### 索引详细信息

```sql
SELECT
    t.relname AS table_name,
    i.relname AS index_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary,
    ix.indisvalid AS is_valid,
    sys_size_pretty(sys_relation_size(i.oid)) AS index_size,
    sys_get_indexdef(ix.indexrelid) AS index_def
FROM sys_index ix
JOIN sys_class t ON ix.indrelid = t.oid
JOIN sys_class i ON ix.indexrelid = i.oid
WHERE t.relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
ORDER BY t.relname, i.relname;
```

### 索引列查询

```sql
SELECT
    t.relname AS table_name,
    i.relname AS index_name,
    a.attname AS column_name,
    ix.indisunique,
    ix.indisprimary
FROM sys_index ix
JOIN sys_class t ON ix.indrelid = t.oid
JOIN sys_class i ON ix.indexrelid = i.oid
JOIN sys_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
WHERE t.relname = 'employees'
ORDER BY i.relname, a.attnum;
```

---

## 5. 约束查询

### 所有约束概览

```sql
SELECT
    table_name,
    constraint_name,
    constraint_type
FROM sys_information_schema.table_constraints
WHERE table_schema = 'public'
ORDER BY table_name, constraint_type;
```

### 主键约束

```sql
SELECT
    tc.table_name,
    tc.constraint_name,
    kcu.column_name
FROM sys_information_schema.table_constraints tc
JOIN sys_information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE tc.constraint_type = 'PRIMARY KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;
```

### 外键约束

```sql
SELECT
    tc.constraint_name,
    tc.table_name AS source_table,
    kcu.column_name AS source_column,
    ccu.table_name AS target_table,
    ccu.column_name AS target_column,
    rc.update_rule,
    rc.delete_rule
FROM sys_information_schema.table_constraints tc
JOIN sys_information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN sys_information_schema.constraint_column_usage ccu
    ON tc.constraint_name = ccu.constraint_name
JOIN sys_referential_constraints rc
    ON tc.constraint_name = rc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;
```

### UNIQUE 和 CHECK 约束

```sql
-- UNIQUE约束
SELECT
    tc.table_name,
    tc.constraint_name,
    STRING_AGG(kcu.column_name, ', ') AS columns
FROM sys_information_schema.table_constraints tc
JOIN sys_information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'UNIQUE'
  AND tc.table_schema = 'public'
GROUP BY tc.table_name, tc.constraint_name;

-- CHECK约束
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    sys_get_constraintdef(oid) AS constraint_def
FROM sys_constraint
WHERE contype = 'c'
  AND conrelid IN (
      SELECT oid FROM sys_class
      WHERE relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
  )
ORDER BY conrelid, conname;
```

---

## 6. 序列查询

### sys_sequences — 序列列表

```sql
SELECT
    sequencename,
    sequenceowner,
    start_value,
    minimum_value,
    maximum_value,
    increment_by,
    is_cyclic,
    cache_value
FROM sys_sequences
WHERE schemaname = 'public'
ORDER BY sequencename;
```

### 序列当前值

```sql
-- 查看序列当前值
SELECT last_value, is_called
FROM employees_id_seq;

-- 或使用函数
SELECT currval('employees_id_seq');
SELECT lastval();  -- 最后使用的任何序列的值
```

### 序列与表关联

```sql
-- 查找表关联的序列
SELECT
    c.relname AS table_name,
    a.attname AS column_name,
    sys_get_expr(d.adbin, d.adrelid) AS default_expr
FROM sys_class c
JOIN sys_attribute a ON a.attrelid = c.oid
JOIN sys_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
WHERE c.relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
  AND sys_get_expr(d.adbin, d.adrelid) LIKE '%nextval%'
ORDER BY c.relname;
```

---

## 7. 函数/过程查询

### 所有函数列表

```sql
SELECT
    routine_schema,
    routine_name,
    routine_type,
    data_type AS return_type,
    external_language
FROM sys_information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

### 函数详细信息

```sql
SELECT
    p.proname AS function_name,
    p.prorettype::regtype AS return_type,
    p.proargnames AS arg_names,
    p.proargtypes AS arg_types,
    l.lanname AS language,
    sys_get_userbyid(p.proowner) AS owner,
    sys_get_function_arguments(p.oid) AS arguments,
    sys_get_functiondef(p.oid) AS full_definition
FROM sys_proc p
JOIN sys_language l ON p.prolangid = l.oid
WHERE p.pronamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
ORDER BY p.proname;
```

### 存储过程 vs 函数

```sql
SELECT
    p.proname,
    CASE WHEN p.prorettype = 'void'::regtype AND p.prokind = 'p' THEN 'PROCEDURE'
         WHEN p.prokind = 'f' THEN 'FUNCTION'
         WHEN p.prokind = 'a' THEN 'AGGREGATE'
         WHEN p.prokind = 'w' THEN 'WINDOW'
         ELSE p.prokind
    END AS object_type,
    p.prorettype::regtype AS return_type,
    l.lanname AS language,
    sys_get_functiondef(p.oid) AS definition
FROM sys_proc p
JOIN sys_language l ON p.prolangid = l.oid
WHERE p.pronamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
ORDER BY p.proname;
```

---

## 8. 触发器查询

### 触发器列表

```sql
SELECT
    t.tgname AS trigger_name,
    t.tgrelid::regclass AS table_name,
    p.proname AS function_name,
    t.tgfreetrace AS action_time,
    CASE t.tgfreetrace
        WHEN 'B' THEN 'BEFORE'
        WHEN 'A' THEN 'AFTER'
        WHEN 'I' THEN 'INSTEAD OF'
    END AS timing,
    substring(ARRAY_TO_STRING(ARRAY(SELECT evt FROM unnest(t.tgevent) evt), ',')
        REPLACE ',I', 'INSERT' REPLACE ',D', 'DELETE' REPLACE ',U', 'UPDATE' REPLACE ',T', 'TRUNCATE'
    ) AS events,
    t.tgenabled AS enabled
FROM sys_trigger t
JOIN sys_proc p ON t.tgfoid = p.oid
WHERE t.tgrelid IN (
    SELECT oid FROM sys_class
    WHERE relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
)
ORDER BY t.tgrelid, t.tgname;
```

---

## 9. 权限查询

### 表权限

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type,
    is_grantable
FROM sys_table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

### 列级权限

```sql
SELECT
    grantee,
    table_name,
    column_name,
    privilege_type,
    is_grantable
FROM sys_column_privileges
WHERE table_schema = 'public'
ORDER BY table_name, column_name, grantee;
```

### Schema 权限

```sql
SELECT
    n.nspname AS schema_name,
    sys_get_userbyid(n.nspowner) AS owner,
    has_schema_privilege(current_user, n.nspname, 'USAGE') AS has_usage,
    has_schema_privilege(current_user, n.nspname, 'CREATE') AS has_create
FROM sys_namespace n
WHERE n.nspname NOT LIKE 'sys%'
  AND n.nspname != 'information_schema'
ORDER BY n.nspname;
```

### 数据库权限

```sql
SELECT
    datname,
    has_database_privilege(current_user, datname, 'CONNECT') AS can_connect,
    has_database_privilege(current_user, datname, 'CREATE') AS can_create,
    has_database_privilege(current_user, datname, 'TEMPORARY') AS can_temp
FROM sys_database;
```

### 角色成员关系

```sql
SELECT
    r.rolname AS role_name,
    m.rolname AS member_name,
    am.admin_member AS can_admin
FROM sys_auth_members am
JOIN sys_authid r ON am.roleid = r.oid
JOIN sys_authid m ON am.member = m.oid
ORDER BY r.rolname, m.rolname;
```

---

## 10. 性能统计视图

### sys_stat_activity — 活跃会话

```sql
SELECT
    pid,
    usename,
    datname,
    client_addr,
    client_port,
    backend_start,
    xact_start,
    query_start,
    state_change,
    state,
    wait_event_type,
    wait_event,
    query
FROM sys_stat_activity
WHERE datname IS NOT NULL
ORDER BY query_start;

-- 字段说明:
-- state: active, idle, idle in transaction, idle in transaction (aborted), fastpath function call
-- wait_event_type: Client, Lock, IO, Activity, LWLock, BufferPin, Lock
```

### 慢查询检测

```sql
SELECT
    pid,
    usename,
    datname,
    NOW() - query_start AS duration,
    state,
    wait_event,
    LEFT(query, 200) AS query_preview
FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '30 seconds'
  AND query NOT LIKE '%sys_stat_activity%'
ORDER BY duration DESC;
```

### 长事务检测

```sql
SELECT
    pid,
    usename,
    NOW() - xact_start AS transaction_age,
    state,
    LEFT(query, 200) AS query_preview
FROM sys_stat_activity
WHERE xact_start IS NOT NULL
  AND NOW() - xact_start > INTERVAL '5 minutes'
ORDER BY transaction_age DESC;
```

### sys_stat_database — 数据库统计

```sql
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
    tup_deleted,
    conflicts,
    temp_files,
    temp_bytes,
    deadlocks
FROM sys_stat_database
WHERE datname IS NOT NULL;

-- 缓存命中率
SELECT
    datname,
    ROUND(blks_hit::DECIMAL / NULLIF(blks_hit + blks_read, 0) * 100, 2) AS hit_ratio
FROM sys_stat_database
WHERE datname IS NOT NULL;
```

### sys_stat_user_tables — 表级统计

```sql
SELECT
    relname,
    seq_scan,           -- 全表扫描次数
    seq_tup_read,       -- 全表扫描读取行数
    idx_scan,           -- 索引扫描次数
    idx_tup_fetch,      -- 索引扫描获取行数
    n_live_tup,         -- 活跃行数
    n_dead_tup,         -- 死亡行数
    n_tup_ins,          -- 写入行数
    n_tup_upd,          -- 更新行数
    n_tup_del,          -- 删除行数
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM sys_stat_user_tables
ORDER BY n_live_tup DESC;

-- 检查是否需要VACUUM
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    ROUND(n_dead_tup::DECIMAL / NULLIF(n_live_tup, 0) * 100, 2) AS dead_ratio
FROM sys_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_ratio DESC;
```

### sys_stat_user_indexes — 索引统计

```sql
SELECT
    relname AS table_name,
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM sys_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY sys_relation_size(indexrelid) DESC;
```

### sys_bgwriter — 后台写入统计

```sql
SELECT
    checkpoints_timed,
    checkpoints_req,
    checkpoint_write_time,
    checkpoint_sync_time,
    buffers_checkpoint,
    buffers_clean,
    maxwritten_clean,
    buffers_backend,
    buffers_alloc
FROM sys_bgwriter;
```

### sys_stat_io_user_tables — I/O统计

```sql
SELECT
    relname,
    heap_blks_read,
    heap_blks_hit,
    idx_blks_read,
    idx_blks_hit,
    toast_blks_read,
    toast_blks_hit,
    tidx_blks_read,
    tidx_blks_hit
FROM sys_stat_io_user_tables
ORDER BY heap_blks_read DESC;
```

---

## 11. 锁信息

### sys_locks — 锁视图

```sql
SELECT
    pid,
    mode,
    granted,
    locktype,
    relation::regclass AS locked_table,
    virtualtransaction,
    transactionid,
    classid::regclass,
    objid,
    objsubid
FROM sys_locks
WHERE relation IS NOT NULL
ORDER BY NOT granted, pid;

-- mode类型: AccessShareLock, RowShareLock, RowExclusiveLock, ShareUpdateExclusiveLock,
-- ShareLock, ShareRowExclusiveLock, ExclusiveLock, AccessExclusiveLock
```

### 锁等待查询

```sql
-- 谁在等待锁
SELECT * FROM sys_locks WHERE NOT granted;

-- 阻塞关系
SELECT
    blocked.pid AS blocked_pid,
    blocked.usename AS blocked_user,
    blocking.pid AS blocking_pid,
    blocking.usename AS blocking_user,
    NOW() - blocked.query_start AS wait_duration,
    LEFT(blocked.query, 100) AS blocked_query,
    LEFT(blocking.query, 100) AS blocking_query
FROM sys_locks blocked_lock
JOIN sys_stat_activity blocked ON blocked_lock.pid = blocked.pid
JOIN sys_locks blocking_lock
    ON blocked_lock.relation = blocking_lock.relation
    AND blocked_lock.pid != blocking_lock.pid
JOIN sys_stat_activity blocking ON blocking_lock.pid = blocking.pid
WHERE NOT blocked_lock.granted
  AND blocking_lock.granted;
```

### 终止阻塞会话

```sql
-- 取消查询
SELECT sys_cancel_pid(pid)
FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '10 minutes';

-- 终止连接
SELECT sys_terminate_pid(pid)
FROM sys_stat_activity
WHERE state = 'idle in transaction'
  AND NOW() - xact_start > INTERVAL '5 minutes';
```

---

## 12. 复制状态

### sys_stat_replication — 复制监控

```sql
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    client_hostname,
    client_port,
    backend_start,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_priority,
    sync_state
FROM sys_stat_replication;
```

### 复制延迟计算

```sql
-- 计算WAL延迟
SELECT
    client_addr,
    application_name,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sys_wal_lsn_diff(sys_current_wal_lsn(), sent_lsn) AS sent_delay_bytes,
    sys_wal_lsn_diff(sys_current_wal_lsn(), replay_lsn) AS replay_delay_bytes
FROM sys_stat_replication;
```

### 复制槽

```sql
SELECT
    slot_name,
    plugin,
    slot_type,
    active,
    restart_lsn,
    confirmed_flush_lsn
FROM sys_replication_slot;
```

---

## 13. 配置参数

### sys_config — 配置参数

```sql
SELECT
    name,
    setting,
    unit,
    context,
    category,
    source,
    sourcefile,
    min_val,
    max_val,
    boot_val,
    reset_val
FROM sys_config
WHERE name IN ('max_connections', 'shared_buffers', 'work_mem', 'effective_cache_size')
ORDER BY name;

-- context: postmaster(需重启), user(用户级), superuser(超级用户), internal(运行时不可变)
-- source: default, database, system, override(ALTER SYSTEM), session, assign
```

### 查看特定参数

```sql
SHOW max_connections;
SHOW shared_buffers;
SHOW work_mem;
SHOW ALL;

-- 从sys_config查看
SELECT name, setting, unit FROM sys_config WHERE name = 'work_mem';
```

---

## 14. 表空间信息

### sys_tablespace — 表空间列表

```sql
SELECT
    spcname,
    sys_get_userbyid(spcowner) AS owner,
    spclocation,
    spcoptions,
    sys_size_pretty(sys_tablespace_size(spcname)) AS size
FROM sys_tablespace
ORDER BY spcname;
```

### 表空间使用详情

```sql
-- 表空间中的表
SELECT
    t.spcname AS tablespace,
    c.relname AS table_name,
    sys_size_pretty(sys_relation_size(c.oid)) AS size,
    c.relkind AS type
FROM sys_class c
JOIN sys_tablespace t ON c.reltablespace = t.oid
WHERE c.relkind = 'r'
  AND c.relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
ORDER BY sys_relation_size(c.oid) DESC;
```

---

## 15. 分区信息

### 分区表查询

```sql
-- 查看分区表
SELECT
    parent.relname AS parent_table,
    child.relname AS child_table,
    sys_get_expr(c.relpartbound, c.oid) AS partition_bound
FROM sys_inherits i
JOIN sys_class parent ON i.inhparent = parent.oid
JOIN sys_class child ON i.inhrelid = child.oid
WHERE parent.relname = 'sales'
ORDER BY child.relname;
```

### 分区边界

```sql
SELECT
    relname,
    relpartbound AS partition_bound,
    relpartstrategy AS strategy
FROM sys_class
WHERE relispartition
  AND relname LIKE 'sales%'
ORDER BY relname;

-- relpartstrategy: r=RANGE, l=LIST, h=HASH
```

---

## 16. 扩展信息

### 已安装扩展

```sql
SELECT
    extname,
    extversion,
    extrelocatable,
    n.nspname AS schema_name
FROM sys_extension e
JOIN sys_namespace n ON e.extnamespace = n.oid
ORDER BY extname;
```

### 扩展可用列表

```sql
SELECT
    name,
    default_version,
    installed_version,
    comment,
    superuser,
    relocatable,
    schema
FROM sys_available_extensions
ORDER BY name;
```

---

## 17. 依赖关系

### 对象依赖

```sql
-- 谁依赖于这个对象
SELECT
    dep.deptype AS dep_type,
    class_parent.relname AS parent_object,
    class_child.relname AS child_object
FROM sys_depend dep
JOIN sys_class class_parent ON dep.classid = sys_class.oid AND dep.refobjid = class_parent.oid
JOIN sys_class class_child ON dep.objid = class_child.oid
WHERE class_parent.relname = 'employees'
ORDER BY class_child.relname;

-- 类型说明: n=正常, a=自动, i=内部, e=扩展, x=扩展成员, p=自动删除
```

### 视图依赖

```sql
-- 视图依赖的基础表
SELECT
    v.relname AS view_name,
    t.relname AS table_name
FROM sys_depend d
JOIN sys_class v ON d.classid = 'sys_class'::regclass AND d.objid = v.oid
JOIN sys_class t ON d.refobjid = t.oid
WHERE v.relkind = 'v'
  AND v.relnamespace = (SELECT oid FROM sys_namespace WHERE nspname = 'public')
ORDER BY v.relname, t.relname;
```

---

## 18. 数据库大小

### 数据库大小

```sql
-- 所有数据库大小
SELECT
    datname,
    sys_size_pretty(sys_database_size(datname)) AS size
FROM sys_database
ORDER BY sys_database_size(datname) DESC;

-- 当前数据库大小
SELECT sys_size_pretty(sys_database_size(current_database()));
```

### 表大小

```sql
-- 表大小排名
SELECT
    relname,
    sys_size_pretty(sys_relation_size(relid)) AS table_size,
    sys_size_pretty(sys_total_relation_size(relid)) AS total_size,
    n_live_tup,
    n_dead_tup
FROM sys_stat_user_tables
ORDER BY sys_total_relation_size(relid) DESC
LIMIT 20;

-- 带索引的完整大小
SELECT
    n.nspname AS schema_name,
    c.relname AS table_name,
    sys_size_pretty(sys_relation_size(c.oid)) AS data_size,
    sys_size_pretty(sys_indexes_size(c.oid)) AS index_size,
    sys_size_pretty(sys_total_relation_size(c.oid)) AS total_size
FROM sys_class c
JOIN sys_namespace n ON c.relnamespace = n.oid
WHERE c.relkind = 'r'
  AND n.nspname = 'public'
ORDER BY sys_total_relation_size(c.oid) DESC;
```

---

## 19. 转换函数速查

### OID 转可读名称

```sql
-- OID → 类型名
SELECT typname FROM sys_type WHERE oid = 23;  -- integer

-- OID → 用户/角色名
SELECT sys_get_userbyid(10);

-- OID → 模式名
SELECT nspname FROM sys_namespace WHERE oid = 2200;

-- OID → 类名
SELECT relname FROM sys_class WHERE oid = 16390;
```

### 对象定义获取

```sql
-- 获取表定义
SELECT sys_get_tabledef(table_oid);

-- 获取索引定义
SELECT sys_get_indexdef(index_oid);

-- 获取约束定义
SELECT sys_get_constraintdef(constraint_oid);

-- 获取函数定义
SELECT sys_get_functiondef(function_oid);

-- 获取触发器定义
SELECT sys_get_triggerdef(trigger_oid);

-- 获取扩展创建语句
SELECT extname, extversion FROM sys_extension;
```

### 类型转换

```sql
-- 使用 ::regtype 转换
SELECT 'integer'::regtype;       -- 23
SELECT 23::regtype;              -- integer

-- 使用 ::regclass 转换
SELECT 'public.employees'::regclass;
SELECT 16390::regclass;          -- public.employees
```

---

## 20. Oracle 兼容视图

### 兼容视图映射

| Oracle视图 | KingbaseES等效 | 说明 |
|-----------|---------------|------|
| all_tables | sys_tables | 可访问的表 |
| all_tab_columns | sys_information_schema.columns | 表列信息 |
| all_indexes | sys_indexes | 索引信息 |
| all_constraints | sys_information_schema.table_constraints | 约束信息 |
| all_users | sys_user | 用户列表 |
| all_tab_privs | sys_table_privileges | 表权限 |
| v$session | sys_stat_activity | 会话信息 |
| v$instance | sys_stat_progress_base | 实例信息 |
| v$parameter | sys_config | 配置参数 |
| dba_tables | sys_tables (需SUPERUSER) | 所有表 |
| dba_segments | 通过sys_class+sys_relation_size | 段信息 |
| user_tables | sys_tables WHERE tableowner=current_user | 当前用户表 |
| user_tab_columns | sys_information_schema.columns WHERE table_schema=current_schema() | 当前用户列 |
| user_indexes | sys_indexes WHERE schemaname=current_schema() | 当前用户索引 |

### 启用Oracle兼容模式

```sql
-- 查看当前模式
SHOW oracle_compatible;

-- 启用
ALTER SYSTEM SET oracle_compatible = on;
SELECT sys_reload_conf();
```

---

## 21. 常用查询模板

### 对象查找

```sql
-- 查找包含特定字符串的表
SELECT schemaname, tablename FROM sys_tables WHERE tablename ILIKE '%employee%';

-- 查找包含特定列名的表
SELECT table_name, column_name
FROM sys_information_schema.columns
WHERE column_name ILIKE '%email%';

-- 查找使用特定类型的列
SELECT table_name, column_name, data_type
FROM sys_information_schema.columns
WHERE data_type = 'jsonb'
  AND table_schema = 'public';
```

### 空间分析

```sql
-- 查找未收缩的表
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    relpages,
    reltuples,
    CASE WHEN reltuples > 0
        THEN ROUND(n_dead_tup::DECIMAL / n_live_tup * 100, 2)
        ELSE 0
    END AS dead_pct
FROM sys_stat_user_tables
WHERE n_dead_tup > 0.1 * n_live_tup
ORDER BY n_dead_tup DESC;
```

### 连接分析

```sql
-- 按用户统计连接
SELECT usename, count(*) AS connections, state
FROM sys_stat_activity
GROUP BY usename, state
ORDER BY connections DESC;

-- 按来源IP统计
SELECT client_addr, count(*) AS connections
FROM sys_stat_activity
WHERE client_addr IS NOT NULL
GROUP BY client_addr
ORDER BY connections DESC;
```

---

## 22. 统计信息管理

### 重置统计

```sql
-- 重置所有统计
SELECT sys_stat_reset();

-- 重置单表统计
SELECT sys_stat_reset_single_table_counters('employees'::regclass);

-- 重置数据库统计
SELECT sys_stat_reset_single_table_counters('employees'::regclass);

-- 重置语句统计
SELECT sys_stat_statements_reset();
```

### 分析器状态

```sql
-- 查看最后分析时间
SELECT
    relname,
    last_analyze,
    last_autoanalyze,
    last_vacuum,
    last_autovacuum
FROM sys_stat_user_tables
ORDER BY last_analyze;
```

---

## 23. 关键原则

1. **sys_ 前缀**：KingbaseES系统视图统一使用 `sys_` 前缀（非 `sys_`）
2. **Oracle兼容**：启用兼容模式后可使用 `v$` 风格视图名
3. **权限过滤**：`sys_stat_user_*` 只返回当前用户可访问的对象
4. **OID转换**：使用 `::regclass`、`::regtype` 将OID转为可读名称
5. **定义获取**：`sys_get_*def()` 系列函数获取对象完整定义
6. **统计重置**：维护后记得重置统计以获得准确基线
7. **信息模式**：`sys_information_schema` 提供SQL标准接口
8. **上下文过滤**：查询时排除 `sys` 和 `sys_information_schema` 模式
