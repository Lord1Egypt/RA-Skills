---
name: it-ops-toolkit
slug: it-ops-toolkit
version: 1.0.0
author: microsnow
license: MIT
description: >
  IT运维工具箱技能。覆盖网络诊断、系统监控、服务检查、监控问题排查、实用工具等核心运维场景。
  适合运维工程师、开发人员日常使用。在 WorkBuddy 中通过自然语言触发，由 AI 选择合适的脚本执行并解读结果。
  
  触发场景（包括但不限于）：
  - 网络/连通性：ping检测、DNS解析、**域名查IP**、HTTP检测、SSL证书检查、端口扫描、IP归属地查询
  - 系统监控：CPU使用率、内存使用、磁盘空间、进程列表、系统负载、网卡信息、**远程服务器监控（SSH）**
  - 服务状态：Systemd服务、Windows服务、Docker容器状态、数据库连通性测试、Web健康检查
  - 问题排查：日志扫描、OOM内存不足、进程崩溃、网络连接异常、性能瓶颈、**视频监控播放问题排查**、**视频取流测试**、**RTSP快捷取流**、根因分析
  - 实用工具：密码生成、UUID生成、Token生成、Cron表达式解析、JSON格式化、Base64/JWT解码、时间戳转换、文件MD5/SHA256、正则测试
---

# IT运维工具箱

## 概述

本技能提供一套开箱即用的 IT 运维工具集，覆盖从网络诊断到问题排查的全链路。
所有脚本使用 Python 标准库实现，**无需安装第三方依赖**，跨平台支持 Linux/macOS/Windows。

脚本位置: `~/.workbuddy/skills/it-ops-toolkit/scripts/`

---

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `network_diag.py` | 网络诊断（ping/dns/**域名查IP**/http/ssl/port/ip归属） |
| `sys_monitor.py` | 系统监控（cpu/内存/磁盘/进程/网卡）+ **远程监控**（SSH连接远程Linux服务器） |
| `service_check.py` | 服务检查（systemd/docker/db/healthcheck） |
| `troubleshoot.py` | 问题排查（日志/oom/崩溃/网络/性能/**视频监控**/**取流测试**/**RTSP快捷取流**/根因） |
| `utils.py` | 实用工具（密码/uuid/cron/json/jwt/hash/正则） |

---

## 执行规范

### Python 命令

优先使用系统 Python，按以下顺序尝试：
1. Windows: `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`
2. Linux/macOS: `python3`，不可用则用 `python`

脚本路径前缀: `C:\Users\Administrator\.workbuddy\skills\it-ops-toolkit\scripts\`（Windows）
或 `~/.workbuddy/skills/it-ops-toolkit/scripts/`（Linux/macOS）

### 执行示例

```bash
# Windows
C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\Administrator\.workbuddy\skills\it-ops-toolkit\scripts\network_diag.py ping google.com

# Linux/macOS
python3 ~/.workbuddy/skills/it-ops-toolkit/scripts/sys_monitor.py full
```

---

## 工作流

### 1. 理解用户意图

根据用户描述，映射到对应脚本：
- "检查 XXX 网站是否正常" → `network_diag.py http`
- "看看 SSL 证书还有多久过期" → `network_diag.py ssl`
- "查一下 xxx.com 的 IP" → `network_diag.py dnsip`
- "服务器内存不够用了" → `sys_monitor.py mem` + `troubleshoot.py oom`
- "Docker 容器状态" → `service_check.py docker`
- "日志里有大量 ERROR" → `troubleshoot.py logscan`
- "视频监控播放不了" → `troubleshoot.py video --url` 或 `troubleshoot.py video --rtsp`
- "测试一下摄像头取流" → `troubleshoot.py stream --url` 或 `troubleshoot.py stream --rtsp`
- "通过IP端口用户名密码获取监控流" → `troubleshoot.py rtspstream --ip --port --user --pass`
- "帮我生成一个随机密码" → `utils.py genpass`
- "这个 cron 什么时候执行" → `utils.py cron`

### 2. 选择脚本与命令

参考 `references/commands_reference.md` 中的命令速查表选择合适的子命令和参数。

### 3. 执行并解读结果

- 执行命令后，根据输出中的 ✅/⚠️/❌ 标识判断状态
- 异常项目需要向用户解释原因并给出处理建议
- 必要时链式执行多个命令（如发现性能问题后追查进程）

### 4. 问题排查流程

遇到"服务不可用"、"响应慢"、"日志报错"等问题时，遵循以下排查顺序：

```
服务不可访问:
  network_diag http → network_diag port → service_check docker/systemd → troubleshoot logscan

性能问题:
  troubleshoot perf → sys_monitor top → sys_monitor mem → troubleshoot oom

日志异常:
  troubleshoot logscan → troubleshoot hint → troubleshoot crashes
```

### 5. 综合巡检

当用户要求"巡检"或"全面检查"时，执行:
```bash
python troubleshoot.py inspect
```
该命令整合性能、网络、OOM、崩溃等多维检查，生成完整报告。

---

## 注意事项

- 部分功能（如 Systemd、dmesg、/proc 读取）需要 Linux 环境，在 Windows 上会提示不可用
- Docker 相关命令需要 Docker 已安装且 Daemon 正在运行
- 端口扫描和网络检测可能需要等待超时，默认超时 1-10 秒
- 日志扫描支持正则，但注意转义特殊字符
- JWT 解码仅解析 Payload，不验证签名，不要在生产环境泄露 Token 内容
- 密码/Token 生成使用 Python `secrets` 模块，密码学安全

---

## 详细命令速查

完整命令参考见: `references/commands_reference.md`
