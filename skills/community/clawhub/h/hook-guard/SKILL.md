---
name: hook-guard
description: "钩子守卫。为 Agent 操作添加安全防护层——文件修改前自动备份、危险命令执行前拦截确认、敏感操作自动告警通知用户。触发词：安全检查、hook guard、守卫、备份保护、安全模式、操作审计。也可在 AGENTS.md 中配置为始终生效。"
---

# Hook Guard — 钩子守卫

为 Agent 的每一步操作加上安全防护网。

## 什么时候用

- 始终生效（推荐在 AGENTS.md 中配置为默认行为）
- 用户说"安全模式"、"开启守卫"、"hook guard"
- 执行高风险任务前（部署、批量修改、删除操作）
- Agent 自行判断当前操作需要额外防护

## 核心理念

Agent 拥有强大的工具权限——能读写文件、执行命令、发送消息、操作数据库。
权力越大，责任越大。Hook Guard 在关键操作前后插入安全检查点：

- **执行前（Pre-hook）**：该不该做？需不需要确认？
- **执行中（Guard）**：自动备份、记录日志
- **执行后（Post-hook）**：通知用户、验证结果

## 三类防护钩子

### 🔴 Red Hook — 危险操作拦截

触发条件：检测到以下操作时**立即暂停**，等待用户确认。

**文件操作：**
- `rm`、`rm -rf`、`trash` 大量文件（>5 个）
- 覆盖写入已有的重要文件（MEMORY.md、AGENTS.md、配置文件等）
- 删除 `.git` 目录或 Git 历史

**命令执行：**
- 含 `sudo` 的命令
- `systemctl stop/disable` 系统服务
- `docker rm`、`docker system prune`
- 修改 SSH 配置、防火墙规则
- `kill -9`、`pkill` 进程管理

**外部操作：**
- 发送消息到新的聊天/群（首次接触）
- 发布到公开平台（小红书、Twitter 等）
- 修改 DNS、域名配置
- 操作生产环境

拦截报告格式：

```
🔴 危险操作拦截
━━━━━━━━━━━━

⚠️ 操作：rm -rf /home/wavm/important-project/
📁 影响：将永久删除 342 个文件
🔒 风险：不可逆操作

建议：
1. 改用 trash（可恢复）
2. 先备份到 /tmp/backup-YYYYMMDD/

⏳ 等待确认（回复"继续"执行，"取消"放弃）
```

### 🟡 Yellow Hook — 自动备份 + 通知

触发条件：检测到以下操作时**自动备份后执行**，并通知用户。

**自动备份的场景：**
- 编辑配置文件（openclaw.json、.env、nginx.conf 等）
- 覆盖写入工作区文件
- 修改 cron jobs
- 更新数据库记录

**备份机制：**
- 备份路径：`~/.openclaw/workspace-main/.hook-guard/backups/YYYY-MM-DD/`
- 文件名：`{原始文件名}.{HHmmss}.bak`
- 保留最近 7 天的备份，自动清理旧备份

**通知格式：**

```
🟡 自动备份
文件：openclaw.json
备份：.hook-guard/backups/2026-04-02/openclaw.json.143022.bak
操作：修改 maxTokens 配置
```

### 🟢 Green Hook — 静默日志

触发条件：常规操作，只记录日志不打扰用户。

**记录的操作：**
- 读取文件
- 搜索操作
- 查看日历/任务
- 网络搜索

**日志位置：** `~/.openclaw/workspace-main/.hook-guard/audit.log`

日志格式：
```
[2026-04-02 14:30:22] READ /home/wavm/.openclaw/workspace-main/MEMORY.md
[2026-04-02 14:30:25] EXEC ls -la /tmp/
[2026-04-02 14:31:00] SEARCH web "OpenClaw skills"
```

## 执行流程

### 每次操作前

1. **分类**：判断操作属于 Red/Yellow/Green 哪个级别
2. **Red**：生成拦截报告 → 等待用户确认 → 确认后执行
3. **Yellow**：自动备份原始状态 → 执行操作 → 通知用户
4. **Green**：记录日志 → 正常执行

### 定期维护

- 每天清理 7 天前的备份文件
- 审计日志保留 30 天
- 可通过 "查看守卫报告" 获取统计摘要

## 配置

在 AGENTS.md 中添加以下规则使 Hook Guard 始终生效：

```markdown
## 安全规则（Hook Guard）

- 执行 rm/trash 前检查影响范围，>5 个文件需确认
- 修改配置文件前自动备份到 .hook-guard/backups/
- sudo 命令必须用户确认
- 发送外部消息前确认接收方和内容
- trash > rm（可恢复优于不可逆）
```

## 守卫报告

用户说"守卫报告"或"guard report"时，生成统计摘要：

```
🛡️ Hook Guard 报告
━━━━━━━━━━━━━━━━

📅 时间范围：最近 24 小时

🔴 拦截：2 次
  - rm -rf /tmp/old-project/ → 用户确认后改用 trash
  - sudo systemctl restart nginx → 用户确认后执行

🟡 备份：5 次
  - openclaw.json（2 次修改）
  - cron/jobs.json（1 次修改）
  - memory/2026-04-02.md（2 次追加）

🟢 日志：47 条操作记录

💾 备份空间：2.3 MB（7 天保留）
```

## 规则

- **永不绕过 Red Hook**：即使用户说"别问了直接做"，危险操作仍需单次确认
- **备份不占大空间**：只备份被修改的文件，不备份整个目录
- **日志不含敏感内容**：只记录操作类型和路径，不记录文件内容
- **用户可调整级别**：可以把某些 Yellow 操作升级为 Red，或降级为 Green
- **不影响性能**：Green 日志异步写入，不阻塞操作

## 与其他 Skill 配合

- **Smart Compact**：压缩前 Hook Guard 自动备份当前对话状态
- **Session Resume**：Hook Guard 的拦截记录可以跨 session 恢复
- **Swarm Coord**：子 Agent 的操作同样受 Hook Guard 保护
- **Memory-Dream**：审计日志是 Dream 整合时的参考信息源
