# li_sentry_check Skill 设计文档

## 概述

`li_sentry_check` 是一个跨平台服务器巡检技能，支持 nanobot、OpenClaw 和 Hermes agent 三大平台。通过 SSH 密钥认证登录远程 Linux 服务器，执行只读巡检命令，生成结构化 Markdown 报告。

## 架构设计

### 双引擎架构

| 平台 | 引擎 | 运行时 | 脚本 |
|------|------|--------|------|
| OpenClaw | Node.js | Node.js 24+ | `scripts/inspect.mjs` |
| NanoBot | Python | Python 3.10+ | `scripts/inspect.py` |
| Hermes | Python | Python 3.10+ | `scripts/inspect.py` |

### 文件结构

```
li_sentry_check/
├── SKILL.md                  # 技能说明文档（大脑）
├── _meta.json                # 技能元数据
├── references/
│   ├── targets.yaml          # 目标服务器配置
│   └── checks.yaml           # 巡检命令白名单
└── scripts/
    ├── inspect.mjs           # Node.js 实现（OpenClaw）
    └── inspect.py            # Python 实现（NanoBot/Hermes）
```

## 核心功能

### 1. SSH 密钥认证

- 使用 SSH 密钥对认证，禁止密码登录
- 支持自定义密钥路径
- 非交互式 SSH（BatchMode=yes）
- 连接超时保护（ConnectTimeout=8）

### 2. 巡检命令白名单

所有巡检命令在 `checks.yaml` 中定义，分为三组：

| 检查组 | 内容 |
|--------|------|
| `basic` | 硬件资源：CPU、内存、磁盘、网络 |
| `services` | 服务状态：systemctl status + 错误日志 |
| `daily` | 完整巡检：basic + services + 安全 + 日志 |

### 3. 动态命令生成

`services` 和 `daily` 检查组的命令根据 `targets.yaml` 中配置的服务动态生成：

```yaml
targets:
  bogon:
    services:
      - sshd
      - mongod
      - docker
```

自动为每个服务生成：
- `svc_<name>_status` — systemctl status
- `svc_<name>_errors` — journalctl 错误日志
- `svc_<name>_recent` — 最近日志（过滤异常关键词）

### 4. 异常检测与报告

报告包含异常关键词检测：
- failed, error, alert, critical
- WARNING, panic, segfault, oom
- killed process, no space, disk quota
- read-only, corrupt, timeout
- refused, denied, unreachable

报告结构：
```
# 🔍 Server Inspection Report
- Target: bogon
- Host: `YOUR_SERVER_IP`
- Overall Status: ⚠️ WARNING
- Anomalies: 3

## ⚠️ Anomalies (Priority)
### ⚠️ systemd_failed_units
...

## <details>View all check results (20 total)</details>
```

## 安全设计

### 只读原则

- 仅执行只读命令（whoami, uptime, free, df, ss 等）
- 禁止修改服务器配置
- 禁止安装软件
- 禁止重启服务

### SSH 安全

- 仅密钥认证，禁止密码
- BatchMode=yes 防止交互式提示
- StrictHostKeyChecking=accept-new 自动接受新主机
- ConnectTimeout=8 防止长时间挂起

### 命令白名单

- 所有命令在 `checks.yaml` 中预定义
- 不支持任意远程命令执行
- 每个命令有超时限制

## 使用方式

### NanoBot / Hermes

```bash
python3 scripts/inspect.py --target bogon --checks daily
python3 scripts/inspect.py --target bogon --checks basic --format json
python3 scripts/inspect.py --target bogon --checks daily --output report.md
```

### OpenClaw

```bash
node scripts/inspect.mjs --target bogon --checks daily
node scripts/inspect.mjs --target bogon --checks basic --format json
node scripts/inspect.mjs --target bogon --checks daily --output report.md
```

## SSH 密钥配置

```bash
# 1. 生成密钥对
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# 2. 复制公钥到远程服务器
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@YOUR_SERVER_IP

# 3. 测试连接
ssh -i ~/.ssh/li_sentry_check inspector@YOUR_SERVER_IP

# 4. 配置 targets.yaml
# 更新 keyPath 为实际密钥路径
```

## 扩展指南

### 添加新目标服务器

编辑 `references/targets.yaml`：

```yaml
targets:
  server2:
    host: YOUR_SERVER_IP_2
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
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
      - id: mongo_status
        cmd: "mongosh --eval 'db.runCommand({ serverStatus: 1 }).ok' || true"
        timeoutSec: 20
```

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-26 | 初始版本：基础巡检、服务巡检、完整巡检 |
