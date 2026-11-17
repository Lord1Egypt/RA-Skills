---
slug: "knowledge-graph-skill-free"
name: "knowledge-graph-skill-free"
version: "1.0.0"
displayName: "知识图谱基础版"
summary: "嵌入式知识图谱基础能力,提供核心能力"
summary_zh: "嵌入式知识图谱基础能力,提供核心能力"
license: "MIT"
description: "|- 嵌入式知识图谱基础能力，兼容实体、关系、属性的基础存储 与查询. 核心能力:.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."

  - 实体与关系的基础创建、更新、删除

  - 基础图查询（邻居、路径、属性过滤）

  - 持久化存储与基础检索

  适用场景:

  - AI 模型调用、智能对话、Agent 编排、LLM 应用

  - 独立开发者与小型团队的结构化知识管控

  - 自发化工作流中的知识持久化

  差异化:基础版聚焦实体与关系的基础存储与查询，去除了高级版的图谱推理、跨图谱关联与向量检索能力.
tags:
  - Development
  - Agents
  - Research
  - 工具
  - 效率
  - string
  - action
  - entity_id
tools:
  - read
  - write
  - exec
homepage: ""
category: "Automation"
pricing_tier: free
---
# 知识图谱基础版

## 核心能力

- 实体管理：创建、更新、删除实体节点，支持实体类型、属性与唯一标识
- 关系管理：在实体之间创建有向关系，支持关系类型与属性标注
- 基础图查询：查询实体的邻居、一度/二度关联节点、按属性过滤实体
- 持久化存储：将图谱数据持久化到本地文件（JSON / SQLite），支持加载与导出
- 基础检索：按实体名称、类型、属性值进行基础检索 关键词: knowledge graph skill
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---|---|---|
| 实体创建 | 实体名称与类型 | 实体唯一标识与存储确认 |
| 关系建立 | 源实体、目标实体、关系类型 | 关系记录与关联确认 |
| 邻居查询 | 实体标识与查询深度 | 邻居实体与关系列表 |
| 属性过滤 | 属性键值条件 | 符合条件的实体列表 |
| 图谱导出 | 导出格式 | JSON 或 SQLite 文件路径 |

**不适用于**：复杂图谱推理（如最短路径、社区发现、中心性分析）、跨图谱关联、向量检索与语义相似度、大规模图数据库（如 Neo4j 级别）、实时流式图谱更新等场景（请使用高级版）

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 初始化或加载一个知识图谱实例
3. 按需执行实体创建、关系建立或查询操作
4. 持久化图谱数据到本地文件
5. 输出操作结果与查询数据

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| action | string | 是 | 操作类型，可选: create_entity/update_entity/delete_entity/create_relation/query_neighbors/query_by_property/export/import |
| entity_id | string | 否 | 实体唯一标识，创建与查询时使用 |
| entity_type | string | 否 | 实体类型，如 person/concept/document |
| properties | object | 否 | 实体或关系的属性键值对 |
| relation_type | string | 否 | 关系类型，如 depends_on/related_to/authored_by |
| source_id | string | 否 | 关系的源实体标识 |
| target_id | string | 否 | 关系的目标实体标识 |
| query_depth | integer | 否 | 邻居查询深度，默认: 1，最大: 2 |
| strict_level | string | 否 | 审查严格度，可选: strict/normal/loose，默认: normal |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_status": "ok",
    "action": "query_neighbors",
    "result": {
      "entity": {
        "id": "entity_001",
        "type": "person",
        "name": "张三"
      },
      "neighbors": [
        {
          "relation": "authored_by",
          "direction": "outgoing",
          "entity": {
            "id": "entity_002",
            "type": "document",
            "name": "架构设计文档"
          }
        },
        {
          "relation": "depends_on",
          "direction": "outgoing",
          "entity": {
            "id": "entity_003",
            "type": "concept",
            "name": "微服务架构"
          }
        }
      ],
      "neighbor_count": 2
    },
    "stats": {
      "total_entities": 24,
      "total_relations": 56,
      "query_duration_ms": 80
    }
  },
  "error": null
}
```

## 异常处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 实体不存在 | entity_id 未找到 | 提示用户先执行 create_entity 创建实体 |
| 关系建立失败 | source_id 或 target_id 不存在 | 提示用户确认两端实体存在后再建立关系 |
| 图谱未初始化 | 未加载或创建图谱实例 | 提示用户先执行 import 或初始化新图谱 |
| 持久化失败 | 文件路径不可写或磁盘空间不足 | 检查路径权限与磁盘空间后检查网络连接和配置后重试 |
| 查询深度超限 | query_depth 超过 2 | 提示基础版最大支持 2 度查询，建议缩小深度 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md规范的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于指令驱动，无需额外API Key（除内容中明确标注的外部API）

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行图谱操作

## 案例展示

### 示例1：创建实体并建立关系

```
输入: action=create_entity, entity_type=person, properties={name:"张三"}
处理: 生成唯一标识 -> 存储实体 -> 返回 entity_id
输出: 实体已创建，entity_id=entity_001
```

### 示例2：查询邻居节点

```
输入: action=query_neighbors, entity_id=entity_001, query_depth=1
处理: 查找该实体的所有一度邻居 -> 按关系类型分组 -> 返回结果
输出: 2 个邻居，分别为文档与概念实体
```

## 常见问题

### Q1: 如何开始使用知识图谱基础版？
A: 查看使用流程章节，初始化或加载一个图谱实例，然后按"输入格式"提供 action 与相关参数即可.
### Q2: 图谱数据如何持久化？
A: 基础版支持 JSON 与 SQLite 两种持久化格式，可通过 export 操作导出到本地文件，下次使用时通过 import 加载.
### Q3: 知识图谱基础版支持图谱推理吗？
A: 不支持。基础版仅提供实体、关系与基础查询，如需最短路径、社区发现、中心性分析、跨图谱关联与向量检索，请升级至高级版.
### Q4: 如何获取图谱推理、跨图谱关联、向量检索等高级能力？
A: 这些属于高级版能力。基础版聚焦实体与关系的基础存储与查询，如需复杂推理、语义相似度检索与大规模图谱分析，请升级至高级版.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:---------|---------:|:---------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 不支持图谱推理（最短路径、社区发现、中心性分析、联通分量）
- 不支持跨图谱关联与多图谱合并
- 不支持向量检索与语义相似度查询
- 不支持大规模图数据库（如 Neo4j、JanusGraph 级别）的性能优化
- 查询深度最大为 2 度，更深的查询需要拆分为多次操作
- 不支持实时流式图谱更新与增量索引
- 不支持图算法库（如 PageRank、Betweenness Centrality）
- 持久化仅支持本地文件，不支持远程图数据库接入
