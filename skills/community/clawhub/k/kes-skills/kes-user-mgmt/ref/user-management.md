# KingbaseES 用户管理与配置指南

包括用户/角色管理、权限控制、表空间配额、资源限制和配置管理。

## 1. 用户与角色管理

### 创建用户

```sql
-- 基本用户创建
CREATE USER app_user WITH ENCRYPTED PASSWORD 'P@ssw0rd123';

-- 带权限的用户
CREATE USER admin_user WITH ENCRYPTED PASSWORD 'Admin@123'
    SUPERUSER
    CREATEDB
    CREATEROLE
    CONNECTION LIMIT 50;

-- 带过期时间的用户
CREATE USER temp_user WITH ENCRYPTED PASSWORD 'Temp@123'
    VALID UNTIL '2026-12-31'
    CONNECTION LIMIT 10;

-- 带属性的完整用户
CREATE USER dev_user WITH
    ENCRYPTED PASSWORD 'Dev@123'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    IN ROLE developers
    CONNECTION LIMIT 20
    VALID UNTIL '2027-06-30';
```

### 修改用户

```sql
-- 修改密码
ALTER USER app_user WITH ENCRYPTED PASSWORD 'NewP@ssw0rd456';

-- 修改连接限制
ALTER USER app_user CONNECTION LIMIT 30;

-- 修改过期时间
ALTER USER app_user VALID UNTIL '2027-12-31';

-- 锁定用户
ALTER USER app_user ACCOUNT LOCK;

-- 解锁用户
ALTER USER app_user ACCOUNT UNLOCK;

-- 强制修改密码（下次登录时）
ALTER USER app_user PASSWORD 'temp_password' PASSWORD EXPIRE;

-- 撤销特权
ALTER USER admin_user NOSUPERUSER NOCREATEDB;
```

### 删除用户

```sql
-- 删除用户（无依赖对象）
DROP USER temp_user;

-- 删除用户并级联删除对象
DROP USER temp_user CASCADE;

-- 先查看用户拥有的对象
SELECT
    n.nspname AS schema,
    c.relname AS object_name,
    c.relkind AS type,
    sys_get_userbyid(c.relowner) AS owner
FROM sys_class c
JOIN sys_namespace n ON c.relnamespace = n.oid
WHERE c.relowner = (SELECT usesysid FROM sys_user WHERE usename = 'temp_user')
  AND c.relkind IN ('r', 'v', 'S', 'm');
```

### 角色管理

```sql
-- 创建角色
CREATE ROLE analysts;
CREATE ROLE reporters;
CREATE ROLE developers;

-- 授予角色属性
ALTER ROLE analysts NOLOGIN CREATEROLE;

-- 授予角色权限
GRANT CONNECT ON DATABASE test TO analysts;
GRANT USAGE ON SCHEMA public TO analysts;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analysts;

-- 用户加入角色
GRANT analysts TO analyst_user;

-- 设置默认角色
ALTER USER analyst_user SET ROLE analysts;

-- 角色继承
CREATE ROLE senior_analyst;
GRANT analysts TO senior_analyst;
-- senior_analyst 自动继承 analysts 的所有权限

-- 查看角色成员
SELECT
    r.rolname AS role_name,
    m.rolname AS member_name,
    admin_member
FROM sys_auth_members am
JOIN sys_authid r ON am.roleid = r.oid
JOIN sys_authid m ON am.member = m.oid;
```

### 用户查询

```sql
-- 查看所有用户
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

-- 查看用户权限
SELECT
    grantee,
    table_name,
    privilege_type,
    is_grantable
FROM sys_table_privileges
WHERE grantee = 'app_user'
ORDER BY table_name, privilege_type;

-- 查看用户所属角色
SELECT
    r.rolname AS role,
    ARRAY_agg(m.rolname) AS members
FROM sys_authid r
LEFT JOIN sys_auth_members am ON r.oid = am.roleid
LEFT JOIN sys_authid m ON am.member = m.oid
GROUP BY r.rolname;

-- 查看用户配置参数
SELECT usename, useconfig FROM sys_user WHERE useconfig IS NOT NULL;
```

---

## 2. 权限管理

### 权限级别

| 级别 | 权限 | 说明 |
|------|------|------|
| 系统级 | SUPERUSER, CREATEDB, CREATEROLE | 全局管理权限 |
| 数据库级 | CONNECT, TEMPORARY | 数据库访问 |
| Schema级 | USAGE, CREATE | 模式操作 |
| 对象级 | SELECT, INSERT, UPDATE, DELETE, ALTER, DROP | 表/视图操作 |
| 列级 | SELECT(column), UPDATE(column) | 列级控制 |
| 函数级 | EXECUTE | 函数/存储过程执行 |

### 授予权限

```sql
-- 数据库级权限
GRANT CONNECT ON DATABASE test TO app_user;
GRANT TEMPORARY ON DATABASE test TO app_user;

-- Schema级权限
GRANT USAGE ON SCHEMA public TO app_user;
GRANT CREATE ON SCHEMA public TO app_user;

-- 表级权限
GRANT SELECT ON employees TO app_user;
GRANT SELECT, INSERT, UPDATE ON employees TO app_user;
GRANT ALL ON employees TO app_user;

-- 批量授予
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;

-- 列级权限
GRANT SELECT(id, name) ON employees TO reporter_user;
GRANT UPDATE(salary) ON employees TO hr_user;

-- 函数权限
GRANT EXECUTE ON FUNCTION get_employee(INT) TO app_user;

-- 序列权限
GRANT USAGE, SELECT ON SEQUENCE emp_seq TO app_user;

-- 表空间权限
GRANT CREATE ON TABLESPACE sys_default TO app_user;
```

### 撤销权限

```sql
-- 撤销表权限
REVOKE SELECT ON employees FROM app_user;
REVOKE ALL ON employees FROM app_user;

-- 撤销Schema权限
REVOKE CREATE ON SCHEMA public FROM app_user;

-- 撤销所有权限
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM app_user;
REVOKE ALL PRIVILEGES ON DATABASE test FROM app_user;

-- 撤销角色成员资格
REVOKE analysts FROM analyst_user;
```

### 默认权限

```sql
-- 设置新表的默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO reporters;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE ON TABLES TO app_user;

-- 查看默认权限
SELECT
    defaclrole::regrole AS owner,
    defaclnamespace::regnamespace AS schema,
    defaclobjtype AS type,
    defaclacl AS privileges
FROM sys_default_acl;
```

### 权限最佳实践

```sql
-- 1. 最小权限原则
-- 创建应用专用角色
CREATE ROLE app_readonly NOLOGIN;
CREATE ROLE app_readwrite NOLOGIN;
CREATE ROLE app_admin NOLOGIN;

-- 授予最小权限
GRANT CONNECT ON DATABASE test TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

GRANT app_readonly TO app_readwrite;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_readwrite;

GRANT app_readwrite TO app_admin;
GRANT CREATE ON SCHEMA public TO app_admin;

-- 2. 用户分配到角色
CREATE USER user1 WITH PASSWORD 'xxx' IN ROLE app_readonly;
CREATE USER user2 WITH PASSWORD 'xxx' IN ROLE app_readwrite;
CREATE USER user3 WITH PASSWORD 'xxx' IN ROLE app_admin;
```

---

## 3. 表空间配额

### 设置配额

```sql
-- 为用户在表空间设置配额
ALTER USER app_user QUOTA 1024 ON sys_default;       -- 1GB
ALTER USER app_user QUOTA 5120 ON data_tbs;          -- 5GB
ALTER USER app_user QUOTA UNLIMITED ON temp_tbs;     -- 无限制

-- 为角色设置配额
ALTER ROLE developers QUOTA 2048 ON dev_tbs;
```

### 查看配额使用情况

```sql
-- 查看用户配额
SELECT
    usename,
    spcname,
    CASE quota
        WHEN -1 THEN 'UNLIMITED'
        ELSE sys_size_pretty(quota * 8192)
    END AS quota,
    sys_size_pretty(sys_tablespace_size(spcname)) AS tablespace_size
FROM sys_user_tablespace_quota q
JOIN sys_tablespace t ON q.tablespace = t.oid
JOIN sys_user u ON q.usename = u.usesysid;

-- 查看用户实际使用量
SELECT
    sys_catalog.sys_get_userbyid(r.relowner) AS owner,
    sys_catalog.sys_tablespace_location(
        sys_catalog.sys_tablespace_dblink(r.reltablespace)
    ) AS tablespace,
    sys_size_pretty(sum(sys_relation_size(r.oid))) AS total_size
FROM sys_class r
WHERE r.relkind = 'r'
GROUP BY r.relowner, r.reltablespace
ORDER BY sum(sys_relation_size(r.oid)) DESC;

-- 检查配额告警
SELECT
    usename,
    spcname,
    quota_mb,
    used_mb,
    ROUND(used_mb / NULLIF(quota_mb, 0) * 100, 1) AS usage_percent
FROM (
    SELECT
        q.usename,
        t.spcname,
        q.quota / 1024 AS quota_mb,
        (SELECT sum(sys_relation_size(c.oid)) / (1024*1024)
         FROM sys_class c
         WHERE c.relowner = q.usename
           AND c.reltablespace = q.tablespace
           AND c.relkind = 'r'
        ) AS used_mb
    FROM sys_user_tablespace_quota q
    JOIN sys_tablespace t ON q.tablespace = t.oid
    WHERE q.quota != -1
) sub
WHERE usage_percent > 80;
```

---

## 4. 资源限制

### 连接限制

```sql
-- 用户级连接限制
CREATE USER batch_user WITH PASSWORD 'xxx' CONNECTION LIMIT 5;
ALTER USER app_user CONNECTION LIMIT 20;

-- 全局连接限制
ALTER SYSTEM SET max_connections = 300;

-- 超级用户预留连接
ALTER SYSTEM SET superuser_reserved_connections = 5;

-- 查看连接使用情况
SELECT
    usename,
    count(*) AS connections,
    (SELECT CASE WHEN rolconnlimit = -1 THEN 'unlimited'
                 ELSE rolconnlimit::text END
     FROM sys_authid WHERE rolname = s.usename
    ) AS limit
FROM sys_stat_activity s
GROUP BY usename
ORDER BY connections DESC;
```

### 语句超时

```sql
-- 全局语句超时
ALTER SYSTEM SET statement_timeout = 60000;  -- 60秒

-- 用户级语句超时
ALTER USER batch_user SET statement_timeout = '300s';
ALTER USER report_user SET statement_timeout = '60s';

-- 会话级设置
SET statement_timeout = '30s';

-- 死锁检测超时
ALTER SYSTEM SET lock_timeout = '10s';
ALTER SYSTEM SET idle_in_transaction_session_timeout = '5min';
```

### 内存限制

```sql
-- 每查询内存
ALTER SYSTEM SET work_mem = '64MB';           -- 每个排序/哈希操作
ALTER SYSTEM SET maintenance_work_mem = '512MB';  -- vacuum/index创建

-- 用户级设置
ALTER USER report_user SET work_mem = '128MB';

-- 临时文件限制
ALTER SYSTEM SET temp_file_limit = 102400;  -- 100MB，0=无限制
```

---

## 5. 配置管理

### kingbase.conf 管理

```sql
-- 查看当前配置
SHOW ALL;

-- 查看特定配置
SHOW max_connections;
SHOW shared_buffers;
SHOW work_mem;
SHOW random_page_cost;

-- 会话级修改（仅当前会话）
SET work_mem = '128MB';
SET random_page_cost = 1.1;

-- 全局修改（立即生效，不持久化）
SET CONFIG 'work_mem'='128MB';

-- 持久化修改（写入配置表）
ALTER SYSTEM SET work_mem = '128MB';
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';

-- 从文件修改（直接编辑kingbase.conf）
-- $KINGBASE_HOME/data/kingbase.conf

-- 查看ALTER SYSTEM写入的值
SELECT name, setting, unit, source
FROM sys_config
WHERE source IN ('override', 'assign');

-- 重置为默认值
ALTER SYSTEM RESET work_mem;
ALTER SYSTEM RESET ALL;
```

### 配置分类

```sql
-- 内存相关
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';
ALTER SYSTEM SET huge_pages = 'try';

-- 连接相关
ALTER SYSTEM SET max_connections = 300;
ALTER SYSTEM SET superuser_reserved_connections = 5;
ALTER SYSTEM SET idle_session_timeout = 1800000;

-- WAL相关
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_keep_size = '2GB';
ALTER SYSTEM SET archive_mode = on;

-- 查询相关
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET default_statistics_target = 200;
ALTER SYSTEM SET parallel_setup_cost = 100;
ALTER SYSTEM SET parallel_tuple_cost = 0.01;
ALTER SYSTEM SET max_parallel_workers_per_gather = 2;

-- 日志相关
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_lock_waits = on;
```

### 配置生效

```sql
-- 重新加载配置（不需要重启）
SELECT sys_reload_conf();

-- 查看配置来源
SELECT name, setting, unit, source, sourcefile
FROM sys_config
WHERE name IN ('max_connections', 'shared_buffers', 'work_mem');

-- source说明：
-- default: 编译默认值
-- system: 系统配置表(kingbase.conf)
-- override: ALTER SYSTEM写入
-- assign: SET CONFIG写入

-- 需要重启的参数
SELECT name, context FROM sys_config WHERE context = 'postmaster';

-- 重启数据库
-- systemctl restart kingbase
-- 或
-- sys_ctl restart -D $KINGBASE_HOME/data
```

### 用户级配置

```sql
-- 为用户设置默认参数
ALTER USER report_user SET work_mem = '128MB';
ALTER USER report_user SET statement_timeout = '60s';
ALTER USER report_user SET search_path = '$user, public, report';

-- 为角色设置默认参数
ALTER ROLE analysts SET work_mem = '256MB';
ALTER ROLE analysts SET statement_timeout = '300s';

-- 查看用户配置
SELECT usename, useconfig FROM sys_user WHERE useconfig IS NOT NULL;

-- 查看角色配置
SELECT rolname, rolconfig FROM sys_authid WHERE rolconfig IS NOT NULL;
```

---

## 6. 存储管理

### 表空间管理

```sql
-- 创建表空间
CREATE TABLESPACE data_tbs
OWNER SYSTEM
LOCATION '/data/kingbase/data';

-- 创建带选项的表空间
CREATE TABLESPACE fast_tbs
OWNER SYSTEM
LOCATION '/data/kingbase/fast'
OPTIONS (random_page_cost = 1.1, effective_io_concurrency = 200);

-- 设置默认表空间
ALTER DATABASE test SET TABLESPACE fast_tbs;
ALTER USER app_user SET TABLESPACE fast_tbs;

-- 在表空间创建表
CREATE TABLE large_table (
    id INT PRIMARY KEY,
    data TEXT
) TABLESPACE data_tbs;

-- 迁移表到表空间
ALTER TABLE large_table SET TABLESPACE data_tbs;

-- 迁移索引到表空间
ALTER INDEX idx_large_table SET TABLESPACE fast_tbs;

-- 查看表空间
SELECT
    spcname,
    spcowner::regrole AS owner,
    sys_size_pretty(sys_tablespace_size(spcname)) AS size,
    spclocation,
    spcoptions
FROM sys_tablespace;

-- 删除表空间（必须先清空）
DROP TABLESPACE data_tbs;
```

### 大对象管理

```sql
-- 创建大对象
SELECT lo_from_bytea(0, E'\\xdeadbeef');

-- 读取大对象
SELECT lo_get(123456);

-- 写入大对象
SELECT lo_put(123456, 0, E'\\xdeadbeef');

-- 删除大对象
SELECT lo_unlink(123456);

-- 大对象表
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    data OID  -- 大对象引用
);

INSERT INTO documents (name, data)
VALUES ('report.pdf', lo_from_bytea(0, sys_read_binary_file('/path/report.pdf')));
```

---

## 7. 会话管理

### 活跃会话

```sql
-- 查看所有会话
SELECT
    pid,
    usename,
    datname,
    client_addr,
    client_port,
    state,
    backend_start,
    xact_start,
    query_start,
    state_change,
    wait_event_type,
    wait_event,
    query
FROM sys_stat_activity
WHERE datname IS NOT NULL
ORDER BY query_start;

-- 查看长时间运行的查询
SELECT
    pid,
    usename,
    NOW() - query_start AS duration,
    state,
    LEFT(query, 200) AS query_preview
FROM sys_stat_activity
WHERE state = 'active'
  AND query NOT LIKE '%sys_stat_activity%'
ORDER BY duration DESC;

-- 查看空闲连接
SELECT
    pid,
    usename,
    client_addr,
    NOW() - state_change AS idle_duration
FROM sys_stat_activity
WHERE state = 'idle'
ORDER BY idle_duration DESC;

-- 查看空闲事务（危险！）
SELECT
    pid,
    usename,
    NOW() - xact_start AS transaction_duration,
    LEFT(query, 200) AS query_preview
FROM sys_stat_activity
WHERE state = 'idle in transaction'
ORDER BY transaction_duration DESC;
```

### 终止会话

```sql
-- 取消当前查询
SELECT sys_cancel_pid(pid);

-- 终止整个会话
SELECT sys_terminate_pid(pid);

-- 批量终止空闲连接
SELECT sys_terminate_pid(pid)
FROM sys_stat_activity
WHERE state = 'idle'
  AND NOW() - state_change > INTERVAL '30 minutes'
  AND usename != 'SYSTEM';

-- 终止长时间运行的查询
SELECT sys_cancel_pid(pid)
FROM sys_stat_activity
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '10 minutes'
  AND usename != 'SYSTEM';

-- 终止特定用户的所有连接
SELECT sys_terminate_pid(pid)
FROM sys_stat_activity
WHERE usename = 'problem_user'
  AND pid != sys_backend_pid();
```

---

## 8. 常见问题

### 问题1：无法删除用户

**现象**：DROP USER 报错 "cannot drop role because it owns objects"。

**解决**：
```sql
-- 1. 查看用户拥有的对象
SELECT nspname, relname, relkind
FROM sys_class c
JOIN sys_namespace n ON c.relnamespace = n.oid
WHERE c.relowner = (SELECT usesysid FROM sys_user WHERE usename = 'target_user');

-- 2. 转移对象所有权
REASSIGN OWNED BY target_user TO SYSTEM;

-- 3. 删除用户拥有的所有对象
DROP OWNED BY target_user;

-- 4. 再删除用户
DROP USER target_user;
```

### 问题2：连接数超限

**现象**：FATAL: too many connections for role "app_user"。

**解决**：
```sql
-- 1. 提高连接限制
ALTER USER app_user CONNECTION LIMIT 50;

-- 2. 或终止空闲连接
SELECT sys_terminate_pid(pid)
FROM sys_stat_activity
WHERE usename = 'app_user'
  AND state = 'idle';

-- 3. 检查连接池配置
-- 应用侧可能创建了过多连接
```

### 问题3：权限不足

**现象**：permission denied for relation table_name。

**解决**：
```sql
-- 1. 检查当前用户
SELECT current_user, current_role;

-- 2. 检查表权限
SELECT grantee, privilege_type
FROM sys_table_privileges
WHERE table_name = 'target_table';

-- 3. 授予权限
GRANT SELECT ON target_table TO app_user;

-- 4. 检查Schema权限
GRANT USAGE ON SCHEMA public TO app_user;
```

### 问题4：配置修改不生效

**现象**：ALTER SYSTEM 后参数未改变。

**解决**：
```sql
-- 1. 检查是否需要重新加载
SELECT sys_reload_conf();

-- 2. 检查参数是否需要重启
SELECT name, context FROM sys_config WHERE name = 'target_param';
-- postmaster: 需要重启
-- usersignals: 需要重载
-- superuser: 超级用户可修改
-- internal: 运行时不可变

-- 3. 验证配置来源
SELECT name, setting, source FROM sys_config WHERE name = 'target_param';
```

---

## 最佳实践

1. **最小权限原则**：用户只授予必要的权限
2. **角色分层**：角色 → 用户，便于权限管理
3. **定期审计**：检查用户权限、过期账户
4. **连接池**：使用连接池管理连接数
5. **配额控制**：为非核心用户设置表空间配额
6. **超时设置**：防止长时间运行的查询占用资源
7. **会话监控**：定期清理空闲连接和空闲事务
