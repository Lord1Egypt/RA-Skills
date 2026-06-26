---
name: skill-extractor
description: 从复杂任务中提取可复用的技能文档，参考 Hermes Agent 的 Skill Documents 设计。用于当任务完成后，识别值得保留的步骤流程，并存储为可搜索的技能文件，下次遇到类似任务时自动检索并建议使用。
metadata:
  openclaw:
    tags: [memory, learning, skills, self-improvement]
    os: [darwin, linux]
---

# Skill Extractor — 任务技能提取器

参考 Hermes Agent 的 Skill Documents 机制，在 OpenClaw 中实现"从经验中学习"的闭环。

## 核心功能

1. **提取（Extract）** — 从对话历史中识别多步骤流程，生成标准化 SKILL.md
2. **存储（Store）** — 保存到 `~/.openclaw/workspace/skills/skill-extractor/skills/`
3. **检索（Search）** — FTS5 全文检索，在新任务中匹配相关技能
4. **建议（Suggest）** — 任务完成后主动提示是否提取技能

## 工作流程

```
复杂任务完成
    ↓
触发技能提取检测（多步骤 / 超过N轮 / 成功率高的任务）
    ↓
LLM 回顾对话 → 提取关键步骤
    ↓
生成 SKILL.md 格式的技能文档
    ↓
展示给用户确认是否保存
    ↓
保存 → 下次遇到类似任务自动建议使用
```

## 触发条件

当检测到以下情况时，建议提取技能：
- 任务超过 5 轮对话完成
- 包含多个工具调用
- 任务执行成功（有明确输出）
- 涉及罕见问题或特殊解决方案

## 技能文档格式

遵循 agentskills.io 标准：

```markdown
---
name: <skill-name>
description: <简短描述：何时使用>
---

# <Skill Name>

## When to Use
- 触发条件描述

## Procedure
1. 步骤1
2. 步骤2
3. 步骤3（含错误处理）

## Notes
- 注意事项或变体
```

## 使用方式

### 手动触发
当用户完成复杂任务后，说"提取技能"或"保存为技能"

### 自动建议
系统检测到适合提取的任务后，主动提示：
"这个任务完成得很好，要把它保存为可复用的技能吗？"

### 检索技能
当用户描述新任务时，自动检索相关技能：
```
# 当前任务: <用户描述>
# 匹配技能:
- skill-name: <名称>
  relevance: <相关性>
  trigger: <触发条件>
```
