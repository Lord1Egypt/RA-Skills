---
name: local-mail-server
description: 本地邮件服务器系统，基于 Stalwart Mail Server + Brevo 中继 + VPS 中继。支持完整的邮件收发功能，适用于无公网 IP 环境。触发词：邮件服务器、email、imap、smtp、stalwart、brevo、vps relay。
version: 1.0.0
author: openclaw-community
license: MIT
tags: [email, mail-server, stalwart, brevo, vps, relay, self-hosted]
---

# 本地邮件服务器（无公网 IP 方案）

基于 Stalwart Mail Server 的本地邮件系统，配合 Brevo 发件中继和 VPS 收件中继，实现完整的邮件收发功能。

**适用场景**：家庭网络、运营商 NAT 环境、无公网 IP

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                       本地服务器 (Mac/Linux)                      │
│                                                                 │
│   Webmail/IMAP客户端 ──IMAP──► Stalwart ──Brevo──► 外部收件人    │
│        │                           │                            │
│        └── 显示/管理邮件           └── 存储/转发邮件             │
└─────────────────────────────────────────────────────────────────┘
              ▲
              │ Tailscale VPN (私有网络 IP)
              │
┌─────────────┴───────────────────────────────────────────────────┐
│                        VPS (公网 IP)                             │
│                                                                 │
│   Postfix 中继 ──► DKIM 验证 ──► Tailscale ──► 本地服务器        │
│       ▲                                                         │
│       │                                                         │
│   外部邮件 (Gmail/QQ Mail 等)                                    │
└─────────────────────────────────────────────────────────────────┘

收件: 外部发件人 → DNS MX → VPS Postfix → Tailscale VPN → 本地 Stalwart
发件: Webmail → Stalwart (SMTP) → Brevo 中继 → 外部收件人
```

## 系统要求

### 本地服务器
- macOS / Linux
- Stalwart Mail Server 0.15.5+
- Tailscale（用于 VPS 通信）

### VPS
- 任意云服务商（Vultr/DigitalOcean/腾讯云等）
- Ubuntu 24.04 LTS
- 公网 IP
- 最小配置即可（1核 512MB 内存）

### 外部服务
- Brevo 账户（免费 300 封/天）
- Cloudflare DNS（管理域名）
- Tailscale 账户（免费）

## 快速开始

### 1. 安装 Stalwart

```bash
# macOS ARM64
curl -L -o stalwart.tar.gz "https://github.com/stalwartlabs/stalwart/releases/download/v0.15.5/stalwart-aarch64-apple-darwin.tar.gz"

# Linux x86_64
curl -L -o stalwart.tar.gz "https://github.com/stalwartlabs/stalwart/releases/download/v0.15.5/stalwart-x86_64-unknown-linux-gnu.tar.gz"

tar -xzf stalwart.tar.gz
chmod +x stalwart
./stalwart -c config/config.toml
```

### 2. 配置 VPS 中继

```bash
# 在 VPS 上安装 Postfix 和 OpenDKIM
sudo apt update
sudo apt install -y postfix opendkim opendkim-tools

# 配置 Postfix 转发到本地服务器
echo "yourdomain.com    smtp:[LOCAL_TAILSCALE_IP]:25" | sudo tee /etc/postfix/transport
sudo postmap /etc/postfix/transport
```

### 3. 配置 DNS

在 Cloudflare DNS 添加：

```
类型    名称           内容
───────────────────────────────────────────────────────────
MX      @              mail.yourdomain.com (优先级 10)
A       mail           YOUR_VPS_IP (仅 DNS，灰色云朵)
TXT     @              v=spf1 ip4:YOUR_VPS_IP include:spf.brevo.com ~all
TXT     _dmarc         v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com
TXT     mail._domainkey  DKIM 公钥
```

## 配置详解

### Stalwart 配置 (config/config.toml)

```toml
# 服务器基本配置
server.hostname = "mail.yourdomain.com"
server.listener.smtp.bind = ["[::]:25"]
server.listener.imap.bind = ["[::]:143"]
server.listener.submission.bind = ["[::]:587"]

# Brevo 发件中继
[relay.brevo]
address = "smtp-relay.brevo.com"
port = 587
protocol = "smtp"

[relay.brevo.auth]
type = "plain"
username = "YOUR_BREVO_LOGIN"
password = "YOUR_BREVO_SMTP_KEY"

# 默认使用 Brevo 中继
queue.outbound.next-hop = "brevo"
```

### Postfix 配置 (VPS)

**/etc/postfix/main.cf**:
```ini
myhostname = relay.yourdomain.com
mydomain = relay.yourdomain.com
mydestination = $myhostname, localhost
mynetworks = 127.0.0.0/8, 100.0.0.0/8  # 包含 Tailscale 网段
inet_interfaces = all
smtp_cname_overrides_servername = no
disable_dns_lookups = yes
transport_maps = hash:/etc/postfix/transport
```

**/etc/postfix/transport**:
```
yourdomain.com    smtp:[YOUR_LOCAL_TAILSCALE_IP]:25
```

### OpenDKIM 配置 (VPS)

**/etc/opendkim.conf**:
```ini
AutoRestart             Yes
Syslog                  yes
Canonicalization        relaxed/simple
KeyTable                refile:/etc/opendkim/KeyTable
SigningTable            refile:/etc/opendkim/SigningTable
Socket                  inet:12301@localhost
SignatureAlgorithm      rsa-sha256
```

**生成 DKIM 密钥**:
```bash
sudo mkdir -p /etc/opendkim/keys/yourdomain.com
sudo opendkim-genkey -D /etc/opendkim/keys/yourdomain.com -d yourdomain.com -s mail
sudo chown -R opendkim:opendkim /etc/opendkim/keys
```

## 用户管理

### 创建用户

通过 Stalwart Web UI (http://localhost:8080) 或 API：

```bash
curl -X POST "http://localhost:8080/api/principal" \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "individual",
    "name": "username",
    "emails": ["username@yourdomain.com"],
    "secrets": ["SecurePassword123"],
    "enabledPermissions": [
      "email-receive",
      "authenticate", 
      "email-send",
      "imap-authenticate",
      "imap-enable",
      "imap-list",
      "imap-select",
      "imap-fetch"
    ]
  }'
```

### 认证说明

⚠️ **重要**：Stalwart 认证使用用户名（如 `username`），而不是完整邮箱地址。

```
正确: 用户名 = username
错误: 用户名 = username@yourdomain.com
```

## Webmail 集成

### Nextcloud Mail 配置

| 配置项 | 值 |
|--------|-----|
| IMAP 主机 | `127.0.0.1` |
| IMAP 端口 | `143` |
| IMAP 加密 | `STARTTLS` |
| SMTP 主机 | `127.0.0.1` |
| SMTP 端口 | `587` |
| SMTP 加密 | `STARTTLS` |
| 认证用户名 | 用户名（不是邮箱） |

### Nextcloud 配置命令

```bash
cd /path/to/nextcloud
php occ config:system:set "allow_local_remote_servers" --value="true"
php occ config:system:set "app.mail.verify-tls-peer" --value="false" --type=boolean
```

## 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 25 | SMTP | 接收邮件（VPS 开放，本地可选） |
| 587 | SMTP | 发送邮件（STARTTLS） |
| 143 | IMAP | 邮件读取（STARTTLS） |
| 465 | SMTPS | 发送邮件 SSL（可选） |
| 993 | IMAPS | 邮件读取 SSL（可选） |
| 8080 | HTTP | Web 管理界面（仅本地） |

## 故障排除

### 邮件无法接收

1. 检查 VPS Postfix 日志：`sudo tail -f /var/log/mail.log`
2. 确认 DNS MX 记录指向 VPS IP
3. 确认 Tailscale 连接正常
4. 检查 VPS 防火墙是否开放 25 端口

### 邮件进入垃圾箱

1. 确认 SPF 记录包含 VPS IP 和 Brevo
2. 确认 DKIM 记录正确配置
3. 确认 DMARC 记录已设置

### DNS 被自动修改

⚠️ **Cloudflare Tunnel 会自动覆盖 DNS 记录**

如果使用 Cloudflare Tunnel，它可能会自动修改 `mail.yourdomain.com` 的 A 记录，导致邮件中继失效。

**解决方案**：
1. 停止 Cloudflare Tunnel
2. 手动添加 A 记录指向 VPS IP
3. 确保 Proxy 状态为灰色云朵（仅 DNS）

## 安全建议

1. **管理界面**：仅绑定 127.0.0.1，不对外暴露
2. **强密码**：为所有用户设置强密码
3. **定期备份**：备份 `data/` 目录
4. **监控日志**：定期检查邮件日志
5. **SPF/DKIM/DMARC**：完整配置防止被标记为垃圾邮件

## 成本估算

| 项目 | 费用 |
|------|------|
| VPS（最小配置）| $2.5-5/月 |
| Brevo（免费版）| $0（300 封/天） |
| Tailscale（免费版）| $0 |
| Cloudflare DNS | $0 |
| **总计** | **$2.5-5/月** |

## 目录结构

```
local-mail-server/
├── SKILL.md              # 技能文档
├── SKILL-PUBLIC.md       # 公开版本（脱敏）
├── config/
│   └── config.toml       # Stalwart 主配置
├── scripts/
│   └── start-mail-server.sh  # 启动/停止脚本
├── bin/
│   └── stalwart          # Stalwart 可执行文件
├── data/                 # 邮件数据
│   ├── stalwart.pid
│   └── stalwart.log.*
└── docs/
    └── brevo-setup.md    # Brevo 配置指南
```

## 参考链接

- [Stalwart Mail Server](https://github.com/stalwartlabs/stalwart)
- [Brevo (原 Sendinblue)](https://www.brevo.com)
- [Tailscale](https://tailscale.com)
- [Postfix](http://www.postfix.org/)
- [OpenDKIM](http://www.opendkim.org/)

## 许可证

MIT License

---

**贡献者**：欢迎提交 Issue 和 Pull Request！
