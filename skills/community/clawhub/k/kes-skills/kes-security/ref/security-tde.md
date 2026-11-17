---
name: kes-security-tde
name_for_command: kes-security-tde
description: TDE 透明数据加密、防篡改、应用层加密函数、客体重用安全
---

# KingbaseES 数据加密保护

包括透明数据加密（TDE）、sysencrypt 插件、kdb_ledger 防篡改、应用层加密函数、配置步骤和常见问题。

## 1. 透明数据加密（TDE）

### 概述

透明加密对存储在表、表空间以及 WAL 日志中的敏感数据进行加密。加密对应用透明，授权用户访问时自动解密，无需修改应用程序。

**加密场景**：
- 磁盘泄露保护
- 备份文件加密
- 合规要求（等保三级、国密合规）

**加密组成**：
- **表加密**：对选定表的数据加密
- **表空间加密**：加密表空间中存储的所有数据
- **WAL 日志加密**：对 WAL 日志加密
- **临时文件加密**：对 syssql_tmp 下的临时文件加密

:::note
表空间加密和表加密互斥，同一加密对象不允许同时支持这两种加密方式。
:::

### 启用透明加密

```sql
-- 1. kingbase.conf 配置
shared_preload_libraries = 'sysencrypt'

-- 2. 重启数据库后创建扩展
CREATE EXTENSION sysencrypt;
```

### 加密算法

KingbaseES 内置支持以下算法：

| 算法 | 类型 | 说明 |
|------|------|------|
| SM4 | 分组加密 | 国密算法，合规首选 |
| RC4 | 流加密 | 内置支持 |

还支持用户自定义扩展加密算法：根据 `sysengine.h` 头文件编译设备库，放置到数据库 LIB 目录下，初始化时通过 `-e` 参数指定。

---

## 2. 表加密

### 创建加密表

```sql
-- 使用随机密钥
CREATE TABLE t2 (id int) ENCRYPTED;

-- 指定密钥（最大有效长度 16 字节）
CREATE TABLE t3 (id int) ENCRYPTED BY '12345678ab';

-- 指定加密方式
CREATE TABLE t5 (id int) ENCRYPTED BY 'method=sm4,key=12345678ab';

-- 仅指定加密方式
CREATE TABLE t7 (id int) ENCRYPTED BY 'method=sm4';
```

### 修改加密状态

```sql
-- 修改为加密
ALTER TABLE t1 ENCRYPTED;
ALTER TABLE t1 ENCRYPTED BY '12345678ab';

-- 修改为非加密
ALTER TABLE t1 UNENCRYPTED;
ALTER TABLE t1 NOT ENCRYPTED;

-- 修改加密算法和密钥
ALTER TABLE t1 ENCRYPTED BY 'key=12345678ab,method=sm4';
```

:::note
修改加密状态时可能会重新生成存储文件，大表需要占用大量资源。
:::

### 查询加密状态

```sql
-- 函数查询
SELECT sysencrypt.is_table_encrypted('tablename');

-- 视图查询
SELECT * FROM sysencrypt.sys_table_encrypt;
```

---

## 3. 表空间加密

### 创建加密表空间

```sql
-- 使用随机密钥
CREATE TABLESPACE tsp1 LOCATION '/tmp/tsp' WITH (encryption = true);

-- 指定密钥
CREATE TABLESPACE tsp2 LOCATION '/tmp/tsp2' WITH (encryption = true, enckey = 'k1ngb2se');

-- 指定加密方式
CREATE TABLESPACE tsp3 LOCATION '/tmp/tsp3' WITH (encryption = true, encmethod = 'sm4');
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| encryption | 是否为加密表空间，true/false |
| enckey | 用户自定义密钥，最大 16 字节，需包含字符和数字 |
| encmethod | 加密方式（设备或算法） |

### 默认加密开关

```sql
-- 设置默认对创建的用户表空间加密
ALTER SYSTEM SET sysencrypt.encrypt_user_tablespace = on;
CALL sys_reload_conf();

-- 查看当前状态
SHOW sysencrypt.encrypt_user_tablespace;
```

### 密钥保护

出于安全性考虑，即使用户指定了密钥，`sys_tablespace` 中也不会显示密钥原文。

---

## 4. WAL 日志加密

### 开启/关闭

```sql
-- 开启
ALTER SYSTEM SET wal_encryption = on;
CALL sys_reload_conf();

-- 关闭
ALTER SYSTEM SET wal_encryption = off;
CALL sys_reload_conf();

-- 查看状态
SHOW wal_encryption;
```

### 注意事项

- WAL 日志加密只能防止被加密的 WAL 日志泄露用户数据
- 加密功能从开启变为关闭后，全页写行为可能导致前面加密的内容出现在后面未加密的 WAL 日志中
- WAL 日志加密开启后，请谨慎关闭

---

## 5. 临时文件加密

### 开启/关闭

```sql
-- kingbase.conf 配置（需重启生效）
temp_file_encryption = on

-- 查看状态
SHOW temp_file_encryption;
```

:::note
临时文件加密密钥不持久保存，每次重启数据库时重新生成。关闭数据库后未被删除的临时文件将失效，下次启动后删除。
:::

---

## 6. 加密设备管理

### 查询加密设备

```sql
SELECT * FROM sysencrypt.show_encrypt_device;
```

**字段说明**：

| 字段 | 说明 |
|------|------|
| device | 加密设备名 |
| devicelib | 加密设备库名 |
| driverlib | 算法驱动库名 |
| maxkeylen | 密钥最大长度 |
| align | 算法对齐长度（分组算法为非 0 偶数，流算法为 0） |
| isdefault | 是否为默认加密设备 |
| isuse | 是否正在使用 |
| ip/port | 设备网络地址 |

### 注册/修改/删除加密设备

```sql
-- 注册加密设备
SELECT sysencrypt.load_encrypt_device('my_device', 'lib_device.so', 'lib_driver.so', 16, 0, '', null);

-- 删除加密设备
SELECT sysencrypt.unload_encrypt_device('my_device');
```

---

## 7. 加密备份

通过 sys_dump 指定 `-K` 参数实现加密备份（仅支持自定义格式 `-F c`）：

```bash
-- 加密备份
./sys_dump -p 54321 -U system -F c -K 123456 -f enc.dmp test

-- 解密还原
./sys_restore -p 54321 -U system -K 123456 -d test1 enc.dmp

-- 篡改后的文件无法还原
-- File SM3 HASH check failure 'enc_bak.dmp' failed.
```

---

## 8. 防篡改（kdb_ledger）

### 概述

防篡改融合区块链思想，将用户操作记录至两种历史表中：用户历史表和全局区块表。

- 用户表通过 `blockchain=true` 属性标识
- DML 操作自动在用户历史表和全局区块表（`sys_global_chain`）中记录
- 提供高性能校验接口验证数据一致性
- 支持历史表归档压缩

### 创建防篡改表

```sql
-- 1. 安装扩展
CREATE EXTENSION kdb_ledger;

-- 2. 创建防篡改表
CREATE TABLE usertable (id int, name text) WITH (blockchain=true);

-- 查看表结构，系统自动添加 hash 列
\d+ usertable

-- 对应的用户历史表在 blockchain 模式下创建
\d+ blockchain.usertable_16396_hist
```

**历史表字段**：

| 字段 | 说明 |
|------|------|
| rec_num | 记录编号 |
| hash_ins | 写入行的 hash 摘要 |
| hash_del | 删除行的 hash 摘要 |
| pre_hash | 当前数据整体 hash 摘要 |

### 数据操作

```sql
-- 写入：历史表记录 hash_ins
INSERT INTO usertable VALUES (1, 'bob');

-- 更新：历史表追加记录，hash_ins 为新行摘要，hash_del 为旧行摘要
UPDATE usertable SET name='bob2' WHERE id=1;

-- 删除：历史表记录 hash_del
DELETE FROM usertable WHERE id=1;

-- 查看全局区块表
SELECT * FROM sys_global_chain;
```

:::note
历史表只能追加不能修改。
:::

### 校验数据一致性

```sql
-- 普通用户接口（仅校验有权限的表）
SELECT blockchain.ledger_hist_check('bc_test', 'usertable');
SELECT blockchain.ledger_gchain_check('bc_test', 'usertable');

-- 安全员接口（校验所有防篡改表）
SELECT * FROM blockchain.all_ledger_hist_check();
SELECT * FROM blockchain.all_ledger_gchain_check();
```

- `ledger_hist_check`：校验用户表与历史表一致性
- `ledger_gchain_check`：校验用户表、历史表和全局区块表三者一致性

### 归档历史表

```sql
-- 指定表归档
SELECT blockchain.ledger_hist_archive('bc_test', 'usertable');

-- 安全员归档所有历史表
SELECT * FROM blockchain.all_ledger_hist_archive(1);
```

---

## 9. 应用层加密函数

与 TDE（透明数据加密）不同，这些函数需要应用程序显式调用，属于应用层数据加密。

### 算法支持

| 算法 | 内建实现 | OpenSSL 实现 | 类型 |
|------|---------|-------------|------|
| MD5 | 是 | 是 | 摘要 |
| SHA1 | 否 | 是 | 摘要 |
| SHA224/256/384/512 | 否 | 是 | 摘要 |
| Blowfish | 否 | 是 | 对称 |
| AES | 否 | 是 | 对称 |
| DES/3DES/CAST5 | 否 | 否 | 对称 |
| RC4 | 否 | 是 | 对称 |
| SM2 | 否 | 是 (OpenSSL >= 1.0.0) | 非对称 |
| SM3 | 是 | 是 (OpenSSL >= 1.0.0) | 摘要 |
| SM4 | 是 | 是 (OpenSSL >= 1.0.0) | 对称 |

SM2/SM3/SM4 依赖 OpenSSL 1.0.0 及以上版本。若版本低于 1.0.0，SM3/SM4 使用内建函数，SM2 不支持。

### 对称加密：encrypt / decrypt

```sql
FUNCTION encrypt(plain bytea, key bytea, type text) RETURNS bytea
FUNCTION decrypt(cipher bytea, key bytea, type text) RETURNS bytea
```

支持的 type 值：bf-cbc, bf-ecb, bf-cfb, des-ecb, des-cbc, des3-ecb, des3-cbc, cast5-ecb, cast5-cbc, aes-cbc

```sql
-- 加密
SELECT encode(encrypt('qwertyuiopasdfghjkl', '123456789', 'aes'), 'hex');

-- 解密
SET bytea_output TO escape;
SELECT decrypt(encrypt('qwertyuiopasdfghjkl', '123456789', 'aes'), '123456789', 'aes');
-- qwertyuiopasdfghjkl
```

### 带初始化向量：encrypt_iv / decrypt_iv

```sql
FUNCTION encrypt_iv(plain bytea, key bytea, iv bytea, type text) RETURNS bytea
FUNCTION decrypt_iv(cipher bytea, key bytea, iv bytea, type text) RETURNS bytea
```

```sql
-- 加密
SELECT encrypt_iv('qwertyuiopasdfghjkl', '123456789', '123456', 'aes');
-- \x1a8062925f728febf21949c8a1e585c34b379acaafa12f3902bc03e26e8697d4

-- 解密
SET bytea_output = 'escape';
SELECT decrypt_iv(
    encrypt_iv('qwertyuiopasdfghjkl', '123456789', '123456', 'aes'),
    '123456789', '123456', 'aes');
-- qwertyuiopasdfghjkl
```

### RC4

```sql
FUNCTION rc4(data bytea, key bytea, flag int4) RETURNS bytea
```

flag 参数：0=传统加密，1=传统解密，2=通用加密，3=通用解密。传统方式限制密钥最大 16 字节，通用方式无限制。

```sql
-- 加密
SELECT rc4('123456789', '123456789', 2);
-- \x05fb691574615fe1d8

-- 解密
SELECT rc4(rc4('123456789', '123456789', 2), '123456789', 3);
-- \x313233343536373839
```

### SM4 / SM4_ex

```sql
-- sm4 基本函数（等效于 sm4_ex 填充模式=0）
FUNCTION sm4(text, text, int)
-- 参数：数据、密钥、0=加密/1=解密

-- 加密
SELECT sm4('123456abcdef', '0123456789ABCDEF', 0);
-- \x354813a85f74b5089991d0a8337a4724

-- 解密
SELECT sm4(sm4('123456abcdef', '0123456789ABCDEF', 0), '0123456789ABCDEF', 1);
-- \x313233343536616263646566
```

sm4_ex 支持选择填充模式：

```sql
FUNCTION sm4_ex(bytea, bytea, int4, int4)
-- 参数：数据、密钥、0=加密/1=解密、填充模式 0=零填充/1=PKCS 填充
```

```sql
-- PKCS 填充模式加密
SELECT sm4_ex('123456abcdef', '0123456789ABCDEF', 0, 1);
-- \x9c66a6bb6b58e8731d70e9c71c76bcfc

-- PKCS 填充模式解密
SELECT sm4_ex(sm4_ex('123456abcdef', '0123456789ABCDEF', 0, 1), '0123456789ABCDEF', 1, 1);
-- \x313233343536616263646566
```

### 摘要/哈希函数

```sql
FUNCTION digest(data bytea, type text) RETURNS bytea
FUNCTION digest(data text, type text) RETURNS bytea
```

支持 type 值：md5, sha1, sha224, sha256, sha384, sha512

```sql
SET bytea_output TO hex;
SELECT digest('12345678', 'md5');
-- \x25d55ad283aa400af464c76d713c07ad

SELECT digest('12345678', 'sha256');
-- \xef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f
```

SM3 国密摘要：

```sql
SELECT sm3('123456abcdef');
-- 977ca9e6b830b32808e36f01745f6a3e4e7539115b56f6512144f746f84f3b2f
```

### 非对称加密：SM2

SM2 加密函数依赖 kbcrypto 插件。

```sql
-- 生成密钥对
SELECT sm2_genkeypair();
-- 返回 PEM 格式的私钥和公钥

-- 加密（使用公钥）
SELECT sm2_encrypt('hello~', 'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...');
-- 306f02200e467e63de5937b645efc7110f58...

-- 解密（使用私钥）
SELECT sm2_decrypt('306f02200e467e63de5937b645efc7110f58...', 'MHcCAQEEIE9Gm3HK...');
-- hello~

-- 签名（使用私钥）
SELECT sm2_sign('hello sign~', 'MHcCAQEEIE9Gm3HK...');
-- 304502205314636312faba3b0661fbfe0f40...

-- 验签（使用公钥）
SELECT sm2_verify('hello sign~', '304502205314636312faba3b0661fbfe0f40...', 'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...');
-- t
```

### 非对称加密：RSA

```sql
-- 加密
SELECT rsa_encrypt(plaintext, public_key);

-- 解密
SELECT rsa_decrypt(ciphertext, private_key);
```

### 与 TDE 对比

| 特性 | 内置加密函数 | TDE（透明数据加密） |
|------|------------|-------------------|
| 透明性 | 不透明，应用需显式调用 | 透明，对应用无感知 |
| 粒度 | 列/字段级 | 表空间级 |
| 加密时机 | 应用层加密后存储 | 存储层写入磁盘时加密 |
| 密钥管理 | 应用自行管理 | 数据库 KMS 管理 |
| 适用场景 | 敏感字段精细加密 | 整体数据存储加密 |

---

## 10. 配置流程

### 完整配置步骤

```sql
-- 1. 加载插件
-- kingbase.conf: shared_preload_libraries = 'sysencrypt'

-- 2. 重启数据库后创建扩展
CREATE EXTENSION sysencrypt;

-- 3. 创建加密表空间
CREATE TABLESPACE secure_tbs LOCATION '/data/secure' WITH (encryption = true);

-- 4. 在加密表空间创建表
CREATE TABLE sensitive_data (id INT PRIMARY KEY, data TEXT) TABLESPACE secure_tbs;

-- 5. 或直接创建加密表
CREATE TABLE encrypted_table (id int) ENCRYPTED;

-- 6. 开启 WAL 加密（可选）
ALTER SYSTEM SET wal_encryption = on;
CALL sys_reload_conf();

-- 7. 开启临时文件加密（可选，需重启）
-- kingbase.conf: temp_file_encryption = on
```

### 集群支持

- 主库使用表或表空间加密，相关信息自动同步到备库
- 加密密钥变更也会自动同步
- WAL 日志加密在传输过程中也保持加密状态

---

## 常见问题

### 问题1：加密性能影响

**解决**：
- 只加密敏感数据，非敏感数据不加密
- 使用内置 SM4/RC4 算法，性能开销较小
- 增大 shared_buffers 缓存命中率

### 问题2：SM2 函数报错

**原因**：OpenSSL 版本低于 1.0.0 或未加载 kbcrypto 插件。

**排查**：
```bash
openssl version
```

### 问题3：sm4 解密结果非原文

**原因**：填充模式不匹配。sm4 默认使用零填充（模式 0），sm4_ex 可指定 PKCS 填充（模式 1）。加解密必须使用相同填充模式。

### 问题4：表加密与非加密互斥

**说明**：表空间加密和表加密方式互斥，同一加密对象不允许同时支持这两种加密方式。

### 问题5：防篡改校验失败

**排查**：
- 确认数据未被非法修改
- 检查全局区块表 `sys_global_chain` 记录是否完整
- 归档操作不影响校验结果

### 问题6：WAL 日志加密关闭风险

**说明**：WAL 日志加密开启后，全页写行为可能导致前面加密的内容出现在后面未加密的 WAL 日志中。开启后请谨慎关闭。

---

## 最佳实践

1. **密钥安全管理**：加密设备密钥与数据分离存储
2. **分级加密**：只加密敏感数据，平衡性能与安全
3. **国密合规**：等保项目优先使用 SM4 算法
4. **防篡改谨慎使用**：仅对核心财务数据启用
5. **备份加密**：使用 sys_dump `-K` 参数加密备份文件
6. **集群环境**：确保主备加密配置一致
7. **应用层加密**：密码存储使用 sm3() 单向哈希；敏感字段加密配合应用层密钥管理
