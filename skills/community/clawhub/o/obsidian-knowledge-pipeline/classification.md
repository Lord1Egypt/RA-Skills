# Classification — 自动分类规则和 Wiki 编译标准

## 自动分类规则

### 分类关键词映射表

| 分类 | 目录 | 关键词 | 示例 |
|------|------|--------|------|
| AI应用 | `wiki/知识透视/AI应用/` | vibe trading, claude code, cursor, AI编程, AI助手, chatgpt应用, copilot, AI Agent应用, 智能体应用 | Vibe-Trading、Claude Code、Cursor |
| AI技术 | `wiki/知识透视/AI技术/` | langchain, MCP, RAG, fine-tuning, prompt engineering, transformer, LLM, embedding, function calling, AI框架 | LangChain、MCP、RAG |
| 基础设施 | `wiki/知识透视/基础设施/` | kubernetes, docker, database, redis, kafka, 微服务, 分布式, CI/CD, devops, 监控, 日志, K8s | K8s、Docker、数据库 |
| 金融科技 | `wiki/知识透视/` | 量化交易, 区块链, crypto, defi, fintech, 交易策略, 风控, 支付 | 量化交易、区块链 |
| 人物观点 | `wiki/知识透视/人物观点/` | 访谈, 观点, 演讲, 对话, 创始人, CEO, CTO, 技术领袖 | 黄仁勋访谈、Karpathy |
| 商业与消费 | `wiki/知识透视/商业与消费/` | 市场, 趋势, 产品, 商业模式, 融资, SaaS, 增长, 用户, 消费 | 市场趋势、产品分析 |

### 分类决策树

```
输入：文章标题 + 正文前500字 + meta标签

1. 检查是否有明确人物名+访谈/观点 → 人物观点
2. 检查是否涉及具体AI应用/产品 → AI应用
3. 检查是否涉及AI技术框架/算法 → AI技术
4. 检查是否涉及基础设施/运维 → 基础设施
5. 检查是否涉及金融/交易/区块链 → 金融科技
6. 以上均不匹配 → 商业与消费（默认分类）
```

### 分类结果格式

```json
{
  "category": "AI应用",
  "target_dir": "wiki/知识透视/AI应用/",
  "tags": ["AI编程", "Code-Agent", "自动化"],
  "confidence": "high",
  "related_concepts": ["Claude Code", "Cursor", "MCP"]
}
```

### 边界情况处理

| 场景 | 处理方式 |
|------|----------|
| 跨分类文章（如AI+金融） | 以主要内容倾向决定主分类，标签中包含所有相关分类 |
| 无法明确分类 | 归入"商业与消费"，标记 `classification_confidence: low` |
| 系列文章 | 使用统一的分类和命名前缀，如 `{系列名}-{章节}` |
| 外语文章 | 分类逻辑不变，Wiki编译节点用中文编写 |

---

## Wiki 编译标准 {#wiki-编译标准}

### 6要素定义

每个 Wiki 编译节点必须包含以下6个要素，缺一不可：

#### 1. 定义

```markdown
## 定义
{一句话定义核心概念，简洁精准}
```

- 必须在一句话内完成定义
- 使用"XXX是一种/是一个/是指……"句式
- 禁止使用模糊的形容词

#### 2. 类型/标签

```markdown
## 类型与标签
- **类型**: {AI应用 | AI技术 | 基础设施 | 金融科技 | 人物观点 | 商业与消费}
- **标签**: #{标签1} #{标签2} #{标签3}
```

- 类型必须与自动分类结果一致
- 标签3-7个，包含中英文
- 使用 Obsidian 标签格式 `#tag`

#### 3. 核心内容

```markdown
## 核心内容

### 背景
{1-2句背景介绍}

### 要点
- **要点1**: {描述}
- **要点2**: {描述}
- **要点3**: {描述}

### 关键数据
| 指标 | 数值 |
|------|------|
| {指标} | {数值} |
```

- 要点3-5个，每个不超过2行
- 有具体数据时必须提取到"关键数据"表格
- 不是原文复制，而是结构化摘要

#### 4. 关联概念

```markdown
## 关联概念
- 相关技术：[[概念1]] · [[概念2]] · [[概念3]]
- 应用场景：[[场景1]] · [[场景2]]
- 对比概念：[[对比概念1]]
```

- 至少包含3个双向链接 `[[概念名]]`
- 按关系类型分组（技术/场景/对比）
- 概念名必须与已存在的 Wiki 节点标题完全匹配

#### 5. 来源

```markdown
## 来源
- **原文**: [{文章标题}]({原始URL})
- **作者**: {作者}
- **发布日期**: {YYYY-MM-DD}
- **编译时间**: {YYYY-MM-DD HH:mm}
- **编译者**: OpenClaw Agent
```

- 原文链接必须是完整URL
- 编译时间为 Agent 实际处理时间
- 编译者统一为 "OpenClaw Agent"

#### 6. 配图

```markdown
## 配图

![{主题}配图](../../raw/images/{主题}-配图.png)
```

- 使用相对路径从 Wiki 节点引用 raw/images/ 下的配图
- 路径格式：`../../raw/images/{主题}-配图.png`（从 wiki/知识透视/{分类}/ 回溯到 vault 根）
- 禁止使用绝对路径
- 禁止使用 `assets/` 目录

---

## Wiki 节点完整示例

```markdown
---
title: "Vibe-Trading"
category: AI应用
tags: [AI交易, 量化投资, 自然语言交互]
status: compiled
source_url: "https://example.com/vibe-trading"
compiled_at: "2025-04-25 20:00"
---

# Vibe-Trading

## 定义
Vibe-Trading 是一种利用自然语言交互驱动的AI交易模式，用户通过对话式界面描述交易意图，AI Agent 自动解析并执行交易策略。

## 类型与标签
- **类型**: AI应用
- **标签**: #AI交易 #量化投资 #自然语言交互 #Agent

## 核心内容

### 背景
随着大语言模型的推理能力提升，AI交易从传统的量化策略转向自然语言交互模式。

### 要点
- **对话式交易**: 用户用自然语言描述交易意图
- **策略自动生成**: AI 解析意图并生成可执行策略
- **风控集成**: 内置止损和仓位管理

### 关键数据
| 指标 | 数值 |
|------|------|
| 回测年化收益 | 23.5% |
| 最大回撤 | 8.2% |

## 关联概念
- 相关技术：[[LLM]] · [[Function Calling]] · [[MCP]]
- 应用场景：[[量化交易]] · [[AI Agent]]
- 对比概念：[[传统量化策略]]

## 来源
- **原文**: [Vibe-Trading: AI交易新范式](https://example.com/vibe-trading)
- **作者**: 张三
- **发布日期**: 2025-04-20
- **编译时间**: 2025-04-25 20:00
- **编译者**: OpenClaw Agent

## 配图

![Vibe-Trading配图](../../raw/images/Vibe-Trading-配图.png)
```
