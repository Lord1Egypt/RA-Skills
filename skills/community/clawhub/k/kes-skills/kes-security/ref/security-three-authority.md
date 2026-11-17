# KingbaseES 三权分立与受限DBA

三权分立将管理特权分别赋予数据库管理员、安全管理员和审计管理员，解决超级用户权力过度集中的问题。受限DBA进一步限制管理员权限。

## 1. 概述

KingbaseES 安全版本初始化后创建三个特权用户：

| 用户 | 简称 | 职责 |
|------|------|------|
| system | 数据库管理员 | 日常管理与自主存取控制 |
| sso | 安全管理员 | 强制访问规则制定、监督审计员和普通用户 |
| sao | 审计管理员 | 审计管理、监督管理员和安全员操作 |

## 2. 权限分离矩阵

### 审计约束

| 角色 | 修改审计参数 | 定义审计策略 | 查看审计记录 | 审计范围 |
|------|------------|------------|------------|---------|
| system | 不支持 | 不支持 | 不支持 | -- |
| sso | 不支持 | 可设置/删除对sao和普通用户的策略 | 可查看sao和普通用户的记录 | sao + 普通用户 |
| sao | 支持开关 | 可设置/删除对system和sso的策略 | 可查看system和sso的记录 | system + sso |

### 安全约束

| 角色 | 安全功能操作 |
|------|------------|
| system | 不支持 |
| sso | 支持开启安全GUC参数、设置/删除标记和策略 |
| sao | 不支持 |

### 用户管理互斥

- system 不能创建/修改 sso 和 sao，也不能将普通用户改为 sso/sao
- sso 只能创建/修改 sso，不能将 sso 改为非 sso
- sao 只能创建/修改 sao，不能将 sao 改为非 sao

## 3. sepapower 插件

sepapower 插件在数据库启动时默认加载，加载后三权分立功能自动生效。

**禁止卸载 sepapower 插件**，否则基于三权分立的权限管理功能将全部失效。

### 增强参数

#### sepapower.separate_power_grant

控制是否由 sso 用户控制 DCL 语句（默认 off）。

```sql
-- 开启：sso 可执行 GRANT/REVOKE 等 DCL 操作
ALTER SYSTEM SET sepapower.separate_power_grant = on;
SELECT sys_reload_conf();

-- 验证
SHOW sepapower.separate_power_grant;
-- on

-- sso 用户执行 DCL
\c - sso
GRANT SELECT ON t1 TO u1;
-- GRANT
```

关闭状态下 sso 执行 DCL 报错：
```
ERROR:  permission denied: sao and sso users are not allowed to use DDL and DCL
```

#### sepapower.check_noprivileges_grant

将无授权权限操作从 WARNING 提升为 ERROR（默认 off）。

```sql
-- 开启 DCL 报错等级提升
ALTER SYSTEM SET sepapower.check_noprivileges_grant = on;
SELECT sys_reload_conf();

-- 验证效果
\c - u1
REVOKE SELECT ON t1 FROM u2;
-- ERROR:  no privileges were granted for "t1"
```

关闭时上述操作仅输出 WARNING 并返回 GRANT。

## 4. sso_update_user 插件

限制 system 对用户的创建和修改能力。

### 加载配置

```sql
-- kingbase.conf
shared_preload_libraries = 'sso_update_user'

-- 重启数据库后创建扩展
\c - system
CREATE EXTENSION sso_update_user;
```

### 开启功能

```sql
\c - sso
ALTER SYSTEM SET sso_update_user.sso_update_user_enable = true;
SELECT sys_reload_conf();
```

### 开启后的限制

| 操作 | 限制 |
|------|------|
| CREATE ROLE/USER | system 创建普通用户时不可指定密码等选项 |
| ALTER ROLE/USER (密码) | 仅 sso 和普通用户本人可改密码；sso 只能将密码修改为 "12345678ab" |
| ALTER ROLE/USER (超级用户) | 超级用户只能修改超级用户或超级用户权限选项 |

### 卸载

```sql
-- kingbase.conf 中移除插件后重启
shared_preload_libraries = ''
```

## 5. 受限DBA

受限DBA功能将管理员权限限制到与普通用户一致。需由安全管理员 sso 确认后方可开启。

### 受限对象类型（16种）

Table、Database、Function、Language、Large Object、Namespace、Tablespace、Foreign Data Wrapper、Foreign Server、Type、Relation、Operator、Operator Class、Search Dictionary、Search Configuration、Conversion、Extension、Schema。

### 加载配置

```sql
-- kingbase.conf
shared_preload_libraries = 'restricted_dba, sepapower'

-- 重启数据库后
\c - system
CREATE EXTENSION restricted_dba;
```

### 开启功能

```sql
-- 必须由 sso 用户执行
\c - sso
ALTER SYSTEM SET restricted_dba.restricted_enable = true;
SELECT sys_reload_conf();

-- 验证
SHOW restricted_dba.restricted_enable;
-- on
```

### 卸载

```sql
-- kingbase.conf 中移除插件后重启
shared_preload_libraries = ''
```

## 6. 审计互斥关系

三权分立下审计权限的互斥设计：

- sao 监督 system 和 sso 的操作，但不能查看自己的审计记录
- sso 监督 sao 和普通用户的操作，但不能查看 system 的审计记录
- system 无法定义审计策略、修改审计参数、查看任何审计记录

这种设计确保每个管理员的行为都有其他管理员监督，形成完整的审计闭环。

## 7. 常见问题

### 问题1：sso 无法执行 DCL

**原因**：sepapower.separate_power_grant 未开启。

**解决**：
```sql
ALTER SYSTEM SET sepapower.separate_power_grant = on;
SELECT sys_reload_conf();
```

### 问题2：受限DBA开启后system无法访问对象

**原因**：受限DBA开启后system需通过显式授权访问非自身对象。

**解决**：sso 确认后按需调整 restricted_dba.restricted_enable 参数。

### 问题3：sepapower 插件无法卸载

这是预期行为。sepapower 为三权分立的基石，卸载后权限管理将全部失效。

## 最佳实践

1. 始终保留 sepapower 插件加载
2. 启用 sepapower.separate_power_grant 将 DCL 权力移交 sso
3. 启用 sso_update_user 限制 system 创建用户的能力
4. 生产环境建议开启受限DBA
5. 定期审查三个特权用户的操作日志
