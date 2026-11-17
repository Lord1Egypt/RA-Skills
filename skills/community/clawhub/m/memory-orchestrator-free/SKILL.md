---
slug: "memory-orchestrator-free"
name: "memory-orchestrator-free"
version: "1.0.0"
displayName: "记忆编排器免费版"
summary: "基础两层记忆管理，支持关键词检索与简单摘要，本地持久化存储。记忆编排器免费版提供基础记忆管理能力，支持短期与长期两层记忆架构. 核心能力包括：两层记忆存储（短期/长期）、关键词检索、基础摘要"
summary_zh: "基础两层记忆管理，支持关键词检索与简单摘要，本地持久化存储。记忆编排器免费版提供基础记忆管理能力，支持短期与长期两层记忆架构. 核心能力包括：两层记忆存储（短期/长期）、关键词检索、基础摘要"
license: "MIT"
description: "|-. 适用于需要memory orchestrator相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  记忆编排器免费版提供基础记忆管理能力，支持短期与长期两层记忆架构.
  核心能力包括：两层记忆存储（短期/长期）、关键词检索、基础摘要生成、本地持久化.
  适用于简单的 Agent 记忆管理场景：当前会话上下文存储、基础偏好记录.
  无需向量数据库，无需额外 API Key，开箱即用.
  如需四层架构、混合检索、健康度仪表盘、并发冲突解决等高级能力，请升级到付费版.
tools:
  - read
  - write
  - exec
homepage: ""
tags:
  - 智能助手
  - memory
  - orchestrator
  - automation
  - productivity
  - 记忆管理
  - 上下文
  - AI
  - action
  - agent
category: "Agents"
pricing_tier: free
---
# 记忆编排器免费版

基础记忆管理系统，两层架构与关键词检索.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 记忆编排器免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力

### 1. 两层记忆存储
短期记忆与长期记忆两层架构，满足基础存储需求.
- **参数**：`type`（short-term/long-term）、`content`、`persist`
- **用法**：添加记忆时指定类型
- **输出**：写入确认与记忆 ID

| 层级 | 名称 | 容量 | 清理策略 |
|:-----|:-----|:-----|:-----|
| 领先层 | 短期记忆 | 上限 100 条 | FIFO 淘汰 |
| 第二层 | 长期记忆 | 无上限 | 手动管理 |

### 2. 关键词检索

通过关键词匹配检索记忆条目.
- **参数**：`query`（搜索关键词）、`limit`
- **用法**：`action: "search"`、`searchMode: "keyword"`
- **输出**：匹配的记忆条目列表

```typescript
const result = await skills.memoryOrchestrator({
  action: "search",
  query: "用户偏好",
  limit: 5,
  searchMode: "keyword"
});
```

### 3. 基础摘要生成
对短期记忆生成简单摘要，控制上下文体积.
- **参数**：`typeFilter`、`maxTokens`（默认 500）
- **用法**：`action: "summarize"` 触发摘要生成
- **输出**：结构化摘要

### 4. 本地持久化

保存记忆到磁盘文件，重启后可加载.
- **参数**：`persistPath`（默认 `./memory-store.json`）
- **用法**：`action: "save"` 保存，`action: "load"` 加载
- **输出**：持久化文件

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

### 领先步：添加记忆

根据内容持久性需求选择短期或长期记忆类型.
```typescript
await skills.memoryOrchestrator({
  action: "add",
  content: "用户喜欢喝咖啡，不加糖",
  type: "long-term",
  persist: true
});
```

### 第二步：检索记忆

使用关键词检索查找相关记忆条目.
```typescript
memoryOrchestrator({
  action: "search",
  query: "用户喜好",
  limit: 3,
  searchMode: "keyword"
});
```

### 第三步：持久化保存

将记忆保存到磁盘，确保重启不丢失.
```typescript
await skills.memoryOrchestrator({
  action: "save",
  persistPath: "./my-memory.json"
});
```

## 错误处理

| 错误类型 | 原因 | 处理方式 |
|---:|---:|---:|
| 搜索结果不准 | 关键词检索无法匹配语义相似内容 | 精确查询用 keyword 模式，模糊查询建议升级到付费版使用 hybrid 模式 |
| 持久化失败 | persistPath 路径无写入权限 | 检查 persistPath 写入权限，确认磁盘空间充足后检查网络连接和配置后重试 |
| 短期记忆爆满 | 超 100 条上限未清理 | 触发 FIFO 淘汰，最旧条目自动移除，或手动清理过期记忆 |

## 示例

### 示例一：基础偏好记忆管理

用户需要记录偏好信息，并在后续会话中检索.
```text
用户："记住我喜欢深色模式，不加糖的咖啡"
# ...
执行：
1. 添加长期记忆：
   await skills.memoryOrchestrator({
     action: "add",
     content: "用户喜欢深色模式，喝咖啡不加糖",
     type: "long-term",
     persist: true
   });
# ...
2. 持久化保存：
   await skills.memoryOrchestrator({
     action: "save",
     persistPath: "./my-memory.json"
   });
# ...
3. 后续会话检索：
memoryOrchestrator({
     action: "search",
     query: "用户偏好",
     limit: 3,
     searchMode: "keyword"
   });
   // 返回："用户喜欢深色模式，喝咖啡不加糖"
```

## FAQ

### Q1：免费版支持几层记忆架构？

免费版提供两层：短期记忆（上限 100 条，FIFO 淘汰）和长期记忆（无上限，手动管理）。如需工作记忆（上限 20 条，超限自动晋升）和重要记忆（永不清理）层级，请升级到付费版获取完整四层架构.
### Q2：能用语义检索吗？

免费版仅支持关键词检索（keyword 模式）。语义检索（semantic）和混合检索（hybrid）需要向量数据库支持，属于付费版功能。如需模糊查询与高召回率检索，请升级到付费版.
### Q3：多 Agent 能同时写入吗？

免费版不支持并发写入冲突解决。多 Agent 同时写入可能导致数据覆盖。如需乐观锁 + 版本合并的并发安全写入，请升级到付费版.
## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux

### 依赖项

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

本技能核心功能无需额外 API Key（LLM 由 Agent 平台提供）.
### 可用性分类

- **分类**：MD+EXEC（Markdown 指令驱动，部分功能需 exec 执行持久化操作）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 管理两层记忆系统

## 已知限制

- 仅支持两层记忆架构（短期/长期），无工作记忆与重要记忆层级
- 仅支持关键词检索，不支持语义检索与混合检索
- 不支持并发写入冲突解决，多 Agent 同时写入可能数据覆盖
- 无记忆健康度仪表盘，无法量化记忆状态与主动告警
- 无自动清理机制，短期记忆超 100 条仅 FIFO 淘汰，无智能归档
- 摘要生成无质量评估器，需手动审查摘要准确性

## 升级提示

本免费版提供基础记忆管理能力。升级到付费版可获得以下增强：

- **四层记忆架构**：工作/短期/长期/重要四层清晰分工，每层独立容量与清理策略，重要信息永不清理
- **三模式检索**：关键词/语义/混合三种检索模式，混合模式加权打分兼顾精确与召回
- **记忆健康度仪表盘**：容量/分布/命中率/陈旧度四维量化指标，主动告警异常情况
- **并发写入冲突解决**：乐观锁 + 版本合并策略，支持多 Agent 安全并发写入
- **摘要质量评估器**：信息保留率/压缩比/可读性/准确性四维指标，不达标自动重试
- **过期记忆自动清理**：按层级与规则自动清理，7 天未访问归档，180 天未引用提示遗忘
- **模块化扩展接口**：语义检索可插拔对接向量数据库（Chroma/LanceDB/Qdrant），无向量库时自动降级

如需这些高级能力，请升级到记忆编排器付费版.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "记忆编排器免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "memory-orchestrator"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
