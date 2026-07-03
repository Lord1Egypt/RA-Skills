# IT运维工具箱 - 命令速查参考

## 脚本总览

| 脚本文件 | 模块 | 主要功能 |
|---|---|---|
| `network_diag.py` | 网络诊断 | ping/dns/域名查IP/http/ssl/端口/IP归属 |
| `sys_monitor.py` | 系统监控 | CPU/内存/磁盘/进程/网卡 |
| `service_check.py` | 服务检查 | Systemd/Windows服务/Docker/数据库/健康检查 |
| `troubleshoot.py` | 问题排查 | 日志扫描/OOM/崩溃/网络异常/性能/视频监控/取流测试/RTSP快捷取流/根因 |
| `utils.py` | 实用工具 | 密码/UUID/Cron/JSON/JWT/时间戳/哈希/正则 |

---

## network_diag.py - 网络诊断

```bash
# Ping 检测
python network_diag.py ping <host> [-c 次数]

# DNS 解析
python network_diag.py dns <domain>

# 域名查IP（多DNS服务器对比）
python network_diag.py dnsip <domain>

# HTTP/HTTPS 检测（状态码+响应时间）
python network_diag.py http <url>

# SSL 证书检查（有效期+颁发机构）
python network_diag.py ssl <host> [-p 端口]

# 端口扫描（默认扫描常用端口）
python network_diag.py port <host> [-p 80,443,3306]

# IP 归属地查询（留空查本机公网IP）
python network_diag.py ipinfo [ip]

# 综合全检
python network_diag.py all <host>
```

---

## sys_monitor.py - 系统监控

```bash
# 系统信息概览
python sys_monitor.py info

# CPU 使用率
python sys_monitor.py cpu

# 内存使用情况
python sys_monitor.py mem

# 磁盘使用情况
python sys_monitor.py disk

# Top 进程列表
python sys_monitor.py top [-n 15] [--sort cpu|mem]

# 网络接口信息
python sys_monitor.py netif

# 全面系统扫描
python sys_monitor.py full

# ── 远程监控（SSH，目标需为 Linux） ──

# 远程全面监控
python sys_monitor.py remote <user>@<host> [-k ~/.ssh/key]

# 远程单项监控
python sys_monitor.py rinfo  <user>@<host> [-k key]   # 系统信息
python sys_monitor.py rcpu   <user>@<host> [-k key]   # CPU
python sys_monitor.py rmem   <user>@<host> [-k key]   # 内存+Swap
python sys_monitor.py rdisk  <user>@<host> [-k key]   # 磁盘
python sys_monitor.py rtop   <user>@<host> [-n 10] [--sort mem] [-k key]
python sys_monitor.py rnetif <user>@<host> [-k key]   # 网卡
python sys_monitor.py rdocker<user>@<host> [-k key]   # Docker容器

# 批量健康检查
python sys_monitor.py batch --hosts <user@host1> <user@host2> [-k key]
python sys_monitor.py batch --file ~/servers.txt [-k key]
```

---

## service_check.py - 服务检查

```bash
# Systemd 服务检查（Linux）
python service_check.py systemd [nginx redis mysql]

# Windows 服务状态
python service_check.py winsvc

# Docker 容器列表
python service_check.py docker [-a]

# Docker 容器日志
python service_check.py dlogs <容器名> [-n 100]

# 数据库连通性
python service_check.py dbconn mysql://127.0.0.1:3306 redis://127.0.0.1

# Web 服务健康检查
python service_check.py health https://example.com/health http://api.local:8080
```

---

## troubleshoot.py - 监控问题排查

```bash
# 日志文件扫描（自动识别错误/警告/OOM等）
python troubleshoot.py logscan /var/log/nginx/error.log
python troubleshoot.py logscan /var/log/app.log -p "NullPointerException" -n 1000

# OOM 内存不足检测
python troubleshoot.py oom

# 进程崩溃/重启检测
python troubleshoot.py crashes

# 网络连接异常排查（TCP状态统计+公网检测）
python troubleshoot.py netcheck

# 性能瓶颈快速定位（CPU/内存/磁盘IO）
python troubleshoot.py perf

# 综合巡检报告
python troubleshoot.py inspect

# 根因分析建议（输入错误信息，获取排查建议）
python troubleshoot.py hint "connection refused to 3306"
python troubleshoot.py hint "out of memory, kill process"

# 视频监控播放问题排查
python troubleshoot.py video --url http://192.168.1.100:8080/video
python troubleshoot.py video --rtsp rtsp://admin:pass@192.168.1.100:554/stream
python troubleshoot.py video --url http://192.168.1.100:37777/ISAPI/Streaming/channels/101

# 视频取流测试（实际拉流并分析码率/数据量）
python troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream
python troubleshoot.py stream --url http://192.168.1.100:8080/live/stream.flv
python troubleshoot.py stream --url http://192.168.1.100:8080/live/stream.m3u8
python troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream --duration 10

# RTSP 快捷取流（通过 IP/端口/用户名/密码自动拼接URL并取流）
python troubleshoot.py rtspstream --ip 192.168.1.100 --port 554 --user admin --pass 12345
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --pass 12345 --path /Streaming/Channels/101
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --pass 12345 --brand hikvision --duration 10
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --pass 12345 --brand dahua
```

---

## utils.py - 实用工具

```bash
# 随机密码生成
python utils.py genpass [-l 20] [-n 5] [-m strong|alphanum|digits|hex]

# UUID 生成
python utils.py uuid [-n 5] [-v 4]

# 随机 Token 生成（hex）
python utils.py token [-l 32]

# Cron 表达式解析
python utils.py cron "*/5 * * * *"
python utils.py cron "0 9-18 * * 1-5"

# JSON 格式化/验证
python utils.py json '{"name":"test","value":1}'
python utils.py json /path/to/config.json

# Base64 编解码
python utils.py b64 "Hello World"
python utils.py b64 -d "SGVsbG8gV29ybGQ="

# JWT Token 解码
python utils.py jwt "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# 时间戳转换（留空显示当前时间）
python utils.py ts
python utils.py ts 1713532800

# 文件哈希校验
python utils.py hash /path/to/file.zip
python utils.py hash /path/to/file.zip -a md5

# 正则表达式测试
python utils.py regex "\d{4}-\d{2}-\d{2}" "今天是 2026-04-19"
```

---

## 常见排查场景快速参考

### 🔥 服务突然不可访问
```
1. python network_diag.py http https://your-service.com
2. python service_check.py health https://your-service.com/health
3. python network_diag.py port your-server.com -p 80,443,8080
4. python service_check.py docker  (如果是容器)
5. python service_check.py systemd nginx  (如果是系统服务)
```

### 💀 服务器响应慢
```
1. python troubleshoot.py perf       # 找出瓶颈
2. python sys_monitor.py top         # 看高CPU/内存进程
3. python sys_monitor.py disk        # 检查磁盘空间
4. python troubleshoot.py netcheck   # 检查网络连接堆积
```

### 📜 日志有大量错误
```
1. python troubleshoot.py logscan /var/log/app/error.log
2. python troubleshoot.py hint "你的错误信息"   # 获取排查建议
3. python troubleshoot.py crashes               # 检查崩溃记录
```

### 🔐 SSL 证书即将到期
```
1. python network_diag.py ssl your-domain.com
```

### 💾 内存告警
```
1. python troubleshoot.py oom         # 检查OOM记录
2. python sys_monitor.py mem          # 当前内存状态
3. python sys_monitor.py top --sort mem  # 内存大户
```

### 📹 视频监控无法播放
```
1. python troubleshoot.py video --url http://192.168.1.100:8080/video
2. python troubleshoot.py video --rtsp rtsp://admin:pass@192.168.1.100:554/stream
3. python network_diag.py port 192.168.1.100 -p 554,80,37777  # 检查端口
4. python network_diag.py dnsip camera.example.com            # 域名查IP
5. python troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream  # 取流测试

### 🎥 通过IP/端口/用户名/密码获取RTSP流
```bash
# 最简用法：指定IP和用户名密码，自动探测常见路径
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345

# 指定摄像头品牌，只探测该品牌路径（海康/大华/宇视）
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345 --brand hikvision

# 已知路径，跳过探测直接取流
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345 --path /Streaming/Channels/101

# 自定义端口和测试时长
python troubleshoot.py rtspstream --ip 192.168.1.100 --port 8554 --user admin --password 12345 --duration 10
```
```

---

## 常用端口速查

| 端口 | 服务 | 备注 |
|------|------|------|
| 22 | SSH | 确保限制来源IP |
| 80/443 | HTTP/HTTPS | Web服务 |
| 3306 | MySQL | 不应对公网开放 |
| 5432 | PostgreSQL | 不应对公网开放 |
| 6379 | Redis | 不应对公网开放，需设密码 |
| 27017 | MongoDB | 不应对公网开放 |
| 9200 | Elasticsearch | 不应对公网开放 |
| 3389 | RDP | Windows远程桌面，高风险 |
| 2375 | Docker API | 绝对不能对公网开放 |

---

## 操作系统差异说明

| 功能 | Linux | macOS | Windows |
|------|-------|-------|---------|
| CPU监控 | /proc/stat | top -l 1 | WMI |
| 内存监控 | /proc/meminfo | vm_stat | WMI |
| 进程列表 | ps aux | ps aux | Get-Process |
| 服务管理 | systemctl | launchctl | Get-Service |
| OOM检测 | dmesg + syslog | 系统日志 | EventLog |
| 网络连接 | ss / netstat | netstat | netstat |
