---
name: memory-assistant
description: 记忆助手 - 帮助用户管理、搜索和组织记忆文件。支持创建记忆条目、按日期或关键词搜索记忆、以及长期记忆的个性化更新。
---

# 记忆助手

这是一个用于帮助用户管理和搜索记忆文件的技能。

## 功能力

### 1. 创建记忆条目

创建新的记忆记录到 daily note 中：

```bash
# 基本创建
echo "今天完成了技能创建" >> memory/$(date +%Y-%m-%d).md
```

### 2. 搜索记忆

使用关键词搜索记忆：

```bash
# 搜索所有记忆文件
rg "关键词" memory/*.md

# 按日期搜索
head -50 memory/2026-07-15.md
```

### 3. 更新长期记忆

将重要信息从 daily notes 合并到 MEMORY.md：

```bash
# 查看最近的 daily notes
ls -la memory/*.md

# 手动编辑 MEMORY.md
nano MEMORY.md
```

## 使用场景

- 记录日常活动和想法
- 搜索历史对话内容
- 整理长期记忆和重要决策
- 项目进度追踪

## 注意事项

- 记忆文件应保持简洁，聚焦于重要信息
- 定期从 daily notes 中提炼内容到 MEMORY.md
- 使用一致的格式和标签便于搜索
