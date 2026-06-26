# Mailserver 架构参考（2026-04-14）

## 入站链路（收件）

```
外部发件方 → cloud:2526 (SMTP AUTH Relay, Windows)
  → SSH → DMS Postfix :25
  → amavis (DKIM/DMARC/SPF) → Dovecot LMTP → mailbox
```

## 出站链路（发件）

```
DMS Postfix → dmsrelay (Postfix pipe)
  → SSH → cloud server
  → cloud_sendmail.py → MX :587
```

SSH 连接用 `~/.ssh/config`（Host: cloudrelay），IP 不暴露。

## 组件清单

| 组件 | 类型 | 位置 | 管理方式 |
|------|------|------|----------|
| DMS mailserver | Docker | home | docker compose |
| DMS Postfix | Docker 内 | port 1025→25 | docker exec |
| Cloud SMTP AUTH Relay | Windows Python | cloud :2526 | Task Scheduler |
| cloudrelay user | Linux user | DMS container | useradd |

## 配置文件

| 文件 | 路径 |
|------|------|
| DMS docker-compose | `/home/axelhu/docker-mailserver/compose.yaml` |
| DMS 环境变量 | `/home/axelhu/docker-mailserver/mailserver.env` |
| Cloud SMTP AUTH Relay | `C:\temp\smtp_auth_relay.py`（cloud Windows）|
| Cloud watchdog | `C:\temp\smtp_auth_watchdog.py`（cloud Windows）|
| Cloud mail sender | `C:\temp\cloud_sendmail.py`（cloud Windows）|
| DMS relay script | `/tmp/dms_send4.sh`（容器内）|
| DMS SSH key | `/home/cloudrelay/.ssh/id_rsa`（容器内）|
| DMS SSH config | `/home/cloudrelay/.ssh/config`（容器内）|
| DMS Postfix master.cf | `/etc/postfix/master.cf`（容器内）|

## 日志位置

| 日志 | 路径 |
|------|------|
| DMS mailserver | `docker logs mailserver` |
| DMS mail.log | `docker exec mailserver tail /var/log/mail/mail.log` |
| Cloud relay | `ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell Get-Content C:\smtp_auth_relay.log -Tail 10"` |
| Cloud watchdog 错误 | `ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell Get-Content C:\smtp_auth_relay_err.log -Tail 10"` |

## 详细故障排查

### 外部邮件收不到

```bash
# 1. cloud relay 在线
ssh -F /home/cloudrelay/.ssh/config cloudrelay "cmd /c netstat -ano | findstr :2526"

# 2. DMS 收到 SSH 连接？
docker exec mailserver tail -30 /var/log/mail/mail.log | grep -E "AUTH|connect|smtpd"

# 3. amavis 回复路径
docker exec mailserver ss -tlnp | grep 10025

# 4. 队列
docker exec mailserver postqueue -p
```

### master.cf 参考配置（/etc/postfix/master.cf 结尾）

```
127.0.0.1:10025 inet n - n - - smtpd    # amavis 回复路径
dmsrelay    unix - n n - - pipe         # 出站 relay
```
