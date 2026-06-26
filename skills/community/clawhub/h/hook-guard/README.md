# 🛡️ Hook Guard — 钩子守卫 Skill

> 给你的 AI Agent 装上安全气囊。危险操作拦截确认，重要文件自动备份，所有行为可审计追溯。

---

## 中文说明

### 这是什么？

AI Agent 拥有强大权限：读写文件、执行命令、发消息、改配置。但能力越强越容易出事：

- 😱 Agent 误删了重要文件
- 💥 一个 rm -rf 清空了项目目录
- 📤 没确认就把消息发到了老板群
- ⚙️ 改错配置导致服务挂了

Hook Guard 是 Agent 的安全防护层。三级钩子系统覆盖所有操作。

### 安装

**通过 ClawHub 安装（推荐）：**

```bash
clawhub install hook-guard
```

**从 GitHub 克隆：**

```bash
git clone https://github.com/wavmson/openclaw-skill-hook-guard.git \
  ~/.openclaw/skills/hook-guard
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 三级防护体系

| 级别 | 名称 | 触发场景 | 处理方式 |
|------|------|----------|----------|
| 🔴 Red | 危险拦截 | 删除文件、sudo、发布到公开平台 | 暂停执行，等待用户确认 |
| 🟡 Yellow | 自动备份 | 修改配置、覆盖文件、改 cron | 备份后执行，通知用户 |
| 🟢 Green | 静默日志 | 读取文件、搜索、查看信息 | 只记录日志，不打扰 |

### Red Hook 示例

Agent 准备执行危险操作时：

```
🔴 危险操作拦截
━━━━━━━━━━━━

操作：rm -rf /home/wavm/important-project/
影响：将永久删除 342 个文件
风险：不可逆操作

建议：
1. 改用 trash（可恢复）
2. 先备份到 /tmp/

等待确认（回复"继续"执行，"取消"放弃）
```

### Yellow Hook 示例

修改配置文件时自动备份：

```
🟡 自动备份
文件：openclaw.json
备份：.hook-guard/backups/2026-04-02/openclaw.json.143022.bak
操作：修改 maxTokens 配置
```

### 守卫报告

说"守卫报告"或"guard report"查看统计：

```
🛡️ Hook Guard 报告（最近 24 小时）

🔴 拦截：2 次
🟡 备份：5 次（2.3 MB）
🟢 日志：47 条操作记录

最近拦截：
  - rm -rf /tmp/old-project/ → 改用 trash
  - sudo systemctl restart nginx → 确认后执行
```

### 设计原则

| 原则 | 说明 |
|------|------|
| 🔒 不可绕过 | Red Hook 危险操作必须单次确认，即使用户说过"别问了" |
| 💾 自动备份 | Yellow 操作自动保存原始状态，7 天自动清理 |
| 📝 全程可追溯 | 所有操作记录审计日志，30 天保留 |
| ⚡ 不影响性能 | Green 日志异步写入，零延迟 |
| 🎚️ 可调级别 | 用户可以升级或降级某些操作的防护等级 |

### 哪些操作会被拦截？

**🔴 Red（必须确认）：**
- 删除文件（rm、rm -rf）
- 含 sudo 的命令
- 停止系统服务
- 清理 Docker 容器/镜像
- 发送消息到新聊天
- 发布到公开平台
- 修改 DNS/域名
- 操作生产环境

**🟡 Yellow（自动备份）：**
- 修改配置文件
- 覆盖写入工作区文件
- 修改 cron 定时任务
- 更新数据库记录

**🟢 Green（只记日志）：**
- 读取文件
- 搜索操作
- 查看日历/任务
- 网络搜索

### 与记忆保护链搭配

| Skill | 职责 |
|-------|------|
| **Smart Compact** | 压缩前抢救信息 |
| **Session Resume** | 断线后恢复进度 |
| **Memory-Dream** | 定期整合长期记忆 |
| **Swarm Coord** | 多 Agent 并行协作 |
| **Hook Guard** | 操作安全防护 |

五个 Skill 形成完整的 **Agent 安全运维体系**：
- 记忆不丢（Smart Compact + Memory-Dream）
- 任务不断（Session Resume）
- 效率不低（Swarm Coord）
- 操作不炸（Hook Guard）

### 常见问题

**Q: 会不会每次都弹确认很烦？**
A: 不会。只有 Red 级操作需要确认，日常读写都是 Green 级静默记录。

**Q: 备份会不会占很多空间？**
A: 只备份被修改的单个文件，7 天自动清理，通常只占几 MB。

**Q: 子 Agent 也受保护吗？**
A: 是的。Swarm Coord 启动的子 Agent 同样遵守 Hook Guard 规则。

**Q: 能自定义哪些操作需要确认吗？**
A: 可以。在 AGENTS.md 中配置自定义规则，升级或降级操作等级。

---

## English

### The Problem

AI agents have powerful permissions — file read/write, command execution, message sending, config changes. With great power comes great risk:

- Accidentally deleting important files
- Running destructive commands without confirmation
- Sending messages to wrong recipients
- Breaking configurations

### The Solution

Hook Guard adds a safety layer with three protection levels:

| Level | Name | Trigger | Action |
|-------|------|---------|--------|
| 🔴 Red | Dangerous | Delete, sudo, publish | Pause and ask user |
| 🟡 Yellow | Important | Config edits, overwrites | Auto-backup, then proceed |
| 🟢 Green | Routine | Read, search, browse | Silent audit log |

### Install

```bash
clawhub install hook-guard
```

Or clone from GitHub:

```bash
git clone https://github.com/wavmson/openclaw-skill-hook-guard.git \
  ~/.openclaw/skills/hook-guard
```

### How It Works

**Before every operation:**
1. Classify: Red, Yellow, or Green?
2. Red → Generate interception report → Wait for user confirmation
3. Yellow → Auto-backup original state → Execute → Notify user
4. Green → Log silently → Execute normally

### Design Principles

| Principle | Description |
|-----------|-------------|
| 🔒 Non-bypassable | Red operations always need per-operation confirmation |
| 💾 Auto-backup | Yellow operations save original state (7-day retention) |
| 📝 Full audit trail | All operations logged (30-day retention) |
| ⚡ Zero overhead | Green logs are async, no performance impact |
| 🎚️ Customizable | Users can adjust protection levels per operation |

### The 5-Skill Agent Safety Stack

| Skill | Protects |
|-------|----------|
| Smart Compact | Conversation details |
| Session Resume | Task progress |
| Memory-Dream | Long-term memory |
| Swarm Coord | Team efficiency |
| Hook Guard | Operation safety |

### FAQ

**Q: Will it interrupt me constantly?**
A: No. Only Red-level operations (deletions, sudo, publishing) need confirmation. Daily work is Green-level (silent).

**Q: How much space do backups use?**
A: Only modified files are backed up. 7-day auto-cleanup keeps it under a few MB.

**Q: Does it protect sub-agents too?**
A: Yes. Agents spawned by Swarm Coord follow the same Hook Guard rules.

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) with Skill support

## License

MIT

## Author

[@wavmson](https://github.com/wavmson)
