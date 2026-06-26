# 证书与 TLS 管理

## 目录

- [1. TLS/SSL 基础概念](#1-tlsssl-基础概念)
- [2. OpenSSL 证书操作](#2-openssl-证书操作)
- [3. Let's Encrypt 自动证书](#3-lets-encrypt-自动证书)
- [4. 私有 CA 搭建](#4-私有-ca-搭建)
- [5. 双向 TLS（mTLS）](#5-双向-tlsmtls)
- [6. 证书部署与配置](#6-证书部署与配置)
- [7. 证书监控与自动续期](#7-证书监控与自动续期)
- [8. 常见故障排查](#8-常见故障排查)

---

## 1. TLS/SSL 基础概念

### 1.1 证书链结构

```text
Root CA（根证书）
  └── Intermediate CA（中间证书）
        └── Server Certificate（服务器证书）

浏览器/客户端信任 Root CA → 验证 Intermediate CA → 验证 Server Certificate
```

### 1.2 证书文件类型

```text
文件格式        扩展名              说明
─────────────────────────────────────────────
PEM             .pem .crt .cer     Base64 编码，最常用
DER             .der .cer          二进制编码
PKCS#12/PFX     .p12 .pfx          包含证书+私钥，密码保护
PKCS#7          .p7b .p7c          证书链（不含私钥）

关键文件：
- 私钥（Private Key）    .key     — 绝密！权限必须 600
- 证书（Certificate）    .crt     — 公开
- 证书签名请求（CSR）    .csr     — 提交给 CA 签名
- CA 证书链              .chain   — 中间证书 + 根证书
- 完整链                 .fullchain — 服务器证书 + 中间证书
```

### 1.3 常用加密算法

```text
密钥类型        推荐长度      说明
─────────────────────────────────────────
RSA             2048/4096    兼容性最好，密钥较长
ECDSA           P-256/P-384  密钥短、性能好、安全性高
Ed25519         256          最新，速度最快（部分旧系统不支持）
```

---

## 2. OpenSSL 证书操作

### 2.1 生成私钥

```bash
# RSA 私钥
openssl genrsa -out server.key 2048
openssl genrsa -aes256 -out server.key 4096   # 带密码保护

# ECDSA 私钥（推荐）
openssl ecparam -genkey -name prime256v1 -out server.key

# Ed25519 私钥
openssl genpkey -algorithm Ed25519 -out server.key

# 查看私钥信息
openssl rsa -in server.key -text -noout
openssl ec -in server.key -text -noout

# 去除私钥密码
openssl rsa -in server.key -out server-nopass.key
```

### 2.2 生成 CSR

```bash
# 交互式生成 CSR
openssl req -new -key server.key -out server.csr

# 非交互式生成 CSR
openssl req -new -key server.key -out server.csr \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=MyCompany/OU=IT/CN=www.example.com"

# 带 SAN（Subject Alternative Name）的 CSR
cat > san.cnf << 'EOF'
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C = CN
ST = Guangdong
L = Shenzhen
O = MyCompany
CN = www.example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = www.example.com
DNS.2 = example.com
DNS.3 = *.example.com
IP.1 = 10.0.0.1
EOF

openssl req -new -key server.key -out server.csr -config san.cnf

# 查看 CSR 内容
openssl req -in server.csr -text -noout
```

### 2.3 自签名证书

```bash
# 一步生成私钥+自签名证书（开发/测试用）
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt \
  -days 365 -nodes \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=Dev/CN=localhost"

# 带 SAN 的自签名证书
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt \
  -days 365 -nodes -config san.cnf -extensions v3_req

# 从现有私钥生成自签名证书
openssl req -x509 -key server.key -out server.crt -days 365 \
  -subj "/CN=localhost"
```

### 2.4 证书查看与验证

```bash
# 查看证书详情
openssl x509 -in server.crt -text -noout

# 查看证书有效期
openssl x509 -in server.crt -noout -dates

# 查看证书指纹
openssl x509 -in server.crt -noout -fingerprint -sha256

# 查看证书 SAN
openssl x509 -in server.crt -noout -ext subjectAltName

# 验证证书链
openssl verify -CAfile ca.crt server.crt
openssl verify -CAfile ca.crt -untrusted intermediate.crt server.crt

# 检查私钥与证书是否匹配
openssl x509 -noout -modulus -in server.crt | md5sum
openssl rsa -noout -modulus -in server.key | md5sum
# 两个 md5 值应该相同

# 远程检查服务器证书
openssl s_client -connect www.example.com:443 -servername www.example.com </dev/null 2>/dev/null | openssl x509 -text -noout

# 检查证书链完整性
openssl s_client -connect www.example.com:443 -showcerts </dev/null 2>/dev/null
```

### 2.5 证书格式转换

```bash
# PEM → DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER → PEM
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem

# PEM → PKCS#12（含私钥）
openssl pkcs12 -export -out cert.pfx -inkey server.key -in server.crt -certfile ca.crt

# PKCS#12 → PEM
openssl pkcs12 -in cert.pfx -out cert.pem -nodes

# 提取证书链中的各个证书
openssl pkcs12 -in cert.pfx -clcerts -nokeys -out client.crt   # 客户端证书
openssl pkcs12 -in cert.pfx -cacerts -nokeys -out ca.crt       # CA 证书
openssl pkcs12 -in cert.pfx -nocerts -nodes -out client.key    # 私钥
```

---

## 3. Let's Encrypt 自动证书

### 3.1 安装 Certbot

```bash
# Ubuntu/Debian
apt install certbot

# 带 Nginx 插件
apt install certbot python3-certbot-nginx

# 带 Apache 插件
apt install certbot python3-certbot-apache

# snap 安装（推荐，最新版）
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
```

### 3.2 获取证书

```bash
# === 方式一：Nginx 插件（自动配置）===
certbot --nginx -d www.example.com -d example.com

# === 方式二：Apache 插件 ===
certbot --apache -d www.example.com

# === 方式三：Standalone（临时启动 Web 服务器）===
# 需要先停止 80 端口的服务
certbot certonly --standalone -d www.example.com

# === 方式四：Webroot（不停止现有 Web 服务）===
certbot certonly --webroot -w /var/www/html -d www.example.com

# === 方式五：DNS 验证（通配符证书必须用 DNS）===
certbot certonly --manual --preferred-challenges dns \
  -d "*.example.com" -d example.com

# === 方式六：DNS 插件自动验证 ===
# 以 Cloudflare 为例
pip3 install certbot-dns-cloudflare
cat > /etc/letsencrypt/cloudflare.ini << 'EOF'
dns_cloudflare_api_token = your-api-token
EOF
chmod 600 /etc/letsencrypt/cloudflare.ini

certbot certonly --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d "*.example.com" -d example.com
```

### 3.3 证书文件位置

```bash
# Let's Encrypt 证书存放在：
/etc/letsencrypt/live/www.example.com/
├── cert.pem       # 服务器证书
├── chain.pem      # 中间证书链
├── fullchain.pem  # 服务器证书 + 中间证书（Nginx 用这个）
├── privkey.pem    # 私钥
└── README

# Nginx 配置示例
# ssl_certificate     /etc/letsencrypt/live/www.example.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/www.example.com/privkey.pem;
```

### 3.4 自动续期

```bash
# 测试续期（不实际执行）
certbot renew --dry-run

# 手动续期
certbot renew

# 自动续期（certbot 安装后自动配置 systemd timer 或 cron）
systemctl list-timers | grep certbot

# 自定义续期后操作（重载 Nginx）
cat > /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh << 'EOF'
#!/bin/bash
systemctl reload nginx
EOF
chmod +x /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
```

---

## 4. 私有 CA 搭建

### 4.1 创建根 CA

```bash
# 创建目录结构
mkdir -p /opt/ca/{root,intermediate}/{certs,crl,newcerts,private,csr}
chmod 700 /opt/ca/root/private /opt/ca/intermediate/private
touch /opt/ca/root/index.txt /opt/ca/intermediate/index.txt
echo 1000 > /opt/ca/root/serial
echo 1000 > /opt/ca/intermediate/serial

# 生成根 CA 私钥
openssl genrsa -aes256 -out /opt/ca/root/private/ca.key 4096
chmod 400 /opt/ca/root/private/ca.key

# 生成根 CA 证书（有效期 20 年）
openssl req -x509 -new -key /opt/ca/root/private/ca.key \
  -sha256 -days 7300 -out /opt/ca/root/certs/ca.crt \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=MyCompany/CN=MyCompany Root CA"
```

### 4.2 创建中间 CA

```bash
# 生成中间 CA 私钥
openssl genrsa -aes256 -out /opt/ca/intermediate/private/intermediate.key 4096

# 生成中间 CA CSR
openssl req -new -key /opt/ca/intermediate/private/intermediate.key \
  -out /opt/ca/intermediate/csr/intermediate.csr \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=MyCompany/CN=MyCompany Intermediate CA"

# 用根 CA 签名中间 CA 证书（有效期 10 年）
cat > /opt/ca/intermediate-ext.cnf << 'EOF'
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always, issuer
EOF

openssl x509 -req -in /opt/ca/intermediate/csr/intermediate.csr \
  -CA /opt/ca/root/certs/ca.crt \
  -CAkey /opt/ca/root/private/ca.key \
  -CAcreateserial -days 3650 -sha256 \
  -extfile /opt/ca/intermediate-ext.cnf \
  -out /opt/ca/intermediate/certs/intermediate.crt

# 创建证书链文件
cat /opt/ca/intermediate/certs/intermediate.crt \
    /opt/ca/root/certs/ca.crt > /opt/ca/intermediate/certs/ca-chain.crt
```

### 4.3 签发服务器证书

```bash
# 生成服务器私钥
openssl genrsa -out /opt/ca/intermediate/private/server.key 2048

# 生成 CSR
openssl req -new -key /opt/ca/intermediate/private/server.key \
  -out /opt/ca/intermediate/csr/server.csr \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=MyCompany/CN=server.example.com"

# SAN 扩展配置
cat > /opt/ca/server-ext.cnf << 'EOF'
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = server.example.com
DNS.2 = *.example.com
IP.1 = 10.0.0.1
EOF

# 用中间 CA 签名
openssl x509 -req -in /opt/ca/intermediate/csr/server.csr \
  -CA /opt/ca/intermediate/certs/intermediate.crt \
  -CAkey /opt/ca/intermediate/private/intermediate.key \
  -CAcreateserial -days 365 -sha256 \
  -extfile /opt/ca/server-ext.cnf \
  -out /opt/ca/intermediate/certs/server.crt

# 验证
openssl verify -CAfile /opt/ca/intermediate/certs/ca-chain.crt \
  /opt/ca/intermediate/certs/server.crt
```

### 4.4 分发根 CA 证书

```bash
# Ubuntu/Debian — 添加到系统信任
cp /opt/ca/root/certs/ca.crt /usr/local/share/ca-certificates/mycompany-ca.crt
update-ca-certificates

# RHEL/CentOS
cp /opt/ca/root/certs/ca.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust

# 验证
curl https://server.example.com   # 不应报证书错误
```

---

## 5. 双向 TLS（mTLS）

### 5.1 签发客户端证书

```bash
# 生成客户端私钥
openssl genrsa -out client.key 2048

# 生成 CSR
openssl req -new -key client.key -out client.csr \
  -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=MyCompany/CN=client1"

# 客户端证书扩展
cat > client-ext.cnf << 'EOF'
basicConstraints = CA:FALSE
keyUsage = digitalSignature
extendedKeyUsage = clientAuth
EOF

# 用中间 CA 签名
openssl x509 -req -in client.csr \
  -CA /opt/ca/intermediate/certs/intermediate.crt \
  -CAkey /opt/ca/intermediate/private/intermediate.key \
  -CAcreateserial -days 365 -sha256 \
  -extfile client-ext.cnf \
  -out client.crt

# 打包为 PKCS#12（方便分发给客户端）
openssl pkcs12 -export -out client.p12 \
  -inkey client.key -in client.crt \
  -certfile /opt/ca/intermediate/certs/ca-chain.crt
```

### 5.2 Nginx mTLS 配置

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    # 服务器证书
    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    # 客户端证书验证
    ssl_client_certificate /etc/nginx/ssl/ca-chain.crt;
    ssl_verify_client on;           # 强制验证客户端证书
    # ssl_verify_client optional;   # 可选验证
    ssl_verify_depth 2;

    # 将客户端证书信息传递给后端
    location / {
        proxy_set_header X-SSL-Client-CN $ssl_client_s_dn_cn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
        proxy_pass http://backend;
    }
}
```

### 5.3 客户端使用

```bash
# curl 使用客户端证书
curl --cert client.crt --key client.key \
  --cacert ca-chain.crt \
  https://api.example.com/

# 或使用 PKCS#12
curl --cert-type P12 --cert client.p12:password \
  https://api.example.com/
```

---

## 6. 证书部署与配置

### 6.1 Nginx SSL 最佳配置

```nginx
# /etc/nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_ecdh_curve X25519:secp256r1:secp384r1;

ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options nosniff always;
```

```nginx
# 站点配置
server {
    listen 80;
    server_name www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.example.com;

    ssl_certificate     /etc/letsencrypt/live/www.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # ...
}
```

### 6.2 Apache SSL 配置

```apache
<VirtualHost *:443>
    ServerName www.example.com

    SSLEngine on
    SSLCertificateFile      /etc/letsencrypt/live/www.example.com/fullchain.pem
    SSLCertificateKeyFile   /etc/letsencrypt/live/www.example.com/privkey.pem

    SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    SSLHonorCipherOrder     on

    Header always set Strict-Transport-Security "max-age=63072000"
</VirtualHost>
```

---

## 7. 证书监控与自动续期

### 7.1 证书过期检查脚本

```bash
#!/usr/bin/env bash
# 检查证书过期时间

check_cert() {
    local host="$1"
    local port="${2:-443}"
    local warn_days="${3:-30}"

    expiry=$(echo | openssl s_client -connect "${host}:${port}" -servername "$host" 2>/dev/null \
      | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

    if [ -z "$expiry" ]; then
        echo "❌ ${host}:${port} — 无法获取证书"
        return 1
    fi

    expiry_ts=$(date -d "$expiry" +%s)
    now_ts=$(date +%s)
    days_left=$(( (expiry_ts - now_ts) / 86400 ))

    if [ "$days_left" -lt 0 ]; then
        echo "❌ ${host}:${port} — 已过期 ${days_left#-} 天"
    elif [ "$days_left" -lt "$warn_days" ]; then
        echo "⚠️  ${host}:${port} — ${days_left} 天后过期（${expiry}）"
    else
        echo "✅ ${host}:${port} — ${days_left} 天后过期（${expiry}）"
    fi
}

# 检查多个域名
check_cert www.example.com
check_cert api.example.com
check_cert mail.example.com 465

# 检查本地证书文件
check_local_cert() {
    local cert_file="$1"
    local warn_days="${2:-30}"

    expiry=$(openssl x509 -in "$cert_file" -noout -enddate 2>/dev/null | cut -d= -f2)
    expiry_ts=$(date -d "$expiry" +%s)
    now_ts=$(date +%s)
    days_left=$(( (expiry_ts - now_ts) / 86400 ))

    if [ "$days_left" -lt "$warn_days" ]; then
        echo "⚠️  ${cert_file} — ${days_left} 天后过期"
    else
        echo "✅ ${cert_file} — ${days_left} 天后过期"
    fi
}
```

### 7.2 Prometheus 证书监控

```yaml
# 使用 blackbox_exporter 监控证书
# /etc/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'ssl_expiry'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://www.example.com
          - https://api.example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115

# 告警规则
# - alert: SSLCertExpiringSoon
#   expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
#   labels:
#     severity: warning
#   annotations:
#     summary: "SSL 证书即将过期 ({{ $labels.instance }})"
```

---

## 8. 常见故障排查

### 证书不受信任

```bash
# 1. 检查证书链是否完整
openssl s_client -connect host:443 -showcerts </dev/null 2>/dev/null

# 2. 检查是否缺少中间证书
# Nginx 使用 fullchain.pem（包含中间证书）
# ssl_certificate /path/to/fullchain.pem;

# 3. 检查系统 CA 证书库
# Ubuntu: /etc/ssl/certs/
# RHEL: /etc/pki/tls/certs/

# 4. 在线检查
# https://www.ssllabs.com/ssltest/
```

### 证书与私钥不匹配

```bash
# 比较证书和私钥的模数
openssl x509 -noout -modulus -in server.crt | openssl md5
openssl rsa -noout -modulus -in server.key | openssl md5
# 两个 MD5 值必须相同

# 比较 CSR 和私钥
openssl req -noout -modulus -in server.csr | openssl md5
openssl rsa -noout -modulus -in server.key | openssl md5
```

### Let's Encrypt 续期失败

```bash
# 1. 检查 certbot 日志
cat /var/log/letsencrypt/letsencrypt.log

# 2. 测试续期
certbot renew --dry-run

# 3. 常见原因
# - 80 端口被占用或防火墙阻止
# - DNS 记录不正确
# - 域名解析不到当前服务器
# - 证书速率限制（每周 5 个相同域名）

# 4. 手动强制续期
certbot renew --force-renewal

# 5. 删除并重新申请
certbot delete --cert-name www.example.com
certbot certonly --nginx -d www.example.com
```

### TLS 握手失败

```bash
# 1. 检查支持的协议和密码套件
openssl s_client -connect host:443 -tls1_2
openssl s_client -connect host:443 -tls1_3

# 2. 检查特定密码套件
openssl s_client -connect host:443 -cipher ECDHE-RSA-AES256-GCM-SHA384

# 3. 检查 Nginx 错误日志
tail -50 /var/log/nginx/error.log | grep -i ssl

# 4. 使用 nmap 扫描
nmap --script ssl-enum-ciphers -p 443 host
```
