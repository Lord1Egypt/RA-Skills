---
name: wiki-blueprint
description: 为 LLM Wiki 定义范围、受众、成功问题、内容模型、命名、责任与新鲜度契约。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-blueprint/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://skills.sh/daymade/claude-code-skills/llm-wiki-setup
metadata:
  category: Wiki 蓝图
  platform: 通用
  difficulty: 专家
---

# Wiki 蓝图设计

> 先定义知识库要持续回答什么问题，再决定目录、页面和检索技术。

## 能力

- 从用户真实任务中提炼 Wiki 范围、受众、非目标和成功问题。
- 定义概念、实体、来源摘要、解释、决策、查询归档等页面类型。
- 建立命名、链接、状态、责任人、引用和新鲜度契约。
- 在个人 Wiki、项目 Wiki、研究 Wiki 与团队知识库之间选择最小治理强度。

## 使用方式

在支持 Agent Skills 的客户端中调用：

```text
/wiki-blueprint 为我的 Agent Runtime 研究建立 Wiki 蓝图，先访谈再给目录
/wiki-blueprint 审查现有知识库的范围和页面类型是否混乱
```

开始前读取 `../../references/information-architecture-playbook.md`。一次只问一组会改变结构的关键问题；能从用户材料中发现的事实不要反问。

## 工作流

1. **发现任务** — 收集 5–15 个用户希望 Wiki 能稳定回答的问题。
2. **划定范围** — 写清受众、领域边界、敏感数据和明确非目标。
3. **定义内容模型** — 为每种页面规定目的、必需字段和晋升条件。
4. **定义运营契约** — 设定来源政策、Owner、新鲜度 SLO、冲突与弃用状态。
5. **选择检索基线** — 默认索引 + `rg`；把语义检索写成满足阈值后的可选升级。
6. **落盘宪章** — 以 `assets/wiki-config.template.yml` 和 `assets/WIKI.template.md` 为骨架。
7. **验收** — 用三个成功问题走查：能否定位页面、来源和未知项。

## 适用场景

- 从零建设某个技术、产品、投研或阅读主题 Wiki。
- 多人知识库内容持续增多，却没有统一页面契约。
- 现有 Vault 只是文件堆，查询与更新都依赖作者记忆。
- 准备引入 RAG 前，先验证问题是否只是信息架构缺失。

## 限制

- 不替用户决定知识边界、保密级别或法律保留期限。
- 不把示例 Taxonomy 强塞给用户；蓝图必须由真实问题长出来。
- 不负责抓取来源、编写正文或实现检索服务；交给后续子技能。
