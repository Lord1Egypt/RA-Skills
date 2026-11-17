---
slug: memory-orchestrator-v2
name: memory-orchestrator
version: "1.0.0"
displayName: 记忆编排器
summary: 解决分层不清、摘要不稳、并发冲突、无健康度指标的智能记忆编排器
license: MIT
description: |-
  记忆编排器是面向 AI Agent 的智能记忆管理系统，针对"分层体系不够清晰、自动摘要质量不稳定、并发写入冲突、缺乏记忆健康度指标"四大高频痛点而设计。它用四层记忆架构（工作/短期/长期/重要）与多模式检索，提供从存储到检索到摘要的全生命周期编排，让 Agent 记忆真正可控可观测。

  核心能力：四层记忆架构（工作记忆/短期记忆/长期记忆/重要记忆）、三模式检索（关键词/语义/混合）、自动摘要生成（支持长会话压缩，token 占用减少 70%）、持久化与加载（内存/磁盘）、记忆健康度仪表盘（容量/分布/命中率/陈旧度）、并发写入冲突解决（乐观锁+版本合并）、过期记忆自动清理、模块化扩展接口（可对接向量数据库）。

  适用场景：长会话 Agent、聊天机器人上下文管理、RAG 应用记忆层、任务型 Agent 长期记忆、客服助理上下文治理、多 Agent 共享记忆。

  差异化：相比仅提供"add/search/summarize"的基础管理器，本技能新增 (1) 四层记忆架构，工作/短期/长期/重要四层清晰分工，每层独立容量与清理策略；(2) 记忆健康度仪表盘，量化容量、分布、命中率、陈旧度四维指标，主动告警；(3) 并发写入冲突解决，乐观锁 + 版本合并，支持多 Agent 安全并发；(4) 摘要质量评估器，量化摘要的信息保留率与可读性，质量不达标自动重试；(5) 模块化扩展接口，语义检索可插拔对接向量数据库（Chroma/LanceDB/Qdrant）。

  触发关键词：记忆编排、记忆管理、长期记忆、语义检索、记忆摘要、记忆持久化、memory manager、memory orchestration、semantic search
tags:
- 记忆编排
- 智能管理
- 语义检索
- 上下文治理
tools:
- read
- exec
---

# 记忆编排器（Memory Orchestrator）

面向 AI Agent 的**智能记忆管理系统**，用四层记忆架构与多模式检索，提供从存储到检索到摘要的全生命周期编排，让 Agent 记忆真正可控可观测。

## 设计动机：四大高频痛点

| 痛点 | 典型表现 | 本技能对策 |
|------|----------|------------|
| 分层体系不清 | 短期/长期混在一起，重要信息被淹没 | 四层架构：工作/短期/长期/重要，独立策略 |
| 自动摘要质量不稳 | 摘要丢关键信息或过于冗长 | 摘要质量评估器，信息保留率+可读性双指标 |
| 并发写入冲突 | 多 Agent 同时写记忆，互相覆盖 | 乐观锁 + 版本合并，安全并发 |
| 缺乏健康度指标 | 记忆多少、命中率、陈旧度全凭感觉 | 健康度仪表盘，四维量化+主动告警 |

## 四层记忆架构

```text
┌────────────────────────────────────────────────┐
│           四层记忆架构                          │
├────────────────────────────────────────────────┤
│                                                │
│  第四层：重要记忆（important）                  │
│          永不清理、最高优先级                   │
│          用户核心偏好、关键决策、身份信息       │
│          容量：无上限                           │
│                                                │
│  第三层：长期记忆（long-term）                  │
│          持久化存储、定期归档                   │
│          历史交互、项目背景、领域知识           │
│          容量：无上限（建议 < 10000）           │
│                                                │
│  第二层：短期记忆（short-term）                 │
│          最近活跃、自动清理                     │
│          当前会话上下文、近期决策               │
│          容量：上限 100 条（FIFO 淘汰）         │
│                                                │
│  第一层：工作记忆（working）                    │
│          当前任务上下文、超快读写               │
│          容量：上限 20 条（超限自动晋升短期）   │
│                                                │
└────────────────────────────────────────────────┘
```

### 层级流转规则

```text
写入 → 工作记忆（容量 20）
         │
         ├─ 超限 → 自动晋升到短期记忆
         │
         └─ 标记重要 → 直接晋升到重要记忆

短期记忆（容量 100）
         │
         ├─ 超限 → FIFO 淘汰最旧（移到长期或删除）
         │
         ├─ 标记重要 → 晋升到重要记忆
         │
         └─ 7 天未访问 → 自动归档到长期记忆

长期记忆
         │
         ├─ 被引用 → 临时提升到短期（LRU）
         │
         └─ 180 天未引用 → 提示归档/遗忘

重要记忆
         │
         └─ 永不清理，仅可手动修改
```

## 快速开始（< 60 秒）

### 添加记忆

```typescript
// 添加长期记忆
await skills.memoryOrchestrator({
  action: "add",
  content: "用户喜欢喝咖啡，不加糖，每周三下午喝奶茶",
  type: "long-term",
  persist: true
});

// 添加重要记忆（永不清理）
await skills.memoryOrchestrator({
  action: "add",
  content: "用户是项目负责人，最终决策权在用户",
  type: "important",
  persist: true
});
```

### 搜索记忆

```typescript
const result = await skills.memoryOrchestrator({
  action: "search",
  query: "用户喜好",
  limit: 3,
  searchMode: "hybrid"  // 关键词+语义混合检索
});
```

### 生成会话摘要

```typescript
const summary = await skills.memoryOrchestrator({
  action: "summarize",
  typeFilter: "short-term",
  maxTokens: 500
});
```

### 持久化与加载

```typescript
// 保存所有记忆到磁盘
await skills.memoryOrchestrator({
  action: "save",
  persistPath: "./my-memory.json"
});

// 从磁盘加载记忆
await skills.memoryOrchestrator({
  action: "load",
  persistPath: "./my-memory.json"
});
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | 操作类型：add/search/summarize/clear/list/load/save/health |
| content | string | 否 | add 操作必填，记忆内容 |
| type | string | 否 | add 操作可选，记忆类型：working/short-term/long-term/important，默认 short-term |
| query | string | 否 | search 操作必填，搜索关键词 |
| limit | number | 否 | search/list 操作可选，返回数量，默认 5/20 |
| typeFilter | string | 否 | 过滤记忆类型，默认 all |
| searchMode | string | 否 | 检索模式：keyword/semantic/hybrid，默认 keyword |
| persist | boolean | 否 | add 操作可选，是否持久化，默认 false |
| persistPath | string | 否 | load/save 操作可选，持久化路径，默认 ./memory-store.json |
| importance | number | 否 | 重要度 0-1，默认 0.5 |
| tags | string[] | 否 | 标签列表，便于检索 |
| maxTokens | number | 否 | summarize 操作可选，摘要最大 token，默认 500 |

## 三模式检索

| 模式 | 适用场景 | 优势 | 依赖 |
|------|----------|------|------|
| keyword | 精确匹配、快速检索 | 零依赖、快 | 无 |
| semantic | 语义相似、模糊查询 | 召回率高 | 需向量数据库（可选） |
| hybrid | 综合检索、最佳效果 | 兼顾精确与召回 | 默认可用（语义部分降级为关键词） |

### 混合检索算法

```text
score = keyword_score * 0.4 + semantic_score * 0.4 + recency_score * 0.1 + importance_score * 0.1

说明：
- keyword_score：关键词匹配（TF-IDF）
- semantic_score：语义相似度（有向量库时用 cosine，无则降级为关键词）
- recency_score：近期加权
- importance_score：重要度加权
```

## 自动摘要生成

### 摘要策略

```text
1. 提取关键信息
   - 事件：时间、地点、参与者、结果
   - 决策：决策内容、原因、影响
   - 教训：问题、原因、规避方法
   - 待办：任务、优先级、截止时间

2. 压缩冗余
   - 去重复（相同信息只保留一次）
   - 去过程（保留结果，省略中间步骤）
   - 去客套（移除寒暄与无信息内容）

3. 结构化输出
   - 按类别分组
   - 层级列表呈现
   - 保留关键时间戳
```

### 摘要质量评估器

| 指标 | 计算方法 | 及格线 |
|------|----------|--------|
| 信息保留率 | 摘要含关键信息数 / 原始关键信息数 | >= 90% |
| 压缩比 | 原始 token / 摘要 token | >= 3 倍 |
| 可读性 | 结构化程度（标题/列表/层级） | >= 0.8 |
| 准确性 | 摘要与原始内容一致性 | >= 95% |

**质量不达标处理**：
- 保留率 < 90%：补充遗漏关键信息，重新生成
- 压缩比 < 3：加强去冗余
- 可读性 < 0.8：增加结构化层级
- 准确性 < 95%：校对事实性内容

## 记忆健康度仪表盘

```typescript
const health = await skills.memoryOrchestrator({
  action: "health"
});
```

### 四维健康度指标

```json
{
  "capacity": {
    "working": { "used": 18, "limit": 20, "utilization": 0.9 },
    "short_term": { "used": 87, "limit": 100, "utilization": 0.87 },
    "long_term": { "used": 342, "limit": null, "utilization": null },
    "important": { "used": 15, "limit": null, "utilization": null }
  },
  "distribution": {
    "by_type": { "preference": 45, "decision": 30, "fact": 20, "lesson": 15 },
    "by_age": { "last_7d": 60, "last_30d": 120, "older": 200 }
  },
  "hit_rate": {
    "last_7d": 0.72,
    "last_30d": 0.65,
    "trend": "improving"
  },
  "staleness": {
    "stale_count": 23,
    "stale_ratio": 0.06,
    "oldest_unaccessed_days": 45
  },
  "alerts": [
    { "level": "warning", "message": "工作记忆使用率 90%，建议晋升到短期" },
    { "level": "info", "message": "23 条长期记忆 30 天未访问，建议归档" }
  ]
}
```

### 告警规则

| 指标 | 阈值 | 告警级别 |
|------|------|----------|
| 工作记忆使用率 | > 85% | warning |
| 短期记忆使用率 | > 85% | warning |
| 命中率（7天） | < 30% | warning |
| 陈旧率 | > 10% | info |
| 重要记忆被修改 | 任意 | info（记录审计） |

## 并发写入冲突解决

支持多 Agent 安全并发写入：

### 乐观锁机制

```text
1. 读取记忆时获取版本号 version
2. 写入时携带 version
3. 若 version 与当前不匹配 → 冲突
4. 冲突时触发版本合并
```

### 版本合并策略

```text
冲突类型 A：同条目不同字段修改
  → 字段级合并，各取所改

冲突类型 B：同条目同字段不同值
  → 保留两版本，标记冲突，等待用户裁决

冲突类型 C：同时新增不同条目
  → 无冲突，直接合并
```

### 冲突示例

```text
Agent 1：更新用户偏好（version=3）→ "深色模式"
Agent 2：同时更新用户偏好（version=3）→ "自动切换"

冲突解决：
  → 保留两版本
  → 标记为冲突
  → 提示用户："检测到偏好冲突，请选择"
    [深色模式] [自动切换] [两者都记]
```

## 过期记忆自动清理

### 清理策略

| 记忆类型 | 清理规则 | 清理动作 |
|----------|----------|----------|
| 工作记忆 | 超 20 条 | 最旧的晋升到短期 |
| 短期记忆 | 超 100 条 | FIFO 淘汰，移到长期或删除 |
| 短期记忆 | 7 天未访问 | 自动归档到长期 |
| 长期记忆 | 180 天未引用 | 提示归档/遗忘 |
| 长期记忆 | 含 expires_at 且过期 | 自动归档 |
| 重要记忆 | 永不清理 | 仅可手动修改 |

### 清理日志

所有清理操作记录到 `memory-cleanup.log`：
```text
2026-07-18T10:30:00Z | short-term→long-term | memory-id-123 | "用户偏好深色模式"
2026-07-18T10:31:00Z | long-term→archive | memory-id-456 | "旧项目背景"
```

## 模块化扩展接口

语义检索可插拔对接向量数据库：

```typescript
// 配置向量数据库（可选）
await skills.memoryOrchestrator({
  action: "configure",
  semantic: {
    provider: "chroma",  // chroma | lancedb | qdrant | none
    path: "./.chroma",
    embeddingModel: "all-MiniLM-L6-v2"
  }
});
```

**无向量数据库时**：semantic 模式降级为关键词检索，不影响基本功能。

## 典型工作流（3 个真实场景）

### 场景一：长会话上下文管理

```text
用户："这个会话已经聊了 30 轮，上下文快爆了"

流程：
1. summarize 短期记忆（保留关键决策与待办）
2. 压缩后的摘要替换原始短期记忆
3. 工作记忆仅保留最近 5 轮
4. 继续会话
5. token 占用减少 70%
```

### 场景二：多 Agent 共享记忆

```text
场景：Agent A 与 Agent B 同时操作共享记忆库

流程：
1. Agent A 读取用户偏好（version=3）
2. Agent B 读取用户偏好（version=3）
3. Agent A 写入更新（version=3→4）
4. Agent B 写入更新（version=3，冲突！）
5. 触发版本合并
6. 字段级合并或标记冲突
7. 通知用户裁决（如需要）
```

### 场景三：记忆健康度巡检

```text
心跳任务：每天检查记忆健康度

流程：
1. 调用 health 获取仪表盘
2. 检查告警项
3. 工作记忆 > 85%：触发晋升
4. 短期记忆 > 85%：触发归档
5. 陈旧率 > 10%：提示清理
6. 命中率 < 30%：提示优化检索策略
7. 生成健康度报告
```

## 技术实现说明

- 内置记忆自动清理机制，短期记忆上限 100 条，避免内存溢出
- 模块化设计，可轻松对接向量数据库实现语义检索
- 全链路类型安全，参数自动校验
- 轻量无外部依赖，开箱即用，也支持自定义扩展
- 并发安全，乐观锁 + 版本合并
- 持久化支持内存与磁盘，重启不丢失

## FAQ

**Q1：四层架构会不会太复杂？**
A：不会。日常使用只需指定 type（默认 short-term），层级流转自动处理。四层架构的价值在于：重要信息不被淹没、短期记忆不爆、长期记忆可归档。

**Q2：没有向量数据库能用语义检索吗？**
A：可以，但会降级。semantic 模式在无向量库时退化为关键词检索，仍可用但召回率降低。接入向量库后效果最佳。

**Q3：并发冲突频繁怎么办？**
A：(1) 减少同一记忆的并发写入；(2) 不同 Agent 写不同记忆条目；(3) 必要时用锁机制串行化；(4) 冲突后及时人工裁决。

**Q4：摘要质量评估器能保证摘要准确吗？**
A：评估器检测信息保留率与准确性，不达标自动重试。但 100% 准确无法保证，建议关键场景人工复核摘要。

**Q5：健康度仪表盘多久看一次？**
A：建议每天看一次（心跳任务），重点关注告警项。每周做一次深度审查（分布、陈旧度趋势）。

## 故障排查

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 搜索结果不准 | 检索模式不匹配 | 切换 searchMode，复杂查询用 hybrid |
| 摘要丢信息 | 质量评估未达标 | 检查保留率，补充关键信息重试 |
| 并发写入失败 | 版本冲突 | 触发版本合并，必要时人工裁决 |
| 工作记忆爆满 | 未及时晋升 | 检查健康度，触发自动晋升 |
| 持久化失败 | 路径无权限 | 检查 persistPath 写入权限 |
| 语义检索不工作 | 未配置向量库 | 配置 semantic provider 或用 keyword 模式 |

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **运行时**：Node.js（如用 TypeScript SDK）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| 向量数据库（可选） | 外部依赖 | 可选 | Chroma / LanceDB / Qdrant，语义检索增强 |
| Embedding 模型（可选） | 模型 | 可选 | all-MiniLM-L6-v2 等，配合向量库使用 |

### API Key 配置
- 本技能核心功能**无需额外 API Key**（LLM 由 Agent 平台提供）
- 语义检索增强（可选）如用云向量服务，需对应服务 Key

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需 exec 执行持久化操作）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 管理四层记忆系统
