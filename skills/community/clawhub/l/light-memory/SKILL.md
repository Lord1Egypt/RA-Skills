# Memory System - Three-Layer Memory Architecture

> 版本：v1.0.0 | 日期：2026-04-12
> 设计原则：轻量、跨平台、Prompt-Driven、原子化安装、用户数据安全

---

## 一句话描述

一个可复用的 LLM Agent 三层记忆架构（L1/L2/L3），解决长周期对话的上下文失忆问题。

## 核心价值

- **纯 Prompt 驱动**：无 Python/Bash 依赖，跨平台开箱即用
- **显式标记协议**：用户主动标记"决策："、"洞察："，后台异步提取
- **Memory Synergy 协议**：不再实时拦截写入对话流，而是通过显式标记协助后台 Cron 任务异步提取，不阻塞用户对话
- **CAR 经验萃取**：结构化长期记忆（Context-Action-Result）
- **物理文件持久化**：不依赖向量数据库，纯 Markdown 可审计
- **OpenClaw 原生集成**：利用 Cron + Session 机制，无需额外服务
- **绝对数据安全**：安装时自动备份，迁移为可选命令

## 目标用户

- OpenClaw 深度用户
- 需要长周期记忆的个人 Agent 开发者
- 对"上下文管理"有痛点的 AI 应用开发者

## 推荐模型

- **推荐**：Claude Sonnet / GPT-4o / 其他强推理模型
- **可用**：其他模型（效果可能因理解能力而异）

---

## 可用命令

### /install-memory

原子化一键安装记忆系统。

**执行流程**（一气呵成，不可中断）：

```
Step 1: 获取绝对路径（pwd）
    ↓
Step 2: 冲突检测（proactive-agent / self-improving-agent）
    ↓
Step 3: 备份现有文件
    ↓
Step 4: 写入 6 个 Prompt 模板
    ↓
Step 5: 初始化记忆文件（L1/L2/L3，保护已有数据）
    ↓
Step 6: 注册 Cron 任务（4 个核心 + 1 个可选心跳）
    ↓
Step 7: 验证 + 输出报告
```

**执行步骤**：
1. 读取 `prompts/install-prompt.md`
2. 严格按 Prompt 指引执行，任何步骤失败立即停止
3. 输出安装报告（备份位置、文件列表、Cron 任务）

**安全检查点**：
- 备份后验证文件存在
- Prompt 写入后验证非空
- Cron 注册后验证任务数量

---

### /migrate-memory

可选迁移旧记忆数据到新格式。

**执行流程**：

```
Step 1: 验证备份存在（来自 /install-memory）
    ↓
Step 2: 读取旧数据（备份目录）
    ↓
Step 3: 识别模式（决策/任务/洞察/完成）
    ↓
Step 4: 清洗并写入新格式（L1/L2/L3）
    ↓
Step 5: 输出迁移报告
```

**执行步骤**：
1. 读取 `prompts/migrate-prompt.md`
2. 严格按 Prompt 指引执行
3. 输出迁移报告（L1/L2/L3 数据统计）

**安全机制**：
- 强制验证备份存在
- 不覆盖现有文件，仅追加
- 输出详细迁移报告

---

### /check-memory

检查记忆系统运行状态。

**执行步骤**：
1. 读取 `references/troubleshooting.md`
2. 执行自检清单
3. 输出状态报告

---

## 架构概览

```
用户对话（显式标记）
    ↓
物理日志 (.jsonl)
    ↓ [每小时:00, Prompt 驱动]
L1 提炼（LLM 读取 → 分析 → 写入）
    ↓
SESSION-STATE.md (L1)
    ↓ [23:05, Prompt 驱动]
L1→L2 归档（LLM 读取 → 按日期写入）
    ↓
memory/YYYY-MM-DD.md (L2)
    ↓ [周日 23:30, Prompt 驱动]
L2→L3 萃取（LLM 读取 → CAR 提炼）
    ↓
MEMORY.md (L3)
    ↓ [每天 23:10, Prompt 驱动]
Session GC（清理临时文件）
    ↓
心跳检查（每 30 分钟，健康监控）
```

## 文件结构

```
openclaw-memory-system/
├── SKILL.md                     # 本文件
├── _meta.json                   # ClawHub 元数据
├── prompts/                     # 7 个核心 Prompt 模板
│   ├── l1-hourly-prompt.md      # L1 每小时提炼
│   ├── l2-nightly-prompt.md     # L2 夜间归档
│   ├── l3-weekly-prompt.md      # L3 每周萃取
│   ├── gc-cleanup-prompt.md     # Session GC 清理
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

## Cron 任务清单

### 核心任务（4 个）

| 任务名称 | 触发时间 | sessionTarget | 目标写入 |
|----------|---------|---------------|---------|
| L1 每小时智能提炼 | `0 9-23 * * *` | isolated | SESSION-STATE.md |
| L2 夜间全自动归档 | `5 23 * * *` | isolated | memory/YYYY-MM-DD.md |
| L3 周度自我进化 | `30 23 * * 0` | isolated | MEMORY.md |
| Session GC 清理 | `10 23 * * *` | isolated | 无（物理删除） |

### 可选任务（1 个）

| 任务名称 | 触发时间 | 说明 |
|----------|---------|------|
| 心跳检查 | `*/30 * * * *` | 每 30 分钟检查系统健康状态 |

## 关键设计原则

1. **禁止 ~ 符号**：Cron 环境中 ~ 可能被解析为 /root，使用 `pwd` 获取绝对路径
2. **禁止硬编码日期**：使用 `date` 动态获取，避免读取过期数据
3. **游标防重**：`[Last_Extracted_Time]` 标记，避免重复提炼
4. **原子化操作**：安装一气呵成，失败立即停止
5. **数据安全**：安装时自动备份，迁移为可选

## 冲突处理

检测到已安装 `proactive-agent` 或 `self-improving-agent` 时：
- 输出对比分析
- 不强制替换
- 用户自行决定是否共存

## 参考文档

- 架构详解：`references/architecture.md`
- CAR 格式：`references/car-format.md`
- 故障排查：`references/troubleshooting.md`

---

*设计完成：2026-04-12 | 版本：v1.0.0*
