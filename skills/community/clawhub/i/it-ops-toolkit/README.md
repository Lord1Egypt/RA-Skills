# 🛠️ IT运维工具箱 (it-ops-toolkit)

> 一套开箱即用的 IT 运维工具集，通过自然语言触发，覆盖网络诊断、系统监控、服务检查、问题排查、实用工具五大场景。

## ✨ 特性

- 🗣️ **自然语言驱动** — 在 WorkBuddy 中用中文描述需求，AI 自动选择合适的工具执行
- 📦 **零依赖** — 纯 Python 标准库实现，无需安装任何第三方包
- 🖥️ **跨平台** — 支持 Windows / Linux / macOS
- 🎨 **彩色输出** — ✅/⚠️/❌ 直观的状态标识，进度条可视化
- 🔍 **智能排查** — 内置根因分析引擎，输入错误信息自动给出处理建议

---

## 📁 目录结构

```
it-ops-toolkit/
├── SKILL.md                          # 技能配置（触发词、工作流）
├── README.md                         # 本文件
├── scripts/
│   ├── network_diag.py               # 网络诊断
│   ├── sys_monitor.py                # 系统监控
│   ├── service_check.py              # 服务检查
│   ├── troubleshoot.py               # 监控问题排查
│   └── utils.py                      # 实用工具
└── references/
    └── commands_reference.md         # 命令速查手册
```

---

## 🚀 快速开始

### 安装

技能已安装到用户级目录：

```
~/.workbuddy/skills/it-ops-toolkit/
```

### 使用方式

在 WorkBuddy 对话中直接用自然语言，例如：

| 你说 | 自动执行 |
|------|---------|
| "帮我 ping 一下 github.com" | `network_diag.py ping github.com` |
| "看看 SSL 证书还有多久过期" | `network_diag.py ssl example.com` |
| "查一下 baidu.com 的 IP" | `network_diag.py dnsip baidu.com` |
| "服务器内存够不够" | `sys_monitor.py mem` |
| "远程服务器全面检查" | `sys_monitor.py remote root@192.168.1.100` |
| "远程看一下CPU和内存" | `sys_monitor.py remote deploy@10.0.0.1` |
| "批量检查所有服务器" | `sys_monitor.py batch --hosts root@10.0.0.1 deploy@10.0.0.2` |
| "Docker 容器状态" | `service_check.py docker` |
| "检查 MySQL 是否能连上" | `service_check.py dbconn mysql://127.0.0.1:3306` |
| "扫描一下错误日志" | `troubleshoot.py logscan /var/log/app/error.log` |
| "服务器响应很慢" | `troubleshoot.py perf` |
| "视频监控播放不了" | `troubleshoot.py video --url http://192.168.1.100:8080/video` |
| "测试摄像头取流" | `troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream` |
| "通过IP端口密码获取监控流" | `troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345` |
| "帮我全面巡检一下" | `troubleshoot.py inspect` |
| "connection refused 怎么排查" | `troubleshoot.py hint "connection refused"` |
| "生成一个随机密码" | `utils.py genpass` |
| "这个 cron 什么时候执行" | `utils.py cron "0 9 * * 1-5"` |

---

## 📋 功能详情

### 1️⃣ 网络诊断 (`network_diag.py`)

| 命令 | 功能 | 示例 |
|------|------|------|
| `ping` | Ping 检测（延迟+丢包率） | `ping google.com -c 10` |
| `dns` | DNS 解析（A/AAAA + 反向解析） | `dns baidu.com` |
| `dnsip` | **域名查IP**（多DNS服务器对比+CDN检测） | `dnsip baidu.com` |
| `http` | HTTP/HTTPS 检测（状态码+响应时间） | `http https://example.com` |
| `ssl` | SSL 证书检查（有效期+SAN+TLS版本） | `ssl example.com` |
| `port` | 端口扫描（默认常用端口+安全提示） | `port 192.168.1.1 -p 22,80,443,3306` |
| `ipinfo` | IP 归属地查询（城市/ISP/时区） | `ipinfo 8.8.8.8` |
| `all` | 综合网络全检 | `all example.com` |

### 2️⃣ 系统监控 (`sys_monitor.py`)

| 命令 | 功能 | 示例 |
|------|------|------|
| `info` | 系统信息概览（OS/主机名/运行时间） | `info` |
| `cpu` | CPU 使用率（型号/核心/负载） | `cpu` |
| `mem` | 内存使用（总量/已用/可用+进度条） | `mem` |
| `disk` | 磁盘使用（各分区使用率+预警） | `disk` |
| `top` | Top 进程列表（按 CPU 或内存排序） | `top -n 10 --sort mem` |
| `netif` | 网络接口信息（IP/掩码） | `netif` |
| `full` | 全面系统扫描 | `full` |
| `remote` | **远程服务器全面监控**（SSH） | `remote root@192.168.1.100` |
| `rinfo` | **远程系统信息** | `rinfo deploy@10.0.0.1 -k ~/.ssh/id_rsa` |
| `rcpu` | **远程CPU监控** | `rcpu root@192.168.1.100` |
| `rmem` | **远程内存监控**（含 Swap） | `rmem deploy@10.0.0.1` |
| `rdisk` | **远程磁盘监控** | `rdisk root@192.168.1.100` |
| `rtop` | **远程Top进程** | `rtop root@192.168.1.100 -n 10 --sort mem` |
| `rnetif` | **远程网络接口** | `rnetif root@192.168.1.100` |
| `rdocker` | **远程Docker容器状态** | `rdocker root@192.168.1.100` |
| `batch` | **批量服务器健康检查** | `batch --hosts root@10.0.0.1 deploy@10.0.0.2` |

### 3️⃣ 服务检查 (`service_check.py`)

| 命令 | 功能 | 示例 |
|------|------|------|
| `systemd` | Systemd 服务状态（Linux） | `systemd nginx redis mysql` |
| `winsvc` | Windows 服务状态 | `winsvc` |
| `docker` | Docker 容器列表 | `docker -a` |
| `dlogs` | Docker 容器日志 | `dlogs myapp -n 100` |
| `dbconn` | 数据库连通性测试 | `dbconn mysql://127.0.0.1:3306 redis://127.0.0.1` |
| `health` | Web 服务健康检查 | `health https://api.example.com/health` |

### 4️⃣ 监控问题排查 (`troubleshoot.py`)

| 命令 | 功能 | 示例 |
|------|------|------|
| `logscan` | 日志智能扫描（自动识别 ERROR/OOM/崩溃等） | `logscan /var/log/app.log -p "OOM" -n 1000` |
| `oom` | OOM 内存不足检测（dmesg/syslog） | `oom` |
| `crashes` | 进程崩溃/重启检测（systemd/coredump/事件日志） | `crashes` |
| `netcheck` | 网络连接异常排查（TCP状态统计+公网检测） | `netcheck` |
| `perf` | 性能瓶颈快速定位（CPU/内存/磁盘IO联动分析） | `perf` |
| `video` | **视频监控播放问题排查**（RTSP/HTTP/HLS/ONVIF） | `video --url http://192.168.1.100:8080/video` |
| `stream` | **视频取流测试**（RTSP/HTTP-FLV/HLS/RTMP，分析码率） | `stream --rtsp rtsp://admin:pass@host:554/stream --duration 10` |
| `rtspstream` | **RTSP快捷取流**（IP/端口/用户名/密码，智能探测厂商路径） | `rtspstream --ip 192.168.1.100 --user admin --password 12345` |
| `inspect` | 综合巡检报告（一键全检） | `inspect` |
| `hint` | 根因分析建议（输入错误信息，智能匹配排查方案） | `hint "connection refused"` |

### 5️⃣ 实用工具 (`utils.py`)

| 命令 | 功能 | 示例 |
|------|------|------|
| `genpass` | 随机密码生成（强/字母数字/纯数字/hex） | `genpass -l 20 -n 5 -m strong` |
| `uuid` | UUID 生成（v1/v4） | `uuid -n 3 -v 4` |
| `token` | 随机 Token 生成（hex） | `token -l 32` |
| `cron` | Cron 表达式解析（人类可读+常见模式匹配） | `cron "*/5 * * * *"` |
| `json` | JSON 格式化/验证/统计 | `json config.json` |
| `b64` | Base64 编解码 | `b64 -d "SGVsbG8="` |
| `jwt` | JWT Token 解码（Header/Payload/exp） | `jwt "eyJ0eXAiOi..."` |
| `ts` | 时间戳转换（秒/毫秒↔日期时间） | `ts 1713532800` |
| `hash` | 文件哈希校验（MD5/SHA1/SHA256/SHA512） | `hash file.zip -a sha256` |
| `regex` | 正则表达式测试（匹配+捕获组） | `regex "\d{4}-\d{2}" "2026-04-19"` |

---

## 🔧 命令行直接调用

也可以直接在终端调用脚本：

```bash
# 设置 Python 路径（Windows）
set PYTHONIOENCODING=utf-8
python C:\Users\Administrator\.workbuddy\skills\it-ops-toolkit\scripts\sys_monitor.py full

# Linux/macOS
python3 ~/.workbuddy/skills/it-ops-toolkit/scripts/sys_monitor.py full
```

---

## 🚨 常见排查场景

### 服务不可访问
```
HTTP检测 → 端口扫描 → 服务状态 → 日志扫描
network_diag http → network_diag port → service_check docker → troubleshoot logscan
```

### 服务器响应慢
```
性能定位 → 进程分析 → 内存检查 → 网络检测
troubleshoot perf → sys_monitor top → sys_monitor mem → troubleshoot netcheck
```

### 日志大量报错
```
日志扫描 → 根因建议 → 崩溃检测
troubleshoot logscan → troubleshoot hint → troubleshoot crashes
```

### 内存告警
```
OOM检测 → 内存状态 → 内存大户
troubleshoot oom → sys_monitor mem → sys_monitor top --sort mem
```

### 视频监控无法播放
```
视频流检测 → 端口检查 → 网络连通性 → 协议兼容性 → 取流验证
troubleshoot video → network_diag port → network_diag dnsip → troubleshoot stream → troubleshoot rtspstream
```

### 通过IP端口密码获取RTSP流
```
连通性预检 → 品牌路径探测（或指定路径） → 取流测试
troubleshoot rtspstream --ip <IP> --user <用户> --password <密码>
```

---

## 📊 支持的数据库连接格式

| 格式 | 示例 |
|------|------|
| `协议://主机:端口` | `mysql://127.0.0.1:3306` |
| `协议://主机`（使用默认端口） | `redis://127.0.0.1` |
| `主机:端口` | `127.0.0.1:5432` |

默认端口映射：MySQL 3306 / PostgreSQL 5432 / Redis 6379 / MongoDB 27017 / MSSQL 1433 / Oracle 1521 / Elasticsearch 9200 / Kafka 9092 / ZooKeeper 2181 / RabbitMQ 5672

---

## ⚠️ 注意事项

- **Linux 专属功能**：Systemd、dmesg、/proc 读取在 Windows/macOS 上不可用
- **Docker 命令**：需要 Docker 已安装且 Daemon 正在运行
- **端口扫描**：扫描大量端口可能耗时较长，建议指定目标端口
- **JWT 解码**：仅解析 Payload，不验证签名安全性
- **密码生成**：使用 Python `secrets` 模块，密码学安全

## 🌐 远程监控说明

远程监控通过系统 SSH 命令连接目标服务器，**目标服务器必须**：
1. 开放 SSH 端口（默认 22）
2. 已配置好 SSH 密钥认证或免密登录（推荐）
3. 远程主机为 Linux 系统（远程监控命令基于 Linux 工具链）

### 主机格式

```
user@host          # 使用默认端口 22
user@host:2222     # 指定自定义端口
```

### SSH 密钥

```bash
# 指定密钥文件
sys_monitor.py remote root@192.168.1.100 -k ~/.ssh/my_key

# 批量检查时统一密钥
sys_monitor.py batch --hosts root@10.0.0.1 deploy@10.0.0.2 -k ~/.ssh/deploy_key
```

### 批量检查

支持从命令行或文件批量检查多台服务器：

```bash
# 命令行指定
sys_monitor.py batch --hosts root@10.0.0.1:22 deploy@10.0.0.2:22 ops@10.0.0.3:2222

# 从文件读取（每行一台，# 开头为注释）
sys_monitor.py batch --file ~/servers.txt
```

---

## 📹 RTSP 快捷取流说明

`rtspstream` 命令通过输入 IP、端口、用户名、密码，自动拼接 RTSP URL 并进行取流测试。

### 工作流程

```
[1/3] 连通性预检 ─ Ping延迟检测 + RTSP端口可达性
[2/3] 路径探测   ─ 未指定 --path 时，按品牌顺序逐条 DESCRIBE 探测常见厂商路径
                  返回 200 则解析 SDP 获取编码/分辨率信息
[3/3] 取流测试   ─ 对最佳匹配流进行完整取流（DESCRIBE→SETUP→PLAY→RTP数据接收）
```

### 内置厂商路径

| 品牌 | 别名 | 路径数 | 路径示例 |
|------|------|--------|---------|
| 海康威视 | hikvision / 海康 / 海康威视 | 5 | `/Streaming/Channels/101`、`/h264/ch1/main/av_stream` |
| 大华 | dahua / 大华 | 5 | `/cam/realmonitor?channel=1&subtype=0`、`/live/ch00_0.264` |
| 宇视 | uniview / 宇视 / unv | 3 | `/video1`、`/video2`、`/Living/ch1` |
| 通用IPC | dhipc / generic | 4 | `/live/main`、`/ch0_0.264` |
| 通用 | generic / 通用 | 9 | `/stream1`、`/live`、`/h264`、`/ch1` |

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--ip` | ✅ | - | 摄像头 IP 地址 |
| `--port` | ❌ | 554 | RTSP 端口 |
| `--user` | ✅ | - | 用户名 |
| `--password` | ❌ | (空) | 密码 |
| `--path` | ❌ | 自动探测 | 指定路径则跳过探测直接取流 |
| `--brand` | ❌ | 全部探测 | 品牌筛选（hikvision/dahua/uniview/dhipc，支持中文） |
| `--duration` | ❌ | 5 | 取流测试时长（秒） |

### 使用示例

```bash
# 最简用法：自动探测所有厂商路径
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345

# 指定品牌，只探测该品牌路径
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345 --brand hikvision

# 已知路径，跳过探测直接取流
python troubleshoot.py rtspstream --ip 192.168.1.100 --user admin --password 12345 --path /Streaming/Channels/101

# 自定义端口和测试时长
python troubleshoot.py rtspstream --ip 192.168.1.100 --port 8554 --user admin --password 12345 --duration 10
```

---

## 📄 License

MIT
