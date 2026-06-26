# 🔍 li_sentry_check - 服务器巡检技能

> 多平台服务器巡检与健康管理技能。通过 SSH 密钥认证登录远程 Linux 服务器，执行只读巡检命令，生成结构化 Markdown 报告。

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Platforms](https://img.shields.io/badge/platforms-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 概述

`li_sentry_check` 是一个跨平台服务器巡检技能，支持 **nanobot**、**OpenClaw** 和 **Hermes agent** 三大平台。通过 SSH 密钥认证登录远程 Linux 服务器，执行只读巡检命令（CPU、内存、磁盘、网络、服务、安全），生成结构化 Markdown 报告，自动突出异常信息。

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔐 SSH 密钥认证 | 仅密钥认证，禁止密码登录，安全加固 |
| 📊 硬件巡检 | CPU、内存、磁盘、网络使用情况 |
| 🖥️ 服务巡检 | 重点服务运行状态、异常日志 |
| 🛡️ 安全巡检 | SSH 异常登录、防火墙告警、内核错误 |
| 📝 结构化报告 | Markdown/JSON 格式，异常优先显示 |
| 🌐 跨平台 | 支持 nanobot、OpenClaw、Hermes |

## 🚀 快速开始

### 1. 安装技能

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. 配置 SSH 密钥

```bash
# 生成密钥对
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# 复制公钥到远程服务器
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<服务器IP>

# 测试连接
ssh -i ~/.ssh/li_sentry_check inspector@<服务器IP>
```

### 3. 配置目标服务器

编辑 `references/targets.yaml`：

```yaml
targets:
  production-web:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. 执行巡检

```bash
# 基础巡检（硬件资源）
python3 scripts/inspect.py --target production-web --checks basic

# 服务巡检
python3 scripts/inspect.py --target production-web --checks services

# 完整巡检（基础 + 服务 + 安全 + 日志）
python3 scripts/inspect.py --target production-web --checks daily

# JSON 格式输出
python3 scripts/inspect.py --target production-web --checks daily --format json

# 输出到文件
python3 scripts/inspect.py --target production-web --checks daily --output report.md
```

## 📖 巡检检查组

| 检查组 | 内容 | 命令数 |
|--------|------|--------|
| `basic` | CPU、内存、磁盘、网络 | 8 |
| `services` | 服务状态 + 错误日志（动态） | 3×N |
| `daily` | 完整巡检（basic + services + 安全 + 日志） | 26 |

## 📊 报告示例

```markdown
# 🔍 Server Inspection Report

- Target: production-web
- Host: YOUR_SERVER_IP
- User: inspector
- Checks: daily
- Started: 2026-04-26T09:00:00+00:00
- Total checks: 26
- ⚠️ Anomalies: 3

## Overall Status: ⚠️ WARNING

## ⚠️ Anomalies (Priority)

### ⚠️ systemd_failed_units
Command: `systemctl --failed --no-pager`
Status: OK (contains anomalies)

Output:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```

## <details>📋 View all check results (26 total)</details>
```

## 🔧 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--target` | 目标服务器名称（targets.yaml 中定义） | （必填） |
| `--checks` | 检查组：`basic`、`services`、`daily` | `basic` |
| `--format` | 输出格式：`markdown`、`json` | `markdown` |
| `--output` | 输出到文件（默认 stdout） | stdout |

## 🌐 跨平台支持

| 平台 | 运行时 | 脚本 | 命令 |
|------|--------|------|------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 文件结构

```
li_sentry_check/
├── SKILL.md                  # 技能说明文档
├── _meta.json                # 技能元数据
├── design.md                 # 设计文档
├── references/
│   ├── targets.yaml          # 目标服务器配置
│   └── checks.yaml           # 巡检命令白名单
└── scripts/
    ├── inspect.mjs           # Node.js 实现（OpenClaw）
    └── inspect.py            # Python 实现（NanoBot/Hermes）
```

## 🔒 安全最佳实践

- **密钥权限**: `chmod 600 ~/.ssh/li_sentry_check`
- **主机验证**: 生产环境建议预填充 `known_hosts`，而非使用 `accept-new`
- **服务名称**: 仅允许字母、数字、连字符、下划线（使用前已验证）
- **命令白名单**: 永远不要在 `checks.yaml` 中添加状态修改命令
- **报告处理**: 报告可能包含系统数据 — 请勿公开分享

## 🔧 扩展指南

### 添加新目标服务器

编辑 `references/targets.yaml`：

```yaml
targets:
  database-server:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### 添加新检查组

编辑 `references/checks.yaml`：

```yaml
checks:
  database:
    description: 数据库巡检
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-26 | 初始版本：基础巡检、服务巡检、完整巡检 |

## 📄 许可证

MIT License
