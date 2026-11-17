---
name: wiki-source-ingestion
description: 将网页、论文、代码文档和笔记摄取到不可变 raw 层，并完成元数据、去重、增量价值与冲突判定。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-source-ingestion/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://skills.sh/astro-han/karpathy-llm-wiki/karpathy-llm-wiki
metadata:
  category: 来源摄取
  platform: 通用
  difficulty: 进阶
---

# Wiki 来源摄取

> 先保存可复查的原始证据，再决定它是否值得改变知识层。

## 能力

- 抓取或接收网页、论文、会议纪要、代码和本地文件并规范化存档。
- 记录 URL、作者、发布日期、采集日期、许可证和内容哈希。
- 对来源做重复检测、可信度分级和 New/Update/Disputed/No material 判定。
- 管理大文件指针、受限内容和不可公开来源，而不污染 Git 仓库。

## 使用方式

```text
/wiki-source-ingestion 把这篇论文加入 Wiki，保留原文与发布信息
/wiki-source-ingestion 批量评估 raw/inbox 中哪些来源会改变现有知识
```

执行前读取 `../../references/source-grounding-playbook.md`。能获取原始页面时优先一手来源；无法访问时明确要求用户提供材料，不根据摘要伪造原文。

## 工作流

1. **识别来源** — 判断一手/二手、公开/私有、文本/二进制及许可约束。
2. **获取全文** — 保留原始语义，清除导航噪音但不改写观点。
3. **确定落点** — 写入 `raw/<kind>/YYYY-MM-DD-<slug>.md`；大文件写 `raw/refs/` 指针。
4. **补齐元数据** — 使用 `assets/source.template.md`，记录来源身份和哈希。
5. **查重与检索** — 用 URL、标题、哈希、实体别名搜索 raw 与 wiki。
6. **增量判定** — 标记 New、Update、Disputed 或 No material，可组合的状态明确列出。
7. **写入日志** — 记录来源路径、判定、后续需要编译的页面，No material 也必须留痕。

## 适用场景

- 向技术研究 Wiki 加入论文、RFC、官方文档或事故复盘。
- 将访谈、会议纪要或项目决策作为私有来源沉淀。
- 批量导入历史材料前先做去重与版权边界检查。
- 新来源与现有结论冲突，需要保留双方证据。

## 限制

- 不绕过登录、付费墙、robots、许可证或组织访问控制。
- 不把自动摘要当作原始来源；摘要属于 `wiki/` 知识层。
- 不在摄取阶段一次性并发修改共享 index；来源可并行保存，编译需串行协调。
