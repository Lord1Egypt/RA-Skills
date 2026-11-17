---
name: obsidian-notes
description: 将当前对话、项目资料、会议记录、技术排障、工作流经验或主题讨论整理成结构化 Obsidian 知识库笔记。适用于用户要求总结、沉淀、保存、写入或整理 Obsidian 文档，并需要 Properties、Key takeaway、摘要、结构化内容块、Key references 和文件引用。
---

# Obsidian Notes

这个 skill 用于把对话或项目/主题上下文整理成长期可用的 Obsidian 笔记。笔记应当在数周后仍然可搜索、可阅读、可复用，并且能够和知识库中已有笔记形成清晰关系。

对于工作项目资料，笔记不是“来源指针”或“摘要卡片”。整理后的正文必须足够完整，让读者不需要重新打开原始文件，也能理解主要内容、关键机制、案例样本、数据口径和可复制启示。

## 核心流程

1. 识别笔记主题：项目、资料、议题、决策、工作流、配置、问题、复盘或可复用方法。
2. 判断笔记类型：
   - `agent-workflow`：Agent 行为、MCP/CLI/tool 设置、可重复工作流。
   - `project-note`：项目资料、项目背景、业务内容、阶段性沉淀。
   - `technical-note`：配置、命令、排障、架构、技术流程。
   - `decision-record`：已选择方向、被排除选项、依据和影响。
   - `reference-note`：长期参考知识、案例、方法或复用框架。
3. 当笔记属于业务/项目归档时，使用 `references/note-types.md` 判断领域模板，尤其是社群和会员运营、营销策划、商业运营、品牌活动、线上产品开发、案例研究和 MOC/索引类笔记。
4. 当输入来自微信文章、URL、PDF、DOCX、EXCEL、PPTX、本地文件、会议记录或已有 Obsidian 笔记时，使用 `references/source-types.md` 判断来源处理规则。
5. 选择存放目录。Agent 工作流和工具设置默认放入 `00-Agent(工作流沉淀）/`；业务资料、案例、报告、活动复盘和来源归档类笔记优先放入 `06-Archives(重要档案）/`，除非用户指定其他位置。
6. 使用 `references/note-template.md` 起草笔记。
7. 写入前应用 `references/style-guide.md` 的样式和质量要求。
8. 写入前检索同目录、同主题或同项目已有笔记，补齐 `related_notes` 和 `## 文件引用`。不要写 `待关联` 这类占位内容。
9. 写入前执行质量检查。
10. 如果可用 Obsidian MCP 或 Local REST API，优先写入并读回验证标题、Properties、`Key takeaway`、`摘要`、`后续可复用关键信息`、`Key references` 和 `文件引用` 是否存在。若不可用，则提供 Markdown 供手动写入。

## 必需笔记结构

每篇笔记必须包含：

- YAML Properties：包含创建信息、更新时间、来源、项目/主题、知识类型、状态、可信度、相关项目、相关笔记和 tags。不要使用 `links` 属性；URL、本地路径和外部证据统一放入 `Key references`。
- 一个具体的 H1 标题。
- `## Key takeaway`：Obsidian callout，包含一句最值得复用的结论，以及一小段解释为什么重要、何时适用、复用时不能忘记什么。
- `## 摘要`：Obsidian callout，固定三条短 bullet，便于快速浏览。
- `## Context`：Obsidian callout，简要说明背景、目标、当前状态、适用范围；如果用户提供了微信或其他平台 URL，必须在这里保留原始 URL。
- 主体内容块：
  - 工作项目归档笔记优先使用 `## 原始内容完整整理`、`## 机制 / 模式`、`## 案例 / 对比`、`## 可复制启示`。
  - 技术/工具/流程类笔记可使用更适合的结构，例如 `Key points`、`Workflow / Method`、配置表或验证清单。
- `## 后续可复用关键信息`：
  - 工作项目归档笔记：只放复用口径、模板沉淀、数据口径、机制抽象、适用条件和注意事项。
  - Agent/技术笔记：可放路径、命令、端点、配置键、验证方式和已知坑点。
  - 不要在这里重复原始文件路径、URL 或页码；这些统一放入 `Key references`。
- `## Key references`：唯一外部来源区，放用户提供 URL、原始文件路径、官方文档、API endpoint、页码/章节/发布时间等证据来源。临时抽取文本、HTML 抓取件、工作区副本只作为消化过程材料；笔记完成后默认不保留引用，除非它本身是长期可复核来源。
- `## 文件引用`：只放 Obsidian 内部 wiki 链接，表达与已有笔记的主要知识关系。

默认不要在工作项目归档笔记中加入 `## Next actions`。只有当笔记本身是行动计划、任务追踪，或用户明确要求后续行动时才加入。

默认不要在 `## 文件引用` 中加入 `后续可延展`。如果整理过程中发现值得拆成新专题的内容，应在最终回复中列为“建议拆分整理项”，等待用户确认后再创建新笔记。

## 写作规则

- 优先使用具体事实、路径、文件名、指标、机制、角色、决策和结论，避免泛泛总结。
- 保留关键本地路径、端口、工具名、文件名和用户提供链接。
- 表格优先用于数据、机制、对比、角色分工、配置矩阵、复用模板和检查清单。
- Mermaid 只在能明显压缩流程或关系时使用。
- 不写入密钥、API key、cookie、token、auth code 或 bearer 值，除非用户明确要求写入该敏感信息。
- 读写 Markdown 使用 UTF-8；Windows PowerShell 中读取含中文标题的文件时使用 `-Encoding UTF8`。
- 保持 `Key references` 和 `文件引用` 的边界：
  - 外部证据、URL、本地路径、页码、端点属于 `Key references`。
  - Obsidian 内部笔记关系属于 `文件引用`。
- 网页 URL 在 `Context` 和 `Key references` 中优先写成可点击 Markdown 链接，链接文字优先使用内容标题、页面标题、文档标题、仓库名或平台入口名，例如 `[我们一起奔赴热爱](https://...)`。只有无法确定标题时才使用 `[微信原文](https://...)` 或 `[来源链接](https://...)`。不要用反引号包裹网页 URL；Windows 本地路径、API endpoint、命令和文件名仍使用反引号。
- `tags` 只放稳定主题分类。不要把 `note_type`、年份、状态、带特殊符号的品牌写法放入 tags；例如不要写 `project-note`、`2022`、`樾+`、`樾⁺`、`社群+`。正文和标题可以保留正式品牌名，标签应转成稳定写法，例如 `樾生活方式`。
- 对微信文章、URL、PDF、DOCX、EXCEL、PPTX，要在 `Key references` 中保留来源身份、访问/保存时间、页码/章节/工作表/幻灯片等可追溯信息。
- 对 `06-Archives` 中的业务/项目归档笔记，不要写轻量指针笔记。必须提取并保留原始资料的主要内容：叙事主线、事实、数据、机制、案例、对比、决策和可复用启示。页码/slide 只是证据，不能替代正文。
- 写入已有笔记时，先读取现有内容，再尽量做定向修改。只有创建新笔记或经用户同意替换生成稿时，才进行整篇替换。
- 删除、移动、大范围替换等破坏性操作需要用户明确确认。

## 质量检查

写入或更新前，确认：

- YAML 包含 `created_at`、`updated_at`、`source`、`project`、`topic`、`note_type`、`knowledge_type`、`status`、`confidence`、`related_projects`、`related_notes` 和 `tags`。
- `tags` 不包含纯数字、`note_type` 值、状态值或特殊符号标签；年份应放标题、topic 或正文，类型应放 `note_type`。
- 写入业务/项目归档笔记前已检索现有知识库关系；`related_notes` 中的笔记必须在 `文件引用` 中解释，且不要保留 `待关联` 占位。
- `Key takeaway` 只有一句可复用结论和一段高密度解释，不凑字数。
- `摘要` 恰好三条 bullet，且不重复 Key takeaway 段落。
- `Context` 简洁说明背景、目标、状态和适用范围；用户提供的 URL 在这里可见。
- 用户提供的网页 URL 在 `Context` 和 `Key references` 中使用 Markdown 链接格式，确保可点击跳转。
- 工作项目归档笔记正文足够完整，读者无需重新打开原始文件即可理解核心内容。
- `后续可复用关键信息` 不重复来源路径或 URL，只保留复用口径、模板沉淀、数据口径、机制抽象、适用条件等内容。
- `Key references` 只包含外部证据、用户 URL、本地文件路径、repo 路径、API endpoint、页码或章节。
- `文件引用` 只包含有意义的 Obsidian 内部 wiki 链接，并说明关系；默认不写 `后续可延展`。
- 没有写入密钥、API key、cookie、token、auth code 或 bearer 值，除非用户明确要求。

## Obsidian 写入建议

如果 MCP 工具可用，优先顺序（这是日常笔记操作的推荐路径；插件开发调试场景在 Obsidian CLI 可用时改用 CLI）：

1. `vault_write`：创建新笔记。
2. `vault_read`：读回验证写入结果。
3. `vault_get_document_map`：修改已有笔记前获取结构。
4. `vault_patch`：定向修改标题、frontmatter 或指定 heading。
5. `vault_append`：仅在明确需要追加且不会重复时使用。

手动使用 Obsidian Local REST API with MCP 时：

- Streamable HTTP MCP endpoint 使用 `https://127.0.0.1:27124/mcp/`。
- JSON 请求使用无 BOM 的 UTF-8。
- Header 包含 `Authorization: Bearer <token>`、`Content-Type: application/json`、`Accept: application/json, text/event-stream`。
- 初始化后保留 `Mcp-Session-Id`，后续请求继续使用。

## 与其它 Skill 的协作

本 skill 是 Obsidian 知识库笔记的结构权威。加载本 skill 时，其它 Obsidian 相关 skill 只能作为语法、文件格式或调试能力补充，不能覆盖本 skill 对笔记结构、Properties、内容完整性和引用边界的要求。

### `obsidian-markdown`：Obsidian 语法手册

使用场景：需要写 embeds、注释 `%%`、LaTeX 数学、Mermaid 图表、脚注、block links 等 Obsidian 特有 Markdown 语法。

分工边界：

- 本 skill 定义笔记应该包含什么结构、哪些 Properties 字段、哪些 callout 样式、哪些内容质量要求。
- `obsidian-markdown` 只定义具体 Obsidian Markdown 语法怎么写。
- Properties 字段以本 skill 为准；默认不要因为 `obsidian-markdown` 的通用示例而新增 `title`、`date` 等字段。
- `aliases`、`cssclasses` 只有在用户明确要求、已有 vault 规范需要，或 Obsidian 视图确实依赖时才补充。
- Callout 规范以本 skill 为准；`obsidian-markdown` 的 callout 类型列表仅作语法参考。

### `obsidian-bases`：`.base` 视图

使用场景：创建或编辑 `.base` 文件，构建笔记的表格、卡片或列表视图。

分工边界：

- 本 skill 不定义 `.base` 文件格式；遇到 `.base` 文件创建或编辑时委托给 `obsidian-bases`。
- 本 skill 定义的 Properties 字段，例如 `note_type`、`project`、`topic`、`status`、`confidence`、`tags`，可作为 `.base` 的过滤、分组和排序字段。
- `.base` 视图不得反向改变本 skill 的 YAML 字段规范。

### `json-canvas`：`.canvas` 图谱

使用场景：创建或编辑 `.canvas` 文件，构建知识图谱、思维导图、流程图或项目关系图。

分工边界：

- 本 skill 不定义 `.canvas` 文件格式；遇到 Canvas 文件创建或编辑时委托给 `json-canvas`。
- Canvas 的 file node 可以指向本 skill 生成的笔记。
- 本 skill 负责保证被引用笔记的命名、结构和内部关系清晰；`json-canvas` 负责 Canvas JSON 结构正确。

### `obsidian-cli`：命令行与插件调试

使用场景：仅在 Obsidian CLI 可用，且任务涉及 MCP 不具备的能力时使用，例如插件热重载、截图验证、错误捕获、DOM/console 检查或版本对比。

日常 vault 读写、搜索和补丁仍优先使用 MCP。

| 场景 | 优先工具 |
|---|---|
| 日常笔记读写搜索 | MCP：`vault_read` / `vault_write` / `vault_patch` / search |
| 分段精准补丁 | MCP：`vault_patch` |
| 文档结构图 | MCP：`vault_get_document_map` |
| 复杂查询 | MCP 暴露的 search/query 能力；如不可用则退回检索和读取 |
| 插件热重载 | Obsidian CLI |
| 错误捕获 | Obsidian CLI |
| 截图验证 | Obsidian CLI |
| DOM / console 检查 | Obsidian CLI |
| 版本对比 | Obsidian CLI 或 Git，按任务场景选择 |

### `defuddle`：网页正文提取

使用场景：当用户提供普通网页 URL（文章、博客、在线文档、新闻稿）并要求读取、分析或整理为笔记时，优先用 `defuddle` 提取正文，再进行消化整理。

分工边界：

- `defuddle` 只负责“网页 → 干净正文”这一层（去除导航、广告、侧栏等杂物，输出 Markdown 或 JSON）；本 skill 负责消化整理、笔记结构、Properties、引用边界和质量检查。
- 提取产物属于消化过程材料：来源身份（URL、标题）按 `references/source-types.md` 的规则进入 `Context` 和 `Key references`；临时抽取文本默认不长期保留引用。
- 需要 JavaScript 渲染的页面、登录墙等提取失败场景，按 `defuddle` 技能自身文档处理（如浏览器工具兜底）；本 skill 不定义提取实现。

### `knap`：数据 → 笔记渲染

使用场景：当用户要求把 JSON/CSV 等结构化数据、或已提取的文本（如网页正文）按模板转成一条或多条 Markdown 笔记时（含批量生成），交给官方 `knap` 完成渲染。

分工边界：

- `knap` 只负责“数据 → Markdown 渲染”这一层：模板、过滤器、批量生成和管道衔接；本 skill 定义笔记应该包含什么结构、哪些 Properties 字段、哪些 callout 样式、哪些内容质量要求和引用边界。
- `knap` 渲染产物一律视为初稿：写入 vault 前，必须按 `references/note-template.md` 核对结构，并走本 skill 的质量检查和读回验证。
- frontmatter 字段集合以本 skill 为准；`knap` 的 `yaml_property` 等过滤器只是生成手段，不得反向增减字段或改变字段规范。
- `knap` 的模板语法、CLI 用法与版本以其官方 skill / 文档为准；本 skill 不定义模板语言。

## 参考文件

- 起草笔记前阅读 `references/note-template.md`。
- 判断样式、内容密度和可读性时阅读 `references/style-guide.md`。
- 判断业务领域模板时阅读 `references/note-types.md`。
- 判断来源处理规则时阅读 `references/source-types.md`。
