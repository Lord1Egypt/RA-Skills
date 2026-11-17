# KingbaseES 数据库审计配置指南

包括审计策略配置、审计日志管理、入侵检测、审计记录管理和常见问题。

## 1. 审计概述

### 审计类型

KingbaseES 通过 sysaudit 插件实现审计功能，分为三种类型：

- **服务器事件审计**：数据库启动、停止、配置重载、用户登录/登出
- **语句级别审计**：DDL、DML、DQL、DCL、TCL 等语句引发的事件
- **模式对象级别审计**：在确定模式对象上的 SELECT/DML 操作（表、视图、物化视图、过程、函数、序列）

:::note
规则仅对当前设置了规则的数据库生效。若要审计多个数据库，需为每个数据库单独设置审计规则。
:::

### 启用审计

```sql
-- 1. kingbase.conf 配置
shared_preload_libraries = 'sysaudit'

-- 2. 开启审计开关
ALTER SYSTEM SET sysaudit.enable = on;
CALL sys_reload_conf();

-- 3. 关闭审计
ALTER SYSTEM SET sysaudit.enable = off;
CALL sys_reload_conf();
```

### 审计相关参数

| 参数 | 说明 |
|------|------|
| sysaudit.enable | 审计总开关，默认 off |
| sysaudit.serverevent | 服务器事件审计，默认 off |
| sysaudit.userevent | 用户事件（登录/退出）审计，默认 off |
| sysaudit.syntaxerror | 语法错误审计，默认 off |
| sysaudit.ids | 入侵检测开关，默认 off |
| sysaudit.shared_cache | 审计共享内存大小，默认 10MB |
| sysaudit.bgw_workers | 审计后台进程数，默认 1 |
| sysaudit.all_error | 审计全部错误事件 |
| sysaudit.report_log | 审计日志外发 |

### 审计记录查看

审计记录存储在 security 数据库下：

- **审计员 sao** 查询 `sysaudit_record_sao`：可查看超级用户和安全员 sso 的审计日志
- **安全员 sso** 查询 `sysaudit_record_sso`：可查看普通用户和审计员 sao 的审计日志

```sql
-- sao 查看审计记录
\c security sao
SELECT * FROM sysaudit_record_sao ORDER BY audit_ts DESC LIMIT 100;

-- sso 查看审计记录
\c security sso
SELECT * FROM sysaudit_record_sso ORDER BY audit_ts DESC LIMIT 100;
```

---

## 2. 审计策略配置

### 语句级别审计

使用 `sysaudit.set_audit_stmt()` 设置语句级审计。

```sql
-- 审计 system 用户的 INSERT 操作
SELECT sysaudit.set_audit_stmt('INSERT TABLE', 'system', 'public', 't1');

-- 审计 system 用户的所有 CREATE TABLE 操作
SELECT sysaudit.set_audit_stmt('CREATE TABLE', 'system', null, null);

-- 审计 user_a 的 ALTER TABLE 操作
SELECT sysaudit.set_audit_stmt('ALTER TABLE', 'user_a', null, null);
```

**支持的审计类型**：ALL、CREATE TABLE/DROP TABLE/ALTER TABLE、CREATE INDEX/DROP INDEX/ALTER INDEX、CREATE VIEW/DROP VIEW/ALTER VIEW、CREATE SCHEMA、CREATE SEQUENCE/DROP SEQUENCE/ALTER SEQUENCE、CREATE FUNCTION/DROP FUNCTION/ALTER FUNCTION、CREATE PROCEDURE/DROP PROCEDURE/ALTER PROCEDURE、CREATE TABLESPACE/DROP TABLESPACE/ALTER TABLESPACE、CREATE USER/ALTER USER/DROP USER、INSERT TABLE/UPDATE TABLE/DELETE TABLE/TRUNCATE TABLE、SELECT TABLE、COPY FROM/COPY TO、GRANT、BEGIN/COMMIT/ROLLBACK/SAVEPOINT 等。

:::warning
不推荐使用 ALL 类型审计，对性能有影响。ALL 类型可以设置语句级和模式对象级，但都不能指定对象。
:::

### 模式对象级别审计

使用 `sysaudit.set_audit_object()` 设置对象级审计。

```sql
-- 审计 user1 对 public.t1 表的任意操作
SELECT sysaudit.set_audit_object('TABLE', 'user1', 'public', 't1');

-- 审计所有用户对 public 模式下所有表的操作
SELECT sysaudit.set_audit_object('TABLE', null, 'public', null);
```

**支持的审计对象类型**：TABLE、VIEW、MATERIALIZED VIEW、PROCEDURE、FUNCTION。

### 取消审计

```sql
-- 取消指定编号的审计规则
SELECT sysaudit.remove_audit(16387);

-- 取消所有审计规则
SELECT sysaudit.remove_audit(null);
```

### 查询审计规则

```sql
-- 查看所有审计规则
SELECT * FROM sysaudit.all_audit_rules;

-- 字段说明：
-- audit_id：审计策略编号
-- audit_target：审计目标（SQL 语句 / Object 对象）
-- audit_type：审计类型
-- audit_users：审计用户
-- audit_schema：审计模式
-- audit_objname：审计对象名
-- audit_objoid：审计对象 ID
-- creator_name：策略设置者角色
```

---

## 3. 审计入侵检测

### 功能简介

入侵检测系统（IDS）实时监控数据库中的可疑活动和未授权访问。当检测到侵害行为次数达到阈值时，服务器将自动断开连接。

### 开启入侵检测

```sql
ALTER SYSTEM SET sysaudit.ids = on;
CALL sys_reload_conf();
```

### 创建入侵检测规则

```sql
-- 语法
SELECT sysaudit.create_ids_rule(
    rulename,        -- 规则名（唯一，大小写敏感）
    actionname,      -- 审计类型
    username,        -- 审计用户名，null 表示所有用户
    schname,         -- 审计模式名
    objname,         -- 审计对象名
    when_ever,       -- ALL/SUCCESSFUL/FAILED，默认 FAILED
    ip,              -- IP 列表，null 表示所有 IP
    start_end_time,  -- 时间段，如 '09:00:00 TO 10:00:00'
    interval_time,   -- 时间间隔（分钟）
    times            -- 检测次数阈值
);

-- 示例：10 分钟内连续 2 次 INSERT 操作触发入侵检测
SELECT sysaudit.create_ids_rule(
    'rule1', 'INSERT TABLE', null, null, null,
    'ALL', null, null, 10, 2
);
```

### 删除/查看入侵检测规则

```sql
-- 删除指定规则
SELECT sysaudit.drop_ids_rule('rule1');

-- 删除所有规则
SELECT sysaudit.drop_ids_rule(null);

-- 查看所有规则
SELECT sysaudit.show_ids_rules();
```

### 邮件告警

```sql
-- 开启邮件告警
ALTER SYSTEM SET sysaudit.ids_mail_enable = true;

-- 配置邮件参数（通过 send_mails 插件）
-- send_mails.ids_mail_server：邮件服务器
-- send_mails.ids_mail_port：端口号
-- send_mails.ids_mail_login：用户名
-- send_mails.ids_mail_password：密码
-- send_mails.ids_mail_from：发送方
-- send_mails.ids_mail_to：接收方
```

---

## 4. 审计配置备份恢复

### 备份

```bash
-- 使用 sao 用户备份
./sys_dump -d test -p 54321 -U sao -W -F c -f audit_sao.dmp

-- 使用 sso 用户备份
./sys_dump -d test -p 54321 -U sso -W -F c -f audit_sso.dmp
```

### 恢复

```bash
./sys_restore -p 54321 -U sao -W -d test audit_sao.dmp
./sys_restore -p 54321 -U sso -W -d test audit_sso.dmp
```

:::tip
- sys_dump 和 sys_restore 不能指定 -a 参数，否则审计配置无法备份恢复
- 如指定 --section 参数，需指定为 post-data
- 数据库升级时也可用此方法升级审计配置
:::

---

## 5. 审计记录管理

### 手动转储

```sql
-- 设置转储目录
ALTER SYSTEM SET sysaudit.auditlog_dump_dir = '/home/test/audlog';
CALL sys_reload_conf();

-- 转储 1 天之前的审计日志
SELECT sysaudit.dump_auditlog(1);

-- 查看转储文件
SELECT sysaudit.show_audlog_dump_file();

-- 恢复转储文件
SELECT sysaudit.restore_auditlog('AUDIT_DUMP_FILE-2021-12-10_170855');
```

### 自动转储

| 参数 | 说明 |
|------|------|
| sysaudit.enable_auto_dump_auditlog | 自动转储开关，默认 false |
| sysaudit.dump_type | size/interval/both，默认 size |
| sysaudit.max_auditlog_size | 审计表最大占用空间，默认 16MB |
| sysaudit.audit_alarm_percent | 触发转储时占用比例，默认 80% |
| sysaudit.dump_interval | 转储时间间隔（分钟），默认 30 |
| sysaudit.auditlog_auto_dump_days | 转储多少天前的记录，默认 0 |

---

## 6. 完整示例

```sql
-- 1. system 用户创建测试表
\c - system
CREATE TABLE t1 (a int);

-- 2. sao 用户开启审计、配置规则
\c - sao
ALTER SYSTEM SET sysaudit.enable = on;
CALL sys_reload_conf();
SELECT sysaudit.set_audit_stmt('INSERT TABLE', 'system', 'public', 't1');

-- 3. system 执行操作触发审计
\c - system
INSERT INTO t1 VALUES (1);

-- 4. sao 查看审计日志
\c security sao
SELECT COUNT(*) FROM sysaudit_record_sao WHERE opr_type = '写入';

-- 5. sao 取消审计规则
\c test sao
SELECT sysaudit.remove_audit(null);
ALTER SYSTEM SET sysaudit.enable = off;
CALL sys_reload_conf();
```

---

## 常见问题

### 问题1：审计规则不生效

**排查**：
```sql
-- 1. 检查审计开关
SHOW sysaudit.enable;

-- 2. 检查插件是否加载
SELECT name, setting FROM sys_settings WHERE name = 'shared_preload_libraries';

-- 3. 检查规则配置
SELECT * FROM sysaudit.all_audit_rules;

-- 4. 确认规则对当前数据库生效
```

### 问题2：审计性能影响

**解决**：
- 避免使用 ALL 类型审计，尽量指定具体的审计类型
- 只审计必要的用户和操作
- 将审计记录转储到独立存储
- 定期清理过期审计记录

### 问题3：无法查看审计日志

**排查**：
- 确认以 sao 或 sso 身份连接 security 数据库
- sao 查看 sysaudit_record_sao，sso 查看 sysaudit_record_sso
- 如有修改 sao 密码的情况，需使用 sys_encpwd 工具配置密码

---

## 最佳实践

1. **最小化审计范围**：只审计必要的操作和用户
2. **定期转储审计记录**：设置自动转储，防止审计表膨胀
3. **独立存储审计日志**：转储目录与数据目录分离
4. **三权分立**：sao（审计员）和 sso（安全员）分离管理
5. **入侵检测**：对敏感操作开启入侵检测，设置合理阈值
6. **异地备份**：审计日志定期异地备份，防止篡改
