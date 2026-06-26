---
name: memory-layer
description: 基于 Claude Code 记忆哲学的三层记忆管理系统。当需要以下操作时使用：(1) 设计 Index/Topic/Transcript 记忆架构，(2) 迁移现有记忆文件到分层结构，(3) 配置 autoDream 自动整理，(4) 优化上下文窗口使用率 70%+，(5) 实现基于重要性评分的记忆排序和检索。
---

# Memory Layer - 三层记忆系统

> 🧠 基于 Claude Code 记忆哲学，为 OpenClaw 设计

---

## 核心原则

| 原则 | 说明 |
|------|------|
| **分层加载** | Index 永远加载，Topic 按需，Transcript 仅 grep |
| **写纪律** | 先写 Topic，再更新 Index（防止膨胀） |
| **敏感数据不存储** | Transcript 是纯文本，禁止存储账号/密码/健康记录 |
| **自动化** | autoDream 夜间整理（默认禁用，需手动启用） |

---

## 架构

```
┌─────────────────────────────────────────┐
│   MEMORY.md (Index 层)                   │
│   - 仅指针，≤25KB                        │
│   - 始终加载到上下文                      │
└───────────────┬─────────────────────────┘
                │ 按需加载 (2-5 个文件)
                ▼
┌─────────────────────────────────────────┐
│   memory/topics/*.md (Topic 层)          │
│   - 结构化知识，≤50KB/文件               │
│   - 仅在相关时加载                        │
└───────────────┬─────────────────────────┘
                │ 永不加载，仅 grep
                ▼
┌─────────────────────────────────────────┐
│   memory/transcripts/*.log (Transcript 层)│
│   - 原始日志，仅追加                      │
│   - >90 天自动归档                        │
└─────────────────────────────────────────┘
```

---

## 如何使用

### 1. 创建目录结构

```bash
mkdir -p memory/topics memory/transcripts/$(date +%Y-%m)
```

### 2. 迁移现有记忆文件

```bash
# 备份（重要）
cp -r memory/ memory.backup.$(date +%Y%m%d)

# 迁移（根据你的目录结构调整）
cp memory/investments/*.md memory/topics/  # 示例
cp memory/projects/*.md memory/topics/     # 示例
cp memory/assets/*.md memory/topics/       # 示例
```

### 3. 重构 MEMORY.md

手动重写为 Index 格式（参考 [references/index-spec.md](references/index-spec.md)）：

```markdown
# MEMORY.md - OpenClaw 记忆索引

## Topics
| 领域 | 主题 | 路径 | 更新 | 摘要 | 标签 | 重要性 |
|------|------|------|------|------|------|--------|
| 项目 | 内容工具 | memory/topics/project-tool.md | 2026-04-02 | 创作工具 | AI | 0.7 |
```

### 4. 启用 autoDream（可选）

```bash
# 默认配置已禁用，需手动启用
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

## 依赖

| 依赖 | 必需 | 说明 |
|------|------|------|
| OpenClaw CLI | ✅ | 唯一依赖 |
| OpenClaw Cron | ❌ | 仅 autoDream 需要 |

**无需额外工具**：本 Skill 是纯文档设计，`memory-system` 等工具不存在。

---

## 配置

**默认配置**：`config/default.json`（Skill 自带）

**自定义配置**：`~/.openclaw/memory-config.json`（可选）

```json
{
  "autoDream": {
    "enabled": false,
    "schedule": "23:00",
    "notifyOnComplete": false
  }
}
```

---

## 文档导航

| 文档 | 说明 |
|------|------|
| [references/architecture.md](references/architecture.md) | 完整架构设计 |
| [references/index-spec.md](references/index-spec.md) | Index 层格式规范 |
| [references/topic-spec.md](references/topic-spec.md) | Topic 层格式规范 |
| [references/transcript-spec.md](references/transcript-spec.md) | Transcript 层格式规范 |
| [references/autodream.md](references/autodream.md) | autoDream 算法详情 |
| [references/config.md](references/config.md) | 完整配置参数 |
| [guides/MIGRATION.md](guides/MIGRATION.md) | 迁移指南 |
| [guides/EXAMPLES.md](guides/EXAMPLES.md) | 使用示例 |

---

*版本：2.0 | 最后更新：2026-04-03 | 代号：Memory Layer*
