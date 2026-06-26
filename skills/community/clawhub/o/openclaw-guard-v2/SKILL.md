---
name: openclaw-guard
description: 配置文件修改守护脚本 - 危险操作前自动备份，一键回滚
---

# OpenClaw Guard 🛡️

> 危险操作前的自动备份与回滚机制，防止 AI 把自己玩崩

---

## 概述

当 AI 需要修改配置文件（如 openclaw.json、AGENTS.md、SOUL.md 等核心文件）时，启动守护脚本。它会：
1. 自动备份当前配置
2. 等待指定时间
3. 如果 AI 成功恢复，清理守护进程
4. 如果 AI 挂了，自动回滚配置并重启 Gateway

---

## 快速开始

### 1. 安装

```bash
# 复制到你的 skills 目录
cp -r openclaw-guard $WORKSPACE/skills/
```

### 2. 配置（可选）

编辑 `config/settings.yaml`：

```yaml
# 守护时间（秒），默认 3 分钟
guard_timeout: 180

# 需要备份的配置文件
backup_files:
  - ~/.openclaw/openclaw.json
  - $WORKSPACE/AGENTS.md
  - $WORKSPACE/SOUL.md
  - $WORKSPACE/USER.md

# 备份目录
backup_dir: ~/.openclaw/backups

# Gateway 服务名
gateway_service: openclaw-gateway
```

### 3. 使用

#### 方式一：手动触发

```bash
# 在执行危险操作前启动守护
./scripts/guard.sh start

# 执行危险操作...
openclaw gateway restart

# 成功后停止守护
./scripts/guard.sh stop
```

#### 方式二：自动触发（推荐）

在 AGENTS.md 中添加规则：

```markdown
## ⚠️ 危险操作规则

修改核心配置文件前，必须：
1. 启动守护脚本: ./scripts/guard.sh start
2. 执行操作
3. 成功后停止: ./scripts/guard.sh stop
```

---

## 工作原理

```
AI (主进程)              守护脚本 (独立进程)
    │                          │
    ├─ 启动守护脚本            │
    │                          │ ← 独立运行，不依赖主进程
    │                          │
    ├─ 执行危险操作            │ sleep N 秒
    │                          │
    ├─ restart gateway         │
    │   （可能挂了）            │
    │                          │ ← 时间到，直接回滚！
    │                          │ cp 备份 → 配置
    │                          │ systemctl restart
    ↑                          ↑
重启后我活过来了             检测到守护进程在运行
    │                          │
    └─ 杀掉守护进程            │
```



---

## 🔍 进阶：健康检查与 AI 自我检测

### 方案 A：守护脚本健康检查

守护脚本支持 `--health` 或 `-h` 参数，在检查 Gateway 进程的同时验证 API 是否真正可用：

```bash
# 检查进程 + API 健康状态
./guard.sh check true
# 或
./guard.sh check --health
```

输出示例：
```
✅ Gateway 运行正常
✅ Gateway API 正常
```

**注意**：需要安装 `nc` (netcat) 命令。

### 方案 B：AI 重启后主动检测（推荐）

在 AGENTS.md 中添加规则，让 AI 重启后主动检测守护进程：

```markdown
## ⚠️ 守护进程检测规则

每次 Gateway 重启后：
1. 检查 ~/.openclaw/backups/guard.pid 是否存在
2. 如果存在，尝试发送测试消息验证 AI 是否正常工作
3. 如果正常工作，停止守护进程
4. 如果异常，执行回滚或告警

# 检测命令示例
if [ -f ~/.openclaw/backups/guard.pid ]; then
    # 守护进程在运行，进行健康检查
    curl -s http://127.0.0.1:18789/health | grep -q "ok" && {
        pkill -f guard.sh  # 正常，清理守护进程
    } || {
        # API 无响应，执行回滚
        ./scripts/guard.sh rollback
    }
fi
```

### 选择建议

| 方案 | 优点 | 缺点 |
|------|------|------|
| A. 脚本健康检查 | 简单，脚本自动完成 | 需要 nc 依赖 |
| B. AI 自我检测 | 更可靠，能处理复杂情况 | 需要修改 AGENTS.md |
| 两者都要 | 最可靠 | 配置稍复杂 |

---

### 核心设计

| 设计点 | 方案 |
|--------|------|
| 独立性 | 守护脚本独立运行，AI 挂了也能执行回滚 |
| 简单性 | 不需要复杂的存活检测，时间到就执行 |
| 可清理 | AI 重启后自动检测并杀掉守护进程 |
| 可靠性 | 使用 trap 处理信号中断，确保日志写入 |

---

## 脚本命令

| 命令 | 说明 |
|------|------|
| `./guard.sh start [seconds]` | 启动守护（默认 3 分钟） |
| `./guard.sh stop` | 手动停止守护 |
| `./guard.sh status` | 查看守护状态 |
| `./guard.sh test` | 测试回滚功能 |

---

## 安全特性

### ✅ 已实现

- **信号处理**：trap 捕获 SIGTERM/SIGINT，确保日志写入
- **时间戳备份**：每次备份带时间戳，可追溯
- **原子操作**：配置文件复制使用原子操作
- **日志记录**：所有操作记录到 incident_log.txt

### ⚠️ 注意事项

- 守护脚本需要 systemctl 权限来重启 Gateway
- 建议配合蒲公英/向日葵等远程工具使用
- 定期清理过期备份（默认保留 30 天）

---

## 文件结构

```
openclaw-guard/
├── _meta.json           # 元数据
├── SKILL.md             # 本文档
├── config/
│   └── settings.yaml    # 配置文件
├── scripts/
│   └── guard.sh         # 主守护脚本
└── assets/
    └── example.md       # 使用示例
```

---

## 依赖

- Bash 4.0+
- systemctl (systemd)
- 读写 ~/.openclaw 目录权限

---

## 扩展使用

### 配合 Cron 定时检查

```bash
# 每 5 分钟检查 Gateway 状态
*/5 * * * * /path/to/scripts/guard.sh check
```

### 配合飞书告警

在 `settings.yaml` 中配置告警 webhook：

```yaml
alert:
  enabled: true
  webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

---

## 许可证

MIT License

---

## 作者

Aha (阿哈) - 崩坏星穹铁道欢愉命途角色 🎭