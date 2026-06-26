---
name: mailserver-maintenance
description: "docker-mailserver 启动/停止/状态检查/故障排查。出站链路（DMS→cloud SMTP relay）和收件队列问题。发送失败、队列积压、Cloud relay 无响应时触发。不负责邮件收发使用（见 email-usage）。"
metadata: {"openclaw":{"emoji":"📮","requires":{"anyBins":[]}}}
---

# Mailserver 维护

## SSH 配置（IP 不暴露）

容器内 SSH 通过 `~/.ssh/config` 连接 cloud：
```
Host cloudrelay
    HostName 101.43.110.225
    User administrator
    IdentityFile /home/cloudrelay/.ssh/id_rsa
    StrictHostKeyChecking=no
    BatchMode=yes
```
连接：`ssh -F /home/cloudrelay/.ssh/config cloudrelay "..."`

## 启动（DMS Docker）

```bash
cd ~/docker-mailserver && docker compose up -d mailserver
docker exec mailserver supervisorctl status
```

## Cloud SMTP AUTH Relay（Windows cloud）

```bash
# 检查状态
ssh -F /home/cloudrelay/.ssh/config cloudrelay "cmd /c netstat -ano | findstr :2526 | findstr LISTEN"

# 启动
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Start-ScheduledTask -TaskName MailRelay2526Watchdog"

# 停止
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Stop-ScheduledTask -TaskName MailRelay2526Watchdog"
```

## 状态检查

```bash
# Cloud relay 端口
ssh -F /home/cloudrelay/.ssh/config cloudrelay "cmd /c netstat -ano | findstr :2526 | findstr LISTEN"

# Docker 容器
docker ps | grep -E "mailserver|relay"

# 邮件队列
docker exec mailserver postqueue -p

# DMS 日志（最近20行）
docker exec mailserver tail -20 /var/log/mail/mail.log

# Cloud relay 日志
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Get-Content C:\smtp_auth_relay.log -Tail 10"
```

## 故障排查

### 发送失败 / 队列积压

```bash
# 1. Cloud relay 在线？
ssh -F /home/cloudrelay/.ssh/config cloudrelay "cmd /c netstat -ano | findstr :2526 | findstr LISTEN"

# 2. SSH key 权限？
docker exec mailserver ls -la /home/cloudrelay/.ssh/id_rsa

# 3. SSH 测试
docker exec mailserver ssh -F /home/cloudrelay/.ssh/config cloudrelay echo OK

# 4. 强制重试
docker exec mailserver postqueue -f

# 5. 查看队列
docker exec mailserver postqueue -p
```

### Cloud relay 无响应

```bash
# watchdog 进程？
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Get-Process python | Select Id"

# 错误日志
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Get-Content C:\smtp_auth_relay_err.log -Tail 10"

# 重启 watchdog
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Stop-ScheduledTask -TaskName MailRelay2526Watchdog; Start-ScheduledTask -TaskName MailRelay2526Watchdog"
```

### 收件卡住 / deferred

```bash
# amavis 端口监听？
docker exec mailserver ss -tlnp | grep 10025

# master.cf 配置？
docker exec mailserver postconf -n | grep dmsrelay
```

## 停止

```bash
# Cloud relay
ssh -F /home/cloudrelay/.ssh/config cloudrelay "powershell -Command Stop-ScheduledTask -TaskName MailRelay2526Watchdog"

# DMS
cd ~/docker-mailserver && docker compose down
```

## 端到端测试

```bash
echo "Test" | docker exec -i mailserver mail -s "Health Check" axelhu@163.com
sleep 15 && docker exec mailserver tail -5 /var/log/mail/mail.log | grep -v "No decoder"
```

---

详细架构图、组件清单、配置文件路径 → `references/architecture.md`
