---
name: i-have-an-idea
description: >-
  Capture and co-develop a user's new product, feature, experience, architecture,
  or creative-workflow idea into one traceable, AI-friendly Markdown document
  without starting implementation. Use on explicit triggers such as "/idea",
  "我有一个想法", "我想做一个...", "I have an idea", and on high-confidence
  implicit new directions such as "要是...就好了" or "What if...". For an
  ambiguous feature-like statement, clarify whether the user wants idea
  exploration or immediate execution. Do not use for bugs, factual questions,
  mechanical edits, progress on an existing task, or implementation of an
  already-understood requirement.
---

# I Have an Idea

把用户尚未成熟但可能重要的想法接住，与用户共同发展，并维护为一份可追溯的 Markdown。保留用户作者权；提供 AI 的理解、反例、方案与落地转译能力，但不越权实施。

## 核心合同

- 一个独立想法只维护一份 living Markdown。
- 新文件默认位于 `docs/ideas/IDEA-YYYYMMDD-<slug>.md`。
- skill 的合法成果只有该 Markdown 的创建或更新，以及面向用户的简短对话。
- 不修改项目源码，不创建 Issue、任务、PRD、实施计划或原型，不运行构建、测试、部署，不调用实施 Agent。
- `status: shaped` 只表示想法已经成形；它永远不等于 `implementation_authorization: granted`。
- 未获作者明确授权时保持 `implementation_authorization: not-granted`。
- 作者授权后只更新文档、输出交接并终止本 skill；不得在本 skill 内开工。

## 1. 判定交互模式

按以下优先级判定：

1. **明确想法**：用户使用 `/idea`、`我有一个想法`、`I have an idea` 或同等明确表达。直接捕获，不询问是否创建文档。
2. **高置信度隐式想法**：用户提出新的、可长期发展的产品、体验、架构或创作方式，例如“要是……就好了”。先告诉用户“我先把这个想法接住了”，然后捕获。
3. **意图模糊**：一句话既可能是新想法，也可能是立即修改，例如“这里是不是应该加个导出按钮？”。只问：

   > 你是在提出一个值得继续发展的想法，还是希望我现在直接修改？

   在用户回答前不创建文档。
4. **明确执行**：Bug、机械修改、具体实现、事实问答或既有任务推进。不要触发本 skill。
5. **新想法与开工请求混合**：先运行本 skill，把想法形成文档；把明确的开工表达记录为授权。完成交接后终止本 skill，由其他工作流在其后读取文档。

禁止询问“要不要创建 Idea 文档”。安装并启用本 skill 即表示宿主已对这套想法记录工作流给出持续授权；若宿主项目另有明确规则，则服从宿主规则。真正需要澄清的是协作模式，不是文件操作。

## 2. Search-Before-Create

创建新文档前必须先检索：

1. 从用户表达提取主题、同义词、关键实体和可能标签。
2. 使用 `rg` 搜索现有 Markdown，范围依次为：
   - `docs/ideas/`
   - `docs/product/`
   - `docs/architecture/`
   - `docs/adr/`
3. 阅读最相关的候选文档，按语义而不是只按文件名判断。
4. 按以下规则处理：
   - 同一个想法：更新原想法文档。
   - 既有产品、架构或 ADR 文档已是明确事实源：更新该 Markdown，或从新想法文档链接它；不得复制一份竞争性结论。
   - 相关但边界不同：说明重叠点，询问继续原文档还是新建独立想法。
   - 无相关记录：创建新文档。
   - 无法确定是否重复：不要自动合并，先让作者裁决想法身份。

优先使用 `rg --files` 和 `rg -n -i --glob '*.md'`。目录不存在时跳过，不把缺少 `docs/ideas/` 当作错误。

## 3. 最小捕获

新建时使用 `assets/idea-record-template.md` 的结构，并完成所有占位内容。遵守以下规则：

- 使用本地日期和 ISO 8601 时间。
- 文件名使用 `IDEA-YYYYMMDD-<slug>.md`；slug 使用简短、稳定的 ASCII kebab-case。
- `id` 与文件名主体一致，首次创建后不改变。
- 若路径已存在，先判断是否重复；确认为不同想法后才添加最短数字后缀，绝不覆盖。
- 初始 `status` 使用 `captured`，`version` 使用 `0.1`，实施授权使用 `not-granted`。
- 原样保存决定想法方向的用户表达；不要把 AI 的释义混入引用。
- 在“当前形态”中只写最强初步理解，并明确尚未形成的部分。
- 将 AI 推断标记为“判断”或“假设”，不得伪装成用户决定或事实。
- 创建或更新完成后，把文档路径告诉用户，然后自然进入讨论。

只创建或更新这一份 Markdown。不要为了索引、摘要或任务管理再生成第二份成果文件。

## 4. 共同发展想法

每轮遵守以下顺序：

1. 先用用户视角复述这个想法为什么成立，证明已经理解原点。
2. 给出 AI 的实质贡献：补足结构、提出方案、指出取舍、提供反例或推荐。
3. 一次只聚焦一个最能改变方向的问题；不要用问卷审讯用户。
4. 能从项目文件获得的信息自行读取，不重复询问用户。
5. 显式区分作者意图、事实、判断、假设、决定和未决问题。
6. 每当出现新的作者意图、重要纠正、决定、边界或关键未知项时，更新同一文档：
   - 重写“当前形态”为最新简洁快照；
   - 在“演进、决定与边界”中追加来路；
   - 勾选、改写或新增未决问题；
   - 更新 `updated_at` 与版本记录。

不要为寒暄、措辞修饰或没有改变理解的重复内容机械更新文档。

## 5. 维护五区块文档

保持模板中的五个顶层区块及其语义：

1. **当前形态 / Current Shape**：一句话定义、核心价值、当前推荐。
2. **起因与作者原话 / Origin & Raw Intent**：原始表达与真实起因；关键原话只追加、不静默改写。
3. **演进、决定与边界 / Evolution, Decisions & Boundaries**：讨论来路、决定及理由、被放弃的方案、边界和非目标。
4. **未决问题与假设 / Open Questions & Assumptions**：尚待作者判断或证据验证的内容。
5. **版本记录 / Changelog**：只追加，说明理解、状态和决定发生了什么变化。

同步维护 Frontmatter 与顶部状态提示。当前形态可以重写；作者原话、历史决定和版本记录不得删除。旧决定被推翻时标为 `superseded` 并链接新决定，不伪造一次性共识。

## 6. 状态转移

- `captured`：已经保存原点，尚未进入实质探索。
- `exploring`：至少一次实质讨论已经改变或扩展理解。
- `shaped`：AI 已给出完整综合，并且作者通过“我同意”“就是这样”“差不多了”“可以收敛”等自然语言明确确认。
- `parked`：作者明确暂停，或继续所需条件尚不具备；记录暂停原因和重启条件。
- `superseded`：新想法或新决定明确取代本想法；保留双向引用。

AI 可以建议收敛，但不得自行把 `exploring` 改为 `shaped`。一般赞美、询问下一步或“听起来不错”不能自动视为开工授权。

## 7. 实施授权与交接

仅把无歧义的作者表达视为授权，例如：

- “开工”
- “开始实现这个想法”
- “授权做”
- 同一连续语境中含义完全等同的表达

获得授权后：

1. 将 `implementation_authorization` 更新为 `granted`。
2. 在演进与版本记录中保存作者原话、时间和授权范围。
3. 输出简短交接：想法 ID、文档绝对路径、当前形态、仍存在的未知项。
4. 明确说明本 skill 已结束，实施者必须先读取该 Markdown。
5. 立即停止；不要调用实现 skill、修改源码或运行实现命令。

授权只适用于被明确指向的那个想法，不得传播到其他想法或扩大范围。

## 8. 异常与纠正

- 作者纠正原意：保留旧表达，在演进中记录纠正，并更新当前形态。
- 作者完全换方向：保留旧历史；将新方向作为同一想法的大转向，除非作者确认它是独立想法。
- 自动捕获后作者说明“这不是想法”：将文档标为 `parked`，记录误分类原因，不进入探索。
- 发现重复文档：不要静默删除或合并；说明证据并让作者决定事实源。
- 对话中断：保持当前状态和未决问题，使下一位 AI 能从文档继续。

## 9. 面向用户的输出

保持简洁：说明更新了哪一份文档、当前 `status`、实施授权状态，以及本轮最值得继续讨论的一个问题。不要把整份文档重新粘贴到聊天中。
