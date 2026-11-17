# Obsidian 笔记样式指南

## Key takeaway

`Key takeaway` 使用 Obsidian callout，高亮显示：

```markdown
## Key takeaway

> [!tip] Key takeaway
> 一句话写出最值得复用的结论。
>
> 一小段解释为什么重要、何时适用、复用时最不能忘记什么。
```

写作要求：

1. 第一段只能是一句话，直接给结论。
2. 第二段是一小段解释，说明适用场景、核心动作和复用边界。
3. 不要复述标题，不要写“本文很有价值”这类空话。

强示例：

> 工作项目归档笔记必须把原始材料的主线、事实、机制、案例和可复制启示整理进正文，而不是只保留来源链接和页码。
>
> 这适用于 PDF、PPTX、微信推文和工作汇报等资料归档。页码和链接只用于证据追踪，正文要成为可直接阅读和复用的知识资产。

弱示例：

> 这篇笔记整理了一个项目资料。
>
> 它对以后有帮助，可以提升效率。

## Properties

使用 YAML frontmatter。字段应稳定、可搜索：

- `created_by`：通常为 `Codex`。
- `created_at`：本地日期，格式 `YYYY-MM-DD`。
- `updated_at`：本地日期，格式 `YYYY-MM-DD`；新建笔记时与 `created_at` 相同。
- `created_method`：简洁说明创建方式，如 `pdf-to-obsidian-note`、`url-to-obsidian-note`。
- `source`：如 `conversation`、`meeting`、`pdf`、`url`、`document`、`repo`、`manual`、`url-and-document`、`url-and-images`。不要写成长句说明；详细来源放入 `Key references`。
- `project`：明确项目或业务名称。
- `topic`：具体主题。
- `note_type`：常用值包括 `agent-workflow`、`project-note`、`technical-note`、`decision-record`、`reference-note`、`business-report`。
- `knowledge_type`：常用值包括 `workflow`、`setup`、`decision`、`reference`、`troubleshooting`、`project-context`。
- `status`：`captured`、`draft`、`validated` 或 `needs-review`。
- `confidence`：`high`、`medium` 或 `low`。
- `related_projects`：相关项目列表，可为空。
- `related_notes`：相关 Obsidian 笔记标题列表，可为空；这些笔记应在 `文件引用` 中解释关系。
- `tags`：2-6 个稳定主题标签。

`tags` 规范：

- 只放主题分类，不放 `note_type`、年份、状态或创建方式。
- 禁止纯数字标签，例如 `2022`、`2026`。
- 禁止含特殊符号的标签，例如 `樾+`、`樾⁺`、`社群+`、`A/B`。
- 正文、标题和内部链接可以保留正式品牌写法；标签要转成稳定写法，例如 `樾+` 写成 `樾生活方式`。
- 不要写与字段重复的标签，例如 `project-note`、`validated`、`url`。

不要在 Properties 中加入 `links`。URL、本地路径和外部证据统一放入 `## Key references`；Obsidian 内部笔记标题放入 `related_notes` 并在 `## 文件引用` 中说明关系。

## 摘要

`摘要` 放在 `Key takeaway` 后、`Context` 前，使用 Obsidian callout，并固定三条 bullet。

工作项目归档笔记推荐：

```markdown
## 摘要

> [!summary] 摘要
> - 核心内容：
> - 关键机制：
> - 可复用价值：
```

技术/工具/Agent 工作流笔记可改为：

```markdown
## 摘要

> [!summary] 摘要
> - 优先路径：
> - 验证闭环：
> - 主要坑点：
```

要求：

- 恰好三条 bullet。
- 每条尽量一行内说清。
- 不要重复 `Key takeaway` 的解释段。

## Context

`Context` 立即放在摘要后，用 Obsidian callout：

```markdown
## Context

> [!info] Context
> - 背景：
> - 目标：
> - 当前状态：
> - 适用范围：
```

要求：

- 保持简洁，用于快速定位来源和适用范围，不要复制整篇正文。
- 如果用户提供了微信或其他平台 URL，必须在 `Context` 中保留原始 URL。
- 网页 URL 使用 Markdown 链接格式，确保在 Obsidian 中可点击；链接文字优先使用内容标题、页面标题、文档标题、仓库名或平台入口名，例如 `[我们一起奔赴热爱](https://mp.weixin.qq.com/...)`。无法确定标题时才使用 `[微信原文](...)` 或 `[来源链接](...)`。不要写成反引号代码格式。
- 用户提供的 URL 也必须在 `Key references` 中再次保留，便于证据追踪。

## 正文内容块

工作项目归档笔记优先使用：

```markdown
## 原始内容完整整理
## 机制 / 模式
## 案例 / 对比
## 可复制启示
```

写作要求：

- `原始内容完整整理`：保留材料主线、章节、事实、数据、结论，不要只写摘要。
- `机制 / 模式`：提炼流程、角色、数据链路、经营模式、治理方式或方法论。
- `案例 / 对比`：整理区域样本、项目样板、竞品/标杆、前后差异或代表案例。
- `可复制启示`：沉淀写作结构、模板化做法、适用条件和注意事项。
- 如果来源中确实没有机制或案例，对应章节可以省略，但不能因为省事而省略。

技术/工具类笔记可以使用更适合的结构，例如：

- `## Key points`
- `## Workflow / Method`
- 配置表
- 验证清单
- 故障与处理表

通用要求：

- H2 用于稳定大段落，H3 用于可扫描子主题。
- 事实、决策、数据、注意事项优先用 bullet 或表格。
- 表格适合用于数据、机制、选项对比、字段定义、复用模板。
- Mermaid 只在流程或关系图能明显提升理解时使用。
- 工作项目归档笔记不能写成“去看原文第几页”的指针；页码只能作为证据。

## 后续可复用关键信息

本节用于沉淀未来复用这篇笔记时真正有用的信息。

工作项目归档笔记：

- 只写复用口径、模板沉淀、数据口径、机制抽象、适用条件、注意事项。
- 不写原始文件路径、URL 或页码；这些统一放 `Key references`。临时抽取文本、HTML 抓取件和工作区副本只作为消化过程材料，笔记完成后默认不保留引用。
- 不写泛泛的“后续可以继续优化”。

推荐结构：

```markdown
## 后续可复用关键信息

### 复用口径

| 复用对象 | 可复用内容 | 使用条件 |

### 模板沉淀

| 场景 | 可复制结构 | 注意事项 |
```

Agent/技术笔记可以使用：

```markdown
## 后续可复用关键信息

### 环境与入口

| 项 | 值 | 用途 |

### 迁移与验证

| 检查项 | 标准 | 失败时处理 |
```

## Key references

`Key references` 是唯一外部来源区。

可放内容：

- 用户提供 URL。
- 微信文章链接、正式发布页、长期保存的原始网页导出。
- PDF、DOCX、PPTX、EXCEL、CSV 等原始文件路径。
- 关键页码、章节、sheet、slide。
- 官方文档、OpenAPI endpoint、repo 路径、工具输出文件。

不要放：

- Obsidian 内部 wiki 链接。
- 泛泛的“可参考某某主题”。
- 已经不存在或没有实际读取依据的来源。
- 临时抽取文本、HTML 抓取件和工作区副本，除非它本身被明确保留为长期可复核来源。

URL 格式规则：

- 网页、微信、在线文档、官方文档等 URL 写成 Markdown 链接：`[内容标题](https://...)`。
- 链接文字要短而明确，优先使用文章标题、页面标题、文档标题、仓库名或平台入口名，例如 `[我们一起奔赴热爱](...)`、`[obsidian-notes-skill](...)`、`[腾讯文档首页](...)`。
- 只有无法确认内容标题时，才使用 `[微信原文](...)`、`[官方文档](...)`、`[来源链接](...)` 这类通用命名。
- 不要用反引号包裹网页 URL；反引号只用于本地路径、文件名、API endpoint、命令、端口和字段名。
- Windows 本地路径不强制做 Markdown 链接，默认用反引号保留原样。

如果没有来源，省略对应来源小节，不要生成 `None captured` 空占位。

## 文件引用

`文件引用` 用于把笔记变成个人知识库中的节点，只放 Obsidian 内部 wiki 链接。

默认结构：

```markdown
## 文件引用

### 上游来源

- [[已有来源笔记]]：说明该笔记如何提供来源、背景、前置判断或旧版本。

### 相关主题

- [[相关主题笔记]]：说明它们之间的业务、项目、机制或案例关系。
```

规则：

- `上游来源`：用于这篇笔记总结、修正、扩展或依赖的已有 Obsidian 笔记。
- `相关主题`：用于同项目、同业务、同机制、同案例家族的已有笔记。
- 不要默认写 `后续可延展`。
- 如果确实发现值得延展的新专题，不要直接写进 `文件引用` 当作已存在链接；应在最终回复里列为“建议拆分整理项”，等待用户确认后再创建。
- 如果某一类没有有意义链接，省略该小节，不要生成 `None captured` 空占位。
- 每条链接都要有一句短说明，说明为什么相关。

## 质量检查

写入或更新前确认：

- YAML metadata 完整，且没有 `links` 属性。
- `related_notes` 中的笔记都在 `文件引用` 中有关系说明。
- `related_notes` 不应在明显存在同主题、同目录或同项目笔记时留空；写入前应检索现有 vault 关系。
- `tags` 不包含纯数字、`note_type` 值、状态值或特殊符号标签。
- `Key takeaway` 是一句强结论 + 一段实用解释。
- `摘要` 恰好三条。
- `Context` 能快速说明来源、目标、状态和适用范围。
- 用户提供的微信或其他平台 URL 同时出现在 `Context` 和 `Key references`，并使用 Markdown 链接格式。
- 工作项目归档笔记正文足够完整，不需要重开原始文件才能理解核心内容。
- `后续可复用关键信息` 不重复来源路径或 URL。
- `Key references` 只包含外部证据、路径、URL、endpoint、页码或章节。
- `文件引用` 只包含 Obsidian 内部 wiki 链接，不默认生成 `后续可延展`。
- 不保留 `待关联`、`待补充`、`可后续关联`、`None captured` 这类占位链接；无法确认关系时省略该小节。
- 没有写入密钥、API key、cookie、token、auth code 或 bearer 值，除非用户明确要求。
- 中文标题和正文按 UTF-8 读取时显示正常。
