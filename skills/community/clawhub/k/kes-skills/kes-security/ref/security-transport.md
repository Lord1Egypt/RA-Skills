# KingbaseES 安全传输

通过 SSL/TLS 协议保障客户端与服务端之间数据安全传输和数据完整性保护。

## 1. 概述

SSL 安全传输分为两个阶段：

1. **认证阶段**：客户端验证服务端证书，服务端验证客户端证书，确保双方可信
2. **数据传输阶段**：使用 SSL 协商的加密算法和密钥进行加密通信

要求客户端和服务端均安装 OpenSSL。

## 2. TLS 1.3 加密套件

KingbaseES 采用 TLS 1.3 协议标准，支持以下加密算法套件：

| OpenSSL 套件名 | IANA 套件名 | 安全程度 |
|---------------|-------------|---------|
| ECDHE-RSA-AES128-GCM-SHA256 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | HIGH |
| ECDHE-RSA-AES256-GCM-SHA384 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | HIGH |
| ECDHE-ECDSA-AES128-GCM-SHA256 | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | HIGH |
| ECDHE-ECDSA-AES256-GCM-SHA384 | TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | HIGH |

## 3. SSL 模式

| sslmode | 窃听保护 | MITM 保护 | 说明 |
|---------|---------|----------|------|
| disable | 否 | 否 | 禁用 SSL |
| allow | 可能 | 否 | 优先非加密，若服务器要求则加密 |
| prefer | 可能 | 否 | 优先加密（默认值） |
| require | 是 | 否 | 强制加密，不验证证书 |
| verify-ca | 是 | 取决于 CA 策略 | 验证服务器证书 |
| verify-full | 是 | 是 | 验证证书和主机名 |

生产环境推荐使用 `verify-full`。

## 4. 服务端配置

### kingbase.conf

```sql
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'root.crt'
# ssl_crl_file = ''
# ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'
```

### 证书文件

| 文件 | 说明 |
|------|------|
| ssl_cert_file | 服务器证书，发送给客户端证明身份 |
| ssl_key_file | 服务器私钥 |
| ssl_ca_file | 可信 CA 证书，用于验证客户端证书 |
| ssl_crl_file | 证书撤销列表 |

### sys_hba.conf

```bash
# 仅加密传输，不验证客户端证书
hostssl all all 127.0.0.1/32 scram-sha-256

# 加密传输并验证客户端证书
hostssl all all 127.0.0.1/32 scram-sha-256 clientcert=1

# 强制 SSL，拒绝非 SSL 连接
# hostssl 要求 SSL，host 不要求
# 将 host 行注释掉，仅保留 hostssl 行即可强制所有连接使用 SSL
```

`hostssl` 与 `host` 的区别：`hostssl` 条目仅匹配 SSL 连接，`host` 条目仅匹配非 SSL 连接。将 `host` 行注释后仅保留 `hostssl` 可强制所有连接使用 SSL。

### clientcert 认证选项

- 未指定或 `clientcert=0`：仅客户端配置了 CA 文件时，服务器根据 CA 文件验证客户端证书
- `clientcert=1`：在 hostssl 行上验证客户端证书，适用于所有认证方法

## 5. 双向认证流程

### 客户端证书验证服务器

1. 服务端向客户端发送 server.crt 证明身份
2. 客户端用 `~/.kingbase/root.crt` 中的 CA 验证服务端证书
3. 验证通过后建立加密通道

### 服务器证书验证客户端

1. 客户端发送 `~/.kingbase/kingbase.crt` 证书
2. 服务端用 `ssl_ca_file` 验证客户端证书
3. 需在 sys_hba.conf 中配置 `clientcert=1` 或使用 `cert` 认证方法

## 6. 国密 SSL (gm_ssl) 配置

```sql
# kingbase.conf
ssl = on
gm_ssl = on
gm_ssl_cert_file = '$KINGBASE_HOME/data/gm_server.crt'
gm_ssl_key_file = '$KINGBASE_HOME/data/gm_server.key'
gm_ssl_cipher = 'SM2-SM3-SM4'
```

## 7. 数据完整性保护

### 存储完整性

通过数据块头"数据水印"实现存储完整性校验。每次读磁盘时自动校验，每次写磁盘时自动更新水印。

```bash
# 初始化时指定校验算法
initdb -a sm3 -D datadir

# 使用 sys_checksums 工具启用/禁用
sys_checksums -e -D datadir          # 启用默认算法
sys_checksums -d -a sm3 -D datadir   # 禁用，指定 sm3

# 查看当前校验算法
sys_controldata -D datadir
# Data page checksum version: 0=关闭, 1=CRC, 2=SM3, 3=SM3_HMAC
```

### 传输完整性

通过 SSL 通信保障传输完整性，配置方法同 SSL 传输加密。

## 8. 常见问题

### 问题1：SSL 连接建立失败

**排查**：
```bash
# 检查 SSL 状态
ksql -c "SHOW ssl;"

# 检查证书权限（必须为 0600 或更严格）
ls -la $KINGBASE_HOME/data/server.*

# 检查证书有效期
openssl x509 -in $KINGBASE_HOME/data/server.crt -noout -dates
```

### 问题2：客户端无法验证服务器证书

**原因**：`~/.kingbase/root.crt` 不存在或包含错误的 CA 证书。

**解决**：将根证书放置到客户端 `~/.kingbase/root.crt`（Linux）或 `%APPDATA%\kingbase\root.crt`（Windows）。

## 最佳实践

1. 生产环境使用 `verify-full` 模式
2. 仅保留 hostssl 条目，注释 host 条目强制加密
3. 配合 `ssl_ca_file` 验证客户端证书
4. 启用数据页完整性校验（SM3 或 SM3_HMAC）
5. 证书文件权限设为 0600
