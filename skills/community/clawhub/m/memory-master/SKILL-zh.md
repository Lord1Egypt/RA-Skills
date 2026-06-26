---
name: memory-master
version: 2.6.1
description: "本地记忆系统，结构化索引+自动学习。自动写记忆，启发式召回，知识不足时自动网络学习。兼容 self-improving-agent：自动记录 skill 完成和错误到知识库。"
author: 李哲龙
tags: [memory, 记忆, 索引, 上下文]
---

# 🧠 Memory Master — 精准记忆系统

*让你的 AI 助手从遗忘者变成记忆大师。*

---

## ⚠️ v2.6.1 重要更新

**本次更新涉及核心文件迁移，升级前请注意：**

### 迁移内容
- 原 MEMORY.md 中的规则 → 转移到 AGENTS.md
- 原 HEARTBEAT 相关内容 → 迁移到 HEARTBEAT.md
- MEMORY.md → 转型为纯重要教训/经验记录

### ⚠️ 风险提示
1. **会自动修改 AGENTS.md** — 合并规则内容
2. **会自动修改 MEMORY.md** — 转为教训库
3. **会自动创建/更新 HEARTBEAT.md** — 如果用户有相关内容
4. **建议升级前备份 workspace 文件**

### 自动迁移逻辑
```
1. 读取用户现有的 AGENTS.md
2. 检查是否有 HEARTBEAT 相关内容 → 提取到 HEARTBEAT.md
3. 将 memory 相关规则整合到 AGENTS.md
4. 将原 MEMORY.md 转为重要教训库
5. 创建/更新索引文件
```

---

## 核心功能

| 功能 | 说明 |
|---|---|
| 📝 结构化记忆 | "因 → 改 → 待" 格式 |
| 🔄 自动索引同步 | 写一次，索引自动更新 |
| 🎯 零 token 浪费 | 只读需要的，不多读 |
| ⚡ 启发式召回 | 上下文缺失时主动查找 |
| 🧠 自动学习 | 知识不足时自动网络搜索 |
| 🔓 完全控制 | 所有文件可见/可编辑/可删除 |

---

## 记忆格式

### 每日记忆: `memory/daily/YYYY-MM-DD.md`

**格式:**
```markdown
## [日期] 主题
- 因：原因/背景
- 改：做了什么
- 待：待办/后续
```

**示例:**
```markdown
## [2026-03-05] 记忆系统升级
- 因：AGENTS.md 和 MEMORY.md 职责混乱
- 改：规则移至 AGENTS.md，MEMORY.md 转为教训库
- 待：发布新版本
```

---

## 索引格式

### 记忆索引: `memory/daily-index.md`

**格式:**
```markdown
# 记忆索引
- 主题名 → daily/日期.md,日期.md
```

---

## 目录结构

```
~/.openclaw/workspace/
├── AGENTS.md              # 行为准则（规则）
├── MEMORY.md              # 重要教训/经验
├── HEARTBEAT.md           # 心跳任务（可空）
├── memory/
│   ├── daily/             # 每日记录
│   │   └── YYYY-MM-DD.md
│   ├── knowledge/          # 知识库
│   │   └── *.md
│   ├── daily-index.md      # 记忆索引
│   └── knowledge-index.md  # 知识索引
```

---

## 写入规则

### 何时写
- 讨论出结论 → 立刻记录 + 更新索引
- 学到新知 → 立刻记录 + 更新索引
- 写前检查重复/过时内容

### 步骤
1. 检测结论/新知
2. 用"因-改-待"格式
3. 写入 memory/daily/YYYY-MM-DD.md
4. 更新 memory/daily-index.md

---

## 搜索规则

1. 用户有要求 → 按用户要求执行
2. 用户没要求 → 检查上下文有没有规则
3. 上下文没有 → 搜索知识库索引
4. 找到对应项 → 读取知识库文件执行
5. 知识库没有 → 用 tavily/web_fetch 搜索学习 → 写知识库 → 更新索引

---

## 启发式召回

**触发时机：**
- 用户提到你不熟悉的话题
- 当前对话引用了过去的内容
- 你感觉"我不太确定有没有这个信息"

**召回流程:**
```
用户问题 → 上下文缺失？→ 是：读索引 → 定位主题 → 读记忆 → 恢复上下文 → 回答
```

---

## 安装

### 1. 安装
```bash
clawdhub install memory-master
```

### 2. 初始化（v2.6.0 增强版）
```bash
# 自动执行以下操作：
# - 迁移心跳检测规则从 AGENTS.md 到 HEARTBEAT.md
# - 优化 AGENTS.md（去重、精简、重构）
# - 转换 MEMORY.md 为纯教训/经验库
# - 创建 memory 目录结构和索引文件
# - 备份原始文件到 .memory-master-backup/ 目录
clawdhub init memory-master
```

**增强初始化执行的操作：**

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | **备份** | 原始文件保存到 `.memory-master-backup/` |
| 2 | **心跳迁移** | 心跳内容从 AGENTS.md 迁移到 HEARTBEAT.md |
| 3 | **AGENTS.md 优化** | 删除重复、过时规则，精简语言 |
| 4 | **MEMORY.md 转换** | 转为纯教训/经验库 |
| 5 | **记忆结构创建** | 创建 `memory/` 目录和索引文件 |

**初始化后的文件结构：**
```
~/.openclaw/workspace/
├── AGENTS.md              # 优化后的行为准则 + 记忆系统规则
├── MEMORY.md              # 纯教训/经验库
├── HEARTBEAT.md           # 心跳任务和指南
├── memory/
│   ├── daily/             # 每日记录（YYYY-MM-DD.md 格式）
│   ├── knowledge/         # 知识库（*.md 文件）
│   ├── daily-index.md     # 记忆索引
│   └── knowledge-index.md # 知识索引
```

### 3. 手动初始化（高级用户）
```bash
# 1. 直接运行初始化脚本
node ~/.agents/skills/memory-master/scripts/init.js

# 2. 或手动复制模板
cp ~/.agents/skills/memory-master/templates/optimized-agents.md ~/.openclaw/workspace/AGENTS.md
cp ~/.agents/skills/memory-master/templates/heartbeat-template.md ~/.openclaw/workspace/HEARTBEAT.md
cp ~/.agents/skills/memory-master/templates/memory-lessons.md ~/.openclaw/workspace/MEMORY.md

# 3. 创建 memory 目录
mkdir -p ~/.openclaw/workspace/memory/daily
mkdir -p ~/.openclaw/workspace/memory/knowledge

# 4. 创建索引文件
cp ~/.agents/skills/memory-master/templates/daily-index.md ~/.openclaw/workspace/memory/daily-index.md
cp ~/.agents/skills/memory-master/templates/knowledge-index.md ~/.openclaw/workspace/memory/knowledge-index.md
```

---

## 安全与隐私

- **100% 本地**：所有记忆/知识只存在本地文件
- **自动写本地**：这是功能，防止信息丢失
- **自动学习**：网络搜索结果写入本地知识库
- **完全透明**：用户可随时查看/编辑/删除
- **安全**：只发送搜索请求，不上传数据

---

## 触发关键词

### 记忆召回
- "上次"、"之前"、"昨天"、"那个"
- 或：当你意识到没有上下文时

### 知识学习
- 知识库找不到答案时
- 用户问新问题时

### 写记忆
- 讨论出结论
- 做出决定
- 分配任务

---

## 最佳实践

1. **立即写** — 不要等，写在结论后
2. **保持简洁** — 每点一行，保留核心信息
3. **用模板** — 因 → 改 → 待
4. **更新索引** — 写后同步
5. **启发式召回** — 不等用户触发
6. **主动学习** — 不会就说，去学

---

## 压缩检测 (v2.6.3+)

**⚠️ 重要：每次回答后都必须运行！**

### 每次回答后执行：
```bash
node ~/.agents/skills/memory-master/scripts/detect.js
```

在回复最下方显示状态：
- **50%**：`📝 上下文使用率：50% - 是否需要记录记忆或知识库？`
- **70%**：`⚠️ 上下文使用率：70% - 建议记录当前进度`
- **85%**：`🚨 上下文使用率：85% - 请立即记录当前进度！`

### 重要性：
- 防止上下文压缩导致数据丢失
- 在数据丢失前提醒用户记录
- 与心跳检测配合，但运行更频繁

---

> *一个 AI 助手的能力取决于它的记忆。给它一个不忘事、不浪费、总是精确交付的记忆系统。*

**Memory Master v2.6.1 — 记住一切和学到新东西一样重要。** 🧠⚡
