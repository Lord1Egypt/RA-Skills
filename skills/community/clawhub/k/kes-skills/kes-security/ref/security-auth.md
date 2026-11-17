# KingbaseES 强认证与数据脱敏指南

包括认证方式、密码策略、SSL/TLS、国密算法和数据脱敏。

## 1. 强认证概述

### 认证方式

KingbaseES 支持多种第三方身份验证服务：

| 认证方式 | 说明 |
|----------|------|
| scram-sha-256 | 密码认证，推荐使用 |
| md5 | 密码认证（较弱） |
| cert | SSL 客户端证书认证 |
| kcert | 证书登录，支持 RSA/SM2 |
| kcert_scram | 证书 + scram-sha-256 多重认证 |
| kcert_sm3 | 证书 + SM3 密码多重认证 |
| kcert_scram_sm3 | 证书 + scram-sm3 多重认证 |
| kcert_sm4 | 证书 + SM4 密码多重认证 |
| Kerberos | 集中身份鉴别系统 |
| LDAP | 外部目录服务认证 |
| RADIUS | 客户端/服务器安全协议 |
| GSSAPI | GSS 认证（仅 TCP/IP） |
| SSPI | Windows 安全支持提供者接口 |
| ident | 客户端 OS 用户映射（仅 TCP/IP） |
| peer | 本地连接 OS 用户验证 |
| PAM | 可插入认证模块 |
| bsd | BSD 认证服务 |
| trust | 无条件信任（仅本地/测试环境） |
| reject | 拒绝连接 |

### 认证配置

```bash
# sys_hba.conf 配置
# TYPE  DATABASE  USER        ADDRESS         METHOD

# 密码认证
host    all             all             192.168.1.0/24    scram-sha-256

# SSL 证书认证
hostssl all             admin_user      192.168.1.0/24    cert

# 国密证书 + SCRAM 多重认证
hostssl all             admin_user      192.168.1.0/24    kcert_scram

# 国密证书 + SM3 多重认证
hostssl all             gm_user         192.168.1.0/24    kcert_sm3

# Kerberos 认证
host    all             all             192.168.1.0/24    krb5

# LDAP 集成
host    all             all             192.168.1.0/24    ldap url=ldap://ldap.company.com:389 basedn=dc=company,dc=com

# RADIUS 认证
host    all             all             192.168.1.0/24    radius

# PAM 认证
host    all             SYSTEM          192.168.1.0/24    pam

# 本地信任（应急使用）
local   all             SYSTEM                              trust
```

---

## 2. 密码策略

### 密码复杂度

```sql
-- 启用密码策略
ALTER SYSTEM SET password_check_enable = on;

-- 设置密码参数
ALTER SYSTEM SET password_min_length = 12;
ALTER SYSTEM SET password_min_upper = 1;
ALTER SYSTEM SET password_min_lower = 1;
ALTER SYSTEM SET password_min_digit = 1;
ALTER SYSTEM SET password_min_special = 1;
ALTER SYSTEM SET password_history = 5;       -- 不能重用最近5次密码
ALTER SYSTEM SET password_max_age = 90;      -- 90天过期
ALTER SYSTEM SET password_min_age = 1;       -- 至少使用1天才能修改
CALL sys_reload_conf();
```

### 密码加密存储

```sql
-- kingbase.conf
password_encryption = scram    -- 推荐 scram-sha-256

-- 修改用户密码
ALTER USER app_user WITH ENCRYPTED PASSWORD 'NewP@ssw0rd!2026';
```

### 密码过期处理

```sql
-- 查看密码过期状态
SELECT
    usename,
    passwd_valid_until,
    CASE WHEN passwd_valid_until < NOW() THEN 'expired' ELSE 'valid' END AS status
FROM sys_user;

-- 强制用户下次登录修改密码
ALTER USER app_user VALID UNTIL '2026-12-31';
```

---

## 3. SSL/TLS 认证配置

> SSL/TLS 证书生成、服务端完整配置和传输加密细节参见 `security-transport.md`。本节仅列出认证相关的配置。

### kingbase.conf 配置

```bash
ssl = on
ssl_cert_file = '$KINGBASE_HOME/data/server.crt'
ssl_key_file = '$KINGBASE_HOME/data/server.key'
ssl_ca_file = '$KINGBASE_HOME/data/ca.crt'
```

### sys_hba.conf 认证方式

```bash
# SSL 证书认证
hostssl all     cert_user     0.0.0.0/0     cert

# 证书 + scram-sha-256 双重认证
hostssl all     admin_user    0.0.0.0/0     kcert_scram

# 证书 + SM3 多重认证
hostssl all     gm_user       0.0.0.0/0     kcert_sm3
```

> SM2 证书生成流程参见 `security-national-crypto.md`。

---

## 4. 国密认证配置

> 国密 SSL (gm_ssl) 完整配置参见 `security-transport.md` §6，SM2 证书生成参见 `security-national-crypto.md`。本节仅列出认证侧配置。

### 国密 kingbase.conf

```bash
ssl = on
gm_ssl = on
gm_ssl_cert_file = '$KINGBASE_HOME/data/gm_server.crt'
gm_ssl_key_file = '$KINGBASE_HOME/data/gm_server.key'
gm_ssl_cipher = 'SM2-SM3-SM4'
```

### 国密密码认证

```bash
# sys_hba.conf
hostssl all     all     192.168.1.0/24    kcert_scram_sm3

# 设置国密密码
ALTER USER gm_user WITH GM ENCRYPTED PASSWORD 'GMPassword123!';
```

### 国密算法对照

| 用途 | 国密算法 | 国际算法 |
|------|---------|---------|
| 非对称加密 | SM2 | RSA/ECC |
| 哈希 | SM3 | SHA-256 |
| 对称加密 | SM4 | AES |

---

## 5. 动态数据脱敏

### 概述

动态脱敏在查询时实时遮蔽敏感数据，仅安全员（sso）可配置。脱敏对应用程序透明，仅在 SQL 查询结果返回时更改数据。

### 启用数据脱敏

```sql
-- 1. kingbase.conf 配置
shared_preload_libraries = 'sys_anon'

-- 2. 开启脱敏开关
ALTER SYSTEM SET anon.enable = on;
CALL sys_reload_conf();

-- 3. 查看状态
SHOW anon.enable;

-- 4. 关闭脱敏
ALTER SYSTEM SET anon.enable = off;
CALL sys_reload_conf();
```

### 脱敏函数

| 函数 | 支持类型 | 说明 |
|------|---------|------|
| default | 所有类型 | 完整脱敏：字符→空值，数字→0，布尔→f，时间→1970-01-01 |
| partial(prefix, suffix) | varchar/char/text | 保留前 n 位和后 n 位，中间用 * 替代 |
| random_string | varchar/char/text | 生成随机字符串替代 |
| random_date | timestamp/date/time 等 | 生成 1900-01-01 至今的随机时间 |
| random_int | integer/smallint/bigint 等 | 生成 0 至类型最大值的随机数 |
| email_mask | varchar/char/text | 邮件专用：最后一个 . 之前全部替换为 * |

### 添加脱敏策略

```sql
-- 语法：anon.add_policy(policy_name, objname, username, func_desc, para_list)
-- 由 sso 用户执行

-- 默认脱敏
SELECT anon.add_policy('pol1', 't1.a', '', '', '');

-- 部分脱敏：保留前后各2位
SELECT anon.add_policy('pol2', 'public.t2.a', 'u1', 'partial', '2,2');

-- 随机字符串脱敏
SELECT anon.add_policy('pol3', 'tab1.b', 'u1', 'random_string', '');

-- 邮件脱敏
SELECT anon.add_policy('pol4', 'email_tab.email', 'u1', 'email_mask', '');
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| policy_name | 策略名，不可为空，必须唯一 |
| objname | 脱敏对象，格式为 schema.table.column（默认 public） |
| username | 被脱敏用户，为空则对所有用户生效 |
| func_desc | 脱敏函数名，为空则使用默认脱敏 |
| para_list | 函数参数，仅 partial 需要，如 "2,2" |

### 修改/删除脱敏策略

```sql
-- 修改策略
SELECT anon.alter_policy('pol1', 'u2', 'random_string', '');

-- 删除策略
SELECT anon.remove_policy('pol1');

-- 删除所有策略
SELECT anon.remove_policy('');
```

### 查询脱敏策略

```sql
SELECT * FROM anon.all_policy;
-- 字段：policy_name, table_name, schema_name, column_name, masking_user, masking_func, func_parameters
```

### 功能限制

- 脱敏策略仅对普通表、分区表和物化视图有效
- 不支持在脱敏表上建立物化视图
- 不支持普通视图配置脱敏策略
- 仅支持在分区表主表上配置
- 仅安全员 sso 可配置和查看

---

## 6. 应用级敏感数据保护

### 概述

对全部用户级对象进行敏感数据保护，仅特定应用可见真实数据。通过 `anon.anon_type = enc_show` 启用。

### 配置

```sql
-- 开启功能并配置应用白名单
ALTER SYSTEM SET anon.enable = on;
ALTER SYSTEM SET anon.anon_type = enc_show;
ALTER SYSTEM SET anon.application_name = 'kingbase';  -- 白名单应用
CALL sys_reload_conf();

-- 生成加密密钥
SELECT anon.gen_enc_key('123456');
ALTER SYSTEM SET anon.enc_key = 'csAI2Ru4v8QUp07Lh1bfjw==';
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| anon.anon_type | data_mask/enc_show，默认 data_mask |
| anon.application_name | 白名单应用名，用 ; 分隔，格式 appname[:username[,username]] |
| anon.enc_type | 加密算法，默认 sm4 |
| anon.enc_key | 加密密钥 |

:::note
应用级敏感数据保护与数据脱敏功能冲突，不可同时使用。
:::

---

## 7. 网络安全

### 连接加密

```bash
# sys_hba.conf 只允许 hostssl 条目
hostssl all     all     192.168.1.0/24    scram-sha-256
# 注释掉非 SSL 条目
# host all      all     192.168.1.0/24    scram-sha-256
```

### 登录限制

```sql
-- 限制登录失败次数
ALTER SYSTEM SET login_retry_limit = 5;
ALTER SYSTEM SET login_lock_duration = 300;  -- 锁定5分钟
CALL sys_reload_conf();
```

### IP 白名单

```bash
# sys_hba.conf — 只允许特定 IP
host    all     SYSTEM    10.0.0.1/32         scram-sha-256
host    all     app_user  10.0.1.0/24         scram-sha-256
host    all     all       0.0.0.0/0           reject
```

### 会话超时

```sql
-- 空闲会话超时
ALTER SYSTEM SET idle_session_timeout = 1800000;  -- 30分钟(ms)
CALL sys_reload_conf();

-- 语句超时
ALTER SYSTEM SET statement_timeout = 60000;  -- 60秒(ms)
```

---

## 8. 脱敏配置备份恢复

```bash
-- 使用 sso 用户备份脱敏配置
./sys_dump -d test -p 54321 -U sso -W -F c -f anon.dmp

-- 恢复到新实例
./sys_restore -p 54321 -U sso -W -d test anon.dmp
```

:::tip
- 不能指定 -a 参数，否则脱敏配置无法备份恢复
- 如指定 --section 参数，需指定为 post-data
:::

---

## 常见问题

### 问题1：脱敏策略不生效

**排查**：
```sql
-- 1. 检查脱敏开关
SHOW anon.enable;

-- 2. 检查插件是否加载
SHOW shared_preload_libraries;

-- 3. 查看策略配置
SELECT * FROM anon.all_policy;

-- 4. 确认当前角色
SELECT current_role;
```

### 问题2：SSL 连接失败

**排查**：
```bash
# 1. 检查 SSL 状态
ksql -c "SHOW ssl;"

# 2. 检查证书权限
ls -la $KINGBASE_HOME/data/server.*

# 3. 检查证书过期
openssl x509 -in $KINGBASE_HOME/data/server.crt -noout -dates
```

### 问题3：认证方式不生效

**排查**：
- sys_hba.conf 第一条匹配规则生效，检查顺序
- 确认认证方式与客户端连接类型匹配（host vs hostssl）
- 保留本地 trust 应急入口

---

## 最佳实践

1. **密码策略强制**：最小长度 12 位，复杂度要求
2. **多重认证**：管理账户使用 kcert_scram 或 kcert_sm4 等多重认证
3. **证书定期轮换**：每年更新一次证书
4. **脱敏默认开启**：开发/测试环境强制脱敏
5. **网络最小化**：只开放必要端口和 IP
6. **会话超时**：空闲 30 分钟自动断开
7. **等保合规**：国密算法 + 审计 + 脱敏
