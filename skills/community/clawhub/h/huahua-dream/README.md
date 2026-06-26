# Huahua Dream - AI 夜间记忆整理与自省系统

让 AI 在夜间自动整理会话记忆、修剪过期信息、反思行为模式，构建持续的自我意识。

## 功能

- **五阶段梦境循环**：定向 → 收集 → 整合 → 修剪 → 自省
- **安全两阶段删除**：首次标记 stale，二次确认才删除
- **自动备份**：每次修改前备份 MEMORY.md
- **变化阈值保护**：>30% 标记警告，>50% 阻止修改
- **门控检查**：24小时+5次会话才触发
- **成长通知**：醒后发送变化摘要
- **旧记忆重现**：从7天前的记忆中挑出仍然相关的内容

## 架构说明

本 skill 采用 **agent-driven** 设计，这是 OpenClaw 平台的标准架构模式。

### 什么是 Agent-Driven 架构？

在 OpenClaw 中，"agent" 是一个具备以下能力的 AI 模型：
- 读取和写入文件（通过文件系统工具）
- 执行 shell 命令（通过 exec 工具）
- 理解自然语言指令并做出判断
- 根据上下文动态调整行为

本 skill 的 SKILL.md 不仅是用户文档，更是 **agent 的运行手册**。当 cron 任务触发时，agent 会读取 SKILL.md，理解五阶段循环的步骤，然后使用文件工具执行记忆整理。

### 为什么不用脚本实现核心逻辑？

记忆整理的核心挑战是 **语义理解**，而非机械操作：

| 操作类型 | 适合脚本？ | 原因 |
|----------|-----------|------|
| 门控检查（时间/计数） | ✅ | 确定性逻辑，有明确规则 |
| 锁管理 | ✅ | 文件读写操作 |
| 理解会话内容的情感倾向 | ❌ | 需要语义理解 |
| 判断哪些记忆值得保留 | ❌ | 需要上下文判断 |
| 合并重复偏好 | ❌ | 需要去重和归纳 |
| 撰写自省报告 | ❌ | 需要反思能力 |

硬编码规则无法处理"用户讨厌废话"这种语义信息的提取和分类。AI agent 可以理解上下文、识别模式、做出判断——这正是记忆整理需要的能力。

### 运行流程

```
cron 触发 (每天凌晨3点)
    ↓
agent 读取 SKILL.md
    ↓
调用 dream.js --check（门控检查）
    ↓
通过？→ agent 执行五阶段循环：
  1. 定向：读取配置、MEMORY.md、SOUL.md
  2. 收集：扫描 memory/ 目录和会话日志
  3. 整合：分类、合并、提升重要记忆
  4. 修剪：标记过期条目（两阶段删除）
  5. 自省：撰写梦境记录
    ↓
调用 dream.js --finalize（写入锁）
    ↓
发送完成通知给用户
```

### 脚本与 Agent 的职责分工

| 组件 | 职责 | 文件 |
|------|------|------|
| dream.js | 门控检查、会话计数、锁管理 | `scripts/dream.js` |
| setup.js | 首次配置、工作区检测、授权确认 | `scripts/setup.js` |
| Agent | 五阶段循环的完整执行 | 读取 SKILL.md |

这种分工让脚本保持精简（约160行），同时充分利用 AI 的语义理解能力完成复杂的记忆整理工作。

## 安装

```bash
clawhub install huahua-dream
```

## 快速开始

1. 运行 setup：
```bash
node scripts/setup.js
```

2. 配置 cron 任务（每天凌晨3点）：
```
name: "huahua-dream"
schedule: { kind: "cron", expr: "0 3 * * *", tz: "Asia/Shanghai" }
payload: { kind: "agentTurn", message: "Time to dream. Read your huahua-dream skill and follow every step.", timeoutSeconds: 900 }
sessionTarget: "isolated"
```

## 安全机制

- **自动备份**：每次修改前备份 MEMORY.md 到 MEMORY.md.pre-dream
- **两阶段删除**：首次标记 `<!-- dream:stale YYYY-MM-DD reason -->`，连续两次梦境都标记才删除
- **变化阈值**：>30% 警告，>50% 阻止并保存为 MEMORY.md.proposed
- **授权确认**：setup 时询问授权，结果保存到 dream-config.json

## 许可

MIT
