# KingbaseES 证书认证与多重鉴别

kcert 系列认证方式支持在不依赖 SSL 的情况下使用证书进行强身份验证，可实现证书认证和密码认证的结合。支持 RSA 和 SM2 两种证书类型。

## 1. 概述

与传统的 cert 认证不同，kcert 不需要 SSL 连接。用户通过 `-C`/`-k` 命令行参数指定证书和密钥路径即可完成认证。

## 2. kcert 系列认证方式比较

| 认证方式 | 证书认证 | 密码认证 | 说明 |
|----------|---------|---------|------|
| kcert | 是 | 否 | 单证书认证 |
| kcert_scram | 是 | scram-sha-256 | 证书 + SCRAM 双重认证 |
| kcert_sm3 | 是 | SM3 哈希 | 证书 + SM3 双重认证 |
| kcert_scram_sm3 | 是 | scram-sm3 | 证书 + SCRAM-SM3 双重认证 |
| kcert_sm4 | 是 | SM4 | 证书 + SM4 双重认证 |

证书认证通过后，若为多重鉴别方式，服务端会返回密码加密认证方式，客户端再输入密码进行二次认证。

## 3. kingbase.conf 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| cert_type | rsa | 证书类型：rsa 或 sm2 |
| ca_cert_file | ca.crt | 根证书文件名，放置于 data 目录 |

```sql
-- 使用 SM2 证书
ALTER SYSTEM SET cert_type = sm2;
ALTER SYSTEM SET ca_cert_file = 'ca.pem';
SELECT sys_reload_conf();
```

使用 RSA 证书时可直接使用默认值。

## 4. SM2 证书生成

SM2 证书依赖 OpenSSL 1.1.1 以上版本。共6步生成根证书、客户端证书和密钥。

```bash
# 1. 生成根证书密钥
openssl ecparam -out ca.key -name SM2 -genkey

# 2. 生成根证书请求文件
openssl req -key ca.key -new -out ca.req

# 3. 生成根证书
openssl x509 -req -in ca.req -signkey ca.key -out ca.pem -days 3650

# 4. 生成 SM2 客户端密钥对
openssl ecparam -out uclient.key -name SM2 -genkey

# 5. 生成客户端证书请求文件
openssl req -key uclient.key -new -out uclient.req

# 6. 生成客户端证书
openssl x509 -req -in uclient.req -CA ca.pem -CAkey ca.key -out uclient.pem -CAcreateserial -days 3650

# 转为 DER 格式（JDBC 等接口需要）
openssl x509 -outform der -in uclient.pem -out uclient.der
```

生成后文件说明：
- ca.pem：根证书，放至服务端 data 目录
- uclient.pem/uclient.der：客户端证书
- uclient.key：客户端私钥

## 5. RSA 证书生成

### 带 PIN 码

```bash
# 1. 生成根证书请求文件和根私钥
openssl req -newkey rsa:2048 -keyout ./ca.key -keyform PEM -out ./ca.csr -outform PEM

# 2. 生成自签名 CA 证书（执行时提示输入 PIN 码）
openssl x509 -req -in ./ca.csr -out ./ca.crt -signkey ./ca.key -days 3650

# 3. 生成客户端私钥和证书请求文件（执行时提示设置 PIN 码）
openssl req -newkey rsa:1024 -keyout ./uclient.key -keyform PEM -out ./uclient.csr -outform PEM

# 4. 生成 CA 签署的客户端证书（执行时提示输入打开 ca.key 的 PIN 码）
openssl x509 -sha1 -req -in ./uclient.csr -CA ./ca.crt -CAkey ./ca.key \
    -CAcreateserial -out ./uclient.crt -days 3650 \
    -extfile /etc/pki/tls/openssl.cnf -extensions v3_req
```

PIN 码用于在读取密钥文件时对密钥解密。打开 ca.key 的 PIN 码与打开 client.key 的 PIN 码需分别保持一致。

### 不带 PIN 码

```bash
# 1. 生成 CA 证书请求文件
openssl req -newkey rsa:2048 -keyout ./ca.key -keyform PEM -out ./ca.csr -outform PEM

# 2. 自签名 CA 证书
openssl x509 -req -in ./ca.csr -out ./ca.crt -signkey ./ca.key -days 3650

# 3. 生成客户端私钥
openssl genrsa -out uclient.key 1024

# 4. 生成 CA 签署的客户端证书请求文件
openssl req -new -key uclient.key -out uclient.csr

# 5. 生成客户端证书
openssl x509 -sha1 -req -in ./uclient.csr -CA ./ca.crt -CAkey ./ca.key \
    -CAcreateserial -out ./uclient.crt -days 3650 \
    -passin pass:123456 -extfile /etc/pki/tls/openssl.cnf -extensions v3_req
```

## 6. sys_hba.conf 配置

```bash
# kcert 单证书认证
host  all  testuser  0.0.0.0/0  kcert

# kcert + scram-sha-256 双重认证
host  all  testuser  0.0.0.0/0  kcert_scram

# kcert + SM3 双重认证
host  all  testuser  0.0.0.0/0  kcert_sm3

# kcert + scram-sm3 双重认证
host  all  testuser  0.0.0.0/0  kcert_scram_sm3

# kcert + SM4 双重认证
host  all  testuser  0.0.0.0/0  kcert_sm4
```

注意：kcert 使用 `host` 而非 `hostssl`，因为不依赖 SSL。

## 7. ksql 连接参数

| 参数 | 说明 |
|------|------|
| -C | 客户端证书路径 |
| -k | 客户端私钥路径 |
| -K | PIN 码存储文件（passfile）路径 |
| -W | 强制提示输入密码（避免双重 PIN 码提示） |

### 基本连接

```bash
# kcert 单证书认证
ksql -d test -p 22223 -U testuser \
    -C /home/testuser/cert/uclient.crt \
    -k /home/testuser/cert/uclient.key \
    -h 10.12.1.30

# kcert_scram 双重认证（加 -W 避免重复输入 PIN 码）
ksql -d test -p 22223 -U testuser -W \
    -C /home/testuser/cert/uclient.crt \
    -k /home/testuser/cert/uclient.key \
    -h 10.12.1.30
```

带 PIN 码的密钥文件在连接时会弹出提示要求输入 PIN 码。加 `-W` 参数后先输入用户密码再输入 PIN 码，只需一次 PIN 码输入。

### Passfile 自动解码

适用于集群服务器间证书登录场景，支持 PIN 码自动输入。

```bash
# 1. 创建 passfile 文件
# 2. 将 PIN 码 base64 编码后写入
echo -n 123456cl | base64

# 3. 连接时使用 -K 指定 passfile
ksql -d test -p 22223 -U testuser -W \
    -C /home/testuser/cert/uclient.crt \
    -k /home/testuser/cert/uclient.key \
    -K /home/testuser/cert/passfile \
    -h 10.12.1.30
```

passfile 文件内容为 PIN 码的 base64 编码值。系统自动解码后填入 PIN 码，无需手动输入。

## 8. 集群配置注意事项

集群环境下，主备机普通用户（非集群用户）的证书认证配置一致，与单机相同。集群用户和物理备份认证不使用证书认证，必须使用 scram-sha-256：

```bash
# sys_hba.conf 最前端配置
local  all           all                scram-sha-256
host   esrep         esrep  0.0.0.0/0   scram-sha-256
host   replication   all    0.0.0.0/0   scram-sha-256
host   esrep         esrep  ::0/0       scram-sha-256
host   replication   all    ::0/0       scram-sha-256
```

上述内容需放置于 sys_hba.conf 最前端，否则集群同步和复制可能因证书认证失败。

## 9. 常见问题

### 问题1：SM2 证书生成失败

**原因**：OpenSSL 版本低于 1.1.1。

**排查**：
```bash
openssl version
```

### 问题2：连接时重复提示输入 PIN 码

**原因**：未加 `-W` 参数，数据库连接时有空连接步骤。

**解决**：添加 `-W` 参数使应用先提示用户密码再提示 PIN 码。

### 问题3：集群复制认证失败

**原因**：esrep/replication 连接配置了 kcert 认证。

**解决**：确保 esrep 和 replication 使用 scram-sha-256 认证，且配置在 sys_hba.conf 最前端。

## 最佳实践

1. RSA 证书用于通用场景，SM2 证书用于国密合规场景
2. 管理账户使用 kcert_scram 或 kcert_sm4 等多重认证
3. 集群环境务必将 esrep/replication 放在 sys_hba.conf 最前端
4. 自动化部署使用 passfile 避免手动输入 PIN 码
5. 保护客户端私钥文件权限：`chmod 600 uclient.key`
