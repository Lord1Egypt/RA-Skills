# OpenClaw Memory System

> 三层记忆架构（L1/L2/L3），解决长周期对话的上下文失忆问题。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://docs.openclaw.ai)

---

## 一句话描述

一个可复用的 LLM Agent 三层记忆架构，纯 Prompt 驱动，无 Python/Bash 依赖，跨平台开箱即用。

---

## 核心价值

| 特性 | 说明 |
|------|------|
| **纯 Prompt 驱动** | 无 Python/Bash 依赖，跨平台开箱即用 |
| **显式标记协议** | 用户主动标记"决策："、"洞察："，后台异步提取 |
| **CAR 经验萃取** | 结构化长期记忆（Context-Action-Result） |
| **物理文件持久化** | 不依赖向量数据库，纯 Markdown 可审计 |
| **OpenClaw 原生集成** | 利用 Cron + Session 机制，无需额外服务 |
| **绝对数据安全** | 安装时自动备份，迁移为可选命令 |

---

## 快速开始

### 安装

```
/install-memory
```

一行命令，一气呵成：
1. 自动备份现有文件
2. 写入 7 个 Prompt 模板
3. 初始化记忆文件
4. 注册 5 个 Cron 任务（4 核心 + 1 可选心跳）
5. 验证安装完成

### 迁移（可选）

```
/migrate-memory
```

将旧记忆数据迁移到新格式（需先运行 `/install-memory`）。

### 检查状态

```
/check-memory
```

检查记忆系统运行状态。

---

## 架构概览

```
用户对话（显式标记）
    ↓
物理日志 (.jsonl)
    ↓ [每小时:00]
L1 提炼（LLM 读取 → 分析 → 写入）
    ↓
SESSION-STATE.md (L1)
    ↓ [23:05]
L1→L2 归档（LLM 读取 → 按日期写入）
    ↓
memory/YYYY-MM-DD.md (L2)
    ↓ [周日 23:30]
L2→L3 萃取（LLM 读取 → CAR 提炼）
    ↓
MEMORY.md (L3)
    ↓ [每天 23:10]
Session GC
    ↓
心跳检查（每 30 分钟）
```

### 三层记忆

| 层级 | 文件 | 用途 | 更新频率 |
|------|------|------|---------|
| **L1** | `SESSION-STATE.md` | 当前任务状态 | 每小时 |
| **L2** | `memory/YYYY-MM-DD.md` | 每日归档 | 每天 |
| **L3** | `MEMORY.md` | 长期法则库 | 每周 |

---

## Cron 任务

### 必选（4 个）

| 任务 | 触发时间 | 说明 |
|------|---------|------|
| L1 每小时提炼 | `0 9-23 * * *` | 每天 9-23 点 |
| L2 夜间归档 | `5 23 * * *` | 每天 23:05 |
| L3 周度萃取 | `30 23 * * 0` | 每周日 23:30 |
| Session GC | `10 23 * * *` | 每天 23:10 |

### 可选（1 个）

| 任务 | 触发时间 | 说明 |
|------|---------|------|
| 心跳检查 | `*/30 * * * *` | 每 30 分钟健康检查 |

---

## 文件结构

```
openclaw-memory-system/
├── SKILL.md                     # Skill 核心指令
├── _meta.json                   # ClawHub 元数据
├── prompts/                     # 7 个 Prompt 模板
│   ├── l1-hourly-prompt.md      # L1 每小时提炼
│   ├── l2-nightly-prompt.md     # L2 夜间归档
│   ├── l3-weekly-prompt.md      # L3 每周萃取
│   ├── gc-cleanup-prompt.md     # Session GC
│   ├── heartbeat-prompt.md      # 心跳检查（可选）
│   ├── install-prompt.md        # 原子化安装
│   └── migrate-prompt.md        # 可选迁移
├── templates/                   # 记忆文件模板
│   ├── SESSION-STATE.template.md
│   ├── daily-log.template.md
│   └── MEMORY.template.md
└── references/                  # 补充文档
    ├── architecture.md          # 架构详解
    ├── car-format.md            # CAR 格式规范
    └── troubleshooting.md       # 故障排查
```

---

## 设计原则

1. **极简 Bash**：仅保留 `pwd`、`date`、`mkdir`，复杂逻辑交给 LLM
2. **绝对路径**：使用 `pwd` 获取基准路径，禁止硬编码 `~`
3. **原子化安装**：一气呵成，失败立即停止
4. **可选迁移**：安装时不迁移旧数据，用户自行决定
5. **冲突检测**：检测已安装 Skill，不强制替换
6. **数据安全**：安装时自动备份，迁移前验证备份存在

---

## 推荐模型

- **推荐**：Claude Sonnet / GPT-4o / 其他强推理模型
- **可用**：其他模型（效果可能因理解能力而异）

---

## 迁移指南

### 从 proactive-agent 迁移

1. 运行 `/install-memory`（自动备份）
2. 运行 `/migrate-memory`（迁移旧数据）
3. 可选：卸载 proactive-agent

### 从零开始

1. 运行 `/install-memory`
2. 系统自动初始化 L1/L2/L3
3. 等待下一个整点自动执行 L1 提炼

---

## 故障排查

运行 `/check-memory` 或查看 `references/troubleshooting.md`。

常见问题：
- L1 提炼未执行 → 检查 Cron 任务
- 归档文件日期错误 → 确保使用动态日期
- MEMORY.md 重复法则 → 萃取前检查已有内容

---

## 贡献

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 作者

Created with ❤️ by the OpenClaw community.

---

## Star History

如果这个项目对你有帮助，请给个 ⭐️！
